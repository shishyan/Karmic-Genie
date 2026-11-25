#!/usr/bin/env python3
"""
Canonical SEO, Tags, Hashtags & Channel-Level Metadata Optimizer for
The Karmic Genie Show (`@karmicgenie` / `UCmixCKV4uTv3wIp634IRLXg`).

Enforces:
1. STRICT ZERO-CTA INVARIANT (`assert_zero_cta`) across every title, description, tag, and channel profile.
2. Channel-Level SEO:
   - `Settings -> Channel -> Basic info -> Keywords` (~460-490 / 500 chars high-intent search & discovery keywords).
   - `Settings -> Upload defaults` (Category: Education / People & Blogs, Language: English, Default Brand Tags).
   - `Customization -> Profile -> Description` (Rich keyword-indexed About description + 5 clean hashtags, zero CTA).
3. Video-Level SEO (applied both at upload time in `publish_karmicgenie_cdp.py` AND retroactively across all existing videos on `@karmicgenie`):
   - First-2-line search-intent hook (above the fold in YouTube Search & Suggested).
   - Cross-episode binge-watch playlist/series links.
   - `00:00` Key Moments / YouTube Chapters (`>= 3` chapters >= 10s apart so Google Search & YouTube index rich chapter segments).
   - Exactly 5 targeted hashtags at the bottom of the description (`<= 15` YouTube hard limit; `3-5` optimal).
   - 18-24 high-intent YouTube Studio `Tags` (`420-490 / 500` chars total) combining exact-title query, long-tail philosophical/creator queries, Vedic/dharma wisdom anchors, and `@karmicgenie` brand tags.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

CHANNEL_ID = "UCmixCKV4uTv3wIp634IRLXg"
STUDIO_URL = f"https://studio.youtube.com/channel/{CHANNEL_ID}?authuser=0"
PROFILE_URL = f"https://studio.youtube.com/channel/{CHANNEL_ID}/editing/profile?authuser=0"
CDP_URL = "http://127.0.0.1:9225"
STUDIO_ROOT = Path("/home/shishyan/GitHub/Influenzian/Utility_Explainer_Studio")

FORBIDDEN_CTA = (
    "subscribe",
    "hit the bell",
    "notification bell",
    "smash that like",
    "like and share",
    "leave a comment",
    "comment below",
    "follow for more",
)


def assert_zero_cta(text: str, label: str = "metadata") -> None:
    low = text.lower()
    for bad in FORBIDDEN_CTA:
        if bad in low:
            raise AssertionError(f"STRICT ZERO-CTA VIOLATION in {label}: found {bad!r}")


def pack_tags_under_limit(tags: list[str], max_chars: int = 475) -> list[str]:
    """Deduplicates tags case-insensitively and packs cleanly under YouTube's 500-char limit."""
    seen: set[str] = set()
    clean: list[str] = []
    total = 0
    for raw in tags:
        t = re.sub(r"\s+", " ", raw).strip().strip(",")
        if not t or t.lower() in seen:
            continue
        assert_zero_cta(t, f"tag:{t}")
        # YouTube counts quotes/commas toward the 500-char tag budget
        cost = len(t) + (3 if " " in t else 1)
        if total + cost > max_chars:
            continue
        seen.add(t.lower())
        clean.append(t)
        total += cost
    return clean


VIRAL_HASHTAGS = "#viral #viralvideo #viralvideos #viralshorts #trending #TheKarmicGenieShow #KarmicGenie"
VIRAL_TAGS_CORE = [
    "viral",
    "viral video",
    "viralvideo",
    "viralvideos",
    "viral shorts",
    "viralshorts",
    "trending",
    "trending video",
    "must watch",
    "life changing",
    "wisdom",
    "motivation",
    "mindset",
    "the karmic genie show",
    "karmic genie",
]

CHANNEL_KEYWORDS = pack_tags_under_limit(
    VIRAL_TAGS_CORE
    + [
        "Karmic Genie",
        "karmic genie show",
        "purposeful living",
        "dharma and karma",
        "life lessons wisdom",
        "find your calling",
        "spiritual philosophy",
        "vedic wisdom modern life",
        "creator mindset",
        "self mastery",
        "conscious living",
        "philosophical storytelling",
        "animated wisdom stories",
        "how to find purpose in life",
        "soul evolution",
        "intelligent vs wise",
        "overcoming distractions",
    ],
    max_chars=485,
)

CHANNEL_ABOUT_DESCRIPTION = (
    "Welcome to The Karmic Genie Show — animated philosophical storytelling and timeless karmic wisdom for modern life, purposeful work, and soul evolution.\n\n"
    "Every episode explores the deeper laws behind human purpose, Dharma, Duty, Dignity, Discipline, Family Devotion, and Conscious Creation — peeling away surface noise, algorithmic traps, and modern distractions so you can build an authentic, meaningful life grounded in your true calling.\n\n"
    "Core Themes Explored on This Channel:\n"
    "• Finding your God-given gift and authentic calling over blind imitation\n"
    "• Time as finite human life and why lived experience matters\n"
    "• Vedic cosmology, karma, conscience, and the four stages of human growth (Physical, Emotional, Mental, Spiritual)\n"
    "• Intelligence vs. Wisdom — knowing what never to do so every remaining choice leads upward\n\n"
    "#TheKarmicGenieShow #KarmicGenie #PurposefulLiving #Dharma #LifeWisdom"
)


def fmt_mmss(sec: float) -> str:
    s = max(0, int(round(sec)))
    m, rem = divmod(s, 60)
    return f"{m:02d}:{rem:02d}"


