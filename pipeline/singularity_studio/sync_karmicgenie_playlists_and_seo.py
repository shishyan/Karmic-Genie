#!/usr/bin/env python3
"""
Canonical Playlist, Bucket Routing, Channel Shelves & Full SEO/Tag/Hashtag Synchronizer
for The Karmic Genie Show (`@karmicgenie` / `UCmixCKV4uTv3wIp634IRLXg`).

Enforces:
1. Strict Zero-CTA (`assert_zero_cta`) across every playlist, title, description, and tag.
2. Three canonical YouTube playlist buckets (plus existing ASMR/Meditation buckets):
   - `singularity_chronicles`: The Singularity Chronicles (2022–2100) — World Industrial Revolution & Future Timeline
     (28 films in exact chronological order: Overviews + Years 2027..2050 + Companion Specials)
   - `dharma_full` (`PLTadq3TncTFE`): The Karmic Genie Show — Purpose, Dharma & Timeless Life Wisdom
     (12 public full-length philosophical & 7D wisdom episodes, cleaned of deleted/private/short entries)
   - `dharma_shorts`: Karmic Genie Shorts — 60-Second Dharma, Purpose & Life Wisdom
     (15 public philosophical & Vedic wisdom Shorts)
3. Right YouTube Category Bucket (`categoryId`):
   - `28` (Science & Technology) for all Singularity, AI & World Industrial Revolution episodes
   - `27` (Education) for all Dharma, Purpose & Life Wisdom episodes and Shorts
4. Complete SEO Tags (`20-28` tags <= 485 chars), Key Chapters (`00:00`), Playlist Cross-Links,
   and Hashtags (`<= 12` hashtags per video) across every public video and Short.
5. Featured `channelSections` shelves on `@karmicgenie` Channel Home Page.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from karmicgenie_seo import (
    LEGACY_VIDEOS_SEO,
    VIRAL_TAGS_CORE,
    assert_zero_cta,
    get_episode_seo_package,
    pack_tags_under_limit,
)

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

CHANNEL_ID = "UCmixCKV4uTv3wIp634IRLXg"
STUDIO_ROOT = Path("/home/shishyan/GitHub/Influenzian/Utility_Explainer_Studio")
KG_EP_ROOT = STUDIO_ROOT / "episodes" / "karmic_genie"
MASTER_PL_PATH = KG_EP_ROOT / "karmicgenie_master_playlists.json"
TOKEN_PATH = Path("/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/credentials/token_karmicgenie.json")

SINGULARITY_PL_TITLE = "The Singularity Chronicles (2022–2100) — World Industrial Revolution & Future Timeline"
SINGULARITY_PL_DESC = (
    "Complete 26-film chronological documentary series exploring the World Industrial Revolution, "
    "Global Business Transformation, Technological Singularity, and Earth's 280-Month Planetary Awakening "
    "from 2022 through every single year (2027 to 2050) and the 2100 horizon—grounded in real engineering "
    "bottlenecks, economic breakthroughs, and timeless Vedic causal principles.\n\n"
    "Series Structure:\n"
    "• Overview Films: World Industrial Revolution (2022–2050) & Technological Singularity (2026–2100)\n"
    "• Decade I (Years 2027–2036): Silicon Photonics, Intent AI, Factory Robotics, Unified Supply Chains, Solid-State Storage, Tandem Solar, Optical Compute, Microbiomics, Abundance Utilities & Biophilic Cities\n"
    "• Decade II (Years 2037–2050): Deep Geothermal, Regenerative Finance, Subterranean Maglev, 100-Year Manufacturing, Ocean Sanctuaries, Cellular Longevity, Honeycomb Cities, Compact Fusion, Unified Science, Month-280 Sovereign Birth, Climate Rebalance, Steward Guilds, Lunar Embassy & Vasudhaiva Kutumbakam\n\n"
    "#Singularity #IndustrialRevolution #FutureTimeline #FutureOfBusiness #VedicWisdom #TheKarmicGenieShow #KarmicGenie #viral"
)

DHARMA_PL_ID = "PLTadq3TncTFE"
DHARMA_PL_TITLE = "The Karmic Genie Show — Purpose, Dharma & Timeless Life Wisdom"
DHARMA_PL_DESC = (
    "Full-length philosophical stories, modern parables, and 7D wisdom episodes (Duty, Dignity, Discipline, "
    "Dharma, Devotion, Divine, Destiny) from The Karmic Genie Show—exploring purposeful work, conscience, "
    "family devotion, intelligence vs. wisdom, and authentic human fulfillment.\n\n"
    "#TheKarmicGenieShow #KarmicGenie #PurposefulLiving #Dharma #LifeWisdom #VedicWisdom #viral"
)

SHORTS_PL_TITLE = "Karmic Genie Shorts — 60-Second Dharma, Purpose & Life Wisdom"
SHORTS_PL_DESC = (
    "Crisp 60-second philosophical reflections, Vedic parables, and 7D life-wisdom Shorts from The Karmic Genie Show "
    "on conscience, true duty, authentic calling, inner peace, and dignified work.\n\n"
    "#KarmicGenie #TheKarmicGenieShow #LifeWisdom #Dharma #Shorts #viralshorts #viral"
)

ASMR_FOCUS_PL_ID = "PLR3b7ZaAl3tk"
ASMR_RAIN_PL_ID = "PLWS2fI-SQXv0"

UNTAGGED_SHORTS_META: dict[str, tuple[str, list[str]]] = {
    "W9geQh1chMs": (
        "What does true duty really mean? True Duty is not merely an office title—it is the sacred responsibility whose neglect awakens your inner conscience, grounding your family, character, and soul.",
        ["what true duty really means", "meaning of duty and dharma", "conscience and karma", "7d purposeful living"],
    ),
    "FS5Ntp7e0ac": (
        "At work, any role can be reassigned tomorrow—at home, to your parents, spouse, and children, you are forever irreplaceable. Guard the duties only you can fulfill.",
        ["you are replaceable at work not at home", "family first wisdom", "work life balance dharma", "irreplaceable at home"],
    ),
    "KTCNN64nzus": (
        "Every honest worker who fulfills daily duty with integrity, care, and 10 out of 10 sincerity stands as noble as a king before the Divine.",
        ["every honest worker is noble", "dignity of labor", "earn with dignity", "honest work karma"],
    ),
    "qgDQNZtzybA": (
        "How do you earn unbroken, peaceful sleep tonight? A clear conscience after fulfilling today's real duties rewards the heart with effortless rest.",
        ["how to earn peaceful sleep tonight", "clear conscience peaceful sleep", "peace of mind wisdom", "night reflection dharma"],
    ),
    "hzdWII4f7a4": (
        "Wealth earned with honesty nourishes generations with pride, whereas money gained through deceit quietly burdens the conscience.",
        ["honest wealth vs dishonest money", "earn with dignity and honor", "karma of honest money", "conscience and wealth"],
    ),
    "R674shyJAcA": (
        "Earth is not a passive vacation hotel—it is a living spiritual school where every challenge, duty, and relationship levels up the soul.",
        ["earth is a school for the soul", "purpose of human life", "soul evolution vedic wisdom", "earth is not a vacation hotel"],
    ),
    "tRkD4TnIM1w": (
        "A corporate salary is like a highway—a helpful road to travel on, never the soul's final destination. Use your career to serve real purpose and family duty.",
        ["corporate salary is merely a highway", "career vs life purpose", "money as a tool not destination", "dharma at work"],
    ),
    "4lKLldCL4yM": (
        "At the end of our journey, titles fade and only how sincerely we lived, loved, and fulfilled our duty remains on the soul's report card.",
        ["souls report card", "what matters at the end of life", "karma and life purpose", "living with conscience"],
    ),
    "hFRwabEwvQY": (
        "இரு வகை ஞானம் — உலகியல் அறிவும் மெய்ஞ்ஞானத் தெளிவும் இணைந்து மனித வாழ்வை உயர்த்தும் வேதாந்தக் குறுங்கதை (Two Kinds of Knowledge — Karmic Genie Wisdom Short).",
        ["இரு வகை ஞானம்", "tamil vedanta shorts", "tamil spiritual wisdom", "two kinds of knowledge vedanta", "karmic genie tamil"],
    ),
    "AmV6i7UiGzs": (
        "இரு பறவைகள் (Mundaka Upanishad Two Birds Parable in Tamil) — ஒரே மரத்தில் அமர்ந்திருக்கும் ஜீவாத்மா மற்றும் பரமாத்மா தத்துவக் குறுங்கதை.",
        ["இரு பறவைகள் உபநிஷத்", "two birds story tamil", "mundaka upanishad tamil", "tamil spiritual shorts", "karmic genie tamil"],
    ),
}


def get_yt():
    assert TOKEN_PATH.exists(), f"Missing token: {TOKEN_PATH}"
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
    ch = yt.channels().list(part="snippet", mine=True).execute()["items"][0]
    if ch["id"] != CHANNEL_ID:
        raise RuntimeError(f"SAFETY ABORT: Token belongs to {ch['id']}, expected {CHANNEL_ID}")
    print(f"[Auth OK] Connected to {ch['snippet']['title'].strip()} ({ch['id']})")
    return yt


def repair_local_delivery_links() -> None:
    ep6_dl = KG_EP_ROOT / "KG_Ep06_Blindfolded_Forest" / "delivery_links.json"
    if ep6_dl.exists():
        d = json.loads(ep6_dl.read_text(encoding="utf-8"))
        if not d.get("youtubeVideoId"):
            d["youtubeVideoId"] = "ExSIPwqywzA"
            d["youtubeUrl"] = "https://youtu.be/ExSIPwqywzA"
            d["privacyStatus"] = "public"
            d.pop("youtubeError", None)
            ep6_dl.write_text(json.dumps(d, indent=2), encoding="utf-8")
            kg_repo_ep = Path("/home/shishyan/GitHub/Karmic-Genie-Show/episodes/KG_Ep06_Blindfolded_Forest")
            kg_repo_ep.mkdir(parents=True, exist_ok=True)
            (kg_repo_ep / "published_manifest.json").write_text(json.dumps(d, indent=2), encoding="utf-8")
            print("[Repair OK] Recorded ExSIPwqywzA in KG_Ep06_Blindfolded_Forest/delivery_links.json")


def list_all_playlists(yt) -> dict[str, dict]:
    out: dict[str, dict] = {}
    tok = None
    while True:
        res = yt.playlists().list(part="snippet,status,contentDetails", mine=True, maxResults=50, pageToken=tok).execute()
        for it in res.get("items", []):
            out[it["id"]] = it
        tok = res.get("nextPageToken")
        if not tok:
            break
    return out


def ensure_playlist(yt, existing_by_id: dict[str, dict], title: str, description: str, preferred_id: str = "") -> str:
    assert_zero_cta(title, "playlist.title")
    assert_zero_cta(description, "playlist.description")

    target_id = ""
    if preferred_id and preferred_id in existing_by_id:
        target_id = preferred_id
    else:
        for pid, pl in existing_by_id.items():
            if pl["snippet"]["title"].strip().lower() == title.strip().lower():
                target_id = pid
                break

    if target_id:
        yt.playlists().update(
            part="snippet,status",
            body={
                "id": target_id,
                "snippet": {"title": title, "description": description, "defaultLanguage": "en"},
                "status": {"privacyStatus": "public"},
            },
        ).execute()
        print(f"[Playlist Updated] {target_id} -> {title}")
        return target_id

    created = yt.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description, "defaultLanguage": "en"},
            "status": {"privacyStatus": "public"},
        },
    ).execute()
    new_id = created["id"]
    print(f"[Playlist Created] {new_id} -> {title}")
    return new_id


def sync_playlist_exact_order(yt, playlist_id: str, desired_video_ids: list[str], remove_unlisted_extras: bool = False) -> int:
    existing_items = []
    tok = None
    while True:
        res = yt.playlistItems().list(part="id,snippet,contentDetails", playlistId=playlist_id, maxResults=50, pageToken=tok).execute()
        existing_items.extend(res.get("items", []))
        tok = res.get("nextPageToken")
        if not tok:
            break

    desired_set = set(desired_video_ids)
    kept_by_vid: dict[str, dict] = {}
    for it in existing_items:
        vid = it["contentDetails"]["videoId"]
        if (remove_unlisted_extras and vid not in desired_set) or (vid in kept_by_vid):
            yt.playlistItems().delete(id=it["id"]).execute()
            print(f"  [Playlist Clean] Removed stale/duplicate {vid} from {playlist_id}")
            time.sleep(0.2)
        else:
            kept_by_vid[vid] = it

    existing_order = [it["contentDetails"]["videoId"] for it in sorted(kept_by_vid.values(), key=lambda x: x["snippet"]["position"]) if it["contentDetails"]["videoId"] in desired_set]
    if existing_order == desired_video_ids:
        print(f"  [Playlist Sync OK] {playlist_id} already has all {len(desired_video_ids)} videos in exact order.")
        return len(desired_video_ids)

    # Insert missing or reorder cleanly
    manual_sort_supported = True
    for pos, vid in enumerate(desired_video_ids):
        if vid not in kept_by_vid:
            snip = {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": vid},
            }
            if manual_sort_supported:
                snip["position"] = pos
            try:
                ins = yt.playlistItems().insert(part="snippet", body={"snippet": snip}).execute()
            except Exception as exc:
                if "support position" in str(exc).lower() or "manual" in str(exc).lower():
                    manual_sort_supported = False
                    snip.pop("position", None)
                    ins = yt.playlistItems().insert(part="snippet", body={"snippet": snip}).execute()
                else:
                    raise
            kept_by_vid[vid] = ins
            print(f"  [Playlist Add] {playlist_id} [{pos:02d}] + {vid}")
            time.sleep(0.25)
        elif manual_sort_supported:
            item = kept_by_vid[vid]
            if item["snippet"].get("position") != pos:
                try:
                    yt.playlistItems().update(
                        part="snippet",
                        body={
                            "id": item["id"],
                            "snippet": {
                                "playlistId": playlist_id,
                                "position": pos,
                                "resourceId": {"kind": "youtube#video", "videoId": vid},
                            },
                        },
                    ).execute()
                    print(f"  [Playlist Reorder] {playlist_id} [{pos:02d}] -> {vid}")
                    time.sleep(0.2)
                except Exception as exc:
                    if "support position" in str(exc).lower() or "manual" in str(exc).lower():
                        manual_sort_supported = False
                    else:
                        raise
    return len(desired_video_ids)


def fetch_video_map(yt, video_ids: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    uniq = list(dict.fromkeys(video_ids))
    for i in range(0, len(uniq), 50):
        batch = uniq[i : i + 50]
        res = yt.videos().list(part="snippet,status", id=",".join(batch)).execute()
        for it in res.get("items", []):
            out[it["id"]] = it
    return out


def sanitize_legacy_desc_and_cap_hashtags(desc: str, max_hashtags: int = 12) -> str:
    """Strips legacy CTA lines from older descriptions and caps total #hashtags <= 12 (YouTube ignores >15)."""
    import re
    clean_lines = []
    for line in desc.splitlines():
        low = line.lower()
        if any(bad in low for bad in ("subscribe", "hit the bell", "notification bell", "smash that like", "like and share", "leave a comment", "comment below", "follow for more")):
            continue
        clean_lines.append(line)
    txt = "\n".join(clean_lines)
    seen_ht: list[str] = []

    def repl_ht(m):
        ht = m.group(0)
        if ht.lower() in [x.lower() for x in seen_ht]:
            return ""
        if len(seen_ht) >= max_hashtags:
            return ""
        seen_ht.append(ht)
        return ht

    txt = re.sub(r"#[A-Za-z0-9_\u0B80-\u0BFF]+", repl_ht, txt)
    txt = re.sub(r"[ \t]{2,}", " ", txt)
    txt = re.sub(r"\n{3,}", "\n\n", txt).strip()
    return txt


