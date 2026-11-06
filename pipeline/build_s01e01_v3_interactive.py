#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Widescreen (16:9, 1920x1080, 30fps, -14 LUFS) Theatrical Cinema Director's Cut Assembler for:
  Karmic Genie Show — Season 1, Episode 1 (v4.1 Cinema Director's Cut + Seamless Wide-Wall Master)
  "200,000 Cuts, 60,000 Buyouts & Why Every One Is a Blessing in Disguise"

Mandatory v4.1 Theatrical Movie Direction & Broadcast Guarantees:
  1. Multi-Camera Revolving Orbit -> Intimate Close-Up Cut on EVERY Full Studio Shot (`layout == "full"`):
     - Camera A (`0..48%`): Smooth orbital tracking / revolving dolly (`2240x1260` animated `crop`
       gliding horizontally + arcing vertically with `sin(PI*t/dur)` so live 30fps lip-sync stays
       100% fluid with zero `zoompan` frame-freezing!).
     - Camera B (`48%..100%`): Instant Hollywood Multi-Cam Cut to an Intimate Eye-Level Cinema
       Close-Up (`1.24x..1.42x` calibrated per shot `(cu_fx, cu_fy)`) with gentle lateral dolly push
       and warm anamorphic edge vignette (`vignette=PI/6.5`)!
  2. Seamless Wide-Wall Studio Masters (`v7_wide_wall_dormant_16x9.jpg` & `v7_wide_wall_genie_16x9.jpg`):
     - Zero `v6` beige paint seams (`plate_s7_05_signoff.mp4` & `batch_06_03.mp4` excluded).
     - ZERO top dark rectangular overlay boxes (`y=0..150` 100% clear; metrics live on the studio's
       curved circular glass barriers + `v4_ig_02.mp4` holographic glass charts!).
  3. Multi-Angle Visual Metric Montage During `2025 -> 2026` Narration (`03`..`05`):
     - `03_Prologue_Since_2025`: 2-angle edit on `v4_ig_02.mp4` curved-glass holographic charts.
     - `04_200K_CrossSector`: 2-angle whip-cut pan across Left & Right curved glass displays of `v7`.
     - `05_720B_Infrastructure`: 2-angle `pip75` edit on `batch_02_05.mp4` punching into the CapEx tablet.
  4. Strict 180-Degree Eyeline 3-Part Tech CEO Interview (`CEO faces RIGHT ->`, `Host faces LEFT <-`).
  5. Revolving 3D Studio Background + Multi-Angle Story Cuts Inside ALL `pip75` Human Stories (`11`..`16`):
     - Emotional Close-Up punch-ins (`11`, `12`, `13`, `15`) and multi-clip B-roll cuts (`14` -> `batch_04_05`,
       `16` -> `batch_03_02`) inside the `1440x810` gold-rimmed window over revolving `v7` studio!
  6. True 360-Degree Revolving Golden Lamp Awakening (`batch_05_02.mp4`) + 2-Angle Crane-to-Close-Up
     Karmic Genie Climax (`v7_wide_wall_genie_16x9.jpg`) -> 100% Verified `@Me` Host Connecting All Dots.
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
DORMANT_STAGE_JPG = MASTERS_DIR / "v7_wide_wall_dormant_16x9.jpg"
GENIE_STAGE_JPG = MASTERS_DIR / "v7_wide_wall_genie_16x9.jpg"
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

# Canonical 25-shot v4.1 Theatrical Cinema Director's Cut Ledger:
V3_SHOT_LEDGER = [
    # --- WELCOME & VISUAL 2025->2026 METRICS PROLOGUE ---
    {
        "sid": "01_Welcome_Home",
        "src": V3_CLIPS_ROOT / "v3_b1_welcome" / "v3_b1_welcome_03.mp4",
        "hint_sp": (0.80, 7.38),
        "layout": "full",
        "orbit_dir": 1,
        "cu_zoom": 1.26,
        "cu_fx": 0.50,
        "cu_fy": 0.22,
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
        "orbit_dir": -1,
        "cu_zoom": 1.30,
        "cu_fx": 0.45,
        "cu_fy": 0.18,
        "voice": "human",
        "overlay": "v3_ov_poll.png",
        "lines": [
            "Raise your hand—and comment at home—",
            "if someone you know faced a buyout or layoff!",
        ],
    },
    {
        # Narrator audio + 2-Angle Curved-Glass Holographic Data Charts (`v4_ig_02.mp4`: Wide Orbit -> 1.28x Chart CU)!
        "sid": "03_Prologue_Since_2025",
        "src": V1_CLIPS_ROOT / "batch_01_prologue" / "batch_01_prologue_06.mp4",
        "video_src": V3_CLIPS_ROOT / "v4_interview_and_genie" / "v4_ig_02.mp4",
        "hint_sp": (0.75, 7.31),
        "layout": "audio_over_video",
        "cu_zoom": 1.28,
        "cu_fx": 0.34,
        "cu_fy": 0.34,
        "voice": "human",
        "overlay": None,
        "lines": [
            "Before anyone speaks tonight, let's take sixty quiet seconds",
            "to see what happened since early 2025.",
        ],
    },
    {
        # Narrator audio + 2-Angle Whip-Cut Close Glide across Left & Right Curved Glass Displays of `v7`!
        "sid": "04_200K_CrossSector",
        "src": V3_CLIPS_ROOT / "v3_b1_welcome" / "v3_b1_welcome_02.mp4",
        "image_src": DORMANT_STAGE_JPG,
        "hint_sp": (1.06, 7.72),
        "layout": "audio_over_glass_pan",
        "voice": "human",
        "overlay": None,
        "lines": [
            "Over 200,000 roles shifted this year",
            "across tech, banking, shipping, auto, and support.",
        ],
    },
    {
        # Narrator audio + 2-Angle `pip75` Financial Capex Tablet (`batch_02_05.mp4` Medium -> 1.34x Tablet CU)!
        "sid": "05_720B_Infrastructure",
        "src": V1_CLIPS_ROOT / "batch_01_prologue" / "batch_01_prologue_03.mp4",
        "video_src": V1_CLIPS_ROOT / "batch_02_scene1_sf_mysuru" / "batch_02_scene1_sf_mysuru_05.mp4",
        "video_ss": 0.35,
        "hint_sp": (0.00, 7.64),
        "layout": "audio_over_pip75",
        "pip_zoom": 1.34,
        "pip_fx": 0.42,
        "pip_fy": 0.62,
        "voice": "human",
        "overlay": None,
        "lines": [
            "Today, infrastructure spending exceeds $720 billion a year—",
            "reshaping every industry's cash flow.",
        ],
    },

    # --- SECTION 1: 3-PART TECH CEO INTERVIEW (CEO FACES RIGHT `->`, HOST FACES LEFT `<-`) ---
    {
        "sid": "06_Host_Grand_Design_Organ",
        "src": V3_CLIPS_ROOT / "v3_grand_design" / "v3_gd_02.mp4",
        "hint_sp": (0.37, 7.69),
        "layout": "full",
        "orbit_dir": 1,
        "cu_zoom": 1.30,
        "cu_fx": 0.68,
        "cu_fy": 0.22,
        "voice": "human",
        "overlay": "v3_ov_ceo.png",
        "lines": [
            "Every industry, company, and city is a vital organ in Earth's living body—",
            "how is AI reshaping our circulation today?",
        ],
    },
    {
        # CEO Part 1 (seated LEFT facing RIGHT `->`): Good things of the AI revolution first!
        "sid": "07_CEO_AI_Good_Things_First",
        "src": V3_CLIPS_ROOT / "v4_ceo_interview" / "v4_ceo_01.mp4",
        "hint_sp": (0.30, 8.00),
        "layout": "full",
        "orbit_dir": -1,
        "cu_zoom": 1.22,
        "cu_fx": 0.33,
        "cu_fy": 0.22,
        "voice": "human",
        "overlay": None,
        "lines": [
            "First, look at the good—AI is accelerating medical discovery,",
            "removing repetitive drudgery, and empowering you.",
        ],
    },
    {
        # CEO Part 2A (`hflip` + clean crop so CEO sits LEFT facing RIGHT `->` + Close-Up punch-in!):
        "sid": "08_CEO_50B_Circulation",
        "src": V1_CLIPS_ROOT / "batch_02_scene1_sf_mysuru" / "batch_02_scene1_sf_mysuru_02.mp4",
        "hint_sp": (0.00, 7.78),
        "layout": "full",
        "hflip": True,
        "hflip_vf": "scale=2960:1665,crop=1920:1080:430:115,hflip",
        "orbit_dir": 1,
        "cu_zoom": 1.25,
        "cu_fx": 0.40,
        "cu_fy": 0.20,
        "voice": "human",
        "overlay": None,
        "lines": [
            "$50 billion a quarter on GPUs flipped free cash flow negative.",
            "Cloud and AI demand every dollar right now.",
        ],
    },
    {
        # CEO Part 2B (seated LEFT facing RIGHT `->` -> Dramatic 1.32x Close-Up on CEO's eyes!):
        "sid": "09_CEO_Cautions_And_Preparation",
        "src": V3_CLIPS_ROOT / "v4_ceo_interview" / "v4_ceo_02.mp4",
        "hint_sp": (0.00, 7.88),
        "layout": "full",
        "orbit_dir": -1,
        "cu_zoom": 1.32,
        "cu_fx": 0.30,
        "cu_fy": 0.22,
        "voice": "human",
        "overlay": "v3_ov_layers.png",
        "lines": [
            "The caution is real—as routine layers streamline,",
            "use generous transition bridges to prepare and master AI tools now.",
        ],
    },
    {
        # Host `@Me` introduces the `>= 4 of 7D` Scorecard Rule (`Orbit -> 1.28x Close-Up`)!
        "sid": "10_Host_7D_Scorecard_Rule",
        "src": V3_CLIPS_ROOT / "v3_7d_philosophy_me" / "v3_phil_03.mp4",
        "hint_sp": (0.00, 7.76),
        "layout": "full",
        "orbit_dir": 1,
        "cu_zoom": 1.28,
        "cu_fx": 0.48,
        "cu_fy": 0.20,
        "voice": "human",
        "overlay": "v3_ov_ceo.png",
        "lines": [
            "Measure every question against all Seven D's—if your life ticks at least four,",
            "stay the course; otherwise, change your route!",
        ],
    },

    # --- SECTION 2: 3 COMBINED HUMAN ISSUES (`pip75` OVER REVOLVING `v7` STUDIO + MULTI-ANGLE CUTS!) ---
    # Issue #1: Connectedness to Home & Aging Parents (2/7 -> 6/7 D)
    {
        "sid": "11_Issue1A_Expat_Abroad_PiP",
        "src": V1_CLIPS_ROOT / "batch_02_scene1_sf_mysuru" / "batch_02_scene1_sf_mysuru_03.mp4",
        "hint_sp": (0.92, 7.60),
        "layout": "pip75",
        "orbit_dir": 1,
        "pip_zoom": 1.28,
        "pip_fx": 0.44,
        "pip_fy": 0.36,
        "voice": "human",
        "overlay": None,
        "lines": [
            "Millions of us work outside our home countries—",
            "telling ourselves we left just briefly to earn dollars.",
        ],
    },
    {
        "sid": "12_Issue1B_Coimbatore_Peace_PiP",
        "src": V1_CLIPS_ROOT / "topup_clean" / "tu2_munich_coimbatore_01.mp4",
        "hint_sp": (1.38, 6.44),
        "layout": "pip75",
        "orbit_dir": -1,
        "pip_zoom": 1.24,
        "pip_fx": 0.60,
        "pip_fy": 0.34,
        "voice": "human",
        "overlay": None,
        "lines": [
            "Coimbatore cut my pay, erased rent, and brought peace—",
            "did I arrive early?",
        ],
    },
    # Issue #2: Family Devotion vs. Flattened Status & 5 Pagers (2/7 -> 5/7 D)
    {
        "sid": "13_Issue2A_Mum_Missed_Bedtimes_PiP",
        "src": V1_CLIPS_ROOT / "topup_clean" / "rec_s2_02_elena.mp4",
        "hint_sp": (0.00, 7.40),
        "layout": "pip75",
        "orbit_dir": 1,
        "pip_zoom": 1.24,
        "pip_fx": 0.58,
        "pip_fy": 0.36,
        "voice": "human",
        "overlay": None,
        "lines": [
            "When companies flattened over 35% of small-team managers,",
            "seven years of missed bedtimes vanished.",
        ],
    },
    {
        # Multi-Clip Cinema Cut inside `pip75`: `batch_04_02` -> final 2.4s `batch_04_05` (dark office monitors)!
        "sid": "14_Issue2B_Tokyo_Five_Pagers_PiP",
        "src": V1_CLIPS_ROOT / "batch_04_scene3_tokyo_munich_coimbatore" / "batch_04_scene3_tokyo_munich_coimbatore_02.mp4",
        "broll_mp4": V1_CLIPS_ROOT / "batch_04_scene3_tokyo_munich_coimbatore" / "batch_04_scene3_tokyo_munich_coimbatore_05.mp4",
        "broll_ss": 1.20,
        "broll_dur": 2.40,
        "hint_sp": (0.92, 7.44),
        "layout": "pip75_broll_cut",
        "orbit_dir": -1,
        "voice": "human",
        "overlay": None,
        "lines": [
            "Four teammates left with zero replacements approved.",
            "My wife eats alone every night while I carry five pagers.",
        ],
    },
    # Issue #3: Seasoned 50s Mastery & Young 20s Builders (3/7 -> 6/7 D)
    {
        "sid": "15_Issue3A_Munich_Veteran_58_PiP",
        "src": V1_CLIPS_ROOT / "topup_clean" / "tu2_munich_coimbatore_02.mp4",
        "hint_sp": (1.00, 7.42),
        "layout": "pip75",
        "orbit_dir": 1,
        "pip_zoom": 1.26,
        "pip_fx": 0.50,
        "pip_fy": 0.32,
        "voice": "human",
        "overlay": None,
        "lines": [
            "At fifty-eight in Munich, thirty-five years becomes 'legacy.'",
            "How do we leave gracefully?",
        ],
    },
    {
        # Multi-Clip Cinema Cut inside `pip75`: `batch_03_01` -> final 2.4s `batch_03_02` (young grad in apartment)!
        "sid": "16_Issue3B_SaoPaulo_7Pct_Grads_PiP",
        "src": V1_CLIPS_ROOT / "batch_03_scene2_london_saopaulo" / "batch_03_scene2_london_saopaulo_01.mp4",
        "broll_mp4": V1_CLIPS_ROOT / "batch_03_scene2_london_saopaulo" / "batch_03_scene2_london_saopaulo_02.mp4",
        "broll_ss": 1.60,
        "broll_dur": 2.40,
        "hint_sp": (0.00, 7.36),
        "layout": "pip75_broll_cut",
        "orbit_dir": -1,
        "voice": "human",
        "overlay": None,
        "lines": [
            "New graduates dropped to 7% of Big Tech hires.",
            "My father sewed suits twenty years—where do we start?",
        ],
    },

    # --- SECTION 3: 360-DEGREE LAMP AWAKENING + 2-ANGLE CRANE-TO-CLOSEUP KARMIC GENIE ---
    {
        # Angle 1: Orbital crane descent on `v7_wide_wall_dormant` -> Angle 2: 3D Revolving Golden Lamp Awakening (`batch_05_02.mp4`)!
        "sid": "17_Host_Summon_Genie",
        "src": V1_CLIPS_ROOT / "topup_clean" / "plate_s4_03_punchline.mp4",
        "image_src": DORMANT_STAGE_JPG,
        "lamp_mp4": V1_CLIPS_ROOT / "batch_05_scene4_punchline_and_awakening" / "batch_05_scene4_punchline_and_awakening_02.mp4",
        "lamp_ss": 0.60,
        "hint_sp": (0.96, 6.90),
        "layout": "summon_lamp_awakening",
        "voice": "human",
        "overlay": None,
        "lines": [
            "Let's quiet the room and ask together:",
            "What does Genie say — the 7D way?",
        ],
    },
    {
        # 2-Angle Theatrical Genie Sequence (`0..3.6s` Wide Revolving Arena -> `3.6s..end` 1.56x Close-Up Revolving Push on Genie)!
        "sid": "18_Genie_Single_Phrase_2Yrs",
        "src": V3_CLIPS_ROOT / "v4_interview_and_genie" / "v4_ig_01.mp4",
        "image_src": GENIE_STAGE_JPG,
        "hint_sp": (0.66, 7.66),
        "layout": "genie_two_angle_cinema",
        "voice": "genie",
        "overlay": None,
        "lines": [
            "Rest easy, dear friends—all that is happening now,",
            "and for the next couple of years, is a blessing in disguise!",
        ],
    },
    {
        # 2.2s Revolving Crane Pull-Back Dissolve from `v7_wide_wall_genie_16x9.jpg` -> `v7_wide_wall_dormant_16x9.jpg`
        "sid": "19_Genie_Lotus_Dissolve",
        "src": GENIE_STAGE_JPG,
        "dst_img": DORMANT_STAGE_JPG,
        "layout": "image_dissolve",
        "visual_dur": 2.20,
        "voice": "genie",
        "overlay": None,
        "lines": [],
    },

    # --- SECTION 4: HOST `@Me` CONNECTS ALL DOTS (MULTI-CAM ORBIT -> CLOSE-UP + REUNION FLASHBACK!) ---
    {
        "sid": "20_Host_Body_Mind_Soul",
        "src": V3_CLIPS_ROOT / "v3_grand_design" / "v3_gd_01.mp4",
        "hint_sp": (0.18, 7.70),
        "layout": "full",
        "orbit_dir": 1,
        "cu_zoom": 1.42,
        "cu_fx": 0.64,
        "cu_fy": 0.35,
        "voice": "human",
        "overlay": None,
        "lines": [
            "Just as human cells renew to serve mind, soul, and para-soul—",
            "every company and career shift serves a grander design!",
        ],
    },
    {
        "sid": "21_Host_Forest_And_Roadways",
        "src": V3_CLIPS_ROOT / "v3_7d_philosophy_me" / "v3_phil_02.mp4",
        "hint_sp": (0.00, 7.54),
        "layout": "full",
        "orbit_dir": -1,
        "cu_zoom": 1.32,
        "cu_fx": 0.44,
        "cu_fy": 0.22,
        "voice": "human",
        "overlay": "v3_ov_ceo.png",
        "lines": [
            "Earning fifty years just to survive is an overgrown forest yielding no fruit—",
            "industries, like highways, are pathways, never your destination!",
        ],
    },
    {
        "sid": "22_Host_IT_Connectedness_Correction",
        "src": V3_CLIPS_ROOT / "v3_7d_philosophy_me" / "v3_phil_01.mp4",
        "hint_sp": (0.11, 8.01),
        "layout": "full",
        "orbit_dir": 1,
        "cu_zoom": 1.22,
        "cu_fx": 0.50,
        "cu_fy": 0.20,
        "voice": "human",
        "overlay": "v3_ov_layers.png",
        "lines": [
            "Tech exists for connectedness! When workers disconnect from home and family,",
            "this buyout wave acts like a stock market correction—reconnecting you!",
        ],
    },
    {
        "sid": "23_Host_Why_Handcuffs",
        "src": V3_CLIPS_ROOT / "v3_host_expansion_me" / "v3_me_exp_03.mp4",
        "hint_sp": (0.00, 7.26),
        "layout": "full",
        "orbit_dir": -1,
        "cu_zoom": 1.28,
        "cu_fx": 0.48,
        "cu_fy": 0.22,
        "voice": "human",
        "overlay": None,
        "lines": [
            "Every single one is a blessing in disguise!",
            "Why? Nobody unlocks golden handcuffs on their own!",
        ],
    },
    {
        "sid": "24_Host_Overdue_Reunion_Split",
        "src": V3_CLIPS_ROOT / "v3_host_expansion_me" / "v3_me_exp_01.mp4",
        "hint_sp": (0.92, 7.84),
        "layout": "split_tail_pip75",
        "cu_fx": 0.65,
        "cu_fy": 0.24,
        "v2_pip_mp4": V1_CLIPS_ROOT / "batch_04_scene3_tokyo_munich_coimbatore" / "batch_04_scene3_tokyo_munich_coimbatore_01.mp4",
        "v2_pip_ss": 2.20,
        "tail_pip_dur": 2.60,
        "voice": "human",
        "overlay": None,
        "lines": [
            "Millions abroad postpone duty to aging parents—",
            "twelve months' buyout pay brings that overdue reunion home guilt-free!",
        ],
    },
    {
        "sid": "25_Host_50s_Dignity",
        "src": V3_CLIPS_ROOT / "v3_host_expansion_me" / "v3_me_exp_02.mp4",
        "hint_sp": (0.00, 6.92),
        "layout": "full",
        "orbit_dir": 1,
        "cu_zoom": 1.32,
        "cu_fx": 0.58,
        "cu_fy": 0.22,
        "voice": "human",
        "overlay": None,
        "lines": [
            "In your fifties or flattened from management?",
            "Take the runway with Dignity—and fulfill your true purpose!",
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


def even_px(val: float) -> int:
    n = int(round(val))
    return n if n % 2 == 0 else n + 1


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


def render_cold_open_v41(out_mp4: Path) -> float:
    """
    Builds the 3-Angle Theatrical Movie Cold Open (9.5s) on `v7_wide_wall_dormant_16x9.jpg`:
      - Angle 1 (3.6s): Sweeping orbital crane descent across the arena & seamless white back wall
      - Angle 2 (3.2s): Low-angle revolving glide across the Curved Circular Glass Displays
      - Angle 3 (2.7s): Intimate Close-Up dolly push on the golden Genie lamp & 7D emblem
    """
    c1 = TEMP_DIR / "co_v41_01.mp4"
    c2 = TEMP_DIR / "co_v41_02.mp4"
    c3 = TEMP_DIR / "co_v41_03.mp4"

    f1 = int(round(3.6 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(DORMANT_STAGE_JPG),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='1.12-0.09*(on/{f1})':x='(iw-iw/zoom)*(0.35+0.30*(on/{f1}))':y='(ih-ih/zoom)*(0.25+0.25*(on/{f1}))':d={f1}:s=1920x1080:fps=30,"
            "eq=contrast=1.03:saturation=1.04,vignette=PI/8.5,setsar=1,format=yuv420p"
        ),
        "-t", "3.60", "-r", "30", "-video_track_timescale", "30000",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(c1)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    f2 = int(round(3.2 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(DORMANT_STAGE_JPG),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='1.34':x='(iw-iw/zoom)*(0.06+0.88*(on/{f2}))':y='(ih-ih/zoom)*0.74':d={f2}:s=1920x1080:fps=30,"
            "eq=contrast=1.04:saturation=1.05,vignette=PI/8,setsar=1,format=yuv420p"
        ),
        "-t", "3.20", "-r", "30", "-video_track_timescale", "30000",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(c2)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    f3 = int(round(2.7 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(DORMANT_STAGE_JPG),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='1.44+0.14*(on/{f3})':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.48':d={f3}:s=1920x1080:fps=30,"
            "eq=contrast=1.04:saturation=1.05,vignette=PI/7,setsar=1,format=yuv420p"
        ),
        "-t", "2.70", "-r", "30", "-video_track_timescale", "30000",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(c3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ct = TEMP_DIR / "co_v41_concat.txt"
    ct.write_text(f"file '{c1}'\nfile '{c2}'\nfile '{c3}'\n", encoding="utf-8")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(ct),
        "-c", "copy", str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return probe_duration(out_mp4)


def render_finale_outro_v41(out_mp4: Path) -> float:
    """Builds the crisp 11.0s Finale Logo Card on pure white (`official_karmic_genie_show_logo.jpg`)."""
    frames = int(round(11.0 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(LOGO_JPG),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=860:860:force_original_aspect_ratio=decrease,"
            "pad=1920:1080:(ow-iw)/2:(oh-ih)/2-42:color=white,"
            f"zoompan=z='min(zoom+0.00045,1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps=30,"
            "setsar=1,format=yuv420p"
        ),
        "-t", "11.00", "-r", "30", "-video_track_timescale", "30000",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return probe_duration(out_mp4)


def render_v41_shot(
    entry: dict,
    sp_st: float,
    sp_en: float,
    raw_dur: float,
    out_mp4: Path,
) -> tuple[float, float, float]:
    """
    Renders a single 1.0x v4.1 Theatrical Cinema shot (ZERO rubberband, ZERO tpad freeze-frames,
    ZERO live-video `zoompan` lip-freezing!):
      - `full`: Two-Camera Movie Cut (`0..48%` Revolving Orbital Medium Shot -> `48%..100%`
        Intimate Cinema Close-Up calibrated to `(cu_fx, cu_fy)` with lateral dolly push + vignette).
      - `audio_over_video`: 2-angle edit on `v4_ig_02.mp4` holographic glass metrics.
      - `audio_over_glass_pan`: 2-angle whip-cut close glide across Left & Right curved glass displays.
      - `audio_over_pip75`: 2-angle `pip75` edit punching into the financial CapEx tablet.
      - `pip75`: Revolving 3D `v7` studio background + 2-angle Orbital-to-Close-Up cut inside `1440x810`.
      - `pip75_broll_cut`: Revolving 3D `v7` studio background + multi-clip B-roll cut inside `1440x810`.
      - `summon_lamp_awakening`: Orbital `v7` crane push -> 360-degree revolving golden lamp awakening!
      - `genie_two_angle_cinema`: Wide revolving `v7` arena sweep -> 1.56x Close-Up revolving push on Genie!
      - `split_tail_pip75`: Orbital push on `@Me` -> sunlit South Indian courtyard reunion inside `pip75`.
    """
    src_mp4 = Path(entry["src"])
    layout = entry["layout"]
    voice = entry["voice"]
    ov_name = entry.get("overlay")
    ov_path = (OVERLAYS_V3_DIR / ov_name) if (ov_name and (OVERLAYS_V3_DIR / ov_name).exists()) else None

    if layout == "image_dissolve":
        target_dur = float(entry["visual_dur"])
        dst_img = Path(entry["dst_img"])
        frames = max(30, int(round(target_dur * 30)))
        fade_st = max(0.35, target_dur * 0.35)
        fade_d = max(0.60, target_dur - fade_st - 0.10)
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-t", f"{target_dur:.3f}", "-i", str(src_mp4),
            "-loop", "1", "-t", f"{target_dur:.3f}", "-i", str(dst_img),
            "-f", "lavfi", "-t", f"{target_dur:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-filter_complex", (
                f"[0:v]scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
                f"zoompan=z='1.28-0.20*(on/{frames})':x='(iw-iw/zoom)*(0.55-0.10*(on/{frames}))':y='(ih-ih/zoom)*0.38':d={frames}:s=1920x1080:fps=30,"
                "vignette=PI/8,setsar=1,format=rgba[v0];"
                f"[1:v]scale=2240:1260:force_original_aspect_ratio=increase,crop=2240:1260,"
                f"zoompan=z='1.04':x='(iw-1920)*(0.30+0.40*(on/{frames}))':y='(ih-1080)*0.50':d={frames}:s=1920x1080:fps=30,"
                f"setsar=1,format=rgba,fade=t=in:st={fade_st:.2f}:d={fade_d:.2f}:alpha=1[v1];"
                "[v0][v1]overlay=0:0:format=auto,format=yuv420p[vout]"
            ),
            "-map", "[vout]", "-map", "2:a:0",
            "-t", f"{target_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, 0.12, max(0.60, d - 0.12))

    trim_st = max(0.0, sp_st - 0.16)
    trim_en = min(raw_dur, sp_en + 0.22)
    if trim_en - trim_st < 1.50:
        trim_st = 0.0
        trim_en = max(2.0, raw_dur - 0.10)
    clip_dur = trim_en - trim_st
    rel_sp_st = max(0.04, sp_st - trim_st)
    rel_sp_en = min(clip_dur - 0.04, sp_en - trim_st)

    if voice == "genie":
        a_eq = (
            "highpass=f=85,"
            "equalizer=f=220:t=q:w=1.1:g=1.5,"
            "equalizer=f=3200:t=q:w=1.1:g=-2.8,"
            "lowpass=f=11200"
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
        # Two-Camera Theatrical Edit: Camera A (Revolving Orbit `0..48%`) -> Camera B (Intimate Close-Up `48%..100%`)
        seg1_dur = round(clip_dur * 0.48, 3)
        seg2_dur = max(0.80, clip_dur - seg1_dur)
        orbit_dir = int(entry.get("orbit_dir", 1))
        cu_zoom = float(entry.get("cu_zoom", 1.28))
        cu_fx = float(entry.get("cu_fx", 0.50))
        cu_fy = float(entry.get("cu_fy", 0.22))

        cu_w = even_px(1920 * cu_zoom)
        cu_h = even_px(1080 * cu_zoom)

        if entry.get("hflip"):
            pre_vf = entry.get(
                "hflip_vf",
                "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,hflip",
            )
        else:
            pre_vf = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"

        x_orb = f"(iw-1920)*(0.20+0.60*(t/{seg1_dur:.3f}))" if orbit_dir >= 0 else f"(iw-1920)*(0.80-0.60*(t/{seg1_dur:.3f}))"
        y_orb = f"(ih-1080)*(0.45-0.18*sin(PI*t/{seg1_dur:.3f}))"

        x_cu = f"clip((iw-1920)*({cu_fx:.3f}-0.045+0.090*(t/{seg2_dur:.3f})),0,iw-1920)"
        y_cu = f"clip((ih-1080)*({cu_fy:.3f}-0.020*(t/{seg2_dur:.3f})),0,ih-1080)"

        cmd = ["ffmpeg", "-y", "-i", str(src_mp4)]
        fc = [
            f"[0:v]trim=start={trim_st:.3f}:end={trim_en:.3f},setpts=PTS-STARTPTS,fps=30,{pre_vf},split=2[vraw1][vraw2]",
            f"[vraw1]trim=start=0:end={seg1_dur:.3f},setpts=PTS-STARTPTS,"
            f"scale=2208:1242,crop=1920:1080:x='{x_orb}':y='{y_orb}',"
            "eq=contrast=1.02:saturation=1.03,vignette=PI/8.5,setsar=1,format=yuv420p[cam_a_raw]",
            f"[vraw2]trim=start={seg1_dur:.3f}:end={clip_dur:.3f},setpts=PTS-STARTPTS,"
            f"scale={cu_w}:{cu_h},crop=1920:1080:x='{x_cu}':y='{y_cu}',"
            "eq=contrast=1.04:saturation=1.05,vignette=PI/6.5,setsar=1,format=yuv420p[cam_b]",
        ]
        if ov_path:
            # Curved-glass holographic refraction locks to Camera A (wide studio angle) and cuts cleanly when punching to Close-Up!
            cmd += ["-loop", "1", "-t", f"{seg1_dur:.3f}", "-i", str(ov_path)]
            fc.append(
                f"[1:v]fade=t=in:st=0.10:d=0.25:alpha=1,"
                f"fade=t=out:st={max(0.50, seg1_dur - 0.25):.2f}:d=0.22:alpha=1[ov]"
            )
            fc.append("[cam_a_raw][ov]overlay=0:0:format=auto,format=yuv420p[cam_a]")
        else:
            fc.append("[cam_a_raw]format=yuv420p[cam_a]")

        fc.append("[cam_a][cam_b]concat=n=2:v=1:a=0,format=yuv420p[vout]")
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

    if layout == "audio_over_video":
        # 2-Angle Edit on `v4_ig_02.mp4` Curved-Glass Holographic Charts (Wide Orbit -> 1.28x Chart Close-Up)!
        v_src = Path(entry["video_src"])
        v_dur = probe_duration(v_src)
        v_ss = float(entry.get("video_ss", 0.0))
        v_avail = max(0.5, v_dur - v_ss - 0.05)
        v_take = min(v_avail, clip_dur)
        pts_v = (clip_dur / v_take) if clip_dur > v_take + 0.01 else 1.0

        seg1_dur = round(clip_dur * 0.50, 3)
        seg2_dur = max(0.80, clip_dur - seg1_dur)
        cu_zoom = float(entry.get("cu_zoom", 1.28))
        cu_fx = float(entry.get("cu_fx", 0.34))
        cu_fy = float(entry.get("cu_fy", 0.34))
        cu_w, cu_h = even_px(1920 * cu_zoom), even_px(1080 * cu_zoom)

        cmd = ["ffmpeg", "-y", "-i", str(src_mp4), "-i", str(v_src)]
        fc = [
            f"[1:v]trim=start={v_ss:.3f}:end={v_ss + v_take:.3f},setpts={pts_v:.5f}*(PTS-STARTPTS),"
            "fps=30,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,split=2[vh1][vh2]",
            f"[vh1]trim=0:{seg1_dur:.3f},setpts=PTS-STARTPTS,"
            f"scale=2208:1242,crop=1920:1080:x='(iw-1920)*(0.15+0.65*(t/{seg1_dur:.3f}))':y='(ih-1080)*0.45',"
            "eq=contrast=1.03:saturation=1.05,vignette=PI/8,setsar=1,format=yuv420p[va]",
            f"[vh2]trim={seg1_dur:.3f}:{clip_dur:.3f},setpts=PTS-STARTPTS,"
            f"scale={cu_w}:{cu_h},crop=1920:1080:x='clip((iw-1920)*({cu_fx:.3f}+0.10*(t/{seg2_dur:.3f})),0,iw-1920)':y='(ih-1080)*{cu_fy:.3f}',"
            "eq=contrast=1.05:saturation=1.06,vignette=PI/6.5,setsar=1,format=yuv420p[vb]",
            "[va][vb]concat=n=2:v=1:a=0,format=yuv420p[vout]",
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

    if layout == "audio_over_glass_pan":
        # 2-Angle Close-Up Whip-Cut across Left Curved Glass (`200,000+ SHIFTS | 60,000 BUYOUTS`) -> Right Curved Glass (`7D SCORE >= 4/7`)!
        img_src = Path(entry["image_src"])
        seg1_dur = round(clip_dur * 0.52, 3)
        seg2_dur = max(0.80, clip_dur - seg1_dur)
        f1 = max(20, int(round(seg1_dur * 30)) + 2)
        f2 = max(20, int(round(seg2_dur * 30)) + 2)

        cmd = [
            "ffmpeg", "-y",
            "-i", str(src_mp4),
            "-loop", "1", "-t", f"{seg1_dur + 0.20:.3f}", "-i", str(img_src),
            "-loop", "1", "-t", f"{seg2_dur + 0.20:.3f}", "-i", str(img_src),
            "-filter_complex", (
                f"[1:v]scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
                f"zoompan=z='1.55+0.08*(on/{f1})':x='(iw-iw/zoom)*(0.03+0.20*(on/{f1}))':y='(ih-ih/zoom)*0.78':d={f1}:s=1920x1080:fps=30,"
                f"trim=0:{seg1_dur:.3f},setpts=PTS-STARTPTS,eq=contrast=1.04:saturation=1.05,vignette=PI/7.5,setsar=1,format=yuv420p[g1];"
                f"[2:v]scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
                f"zoompan=z='1.55+0.08*(on/{f2})':x='(iw-iw/zoom)*(0.77+0.19*(on/{f2}))':y='(ih-ih/zoom)*0.78':d={f2}:s=1920x1080:fps=30,"
                f"trim=0:{seg2_dur:.3f},setpts=PTS-STARTPTS,eq=contrast=1.04:saturation=1.05,vignette=PI/7.5,setsar=1,format=yuv420p[g2];"
                "[g1][g2]concat=n=2:v=1:a=0,format=yuv420p[vout];"
                f"[0:a]{a_chain}[aout]"
            ),
            "-map", "[vout]", "-map", "[aout]",
            "-t", f"{clip_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, rel_sp_st, min(d - 0.04, rel_sp_en))

    if layout == "summon_lamp_awakening":
        # Angle 1 (`0..48%`): Orbital crane descent on `v7_wide_wall_dormant` -> Angle 2 (`48%..end`): 360-degree Revolving Golden Lamp Awakening (`batch_05_02.mp4`)!
        img_src = Path(entry["image_src"])
        lamp_mp4 = Path(entry["lamp_mp4"])
        lamp_ss = float(entry.get("lamp_ss", 0.5))

        seg1_dur = round(clip_dur * 0.48, 3)
        seg2_dur = max(1.20, clip_dur - seg1_dur)
        f1 = max(20, int(round(seg1_dur * 30)) + 2)

        l_avail = max(0.5, probe_duration(lamp_mp4) - lamp_ss - 0.05)
        l_take = min(l_avail, seg2_dur)
        pts_l = (seg2_dur / l_take) if seg2_dur > l_take + 0.01 else 1.0

        cmd = [
            "ffmpeg", "-y",
            "-i", str(src_mp4),
            "-loop", "1", "-t", f"{seg1_dur + 0.20:.3f}", "-i", str(img_src),
            "-i", str(lamp_mp4),
            "-filter_complex", (
                f"[1:v]scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
                f"zoompan=z='1.04+0.18*(on/{f1})':x='(iw-iw/zoom)*(0.38+0.24*(on/{f1}))':y='(ih-ih/zoom)*(0.45+0.12*(on/{f1}))':d={f1}:s=1920x1080:fps=30,"
                f"trim=0:{seg1_dur:.3f},setpts=PTS-STARTPTS,eq=contrast=1.03:saturation=1.04,vignette=PI/8,setsar=1,format=yuv420p[s1];"
                f"[2:v]trim=start={lamp_ss:.3f}:end={lamp_ss + l_take:.3f},setpts={pts_l:.5f}*(PTS-STARTPTS),fps=30,"
                f"scale=2208:1242:force_original_aspect_ratio=increase,crop=1920:1080:x='(iw-1920)*(0.25+0.50*(t/{seg2_dur:.3f}))':y='(ih-1080)*0.48',"
                "eq=contrast=1.05:saturation=1.08,vignette=PI/7,setsar=1,format=yuv420p[s2];"
                "[s1][s2]concat=n=2:v=1:a=0,format=yuv420p[vout];"
                f"[0:a]{a_chain}[aout]"
            ),
            "-map", "[vout]", "-map", "[aout]",
            "-t", f"{clip_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, rel_sp_st, min(d - 0.04, rel_sp_en))

    if layout == "genie_two_angle_cinema":
        # Angle 1 (`0..48%`): Wide Revolving Arena Sweep on `v7_wide_wall_genie_16x9.jpg`
        # Angle 2 (`48%..100%`): Dramatic 1.48x -> 1.66x Close-Up Revolving Push-In on the Cross-Legged Karmic Genie!
        img_src = Path(entry["image_src"])
        seg1_dur = round(clip_dur * 0.48, 3)
        seg2_dur = max(1.20, clip_dur - seg1_dur)
        f1 = max(20, int(round(seg1_dur * 30)) + 2)
        f2 = max(20, int(round(seg2_dur * 30)) + 2)

        cmd = [
            "ffmpeg", "-y",
            "-i", str(src_mp4),
            "-loop", "1", "-t", f"{seg1_dur + 0.20:.3f}", "-i", str(img_src),
            "-loop", "1", "-t", f"{seg2_dur + 0.20:.3f}", "-i", str(img_src),
            "-filter_complex", (
                f"[1:v]scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
                f"zoompan=z='1.02+0.10*(on/{f1})':x='(iw-iw/zoom)*(0.25+0.50*(on/{f1}))':y='(ih-ih/zoom)*0.44':d={f1}:s=1920x1080:fps=30,"
                f"trim=0:{seg1_dur:.3f},setpts=PTS-STARTPTS,eq=contrast=1.03:saturation=1.05,vignette=PI/8,setsar=1,format=yuv420p[g1];"
                f"[2:v]scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
                f"zoompan=z='1.48+0.18*(on/{f2})':x='(iw-iw/zoom)*(0.47+0.06*(on/{f2}))':y='(ih-ih/zoom)*0.33':d={f2}:s=1920x1080:fps=30,"
                f"trim=0:{seg2_dur:.3f},setpts=PTS-STARTPTS,eq=contrast=1.05:saturation=1.08,vignette=PI/6.5,setsar=1,format=yuv420p[g2];"
                "[g1][g2]concat=n=2:v=1:a=0,format=yuv420p[vout];"
                f"[0:a]{a_chain}[aout]"
            ),
            "-map", "[vout]", "-map", "[aout]",
            "-t", f"{clip_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, rel_sp_st, min(d - 0.04, rel_sp_en))

    if layout in ("pip75", "audio_over_pip75"):
        # Revolving 3D `v7` Studio Background + 2-Angle Orbital-to-Close-Up Cut inside the `1440x810` (`75%`) window!
        frames = max(30, int(round(clip_dur * 30)) + 5)
        seg1_dur = round(clip_dur * 0.48, 3)
        seg2_dur = max(0.80, clip_dur - seg1_dur)
        orbit_dir = int(entry.get("orbit_dir", 1))
        pip_zoom = float(entry.get("pip_zoom", 1.26))
        pip_fx = float(entry.get("pip_fx", 0.50))
        pip_fy = float(entry.get("pip_fy", 0.34))

        pw_a, ph_a = even_px(1432 * 1.12), even_px(802 * 1.12)
        pw_b, ph_b = even_px(1432 * pip_zoom), even_px(802 * pip_zoom)

        if layout == "audio_over_pip75":
            v_src = Path(entry["video_src"])
            v_ss = float(entry.get("video_ss", 0.0))
            v_avail = max(0.5, probe_duration(v_src) - v_ss - 0.05)
            v_take = min(v_avail, clip_dur)
            pts_v = (clip_dur / v_take) if clip_dur > v_take + 0.01 else 1.0
            fg_trim = f"trim=start={v_ss:.3f}:end={v_ss + v_take:.3f},setpts={pts_v:.5f}*(PTS-STARTPTS)"
            cmd = [
                "ffmpeg", "-y",
                "-i", str(src_mp4),
                "-i", str(v_src),
                "-loop", "1", "-t", f"{clip_dur + 0.25:.3f}", "-i", str(DORMANT_STAGE_JPG),
            ]
            bg_idx, fg_idx = 2, 1
        else:
            fg_trim = f"trim=start={trim_st:.3f}:end={trim_en:.3f},setpts=PTS-STARTPTS"
            cmd = [
                "ffmpeg", "-y",
                "-i", str(src_mp4),
                "-loop", "1", "-t", f"{clip_dur + 0.25:.3f}", "-i", str(DORMANT_STAGE_JPG),
            ]
            bg_idx, fg_idx = 1, 0

        bg_x = f"(iw-1920)*(0.08+0.84*(on/{frames}))" if orbit_dir >= 0 else f"(iw-1920)*(0.92-0.84*(on/{frames}))"
        fg_xa = f"(iw-1432)*(0.20+0.60*(t/{seg1_dur:.3f}))" if orbit_dir >= 0 else f"(iw-1432)*(0.80-0.60*(t/{seg1_dur:.3f}))"
        fg_xb = f"clip((iw-1432)*({pip_fx:.3f}-0.04+0.08*(t/{seg2_dur:.3f})),0,iw-1432)"
        fg_yb = f"clip((ih-802)*({pip_fy:.3f}-0.02*(t/{seg2_dur:.3f})),0,ih-802)"

        fc = [
            f"[{bg_idx}:v]scale=2140:1204:force_original_aspect_ratio=increase,crop=2140:1204,"
            f"zoompan=z='1.00':x='{bg_x}':y='(ih-1080)*(0.52-0.16*sin(PI*on/{frames}))':d={frames}:s=1920x1080:fps=30,"
            f"trim=0:{clip_dur:.3f},setpts=PTS-STARTPTS,"
            "eq=brightness=-0.03:saturation=0.98,vignette=PI/9,setsar=1,format=yuv420p[bg]",
            f"[{fg_idx}:v]{fg_trim},fps=30,scale=1432:802:force_original_aspect_ratio=increase,crop=1432:802,split=2[fraw1][fraw2]",
            f"[fraw1]trim=0:{seg1_dur:.3f},setpts=PTS-STARTPTS,"
            f"scale={pw_a}:{ph_a},crop=1432:802:x='{fg_xa}':y='(ih-802)*0.46',"
            "eq=contrast=1.02:saturation=1.03,setsar=1,format=yuv420p[fa]",
            f"[fraw2]trim={seg1_dur:.3f}:{clip_dur:.3f},setpts=PTS-STARTPTS,"
            f"scale={pw_b}:{ph_b},crop=1432:802:x='{fg_xb}':y='{fg_yb}',"
            "eq=contrast=1.04:saturation=1.05,vignette=PI/7,setsar=1,format=yuv420p[fb]",
            "[fa][fb]concat=n=2:v=1:a=0,pad=w=1440:h=810:x=4:y=4:color=#EBC670,setsar=1,format=yuv420p[fg]",
            "[bg][fg]overlay=240:135:shortest=1,format=yuv420p[vout]",
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

    if layout == "pip75_broll_cut":
        # Revolving 3D `v7` Studio Background + Multi-Clip Story Cut inside `pip75` (`src` -> final `2.4s` `broll_mp4`)!
        broll_mp4 = Path(entry["broll_mp4"])
        broll_ss = float(entry.get("broll_ss", 1.2))
        seg2_dur = min(float(entry.get("broll_dur", 2.40)), max(1.40, clip_dur - 1.80))
        seg1_dur = clip_dur - seg2_dur
        frames = max(30, int(round(clip_dur * 30)) + 5)
        orbit_dir = int(entry.get("orbit_dir", -1))

        b_avail = max(0.5, probe_duration(broll_mp4) - broll_ss - 0.05)
        b_take = min(b_avail, seg2_dur)
        pts_b = (seg2_dur / b_take) if seg2_dur > b_take + 0.01 else 1.0

        pw_a, ph_a = even_px(1432 * 1.12), even_px(802 * 1.12)
        pw_b, ph_b = even_px(1432 * 1.18), even_px(802 * 1.18)
        bg_x = f"(iw-1920)*(0.08+0.84*(on/{frames}))" if orbit_dir >= 0 else f"(iw-1920)*(0.92-0.84*(on/{frames}))"

        cmd = [
            "ffmpeg", "-y",
            "-i", str(src_mp4),
            "-i", str(broll_mp4),
            "-loop", "1", "-t", f"{clip_dur + 0.25:.3f}", "-i", str(DORMANT_STAGE_JPG),
        ]
        fc = [
            f"[2:v]scale=2140:1204:force_original_aspect_ratio=increase,crop=2140:1204,"
            f"zoompan=z='1.00':x='{bg_x}':y='(ih-1080)*(0.52-0.16*sin(PI*on/{frames}))':d={frames}:s=1920x1080:fps=30,"
            f"trim=0:{clip_dur:.3f},setpts=PTS-STARTPTS,"
            "eq=brightness=-0.03:saturation=0.98,vignette=PI/9,setsar=1,format=yuv420p[bg]",
            f"[0:v]trim=start={trim_st:.3f}:end={trim_st + seg1_dur:.3f},setpts=PTS-STARTPTS,fps=30,"
            f"scale={pw_a}:{ph_a}:force_original_aspect_ratio=increase,crop=1432:802:x='(iw-1432)*(0.22+0.56*(t/{seg1_dur:.3f}))':y='(ih-802)*0.45',"
            "eq=contrast=1.02:saturation=1.03,setsar=1,format=yuv420p[fa]",
            f"[1:v]trim=start={broll_ss:.3f}:end={broll_ss + b_take:.3f},setpts={pts_b:.5f}*(PTS-STARTPTS),fps=30,"
            f"scale={pw_b}:{ph_b}:force_original_aspect_ratio=increase,crop=1432:802:x='(iw-1432)*(0.75-0.50*(t/{seg2_dur:.3f}))':y='(ih-802)*0.42',"
            "eq=contrast=1.04:saturation=1.05,vignette=PI/7,setsar=1,format=yuv420p[fb]",
            "[fa][fb]concat=n=2:v=1:a=0,pad=w=1440:h=810:x=4:y=4:color=#EBC670,setsar=1,format=yuv420p[fg]",
            "[bg][fg]overlay=240:135:shortest=1,format=yuv420p[vout]",
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

    if layout in ("split_full_to_pip75", "split_tail_pip75"):
        v2_mp4 = Path(entry["v2_pip_mp4"])
        v2_ss = float(entry.get("v2_pip_ss", 2.0))
        cu_fx = float(entry.get("cu_fx", 0.65))
        cu_fy = float(entry.get("cu_fy", 0.24))

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
            f"[1:v]trim=start={v1_ss:.3f}:end={v1_ss + seg1_dur:.3f},setpts=PTS-STARTPTS,fps=30,"
            f"scale=2400:1350:force_original_aspect_ratio=increase,"
            f"crop=1920:1080:x='clip((iw-1920)*({cu_fx:.3f}-0.05+0.10*(t/{seg1_dur:.3f})),0,iw-1920)':y='(ih-1080)*{cu_fy:.3f}',"
            "eq=contrast=1.03:saturation=1.04,vignette=PI/7.5,setsar=1,format=yuv420p[v_seg1]",
            f"[3:v]scale=2140:1204:force_original_aspect_ratio=increase,crop=2140:1204,"
            f"zoompan=z='1.00':x='(iw-1920)*(0.12+0.76*(on/{frames2}))':y='(ih-1080)*0.48':d={frames2}:s=1920x1080:fps=30,"
            f"trim=0:{seg2_dur:.3f},setpts=PTS-STARTPTS,"
            "eq=brightness=-0.03:saturation=0.98,vignette=PI/9,setsar=1,format=yuv420p[bg2]",
            f"[2:v]trim=start={v2_ss:.3f}:end={v2_ss + v2_take:.3f},setpts={pts_v2:.5f}*(PTS-STARTPTS),fps=30,"
            f"scale=1646:922:force_original_aspect_ratio=increase,crop=1432:802:x='(iw-1432)*(0.25+0.50*(t/{seg2_dur:.3f}))':y='(ih-802)*0.40',"
            "eq=contrast=1.04:saturation=1.06,pad=w=1440:h=810:x=4:y=4:color=#EBC670,setsar=1,format=yuv420p[fg2]",
            "[bg2][fg2]overlay=240:135:shortest=1,format=yuv420p[v_seg2]",
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


def build_master_ass_v41(
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
    placed cleanly at `MarginV=28` (below `y=945` of the `pip75` gold frame).
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
            (6.50, min(cold_dur - 0.20, 9.25), "TitleGold", "THE 7D WAY  •  Tick ≥ 4 of 7D to Stay the Course — Or Change Your Route!"),
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
    print(f"1️⃣ Verifying v4.1 Theatrical Cinema Director's Cut & Editorial Purity across all {total_slots} shots...", flush=True)
    for entry in V3_SHOT_LEDGER:
        src = Path(entry["src"])
        if not src.exists():
            raise FileNotFoundError(f"Missing clip/image for {entry['sid']}: {src}")
        for extra_k in ("video_src", "image_src", "broll_mp4", "lamp_mp4", "v2_pip_mp4"):
            if extra_k in entry and not Path(entry[extra_k]).exists():
                raise FileNotFoundError(f"Missing {extra_k} for {entry['sid']}: {entry[extra_k]}")
        for ln in entry["lines"]:
            assert_editorial_purity(ln, entry["sid"])

    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")

    print("2️⃣ Rendering 3-Angle Theatrical Cold Open (9.5s) & Finale Logo Card (11.0s)...", flush=True)
    co_mp4 = TEMP_DIR / "part_00_cold_open_v41.mp4"
    cold_dur = render_cold_open_v41(co_mp4)

    fin_mp4 = TEMP_DIR / "part_99_finale_logo_v41.mp4"
    fin_dur = render_finale_outro_v41(fin_mp4)

    print(f"3️⃣ Directing all {total_slots} v4.1 shots (Revolving Orbits + Multi-Cam Close-Ups + 360 Lamp Awakening + 2-Angle Genie)...", flush=True)
    parts = [co_mp4]
    cursor = cold_dur
    shot_timings = []

    for idx, entry in enumerate(V3_SHOT_LEDGER, 1):
        sid = entry["sid"]
        src = Path(entry["src"])
        if entry["layout"] == "image_dissolve":
            raw_dur = float(entry["visual_dur"])
            sp_st, sp_en, txt = 0.0, raw_dur, "[dissolve]"
        else:
            txt, sp_st, sp_en, raw_dur = transcribe_clip_whisper(src, model, entry["hint_sp"])
            assert_editorial_purity(txt, f"{sid}_audio_transcript")

        out_p = TEMP_DIR / f"v41_part_{idx:02d}_{sid}.mp4"
        dur, rel_st, rel_en = render_v41_shot(
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
        flip_tag = " [hflip->RIGHT]" if entry.get("hflip") else ""
        cu_tag = f" [Orbit->CU {entry['cu_zoom']:.2f}x]" if "cu_zoom" in entry else ""
        print(
            f"    [{idx:02d}/{total_slots}] {sid} [{entry['layout']}]{flip_tag}{cu_tag} <- {src.name} "
            f"({dur:.2f}s, cum={cursor:.1f}s){ov_tag}",
            flush=True,
        )

    finale_start = cursor
    parts.append(fin_mp4)

    concat_txt = TEMP_DIR / "master_v41_concat.txt"
    concat_txt.write_text("\n".join(f"file '{p}'" for p in parts) + "\n", encoding="utf-8")
    stitched_mp4 = TEMP_DIR / "stitched_v41_raw.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy", str(stitched_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    actual_total = probe_duration(stitched_mp4)
    print(f"4️⃣ Stitched raw v4.1 Cinema Director's Cut runtime: {actual_total:.2f}s ({int(actual_total//60):02d}:{actual_total%60:05.2f})", flush=True)

    ass_path = TEMP_DIR / "s01e01_v41_interactive.ass"
    build_master_ass_v41(ass_path, cold_dur, shot_timings, finale_start, actual_total, include_bookends=True)

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
    print(f"\n🏆 S01E01 v4.1 THEATRICAL CINEMA DIRECTOR'S CUT READY: {OUT_MP4}")
    print(f"   Runtime: {int(final_d//60):02d}:{final_d%60:05.2f} ({final_d:.2f}s) | Size: {OUT_MP4.stat().st_size/1e6:.2f} MB", flush=True)


if __name__ == "__main__":
    main()