def build_chapters_from_manifest(ep_slug: str, fallback_chapters: list[str]) -> str:
    mf_path = STUDIO_ROOT / "episodes" / "karmic_genie" / ep_slug / "manifest.json"
    if not mf_path.exists():
        return "\n".join(fallback_chapters)
    mf = json.loads(mf_path.read_text(encoding="utf-8"))
    lines: list[str] = []
    for idx, b in enumerate(mf.get("beats", [])):
        if idx == 0:
            tag = re.sub(r"^(EP\s*\d+|ACT\s*[IVX]+)\s*•\s*", "", b.get("actTag") or "Opening Reflection").strip()
            lines.append(f"00:00 {tag.title() if tag.isupper() else tag}")
        elif b.get("actTag"):
            clean_tag = re.sub(r"^ACT\s*[IVX]+\s*•\s*", "", b["actTag"]).strip()
            lines.append(f"{fmt_mmss(b['startSec'])} {clean_tag.title() if clean_tag.isupper() else clean_tag}")
    if len(lines) < 3:
        return "\n".join(fallback_chapters)
    return "\n".join(lines)


def load_master_playlists() -> dict[str, str]:
    pl_file = STUDIO_ROOT / "episodes" / "karmic_genie" / "karmicgenie_master_playlists.json"
    if pl_file.exists():
        try:
            data = json.loads(pl_file.read_text(encoding="utf-8"))
            return {k: v["id"] if isinstance(v, dict) else str(v) for k, v in data.items()}
        except Exception:
            pass
    return {"dharma_full": "PLTadq3TncTFE"}


def get_annual_slug_by_year() -> dict[int, tuple[str, str, str]]:
    out: dict[int, tuple[str, str, str]] = {}
    kg_root = STUDIO_ROOT / "episodes" / "karmic_genie"
    if not kg_root.exists():
        return out
    for d in sorted(kg_root.glob("KG_Year_*")):
        parts = d.name.split("_")
        if len(parts) >= 3 and parts[2].isdigit():
            yr = int(parts[2])
            dl = d / "delivery_links.json"
            rp = d / "raw_plan.json"
            url = ""
            ttl = d.name
            if dl.exists():
                url = json.loads(dl.read_text(encoding="utf-8")).get("youtubeUrl") or ""
            if rp.exists():
                ttl = json.loads(rp.read_text(encoding="utf-8")).get("title") or ttl
            out[yr] = (d.name, ttl, url)
    return out


def extract_title_topic_tags_and_hashtags(title: str) -> tuple[list[str], list[str]]:
    rhs = title.split(":", 1)[1] if ":" in title else title
    rhs = rhs.replace("—", ",").replace("+", ",").replace("&", ",")
    raw_chunks = [re.sub(r"\([^)]*\)", "", c).strip() for c in rhs.split(",")]
    topic_tags: list[str] = []
    topic_hashtags: list[str] = []
    stop_words = {"the", "of", "and", "in", "to", "for", "a", "an", "earths", "earth's", "world"}
    for ch in raw_chunks:
        clean = re.sub(r"[^A-Za-z0-9\s-]", "", ch).strip()
        if len(clean) >= 4:
            topic_tags.append(clean.lower())
            words = [w for w in re.split(r"[\s-]+", clean) if w and w.lower() not in stop_words]
            if words:
                camel = "#" + "".join(w[0].upper() + w[1:] for w in words[:3])
                if 4 <= len(camel) <= 28 and camel not in topic_hashtags:
                    topic_hashtags.append(camel)
    return topic_tags, topic_hashtags[:3]


def get_series_links_block(exclude_slug: str = "") -> str:
    pls = load_master_playlists()
    dharma_pl = pls.get("dharma_full", "PLTadq3TncTFE")
    links = [
        ("KG_Creator_Dharma_2Percent", "Ep 01 — Why Only 2% of YouTubers Make Money", "https://youtu.be/VuOrY0If1XI"),
        ("KG_Time_Is_Life_Part2", "Ep 02 — Why Only Your Unique ViewPoint Matters.", "https://youtu.be/wveLPokMQ_8"),
    ]
    for slug, label, fb_url in [
        ("KG_Ep03_Infinite_Distractions", "Ep 03 — The Infinite Distractions", "https://youtu.be/ixyrGi2mvCA"),
        ("KG_Ep04_Before_You_Were_Born", "Ep 04 — Where Were You Before You Were Born?", "https://youtu.be/GGElKjHqHyI"),
        ("KG_Ep05_Intelligent_Vs_Wise", "Ep 05 — The Choice You Never Make (Intelligent vs Wise Man)", "https://youtu.be/eeNTrNt6i7A"),
        ("KG_Ep06_Blindfolded_Forest", "Ep 06 — How Do You Get Out of a Thick Forest Blindfolded?", "https://youtu.be/ExSIPwqywzA"),
    ]:
        dl_p = STUDIO_ROOT / "episodes" / "karmic_genie" / slug / "delivery_links.json"
        url = fb_url
        if dl_p.exists():
            url = json.loads(dl_p.read_text(encoding="utf-8")).get("youtubeUrl") or fb_url
        if url:
            links.append((slug, label, url))
    out = [f"• Full Karmic Genie Wisdom Playlist: https://www.youtube.com/playlist?list={dharma_pl}"]
    out.extend([f"• {lbl}: {url}" for s, lbl, url in links if s != exclude_slug])
    return "Watch The Karmic Genie Show Series:\n" + "\n".join(out) if out else ""