def update_video_snippet_if_needed(
    yt,
    current_v: dict,
    title: str,
    description: str,
    tags: list[str],
    category_id: str,
    default_lang: str = "en",
) -> bool:
    vid = current_v["id"]
    assert_zero_cta(title, f"{vid}.title")
    assert_zero_cta(description, f"{vid}.description")
    for t in tags:
        assert_zero_cta(t, f"{vid}.tag")

    cur_snip = current_v["snippet"]
    cur_tags = cur_snip.get("tags", [])
    if (
        cur_snip.get("title") == title[:100]
        and cur_snip.get("description") == description
        and cur_tags == tags
        and str(cur_snip.get("categoryId")) == str(category_id)
    ):
        return False

    body = {
        "id": vid,
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": str(category_id),
            "defaultLanguage": cur_snip.get("defaultLanguage") or default_lang,
        },
    }
    if cur_snip.get("defaultAudioLanguage"):
        body["snippet"]["defaultAudioLanguage"] = cur_snip["defaultAudioLanguage"]

    yt.videos().update(part="snippet", body=body).execute()
    ht_cnt = len([w for w in description.split() if w.startswith("#")])
    print(f"  [SEO Updated] {vid} | cat={category_id} | tags={len(tags)} | hashtags={ht_cnt} | {title[:68]}")
    time.sleep(0.2)
    return True


