#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publishes the Season 1, Episode 1 Full ~7-Minute Widescreen Film:
  renders/Karmic_Genie_Show_S01E01_Full_Film_16x9.mp4
to:
  1) PRIME CHANNEL: `@karmicgenie` ("Karmic Genie Show", ID: `UCmixCKV4uTv3wIp634IRLXg`)
  2) SYNDICATION CHANNEL: `@influenzian` ("Influenzian", ID: `UCcJFqC7z0f-ARNcJadKiKpQ`)
Also sets the custom 1920x1080 broadcast thumbnail (if channel custom-thumbnails enabled)
and records live URLs in `episodes/S01E01_Employees_vs_Tech_CEO/published_manifest.json`.
"""

import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
FILM_MP4 = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E01_Full_Film_16x9.mp4"
THUMB_JPG = REPO_DIR / "episodes" / "S01E01_Employees_vs_Tech_CEO" / "s01e01_youtube_thumbnail_16x9.jpg"
MANIFEST_JSON = REPO_DIR / "episodes" / "S01E01_Employees_vs_Tech_CEO" / "published_manifest.json"
SRC_STAGE_JPG = REPO_DIR / "assets" / "studio_v5_masters" / "v6_7d_saintly_genie_16x9.jpg"
CRED_DIR = Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/credentials")

TITLE = "Non-AI Teams, $720B CapEx & The 2030 Clock | What Does Genie Say — The 7D Way? (S1 E1)"

CHANNELS = [
    {
        "handle": "@karmicgenie",
        "expected_id": "UCmixCKV4uTv3wIp634IRLXg",
        "role": "PRIME",
        "token_candidates": [
            CRED_DIR / "tokens_karmicgenie" / "token_942198183044.json",
            CRED_DIR / "token_karmicgenie.json",
            CRED_DIR / "tokens_karmicgenie" / "token_472322435541.json",
        ],
    },
    {
        "handle": "@influenzian",
        "expected_id": "UCcJFqC7z0f-ARNcJadKiKpQ",
        "role": "SYNDICATION",
        "token_candidates": [
            CRED_DIR / "token_influenzian.json",
            CRED_DIR / "tokens_influenzian" / "token_942198183044.json",
        ],
    },
]


def build_thumbnail():
    im = Image.open(SRC_STAGE_JPG).convert("RGBA").resize((1920, 1080), Image.Resampling.LANCZOS)
    grad = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d_g = ImageDraw.Draw(grad)
    # Subtle bottom dark gradient for clean broadcast title legibility (< 1.8 MB JPEG for YouTube API)
    for y in range(760, 1080):
        alpha = int(215 * ((y - 760) / 320.0) ** 1.2)
        d_g.line([(0, y), (1920, y)], fill=(10, 12, 22, alpha))
    d_g.rounded_rectangle([58, 42, 468, 98], radius=12, fill=(18, 22, 36, 210), outline=(232, 195, 110, 220), width=2)

    out = Image.alpha_composite(im, grad).convert("RGB")
    draw = ImageDraw.Draw(out)
    f_badge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    f_main = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 62)
    f_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)

    draw.text((82, 54), "SEASON 1  •  EPISODE 1", font=f_badge, fill=(242, 206, 122))
    t1 = "NON-AI TEAMS & THE $720B SHIFT"
    t2 = "\"What does Genie say — the 7D way?\""
    w1 = draw.textbbox((0, 0), t1, font=f_main)[2]
    w2 = draw.textbbox((0, 0), t2, font=f_sub)[2]
    draw.text(((1920 - w1) // 2, 905), t1, font=f_main, fill=(255, 255, 255))
    draw.text(((1920 - w2) // 2, 988), t2, font=f_sub, fill=(245, 212, 130))

    out.save(THUMB_JPG, quality=88, optimize=True)
    print(f"✅ Thumbnail ready: {THUMB_JPG} ({THUMB_JPG.stat().st_size/1e3:.0f} KB)")


def build_description(handle: str) -> str:
    return (
        "Karmic Genie Show — Season 1, Episode 1 (Full Film)\n"
        "\"Seven Chairs Around One Fire: Non-AI Teams, Hyperscaler Billions & The 2030 Clock\"\n"
        "Signature Question: \"What does Genie say — the 7D way?\"\n\n"
        "Between early 2025 and late 2026, combined annual AI & Cloud CapEx across the four largest "
        "hyperscalers surged from ~$410B to $720B–$760B ($201.9B in Q3 2026 alone), while over 325,900 "
        "US tech roles were eliminated—falling almost entirely on non-cloud, non-AI divisions (consumer "
        "devices, core retail tech, traditional on-prem hardware, HR/internal ops, flattened small-team "
        "middle management, and entry-level developer funnels).\n\n"
        "Tonight, seven voices across seven cities—San Francisco, Seattle/Mysuru, London, São Paulo, "
        "Tokyo, Munich, and Coimbatore—share what happened at home without debate. Then we quiet the hall "
        "and invite the Karmic Genie to offer open-ended reflections along The 7D Way (inspired in passing "
        "by the two-minute Brihadaranyaka Upanishad parable of the 'Single Thunderclap'—worth reading quietly "
        "at home).\n\n"
        "⏳ Episode Chapters:\n"
        "00:00 — The 7D Way Title Sting & Global Timeline (2025 → Today)\n"
        "01:15 — San Francisco ($201.9B Quarter) & Seattle/Mysuru (The Overseas $-Chase)\n"
        "02:03 — London (Flattened Management) & São Paulo (The 7% Grad Funnel)\n"
        "02:32 — Tokyo (Midnight Non-AI Freeze), Munich (Dignity at 58) & Coimbatore\n"
        "03:30 — \"What does Genie say — the 7D way?\" & Lamp Awakening\n"
        "04:08 — The Wise Saint's Open Mirror (Upanishad 'Single Thunderclap' Hook)\n"
        "05:08 — A Blessing in Disguise & The 7D Way Reflections\n"
        "06:10 — One Quiet Question for 2036 & Official 7D Finale\n\n"
        "✨ Governed by The 7D Way:\n"
        "• Respect Your DUTY First.\n"
        "• Earn with DIGNITY Always.\n"
        "• Practice Life DISCIPLINE.\n"
        "• Uphold Karmic DHARMA.\n"
        "• Raise Family with DEVOTION.\n"
        "• Be Grateful to Your DIVINE.\n"
        "• Purposeful Life Is Your DESTINY.\n\n"
        f"📺 Subscribe to {handle} for Season 1 of Karmic Genie Show.\n\n"
        "#KarmicGenieShow #The7DWay #Season1Episode1 #TechLayoffs #FutureOfWork #AI #NonAITeams #WorkLifeBalance #Dharma #Duty"
    )


TAGS = [
    "Karmic Genie Show",
    "What does Genie say the 7D way",
    "The 7D Way",
    "Season 1 Episode 1",
    "Tech Layoffs 2026",
    "Hyperscaler CapEx",
    "Non AI Teams",
    "Future of Work",
    "Overseas Workers Family Duty",
    "Blessing in Disguise",
    "Brihadaranyaka Upanishad Single Thunderclap",
    "Duty Dharma Destiny",
]


def main():
    if not FILM_MP4.exists():
        raise FileNotFoundError(f"Missing {FILM_MP4}")

    build_thumbnail()

    raw_manifest = {}
    if MANIFEST_JSON.exists():
        try:
            raw_manifest = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
        except Exception:
            raw_manifest = {}

    fname = FILM_MP4.name
    entry = raw_manifest.get(fname, {
        "season": 1,
        "episode": 1,
        "format": "16:9 Full Widescreen Film (~7m)",
        "title": TITLE,
        "channels": {},
    })

    for ch_cfg in CHANNELS:
        handle = ch_cfg["handle"]
        exp_id = ch_cfg["expected_id"]
        if handle in entry["channels"] and entry["channels"][handle].get("video_id"):
            print(f"✅ Already published on {handle} ({ch_cfg['role']}): {entry['channels'][handle]['watch_url']}")
            continue

        uploaded = False
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
                print(f"🚀 Uploading {fname} ({FILM_MP4.stat().st_size/1e6:.2f} MB) to '{ch_title}' ({handle}) via {tpath.name}...")
                body = {
                    "snippet": {
                        "title": TITLE[:100],
                        "description": build_description(handle),
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
                media = MediaFileUpload(str(FILM_MP4), mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
                req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
                resp = None
                while resp is None:
                    _, resp = req.next_chunk()
                vid_id = resp["id"]
                watch_url = f"https://www.youtube.com/watch?v={vid_id}"
                print(f"🎉 PUBLISHED FULL FILM ON {handle} ({ch_title}): {watch_url}")

                # Attempt custom thumbnail upload (graceful if unverified on a newer channel)
                try:
                    yt.thumbnails().set(
                        videoId=vid_id,
                        media_body=MediaFileUpload(str(THUMB_JPG), mimetype="image/jpeg"),
                    ).execute()
                    print(f"   🖼️ Custom 16:9 thumbnail set on {vid_id}!")
                except Exception as te:
                    print(f"   ℹ️ Custom thumbnail skipped ({te})")

                entry["channels"][handle] = {
                    "role": ch_cfg["role"],
                    "channel_id": exp_id,
                    "channel_title": ch_title,
                    "video_id": vid_id,
                    "watch_url": watch_url,
                    "token": str(tpath.relative_to(CRED_DIR)),
                }
                raw_manifest[fname] = entry
                MANIFEST_JSON.write_text(json.dumps(raw_manifest, indent=2, ensure_ascii=False), encoding="utf-8")
                uploaded = True
                break
            except HttpError as e:
                print(f"  ⚠️ HTTP error on {tpath.name} for {handle}: {e}")
            except Exception as e:
                print(f"  ⚠️ Error on {tpath.name} for {handle}: {e}")

        if not uploaded:
            print(f"❌ Failed to publish on {handle}")
            sys.exit(1)


if __name__ == "__main__":
    main()