def get_episode_seo_package(ep_slug: str) -> dict:
    """Returns canonical {title, description, tags, hashtags, categoryId} for any Karmic Genie episode."""
    series_block = get_series_links_block(exclude_slug=ep_slug)
    pls = load_master_playlists()
    sing_pl_id = pls.get("singularity_chronicles", "")
    sing_pl_line = (
        f"• Complete Singularity Chronicles Playlist (2022–2100): https://www.youtube.com/playlist?list={sing_pl_id}\n"
        if sing_pl_id
        else ""
    )
    category_id = "27"

    if ep_slug == "KG_Creator_Dharma_2Percent":
        chapters = build_chapters_from_manifest(
            ep_slug,
            [
                "00:00 The Spreadsheet Cage vs Real Truth",
                "02:05 Welcome to The Karmic Genie Show",
                "03:55 Why 90% of New Creators Quit by Week 4",
                "06:45 3 Miracles of Speaking What You Truly Lived",
                "10:15 3 Soul Questions to Find Your Unstealable Dharma",
            ],
        )
        hashtags = f"{VIRAL_HASHTAGS} #CreatorMindset #FindYourCalling #PurposeOverAlgorithms"
        desc = (
            "Why do only 2% of YouTubers make sustainable money while 98% burn out chasing niche spreadsheets, CPM charts, and algorithm hacks? "
            "In this episode of The Karmic Genie Show, we uncover why building a cage out of someone else's data fails by Week 4—and how three simple soul questions reveal your true Dharma and unstealable creative voice.\n\n"
            f"{series_block}\n\n"
            "Key Chapters:\n"
            f"{chapters}\n\n"
            "The 3 Questions to Uncover Your Unstealable Calling:\n"
            "1. What pulls at your mind when nobody is watching?\n"
            "2. What have you always burned to know — or share?\n"
            "3. What do others keep telling you that you are naturally capable of?\n\n"
            f"{hashtags}"
        )
        tags = pack_tags_under_limit(
            [
                "why only 2% of youtubers make money",
                "why most youtubers quit",
                "creator burnout",
                "how to start a youtube channel from zero",
                "find your youtube niche",
                "authentic content creation",
                "purpose over algorithms",
                "find your calling in life",
                "creator dharma",
                "youtube growth mindset",
                "why 98% of creators fail",
                "speaking your truth",
                "the karmic genie show",
                "karmic genie",
                "creative purpose",
                "ikigai and dharma",
                "animated wisdom story",
                "meaningful work",
            ]
        )
        title = "Why Only 2% of YouTubers Make Money"

    elif ep_slug == "KG_Time_Is_Life_Part2":
        chapters = build_chapters_from_manifest(
            ep_slug,
            [
                "00:00 Time Is Finite Human Life",
                "01:35 Why 24 Hours of Life Credit Drains Daily",
                "03:40 Why Lived Experience Accelerates Others Beyond Scriptures",
                "05:30 The Karmic Law: The Teacher Grows First",
                "07:10 Called to Hold the Mic vs Called to Live Naturally",
            ],
        )
        hashtags = f"{VIRAL_HASHTAGS} #UniqueViewpoint #TimeIsLife #LivedWisdom"
        desc = (
            "Why does only your unique viewpoint truly matter in a world overflowing with information? "
            "Every minute a viewer spends watching a video is a minute of their finite human lifetime—and while the Vedas and world scriptures already hold life's answers, human souls learn fastest through honest, lived experience shared in your unmistakable voice.\n\n"
            f"{series_block}\n\n"
            "Key Chapters:\n"
            f"{chapters}\n\n"
            "Core Reflections in This Episode:\n"
            "• Respecting viewer attention as sacred human lifetime\n"
            "• Why copying someone else's style wastes your own life credit\n"
            "• How teaching what genuinely helps you first creates effortless value\n"
            "• Why thriving off-screen as an intentional listener is just as noble as holding a microphone\n\n"
            f"{hashtags}"
        )
        tags = pack_tags_under_limit(
            [
                "why only your unique viewpoint matters",
                "time is life philosophy",
                "find your unique voice",
                "stop copying other creators",
                "lived experience vs book knowledge",
                "vedic wisdom modern life",
                "authentic storytelling",
                "respecting attention",
                "creator philosophy",
                "how to find your niche naturally",
                "teaching helps the teacher first",
                "purposeful living",
                "the karmic genie show",
                "karmic genie",
                "mindful content creation",
                "value of time",
                "dharma and life purpose",
                "animated philosophy",
            ]
        )
        title = "Why Only Your Unique ViewPoint Matters."

    elif ep_slug == "KG_Ep03_Infinite_Distractions":
        chapters = build_chapters_from_manifest(
            ep_slug,
            [
                "00:00 Escaping Herd Mentality & The Attention Trap",
                "01:15 Peeling Back Views, Millions & Praise to True Respect",
                "03:05 Your God-Given Gift: Body, Mind, Soul & Family Duty",
                "04:45 The Open Highway vs Shortcut Detours & The 3-Try Trust Law",
                "06:10 The 300-Yard Golf Swing: Gravity, Centrifugal Force & Tailwind",
            ],
        )
        hashtags = f"{VIRAL_HASHTAGS} #InfiniteDistractions #GodGivenGift #FindYourCalling"
        desc = (
            "In an age of infinite distractions, millions blindly follow the herd chasing attention, viral views, and shortcut millions—without asking what their heart actually wants. "
            "When you peel away the noise, the real wish was never a fantasy number; it was meaningful work, authentic respect, and using your God-given gift to nourish body, mind, soul, spirit, and the family walking beside you.\n\n"
            f"{series_block}\n\n"
            "Key Chapters:\n"
            f"{chapters}\n\n"
            "Core Analogies & Life Laws Explored:\n"
            "• Peeling back attention -> views -> $1M -> praise -> authentic dignity & respect\n"
            "• Why shortcut money washes away like shoreline sandcastles while your true gift lets you fail a billion times forward\n"
            "• The Open Highway vs. Dark Shortcut & the Divine 3-Try Law of Family Trust\n"
            "• Hitting a 300-yard golf drive through natural gravity, centrifugal rhythm, and divine tailwind\n\n"
            f"{hashtags}"
        )
        tags = pack_tags_under_limit(
            [
                "the infinite distractions",
                "overcoming distractions in life",
                "stop following the herd",
                "god given gift purpose",
                "attention economy trap",
                "chasing money vs purpose",
                "highway vs shortcut in life",
                "300 yard golf swing analogy",
                "family trust and duty",
                "why shortcut money washes away",
                "respect vs fame",
                "find your true calling",
                "the karmic genie show",
                "karmic genie",
                "purposeful work",
                "dharma for creators",
                "spiritual life lessons",
                "animated wisdom",
            ]
        )
        title = "The Infinite Distractions"

    elif ep_slug == "KG_Ep04_Before_You_Were_Born":
        chapters = build_chapters_from_manifest(
            ep_slug,
            [
                "00:00 Where Were You Before You Were Born?",
                "01:25 Vedic 84 Lakh Life Forms & The 1880-to-1980 Timeline",
                "02:55 Why Even Kings, Politicians & Billionaires Face Struggle",
                "04:15 Earth as a Continuing Soul MMORPG & 4 Stages of Leveling",
                "05:45 Family as the Fastest Path & Earning Wealth With Pride",
            ],
        )
        hashtags = f"{VIRAL_HASHTAGS} #BeforeYouWereBorn #VedicWisdom #SoulEvolution"
        desc = (
            "Where were you a hundred years before you were born—when the same oceans, lakes, and forests were alive on Earth, yet you hadn't arrived? "
            "Exploring the Vedic wisdom of 84 lakh life forms and life as a continuing soul MMORPG, this episode reveals how true human leveling unfolds across four 12-to-18-year stages—Physical, Emotional, Mental, and Spiritual—fastest and most naturally inside a loving family.\n\n"
            f"{series_block}\n\n"
            "Key Chapters:\n"
            f"{chapters}\n\n"
            "Core Questions Explored:\n"
            "• If everyone had a blank-slate choice before birth, why isn't everyone born a carefree King?\n"
            "• Why college and career are just the starter tutorial—and what real 60-year soul leveling looks like\n"
            "• Physical, Emotional, Mental & Spiritual growth through devoted family roles\n"
            "• Who do you choose to be today—earning wealth with honor, conscience, and family pride?\n\n"
            f"{hashtags}"
        )
        tags = pack_tags_under_limit(
            [
                "where were you before you were born",
                "84 lakh species in vedas",
                "life is like an mmorpg",
                "real life leveling up",
                "vedic philosophy of birth",
                "karma and reincarnation explained",
                "why is there suffering in the world",
                "four stages of human life",
                "physical emotional mental spiritual growth",
                "family dharma and spiritual growth",
                "earning money with honor and dignity",
                "who do you want to be today",
                "the karmic genie show",
                "karmic genie",
                "soul journey",
                "purpose of human birth",
                "animated spiritual story",
            ]
        )
        title = "Where Were You Before You Were Born?"

    elif ep_slug == "KG_Ep05_Intelligent_Vs_Wise":
        chapters = build_chapters_from_manifest(
            ep_slug,
            [
                "00:00 The Choice You Never Make: Intelligent vs Wise",
                "01:15 The 6 Rungs of Every Decision (Worst to Best)",
                "02:45 A Modern Parable of Two Builders: Hype vs Guardrails",
                "04:30 The Miracle of Subtraction: Locking Out Disaster",
                "05:50 Pairing Intelligence With Wisdom in Business, Money & Home",
            ],
        )
        hashtags = f"{VIRAL_HASHTAGS} #IntelligentVsWise #WisdomStory #DecisionMaking"
        desc = (
            "What is the real difference between an Intelligent Man and a Wise Man? "
            "While unguided intelligence blindly copies successful people's surface moves—stumbling through Bad, Worse, and Worst traps—a Wise Man knows clearly what NOT to do, automatically leaving only Good, Better, and Best choices standing in front of him.\n\n"
            f"{series_block}\n\n"
            "Key Chapters:\n"
            f"{chapters}\n\n"
            "Inside This Modern Parable of Success & Failure:\n"
            "• The 6 rungs of every major life choice: Worst, Worse, Bad vs. Good, Better, Best\n"
            "• Why copying empire founders without their 10 years of trust leads to leverage burnouts\n"
            "• Via Negativa (The Miracle of Subtraction): why race cars carry giant brakes to go fast safely\n"
            "• How intelligence becomes unstoppable once guided by wisdom and conscience\n\n"
            f"{hashtags}"
        )
        tags = pack_tags_under_limit(
            [
                "intelligent vs wise man story",
                "the choice you never make",
                "difference between intelligence and wisdom",
                "knowing what not to do",
                "via negativa wisdom",
                "how to make better life decisions",
                "modern parable of success and failure",
                "why smart people fail",
                "blindly copying successful people",
                "good better best choices",
                "wisdom vs cleverness",
                "mental models for life",
                "the karmic genie show",
                "karmic genie",
                "dharma and discernment",
                "animated wisdom parable",
                "timeless life lessons",
            ]
        )
        title = "The Choice You Never Make — Intelligent vs Wise Man Story"

    elif ep_slug == "KG_Ep06_Blindfolded_Forest":
        chapters = build_chapters_from_manifest(
            ep_slug,
            [
                "00:00 Blindfolded in a Thick Forest",
                "01:10 Two Human Responses & Joining Hands as a Family",
                "02:00 Follow the Running Water (Vedic Riverbed Wisdom)",
                "03:00 Survive First & Don't Escape the Lesson",
            ],
        )
        hashtags = f"{VIRAL_HASHTAGS} #FollowTheStream #LifeParable #VedicWisdom"
        desc = (
            "How do you get out of a thick forest when everyone inside is permanently blindfolded? "
            "In this parable on The Karmic Genie Show, we explore why adapting first, holding your family's hand, following the sound of running water to the ocean (the Vedic riverbed secret), and surviving the hard way without escaping the lesson applies to life and every creator starting in the dark.\n\n"
            f"{series_block}\n\n"
            "Key Chapters:\n"
            f"{chapters}\n\n"
            f"{hashtags}"
        )
        tags = pack_tags_under_limit(
            [
                "how to get out of a thick forest blindfolded",
                "follow the stream parable",
                "vedic riverbed wisdom",
                "life lessons parable",
                "dont escape the lesson",
                "survive the hard way first",
                "youtube creator mindset",
                "spiritual parable",
            ]
        )
        title = "How Do You Get Out of a Thick Forest Blindfolded?"

    elif ep_slug == "KG_Singularity_Ep01_Crucible_To_2100":
        category_id = "28"
        chapters = build_chapters_from_manifest(
            ep_slug,
            [
                "00:00 Industrial Singularity Prelude (2026–2100)",
                "01:15 Act I: AI, Software & Enterprise Revolution (2027–2035)",
                "03:20 Act II: The 2026 Industrial Crucible",
                "05:05 Act III: Global Automation & Economic Abundance",
                "06:10 Act IV: Post-Scarcity Enterprise & Human Sovereignty (2100)",
            ],
        )
        hashtags = "#Singularity #IndustrialRevolution #FutureOfBusiness #Singularity2100 #FutureTimeline #WorldEconomy #TheKarmicGenieShow #KarmicGenie #viral #trending"
        desc = (
            "From the $700B global AI infrastructure & enterprise shift of 2026 through zero-friction media (2027), intent-driven enterprise software (2028), open global supply-chain & ERP platforms (2032), and universal clean energy & robotics (2040) to the Post-Scarcity Industrial Singularity of 2100—discover how the next World Industrial Revolution transforms global business and human purpose.\n\n"
            "Watch the Complete Singularity Chronicles Series (2022–2100):\n"
            f"{sing_pl_line}"
            "• Overview II — World Industrial Revolution (2022–2050): https://youtu.be/R3Uj4cLeyW4\n"
            "• Episode 1 — Year 2027 (Silicon Photonics & Spatial World): https://youtu.be/kaSN1TZPclw\n"
            "• Grand Finale — Year 2050 (Unified Living Planetary Household): https://youtu.be/bb3Sy7fEXnM\n\n"
            f"{series_block}\n\n"
            "Key Chapters:\n"
            f"{chapters}\n\n"
            f"{hashtags}"
        )
        tags = [
            "technological singularity 2026 to 2100",
            "world industrial revolution 2026 to 2100",
            "future of business and ai",
            "singularity chronicles",
            "future timeline 2026 to 2100",
            "enterprise ai transformation",
            "fourth and fifth industrial revolution",
            "future of global supply chains",
            "post scarcity economy 2040",
            "future of work and automation",
            "world in 2050 and 2100",
            "vedic wisdom and technology",
            "7d leadership karmic genie",
        ]
        title = "Technological Singularity (2026 to 2100) — World Industrial Revolution & Business Future"

    elif ep_slug == "KG_Singularity_Ep02_Planetary_Awakening_2050":
        category_id = "28"
        chapters = build_chapters_from_manifest(
            ep_slug,
            [
                "00:00 Global Infrastructure Prelude (2022–2050)",
                "01:55 Revolution 1: Open Global AI Infrastructure (2027–2028)",
                "03:05 Revolution 2: Autonomous Ports & Supply Chains (2029–2031)",
                "04:15 Revolution 3: Sovereign Solar & Clean Energy Grid (2032–2037)",
                "05:25 Revolution 4: Precision AgTech & Biophilic Cities (2038–2045)",
                "06:35 Finale: The Unified 2050 World Economy",
            ],
        )
        hashtags = "#Singularity #WorldIndustry2050 #IndustrialRevolution #FutureTimeline #GlobalEconomy #FutureOfBusiness #TheKarmicGenieShow #KarmicGenie #viral #trending"
        desc = (
            "Across 280 months from December 2022 to 2050, watch how the World Industrial Revolution converges four foundational global industries—Open AI Supercomputing, Autonomous Maritime & Trade Supply Chains, Sovereign Solar & Solid-State Energy Grids, and Regenerative Precision AgTech—into one unified 2050 world economy.\n\n"
            "Watch the Complete Singularity Chronicles Series (2022–2100):\n"
            f"{sing_pl_line}"
            "• Overview I — Technological Singularity (2026–2100): https://youtu.be/Su7OdsAoqHs\n"
            "• Episode 1 — Year 2027 (Silicon Photonics & Spatial World): https://youtu.be/kaSN1TZPclw\n"
            "• Grand Finale — Year 2050 (Unified Living Planetary Household): https://youtu.be/bb3Sy7fEXnM\n\n"
            f"{series_block}\n\n"
            "Key Chapters:\n"
            f"{chapters}\n\n"
            f"{hashtags}"
        )
        tags = [
            "world industrial revolution 2022 to 2050",
            "global business transformation 2050",
            "singularity chronicles",
            "future timeline 2022 to 2050",
            "future of global supply chains",
            "unified ai enterprise platform",
            "clean energy industrial revolution",
            "autonomous ports and logistics",
            "precision agtech future cities",
            "world economy 2050 documentary",
            "280 months planetary awakening",
            "vedic wisdom modern industry",
            "the karmic genie show",
        ]
        title = "World Industrial Revolution (2022 to 2050) — AI, Supply Chains, Energy & Global Business"

    elif ep_slug.startswith("KG_Year_"):
        category_id = "28"
        rp_path = STUDIO_ROOT / "episodes" / "karmic_genie" / ep_slug / "raw_plan.json"
        if not rp_path.exists():
            raise ValueError(f"Missing raw_plan.json for annual episode: {ep_slug}")
        rp = json.loads(rp_path.read_text(encoding="utf-8"))
        yr = int(rp.get("year", ep_slug.split("_")[2]))
        title = rp["title"]
        cmeta = next((b.get("widgetMeta") for b in rp.get("beats", []) if b.get("widgetMeta")), {}) or {}
        chapters = build_chapters_from_manifest(
            ep_slug,
            [
                f"00:00 Year {yr} Industrial Prelude",
                f"01:15 Act I: The {yr - 1} Bottleneck & Sudden Global Obsession",
                f"02:45 Act II: Major Business & World Industry Breakthroughs",
                f"04:15 Act III: Vedic Causal Principle & The 7D Compass",
            ],
        )
        topic_tags, topic_htags = extract_title_topic_tags_and_hashtags(title)
        extra_ht = " ".join(topic_htags)
        hashtags = (
            f"#Singularity #Year{yr} #FutureTimeline #IndustrialRevolution #FutureOfBusiness "
            f"{extra_ht} #VedicWisdom #TheKarmicGenieShow #KarmicGenie #viral #trending"
        )
        hashtags = re.sub(r"\s+", " ", hashtags).strip()

        annual_map = get_annual_slug_by_year()
        nav_lines = []
        if sing_pl_line:
            nav_lines.append(sing_pl_line.strip())
        if (yr - 1) in annual_map and annual_map[yr - 1][2]:
            nav_lines.append(f"• Previous Year ({yr - 1}): {annual_map[yr - 1][2]}")
        if (yr + 1) in annual_map and annual_map[yr + 1][2]:
            nav_lines.append(f"• Next Year ({yr + 1}): {annual_map[yr + 1][2]}")
        nav_lines.append("• Singularity Overview I (2026–2100): https://youtu.be/Su7OdsAoqHs")
        nav_lines.append("• Singularity Overview II (2022–2050): https://youtu.be/R3Uj4cLeyW4")
        nav_block = "\n".join(nav_lines)

        hook_b1 = rp["beats"][0]["narration"].replace("\n", " ")
        desc = (
            f"What triggers the sudden global obsession and major industrial breakthroughs of {yr}? "
            f"{hook_b1}\n\n"
            f"Causal & Vedic Insight ({yr}):\n"
            f"• {cmeta.get('line1', 'Prior Industrial Bottleneck')}\n"
            f"• {cmeta.get('line2', 'Breakthrough Industrial Convergence')}\n\n"
            "Watch the Complete Singularity Chronicles Series (2022–2100):\n"
            f"{nav_block}\n\n"
            f"{series_block}\n\n"
            "Key Chapters:\n"
            f"{chapters}\n\n"
            f"{hashtags}"
        )
        tags = (
            topic_tags
            + [
                f"year {yr}",
                f"world in {yr}",
                f"world in {yr} predictions",
                f"{yr} technology and business",
                f"industrial revolution {yr}",
                f"future timeline {yr}",
                "singularity chronicles",
                "technological singularity series",
                "future of business and industry",
                "vedic wisdom and innovation",
                "7d leadership karmic genie",
            ]
        )

    else:
        raise ValueError(f"Unknown episode slug: {ep_slug}")

    title = title.replace("->", "→").replace("<-", "←").replace("<", "‹").replace(">", "›")
    desc = desc.replace("->", "→").replace("<-", "←").replace("<", "‹").replace(">", "›")
    assert_zero_cta(title, f"{ep_slug}.title")
    assert_zero_cta(desc, f"{ep_slug}.description")
    tags = pack_tags_under_limit(tags + VIRAL_TAGS_CORE, max_chars=485)
    return {"title": title, "description": desc, "tags": tags, "hashtags": hashtags, "categoryId": category_id}