def sync_channel_sections(yt, playlist_ids_ordered: list[str]) -> None:
    existing = yt.channelSections().list(part="id,snippet,contentDetails", mine=True).execute().get("items", [])
    existing_pl_sections = [
        s for s in existing if s["snippet"]["type"] == "singleplaylist"
    ]
    existing_pids = [
        (s.get("contentDetails", {}).get("playlists") or [""])[0] for s in existing_pl_sections
    ]
    if existing_pids == playlist_ids_ordered:
        print("[Channel Sections OK] Home tab shelves already match canonical playlist order.")
        return

    for s in existing_pl_sections:
        yt.channelSections().delete(id=s["id"]).execute()
        time.sleep(0.2)

    for pos, pid in enumerate(playlist_ids_ordered):
        yt.channelSections().insert(
            part="snippet,contentDetails",
            body={
                "snippet": {"type": "singleplaylist", "position": pos},
                "contentDetails": {"playlists": [pid]},
            },
        ).execute()
        print(f"  [Channel Shelf Added] position={pos} -> playlist={pid}")
        time.sleep(0.25)


def main() -> None:
    repair_local_delivery_links()
    yt = get_yt()
    existing_pls = list_all_playlists(yt)

    # 1. Build exact chronological Singularity video list (28 public films)
    annual_vids: list[tuple[int, str, str]] = []
    for yr in range(2027, 2051):
        matches = list(KG_EP_ROOT.glob(f"KG_Year_{yr}_*"))
        assert len(matches) == 1, f"Expected 1 folder for year {yr}, found {matches}"
        ep_d = matches[0]
        dl = json.loads((ep_d / "delivery_links.json").read_text(encoding="utf-8"))
        vid = dl["youtubeVideoId"]
        assert vid, f"Missing youtubeVideoId for {ep_d.name}"
        annual_vids.append((yr, ep_d.name, vid))

    singularity_ordered_ids = (
        ["R3Uj4cLeyW4", "Su7OdsAoqHs"]
        + [vid for _, _, vid in annual_vids]
        + ["5WY5cCYrO-k", "t6kTW4S97KE"]
    )

    dharma_full_ordered_ids = [
        "VuOrY0If1XI",  # Ep 01: Why Only 2% of YouTubers Make Money
        "wveLPokMQ_8",  # Ep 02: Why Only Your Unique ViewPoint Matters.
        "ixyrGi2mvCA",  # Ep 03: The Infinite Distractions
        "GGElKjHqHyI",  # Ep 04: Where Were You Before You Were Born?
        "eeNTrNt6i7A",  # Ep 05: The Choice You Never Make — Intelligent vs Wise Man Story
        "ExSIPwqywzA",  # Ep 06: How Do You Get Out of a Thick Forest Blindfolded?
        "zWju3qw3eeg",  # 83% Memory Collapse: MIT Cognitive Debt & 10-80-10 Brain Protocol
        "uitI7BZs3R0",  # S1E1: Non-AI Teams, $720B CapEx & The 2030 Clock
        "tMKfgkEkqeY",  # S1E1: 200,000 Cuts, 60,000 Buyouts & Blessing in Disguise
        "3b6Y9QaEc0A",  # S1E1: Respect Your Duty First
        "FW5sTSnkBz4",  # Pilot: Two Birds Story!
        "HgJWcfoZzBY",  # Peace of Mind
    ]

    dharma_shorts_ordered_ids = [
        "Pr1sLM829PQ",
        "ajhyYdyunQs",
        "tIvZuDVRj3w",
        "Dzne0-aAGi8",
        "GSslzrrK8NM",
        "W9geQh1chMs",
        "FS5Ntp7e0ac",
        "KTCNN64nzus",
        "qgDQNZtzybA",
        "hzdWII4f7a4",
        "R674shyJAcA",
        "tRkD4TnIM1w",
        "4lKLldCL4yM",
        "hFRwabEwvQY",
        "AmV6i7UiGzs",
    ]

    # 2. Ensure Playlists exist & save registry BEFORE generating cross-linked SEO descriptions
    prev_reg = json.loads(MASTER_PL_PATH.read_text(encoding="utf-8")) if MASTER_PL_PATH.exists() else {}
    sing_pref_id = prev_reg.get("singularity_chronicles", {}).get("id", "")
    shorts_pref_id = prev_reg.get("dharma_shorts", {}).get("id", "")

    sing_pl_id = ensure_playlist(yt, existing_pls, SINGULARITY_PL_TITLE, SINGULARITY_PL_DESC, preferred_id=sing_pref_id)
    dharma_pl_id = ensure_playlist(yt, existing_pls, DHARMA_PL_TITLE, DHARMA_PL_DESC, preferred_id=DHARMA_PL_ID)
    shorts_pl_id = ensure_playlist(yt, existing_pls, SHORTS_PL_TITLE, SHORTS_PL_DESC, preferred_id=shorts_pref_id)

    master_registry = {
        "singularity_chronicles": {
            "id": sing_pl_id,
            "url": f"https://www.youtube.com/playlist?list={sing_pl_id}",
            "title": SINGULARITY_PL_TITLE,
            "categoryBucket": "28 (Science & Technology)",
            "count": len(singularity_ordered_ids),
            "videoIds": singularity_ordered_ids,
        },
        "dharma_full": {
            "id": dharma_pl_id,
            "url": f"https://www.youtube.com/playlist?list={dharma_pl_id}",
            "title": DHARMA_PL_TITLE,
            "categoryBucket": "27 (Education)",
            "count": len(dharma_full_ordered_ids),
            "videoIds": dharma_full_ordered_ids,
        },
        "dharma_shorts": {
            "id": shorts_pl_id,
            "url": f"https://www.youtube.com/playlist?list={shorts_pl_id}",
            "title": SHORTS_PL_TITLE,
            "categoryBucket": "27 (Education)",
            "count": len(dharma_shorts_ordered_ids),
            "videoIds": dharma_shorts_ordered_ids,
        },
        "asmr_meditation_focus": {
            "id": ASMR_FOCUS_PL_ID,
            "url": f"https://www.youtube.com/playlist?list={ASMR_FOCUS_PL_ID}",
            "title": "ASMR Meditation & Focus — Zen Flute, Piano & Mountains",
        },
        "asmr_rain_forest": {
            "id": ASMR_RAIN_PL_ID,
            "url": f"https://www.youtube.com/playlist?list={ASMR_RAIN_PL_ID}",
            "title": "Deep Sleep & ASMR — Rain, Forest & Waterfall Soundscapes",
        },
    }
    MASTER_PL_PATH.write_text(json.dumps(master_registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[Registry Saved] {MASTER_PL_PATH}")

    # 3. Populate & order all Playlists ("right buckets")
    print("\n=== Step 3: Populating & Ordering Playlist Buckets ===")
    sync_playlist_exact_order(yt, sing_pl_id, singularity_ordered_ids, remove_unlisted_extras=True)
    sync_playlist_exact_order(yt, dharma_pl_id, dharma_full_ordered_ids, remove_unlisted_extras=True)
    sync_playlist_exact_order(yt, shorts_pl_id, dharma_shorts_ordered_ids, remove_unlisted_extras=True)

    # Also ensure the 2 Botanical Time-Lapses sit inside ASMR Meditation & Focus (PLR3b7ZaAl3tk)
    focus_existing = []
    tok = None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=ASMR_FOCUS_PL_ID, maxResults=50, pageToken=tok).execute()
        focus_existing.extend([x["contentDetails"]["videoId"] for x in r.get("items", [])])
        tok = r.get("nextPageToken")
        if not tok:
            break
    for tl_vid in ["DEMHBbwT7Bc", "R7UsKjz9144"]:
        if tl_vid not in focus_existing:
            yt.playlistItems().insert(
                part="snippet",
                body={"snippet": {"playlistId": ASMR_FOCUS_PL_ID, "resourceId": {"kind": "youtube#video", "videoId": tl_vid}}},
            ).execute()
            print(f"  [Playlist Add] {ASMR_FOCUS_PL_ID} + {tl_vid} (Botanical Time-Lapse)")

    # 4. Update SEO Tags, Hashtags, Playlist Links & Category Buckets across ALL videos
    print("\n=== Step 4: Auditing & Updating Video SEO Tags, Hashtags & Category Buckets ===")
    all_target_vids = (
        singularity_ordered_ids
        + dharma_full_ordered_ids
        + dharma_shorts_ordered_ids
    )
    vmap = fetch_video_map(yt, all_target_vids)
    updated_count = 0

    # 4A. All 26 Singularity Chronicles + 6 ShishyanEN Dharma Episodes via get_episode_seo_package
    slug_vid_pairs = [
        ("KG_Singularity_Ep02_Planetary_Awakening_2050", "R3Uj4cLeyW4"),
        ("KG_Singularity_Ep01_Crucible_To_2100", "Su7OdsAoqHs"),
    ] + [(slug, vid) for _, slug, vid in annual_vids] + [
        ("KG_Creator_Dharma_2Percent", "VuOrY0If1XI"),
        ("KG_Time_Is_Life_Part2", "wveLPokMQ_8"),
        ("KG_Ep03_Infinite_Distractions", "ixyrGi2mvCA"),
        ("KG_Ep04_Before_You_Were_Born", "GGElKjHqHyI"),
        ("KG_Ep05_Intelligent_Vs_Wise", "eeNTrNt6i7A"),
        ("KG_Ep06_Blindfolded_Forest", "ExSIPwqywzA"),
    ]
    for slug, vid in slug_vid_pairs:
        pkg = get_episode_seo_package(slug)
        if update_video_snippet_if_needed(
            yt,
            vmap[vid],
            title=pkg["title"],
            description=pkg["description"],
            tags=pkg["tags"],
            category_id=pkg["categoryId"],
        ):
            updated_count += 1

    # 4B. Companion Future Specials (ensure Singularity Playlist link + Science & Tech cat=28 + full tags/hashtags)
    for comp_vid, comp_tags in [
        (
            "5WY5cCYrO-k",
            [
                "2026 to 2050 future timeline",
                "how future leaders will rebuild everything",
                "singularity chronicles",
                "world industrial revolution 2026 to 2050",
                "future of business and ai",
                "year by year future predictions",
                "world in 2050",
            ],
        ),
        (
            "t6kTW4S97KE",
            [
                "future timeline documentary",
                "technological singularity",
                "world industrial revolution",
                "singularity chronicles",
                "future of humanity and technology",
                "vedic wisdom and future",
            ],
        ),
    ]:
        cv = vmap[comp_vid]
        cur_t = cv["snippet"]["title"]
        cur_d = cv["snippet"].get("description", "")
        pl_url = f"https://www.youtube.com/playlist?list={sing_pl_id}"
        if pl_url not in cur_d:
            cur_d = (
                cur_d.rstrip()
                + f"\n\nWatch the Complete Singularity Chronicles Playlist (2022–2100):\n{pl_url}\n\n"
                "#Singularity #FutureTimeline #IndustrialRevolution #FutureOfBusiness #TheKarmicGenieShow #KarmicGenie #viral"
            )
        cur_d = sanitize_legacy_desc_and_cap_hashtags(cur_d, max_hashtags=12)
        merged_tags = pack_tags_under_limit(comp_tags + (cv["snippet"].get("tags") or []) + VIRAL_TAGS_CORE, max_chars=485)
        if update_video_snippet_if_needed(yt, cv, cur_t, cur_d, merged_tags, category_id="28"):
            updated_count += 1

    # 4C. Legacy Studio Episodes (3b6Y9QaEc0A, FW5sTSnkBz4, HgJWcfoZzBY) + Cognitive Debt Episode (zWju3qw3eeg)
    for leg_vid, meta in LEGACY_VIDEOS_SEO.items():
        if leg_vid in vmap:
            cv = vmap[leg_vid]
            desc = meta["description"]
            pl_url = f"https://www.youtube.com/playlist?list={dharma_pl_id}"
            if pl_url not in desc:
                desc = desc.replace("#TheKarmicGenieShow", f"Full Karmic Genie Wisdom Playlist: {pl_url}\n\n#TheKarmicGenieShow")
            tags = pack_tags_under_limit(meta["tags"] + VIRAL_TAGS_CORE, max_chars=485)
            if update_video_snippet_if_needed(yt, cv, cv["snippet"]["title"], desc, tags, category_id="27"):
                updated_count += 1

    for st_vid in ["zWju3qw3eeg", "uitI7BZs3R0", "tMKfgkEkqeY"]:
        if st_vid in vmap:
            cv = vmap[st_vid]
            cur_d = cv["snippet"].get("description", "")
            pl_url = f"https://www.youtube.com/playlist?list={dharma_pl_id}"
            if pl_url not in cur_d:
                cur_d = cur_d.rstrip() + f"\n\nFull Karmic Genie Wisdom Playlist: {pl_url}"
            cur_d = sanitize_legacy_desc_and_cap_hashtags(cur_d, max_hashtags=12)
            clean_existing_tags = [t for t in (cv["snippet"].get("tags") or []) if "subscribe" not in t.lower()]
            merged_tags = pack_tags_under_limit(clean_existing_tags + VIRAL_TAGS_CORE, max_chars=485)
            if update_video_snippet_if_needed(yt, cv, cv["snippet"]["title"], cur_d, merged_tags, category_id="27"):
                updated_count += 1

    # 4D. All 15 Dharma Shorts (populate rich SEO descriptions, 18+ tags & hashtags on the 10 untagged Shorts too)
    shorts_pl_url = f"https://www.youtube.com/playlist?list={shorts_pl_id}"
    for svid in dharma_shorts_ordered_ids:
        cv = vmap[svid]
        cur_t = cv["snippet"]["title"]
        if svid in UNTAGGED_SHORTS_META:
            hook_text, extra_tags = UNTAGGED_SHORTS_META[svid]
            is_ta = svid in ("hFRwabEwvQY", "AmV6i7UiGzs")
            ht = (
                "#KarmicGenie #TheKarmicGenieShow #TamilWisdom #Vedanta #Shorts #viralshorts #viral #trending"
                if is_ta
                else "#KarmicGenie #TheKarmicGenieShow #LifeWisdom #Dharma #PurposefulLiving #Shorts #viralshorts #viral #trending"
            )
            desc = (
                f"{hook_text}\n\n"
                f"Watch More 60-Second Wisdom Shorts: {shorts_pl_url}\n"
                f"Full Karmic Genie Episodes: https://www.youtube.com/playlist?list={dharma_pl_id}\n\n"
                f"{ht}"
            )
            tags = pack_tags_under_limit(
                extra_tags
                + [
                    "karmic genie shorts",
                    "life lessons shorts",
                    "philosophical shorts",
                    "vedic wisdom shorts",
                    "dharma and purpose",
                ]
                + VIRAL_TAGS_CORE,
                max_chars=485,
            )
            if update_video_snippet_if_needed(yt, cv, cur_t, desc, tags, category_id="27", default_lang="ta" if is_ta else "en"):
                updated_count += 1
        else:
            cur_d = cv["snippet"].get("description", "")
            if shorts_pl_url not in cur_d:
                cur_d = cur_d.rstrip() + f"\n\nWatch More Karmic Genie Shorts: {shorts_pl_url}"
            tags = pack_tags_under_limit((cv["snippet"].get("tags") or []) + VIRAL_TAGS_CORE, max_chars=485)
            if update_video_snippet_if_needed(yt, cv, cur_t, cur_d, tags, category_id="27"):
                updated_count += 1

    # 5. Update Channel Home Page Shelves (`channelSections`)
    print("\n=== Step 5: Syncing @karmicgenie Channel Home Page Shelves ===")
    sync_channel_sections(
        yt,
        [
            sing_pl_id,
            dharma_pl_id,
            shorts_pl_id,
            ASMR_FOCUS_PL_ID,
            ASMR_RAIN_PL_ID,
        ],
    )

    print(f"\n[COMPLETE] Updated SEO/Tags/Hashtags/Categories on {updated_count} videos across @karmicgenie!")
    print(json.dumps(master_registry, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
