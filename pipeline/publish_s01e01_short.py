#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publishes the 70%-Speed Season 1, Episode 1 Vertical Short (`Karmic_Genie_Show_S01E01_Tech_CEO_Short_70pct_9x16.mp4`)
to:
  1) PRIME CHANNEL: `@karmicgenie` ("Karmic Genie Show", ID: `UCmixCKV4uTv3wIp634IRLXg`)
  2) SYNDICATION CHANNEL: `@influenzian` ("Influenzian", ID: `UCcJFqC7z0f-ARNcJadKiKpQ`)
Strictly verifies `channel_id` via `channels().list(mine=True)` before uploading!
"""

import json
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

BASE_DIR = Path("/home/shishyan/GitHub/Influenzian/Karmic_Genie_Show")
SHORT_MP4 = BASE_DIR / "renders" / "Karmic_Genie_Show_S01E01_Tech_CEO_Short_70pct_9x16.mp4"
MANIFEST_JSON = BASE_DIR / "renders" / "published_manifest.json"
CRED_DIR = Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/credentials")

TITLE = "Employees vs. Tech CEO: Why AI Arrived Now | Karmic Genie Show (S1 E1) #Shorts"

CHANNELS = [
    {
        "handle": "@karmicgenie",
        "expected_id": "UCmixCKV4uTv3wIp634IRLXg",
        "role": "PRIME",
        "token_candidates": [
            CRED_DIR / "token_karmicgenie.json",
            CRED_DIR / "tokens_karmicgenie" / "token_472322435541.json",
            CRED_DIR / "tokens_karmicgenie" / "token_942198183044.json",
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


def build_description(handle: str) -> str:
    return (
        "Karmic Genie Show — Season 1, Episode 1: Employees vs. The Tech CEO\n"
        "\"What does Genie say — the 7D way?\"\n\n"
        "Record industry profits on one side, sweeping tech layoffs for AI hardware on the other—while years of "
        "real human duties (aging parents, children, health, and inner peace) waited on hold. When human debate "
        "hits a wall, the Karmic Genie awakens to share the deeper 2020–2030 perspective and Monday morning's Step Two.\n\n"
        "✨ Governed by The 7D Way:\n"
        "Do Your DUTY. • Practice DHARMA. • Remember the DIVINE. • Live by DISCIPLINE. • "
        "Keep Your DIGNITY. • Be DEVOUT. • Respect DESTINY.\n\n"
        f"📺 Subscribe to {handle} for full Season 1 episodes featuring candid real-life stories & commentary.\n\n"
        "#Shorts #KarmicGenieShow #Season1Episode1 #TechLayoffs #AI #FutureOfWork #The7DWay #Dharma #Duty"
    )


TAGS = [
    "Shorts",
    "Karmic Genie Show",
    "What does Genie say the 7D way",
    "Season 1 Episode 1",
    "Employees vs Tech CEO",
    "Tech Layoffs",
    "AI Revolution",
    "Future of Work",
    "Work Life Balance",
    "The 7D Way",
    "Duty Dharma Destiny",
]


def main():
    if not SHORT_MP4.exists():
        raise FileNotFoundError(f"Missing {SHORT_MP4}")

    raw_manifest = {}
    if MANIFEST_JSON.exists():
        try:
            raw_manifest = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
        except Exception:
            raw_manifest = {}

    fname = SHORT_MP4.name
    # Migrate single-channel entry if needed into per-channel dict
    entry = raw_manifest.get(fname, {})
    if "video_id" in entry and "channels" not in entry:
        entry = {
            "season": 1,
            "episode": 1,
            "speed": "70%",
            "title": TITLE,
            "channels": {
                entry.get("channel", "@influenzian"): {
                    "video_id": entry["video_id"],
                    "url": entry["url"],
                    "watch_url": entry.get("watch_url", f"https://www.youtube.com/watch?v={entry['video_id']}"),
                    "token": entry.get("token", ""),
                }
            },
        }
    elif "channels" not in entry:
        entry = {"season": 1, "episode": 1, "speed": "70%", "title": TITLE, "channels": {}}

    for ch_cfg in CHANNELS:
        handle = ch_cfg["handle"]
        exp_id = ch_cfg["expected_id"]
        if handle in entry["channels"] and entry["channels"][handle].get("video_id"):
            print(f"✅ Already published on {handle} ({ch_cfg['role']}): {entry['channels'][handle]['url']}")
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
                print(f"🚀 Uploading {fname} ({SHORT_MP4.stat().st_size/1e6:.2f} MB) to PRIME/TARGET '{ch_title}' ({handle}) via {tpath.name}...")
                body = {
                    "snippet": {
                        "title": TITLE[:100],
                        "description": build_description(handle),
                        "tags": TAGS,
                        "categoryId": "22",
                    },
                    "status": {
                        "privacyStatus": "public",
                        "selfDeclaredMadeForKids": False,
                    },
                }
                media = MediaFileUpload(str(SHORT_MP4), mimetype="video/mp4", chunksize=8 * 1024 * 1024, resumable=True)
                req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
                resp = None
                while resp is None:
                    _, resp = req.next_chunk()
                vid_id = resp["id"]
                url = f"https://youtube.com/shorts/{vid_id}"
                print(f"🎉 PUBLISHED ON {handle} ({ch_title}): {url}")
                entry["channels"][handle] = {
                    "role": ch_cfg["role"],
                    "channel_id": exp_id,
                    "channel_title": ch_title,
                    "video_id": vid_id,
                    "url": url,
                    "watch_url": f"https://www.youtube.com/watch?v={vid_id}",
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