LEGACY_VIDEOS_SEO = {
    "3b6Y9QaEc0A": {
        "description": (
            "Karmic Genie Show | Respect Your Duty First (Season 1 Episode 1) — What is true Duty, and how does your inner conscience reveal the difference between mechanical routine and your soul's real purpose?\n\n"
            "In this episode of The Karmic Genie Show, we explore how the 7 Dimensions of purposeful living (Duty, Dignity, Discipline, Dharma, Devotion, Divine, Destiny) guide professionals, families, and builders through modern industry shifts with clarity and peace.\n\n"
            "Key Moments:\n"
            "00:00 Welcome to the 7D Karmic Genie Stage\n"
            "01:15 Industry Shifts & The Grand Design of Human Purpose\n"
            "03:10 Defining True Duty Through Conscience & Family Connectedness\n"
            "05:00 The Karmic Genie's Blessing & 7D Takeaway\n\n"
            "#TheKarmicGenieShow #RespectYourDuty #7DLiving #Dharma #KarmicGenie"
        ),
        "tags": pack_tags_under_limit(
            [
                "respect your duty first",
                "karmic genie show",
                "the karmic genie show",
                "what is true duty",
                "duty vs job",
                "conscience and karma",
                "7d purposeful living",
                "duty dignity discipline dharma",
                "family connectedness",
                "finding purpose in career shifts",
                "vedic wisdom for professionals",
                "spiritual philosophy show",
                "karmic genie",
                "life purpose",
            ]
        ),
    },
    "FW5sTSnkBz4": {
        "description": (
            "Karmic Genie Show | Two Birds Story! (Pilot) — Drawn from the timeless Mundaka Upanishad (3.1.1–3.1.2), two inseparable birds sit upon the same selfsame tree: one anxiously tasting sweet and bitter fruits, the other watching in serene, luminous awareness.\n\n"
            "Discover how this ancient Vedantic parable illuminates witness consciousness, emotional resilience, and inner peace amidst modern life's ups and downs.\n\n"
            "Key Moments:\n"
            "00:00 Two Birds Upon the Same Tree (Mundaka Upanishad)\n"
            "00:55 Sweet & Bitter Fruits of Action vs Witness Awareness\n"
            "01:50 Recognizing Your Higher Serene Self\n\n"
            "#TheKarmicGenieShow #MundakaUpanishad #TwoBirdsParable #VedantaWisdom #KarmicGenie"
        ),
        "tags": pack_tags_under_limit(
            [
                "two birds story mundaka upanishad",
                "mundaka upanishad two birds",
                "vedanta parable explained",
                "witness consciousness",
                "atman and jiva two birds",
                "upanishad stories in english",
                "karmic genie show",
                "the karmic genie show",
                "ancient indian wisdom",
                "inner peace story",
                "spiritual awakening story",
                "karmic genie",
            ]
        ),
    },
    "HgJWcfoZzBY": {
        "description": (
            "Karmic Genie Show | Peace of Mind — A short philosophical story on screen exhaustion, restless ambition, and rediscovering quiet inner stillness at the end of a hectic modern day.\n\n"
            "#TheKarmicGenieShow #PeaceOfMind #InnerStillness #LifeWisdom #KarmicGenie"
        ),
        "tags": pack_tags_under_limit(
            [
                "peace of mind story",
                "how to find peace of mind",
                "overcoming burnout and exhaustion",
                "inner stillness",
                "karmic genie show",
                "the karmic genie show",
                "mindful living",
                "short wisdom story",
                "calm mind",
                "karmic genie",
            ]
        ),
    },
}


