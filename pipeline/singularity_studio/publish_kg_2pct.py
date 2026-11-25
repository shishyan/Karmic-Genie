#!/usr/bin/env python3
"""
Step 6: Export OpenReel v1.2.0 Project, Mirror Code/Manifest to Karmic-Genie-Show Repo,
Sync Deliverables to Google Drive (`gdrive:KarmicGenie/<ep_slug>/`) with
clickable `https://drive.google.com/...` URLs, and Upload UNLISTED to `@karmicgenie`.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

STUDIO_ROOT = Path("/home/shishyan/GitHub/Influenzian/Utility_Explainer_Studio")
TOKEN_CANDIDATES = [
    Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/credentials/token_karmicgenie.json"),
    Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/credentials/tokens_karmicgenie/token_942198183044.json"),
]


def run_cmd(cmd: list[str]) -> str:
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed ({res.returncode}): {' '.join(cmd)}\n{res.stderr}\n{res.stdout}")
    return res.stdout.strip()


def export_openreel(manifest: dict, ep_dir: Path, out_path: Path) -> None:
    compat = {
        "episodeId": manifest["episodeId"],
        "width": manifest["width"],
        "height": manifest["height"],
        "fps": manifest["fps"],
        "audioFile": manifest["audioFile"],
        "totalDurationSec": manifest["totalDurationSec"],
        "scenes": [
            {
                "chapterIndex": i,
                "chapterTitle": b.get("actTag") or b.get("overlayWidget") or b["id"],
                "heroMetric": b.get("actTag") or "",
                "accentColor": "amber",
                "startSec": b["startSec"],
                "durationSec": b["durationSec"],
                "narration": b.get("narration") or "Karmic Genie Show Closing Card",
                "citation": {"sourceName": "The Karmic Genie Show", "year": "2026", "sourceDetail": "ShishyanEN"},
            }
            for i, b in enumerate(manifest["beats"], start=1)
        ],
    }
    compat_path = ep_dir / "_openreel_compat.json"
    compat_path.write_text(json.dumps(compat, indent=2), encoding="utf-8")
    run_cmd(["node", str(STUDIO_ROOT / "scripts" / "export_openreel_project.mjs"), str(compat_path), str(out_path)])
    compat_path.unlink(missing_ok=True)


def sync_to_drive(files: list[Path], drive_folder: str) -> dict[str, str]:
    urls: dict[str, str] = {}
    run_cmd(["rclone", "mkdir", drive_folder])
    for fp in files:
        if not fp.exists():
            continue
        run_cmd(["rclone", "copy", str(fp), drive_folder])
        link = run_cmd(["rclone", "link", f"{drive_folder}/{fp.name}"])
        urls[fp.name] = link
        print(f"[Drive OK] {fp.name} ({fp.stat().st_size / (1024*1024):.2f} MB) -> {link}", flush=True)
    return urls


def upload_unlisted_karmicgenie(mp4_path: Path, thumb_path: Path, manifest: dict, ep_slug: str) -> str | None:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    creds = None
    active_tp = None
    for tp in TOKEN_CANDIDATES:
        if not tp.exists():
            continue
        try:
            c = Credentials.from_authorized_user_file(str(tp))
            if c.expired and c.refresh_token:
                c.refresh(Request())
                tp.write_text(c.to_json(), encoding="utf-8")
            creds = c
            active_tp = tp
            break
        except Exception:
            continue
    if creds is None:
        print("[YouTube Warning] No valid OAuth token found in TOKEN_CANDIDATES", flush=True)
        return None

    yt = build("youtube", "v3", credentials=creds)
    ch_resp = yt.channels().list(part="snippet", mine=True).execute()
    items = ch_resp.get("items") or []
    ch_id = items[0]["id"] if items else ""
    if ch_id != "UCmixCKV4uTv3wIp634IRLXg":
        raise RuntimeError(f"SAFETY ABORT: Unexpected YouTube channel {ch_id}, expected UCmixCKV4uTv3wIp634IRLXg (@karmicgenie)")

    from karmicgenie_seo import get_episode_seo_package
    seo_pkg = get_episode_seo_package(ep_slug)
    title = seo_pkg["title"]
    description = seo_pkg["description"]
    cat_id = seo_pkg.get("categoryId", "28" if ("Singularity" in ep_slug or ep_slug.startswith("KG_Year_")) else "27")

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": seo_pkg["tags"],
            "categoryId": cat_id,
            "defaultLanguage": "en",
        },
        "status": {
            "privacyStatus": "unlisted",
            "selfDeclaredMadeForKids": False,
        },
    }
    assert body["status"]["privacyStatus"] == "unlisted"

    print(f"[YouTube] Uploading UNLISTED to @karmicgenie ({ch_id})...", flush=True)
    req = yt.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(str(mp4_path), chunksize=8 * 1024 * 1024, resumable=True),
    )
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"  Upload {int(status.progress() * 100)}%", flush=True)
    vid = resp["id"]
    print(f"[YouTube UNLISTED Live] https://youtu.be/{vid}", flush=True)

    if thumb_path.exists():
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(thumb_path))).execute()
            print(f"[Thumbnail OK] Custom 16:9 thumbnail applied to {vid}", flush=True)
        except Exception as exc:
            print(f"[Thumbnail Notice] Non-fatal error setting thumbnail (video already uploaded): {exc}", flush=True)

    return vid


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep-slug", default="KG_Creator_Dharma_2Percent")
    args = ap.parse_args()

    ep_slug = args.ep_slug
    ep_dir = STUDIO_ROOT / "episodes" / "karmic_genie" / ep_slug
    kg_repo_ep_dir = Path(f"/home/shishyan/GitHub/Karmic-Genie-Show/episodes/{ep_slug}")
    drive_folder = f"gdrive:KarmicGenie/{ep_slug}"

    mp4_path = ep_dir / f"{ep_slug}_1080p.mp4"
    thumb_path = ep_dir / "thumbnail_16x9.jpg"
    audio_path = ep_dir / f"{ep_slug}_ShishyanEN_Master.mp3"
    manifest_path = ep_dir / "manifest.json"
    openreel_path = ep_dir / f"{ep_slug}.openreel.json"

    assert mp4_path.exists(), f"Missing rendered MP4: {mp4_path}"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    # 1. OpenReel export
    export_openreel(manifest, ep_dir, openreel_path)

    # 2. Mirror text/JSON to Karmic-Genie-Show repo (no binaries!)
    kg_repo_ep_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(manifest_path, kg_repo_ep_dir / "manifest.json")
    script_md = kg_repo_ep_dir / f"{ep_slug}_Script.md"
    lines = [f"# {manifest['title']} — {manifest['show']}\n"]
    for b in manifest["beats"]:
        if b.get("narration"):
            lines.append(f"## {b['id']} ({b['startSec']:.2f}s – {b['startSec'] + b['durationSec']:.2f}s)\n{b['narration']}\n")
    script_md.write_text("\n".join(lines), encoding="utf-8")

    # 3. Google Drive sync
    drive_urls = sync_to_drive([mp4_path, thumb_path, audio_path, openreel_path, manifest_path, script_md], drive_folder)

    # 4. Upload UNLISTED to @karmicgenie
    yt_id = None
    yt_error = None
    try:
        yt_id = upload_unlisted_karmicgenie(mp4_path, thumb_path, manifest, ep_slug)
    except Exception as exc:
        yt_error = str(exc)
        print(f"[YouTube Error] {yt_error}", flush=True)

    result = {
        "episodeId": manifest["episodeId"],
        "youtubeVideoId": yt_id,
        "youtubeUrl": f"https://youtu.be/{yt_id}" if yt_id else None,
        "youtubeError": yt_error,
        "privacyStatus": "unlisted" if yt_id else None,
        "driveLinks": drive_urls,
    }
    (ep_dir / "delivery_links.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
