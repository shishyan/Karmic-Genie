#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom 1920x1080 Dual-@Me Pilot Thumbnail Renderer & UNLISTED-Only Release Publisher for:
  Karmic Genie Show — Season 1, Episode 0 (Pilot: "The 7D Way — Pioneers of the New World")
  `renders/Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_360p.mp4` (mirrored to `..._16x9.mp4`)

Safety, Philosophical & Release Guarantees:
  1. Hard assertion `assert body["status"]["privacyStatus"] == "unlisted"` — NEVER `public`!
  2. Strictly ZERO company names, ZERO real/fictional person names, and ZERO blame!
  3. Dual-@Me Key Art: Composites `v8_pilot_7d_scorecard_stage_16x9.jpg` with BOTH the Adult
     Narrator `@Me` in his ivory-white bandhgala (`v9_host_adult_ivory_bandhgala_16x9.jpg`) AND
     the approved Sample 2 `4-Year-Old Bala-Rishi @Me` + ornate golden Genie lamp
     (`v9_genie_4yo_bala_rishi_16x9.jpg`), with ZERO top dark rectangular boxes!
"""

import argparse
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
FILM_360P_MP4 = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_360p.mp4"
FILM_16X9_MP4 = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_16x9.mp4"
PILOT_DIR = REPO_DIR / "episodes" / "S01E00_Pilot_The_7D_Way"
THUMB_JPG = PILOT_DIR / "s01e00_pilot_thumbnail_16x9.jpg"
MANIFEST_JSON = PILOT_DIR / "published_manifest.json"

MASTERS_DIR = REPO_DIR / "assets" / "studio_v5_masters"
STAGE_V8_JPG = MASTERS_DIR / "v8_pilot_7d_scorecard_stage_16x9.jpg"
HOST_ADULT_JPG = MASTERS_DIR / "v9_host_adult_ivory_bandhgala_16x9.jpg"
GENIE_BALA_JPG = MASTERS_DIR / "v9_genie_4yo_bala_rishi_16x9.jpg"
CRED_DIR = Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/credentials")

TITLE = "The 7D Way: 7 Great Virtues & The 35/70 Conscience Test | Karmic Genie Show (Pilot S1 E0)"

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
    "The 7D Way",
    "What does Genie say the 7D way",
    "7D Scorecard",
    "Voice of Conscience",
    "Pioneers of the New World",
    "Duty Dignity Discipline",
    "Dharma Devotion Divine Destiny",
    "Bala Rishi Wisdom",
    "Spiritual Self Audit",
    "Body Mind Soul Para-Soul",
    "Pilot Episode",
]


def assert_editorial_purity(text: str, context: str):
    low = text.lower()
    for bad in FORBIDDEN_NAMES:
        if re.search(rf"\b{re.escape(bad)}\b", low):
            raise ValueError(f"Forbidden company/person name '{bad}' found in {context}!")
    for phrase in FORBIDDEN_BLAME_PHRASES:
        if phrase in low:
            raise ValueError(f"Forbidden blame phrase '{phrase}' found in {context}!")


def build_pilot_thumbnail(out_jpg: Path = THUMB_JPG) -> Path:
    """
    Renders a luminous 1920x1080 Dual-@Me custom YouTube thumbnail (< 2MB JPEG) compositing:
      - `v8_pilot_7d_scorecard_stage_16x9.jpg` (wide arena + `1–10 / <35` curved glass barriers)
      - Left-Center: Adult Narrator `@Me` in ivory-white bandhgala (`v9_host_adult_ivory_bandhgala_16x9.jpg`)
      - Center & Right-Center: Ornate Golden Genie Lamp + `4-Year-Old Bala-Rishi @Me` with topknot,
        sacred tilak, rudraksha mala, and golden-saffron stole (`v9_genie_4yo_bala_rishi_16x9.jpg`)
      - Clean bottom gradient + high-contrast 7D headline (ZERO top dark boxes!).
    """
    for req in (STAGE_V8_JPG, HOST_ADULT_JPG, GENIE_BALA_JPG):
        if not req.exists():
            raise FileNotFoundError(f"Missing master image for Dual-@Me thumbnail: {req}")

    bg = Image.open(STAGE_V8_JPG).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)

    # Cleanly remove the tiny distant center-stage figure (`x=912..1018, y=506..650`) on `v8` stage
    # while keeping the `Karmic Genie Show` wall emblem above `y=505` 100% untouched!
    clean_patch = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    cpd = ImageDraw.Draw(clean_patch)
    cpd.ellipse([882, 502, 1048, 710], fill=(231, 229, 224, 255))
    clean_patch = clean_patch.filter(ImageFilter.GaussianBlur(radius=10))
    bg = Image.alpha_composite(bg, clean_patch)

    adult_full = Image.open(HOST_ADULT_JPG).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
    adult_full = ImageEnhance.Brightness(adult_full).enhance(1.06)
    adult_full = ImageEnhance.Contrast(adult_full).enhance(1.06)
    adult_full = ImageEnhance.Sharpness(adult_full).enhance(1.22)

    bala_full = Image.open(GENIE_BALA_JPG).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
    bala_full = ImageEnhance.Contrast(bala_full).enhance(1.05)

    # Warm golden-saffron stage aura uniting Adult @Me, Golden Genie Lamp & 4-Year-Old Bala-Rishi @Me
    aura = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    ad = ImageDraw.Draw(aura)
    ad.ellipse([480, 175, 1460, 815], fill=(255, 226, 152, 76))
    aura = aura.filter(ImageFilter.GaussianBlur(radius=44))
    comp_rgba = Image.alpha_composite(bg, aura)

    # 1. Left-Center: Adult Narrator @Me in tailored ivory-white bandhgala
    adult_crop = adult_full.crop((540, 85, 1360, 1065))  # 820x980
    aw, ah = 500, 598
    adult_scaled = adult_crop.resize((aw, ah), Image.Resampling.LANCZOS)
    amask = Image.new("L", (aw, ah), 0)
    amd = ImageDraw.Draw(amask)
    amd.ellipse([172, 10, 330, 260], fill=255)  # Tight head & hair contour (zero dark wall halo)
    amd.polygon([
        (196, 218), (306, 218),
        (444, 294), (470, 578),
        (30, 578), (56, 294),
    ], fill=255)  # Tight ivory bandhgala shoulders & sleeves
    amask = amask.filter(ImageFilter.GaussianBlur(radius=10))
    adult_layer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    adult_layer.paste(adult_scaled, (445, 205), amask)
    comp_rgba = Image.alpha_composite(comp_rgba, adult_layer)

    # 2. Center + Right-Center: Ornate Golden Genie Lamp + 4-Year-Old Bala-Rishi @Me
    bala_crop = bala_full.crop((260, 50, 1510, 1075))  # 1250x1025
    bw, bh = 770, 632
    bala_scaled = bala_crop.resize((bw, bh), Image.Resampling.LANCZOS)
    bmask = Image.new("L", (bw, bh), 0)
    bmd = ImageDraw.Draw(bmask)
    bmd.ellipse([34, 442, 288, 616], fill=255)   # Tight ornate golden Genie lamp in center foreground
    bmd.ellipse([352, 8, 604, 326], fill=255)    # Tight 4yo Bala-Rishi topknot, tilak & smiling face
    bmd.polygon([
        (385, 268), (576, 268),
        (715, 366), (738, 616),
        (298, 616), (322, 366),
    ], fill=255)  # Ivory silk kurta, rudraksha mala & golden-saffron stole
    bmask = bmask.filter(ImageFilter.GaussianBlur(radius=11))
    bala_layer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    bala_layer.paste(bala_scaled, (735, 205), bmask)
    comp_rgba = Image.alpha_composite(comp_rgba, bala_layer)

    # Soft bottom vignette for crystal-clear headline below the curved glass barriers (y >= 808)
    grad = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for y in range(805, 1080):
        prog = (y - 805) / 275.0
        alpha = int(228 * (prog ** 1.12))
        gd.line([(0, y), (1920, y)], fill=(6, 8, 18, alpha))

    comp = Image.alpha_composite(comp_rgba, grad).convert("RGB")
    draw = ImageDraw.Draw(comp)

    f_line1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 62)
    f_line2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 78)

    line1_txt = "THE 7D WAY • SCORE ALL 7 VIRTUES / 70"
    line2_txt = "BELOW 35? CHANGE YOUR COURSE!"

    for t in (line1_txt, line2_txt):
        assert_editorial_purity(t, "pilot_thumbnail")

    w1 = draw.textbbox((0, 0), line1_txt, font=f_line1)[2]
    w2 = draw.textbbox((0, 0), line2_txt, font=f_line2)[2]
    x1 = (1920 - w1) // 2
    x2 = (1920 - w2) // 2

    draw.text((x1 + 3, 868 + 3), line1_txt, font=f_line1, fill=(0, 0, 0))
    draw.text((x1, 868), line1_txt, font=f_line1, fill=(255, 255, 255))

    draw.text((x2 + 3, 952 + 3), line2_txt, font=f_line2, fill=(0, 0, 0))
    draw.text((x2, 952), line2_txt, font=f_line2, fill=(255, 216, 112))

    out_jpg.parent.mkdir(parents=True, exist_ok=True)
    comp.save(out_jpg, format="JPEG", quality=89, optimize=True)
    size_bytes = out_jpg.stat().st_size
    assert size_bytes < 2_000_000, f"Thumbnail exceeds 2MB YouTube limit: {size_bytes} bytes"
    print(f"✅ Rendered Dual-@Me Pilot S01E00 thumbnail: {out_jpg} ({size_bytes / 1024:.1f} KB < 2MB)", flush=True)
    return out_jpg


def build_pilot_description(handle: str) -> str:
    desc = (
        "Karmic Genie Show — Pilot Episode (Season 1, Episode 0)\n"
        "\"The 7D Way: 7 Great Virtues to Become a Pioneer of the New World\"\n"
        "Signature Question: \"What does Genie say — the 7D way?\"\n\n"
        "🧭 TAKE YOUR 7D LIFE AUDIT TONIGHT (SCORE 1–10 PER VIRTUE, MAX 70):\n"
        "• Total Score below 35 / 70 (Red Zone — Conscience Silenced): Change the course of your life!\n"
        "• Total Score 35–49 / 70 (Amber Zone — Awakening Traveler): Realign neglected dimensions.\n"
        "• Total Score 50–70 / 70 (Gold Zone — Pioneer of the New World): Bear fruit & shade for all.\n\n"
        "No soul came to Earth merely to earn money for fifty years, survive, and depart—like an "
        "overgrown forest yielding neither fruit nor flower. In this foundational Pilot Episode of "
        "Karmic Genie Show, our Host explains the real-life philosophy and conscience tests behind "
        "every dimension, while the Awakened Bala-Rishi Karmic Genie delivers the luminous child-sage "
        "essence of all seven timeless virtues:\n\n"
        "1️⃣ DUTY (1–10) — Respect Your DUTY First: Duty is never your office job; Duty is what grows "
        "your soul—the task that triggers guilt in your conscience when left undone. Silence that "
        "conscience with intoxicants or neglect, and our world loses empathy and compassion.\n"
        "2️⃣ DIGNITY (1–10) — Earn with DIGNITY Always: Unbought self-respect and honest value.\n"
        "3️⃣ DISCIPLINE (1–10) — Practice Life DISCIPLINE: Sovereign mastery over your senses, sleep, "
        "and clock so cravings never enslave your mind.\n"
        "4️⃣ DHARMA (1–10) — Uphold Karmic DHARMA: Living as a vital organ in Earth's body, like a "
        "fruit-bearing banyan and mango tree sharing shade and nourishment with all.\n"
        "5️⃣ DEVOTION (1–10) — Raise Family with DEVOTION: Giving aging parents, spouse, and children "
        "your warm, undivided presence today—never exhausted leftovers.\n"
        "6️⃣ DIVINE (1–10) — Be Grateful to Your DIVINE: Daily humility before the Grand Architect of "
        "body, mind, soul, and para-soul.\n"
        "7️⃣ DESTINY (1–10) — Purposeful Life Is Your DESTINY: Aligning above 35 / 70 to flower into a "
        "compassionate Pioneer of the New World.\n\n"
        f"💬 Share your 7D Total Score (/70) in the comments and subscribe to {handle}!\n\n"
        "#KarmicGenieShow #The7DWay #7DScorecard #VoiceOfConscience #PioneersOfTheNewWorld "
        "#Duty #Dignity #Discipline #Dharma #Devotion #Divine #Destiny"
    )
    assert_editorial_purity(desc, "pilot_description")
    return desc


def upload_unlisted(channel_key: str, video_path: Path | None = None, force: bool = False) -> dict:
    """
    Uploads the rendered Pilot MP4 (`Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_360p.mp4` or `_16x9.mp4`)
    strictly as `unlisted` to `karmicgenie` or `influenzian` and attaches `s01e00_pilot_thumbnail_16x9.jpg`.
    """
    norm_key = channel_key.lstrip("@").strip().lower()
    if norm_key not in CHANNELS:
        raise ValueError(f"Unknown channel_key '{channel_key}'. Expected one of: {list(CHANNELS.keys())}")

    film_mp4 = video_path or (FILM_360P_MP4 if FILM_360P_MP4.exists() else FILM_16X9_MP4)
    if not film_mp4.exists():
        raise FileNotFoundError(f"Missing rendered Pilot MP4: {film_mp4}")

    if not THUMB_JPG.exists():
        build_pilot_thumbnail(THUMB_JPG)

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

    fname = film_mp4.name
    manifest_key = "Karmic_Genie_Show_S01E00_Pilot_BalaRishi_360p_Unlisted"
    entry = raw_manifest.get(manifest_key, {
        "season": 1,
        "episode": 0,
        "version": "v2.0_4yo_bala_rishi_dual_me_360p_unlisted",
        "source_file": fname,
        "format": "16:9 Widescreen 360p Preview Master",
        "title": TITLE,
        "privacy": "unlisted",
        "channels": {},
    })

    if not force and handle in entry["channels"] and entry["channels"][handle].get("video_id"):
        print(f"✅ Already uploaded Pilot S01E00 (unlisted) on {handle}: {entry['channels'][handle]['watch_url']}", flush=True)
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
                    "description": build_pilot_description(handle),
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
                f"🚀 Uploading UNLISTED Pilot {fname} ({film_mp4.stat().st_size/1e6:.2f} MB) "
                f"to '{ch_title}' ({handle}) via {tpath.name}...",
                flush=True,
            )
            media = MediaFileUpload(str(film_mp4), mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
            req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
            resp = None
            while resp is None:
                _, resp = req.next_chunk()

            vid_id = resp["id"]
            watch_url = f"https://www.youtube.com/watch?v={vid_id}"
            print(f"🎉 UPLOADED PILOT UNLISTED ON {handle} ({ch_title}): {watch_url}", flush=True)

            try:
                yt.thumbnails().set(
                    videoId=vid_id,
                    media_body=MediaFileUpload(str(THUMB_JPG), mimetype="image/jpeg"),
                ).execute()
                print(f"   🖼️ Custom Dual-@Me Pilot thumbnail set on {vid_id}!", flush=True)
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
            MANIFEST_JSON.parent.mkdir(parents=True, exist_ok=True)
            MANIFEST_JSON.write_text(json.dumps(raw_manifest, indent=2, ensure_ascii=False), encoding="utf-8")
            return rec

        except HttpError as e:
            print(f"  ⚠️ HTTP error on {tpath.name} for {handle}: {e}", flush=True)
        except Exception as e:
            print(f"  ⚠️ Error on {tpath.name} for {handle}: {e}", flush=True)

    raise RuntimeError(f"❌ Failed to upload unlisted Pilot video on {handle}")


def main():
    parser = argparse.ArgumentParser(description="Render S01E00 Dual-@Me Pilot thumbnail and publish strictly as UNLISTED.")
    parser.add_argument(
        "--thumbnail-only",
        action="store_true",
        help="Only render & verify `s01e00_pilot_thumbnail_16x9.jpg` without uploading to YouTube.",
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
        default="karmicgenie",
        choices=["karmicgenie", "influenzian", "all"],
        help="Target channel key for unlisted upload (default: karmicgenie).",
    )
    parser.add_argument(
        "--video",
        default=None,
        help="Optional explicit MP4 path to upload (defaults to 360p master if present).",
    )
    args = parser.parse_args()
    assert args.privacy == "unlisted", "CRITICAL: privacy MUST be 'unlisted'!"

    build_pilot_thumbnail(THUMB_JPG)
    if args.thumbnail_only:
        return

    vid_p = Path(args.video) if args.video else None
    targets = ["karmicgenie", "influenzian"] if args.channel == "all" else [args.channel]
    for ch in targets:
        upload_unlisted(ch, video_path=vid_p, force=args.force)


if __name__ == "__main__":
    main()