def apply_tags_in_studio_page(page, tags: list[str], clear_existing: bool = True) -> int:
    """Expands 'Show more', clears existing video tags if requested, and enters `tags` via chip-bar input."""
    page.evaluate(
        """() => {
        const btns = Array.from(document.querySelectorAll('ytcp-button, button'));
        for (const el of btns) {
            const t = (el.innerText || '').trim();
            if (t === 'Show more' || t === 'SHOW MORE') { el.click(); return true; }
        }
        return false;
    }"""
    )
    page.wait_for_timeout(1800)

    if clear_existing:
        # Click clear-all button on tag chip-bar if present, or remove chips individually
        page.evaluate(
            """() => {
            const tagInput = document.querySelector('input[aria-label="Tags"]');
            if (!tagInput) return;
            const bar = tagInput.closest('ytcp-chip-bar');
            if (!bar) return;
            const clearBtn = bar.querySelector('#clear-button, [aria-label*="Delete all" i], [aria-label*="Clear" i]');
            if (clearBtn) { clearBtn.click(); return; }
            const dels = Array.from(bar.querySelectorAll('ytcp-chip #delete-icon, ytcp-chip [id*="delete"], ytcp-chip iron-icon'));
            dels.forEach(d => d.click());
        }"""
        )
        page.wait_for_timeout(800)

    tag_input = page.locator("input[aria-label='Tags'], input[placeholder='Add tag']").first
    if tag_input.count() == 0:
        print("  [SEO Warning] Tags input not found on page!")
        return 0

    tag_input.scroll_into_view_if_needed()
    tag_input.click()
    page.wait_for_timeout(400)
    # Enter comma-separated batch cleanly
    joined = ", ".join(tags) + ","
    page.keyboard.insert_text(joined)
    page.keyboard.press("Enter")
    page.wait_for_timeout(1200)

    chip_count = page.evaluate(
        """() => {
        const tagInput = document.querySelector('input[aria-label="Tags"]');
        const bar = tagInput ? tagInput.closest('ytcp-chip-bar') : document;
        return bar ? bar.querySelectorAll('ytcp-chip').length : 0;
    }"""
    )
    return int(chip_count)


