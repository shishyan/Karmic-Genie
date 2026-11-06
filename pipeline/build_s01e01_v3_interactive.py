#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Widescreen (16:9, 1920x1080, 30fps, -14 LUFS) Interactive Broadcast Assembler for:
  Karmic Genie Show — Season 1, Episode 1 (v3.1 Interactive Grand-Design Master)
  "200,000 Cuts, 60,000 Buyouts & Why Every One Is a Blessing in Disguise"

Mandatory Editorial, Philosophical & Broadcast Guarantees:
  1. Grand Design Philosophy (ZERO Blame / ZERO Portraying Anyone in a Bad Spot):
     - Every company, industry, employee, city, and country serves a purpose—akin to critical
       organs, vessels, and renewing cells in Earth's living body serving mind, soul, and para-soul.
     - Corporate restructurings and 60,000-person Voluntary Buyout bridges are framed as minor
       career hiccups that relieve deeper pressure points of overdue family reunions and duties.
     - Strictly ZERO "record profits", ZERO "corporate greed", ZERO company names, and ZERO
       real/fictional person names anywhere in audio, badges, or subtitles!
  2. Brisk 1.0x Natural Broadcast Pacing:
     - ZERO rubberband slow-down, ZERO tpad freeze-frames!
     - Whisper (`tiny.en` on 16kHz mono WAV numpy array) verifies `(sp_st, sp_en)` on every spoken
       clip (filtering out non-speech crowd tokens like `APPLAUSE`) and trims cleanly to
       `[max(0.0, sp_st - 0.16), min(dur, sp_en + 0.22)]`.
  3. Picture-in-Studio 75% Clip / 25% Studio Visible (`pip75`) Compositing:
     - All external/story clips play inside a `1480x832` foreground window with a crisp `4px`
       brushed-gold border (`#EBC670`) at `(216, 158)` over `v6_7d_dormant_stage_16x9.jpg`
       (`eq=brightness=-0.06:saturation=0.95` + subtle slow pan) so ~25% of the live studio
       (vaulted ceiling, left/right blue stadium audience, and white marble floor) stays visible!
  4. 100% Readable Dark-Shaded Subtitles (`BorderStyle=3`):
     - `OutlineColour=&H38080A10`, `BackColour=&H38080A10`, `Outline=11.0`, `Shadow=0.0`,
       single-line sequential events so boxes never overlap or collide!
