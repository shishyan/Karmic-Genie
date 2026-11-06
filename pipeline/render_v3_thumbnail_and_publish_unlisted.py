#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom 1920x1080 Thumbnail Renderer & UNLISTED-Only Release Publisher for:
  Karmic Genie Show — Season 1, Episode 1 (v3.1 Interactive Grand-Design Master)
  `renders/Karmic_Genie_Show_S01E01_v3_Interactive_16x9.mp4`

Safety, Philosophical & Release Guarantees:
  1. Hard assertion `assert body["status"]["privacyStatus"] == "unlisted"` — NEVER `public`!
  2. Strictly ZERO company names and ZERO real/fictional person names!
  3. Zero blame / zero "record profits" / zero "corporate greed": honors every industry,
     company, and city as a vital organ in Earth's Grand Design serving mind, soul, and para-soul,
     where career shifts act as minor hiccups relieving overdue family reunions & duties!
"""

import argparse
import json
import re
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
FILM_MP4 = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E01_v3_Interactive_16x9.mp4"
EP_DIR = REPO_DIR / "episodes" / "S01E01_Employees_vs_Tech_CEO"
THUMB_JPG = EP_DIR / "s01e01_v3_thumbnail_16x9.jpg"
MANIFEST_JSON = EP_DIR / "published_manifest.json"
SRC_STAGE_JPG = REPO_DIR / "assets" / "studio_v5_masters" / "v7_wide_wall_genie_16x9.jpg"
CRED_DIR = Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/credentials")

TITLE = "200,000 Cuts, 60,000 Buyouts & Why Every One Is a Blessing in Disguise | Karmic Genie Show (S1 E1)"

FORBIDDEN_NAMES = (
    "marcus", "arjun", "elena", "mateo", "kenji", "heinrich", "kavitha",
    "amazon", "google", "alphabet", "microsoft", "meta", "apple", "oracle",
    "dell", "cisco", "intel", "ups", "tcs", "infosys", "wipro", "hsbc", "citi",
)

FORBIDDEN_BLAME_PHRASES = (
    "record profit", "corporate greed", "heartless",
)

CHANNELS = {
    "karmicgenie": {
        "handle": "@karmicgenie",
        "expected_id": "UCmixCKV4uTv3wIp634IRLXg",
        "role": "PRIME",
        "token_candidates": [
            CRED_DIR / "tokens_karmicgenie" / "token_942198183044.json",
            CRED_DIR / "token_karmicgenie.json",
            CRED_DIR / "tokens_karmicgenie" / "token_472322435541.json",
        ],
    },
    "influenzian": {
        "handle": "@influenzian",
        "expected_id": "UCcJFqC7z0f-ARNcJadKiKpQ",
        "role": "SYNDICATION",
        "token_candidates": [
            CRED_DIR / "token_influenzian.json",
            CRED_DIR / "tokens_influenzian" / "token_942198183044.json",
        ],
    },
}

TAGS = [
    "Karmic Genie Show",
    "What does Genie say the 7D way",
    "The 7D Way",
    "Season 1 Episode 1",
    "Blessing in Disguise",
    "Grand Design Purpose",
    "Voluntary Buyout Bridge",
    "AI Era Renewal",
    "Family Reunion and Duty",
    "Single Thunderclap Parable",
    "Mind Soul Higher Purpose",
    "Duty Dignity Dharma Destiny",
]


def assert_editorial_purity(text: str, context: str):
    low = text.lower()
    for bad in FORBIDDEN_NAMES:
        if re.search(rf"\b{re.escape(bad)}\b", low):
            raise ValueError(f"Forbidden company/person name '{bad}' found in {context}!")
    for phrase in FORBIDDEN_BLAME_PHRASES:
        if phrase in low:
            raise ValueError(f"Forbidden blame phrase '{phrase}' found in {context}!")


def build_v3_thumbnail(out_jpg: Path = THUMB_JPG) -> Path:
    """
    Renders a high-contrast 1920x1080 custom YouTube thumbnail (< 2MB JPEG) compositing
    `v6_7d_saintly_genie_16x9.jpg` with dark-shaded headline text:
      - `200,000 CUTS • 60,000 BUYOUTS`
      - `BLESSING IN DISGUISE?`
    """
    if not SRC_STAGE_JPG.exists():
        raise FileNotFoundError(f"Missing master stage image: {SRC_STAGE_JPG}")

    im = Image.open(SRC_STAGE_JPG).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)

    for y in range(820, 1080):
        prog = (y - 820) / 260.0
        alpha = int(218 * (prog ** 1.15))
        d_ov.line([(0, y), (1920, y)], fill=(6, 8, 16, alpha))

    comp = Image.alpha_composite(im, overlay).convert("RGB")
    draw = ImageDraw.Draw(comp)

    f_line1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 68)
    f_line2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 82)

    line1_txt = "200,000 CUTS • 60,000 BUYOUTS"
    line2_txt = "BLESSING IN DISGUISE?"

    for t in (line1_txt, line2_txt):
        assert_editorial_purity(t, "thumbnail")

    w1 = draw.textbbox((0, 0), line1_txt, font=f_line1)[2]
    w2 = draw.textbbox((0, 0), line2_txt, font=f_line2)[2]
    x1 = (1920 - w1) // 2
    x2 = (1920 - w2) // 2

    draw.text((x1 + 3, 868 + 3), line1_txt, font=f_line1, fill=(0, 0, 0))
    draw.text((x1, 868), line1_txt, font=f_line1, fill=(255, 255, 255))

    draw.text((x2 + 3, 954 + 3), line2_txt, font=f_line2, fill=(0, 0, 0))
    draw.text((x2, 954), line2_txt, font=f_line2, fill=(255, 216, 112))

    out_jpg.parent.mkdir(parents=True, exist_ok=True)
    comp.save(out_jpg, format="JPEG", quality=88, optimize=True)
    size_bytes = out_jpg.stat().st_size
    assert size_bytes < 2_000_000, f"Thumbnail exceeds 2MB YouTube limit: {size_bytes} bytes"
    print(f"✅ Rendered v3 thumbnail: {out_jpg} ({size_bytes / 1024:.1f} KB < 2MB)", flush=True)
    return out_jpg


def build_interactive_description(handle: str) -> str:
    desc = (
        "Karmic Genie Show — Season 1, Episode 1 (v4.0 Interactive Broadcast)\n"
        "\"200,000 Cuts, 60,000 Buyouts & Why Every One Is a Blessing in Disguise\"\n"
        "Signature Question: \"What does Genie say — the 7D way?\"\n\n"
        "💬 JOIN OUR VIEWER CIRCLE IN THE COMMENTS:\n"
        "1) Share your industry or city below if someone in your circle experienced a career shift "
        "or Voluntary Buyout bridge since early 2025.\n"
        "2) Measure your current path against all Seven D's—does your life tick at least 4 of 7D "
        "(Stay the Course), or is it time to Change Your Route?\n\n"
        "Every industry, every company, and every city serves a vital purpose in Earth's Grand Design—"
        "like critical organs in a living body, and like highways built as pathways for travelers rather "
        "than final destinations. Spending fifty years merely earning to survive is like an overgrown "
        "forest yielding no fruit. Technology exists for connectedness; when workers disconnect from "
        "real home and family, this buyout wave acts like a natural market correction—unlocking golden "
        "handcuffs and bringing overdue family reunions and deeper life duties back within reach.\n\n"
        "Tonight we examine the 2025→2026 global shift metrics on our curved studio glass displays, "
        "open with a candid 3-part executive dialogue on both the breakthroughs and cautions of the AI "
        "era, hear three combined human stories from around the world, welcome a crisp one-phrase "
        "blessing from the Karmic Genie, and connect every dot along The 7D Way.\n\n"
        "✨ Live & Measure Every Question by The 7D Scorecard (Tick ≥ 4 of 7D):\n"
        "• 1. Respect Your DUTY First.\n"
        "• 2. Earn with DIGNITY Always.\n"
        "• 3. Practice Life DISCIPLINE.\n"
        "• 4. Uphold Karmic DHARMA.\n"
        "• 5. Raise Family with DEVOTION.\n"
        "• 6. Be Grateful to Your DIVINE.\n"
        "• 7. Purposeful Life Is Your DESTINY.\n\n"
        f"📺 Subscribe to {handle} and share your 7D reflection below!\n\n"
        "#KarmicGenieShow #The7DWay #BlessingInDisguise #GrandDesign #FutureOfWork "
        "#7DScorecard #FamilyDuty #Duty #Dignity #Destiny"
    )
    assert_editorial_purity(desc, "description")
    return desc


def upload_unlisted(channel_key: str, force: bool = False) -> dict:
    """
    Uploads `Karmic_Genie_Show_S01E01_v3_Interactive_16x9.mp4` strictly as `unlisted`
    to the specified channel (`karmicgenie` or `influenzian`) and sets the custom v4 thumbnail.
    """
    norm_key = channel_key.lstrip("@").strip().lower()
    if norm_key not in CHANNELS:
        raise ValueError(f"Unknown channel_key '{channel_key}'. Expected one of: {list(CHANNELS.keys())}")

    if not FILM_MP4.exists():
        raise FileNotFoundError(f"Missing rendered master MP4: {FILM_MP4}")

    if not THUMB_JPG.exists():
        build_v3_thumbnail(THUMB_JPG)

    assert len(TITLE) <= 100, f"YouTube title exceeds 100 chars ({len(TITLE)}): {TITLE}"
    assert_editorial_purity(TITLE, "title")
    for tg in TAGS:
        assert_editorial_purity(tg, "tags")

    ch_cfg = CHANNELS[norm_key]
    handle = ch_cfg["handle"]
    exp_id = ch_cfg["expected_id"]

    raw_manifest = {}
    if MANIFEST_JSON.exists():
        try:
            raw_manifest = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
        except Exception:
            raw_manifest = {}

    fname = FILM_MP4.name
    manifest_key = "Karmic_Genie_Show_S01E01_v4_Interactive_16x9.mp4"
    entry = raw_manifest.get(manifest_key, {
        "season": 1,
        "episode": 1,
        "version": "v4.0_seamless_wide_wall_curved_glass_unlisted",
        "source_file": fname,
        "format": "16:9 Seamless Wide-Wall Interactive Broadcast",
        "title": TITLE,
        "privacy": "unlisted",
        "channels": {},
    })

    if not force and handle in entry["channels"] and entry["channels"][handle].get("video_id"):
        print(f"✅ Already uploaded v4.0 (unlisted) on {handle}: {entry['channels'][handle]['watch_url']}", flush=True)
        return entry["channels"][handle]

    for tpath in ch_cfg["token_candidates"]:
        if not tpath.exists():
            continue
        try:
            creds = Credentials.from_authorized_user_file(str(tpath))
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                tpath.write_text(creds.to_json(), encoding="utf-8")

            yt = build("youtube", "v3", credentials=creds)
            items = yt.channels().list(part="snippet", mine=True).execute().get("items", [])
            if not items or items[0]["id"] != exp_id:
                print(f"  Skipping {tpath.name}: channel mismatch ({items[0]['id'] if items else 'none'} != {exp_id})")
                continue

            ch_title = items[0]["snippet"]["title"]
            body = {
                "snippet": {
                    "title": TITLE,
                    "description": build_interactive_description(handle),
                    "tags": TAGS,
                    "categoryId": "22",
                    "defaultLanguage": "en",
                    "defaultAudioLanguage": "en",
                },
                "status": {
                    "privacyStatus": "unlisted",
                    "selfDeclaredMadeForKids": False,
                },
            }
            # MANDATORY HARD SAFETY LOCK: NEVER PUBLIC!
            assert body["status"]["privacyStatus"] == "unlisted", "CRITICAL: privacyStatus MUST be 'unlisted'!"

            print(
                f"🚀 Uploading UNLISTED {fname} ({FILM_MP4.stat().st_size/1e6:.2f} MB) "
                f"to '{ch_title}' ({handle}) via {tpath.name}...",
                flush=True,
            )
            media = MediaFileUpload(str(FILM_MP4), mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
            req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
            resp = None
            while resp is None:
                _, resp = req.next_chunk()

            vid_id = resp["id"]
            watch_url = f"https://www.youtube.com/watch?v={vid_id}"
            print(f"🎉 UPLOADED UNLISTED ON {handle} ({ch_title}): {watch_url}", flush=True)

            try:
                yt.thumbnails().set(
                    videoId=vid_id,
                    media_body=MediaFileUpload(str(THUMB_JPG), mimetype="image/jpeg"),
                ).execute()
                print(f"   🖼️ Custom v3 thumbnail set on {vid_id}!", flush=True)
            except Exception as te:
                print(f"   ℹ️ Custom thumbnail skipped ({te})", flush=True)

            rec = {
                "role": ch_cfg["role"],
                "channel_id": exp_id,
                "channel_title": ch_title,
                "video_id": vid_id,
                "watch_url": watch_url,
                "privacyStatus": body["status"]["privacyStatus"],
                "token": str(tpath.relative_to(CRED_DIR)),
            }
            entry["channels"][handle] = rec
            raw_manifest[manifest_key] = entry
            MANIFEST_JSON.write_text(json.dumps(raw_manifest, indent=2, ensure_ascii=False), encoding="utf-8")
            return rec

        except HttpError as e:
            print(f"  ⚠️ HTTP error on {tpath.name} for {handle}: {e}", flush=True)
        except Exception as e:
            print(f"  ⚠️ Error on {tpath.name} for {handle}: {e}", flush=True)

    raise RuntimeError(f"❌ Failed to upload unlisted video on {handle}")


def main():
    parser = argparse.ArgumentParser(description="Render v4 custom thumbnail and publish S01E01 v4 strictly as UNLISTED.")
    parser.add_argument(
        "--thumbnail-only",
        action="store_true",
        help="Only render & verify `s01e01_v3_thumbnail_16x9.jpg` without uploading to YouTube.",
    )
    parser.add_argument(
        "--privacy",
        default="unlisted",
        choices=["unlisted"],
        help="Hard-locked to 'unlisted' (NEVER public).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force a fresh unlisted upload even if already present in manifest.",
    )
    parser.add_argument(
        "--channel",
        default="all",
        choices=["karmicgenie", "influenzian", "all"],
        help="Target channel key for unlisted upload (default: all).",
    )
    args = parser.parse_args()
    assert args.privacy == "unlisted", "CRITICAL: privacy MUST be 'unlisted'!"

    build_v3_thumbnail(THUMB_JPG)
    if args.thumbnail_only:
        return

    targets = ["karmicgenie", "influenzian"] if args.channel == "all" else [args.channel]
    for ch in targets:
        upload_unlisted(ch, force=args.force)


if __name__ == "__main__":
    main()