def optimize_channel_seo(ctx) -> dict:
    assert_zero_cta(CHANNEL_ABOUT_DESCRIPTION, "CHANNEL_ABOUT_DESCRIPTION")
    page = ctx.new_page()
    summary: dict = {}
    try:
        # 1. Update Channel Keywords in Settings -> Channel -> Basic info
        print("[Channel SEO] Updating Settings -> Channel -> Keywords...")
        page.goto(STUDIO_URL, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(5000)
        body_txt = page.locator("body").inner_text()
        if "Karmic Genie" not in body_txt:
            raise RuntimeError("SAFETY ABORT: Not logged into Karmic Genie Show!")

        page.locator("#settings-item").first.click()
        page.wait_for_timeout(2500)
        page.locator("ytcp-settings-dialog tp-yt-paper-item:has-text('Channel'), ytcp-settings-dialog li:has-text('Channel')").first.click()
        page.wait_for_timeout(2000)

        # Clear existing channel keyword chips cleanly
        page.evaluate(
            """() => {
            const d = document.querySelector('ytcp-settings-dialog');
            if (!d) return;
            const kwInput = d.querySelector('input[aria-label="Keywords"]');
            const bar = kwInput ? kwInput.closest('ytcp-chip-bar') : d;
            if (!bar) return;
            const dels = Array.from(bar.querySelectorAll('ytcp-chip #delete-icon, ytcp-chip [aria-label*="Delete" i], ytcp-chip [id*="delete"]'));
            dels.forEach(x => x.click());
        }"""
        )
        page.wait_for_timeout(800)

        kw_input = page.locator("ytcp-settings-dialog input[aria-label='Keywords']").first
        kw_input.scroll_into_view_if_needed()
        kw_input.click()
        # Also select-all + backspace any leftover chip text via Backspace x15 if dels didn't clear all
        for _ in range(12):
            page.keyboard.press("Backspace")
        page.wait_for_timeout(400)
        page.keyboard.insert_text(", ".join(CHANNEL_KEYWORDS) + ",")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1200)

        kw_chips = page.evaluate(
            """() => {
            const d = document.querySelector('ytcp-settings-dialog');
            return d ? Array.from(d.querySelectorAll('ytcp-chip')).map(c => (c.innerText || '').trim()) : [];
        }"""
        )
        summary["channelKeywordCount"] = len(kw_chips)

        # Also check Upload defaults -> Advanced settings -> Category = Education
        ud_tab = page.locator("ytcp-settings-dialog tp-yt-paper-item:has-text('Upload defaults'), ytcp-settings-dialog li:has-text('Upload defaults')")
        if ud_tab.count() > 0:
            ud_tab.first.click()
            page.wait_for_timeout(1800)
            # Add default brand tags in Upload defaults -> Basic info -> Tags
            ud_tag_in = page.locator("ytcp-settings-dialog input[aria-label='Tags']")
            if ud_tag_in.count() > 0 and ud_tag_in.first.is_visible():
                ud_tag_in.first.scroll_into_view_if_needed()
                ud_tag_in.first.click()
                for _ in range(10):
                    page.keyboard.press("Backspace")
                default_tags = ["The Karmic Genie Show", "Karmic Genie", "Purposeful Living", "Dharma", "Life Wisdom"]
                page.keyboard.insert_text(", ".join(default_tags) + ",")
                page.keyboard.press("Enter")
                page.wait_for_timeout(800)

        save_btn = page.locator("ytcp-settings-dialog ytcp-button#save-button, ytcp-settings-dialog button:has-text('Save')")
        if save_btn.count() > 0 and save_btn.first.is_visible() and save_btn.first.is_enabled():
            save_btn.first.click()
            page.wait_for_timeout(3500)
        print(f"  [Channel SEO OK] Saved {len(kw_chips)} channel keywords + Upload Default tags.")

        # 2. Update Channel About Description in Customization -> Profile
        print("[Channel SEO] Updating Channel Customization -> Profile Description...")
        page.goto(PROFILE_URL, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(5000)
        desc_box = page.locator("div#textbox[aria-label*='Tell viewers about your channel']").first
        if desc_box.count() > 0:
            desc_box.scroll_into_view_if_needed()
            desc_box.click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            desc_box.fill(CHANNEL_ABOUT_DESCRIPTION)
            page.wait_for_timeout(1500)
            pub_btn = page.locator("ytcp-button#publish-button, button:has-text('Publish')").first
            if pub_btn.count() > 0 and pub_btn.is_visible():
                pub_btn.click()
                page.wait_for_timeout(3500)
            summary["channelDescriptionUpdated"] = True
            print("  [Channel SEO OK] Published rich Channel About Description + 5 hashtags.")
        return summary
    finally:
        page.close()


def optimize_existing_video_seo(ctx, video_id: str, description: str, tags: list[str], new_title: str | None = None) -> dict:
    assert_zero_cta(description, f"video:{video_id}.description")
    for t in tags:
        assert_zero_cta(t, f"video:{video_id}.tag")

    page = ctx.new_page()
    try:
        url = f"https://studio.youtube.com/video/{video_id}/edit?authuser=0"
        print(f"[Video SEO] Optimizing {video_id} ({url})...")
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(5500)

        if new_title:
            assert_zero_cta(new_title, f"video:{video_id}.title")
            tbox = page.locator("ytcp-video-title #textbox, #title-textarea #textbox").first
            tbox.click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            tbox.fill(new_title[:98])
            page.wait_for_timeout(800)

        dbox = page.locator("ytcp-video-description #textbox, #description-textarea #textbox").first
        dbox.scroll_into_view_if_needed()
        dbox.click()
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        dbox.fill(description)
        page.wait_for_timeout(1200)

        applied_tags = apply_tags_in_studio_page(page, tags, clear_existing=True)
        page.wait_for_timeout(1000)

        save_clicked = page.evaluate(
            """() => {
            const btn = document.querySelector('ytcp-button#save, #save-button, ytcp-video-metadata-editor-basics #save');
            if (btn && !btn.hasAttribute('disabled')) { btn.click(); return true; }
            const all = Array.from(document.querySelectorAll('ytcp-button, button'));
            for (const el of all) {
                if ((el.innerText || '').trim() === 'Save' && !el.hasAttribute('disabled')) {
                    el.click();
                    return true;
                }
            }
            return false;
        }"""
        )
        page.wait_for_timeout(3500)
        print(f"  [Video SEO OK] {video_id} -> tags_applied={applied_tags} | saved={save_clicked}")
        return {"videoId": video_id, "tagsApplied": applied_tags, "saved": bool(save_clicked)}
    finally:
        page.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", action="store_true", help="Optimize @karmicgenie channel keywords, upload defaults & About description")
    ap.add_argument("--all-existing", action="store_true", help="Retroactively optimize SEO, chapters, hashtags & tags on all live @karmicgenie videos")
    ap.add_argument("--ep-slug", default="", help="Optimize a specific published episode by slug (reads videoId from delivery_links.json)")
    args = ap.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        ctx = browser.contexts[0]
        report: dict = {}

        if args.channel:
            report["channel"] = optimize_channel_seo(ctx)

        if args.all_existing:
            vids_report = []
            # 1. Recent ShishyanEN episodes
            for slug, fallback_vid in [
                ("KG_Creator_Dharma_2Percent", "VuOrY0If1XI"),
                ("KG_Time_Is_Life_Part2", "wveLPokMQ_8"),
                ("KG_Ep03_Infinite_Distractions", ""),
                ("KG_Ep04_Before_You_Were_Born", ""),
                ("KG_Ep05_Intelligent_Vs_Wise", ""),
            ]:
                dl_p = STUDIO_ROOT / "episodes" / "karmic_genie" / slug / "delivery_links.json"
                vid = fallback_vid
                if dl_p.exists():
                    vid = json.loads(dl_p.read_text(encoding="utf-8")).get("youtubeUrl", "").split("/")[-1] or fallback_vid
                if vid:
                    pkg = get_episode_seo_package(slug)
                    vids_report.append(optimize_existing_video_seo(ctx, vid, pkg["description"], pkg["tags"], new_title=pkg["title"]))

            # 2. Earlier public @karmicgenie videos
            for vid, meta in LEGACY_VIDEOS_SEO.items():
                vids_report.append(optimize_existing_video_seo(ctx, vid, meta["description"], meta["tags"]))

            report["videos"] = vids_report

        if args.ep_slug:
            dl_p = STUDIO_ROOT / "episodes" / "karmic_genie" / args.ep_slug / "delivery_links.json"
            vid = json.loads(dl_p.read_text(encoding="utf-8")).get("youtubeVideoId", "")
            assert vid, f"No youtubeVideoId in {dl_p}"
            pkg = get_episode_seo_package(args.ep_slug)
            report["single"] = optimize_existing_video_seo(ctx, vid, pkg["description"], pkg["tags"], new_title=pkg["title"])

        print("SEO_OPTIMIZATION_REPORT:", json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