"""

import json
import re
import shutil
import subprocess
import wave
from pathlib import Path
import numpy as np

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
MASTERS_DIR = REPO_DIR / "assets" / "studio_v5_masters"
DORMANT_STAGE_JPG = MASTERS_DIR / "v6_7d_dormant_stage_16x9.jpg"
THEME_WAV = REPO_DIR / "assets" / "theme" / "official_karmic_genie_7d_theme_song.wav"
LOGO_JPG = REPO_DIR / "assets" / "logo" / "official_karmic_genie_show_logo.jpg"

EP_DIR = REPO_DIR / "episodes" / "S01E01_Employees_vs_Tech_CEO"
V3_CLIPS_ROOT = EP_DIR / "flow_v3_interactive_clips"
V1_CLIPS_ROOT = EP_DIR / "flow_16x9_clips"
OVERLAYS_V3_DIR = EP_DIR / "overlays_v3"
TEMP_DIR = EP_DIR / "temp_v3_film_build"

OUT_MP4 = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E01_v3_Interactive_16x9.mp4"
ARTIFACT_DIR = Path("/home/shishyan/.gemini/antigravity/brain/b55fc9ea-1a2e-45b9-8d71-a53ee11caf0c")
ARTIFACT_MP4 = ARTIFACT_DIR / "Karmic_Genie_Show_S01E01_v3_Interactive_16x9.mp4"

FORBIDDEN_NAMES = (
    "marcus", "arjun", "elena", "mateo", "kenji", "heinrich", "kavitha",
    "amazon", "google", "alphabet", "microsoft", "meta", "apple", "oracle",
    "dell", "cisco", "intel", "ups", "tcs", "infosys", "wipro", "hsbc", "citi",
)

FORBIDDEN_BLAME_PHRASES = (
    "record profit", "corporate greed", "heartless",
)

NON_SPEECH_HALLUCINATIONS = {"applause", "[applause]", "(applause)", "music", "[music]"}

# Canonical 31-shot Grand-Design Interactive Broadcast Ledger:
V3_SHOT_LEDGER = [
    # --- INTERACTIVE WELCOME & GRAND-DESIGN STAGE-SETTER (STUDIO FULL) ---
    {
        "sid": "01_Welcome_Home",
        "src": V3_CLIPS_ROOT / "v3_b1_welcome" / "v3_b1_welcome_03.mp4",
        "hint_sp": (0.80, 7.38),
        "layout": "full",
        "voice": "human",
        "overlay": None,
        "lines": [
            "Welcome home to Karmic Genie Show—",
            "whether you're in our circle tonight or watching from your living room!",
        ],
    },
    {
        "sid": "02_Show_Of_Hands",
        "src": V3_CLIPS_ROOT / "v3_b1_welcome" / "v3_b1_welcome_01.mp4",
        "hint_sp": (0.90, 7.32),
        "layout": "full",
        "voice": "human",
        "overlay": "v3_ov_poll.png",
        "lines": [
            "Raise your hand—and comment at home—",
            "if someone you know faced a buyout or layoff!",
        ],
    },
    {
        "sid": "03_Prologue_Since_2025",
        "src": V1_CLIPS_ROOT / "batch_01_prologue" / "batch_01_prologue_06.mp4",
        "hint_sp": (0.75, 7.31),
        "layout": "full",
        "voice": "human",
        "overlay": None,
        "lines": [
            "Before anyone speaks tonight, let's take sixty quiet seconds",
            "to see what happened since early 2025.",
        ],
    },
    {
        "sid": "04_200K_CrossSector",
        "src": V3_CLIPS_ROOT / "v3_b1_welcome" / "v3_b1_welcome_02.mp4",
        "hint_sp": (1.06, 7.72),
        "layout": "full",
        "voice": "human",
        "overlay": None,
        "lines": [
            "Over 200,000 roles shifted this year",
            "across tech, banking, shipping, auto, and support.",
        ],
    },
    {
        "sid": "05_720B_Infrastructure",
        "src": V1_CLIPS_ROOT / "batch_01_prologue" / "batch_01_prologue_03.mp4",
        "hint_sp": (0.00, 7.64),
        "layout": "full",
        "voice": "human",
        "overlay": None,
        "lines": [
            "Today, infrastructure spending exceeds $720 billion a year—",
            "reshaping every industry's cash flow.",
        ],
    },

    # --- ACT I: LIVE EXECUTIVE DIALOGUE FIRST — INDUSTRIES AS VITAL ORGANS (STUDIO FULL) ---
    {
        # Verified via Whisper: `v3_gd_02.mp4` speaks "Every industry, company and city is a vital organ..."
        "sid": "06_Host_Grand_Design_Organ",
        "src": V3_CLIPS_ROOT / "v3_grand_design" / "v3_gd_02.mp4",
        "hint_sp": (0.37, 7.69),
        "layout": "full",
        "voice": "human",
        "overlay": "v3_ov_ceo.png",
        "lines": [
            "Every industry, company, and city is a vital organ in Earth's living body—",
            "how is AI reshaping our circulation today?",
        ],
    },
    {
        "sid": "07_CEO_50B_Circulation",
        "src": V1_CLIPS_ROOT / "batch_02_scene1_sf_mysuru" / "batch_02_scene1_sf_mysuru_02.mp4",
        "hint_sp": (0.00, 7.78),
        "layout": "full",
        "voice": "human",
        "overlay": None,
        "lines": [
            "$50 billion a quarter on GPUs flipped free cash flow negative.",
            "Cloud and AI demand every dollar right now.",
        ],
    },
    {
        "sid": "08_CEO_Structural_Renewal",
        "src": V1_CLIPS_ROOT / "batch_02_scene1_sf_mysuru" / "batch_02_scene1_sf_mysuru_04.mp4",
        "hint_sp": (0.27, 7.59),
        "layout": "full",
        "voice": "human",
        "overlay": "v3_ov_layers.png",
        "lines": [
            "If I keep funding non-AI devices and middle layers,",
            "in four years 90,000 jobs vanish instead of 30,000.",
        ],
    },

    # --- ACT II: STORIES ON DEMAND (75% CLIP WINDOW / 25% STUDIO VISIBLE + INLINE CUTS) ---
    {
        "sid": "09_Expat_Father_Phone_PiP",
        "src": V1_CLIPS_ROOT / "batch_02_scene1_sf_mysuru" / "batch_02_scene1_sf_mysuru_03.mp4",
        "hint_sp": (0.92, 7.60),
        "layout": "pip75",
        "voice": "human",
        "overlay": "v3_ov_expat.png",
        "lines": [
            "Millions of us work outside our home countries—",
            "telling ourselves we left just briefly to earn dollars.",
        ],
    },
    {
        "sid": "10_Expat_Ghost_At_Home_Split",
        "src": V1_CLIPS_ROOT / "batch_02_scene1_sf_mysuru" / "batch_02_scene1_sf_mysuru_01.mp4",
        "hint_sp": (0.53, 7.85),
        "layout": "split_full_to_pip75",
        "v1_full_mp4": V1_CLIPS_ROOT / "batch_05_scene4_punchline_and_awakening" / "batch_05_scene4_punchline_and_awakening_01.mp4",
        "v1_full_ss": 0.00,
        "v1_head_dur": 3.50,
        "v2_pip_mp4": V1_CLIPS_ROOT / "batch_02_scene1_sf_mysuru" / "batch_02_scene1_sf_mysuru_03.mp4",
        "v2_pip_ss": 2.10,
        "voice": "human",
        "overlay": None,
        "lines": [
            "I wasn't in AI—I built consumer devices for twelve years.",
            "Chasing dollars and visas, I became a ghost at home.",
        ],
    },
    {
        "sid": "11_Mum_Missed_Bedtimes_PiP",
        "src": V1_CLIPS_ROOT / "topup_clean" / "rec_s2_02_elena.mp4",
        "hint_sp": (0.00, 7.40),
        "layout": "pip75",
        "voice": "human",
        "overlay": "v3_ov_mum.png",
        "lines": [
            "When companies flattened over 35% of small-team managers,",
            "seven years of missed bedtimes vanished.",
        ],
    },
    {
        "sid": "12_Munich_Veteran_58_PiP",
        "src": V1_CLIPS_ROOT / "topup_clean" / "tu2_munich_coimbatore_02.mp4",
        "hint_sp": (1.00, 7.42),
        "layout": "pip75",
        "voice": "human",
        "overlay": "v3_ov_veteran.png",
        "lines": [
            "At fifty-eight in Munich, thirty-five years becomes 'legacy.'",
            "How do we leave gracefully?",
        ],
    },
    {
        "sid": "13_Tokyo_Hiring_Freeze_PiP",
        "src": V1_CLIPS_ROOT / "batch_04_scene3_tokyo_munich_coimbatore" / "batch_04_scene3_tokyo_munich_coimbatore_05.mp4",
        "hint_sp": (0.00, 7.30),
        "layout": "pip75",
        "voice": "human",
        "overlay": "v3_ov_dispatch.png",
        "lines": [
            "In Tokyo, I maintain non-cloud retail billing",
            "inside the surviving 80% under a strict hiring freeze.",
        ],
    },
    {
        "sid": "14_Tokyo_Five_Pagers_PiP",
        "src": V1_CLIPS_ROOT / "batch_04_scene3_tokyo_munich_coimbatore" / "batch_04_scene3_tokyo_munich_coimbatore_02.mp4",
        "hint_sp": (0.92, 7.44),
        "layout": "pip75",
        "voice": "human",
        "overlay": None,
        "lines": [
            "Four teammates left with zero replacements approved.",
            "My wife eats alone every night while I carry five pagers.",
        ],
    },
    {
        "sid": "15_SaoPaulo_First_Rung_PiP",
        "src": V1_CLIPS_ROOT / "batch_03_scene2_london_saopaulo" / "batch_03_scene2_london_saopaulo_02.mp4",
        "hint_sp": (1.50, 7.48),
        "layout": "pip75",
        "voice": "human",
        "overlay": None,
        "lines": [
            "In São Paulo, nobody laid me off—",
            "the first rung simply vanished before I could step on it.",
        ],
    },
    {
        "sid": "16_SaoPaulo_7Pct_Grads_PiP",
        "src": V1_CLIPS_ROOT / "batch_03_scene2_london_saopaulo" / "batch_03_scene2_london_saopaulo_01.mp4",
        "hint_sp": (0.00, 7.36),
        "layout": "pip75",
        "voice": "human",
        "overlay": None,
        "lines": [
            "New graduates dropped to 7% of Big Tech hires.",
            "My father sewed suits twenty years—where do we start?",
        ],
    },
    {
        "sid": "17_Bengaluru_Courtyard_PiP",
        "src": V1_CLIPS_ROOT / "batch_04_scene3_tokyo_munich_coimbatore" / "batch_04_scene3_tokyo_munich_coimbatore_01.mp4",
        "hint_sp": (0.00, 6.86),
        "layout": "pip75",
        "voice": "human",
        "overlay": None,
        "lines": [
            "I led internal talent tools in Bengaluru—",
            "one of the first non-AI teams automated earlier this year.",
        ],
    },
    {
        "sid": "18_Coimbatore_Peace_PiP",
        "src": V1_CLIPS_ROOT / "topup_clean" / "tu2_munich_coimbatore_01.mp4",
        "hint_sp": (1.38, 6.44),
        "layout": "pip75",
        "voice": "human",
        "overlay": None,
        "lines": [
            "Coimbatore cut my pay, erased rent, and brought peace—",
            "did I arrive early?",
        ],
    },

    # --- HOST BRIDGES & SUMMONS THE KARMIC GENIE (STUDIO FULL) ---
    {
        "sid": "19_Host_Bridge_Seven_Chairs",
        "src": V1_CLIPS_ROOT / "batch_05_scene4_punchline_and_awakening" / "batch_05_scene4_punchline_and_awakening_03.mp4",
        "hint_sp": (0.00, 7.68),
        "layout": "full",
        "voice": "human",
        "overlay": None,
        "lines": [
            "From $200 billion in San Francisco to a quiet courtyard in Coimbatore—",
            "no spreadsheet answers all seven chairs.",
        ],
    },
    {
        "sid": "20_Host_Summon_Genie",
        "src": V1_CLIPS_ROOT / "topup_clean" / "plate_s4_03_punchline.mp4",
        "hint_sp": (0.96, 6.90),
        "layout": "full",
        "voice": "human",
        "overlay": None,
        "lines": [
            "Let's quiet the room and ask together:",
            "What does Genie say — the 7D way?",
        ],
    },

    # --- ACT III: SHORT, CRISP CROSS-LEGGED KARMIC GENIE (~22s TOTAL, ZERO LONG LECTURE!) ---
    {
        "sid": "21_Genie_Lamp_Awaken",
        "src": V1_CLIPS_ROOT / "batch_05_scene4_punchline_and_awakening" / "batch_05_scene4_punchline_and_awakening_02.mp4",
        "layout": "visual_full",
        "visual_dur": 3.20,
        "pts_mul": 0.50,
        "voice": "genie",
        "overlay": "v3_ov_genie.png",
        "lines": [],
    },
    {
        "sid": "22_Genie_Single_Thunderclap",
        "src": V1_CLIPS_ROOT / "batch_06_scene5_wise_saint_mirror" / "batch_06_scene5_wise_saint_mirror_03.mp4",
        "hint_sp": (0.00, 7.60),
        "layout": "full",
        "voice": "genie",
        "overlay": None,
        "lines": [
            "Like the ancient Upanishad parable of the Single Thunderclap—",
            "a two-minute story you might enjoy reading quietly at home tonight...",
        ],
    },
    {
        "sid": "23_Genie_Golden_Handcuffs",
        "src": V1_CLIPS_ROOT / "topup_clean" / "rec_s6_05_genie_handcuffs.mp4",
        "hint_sp": (1.04, 6.84),
        "layout": "full",
        "voice": "genie",
        "overlay": None,
        "lines": [
            "When a closed non-AI floor loosens those golden handcuffs",
            "while aging parents still wait...",
        ],
    },
    {
        "sid": "24_Genie_Blessing_In_Disguise",
        "src": V1_CLIPS_ROOT / "topup_clean" / "plate_s6_05b_blessing.mp4",
        "layout": "visual_full",
        "visual_dur": 2.40,
        "pts_mul": 0.55,
        "voice": "genie",
        "overlay": None,
        "lines": [
            "...every single one is a blessing in disguise!",
        ],
    },
    {
        "sid": "25_Genie_Lotus_Dissolve",
        "src": V1_CLIPS_ROOT / "topup_clean" / "plate_s7_03_lotus_dissolve.mp4",
        "layout": "visual_full",
        "visual_dur": 2.50,
        "pts_mul": 0.45,
        "voice": "genie",
        "overlay": None,
        "lines": [],
    },

    # --- ACT IV: CONNECTING THE DOTS — BODY, MIND, SOUL & OVERDUE FAMILY REUNIONS ---
    {
        # Verified via Whisper: `v3_gd_01.mp4` speaks "Just as human cells renew to serve mind, soul and para-soul..."
        "sid": "26_Host_Body_Mind_Soul",
        "src": V3_CLIPS_ROOT / "v3_grand_design" / "v3_gd_01.mp4",
        "hint_sp": (0.18, 7.70),
        "layout": "full",
        "voice": "human",
        "overlay": None,
        "lines": [
            "Just as human cells renew to serve mind, soul, and para-soul—",
            "this minor hiccup serves a grander design of overdue reunions!",
        ],
    },
    {
        "sid": "27_Host_Why_Handcuffs",
        "src": V3_CLIPS_ROOT / "v3_host_expansion" / "v3_host_exp_02.mp4",
        "hint_sp": (0.05, 6.95),
        "layout": "full",
        "voice": "human",
        "overlay": None,
        "lines": [
            "Every single one is a blessing in disguise!",
            "Why? Nobody unlocks golden handcuffs on their own!",
        ],
    },
    {
        # Cuts inline for the last 2.5s to the 75% Studio Window of the sunlit South Indian reunion courtyard!
        "sid": "28_Host_Overdue_Reunion_Split",
        "src": V3_CLIPS_ROOT / "v3_host_expansion" / "v3_host_exp_04.mp4",
        "hint_sp": (0.00, 7.58),
        "layout": "split_tail_pip75",
        "v2_pip_mp4": V1_CLIPS_ROOT / "batch_04_scene3_tokyo_munich_coimbatore" / "batch_04_scene3_tokyo_munich_coimbatore_01.mp4",
        "v2_pip_ss": 2.20,
        "tail_pip_dur": 2.50,
        "voice": "human",
        "overlay": None,
        "lines": [
            "Millions abroad postpone duty to aging parents—",
            "twelve months' buyout pay brings that overdue reunion home guilt-free!",
        ],
    },
    {
        "sid": "29_Host_50s_Dignity",
        "src": V3_CLIPS_ROOT / "v3_host_expansion" / "v3_host_exp_03.mp4",
        "hint_sp": (1.14, 6.92),
        "layout": "full",
        "voice": "human",
        "overlay": None,
        "lines": [
            "In your fifties or flattened from management?",
            "Take the runway with Dignity—and fulfill your true purpose!",
        ],
    },
    {
        "sid": "30_Host_No_Single_Answer",
        "src": V1_CLIPS_ROOT / "batch_08_scene7_finale" / "s7b_host_01.mp4",
        "hint_sp": (0.72, 7.56),
        "layout": "full",
        "voice": "human",
        "overlay": None,
        "lines": [
            "No single answer fits twenty-three in São Paulo, thirty-nine in Seattle,",
            "fifty-eight in Munich, or San Francisco.",
        ],
    },
    {
        "sid": "31_Host_Interactive_Signoff",
        "src": V1_CLIPS_ROOT / "topup_clean" / "plate_s7_05_signoff.mp4",
        "hint_sp": (0.00, 6.26),
        "layout": "full",
        "voice": "human",
        "overlay": None,
        "lines": [
            "Only you know your quiet thunder tonight...",
            "What does Genie say — the 7D way?",
        ],
    },
]


def assert_editorial_purity(text: str, context: str):
    low = text.lower()
    for bad in FORBIDDEN_NAMES:
        if re.search(rf"\b{re.escape(bad)}\b", low):
            raise ValueError(f"Forbidden company/person name '{bad}' detected in {context}: {text}")
    for phrase in FORBIDDEN_BLAME_PHRASES:
        if phrase in low:
            raise ValueError(f"Forbidden blame phrase '{phrase}' detected in {context}: {text}")


def probe_duration(path: Path) -> float:
    res = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)
    ]).decode())
    return float(res["format"]["duration"])


def has_audio_stream(path: Path) -> bool:
    res = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "json", str(path)
    ]).decode())
    return any(s.get("codec_type") == "audio" for s in res.get("streams", []))


def format_ass_time(sec: float) -> str:
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def transcribe_clip_whisper(mp4_path: Path, model, fallback_bounds: tuple[float, float]) -> tuple[str, float, float, float]:
    """
    Transcribes `mp4_path` using Whisper `tiny.en` on a 16kHz mono WAV numpy array
    to detect exact `(sp_st, sp_en)` speech timestamps (ignoring trailing crowd hallucinations).
    """
    dur = probe_duration(mp4_path)
    if not has_audio_stream(mp4_path):
        return ("", fallback_bounds[0], min(dur, fallback_bounds[1]), dur)

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    wav_tmp = TEMP_DIR / f"w_{mp4_path.parent.name}_{mp4_path.stem}.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(mp4_path), "-vn", "-ac", "1", "-ar", "16000", str(wav_tmp)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with wave.open(str(wav_tmp), "rb") as wf:
        arr = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0

    segs, _ = model.transcribe(arr, word_timestamps=True, vad_filter=True)
    words = []
    txt_parts = []
    for s in segs:
        if s.words:
            for w in s.words:
                clean_w = w.word.strip().lower()
                if clean_w in NON_SPEECH_HALLUCINATIONS:
                    continue
                words.append((w.start, w.end))
                txt_parts.append(w.word.strip())

    full_txt = " ".join(txt_parts).lower().strip()
    if words and (words[-1][1] - words[0][0]) >= 2.0:
        sp_st = float(words[0][0])
        sp_en = float(words[-1][1])
    else:
        sp_st, sp_en = float(fallback_bounds[0]), min(dur, float(fallback_bounds[1]))

    return (full_txt, sp_st, sp_en, dur)


def render_cold_open_v3(out_mp4: Path) -> float:
    """
    Builds the crisp 9.5s Cold Open:
      - 5.5s crane push on `v6_7d_dormant_stage_16x9.jpg`
      - 4.0s close pan across the `v6` 7D wall & padded `Karmic Genie Show` logo
    """
    c1 = TEMP_DIR / "co_v3_01.mp4"
    c2 = TEMP_DIR / "co_v3_02.mp4"

    frames1 = int(round(5.5 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(DORMANT_STAGE_JPG),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='min(zoom+0.00075,1.075)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames1}:s=1920x1080:fps=30,"
            "setsar=1,format=yuv420p"
        ),
        "-t", "5.50", "-r", "30", "-video_track_timescale", "30000",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(c1)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    frames2 = int(round(4.0 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(DORMANT_STAGE_JPG),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='1.42':x='(iw-iw/zoom)*0.24 + (iw-iw/zoom)*0.50*(on/{frames2})':y='(ih-ih/zoom)*0.33':d={frames2}:s=1920x1080:fps=30,"
            "setsar=1,format=yuv420p"
        ),
        "-t", "4.00", "-r", "30", "-video_track_timescale", "30000",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(c2)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ct = TEMP_DIR / "co_v3_concat.txt"
    ct.write_text(f"file '{c1}'\nfile '{c2}'\n", encoding="utf-8")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(ct),
        "-c", "copy", str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return probe_duration(out_mp4)


def render_finale_outro_v3(out_mp4: Path) -> float:
    """Builds the crisp 11.0s Finale Logo Card on pure white (`official_karmic_genie_show_logo.jpg`)."""
    frames = int(round(11.0 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(LOGO_JPG),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=860:860:force_original_aspect_ratio=decrease,"
            "pad=1920:1080:(ow-iw)/2:(oh-ih)/2-42:color=white,"
            f"zoompan=z='min(zoom+0.00035,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps=30,"
            "setsar=1,format=yuv420p"
        ),
        "-t", "11.00", "-r", "30", "-video_track_timescale", "30000",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return probe_duration(out_mp4)


def render_v3_shot(
    entry: dict,
    sp_st: float,
    sp_en: float,
    raw_dur: float,
    out_mp4: Path,
) -> tuple[float, float, float]:
    """
    Renders a single 1.0x broadcast shot (ZERO rubberband, ZERO tpad freeze-frames!):
      - `visual_full`: brisk `setpts` visual plate + stereo silence (+ optional badge).
      - `full`: trimmed `[max(0.0, sp_st - 0.16), min(raw_dur, sp_en + 0.22)]` full-screen studio shot.
      - `pip75`: 75% foreground clip (`1480x832` + 4px `#EBC670` gold border = `1488x840` at `x=216, y=158`)
        over `1920x1080` `v6_7d_dormant_stage_16x9.jpg` (`eq=brightness=-0.06:saturation=0.95` + subtle slow pan)
        so ~25% of the live studio remains visible around the window!
      - `split_full_to_pip75`: Audio from `src`, Video = `v1_full_mp4` Full Studio (`v1_head_dur`)
        cutting inline to `pip75` (`v2_pip_mp4`) for remaining duration!
      - `split_tail_pip75`: Audio + Head Video from `src` Full Studio, cutting inline for the last
        `tail_pip_dur` seconds to `pip75` (`v2_pip_mp4`) while `src` voiceover finishes seamlessly!
    Returns `(rendered_dur, rel_sp_st, rel_sp_en)`.
    """
    src_mp4 = Path(entry["src"])
    layout = entry["layout"]
    voice = entry["voice"]
    ov_name = entry.get("overlay")
    ov_path = (OVERLAYS_V3_DIR / ov_name) if (ov_name and (OVERLAYS_V3_DIR / ov_name).exists()) else None

    if layout == "visual_full":
        target_dur = float(entry["visual_dur"])
        pts_mul = float(entry["pts_mul"])
        v_base = (
            f"setpts={pts_mul:.4f}*PTS,fps=30,"
            "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
            "setsar=1,format=yuv420p"
        )
        cmd = ["ffmpeg", "-y", "-i", str(src_mp4)]
        if ov_path:
            cmd += [
                "-loop", "1", "-t", f"{target_dur:.3f}", "-i", str(ov_path),
                "-f", "lavfi", "-t", f"{target_dur:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                "-filter_complex", (
                    f"[0:v]{v_base}[vb];"
                    f"[1:v]fade=t=in:st=0.15:d=0.35:alpha=1,fade=t=out:st={max(0.8, target_dur-0.45):.2f}:d=0.35:alpha=1[ov];"
                    "[vb][ov]overlay=0:0:format=auto,format=yuv420p[vout]"
                ),
                "-map", "[vout]", "-map", "2:a:0",
            ]
        else:
            cmd += [
                "-f", "lavfi", "-t", f"{target_dur:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                "-vf", v_base,
                "-map", "0:v:0", "-map", "1:a:0",
            ]
        cmd += [
            "-t", f"{target_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, 0.14, max(0.80, d - 0.14))

    # Spoken shot: trim cleanly to [max(0.0, sp_st - 0.16), min(raw_dur, sp_en + 0.22)]
    trim_st = max(0.0, sp_st - 0.16)
    trim_en = min(raw_dur, sp_en + 0.22)
    if trim_en - trim_st < 1.50:
        trim_st = 0.0
        trim_en = max(2.0, raw_dur - 0.10)
    clip_dur = trim_en - trim_st
    rel_sp_st = max(0.04, sp_st - trim_st)
    rel_sp_en = min(clip_dur - 0.04, sp_en - trim_st)

    # 1.0x natural speech speed EQ (ZERO rubberband!)
    if voice == "genie":
        a_eq = (
            "highpass=f=85,"
            "equalizer=f=220:t=q:w=1.1:g=1.5,"
            "equalizer=f=3200:t=q:w=1.1:g=-3.2,"
            "lowpass=f=10800"
        )
    else:
        a_eq = "highpass=f=75,lowpass=f=12500"

    a_chain = (
        f"atrim=start={trim_st:.3f}:end={trim_en:.3f},asetpts=PTS-STARTPTS,"
        f"{a_eq},"
        f"afade=t=in:st=0:d=0.04,afade=t=out:st={max(0.10, clip_dur - 0.05):.3f}:d=0.05,"
        "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"
    )

    if layout == "full":
        cmd = ["ffmpeg", "-y", "-i", str(src_mp4)]
        fc = [
            f"[0:v]trim=start={trim_st:.3f}:end={trim_en:.3f},setpts=PTS-STARTPTS,"
            "fps=30,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
            "setsar=1,format=yuv420p[vb]"
        ]
        if ov_path:
            cmd += ["-loop", "1", "-t", f"{clip_dur:.3f}", "-i", str(ov_path)]
            fc.append(
                f"[1:v]fade=t=in:st=0.18:d=0.35:alpha=1,"
                f"fade=t=out:st={max(1.10, clip_dur - 0.50):.2f}:d=0.38:alpha=1[ov]"
            )
            fc.append("[vb][ov]overlay=0:0:format=auto,format=yuv420p[vout]")
        else:
            fc.append("[vb]format=yuv420p[vout]")
        fc.append(f"[0:a]{a_chain}[aout]")

        cmd += [
            "-filter_complex", ";".join(fc),
            "-map", "[vout]", "-map", "[aout]",
            "-t", f"{clip_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, rel_sp_st, min(d - 0.04, rel_sp_en))

    if layout == "pip75":
        frames = max(30, int(round(clip_dur * 30)) + 5)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(src_mp4),
            "-loop", "1", "-t", f"{clip_dur + 0.25:.3f}", "-i", str(DORMANT_STAGE_JPG),
        ]
        fc = [
            f"[1:v]scale=2112:1188:force_original_aspect_ratio=increase,crop=2112:1188,"
            f"zoompan=z='1.02':x='(iw-iw/zoom)*0.36+(iw-iw/zoom)*0.28*(on/{frames})':y='(ih-ih/zoom)*0.50':d={frames}:s=1920x1080:fps=30,"
            f"trim=0:{clip_dur:.3f},setpts=PTS-STARTPTS,"
            "eq=brightness=-0.06:saturation=0.95,setsar=1,format=yuv420p[bg]",
            f"[0:v]trim=start={trim_st:.3f}:end={trim_en:.3f},setpts=PTS-STARTPTS,"
            "fps=30,scale=1480:832:force_original_aspect_ratio=increase,crop=1480:832,"
            "pad=w=iw+8:h=ih+8:x=4:y=4:color=#EBC670,setsar=1,format=yuv420p[fg]",
            "[bg][fg]overlay=216:158:shortest=1,format=yuv420p[vb]",
        ]
        if ov_path:
            cmd += ["-loop", "1", "-t", f"{clip_dur:.3f}", "-i", str(ov_path)]
            fc.append(
                f"[2:v]fade=t=in:st=0.18:d=0.35:alpha=1,"
                f"fade=t=out:st={max(1.10, clip_dur - 0.50):.2f}:d=0.38:alpha=1[ov]"
            )
            fc.append("[vb][ov]overlay=0:0:format=auto,format=yuv420p[vout]")
        else:
            fc.append("[vb]format=yuv420p[vout]")
        fc.append(f"[0:a]{a_chain}[aout]")

        cmd += [
            "-filter_complex", ";".join(fc),
            "-map", "[vout]", "-map", "[aout]",
            "-t", f"{clip_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, rel_sp_st, min(d - 0.04, rel_sp_en))

    if layout in ("split_full_to_pip75", "split_tail_pip75"):
        v2_mp4 = Path(entry["v2_pip_mp4"])
        v2_ss = float(entry.get("v2_pip_ss", 2.0))

        if layout == "split_full_to_pip75":
            v1_mp4 = Path(entry["v1_full_mp4"])
            v1_ss = float(entry.get("v1_full_ss", 0.0))
            seg1_dur = min(float(entry["v1_head_dur"]), max(1.50, clip_dur - 1.50))
            seg2_dur = clip_dur - seg1_dur
        else:
            # `split_tail_pip75`: use `src_mp4` itself for segment 1!
            v1_mp4 = src_mp4
            v1_ss = trim_st
            seg2_dur = min(float(entry["tail_pip_dur"]), max(1.40, clip_dur - 1.80))
            seg1_dur = clip_dur - seg2_dur

        v2_avail = max(0.5, probe_duration(v2_mp4) - v2_ss - 0.05)
        v2_take = min(v2_avail, seg2_dur)
        pts_v2 = (seg2_dur / v2_take) if seg2_dur > v2_take + 0.01 else 1.0
        frames2 = max(30, int(round(seg2_dur * 30)) + 5)

        cmd = [
            "ffmpeg", "-y",
            "-i", str(src_mp4),
            "-i", str(v1_mp4),
            "-i", str(v2_mp4),
            "-loop", "1", "-t", f"{seg2_dur + 0.25:.3f}", "-i", str(DORMANT_STAGE_JPG),
        ]
        fc = [
            f"[1:v]trim=start={v1_ss:.3f}:end={v1_ss + seg1_dur:.3f},setpts=PTS-STARTPTS,"
            "fps=30,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
            "setsar=1,format=yuv420p[v_seg1]",
            f"[3:v]scale=2112:1188:force_original_aspect_ratio=increase,crop=2112:1188,"
            f"zoompan=z='1.02':x='(iw-iw/zoom)*0.36+(iw-iw/zoom)*0.28*(on/{frames2})':y='(ih-ih/zoom)*0.50':d={frames2}:s=1920x1080:fps=30,"
            f"trim=0:{seg2_dur:.3f},setpts=PTS-STARTPTS,"
            "eq=brightness=-0.06:saturation=0.95,setsar=1,format=yuv420p[bg2]",
            f"[2:v]trim=start={v2_ss:.3f}:end={v2_ss + v2_take:.3f},setpts={pts_v2:.5f}*(PTS-STARTPTS),"
            "fps=30,scale=1480:832:force_original_aspect_ratio=increase,crop=1480:832,"
            "pad=w=iw+8:h=ih+8:x=4:y=4:color=#EBC670,setsar=1,format=yuv420p[fg2]",
            "[bg2][fg2]overlay=216:158:shortest=1,format=yuv420p[v_seg2]",
            "[v_seg1][v_seg2]concat=n=2:v=1:a=0,format=yuv420p[vout]",
            f"[0:a]{a_chain}[aout]",
        ]
        cmd += [
            "-filter_complex", ";".join(fc),
            "-map", "[vout]", "-map", "[aout]",
            "-t", f"{clip_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, rel_sp_st, min(d - 0.04, rel_sp_en))

    raise ValueError(f"Unsupported layout mode: {layout}")


def build_master_ass_v3(
    ass_path: Path,
    cold_dur: float,
    shot_timings: list[dict],
    finale_start: float,
    total_dur: float,
    include_bookends: bool = True,
):
    """
    Builds the dark-shaded (`BorderStyle=3`, `OutlineColour=&H38080A10`, `BackColour=&H38080A10`,
    `Outline=11.0`, `Shadow=0.0`) ASS subtitle file using strictly single-line sequential events
    placed cleanly at `MarginV=28` (below the `y=998` 75%-window gold frame and over the bottom
    white marble studio rim) so boxes NEVER overlap or collide!
    """
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TitleGold,DejaVu Sans,33,&H00B8F2FF,&H00B8F2FF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.5,0,3,11.0,0.0,2,70,70,30,1
Style: CinemaWhite,DejaVu Sans,32,&H00FFFFFF,&H00FFFFFF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.3,0,3,11.0,0.0,2,70,70,28,1
Style: GenieGold,DejaVu Sans,32,&H00B8F2FF,&H00B8F2FF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.3,0,3,11.0,0.0,2,70,70,28,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    raw_events: list[tuple[float, float, str, str]] = []

    if include_bookends and cold_dur >= 8.0:
        raw_events.extend([
            (0.45, 3.30, "TitleGold", "KARMIC GENIE SHOW  •  SEASON 1, EPISODE 1"),
            (3.45, 6.35, "CinemaWhite", "Every Industry, City & Career Shift Serves a Grander Design"),
            (6.50, min(cold_dur - 0.20, 9.25), "TitleGold", "THE 7D WAY  •  Duty • Dignity • Discipline • Dharma • Devotion • Divine • Destiny"),
        ])

    for st in shot_timings:
        lines = st["lines"]
        if not lines:
            continue
        style = "GenieGold" if st["voice"] == "genie" else "CinemaWhite"
        sp_s = st["abs_start"] + st["rel_sp_st"]
        sp_e = min(st["abs_end"] - 0.04, st["abs_start"] + st["rel_sp_en"])
        if sp_e <= sp_s + 0.80:
            sp_s = st["abs_start"] + 0.08
            sp_e = max(sp_s + 0.80, st["abs_end"] - 0.08)

        total_chars = sum(max(1, len(x)) for x in lines)
        cur = sp_s
        for i, ln in enumerate(lines):
            assert "\\N" not in ln and "\n" not in ln, f"Multi-line break forbidden in BorderStyle=3: {ln}"
            assert_editorial_purity(ln, st["sid"])
            frac = max(1, len(ln)) / total_chars
            nxt = sp_e if i == len(lines) - 1 else (cur + (sp_e - sp_s) * frac)
            ev_end = max(cur + 0.45, nxt - 0.05) if i < len(lines) - 1 else max(cur + 0.45, nxt)
            raw_events.append((cur, ev_end, style, ln))
            cur = max(cur + 0.49, nxt)

    if include_bookends and total_dur - finale_start >= 6.0:
        mid_f = finale_start + (total_dur - finale_start) * 0.50
        raw_events.extend([
            (finale_start + 0.65, mid_f - 0.15, "CinemaWhite",
             "Respect Your DUTY First  •  Earn with DIGNITY Always  •  Practice Life DISCIPLINE"),
            (mid_f + 0.05, total_dur - 0.75, "TitleGold",
             "Uphold Karmic DHARMA  •  Raise Family with DEVOTION  •  Purposeful Life Is Your DESTINY"),
        ])

    raw_events.sort(key=lambda x: x[0])
    dialogue_lines = []
    for idx, (s_t, e_t, style, txt) in enumerate(raw_events):
        if idx + 1 < len(raw_events) and e_t > raw_events[idx + 1][0] - 0.04:
            e_t = max(s_t + 0.25, raw_events[idx + 1][0] - 0.04)
        dialogue_lines.append(
            f"Dialogue: 0,{format_ass_time(s_t)},{format_ass_time(e_t)},{style},,0,0,0,,{txt}"
        )

    ass_path.write_text(header + "\n".join(dialogue_lines) + "\n", encoding="utf-8")


def main():
    from faster_whisper import WhisperModel

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUT_MP4.parent.mkdir(parents=True, exist_ok=True)

    total_slots = len(V3_SHOT_LEDGER)
    print(f"1️⃣ Verifying Grand-Design editorial purity & probing all {total_slots} clips with Whisper (`tiny.en`)...", flush=True)
    for entry in V3_SHOT_LEDGER:
        src = Path(entry["src"])
        if not src.exists():
            raise FileNotFoundError(f"Missing clip for {entry['sid']}: {src}")
        for ln in entry["lines"]:
            assert_editorial_purity(ln, entry["sid"])

    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")

    print("2️⃣ Rendering crisp 9.5s Cold Open & 11.0s Finale Logo Card...", flush=True)
    co_mp4 = TEMP_DIR / "part_00_cold_open.mp4"
    cold_dur = render_cold_open_v3(co_mp4)

    fin_mp4 = TEMP_DIR / "part_99_finale_logo.mp4"
    fin_dur = render_finale_outro_v3(fin_mp4)

    print(f"3️⃣ Assembling all {total_slots} shots at brisk 1.0x pace (Full Studio + 75% Gold-Framed Studio Window)...", flush=True)
    parts = [co_mp4]
    cursor = cold_dur
    shot_timings = []

    for idx, entry in enumerate(V3_SHOT_LEDGER, 1):
        sid = entry["sid"]
        src = Path(entry["src"])
        if entry["layout"] == "visual_full":
            raw_dur = probe_duration(src)
            sp_st, sp_en, txt = 0.0, raw_dur, "[visual]"
        else:
            txt, sp_st, sp_en, raw_dur = transcribe_clip_whisper(src, model, entry["hint_sp"])
            assert_editorial_purity(txt, f"{sid}_audio_transcript")

        out_p = TEMP_DIR / f"part_{idx:02d}_{sid}.mp4"
        dur, rel_st, rel_en = render_v3_shot(
            entry=entry,
            sp_st=sp_st,
            sp_en=sp_en,
            raw_dur=raw_dur,
            out_mp4=out_p,
        )
        shot_timings.append({
            "sid": sid,
            "voice": entry["voice"],
            "lines": entry["lines"],
            "abs_start": cursor,
            "abs_end": cursor + dur,
            "rel_sp_st": rel_st,
            "rel_sp_en": rel_en,
        })
        parts.append(out_p)
        cursor += dur
        ov_tag = f" + {entry['overlay']}" if entry.get("overlay") else ""
        print(
            f"    [{idx:02d}/{total_slots}] {sid} [{entry['layout']}] <- {src.name} "
            f"({dur:.2f}s, cum={cursor:.1f}s){ov_tag}",
            flush=True,
        )

    finale_start = cursor
    parts.append(fin_mp4)

    concat_txt = TEMP_DIR / "master_v3_concat.txt"
    concat_txt.write_text("\n".join(f"file '{p}'" for p in parts) + "\n", encoding="utf-8")
    stitched_mp4 = TEMP_DIR / "stitched_v3_raw.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy", str(stitched_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    actual_total = probe_duration(stitched_mp4)
    print(f"4️⃣ Stitched raw broadcast runtime: {actual_total:.2f}s ({int(actual_total//60):02d}:{actual_total%60:05.2f})", flush=True)

    ass_path = TEMP_DIR / "s01e01_v3_interactive.ass"
    build_master_ass_v3(ass_path, cold_dur, shot_timings, finale_start, actual_total, include_bookends=True)

    vol_expr = (
        f"if(lt(t,{cold_dur-0.35:.2f}), 0.56, "
        f"if(gt(t,{finale_start-0.60:.2f}), 0.54, 0.036))"
    )

    print("5️⃣ Burning dark-shaded BorderStyle=3 subtitles + mixing 7D Theme at -14 LUFS...", flush=True)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(stitched_mp4),
        "-ss", "4.00", "-stream_loop", "-1", "-i", str(THEME_WAV),
        "-filter_complex", (
            f"[0:v]ass={ass_path},fade=t=in:st=0:d=0.60,fade=t=out:st={actual_total-1.10:.2f}:d=1.05[vout];"
            f"[1:a]atrim=0:{actual_total:.3f},asetpts=PTS-STARTPTS,lowpass=f=9000,volume='{vol_expr}':eval=frame[bgm];"
            "[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
        ),
        "-map", "[vout]", "-map", "[aout]",
        "-t", f"{actual_total:.3f}",
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "18",
        "-r", "30",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-movflags", "+faststart",
        str(OUT_MP4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if ARTIFACT_DIR.exists():
        shutil.copy2(OUT_MP4, ARTIFACT_MP4)

    final_d = probe_duration(OUT_MP4)
    print(f"\n🏆 S01E01 v3.1 INTERACTIVE GRAND-DESIGN MASTER READY: {OUT_MP4}")
    print(f"   Runtime: {int(final_d//60):02d}:{final_d%60:05.2f} ({final_d:.2f}s) | Size: {OUT_MP4.stat().st_size/1e6:.2f} MB", flush=True)


if __name__ == "__main__":
    main()
