#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master 360p (640x360, 30fps, -14 LUFS) Broadcast Assembler for:
  1. S01E00: Pilot — "The 7D Way — Pioneers of the New World" (with the Canonical Vedic 7D Intro Narration
     + zero static drawings + Side-by-Side Curved-Glass Metrics & Philosopher Quote HUD alongside
     Adult Narrator @Me and 4-year-old Bala-Rishi @Me across all 7 Virtues).
  2. S01E01: Episode 1 (D1) — "Respect Your DUTY First." (Full-blown 41-beat / 5-minute 10-second episode
     starting with the Canonical Vedic 7D Introductory Narration -> all 7 Pages of the D1 Treatise ->
     Age 4 Play [Body], Age 24 Think [Mind], Age 54 Thank [Soul], Male 50/15/15/10/10 Porul Matrix,
     Female 100% Arul & Daily Pooja Matrix, Why Family Life [Karma Margam] is Safest & Fastest with
     Rule Relaxations vs. Strict Solitary Jnana/Bhakti, Three Wise Eastern Philosophers' Take, and
     Live 1-10 [70-Point, <35/70] Conscience Self-Audit Scorecard).
"""

import asyncio
import json
import shutil
import subprocess
import wave
from pathlib import Path
import edge_tts
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
PILOT_DIR = REPO_DIR / "episodes" / "S01E00_Pilot_The_7D_Way"
EP01_DIR = REPO_DIR / "episodes" / "S01E01_Employees_vs_Tech_CEO"
MASTERS_DIR = REPO_DIR / "assets" / "studio_v5_masters"
THEME_WAV = REPO_DIR / "assets" / "theme" / "official_karmic_genie_7d_theme_song.wav"
LOGO_JPG = REPO_DIR / "assets" / "logo" / "official_karmic_genie_show_logo.jpg"

PILOT_STAGE_JPG = MASTERS_DIR / "v8_pilot_7d_scorecard_stage_16x9.jpg"
GENIE_BALA_JPG = MASTERS_DIR / "v9_genie_4yo_bala_rishi_16x9.jpg"
HOST_IVORY_JPG = MASTERS_DIR / "v9_host_adult_ivory_bandhgala_16x9.jpg"
GENIE_INDIGO_JPG = MASTERS_DIR / "v8_genie_royal_indigo_sage_16x9.jpg"

CLIP_MAP_JSON = PILOT_DIR / "pilot_clip_map.json"
V3_CLIPS_ROOT = EP01_DIR / "flow_v3_interactive_clips"
V1_CLIPS_ROOT = EP01_DIR / "flow_16x9_clips"

PREV_BRAIN = Path("/home/shishyan/.gemini/antigravity/brain/b55fc9ea-1a2e-45b9-8d71-a53ee11caf0c")
CUR_BRAIN = Path("/home/shishyan/.gemini/antigravity/brain/5d5e5767-c891-45b6-b050-31578382d046")

TEMP_DIR = PILOT_DIR / "temp_vedic_7d_360p_build"
HUD_DIR = TEMP_DIR / "hud_cards"

OUT_RENDERS = REPO_DIR / "renders"
OUT_S01E01_360P = OUT_RENDERS / "Karmic_Genie_Show_S01E01_Respect_Your_DUTY_First_360p.mp4"
OUT_PILOT_360P = OUT_RENDERS / "Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_360p.mp4"

ART_S01E01_360P = CUR_BRAIN / "Karmic_Genie_Show_S01E01_Respect_Your_DUTY_First_360p.mp4"
ART_PILOT_360P = CUR_BRAIN / "Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_360p.mp4"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def probe_duration(path: Path) -> float:
    res = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)
    ]).decode())
    return float(res["format"]["duration"])


def detect_speech_bounds_rms(audio_path: Path, fallback: tuple[float, float] = (0.10, 7.40)) -> tuple[float, float, float]:
    raw_dur = probe_duration(audio_path)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    wav_tmp = TEMP_DIR / f"rms_{audio_path.stem}.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(audio_path), "-vn", "-ac", "1", "-ar", "16000", str(wav_tmp)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(str(wav_tmp), "rb") as wf:
        arr = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    win = 800
    if len(arr) < win * 4:
        return (fallback[0], min(raw_dur, fallback[1]), raw_dur)
    n_wins = len(arr) // win
    rms = np.sqrt(np.mean(arr[: n_wins * win].reshape(n_wins, win) ** 2, axis=1))
    peak = float(np.percentile(rms, 95))
    thresh = max(0.010, peak * 0.14)
    active = np.where(rms >= thresh)[0]
    if len(active) < 3:
        return (fallback[0], min(raw_dur, fallback[1]), raw_dur)
    sp_st = max(0.06, float(active[0] * 0.05))
    sp_en = min(raw_dur - 0.06, float((active[-1] + 1) * 0.05))
    return (sp_st, sp_en, raw_dur)


async def _synth_tts(text: str, role: str, out_mp3: Path):
    if role == "bala":
        comm = edge_tts.Communicate(text, voice="en-IN-NeerjaExpressiveNeural", rate="+6%", pitch="+28Hz")
    elif role == "genie":
        comm = edge_tts.Communicate(text, voice="en-IN-PrabhatNeural", rate="-4%", pitch="-8Hz")
    else:
        comm = edge_tts.Communicate(text, voice="en-IN-PrabhatNeural", rate="+4%", pitch="-2Hz")
    await comm.save(str(out_mp3))


def build_beat_audio(beat_id: str, text: str, role: str, target_dur: float = 7.50) -> tuple[Path, float, float, float]:
    """Synthesizes crystal-clear spoken narration fitted cleanly into `target_dur` (or slightly longer for Beat 00)."""
    out_wav = TEMP_DIR / f"aud_{beat_id}.wav"
    if out_wav.exists() and out_wav.stat().st_size > 10000:
        d = probe_duration(out_wav)
        return (out_wav, 0.12, max(1.0, d - 0.14), d)

    raw_mp3 = TEMP_DIR / f"raw_{beat_id}.mp3"
    asyncio.run(_synth_tts(text, role, raw_mp3))
    sp_st, sp_en, raw_dur = detect_speech_bounds_rms(raw_mp3, (0.05, 11.0))
    trim_st = max(0.0, sp_st - 0.06)
    trim_en = min(raw_dur, sp_en + 0.10)
    sp_len = max(1.0, trim_en - trim_st)

    usable = max(2.0, target_dur - 0.24)
    tempo = float(np.clip(sp_len / usable, 0.90, 1.24))

    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_mp3),
        "-af", (
            f"atrim=start={trim_st:.3f}:end={trim_en:.3f},asetpts=PTS-STARTPTS,"
            f"atempo={tempo:.4f},"
            "equalizer=f=170:width_type=o:width=1.2:g=2.0,"
            "equalizer=f=3200:width_type=o:width=1.0:g=1.4,"
            "highpass=f=80,lowpass=f=13000,"
            "adelay=110|110,"
            f"apad=whole_dur={target_dur:.3f},"
            f"afade=t=in:st=0:d=0.05,afade=t=out:st={max(0.2, target_dur-0.08):.3f}:d=0.08,"
            "aresample=48000,aformat=sample_fmts=s16:channel_layouts=stereo"
        ),
        "-t", f"{target_dur:.3f}", str(out_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    d = probe_duration(out_wav)
    return (out_wav, 0.11, max(1.0, d - 0.12), d)


def fit_font(draw: ImageDraw.ImageDraw, text: str, font_path: str, start_px: int, min_px: int, max_w: int):
    for sz in range(start_px, min_px - 1, -1):
        f = ImageFont.truetype(font_path, sz)
        w = draw.textbbox((0, 0), text, font=f)[2]
        if w <= max_w:
            return f
    return ImageFont.truetype(font_path, min_px)


def wrap_line(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines = []
    cur = words[0]
    for w in words[1:]:
        test = f"{cur} {w}"
        if draw.textbbox((0, 0), test, font=font)[2] <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def render_side_by_side_hud_png(
    hud_id: str,
    maxim_banner: str,
    header_tag: str,
    card_title: str,
    bullets: list[tuple[str, str]],
    footer_metric: str,
    score_badge: str = "D1 SCORE: 1–10 PTS  •  PASS >= 35 / 70",
) -> Path:
    """
    Renders a sleek, curved-glass translucent Side-by-Side HUD overlay (`1920x1080` RGBA)
    where:
      - Left half (`x=0..950`): Framing for Live @Me (Adult Narrator @Me or 4yo Bala-Rishi @Me)
        with a clean top-left golden wall maxim pill (`1. Respect Your DUTY First.`).
      - Right half (`x=960..1876`, `y=76..900`): Curved-Glass Sapphire & Brushed-Gold Metrics
        & Philosopher Quote HUD displaying stage cycles, proportional matrices (`Porul`/`Arul`),
        *Karma Margam* vs. *Jnana*/*Bhakti*, and verbatim Eastern Philosopher teachings.
    """
    HUD_DIR.mkdir(parents=True, exist_ok=True)
    out_png = HUD_DIR / f"hud_{hud_id}.png"
    im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # 1. Top-Left Golden Wall Maxim Pill over the Studio Stage (`x=42..890, y=34..88`)
    d.rounded_rectangle([42, 34, 890, 88], radius=14, fill=(10, 16, 28, 212), outline=(242, 204, 118, 240), width=2)
    f_max = fit_font(d, maxim_banner, FONT_BOLD, 24, 16, 820)
    d.text((62, 47), maxim_banner, font=f_max, fill=(255, 226, 148, 255))

    # 2. Right-Side Curved-Glass Metrics & Philosopher HUD Panel (`x=964..1878, y=34..892`)
    px0, py0, px1, py1 = 964, 34, 1878, 892
    d.rounded_rectangle([px0, py0, px1, py1], radius=24, fill=(8, 16, 30, 224), outline=(140, 225, 255, 210), width=3)
    d.rounded_rectangle([px0 + 5, py0 + 5, px1 - 5, py1 - 5], radius=20, outline=(245, 206, 122, 145), width=1)

    # Top Header Bar inside Right HUD
    d.rounded_rectangle([px0 + 16, py0 + 16, px1 - 16, py0 + 68], radius=12, fill=(18, 36, 64, 235), outline=(245, 206, 122, 190), width=1)
    f_htag = fit_font(d, header_tag, FONT_BOLD, 20, 13, (px1 - px0) - 56)
    d.text((px0 + 30, py0 + 29), header_tag, font=f_htag, fill=(182, 244, 255, 255))

    # Card Main Title
    f_ctitle = fit_font(d, card_title, FONT_BOLD, 27, 17, (px1 - px0) - 56)
    d.text((px0 + 28, py0 + 84), card_title, font=f_ctitle, fill=(255, 224, 138, 255))
    d.line([(px0 + 28, py0 + 124), (px1 - 28, py0 + 124)], fill=(245, 206, 122, 160), width=2)

    # Bullet Cards
    cur_y = py0 + 140
    max_text_w = (px1 - px0) - 76
    f_bhead = ImageFont.truetype(FONT_BOLD, 21)
    f_bbody = ImageFont.truetype(FONT_REG, 19)

    palette_map = {
        "gold": (255, 224, 140, 255),
        "cyan": (175, 245, 255, 255),
        "emerald": (160, 252, 208, 255),
        "amber": (255, 196, 132, 255),
        "white": (244, 250, 255, 255),
    }

    for b_label, b_text in bullets:
        col = palette_map.get("gold")
        if b_label.startswith("[GOLD]"):
            col = palette_map["gold"]
            b_label = b_label.replace("[GOLD]", "").strip()
        elif b_label.startswith("[CYAN]"):
            col = palette_map["cyan"]
            b_label = b_label.replace("[CYAN]", "").strip()
        elif b_label.startswith("[EMERALD]"):
            col = palette_map["emerald"]
            b_label = b_label.replace("[EMERALD]", "").strip()
        elif b_label.startswith("[AMBER]"):
            col = palette_map["amber"]
            b_label = b_label.replace("[AMBER]", "").strip()

        wrapped_body = wrap_line(d, b_text, f_bbody, max_text_w - 16)
        box_h = 38 + len(wrapped_body) * 26 + 14
        if cur_y + box_h > py1 - 118:
            break

        d.rounded_rectangle(
            [px0 + 22, cur_y, px1 - 22, cur_y + box_h],
            radius=14,
            fill=(14, 26, 46, 215),
            outline=(90, 165, 210, 125),
            width=1,
        )
        f_bh = fit_font(d, b_label, FONT_BOLD, 21, 14, max_text_w - 16)
        d.text((px0 + 38, cur_y + 10), b_label, font=f_bh, fill=col)
        ty = cur_y + 38
        for ln in wrapped_body:
            d.text((px0 + 38, ty), ln, font=f_bbody, fill=palette_map["white"])
            ty += 26
        cur_y += box_h + 14

    # Footer Metric Box + 7D Compass Score Strip
    fy0 = py1 - 104
    d.rounded_rectangle([px0 + 20, fy0, px1 - 20, py1 - 18], radius=14, fill=(20, 38, 62, 238), outline=(245, 206, 122, 215), width=2)
    f_foot = fit_font(d, footer_metric, FONT_BOLD, 19, 13, (px1 - px0) - 68)
    d.text((px0 + 34, fy0 + 12), footer_metric, font=f_foot, fill=(162, 252, 212, 255))

    f_sc = fit_font(d, score_badge, FONT_BOLD, 17, 12, (px1 - px0) - 68)
    d.text((px0 + 34, fy0 + 46), score_badge, font=f_sc, fill=(255, 222, 142, 255))

    im.save(out_png)
    return out_png


def render_side_by_side_beat_mp4(
    beat_id: str,
    video_clip: Path,
    audio_wav: Path,
    hud_png: Path,
    target_dur: float,
    cam_dir: int = 1,
) -> Path:
    """
    Renders a single Side-by-Side (`Left: @Me on Studio Stage`, `Right: Curved-Glass Metrics HUD`)
    broadcast segment at internal 1920x1080 resolution with fluid 30fps motion.
    """
    out_mp4 = TEMP_DIR / f"seg_{beat_id}.mp4"
    if out_mp4.exists() and out_mp4.stat().st_size > 15000:
        return out_mp4

    v_dur = probe_duration(video_clip)
    ss = 0.25 if v_dur > 4.0 else 0.0

    # Dynamic multi-camera drift on the Left Stage (`888x776`) so @Me stays centered and expressive
    crop_x = (
        f"clip((iw-888)*(0.45+0.10*sin(PI*t/{target_dur:.2f})),0,iw-888)"
        if cam_dir >= 0
        else f"clip((iw-888)*(0.55-0.10*sin(PI*t/{target_dur:.2f})),0,iw-888)"
    )

    bg_x = (
        f"(iw-1920)*(0.15+0.70*(t/{target_dur:.2f}))"
        if cam_dir >= 0
        else f"(iw-1920)*(0.85-0.70*(t/{target_dur:.2f}))"
    )

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-ss", f"{ss:.2f}", "-i", str(video_clip),
        "-loop", "1", "-r", "30", "-t", f"{target_dur + 0.15:.3f}", "-i", str(PILOT_STAGE_JPG),
        "-i", str(audio_wav),
        "-loop", "1", "-r", "30", "-t", f"{target_dur + 0.15:.3f}", "-i", str(hud_png),
        "-filter_complex", (
            # Full-frame revolving marble studio backdrop (fast crop pan)
            f"[1:v]scale=2160:1215:force_original_aspect_ratio=increase,crop=1920:1080:x='{bg_x}':y='(ih-1080)*0.50',"
            f"trim=0:{target_dur:.3f},setpts=PTS-STARTPTS,"
            "eq=brightness=-0.04:saturation=0.96,setsar=1,format=yuv420p[bg];"
            # Left Stage Panel (`896x784` at `x=42, y=104`) featuring live @Me (Adult or 4yo Bala-Rishi)
            f"[0:v]trim=0:{target_dur:.3f},setpts=PTS-STARTPTS,fps=30,"
            f"scale=1520:855:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop=888:776:x='{crop_x}':y='(ih-776)*0.24',"
            "eq=contrast=1.03:saturation=1.04,"
            "pad=w=896:h=784:x=4:y=4:color=#EBC670,setsar=1,format=yuv420p[left_me];"
            "[bg][left_me]overlay=42:104:shortest=1,format=yuv420p[st];"
            # Overlay the Right Curved-Glass Metrics & Philosopher HUD + Top-Left Maxim Banner
            f"[3:v]fade=t=in:st=0.06:d=0.18:alpha=1,fade=t=out:st={max(0.4, target_dur-0.22):.2f}:d=0.18:alpha=1[hud];"
            "[st][hud]overlay=0:0:format=auto,format=yuv420p[vout]"
        ),
        "-map", "[vout]", "-map", "2:a:0",
        "-t", f"{target_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "ultrafast", "-crf", "19",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_mp4


def format_ass_time(sec: float) -> str:
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def split_caption_chunks(text: str, max_chars: int = 62) -> list[str]:
    words = text.strip().split()
    if not words:
        return []
    chunks = []
    cur = words[0]
    for w in words[1:]:
        if len(cur) + 1 + len(w) <= max_chars:
            cur = f"{cur} {w}"
        else:
            chunks.append(cur)
            cur = w
    chunks.append(cur)
    return chunks


# ======================================================================================
# COMPLETE 41-BEAT (`Beat 00` VEDIC INTRO + `Beats 01..40`) SPECIFICATION FOR S01E01:
#   "Respect Your DUTY First."
# ======================================================================================
S01E01_BEATS = [
    # BEAT 00: CANONICAL VEDIC 7D SHOW INTRODUCTORY NARRATION
    (
        "E01_B00_Vedic_Intro", "host", 9.5,
        "In this show, we follow the Seven D Way, that characterizes the key virtues of Vedic philosophy that upholds Dharmic life and accelerates a soul's growth to the maximum possible way. In today's episode, we are going to start with Respect Your DUTY First!",
        "KARMIC GENIE SHOW • THE 7D WAY",
        "VEDIC PHILOSOPHY THAT UPHOLDS DHARMIC LIFE",
        [
            ("[CYAN]THE 7D WAY (VEDIC VIRTUES):", "Characterizes the 7 key virtues of Vedic philosophy that uphold Dharmic life."),
            ("[EMERALD]MAXIMUM SOUL ACCELERATION:", "Accelerates a soul's growth (Body -> Mind -> Soul -> Para-Soul) to the maximum possible way."),
            ("[GOLD]TODAY'S EPISODE (S01E01):", "We start with Dimension 1: \"Respect Your DUTY First.\""),
        ],
        "7 VIRTUES × 10 PTS = 70 MAX  •  < 35 / 70 = CHANGE COURSE",
    ),
    # ACT I: PAGE 1 OF TREATISE (Beats 01–06)
    (
        "E01_B01", "bala", 7.5,
        "Dimension One is Respect Your DUTY First! Never silence your heart's first whisper—when conscience says care for someone today, obey right away!",
        "ACT I • PRIMARY DEFINITION BY BALA-RISHI",
        "1. RESPECT YOUR DUTY FIRST.",
        [
            ("[GOLD]PRIMARY DEFINITION:", "Obeying the immediate whisper of Conscience (Manasatchi) at every stage of life."),
            ("[CYAN]CONSCIENCE ALARM:", "Duty is never your office job—Duty is the task that triggers guilt when left undone."),
            ("[EMERALD]CORE KARMIC LAW:", "Whisper of Heart -> Immediate Action -> 10 / 10 Peace of Mind."),
        ],
        "SPEAKER: 4-YEAR-OLD BALA-RISHI (@Me)",
    ),
    (
        "E01_H02", "host", 7.5,
        "Welcome to Episode One: Respect Your DUTY First. Every living being—banyan tree, honeybee, and flowing river—obeys a hundred-percent proportional stage duty!",
        "ACT I • COSMIC 100% ECOLOGICAL LAW",
        "100% PROPORTIONAL DUTY ACROSS NATURE",
        [
            ("[EMERALD]BANYAN TREE (100%):", "40% Roots/Sun + 30% Shade/O2 + 20% Fruit/Medicine + 10% Seeds = 100%."),
            ("[GOLD]HONEYBEE (100%):", "50% Hive Nectar + 35% Pollinating Flowers + 15% Guarding Brood = 100%."),
            ("[CYAN]FLOWING RIVER (100%):", "50% Mountain-to-Sea Flow + 35% Irrigating Fields + 15% Aquatic Life = 100%."),
        ],
        "SWADHARMA: EVERY LIVING BEING OBEYS ITS 100% RATIO",
    ),
    (
        "E01_H03", "host", 7.5,
        "Why is family life, Karma Margam, the safest and fastest path to grow your soul? Because unlike strict ascetic paths, home offers loving relaxations!",
        "ACT I • THREE SPIRITUAL PATHS (MARGAMS)",
        "WHY FAMILY LIFE (KARMA MARGAM) IS SAFEST & FASTEST",
        [
            ("[AMBER]SOLITARY JNANA & BHAKTI MARGAM:", "Razor-strict rules (0% margin for error—one ego slip derails the seeker)."),
            ("[EMERALD]FAMILY LIFE (KARMA MARGAM / ILLARAM):", "Built-in exceptions, rule relaxations & loving family shock-absorbers to forgive mistakes!"),
            ("[GOLD]PROGRESSIVE SYNTHESIS:", "Mix in Jnana (Buddhi) at Age 24 & Bhakti (Bakthi) at Age 54 right inside home!"),
        ],
        "THIRUKKURAL KURALS 46–48: ILLARAM IS SUPREME",
    ),
    (
        "E01_H04", "host", 7.5,
        "Across our fourfold temple, modern civilization confuses an office job with Respect Your DUTY First—making money ninety-five percent of life starves family and triggers conscience rejection!",
        "ACT I • FOURFOLD TEMPLE & WORKAHOLIC TRAP",
        "OFFICE JOB != YOUR ETERNAL LIFE DUTY",
        [
            ("[CYAN]FOURFOLD HUMAN TEMPLE:", "Body (0–12) -> Mind (12–36) -> Soul (36–60) -> Para-Soul (60–84+)."),
            ("[AMBER]95% PORUL DISTORTION:", "Letting money-earning bloat to 95% starves the 50% family covenant!"),
            ("[EMERALD]RESPECT YOUR DUTY FIRST:", "Maintaining stage-specific 100% proportional equilibrium."),
        ],
        "95% WORK / 5% HOME = SEVERE CONSCIENCE REJECTION",
    ),
    (
        "E01_H05", "host", 7.5,
        "Even a thief feels burning guilt the first three nights he steals. Drown that conscience alarm in alcohol or screens, and human empathy dies!",
        "ACT I • THE FATAL TRAP OF NUMBING CONSCIENCE",
        "HOW ALCOHOL & SCREENS KILL EMPATHY",
        [
            ("[GOLD]NIGHTS 1–3 OF BETRAYAL:", "Every human feels sharp Conscience Rejection and sleepless guilt at first."),
            ("[AMBER]FALSE ANESTHETICS:", "Alcohol, intoxicants, midnight scrolling, and workaholism mute the inner alarm."),
            ("[CYAN]TERMINAL OUTCOME:", "Silenced Conscience = 0% Human Empathy across society."),
        ],
        "NEVER DROWN THE WHISPER OF MANASATCHI",
    ),
    (
        "E01_H06", "host", 7.5,
        "Obey the exact rule, Respect Your DUTY First, and conscience rejection vanishes—flooding your nervous system with immediate relief and deep peace of mind!",
        "ACT I • THE ONE INVARIANT COSMIC LAW",
        "CONSCIENCE REJECTION vs. PEACE OF MIND",
        [
            ("[AMBER]VIOLATING STAGE DUTY:", "Triggers immediate Conscience Rejection, midnight restlessness & shame."),
            ("[EMERALD]FULFILLING STAGE DUTY:", "Unlocks instant nervous-system relief and unshakable Peace of Mind (Shanti)."),
            ("[GOLD]TONIGHT'S COMPASS:", "Your pillow at 10:00 PM is the incorruptible judge of your day."),
        ],
        "FULFILLMENT = 10 / 10 DEEP PEACE OF MIND",
    ),
    # ACT II: PAGE 2 OF TREATISE (Beats 07–14)
    (
        "E01_B07", "bala", 7.5,
        "Respect Your DUTY First begins at age four! My hundred-percent duty at four is simply to play outdoors, or my physical body cannot grow!",
        "ACT II • MILESTONE 1 ANCHOR (AGE 4)",
        "AGE 4: 100% PLAY -> PHYSICAL BODY GROWTH",
        [
            ("[GOLD]MAXIM IN ACTION:", "1. Respect Your DUTY First."),
            ("[EMERALD]AGE 4 PROPORTIONAL LAW:", "100% Free Outdoor Play + 0% Formal Study = Physical Body Growth!"),
            ("[AMBER]BIOLOGICAL FAILURE MODE:", "Without play at Age 4, the physical body cannot grow!"),
        ],
        "BALA-RISHI ANCHOR #1: PLAY AT AGE 4",
    ),
    (
        "E01_H08", "host", 7.5,
        "In Macro-Cycle One, ages zero to four, barefoot play wires the cerebellum and immunity. Handing tablets to toddlers triggers instant parental conscience rejection!",
        "ACT II • MACRO-CYCLE 1 (AGES 0–12: BODY)",
        "SUB-CYCLE 1.1 (AGES 0–4): 100% BAREFOOT PLAY",
        [
            ("[CYAN]BIOLOGICAL METRICS:", "100% unscripted play drives cerebellum wiring, lung capacity & bone density."),
            ("[AMBER]SCORE 1–3 VIOLATION:", "Glowing mealtime screens & academic pressure at age 4 stunt growth."),
            ("[EMERALD]SCORE 8–10 FULFILLMENT:", "Sunlight, laughter, mud play & 11-hour deep restorative sleep."),
        ],
        "CYCLE 1.1 (0–4 YRS): 100% PLAY = STRONG BODY",
    ),
    (
        "E01_H09", "host", 7.5,
        "From ages five to eight, a child's hundred-percent duty shifts to seventy percent motor play, twenty percent moral stories, and ten percent family truth.",
        "ACT II • MACRO-CYCLE 1 (AGES 0–12: BODY)",
        "SUB-CYCLE 1.2 (AGES 4–8): 70 / 20 / 10 RATIO",
        [
            ("[EMERALD]70% MOTOR PLAY:", "Tree climbing, running, balance, and group playground joy."),
            ("[GOLD]20% STORIES & RHYTHM:", "Hearthside moral storytelling, music, and joyful curiosity."),
            ("[CYAN]10% FAMILY TRUTH & POOJA:", "Watching Mother's daily Pooja lamp & speaking simple truth = 100%."),
        ],
        "CYCLE 1.2 (4–8 YRS): 70% PLAY + 20% STORY + 10% KINSHIP",
    ),
    (
        "E01_H10", "host", 7.5,
        "In school years, ages eight to sixteen, a child's duty is fifty percent focused studying and fifty percent outdoor play and family kinship!",
        "ACT II • SCHOOL-AGE PROPORTIONAL LAW",
        "AGES 8–16: 50% STUDYING + 50% PLAY = 100%",
        [
            ("[GOLD]50% STUDYING (KALVI):", "Focused classroom learning, reading, mathematics & curiosity."),
            ("[EMERALD]35% OUTDOOR PLAY & SPORTS:", "Team athletics, running, endurance & physical vitality."),
            ("[CYAN]15% FAMILY KINSHIP:", "Helping parents, sibling warmth & household tasks (50% + 50% = 100%)."),
        ],
        "VIOLATION: 95% CRAMMING / 5% PLAY = CONSCIENCE REJECTION",
    ),
    (
        "E01_H11", "host", 7.5,
        "Macro-Cycle Two spans ages twelve to twenty-four. From twelve to sixteen, guard that fifty-fifty study-and-play balance while channeling adolescent fire into honoring teachers.",
        "ACT II • MACRO-CYCLE 2 (AGES 12–24: SKILL)",
        "SUB-CYCLE 2.1 (AGES 12–16): ADOLESCENT FIRE",
        [
            ("[CYAN]50% / 50% GUARDRAIL:", "Maintain 50% deep study + 35% sport + 15% honoring parents & teachers."),
            ("[AMBER]CONSCIENCE REJECTION:", "Slamming doors, mocking elders, or secret midnight screen vices."),
            ("[EMERALD]PEACE OF MIND:", "Disciplined athletics and respectful speech at the family table."),
        ],
        "CYCLE 2.1 (12–16 YRS): RESPECT TEACHERS & PARENTS",
    ),
    (
        "E01_H12", "host", 7.5,
        "From sixteen to twenty-four, youth duty shifts to sixty-five percent deep skill mastery, twenty percent physical sport, and fifteen percent filial service to parents!",
        "ACT II • MACRO-CYCLE 2 (AGES 12–24: SKILL)",
        "AGES 16–24: 65% SKILL + 20% SPORT + 15% FILIAL",
        [
            ("[GOLD]65% CRAFT & VIDYA:", "3-hour deep apprenticeship blocks building real vocational mastery."),
            ("[EMERALD]20% PHYSICAL DISCIPLINE:", "Daily strength, stamina, and zero chemical intoxicants."),
            ("[CYAN]15% FILIAL SERVICE:", "Standing beside parents and preparing for adult independence = 100%."),
        ],
        "CYCLE 2.2 (16–20 YRS): FORGING THE VOCATIONAL INSTRUMENT",
    ),
    (
        "E01_H13", "host", 7.5,
        "From twenty to twenty-four, earn your first honest bread, offer its first fruits to mother and father, and prepare for mental awakening.",
        "ACT II • MACRO-CYCLE 2 (AGES 12–24: SKILL)",
        "SUB-CYCLE 2.3 (AGES 20–24): FIRST HONEST SWEAT",
        [
            ("[EMERALD]FIRST PAYCHECK OFFERING:", "Placing the first fruits of honest labor into Mother and Father's hands."),
            ("[GOLD]SELF-RELIANCE:", "Showing up 10 minutes early, 0% vanity debt, 100% dependable craft."),
            ("[CYAN]THRESHOLD OF 24:", "Vessel forged—ready to awaken Independent Thinking (Jnana Buddhi)!"),
        ],
        "CYCLE 2.3 (20–24 YRS): HONORING PARENTS WITH FIRST FRUITS",
    ),
    (
        "E01_H14", "host", 7.5,
        "Look at the curved-glass matrix: from hundred-percent play at four to fifty-fifty in school and sixty-five percent skill in youth, nature builds strength!",
        "ACT II • CYCLES 1 & 2 MASTER SUMMARY",
        "HOW PROPORTIONAL DUTY EVOLVES (AGES 0–24)",
        [
            ("[GOLD]AGE 4 (SUB-CYCLE 0–4):", "100% Outdoor Play + 0% Study -> Physical Body Grows."),
            ("[CYAN]AGES 8–16 (SCHOOL):", "50% Studying (Kalvi) + 50% Play & Family Kinship = 100%."),
            ("[EMERALD]AGES 16–24 (YOUTH):", "65% Deep Skill + 20% Sport + 15% Filial Care = 100%."),
        ],
        "PROTECTED INSIDE SAFE FAMILY KARMA MARGAM",
    ),
    # ACT III: PAGE 3 OF TREATISE (Beats 15–22)
    (
        "E01_B15", "bala", 7.5,
        "At age twenty-four, Respect Your DUTY First means start thinking independently for yourself—otherwise your adult mind stops growing and stays asleep!",
        "ACT III • MILESTONE 2 ANCHOR (AGE 24)",
        "AGE 24: INDEPENDENT THINKING -> MIND GROWTH",
        [
            ("[GOLD]MAXIM IN ACTION:", "1. Respect Your DUTY First."),
            ("[CYAN]AGE 24 COSMIC LAW:", "Start Thinking Independently (Buddhi) -> Mental Growth!"),
            ("[AMBER]FAILURE MODE:", "Blind herd conformity at 24 -> Mind stays permanently asleep."),
        ],
        "BALA-RISHI ANCHOR #2: THINK AT AGE 24",
    ),
    (
        "E01_H16", "host", 7.5,
        "In Macro-Cycle Three, at twenty-four, you blend Jnana Margam—independent Buddhi thinking—safely inside family life, separating truth from herd propaganda without solitary ascetic risk!",
        "ACT III • MACRO-CYCLE 3 (AGES 24–36: MIND)",
        "BLENDING JNANA MARGAM (BUDDHI) INTO FAMILY LIFE",
        [
            ("[EMERALD]THE SAFE BLEND AT 24:", "Mix Jnana Margam (Buddhi / Discernment) directly into Family Karma Margam!"),
            ("[GOLD]WHY SAFER THAN A CAVE:", "You gain razor-sharp intellect while cushioned by warm family love."),
            ("[AMBER]VIOLATION:", "Quarter-life herd conformity drowned in Friday-night alcohol."),
        ],
        "AGE 24+: KARMA MARGAM + JNANA MARGAM (BUDDHI)",
    ),
    (
        "E01_H17", "host", 7.5,
        "Between twenty twenty-five and twenty twenty-six, over two hundred thousand workforce shifts, sixty thousand voluntary buyouts, and seven hundred twenty billion in automation occurred.",
        "ACT III • REAL-WORLD 2025 -> 2026 METRICS",
        "WHY AN OFFICE BADGE IS NEVER YOUR LIFE DUTY",
        [
            ("[AMBER]GLOBAL WORKFORCE SHIFTS:", "154,000+ (2025) -> 200,000+ (2026) displaced corporate roles."),
            ("[CYAN]VOLUNTARY BUYOUTS:", "60,000+ mid-career transitions & role resets."),
            ("[GOLD]AI INFRASTRUCTURE SPEND:", "$720 Billion deployed—proving jobs are highways, never your home!"),
        ],
        "2025–2026 METRICS: GUARD YOUR PERMANENT FAMILY COVENANT",
    ),
    (
        "E01_H18", "host", 7.5,
        "For a householder man, duty is fifty percent earning righteous Porul, fifteen percent husband, fifteen percent father, ten percent son, and ten percent citizen!",
        "ACT III • ADULT MALE 100% PROPORTIONAL MATRIX",
        "MALE HOUSEHOLDER COVENANT (PORUL ANCHOR = 100%)",
        [
            ("[GOLD]50% EARNING PORUL (SVADHARMA WEALTH):", "Righteous material wealth & clean economic security (Kural 754)."),
            ("[EMERALD]30% IMMEDIATE HEARTH:", "15% Good Husband (cherishing wife) + 15% Good Father (guiding kids)."),
            ("[CYAN]20% LINEAGE & SOCIETY:", "10% Good Son (aging parents) + 10% Brother/Relative/Citizen = 100%!"),
        ],
        "WARNING: 95% PORUL STARVES 50% FAMILY & TRIGGERS GUILT!",
    ),
    (
        "E01_H19", "host", 7.5,
        "For a householder woman, duty is fifty percent earning sacred Arul—giving birth, raising children, and daily Pooja—plus wife, nurturer, daughter, and hospitality!",
        "ACT III • ADULT FEMALE 100% PROPORTIONAL MATRIX",
        "FEMALE HOUSEHOLDER COVENANT (ARUL ANCHOR = 100%)",
        [
            ("[GOLD]50% EARNING ARUL (DIVINE GRACE - KURAL 241):", "Giving birth, raising kids with pure values & performing Daily Pooja!"),
            ("[EMERALD]35% HEARTH & NURTURING:", "20% Wise Devoted Wife (Illal) + 15% Child Health & Food Sanctity."),
            ("[CYAN]15% KINSHIP & GRACE:", "10% Loving Daughter/In-Law + 5% Hospitality (Virundhombal) = 100%!"),
        ],
        "PORUL (50%) + ARUL (50% DAILY POOJA) = 10/10 HOME",
    ),
    (
        "E01_H20", "host", 7.5,
        "Macro-Cycle Four, ages thirty-six to forty-eight, is two-generation stewardship. Harmonize Porul and Arul while standing as a double shield for children and aging parents.",
        "ACT III • MACRO-CYCLE 4 (AGES 36–48: STEWARDSHIP)",
        "SUB-CYCLE 4.1 (AGES 36–40): THE DOUBLE SHIELD",
        [
            ("[EMERALD]DOWNWARD SHIELD:", "Protecting school-age children's 50% Study / 50% Play balance."),
            ("[GOLD]UPWARD SHIELD:", "Caring for aging Cycle-6 parents with unhurried daily warmth."),
            ("[CYAN]CIVIC SHIELD:", "Mentoring junior colleagues without stealing their credit."),
        ],
        "CYCLE 4.1 (36–40 YRS): TWO-GENERATION PILLAR",
    ),
    (
        "E01_H21", "host", 7.5,
        "From forty to forty-four comes the midlife conscience crucible. So-called midlife crisis is simply twenty years of accumulated conscience rejection demanding course correction!",
        "ACT III • MACRO-CYCLE 4 (AGES 36–48)",
        "SUB-CYCLE 4.2 (AGES 40–44): MIDLIFE CRUCIBLE",
        [
            ("[AMBER]DIAGNOSTIC TRUTH:", "Midlife crisis = 20 years of neglected family duties erupting at age 42."),
            ("[EMERALD]KARMA MARGAM SAFETY NET:", "Because family life allows rule relaxations, you can apologize & reset tonight!"),
            ("[GOLD]35 / 70 RULE:", "If your score is below 35 / 70, rebalance Porul and family presence now."),
        ],
        "CYCLE 4.2 (40–44 YRS): COURSE-CORRECT INSIDE FAMILY LIFE",
    ),
    (
        "E01_H22", "host", 7.5,
        "From forty-four to forty-eight, transition from commander to counselor for teenage children, honor frail seventy-year-old parents, and loosen ego grip for soul awakening.",
        "ACT III • MACRO-CYCLE 4 (AGES 36–48)",
        "SUB-CYCLE 4.3 (AGES 44–48): COMMANDER -> COUNSELOR",
        [
            ("[CYAN]GUIDING TEENS:", "Transitioning from strict command to wise dialogic counsel."),
            ("[GOLD]TENDER ELDER CARE:", "Honoring frail 70+ parents with daily reverence (Xiao)."),
            ("[EMERALD]SOUL PREPARATION:", "Loosening attachment to Porul ahead of the Age 54 Soul Turning Point."),
        ],
        "CYCLE 4.3 (44–48 YRS): BRIDGE FROM MIND TO SOUL",
    ),
    # ACT IV: PAGE 4 OF TREATISE (Beats 23–28)
    (
        "E01_B23", "bala", 7.5,
        "At age fifty-four, Respect Your DUTY First means start thanking everyone with pure gratitude—otherwise your living soul cannot grow and blossom!",
        "ACT IV • MILESTONE 3 ANCHOR (AGE 54)",
        "AGE 54: THANKING -> SOUL GROWTH",
        [
            ("[GOLD]MAXIM IN ACTION:", "1. Respect Your DUTY First."),
            ("[EMERALD]THREEFOLD LIFECYCLE LAW:", "Age 4 PLAY (Body) -> Age 24 THINK (Mind) -> Age 54 THANK (Soul)!"),
            ("[AMBER]FAILURE MODE:", "Clinging to ego & Porul hoarding at 54 -> Soul cannot grow!"),
        ],
        "BALA-RISHI ANCHOR #3: THANK AT AGE 54",
    ),
    (
        "E01_H24", "host", 7.5,
        "In Macro-Cycle Five, from ages forty-eight to fifty-two, release ego micromanagement, empower twenty-four-year-old children to think independently, and serve elderly parents with tenderness.",
        "ACT IV • MACRO-CYCLE 5 (AGES 48–60: SOUL)",
        "SUB-CYCLE 5.1 (AGES 48–52): RELEASING EGO CONTROL",
        [
            ("[CYAN]EMPOWERING ADULT CHILDREN:", "Stepping back so your 24-year-old children awaken their own Buddhi."),
            ("[GOLD]ELDER DEVOTION:", "Serving 75–80yo parents so zero unspoken regret remains."),
            ("[EMERALD]INNER SHIFT:", "Turning outward ambition into inward gratitude."),
        ],
        "CYCLE 5.1 (48–52 YRS): PREPARING THE SOUL FOR AGE 54",
    ),
    (
        "E01_H25", "host", 7.5,
        "At fifty-four, blend Bhakti Margam safely inside family life: fifty percent thanking the Divine and world, twenty-five percent mentoring, fifteen percent counsel, and ten percent simplicity!",
        "ACT IV • AGE 54 PROPORTIONAL SHIFT (100%)",
        "BLENDING BHAKTI MARGAM INTO FAMILY LIFE AT 54",
        [
            ("[GOLD]50% THANKING (NANDRI & ARUL):", "Shifting from Porul accumulation to 50%+ Bhakti thanksgiving & prayer!"),
            ("[EMERALD]25% MENTORING NEXT GEN:", "Pouring decades of craft wisdom into younger builders without ego."),
            ("[CYAN]15% FAMILY COUNSEL + 10% SIMPLICITY:", "Crowning Karma Margam + Jnana Margam with Bhakti Margam = 100%!"),
        ],
        "AGE 54+: KARMA + JNANA + BHAKTI MARGAM UNITED AT HOME",
    ),
    (
        "E01_H26", "host", 7.5,
        "From fifty-six to sixty, pass the executive torch gracefully to younger builders, forgive every fifty-year grievance, and clear your conscience ledger completely.",
        "ACT IV • MACRO-CYCLE 5 (AGES 48–60: SOUL)",
        "SUB-CYCLE 5.3 (AGES 56–60): PASSING THE TORCH",
        [
            ("[EMERALD]GRACEFUL SUCCESSION:", "Handing over leadership batons without bitterness or insecurity."),
            ("[GOLD]TOTAL FORGIVENESS:", "Releasing every old grievance across family and career."),
            ("[CYAN]CRYSTAL-CLEAR LEDGER:", "Entering age 60 with zero unpaid moral debts."),
        ],
        "CYCLE 5.3 (56–60 YRS): UNBURDENED SOUL LEDGER",
    ),
    (
        "E01_H27", "host", 7.5,
        "In Macro-Cycle Six, past age sixty, Para-Soul duty is seventy percent radiating Arul and blessing, twenty percent protecting grandchildren's play, and ten percent detachment!",
        "ACT IV • MACRO-CYCLE 6 (AGES 60–72: PARA-SOUL)",
        "PARA-SOUL 100% PROPORTIONAL DUTY (AGES 60+)",
        [
            ("[GOLD]70% RADIATING ARUL & BLESSING:", "Living as a sanctuary of prayer, grace, and impartiality."),
            ("[EMERALD]20% PROTECTING 4YO GRANDCHILD'S PLAY:", "Guarding the next generation's 100% outdoor play!"),
            ("[CYAN]10% PEACEFUL DETACHMENT:", "Zero interference in adult children's household management = 100%."),
        ],
        "CYCLE 6 (60–72 YRS): 70% ARUL + 20% GRANDKIDS + 10% PEACE",
    ),
    (
        "E01_H28", "host", 7.5,
        "From sixty-eight past eighty-four, in Macro-Cycle Seven, the Para-Soul shines like a harvest moon on still water—radiating fearless blessing to all.",
        "ACT IV • MACRO-CYCLE 7 (AGES 68–84+: PARA-SOUL)",
        "THE LIVING BANYAN CANOPY OF THE PARA-SOUL",
        [
            ("[EMERALD]HARVEST MOON RADIANCE:", "Body, Mind, and Soul merge into luminous Para-Soul peace."),
            ("[GOLD]ZERO DEATH FEAR:", "A life of fulfilled stage duties leaves zero conscience rejection."),
            ("[CYAN]ETERNAL FRAGRANCE:", "Blessing three generations beneath one grateful roof."),
        ],
        "CYCLE 7 (72–84+ YRS): 10 / 10 SOVEREIGN PEACE",
    ),
    # ACT V: PAGE 5 OF TREATISE — THE THREE WISE EASTERN PHILOSOPHERS' TAKE (Beats 29–33)
    (
        "E01_H29", "host", 7.5,
        "Hear the first wise philosopher on Respect Your DUTY First: Kural forty-six crowns family life supreme, and two ninety-three warns a betrayed conscience burns within!",
        "ACT V • EASTERN PHILOSOPHER #1: THIRUVALLUVAR",
        "SAINT THIRUVALLUVAR (THIRUKKURAL KURALS 46 & 293)",
        [
            ("[GOLD]THIRUKKURAL KURAL 46–48 (ILLARAM):", "\"Righteous family life (Karma Margam) is foremost—what need to seek outside ascetic paths?\""),
            ("[CYAN]KURAL 754 (PORUL) & KURAL 241 (ARUL):", "Father's righteous Porul + Mother's sacred Arul form the complete home."),
            ("[AMBER]KURAL 293 (MANASATCHI):", "\"Even if hidden from the world, a betrayed conscience burns within.\""),
        ],
        "PHILOSOPHER 1: SAINT THIRUVALLUVAR ON DUTY & ILLARAM",
    ),
    (
        "E01_H30", "host", 7.5,
        "Hear the second wise Eastern philosopher: the Six Sacred Directions honor parents, teachers, family, friends, workers, and sages, while heedlessness callouses the mind.",
        "ACT V • EASTERN PHILOSOPHER #2: GAUTAMA BUDDHA",
        "SIGALOVADA SUTTA (DN 31) & DHAMMAPADA 117–119",
        [
            ("[EMERALD]SIX SACRED DIRECTIONS (SIGALOVADA):", "East (Parents), South (Teachers), West (Spouse/Kids), North (Friends), Nadir (Workers), Zenith (Sages)."),
            ("[GOLD]MIDDLE WAY (MAJJHIMA PATIPADA):", "Avoiding brittle ascetic extremes through balanced household Dharma."),
            ("[AMBER]DHAMMAPADA 117 & 119:", "Repeating neglected duty & intoxicants callouses the mind (Chitta)."),
        ],
        "PHILOSOPHER 2: GAUTAMA BUDDHA ON THE 6 DIRECTIONS",
    ),
    (
        "E01_H31", "host", 7.5,
        "Hear the third wise Eastern philosophy: feeding parents without warm presence of heart is no filial duty, and thousand-mile journeys begin today.",
        "ACT V • EASTERN PHILOSOPHER #3: CONFUCIUS & LAOZI",
        "ANALECTS (1.2, 2.4, 2.7) & TAO TE CHING (CH. 64)",
        [
            ("[GOLD]CONFUCIUS (ANALECTS 2.7 - XIAO):", "Money transfers without warm facial affection and presence are NOT filial duty!"),
            ("[CYAN]ANALECTS 2.4 (LIFECYCLE SPIRAL):", "15 Learning -> 30 Standing Firm -> 50 Heaven's Mandate -> 70 Heart's Peace."),
            ("[EMERALD]LAOZI (TAO TE CHING CH. 64):", "A 1,000-mile journey begins beneath your feet tonight."),
        ],
        "PHILOSOPHER 3: CONFUCIUS & LAOZI ON FILIAL ROOT",
    ),
    (
        "E01_H32", "host", 7.5,
        "Behold two Karmic Genie analogies: hoarding titles while neglecting family creates a barren forest without fruit, and career highways are never life's destination!",
        "ACT V • CANONICAL KARMIC GENIE ANALOGIES 1 & 2",
        "BARREN FOREST vs. BANYAN  •  HIGHWAY vs. HOME",
        [
            ("[AMBER]ANALOGY 1 (BARREN FOREST):", "Chasing promotions (24–54) while neglecting Play/Think/Thank yields zero sweet fruit."),
            ("[EMERALD]ANALOGY 2 (HIGHWAY vs. HOME):", "Industries and job titles are highways to carry supplies home—never your destination!"),
            ("[GOLD]DESTINATION:", "Unbroken Peace of Conscience at the family hearth."),
        ],
        "NEVER PARK YOUR SOUL ON A CORPORATE HIGHWAY",
    ),
    (
        "E01_H33", "host", 7.5,
        "Third is the connectedness paradox: global fiber networks span continents in milliseconds, yet a parent ignores a four-year-old child or seventy-year-old mother nearby!",
        "ACT V • CANONICAL KARMIC GENIE ANALOGY 3",
        "THE IT CONNECTEDNESS PARADOX",
        [
            ("[CYAN]GLOBAL BANDWIDTH:", "10 Gbps fiber connecting continents in milliseconds."),
            ("[AMBER]LOCAL HEART BANDWIDTH:", "0 bps three feet away from your 4yo child or 72yo mother at dinner!"),
            ("[EMERALD]KARMIC CORRECTION:", "Put down the glowing screen tonight and restore local human warmth."),
        ],
        "TRUE CONNECTEDNESS BEGINS AT YOUR DINNER TABLE",
    ),
    # ACT VI: PAGE 6 OF TREATISE — LIVE 1–10 (70-POINT) SCORECARD (Beats 34–36)
    (
        "E01_H34", "host", 7.5,
        "Score yourself from one to ten on Respect Your DUTY First! Across all seven dimensions, any total below thirty-five out of seventy demands course correction.",
        "ACT VI • LIVE 1–10 (70-POINT) CONSCIENCE SCORECARD",
        "THE 35 / 70 COURSE-CORRECTION COMPASS",
        [
            ("[GOLD]DIMENSION 1 WEIGHT:", "Respect Your DUTY First = 1 to 10 Points (out of 70 Max)."),
            ("[AMBER]BELOW 35 / 70 (RED ZONE):", "Chronic Conscience Rejection -> Change the course of your life today!"),
            ("[EMERALD]50–70 / 70 (GOLD ZONE):", "Harmonized Body, Mind, Soul & Para-Soul -> Pioneer of the New World."),
        ],
        "SCORE YOUR LIFE HONESTLY FROM 1 TO 10 TONIGHT",
    ),
    (
        "E01_H35", "host", 7.5,
        "Score one to three means ninety-five percent study crushing play, or ninety-five percent money starving family—score eight to ten restores hundred-percent proportional peace!",
        "ACT VI • PROPORTIONAL SCORECARD DIAGNOSTIC",
        "SCORE 1–3 (REJECTION) vs. SCORE 8–10 (PEACE)",
        [
            ("[AMBER]SCORE 1–3 (CONSCIENCE REJECTION):", "iPad toddler (Age 4), 95% cramming (School), 95% Porul starving family (Adult), 0% thanking (54)."),
            ("[CYAN]SCORE 4–6 (DRIFTING):", "Mechanical bank transfers without unhurried eye contact or daily Pooja grace."),
            ("[EMERALD]SCORE 8–10 (PEACE OF MIND):", "100% Play (4), 50/50 Study-Play (8–16), 50/15/15/10/10 Porul + 100% Arul, 50% Thanking (54)."),
        ],
        "PROPORTIONAL HARMONY = 10 / 10 PEACE OF MIND",
    ),
    (
        "E01_H36", "host", 7.5,
        "Take the five-question audit tonight, two points each: stage alignment, unhurried family presence, zero alcohol numbing, duty over politics, and peaceful pillow rest!",
        "ACT VI • THE 5-QUESTION TONIGHT SELF-AUDIT",
        "SCORE 2 POINTS FOR EACH 'YES' (MAX 10 / 10)",
        [
            ("[GOLD]Q1 & Q2 (4 PTS):", "1) Aligned with my 12-year/4-year cycle?  2) Unhurried time with parents, spouse & kids today?"),
            ("[CYAN]Q3 & Q4 (4 PTS):", "3) Zero alcohol/screen numbing of conscience?  4) Kept 50% Porul / 50% Family & Arul balance?"),
            ("[EMERALD]Q5 PILLOW TEST (2 PTS):", "5) Does my head touch the pillow tonight in immediate relief & peace of mind?"),
        ],
        "TOTAL D1 SCORE: ___ / 10 PTS",
    ),
    # ACT VII: PAGE 7 OF TREATISE — GENIE BLESSING & CLOSING CALL (Beats 37–40)
    (
        "E01_H37", "host", 7.5,
        "We have walked all seven cycles of human conscience. Now let us ask the timeless question: what does Genie say—the Seven D way?",
        "ACT VII • SUMMONING THE KARMIC GENIE",
        "WHAT DOES GENIE SAY — THE 7D WAY?",
        [
            ("[GOLD]SEVEN CYCLES COMPLETE:", "From Age 4 Play (Body) -> Age 24 Think (Mind) -> Age 54 Thank (Soul) -> Para-Soul."),
            ("[CYAN]THE SACRED LAMP AWAKENS:", "Golden sapphire light rises from the jeweled lamp on the pure-white stage."),
            ("[EMERALD]WALL INSCRIPTION:", "1. RESPECT YOUR DUTY FIRST."),
        ],
        "AWAKENING THE KARMIC GENIE BLESSING",
    ),
    (
        "E01_G38", "genie", 7.5,
        "Play freely at four, think independently at twenty-four, thank deeply at fifty-four—obey your conscience tonight, and receive unbroken peace of mind!",
        "ACT VII • THE KARMIC GENIE'S 1-PHRASE BLESSING",
        "PLAY AT 4  •  THINK AT 24  •  THANK AT 54",
        [
            ("[GOLD]AGE 4 (BODY):", "Play 100% freely outdoors so the physical temple grows strong."),
            ("[CYAN]AGE 24 (MIND):", "Blend Jnana Buddhi inside safe Family Karma Margam (Porul + Arul)."),
            ("[EMERALD]AGE 54 (SOUL):", "Crown Family Life with Bhakti Thanksgiving -> Unbroken Peace of Mind!"),
        ],
        "SPEAKER: AWAKENED MAHARISHI KARMIC GENIE (@Me)",
    ),
    (
        "E01_B39", "bala", 7.5,
        "Make that phone call to your parents, play with your children tonight, and always remember our first golden rule: Respect Your DUTY First!",
        "ACT VII • BALA-RISHI CLOSING ANCHOR",
        "TONIGHT'S IMMEDIATE ACTION (0% DELAY)",
        [
            ("[EMERALD]ACTION 1 (PARENTS):", "Call your mother and father tonight with a warm, unhurried voice."),
            ("[GOLD]ACTION 2 (CHILDREN & SPOUSE):", "Put away the phone, kneel on the floor, and play with your child."),
            ("[CYAN]FIRST GOLDEN RULE:", "1. Respect Your DUTY First!"),
        ],
        "SPEAKER: 4-YEAR-OLD BALA-RISHI (@Me)",
    ),
    (
        "E01_H40", "host", 7.5,
        "Respect Your DUTY First, my friends, and sleep in royal peace tonight! Join us next in Episode Two: Earn with DIGNITY Always!",
        "ACT VII • EPISODE 1 FINALE & EPISODE 2 TEASE",
        "LOCKED IN GOLD: 1. RESPECT YOUR DUTY FIRST.",
        [
            ("[EMERALD]EPISODE 1 MASTERED:", "\"Respect Your DUTY First.\" — Score 10 / 10 Peace of Mind!"),
            ("[GOLD]NEXT EPISODE (S01E02):", "\"Earn with DIGNITY Always.\" — Unbought Self-Respect & Right Livelihood."),
            ("[CYAN]WALK THE 7D WAY:", "Pioneers of the New World!"),
        ],
        "NEXT: S01E02 — \"EARN WITH DIGNITY ALWAYS.\"",
    ),
]


def collect_verified_me_clips() -> dict[str, list[Path]]:
    """Collects verified Flow clips of Adult @Me, 4yo Bala-Rishi @Me, and Awakened Maharishi Genie @Me."""
    cm = json.loads(CLIP_MAP_JSON.read_text(encoding="utf-8"))["clips"]
    host_clips = [
        Path(cm["H01_Host_Pilot_35_Rule"]),
        Path(cm["H02_Host_D1_Duty_Definition"]),
        Path(cm["H03_Host_D1_Silenced_Conscience"]),
        Path(cm["H04_Host_D2_Dignity_Explain"]),
        Path(cm["H05_Host_D3_Discipline_Explain"]),
        Path(cm["H06_Host_D4_Dharma_Explain"]),
        Path(cm["H07_Host_D5_Devotion_Explain"]),
        Path(cm["H08_Host_D6_Divine_Explain"]),
        Path(cm["H09_Host_D7_Destiny_Explain"]),
        V3_CLIPS_ROOT / "v3_b1_welcome" / "v3_b1_welcome_03.mp4",
        V3_CLIPS_ROOT / "v3_7d_philosophy_me" / "v3_phil_01.mp4",
        V3_CLIPS_ROOT / "v3_7d_philosophy_me" / "v3_phil_02.mp4",
        V3_CLIPS_ROOT / "v3_7d_philosophy_me" / "v3_phil_03.mp4",
        V3_CLIPS_ROOT / "v3_grand_design" / "v3_gd_01.mp4",
        V3_CLIPS_ROOT / "v3_host_expansion_me" / "v3_me_exp_01.mp4",
        V3_CLIPS_ROOT / "v3_host_expansion_me" / "v3_me_exp_02.mp4",
        V3_CLIPS_ROOT / "v3_host_expansion_me" / "v3_me_exp_03.mp4",
    ]
    bala_clips = [
        Path(cm["G00_Bala_Opening_Sample2"]),
        Path(cm["G01_Bala_D1_Duty"]),
        Path(cm["G02_Bala_D2_Dignity"]),
        Path(cm["G03_Bala_D3_Discipline"]),
        Path(cm["G04_Bala_D4_Dharma"]),
        Path(cm["G05_Bala_D5_Devotion"]),
        Path(cm["G06_Bala_D6_Divine"]),
        Path(cm["G07_Bala_D7_Destiny_Blessing"]),
    ]
    genie_clips = [
        PREV_BRAIN / "scratch" / "flow_me_maharishi_samples" / "flow_me_sample_01.mp4",
        PREV_BRAIN / "scratch" / "flow_me_maharishi_samples" / "flow_me_sample_02.mp4",
    ]
    return {
        "host": [p for p in host_clips if p.exists()],
        "bala": [p for p in bala_clips if p.exists()],
        "genie": [p for p in genie_clips if p.exists()] or [p for p in bala_clips if p.exists()],
    }


def build_ass_subtitles(ass_path: Path, timings: list[dict]):
    """Builds single-line sequential BorderStyle=3 dark-shaded subtitles at bottom of frame."""
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HostWhite,DejaVu Sans,30,&H00FFFFFF,&H00FFFFFF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.2,0,3,10.0,0.0,2,48,48,26,1
Style: BalaGold,DejaVu Sans,31,&H00B8F2FF,&H00B8F2FF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.2,0,3,10.0,0.0,2,48,48,26,1
Style: GenieCyan,DejaVu Sans,31,&H00FFFFB8,&H00FFFFB8,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.2,0,3,10.0,0.0,2,48,48,26,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev_lines = []
    for item in timings:
        s0 = item["start"] + 0.10
        e0 = item["end"] - 0.10
        role = item["role"]
        style = "BalaGold" if role == "bala" else ("GenieCyan" if role == "genie" else "HostWhite")
        chunks = split_caption_chunks(item["text"], max_chars=62)
        tot_chars = max(1, sum(len(c) for c in chunks))
        cur_t = s0
        for idx, c in enumerate(chunks):
            dur_c = (e0 - s0) * (len(c) / tot_chars)
            nxt_t = e0 if idx == len(chunks) - 1 else (cur_t + dur_c)
            ev_lines.append(
                f"Dialogue: 0,{format_ass_time(cur_t)},{format_ass_time(max(cur_t+0.35, nxt_t-0.03))},{style},,0,0,0,,{c}"
            )
            cur_t = nxt_t

    ass_path.write_text(header + "\n".join(ev_lines) + "\n", encoding="utf-8")


def build_s01e01_360p(pools: dict[str, list[Path]]) -> Path:
    print("\n🎬 Building Full-Blown Episode 1 (S01E01): '1. Respect Your DUTY First.' (360p)...", flush=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RENDERS.mkdir(parents=True, exist_ok=True)

    # 1. Cold Open (5.0s) & Finale Logo Card (5.0s)
    co_mp4 = TEMP_DIR / "e01_cold_open.mp4"
    if not co_mp4.exists():
        f_co = 150
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(PILOT_STAGE_JPG),
            "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-vf", (
                "scale=2400:1350:force_original_aspect_ratio=increase,crop=2400:1350,"
                f"zoompan=z='1.10-0.06*(on/{f_co})':x='(iw-iw/zoom)*(0.35+0.30*(on/{f_co}))':y='(ih-ih/zoom)*0.35':d={f_co}:s=1920x1080:fps=30,"
                "setsar=1,format=yuv420p"
            ),
            "-t", "5.00", "-r", "30", "-video_track_timescale", "30000",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "veryfast", "-crf", "19",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(co_mp4)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    fin_mp4 = TEMP_DIR / "e01_finale_logo.mp4"
    if not fin_mp4.exists():
        f_fin = 150
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(LOGO_JPG),
            "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-vf", (
                "scale=860:860:force_original_aspect_ratio=decrease,"
                "pad=1920:1080:(ow-iw)/2:(oh-ih)/2-36:color=white,"
                f"zoompan=z='min(zoom+0.0004,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={f_fin}:s=1920x1080:fps=30,"
                "setsar=1,format=yuv420p"
            ),
            "-t", "5.00", "-r", "30", "-video_track_timescale", "30000",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "veryfast", "-crf", "19",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(fin_mp4)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    parts = [co_mp4]
    cursor = probe_duration(co_mp4)
    timings = []

    h_idx, b_idx, g_idx = 0, 0, 0
    for idx, (bid, role, dur_s, spoken_txt, h_tag, c_title, bullets, f_metric) in enumerate(S01E01_BEATS):
        if role == "bala":
            v_clip = pools["bala"][b_idx % len(pools["bala"])]
            b_idx += 1
        elif role == "genie":
            v_clip = pools["genie"][g_idx % len(pools["genie"])]
            g_idx += 1
        else:
            v_clip = pools["host"][h_idx % len(pools["host"])]
            h_idx += 1

        aud_wav, _, _, actual_a_dur = build_beat_audio(bid, spoken_txt, role, target_dur=dur_s)
        hud_png = render_side_by_side_hud_png(
            hud_id=bid,
            maxim_banner="KARMIC GENIE SHOW  •  1. Respect Your DUTY First.",
            header_tag=h_tag,
            card_title=c_title,
            bullets=bullets,
            footer_metric=f_metric,
        )
        seg_mp4 = render_side_by_side_beat_mp4(
            beat_id=bid,
            video_clip=v_clip,
            audio_wav=aud_wav,
            hud_png=hud_png,
            target_dur=actual_a_dur,
            cam_dir=1 if idx % 2 == 0 else -1,
        )
        seg_d = probe_duration(seg_mp4)
        timings.append({
            "bid": bid,
            "role": role,
            "text": spoken_txt,
            "start": cursor,
            "end": cursor + seg_d,
        })
        parts.append(seg_mp4)
        cursor += seg_d
        if (idx + 1) % 5 == 0 or idx == len(S01E01_BEATS) - 1:
            print(f"   • Rendered [{idx+1:02d}/{len(S01E01_BEATS)}] {bid} ({role}) -> cum={cursor:.1f}s", flush=True)

    fin_start = cursor
    parts.append(fin_mp4)

    concat_txt = TEMP_DIR / "e01_concat.txt"
    concat_txt.write_text("\n".join(f"file '{p}'" for p in parts) + "\n", encoding="utf-8")
    stitched_mp4 = TEMP_DIR / "e01_stitched_1080p.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy", str(stitched_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    tot_dur = probe_duration(stitched_mp4)
    ass_path = TEMP_DIR / "e01_subtitles.ass"
    build_ass_subtitles(ass_path, timings)

    vol_expr = f"if(lt(t,4.80), 0.52, if(gt(t,{fin_start-0.40:.2f}), 0.52, 0.036))"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(stitched_mp4),
        "-ss", "4.00", "-stream_loop", "-1", "-i", str(THEME_WAV),
        "-filter_complex", (
            f"[0:v]ass={ass_path},fade=t=in:st=0:d=0.50,fade=t=out:st={tot_dur-0.80:.2f}:d=0.75,"
            "scale=640:360:flags=bicubic[vout];"
            f"[1:a]atrim=0:{tot_dur:.3f},asetpts=PTS-STARTPTS,lowpass=f=9000,volume='{vol_expr}':eval=frame[bgm];"
            "[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0,volume=1.45[aout]"
        ),
        "-map", "[vout]", "-map", "[aout]",
        "-t", f"{tot_dur:.3f}",
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-crf", "20",
        "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(OUT_S01E01_360P)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    shutil.copy2(OUT_S01E01_360P, ART_S01E01_360P)
    print(f"🏆 S01E01 ('Respect Your DUTY First.') 360p READY: {OUT_S01E01_360P} ({tot_dur:.2f}s | {OUT_S01E01_360P.stat().st_size/1e6:.2f} MB)", flush=True)
    return OUT_S01E01_360P


# ======================================================================================
# PILOT S01E00 (`30s × 7 Virtues` + CANONICAL VEDIC 7D INTRO NARRATION) IN 360P
# ======================================================================================
PILOT_BEATS = [
    (
        "P00_Vedic_Intro", "host", 9.5,
        "In this show, we follow the Seven D Way, that characterizes the key virtues of Vedic philosophy that upholds Dharmic life and accelerates a soul's growth to the maximum possible way. In today's episode, we are going to start with all seven virtues—beginning with Respect Your DUTY First!",
        "KARMIC GENIE SHOW  •  PILOT: THE 7D WAY",
        "PROLOGUE • VEDIC PHILOSOPHY OF DHARMIC LIFE",
        "ACCELERATING SOUL GROWTH TO THE MAXIMUM WAY",
        [
            ("[GOLD]1. Respect Your DUTY First.", "2. Earn with DIGNITY Always.  •  3. Practice Life DISCIPLINE."),
            ("[CYAN]4. Uphold Karmic DHARMA.", "5. Raise Family with DEVOTION.  •  6. Be Grateful to Your DIVINE."),
            ("[EMERALD]7. Purposeful Life Is Your DESTINY.", "Score 1–10 across all 7 Virtues (Pass >= 35 / 70)!"),
        ],
        "SAFEST & FASTEST PATH: FAMILY KARMA MARGAM",
    ),
    # D1: Respect Your DUTY First. (2 beats = 15s)
    (
        "P_D1_Bala", "bala", 7.5,
        "Dimension One is Respect Your DUTY First! Never drink away the whisper of your conscience—when your heart says care for someone today, listen right away!",
        "KARMIC GENIE SHOW  •  1. Respect Your DUTY First.",
        "DIMENSION 1 • PRIMARY DEFINITION BY BALA-RISHI",
        "1. RESPECT YOUR DUTY FIRST.",
        [
            ("[GOLD]CONSCIENCE TRIGGER:", "Duty is never your office job—it is the task that triggers guilt when left undone."),
            ("[EMERALD]STAGE LIFECYCLE LAW:", "Age 4 Play (100%) -> Age 8–16 Study/Play (50/50) -> Age 24 Think -> Age 54 Thank."),
            ("[CYAN]THIRUKKURAL KURAL 293:", "Even if hidden from the world, a betrayed conscience burns within."),
        ],
        "FULFILLMENT = IMMEDIATE PEACE OF MIND",
    ),
    (
        "P_D1_Host", "host", 7.5,
        "For a man, duty is fifty percent Porul and fifty percent family; for a woman, sacred Arul and daily Pooja—inside safe family Karma Margam!",
        "KARMIC GENIE SHOW  •  1. Respect Your DUTY First.",
        "DIMENSION 1 • 100% PORUL & ARUL MATRIX",
        "MALE PORUL (100%) & FEMALE ARUL (100%)",
        [
            ("[GOLD]MALE (100% PORUL MATRIX):", "50% Earning Porul + 15% Husband + 15% Father + 10% Son + 10% Citizen = 100%."),
            ("[EMERALD]FEMALE (100% ARUL MATRIX):", "50% Birth, Raising Kids & Daily Pooja + 20% Wife + 15% Health + 15% Kin = 100%."),
            ("[CYAN]NATURE'S 100% COVENANT:", "Banyan Tree (40/30/20/10), Honeybee (50/35/15) & River (50/35/15)."),
        ],
        "KARMA MARGAM ALLOWS SAFE RULE RELAXATIONS",
    ),
    # D2: Earn with DIGNITY Always. (2 beats = 15s)
    (
        "P_D2_Bala", "bala", 7.5,
        "Dimension Two is Earn with DIGNITY Always! Stand tall with an honest heart—no paycheck or title is ever worth trading away your self-respect!",
        "KARMIC GENIE SHOW  •  2. Earn with DIGNITY Always.",
        "DIMENSION 2 • PRIMARY DEFINITION BY BALA-RISHI",
        "2. EARN WITH DIGNITY ALWAYS.",
        [
            ("[GOLD]UNBOUGHT SELF-RESPECT (MAANAM):", "Earning honest bread by creating real value without ever selling your spine."),
            ("[CYAN]AGE 24 MENTAL AWAKENING:", "At Age 24, blend Jnana Buddhi (Independent Thinking) inside Family Life!"),
            ("[EMERALD]RIGHT LIVELIHOOD (SAMMA AJIVA):", "Dishonest wealth is a floating cloud; upright bamboo never surrenders its spine."),
        ],
        "D2 SCORE: 1–10 PTS  •  UNBOUGHT SPINE",
    ),
    (
        "P_D2_Host", "host", 7.5,
        "At age twenty-four you must start thinking independently so your mind grows—earning fifty percent Porul with upright bamboo dignity and unbowed peace!",
        "KARMIC GENIE SHOW  •  2. Earn with DIGNITY Always.",
        "DIMENSION 2 • AGE 24 THINKING & DIGNITY",
        "UPRIGHT BAMBOO INTEGRITY IN EVERY STORM",
        [
            ("[GOLD]THIRUKKURAL CH. 97 (MAANAM):", "True greatness guards unbought honor above every external badge."),
            ("[EMERALD]AGE 24 JNANA MARGAM BLEND:", "Awakening independent thought inside safe Family Karma Margam."),
            ("[AMBER]CONSCIENCE REJECTION:", "Flattering falsehood or stealing a junior's credit rots inner nobility."),
        ],
        "CLEAN SWEAT = EMPEROR-LEVEL PEACE OF MIND",
    ),
    # D3: Practice Life DISCIPLINE. (2 beats = 15s)
    (
        "P_D3_Bala", "bala", 7.5,
        "Dimension Three is Practice Life DISCIPLINE! Rule your habits, your sleep, and your senses every morning so your mind stays free and bright!",
        "KARMIC GENIE SHOW  •  3. Practice Life DISCIPLINE.",
        "DIMENSION 3 • PRIMARY DEFINITION BY BALA-RISHI",
        "3. PRACTICE LIFE DISCIPLINE.",
        [
            ("[GOLD]SOVEREIGN SENSE MASTERY:", "Guarding the five senses and tongue like a tortoise in its shell (Kural 126)."),
            ("[EMERALD]AGE 4 TO SCHOOL SHIFT:", "100% Play at Age 4 -> 50% Studying + 50% Outdoor Play in School Years (8–16)."),
            ("[CYAN]DHAMMAPADA VERSE 80:", "Irrigators channel water; archers straighten arrows; the wise master themselves."),
        ],
        "D3 SCORE: 1–10 PTS  •  OWN YOUR SUNRISE HOUR",
    ),
    (
        "P_D3_Host", "host", 7.5,
        "At age four your duty is hundred-percent play so your body grows—in adulthood, discipline guards your fifty-fifty Porul and family balance!",
        "KARMIC GENIE SHOW  •  3. Practice Life DISCIPLINE.",
        "DIMENSION 3 • STAGE-APPROPRIATE RHYTHM",
        "GUARDING THE 100% PROPORTIONAL MATRIX",
        [
            ("[EMERALD]WHY KARMA MARGAM IS SAFEST:", "Solitary Jnana/Bhakti have zero margin for error; Family Life cushions mistakes!"),
            ("[GOLD]GUARDING MALE & FEMALE RATIOS:", "Prevents 50% Porul or screens from bloating to 90% and starving home."),
            ("[CYAN]10:00 PM PILLOW TEST:", "Zero midnight doomscrolling -> Deep restorative sleep."),
        ],
        "DISCIPLINE = BIOLOGICAL RHYTHM OF FREEDOM",
    ),
    # D4: Uphold Karmic DHARMA. (2 beats = 15s)
    (
        "P_D4_Bala", "bala", 7.5,
        "Dimension Four is Uphold Karmic DHARMA! Be like a sweet mango tree sharing shade and fruit with every creature on Mother Earth!",
        "KARMIC GENIE SHOW  •  4. Uphold Karmic DHARMA.",
        "DIMENSION 4 • PRIMARY DEFINITION BY BALA-RISHI",
        "4. UPHOLD KARMIC DHARMA.",
        [
            ("[GOLD]VITAL ORGAN IN EARTH'S BODY:", "Living like a heart or lung nourishing 37 trillion cells, never a hoarding tumor."),
            ("[EMERALD]THIRUKKURAL KURALS 215–217:", "Ooruni (Overflowing Village Well), Payan Maram (Fruit Tree) & Medicine Tree."),
            ("[CYAN]LAOZI (TAO TE CHING CH. 8):", "The highest good is like water that nourishes all things without competing."),
        ],
        "D4 SCORE: 1–10 PTS  •  FRUIT-BEARING BANYAN",
    ),
    (
        "P_D4_Host", "host", 7.5,
        "When a father's fifty-percent Porul and a mother's sacred Arul unite in family Dharma, your home becomes an overflowing village spring!",
        "KARMIC GENIE SHOW  •  4. Uphold Karmic DHARMA.",
        "DIMENSION 4 • MARRIAGE OF PORUL & ARUL",
        "HIGHWAYS ARE PATHWAYS, NEVER YOUR HOME",
        [
            ("[GOLD]KURALS 46–48 SUPREME DHARMA:", "Householder Family Life (Illaram) nourishes ascetics, elders, and children alike."),
            ("[EMERALD]BANYAN (40/30/20/10) & BEE (50/35/15):", "Every living creature shares its surplus with Mother Earth."),
            ("[AMBER]BARREN FOREST WARNING:", "Hoarding wealth across four 12-year cycles leaves the heart in Conscience Rejection."),
        ],
        "PORUL + ARUL = VILLAGE WELL & MEDICINE TREE",
    ),
    # D5: Raise Family with DEVOTION. (2 beats = 15s)
    (
        "P_D5_Bala", "bala", 7.5,
        "Dimension Five is Raise Family with DEVOTION! Put down your phone tonight, hug your parents and children tight, and give them your whole heart!",
        "KARMIC GENIE SHOW  •  5. Raise Family with DEVOTION.",
        "DIMENSION 5 • PRIMARY DEFINITION BY BALA-RISHI",
        "5. RAISE FAMILY WITH DEVOTION.",
        [
            ("[GOLD]UNDIVIDED HEART AT HOME:", "Giving aging parents, spouse, and children your warmest presence, never leftovers."),
            ("[EMERALD]BUDDHA'S MANGALA SUTTA:", "Supporting mother and father, cherishing spouse and children is the highest blessing."),
            ("[CYAN]THIRUKKURAL KURAL 80:", "A body with living love is the seat of the soul; without it, mere bones wrapped in skin."),
        ],
        "D5 SCORE: 1–10 PTS  •  TRUE CONNECTEDNESS",
    ),
    (
        "P_D5_Host", "host", 7.5,
        "Family Karma Margam is the safest, fastest soul path—forgiving mistakes with rule relaxations while blending Buddhi at twenty-four and Bakthi at fifty-four!",
        "KARMIC GENIE SHOW  •  5. Raise Family with DEVOTION.",
        "DIMENSION 5 • SAFEST & FASTEST SOUL LABORATORY",
        "WHY FAMILY LIFE OUTPACES SOLITARY CAVES",
        [
            ("[EMERALD]HUMANE RULE RELAXATIONS:", "In Family Karma Margam, you can afford to make mistakes, be forgiven & keep growing!"),
            ("[GOLD]MOTHER BIRD (50/50) & HOME HEARTH:", "Father's 50/15/15/10/10 Porul + Mother's 100% Arul & Daily Pooja."),
            ("[CYAN]PROGRESSIVE MARGAM MIX:", "Safe Family Karma Margam + Jnana (@ 24) + Bhakti (@ 54) = Fastest Soul Growth!"),
        ],
        "KURALS 46–48: FAMILY LIFE IS THE SUPREME PATH",
    ),
    # D6: Be Grateful to Your DIVINE. (2 beats = 15s)
    (
        "P_D6_Bala", "bala", 7.5,
        "Dimension Six is Be Grateful to Your DIVINE! Say thank you every sunrise to the Grand Architect of your body, mind, and soul!",
        "KARMIC GENIE SHOW  •  6. Be Grateful to Your DIVINE.",
        "DIMENSION 6 • PRIMARY DEFINITION BY BALA-RISHI",
        "6. BE GRATEFUL TO YOUR DIVINE.",
        [
            ("[GOLD]DAWN HUMILITY (KURAL 1 & 2):", "Bowing before the Grand Architect who harmonized Body, Mind, Soul & Para-Soul."),
            ("[EMERALD]AGE 54 SOUL TURNING POINT:", "At Age 54, shift from accumulating Porul to 50%+ Arul and Thanking!"),
            ("[CYAN]MOTHER'S DAILY POOJA:", "Brings living Bhakti Margam directly into the family home from childhood."),
        ],
        "D6 SCORE: 1–10 PTS  •  THANK AT AGE 54",
    ),
    (
        "P_D6_Host", "host", 7.5,
        "At age fifty-four you must shift from Porul to fifty-percent Arul and start thanking—bringing Bhakti Margam home so your soul blossoms!",
        "KARMIC GENIE SHOW  •  6. Be Grateful to Your DIVINE.",
        "DIMENSION 6 • AGE 54 BHAKTI THANKSGIVING",
        "SHIFTING FROM PORUL TO 50%+ ARUL AT 54",
        [
            ("[GOLD]AGE 54 MANDATE:", "Without Thanking at Age 54, the Soul cannot grow and suffocates in ego boasting."),
            ("[EMERALD]SAFE BHAKTI INSIDE HOME:", "Mother's daily Pooja + Age 54 Thanksgiving = Bhakti without ascetic peril."),
            ("[CYAN]EVERY CLOSED DOOR IS GRACE:", "Gratitude turns every career shift into redirection toward higher purpose."),
        ],
        "AGE 54: 50% THANKING + 25% MENTORING + 25% GRACE",
    ),
    # D7: Purposeful Life Is Your DESTINY. (2 beats = 15s)
    (
        "P_D7_Bala", "bala", 7.5,
        "Dimension Seven is Purposeful Life Is Your DESTINY! Score above thirty-five across all Seven D's—and shine as a Pioneer of the New World!",
        "KARMIC GENIE SHOW  •  7. Purposeful Life Is Your DESTINY.",
        "DIMENSION 7 • PRIMARY DEFINITION BY BALA-RISHI",
        "7. PURPOSEFUL LIFE IS YOUR DESTINY.",
        [
            ("[GOLD]SEVENTH FLOWER OF SIX ROOTS:", "When D1–D6 align above 35 / 70, Purposeful Destiny blossoms naturally!"),
            ("[CYAN]BUDDHA'S 5-LINK KARMIC CHAIN:", "Thought -> Action -> Habit -> Character -> Sovereign Destiny."),
            ("[EMERALD]THIRUKKURAL KURAL 620:", "Tireless righteous effort makes even Fate step aside."),
        ],
        "D7 SCORE: 1–10 PTS  •  PIONEER OF THE NEW WORLD",
    ),
    (
        "P_D7_Host", "host", 7.5,
        "Walk safe family Karma Margam—play hundred percent at four, blend Jnana Buddhi at twenty-four, and Bhakti thanksgiving at fifty-four to claim your Destiny!",
        "KARMIC GENIE SHOW  •  7. Purposeful Life Is Your DESTINY.",
        "DIMENSION 7 • GRAND SYNTHESIS OF THE 7D WAY",
        "PLAY AT 4  •  THINK AT 24  •  THANK AT 54",
        [
            ("[GOLD]LIFECYCLE HARMONY:", "100% Play (@ 4) -> 50/50 Study-Play (@ 8–16) -> Porul & Arul (@ 24–48) -> Thank (@ 54+)."),
            ("[EMERALD]THREE MARGAMS IN ONE HOME:", "Safe Family Karma Margam + Jnana (@ 24) + Bhakti (@ 54) = Maximum Soul Growth!"),
            ("[CYAN]FINAL COMPASS CALL:", "Never settle below 35 / 70 in Conscience Rejection—claim 10/10 Peace of Mind!"),
        ],
        "WALK THE 7D WAY  •  PIONEERS OF THE NEW WORLD",
    ),
]


def build_pilot_s01e00_360p(pools: dict[str, list[Path]]) -> Path:
    print("\n🎬 Building Updated Pilot (S01E00): 'The 7D Way' with Vedic Intro Narration & Side-by-Side HUD (360p)...", flush=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    co_mp4 = TEMP_DIR / "e01_cold_open.mp4"
    fin_mp4 = TEMP_DIR / "e01_finale_logo.mp4"

    parts = [co_mp4]
    cursor = probe_duration(co_mp4)
    timings = []

    h_idx, b_idx = 0, 0
    for idx, (bid, role, dur_s, spoken_txt, m_banner, h_tag, c_title, bullets, f_metric) in enumerate(PILOT_BEATS):
        if role == "bala":
            v_clip = pools["bala"][b_idx % len(pools["bala"])]
            b_idx += 1
        else:
            v_clip = pools["host"][h_idx % len(pools["host"])]
            h_idx += 1

        aud_wav, _, _, actual_a_dur = build_beat_audio(bid, spoken_txt, role, target_dur=dur_s)
        hud_png = render_side_by_side_hud_png(
            hud_id=bid,
            maxim_banner=m_banner,
            header_tag=h_tag,
            card_title=c_title,
            bullets=bullets,
            footer_metric=f_metric,
        )
        seg_mp4 = render_side_by_side_beat_mp4(
            beat_id=bid,
            video_clip=v_clip,
            audio_wav=aud_wav,
            hud_png=hud_png,
            target_dur=actual_a_dur,
            cam_dir=1 if idx % 2 == 0 else -1,
        )
        seg_d = probe_duration(seg_mp4)
        timings.append({
            "bid": bid,
            "role": role,
            "text": spoken_txt,
            "start": cursor,
            "end": cursor + seg_d,
        })
        parts.append(seg_mp4)
        cursor += seg_d
        print(f"   • Rendered Pilot [{idx+1:02d}/{len(PILOT_BEATS)}] {bid} ({role}) -> cum={cursor:.1f}s", flush=True)

    fin_start = cursor
    parts.append(fin_mp4)

    concat_txt = TEMP_DIR / "pilot_vedic_concat.txt"
    concat_txt.write_text("\n".join(f"file '{p}'" for p in parts) + "\n", encoding="utf-8")
    stitched_mp4 = TEMP_DIR / "pilot_vedic_stitched_1080p.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy", str(stitched_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    tot_dur = probe_duration(stitched_mp4)
    ass_path = TEMP_DIR / "pilot_vedic_subtitles.ass"
    build_ass_subtitles(ass_path, timings)

    vol_expr = f"if(lt(t,4.80), 0.52, if(gt(t,{fin_start-0.40:.2f}), 0.52, 0.036))"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(stitched_mp4),
        "-ss", "4.00", "-stream_loop", "-1", "-i", str(THEME_WAV),
        "-filter_complex", (
            f"[0:v]ass={ass_path},fade=t=in:st=0:d=0.50,fade=t=out:st={tot_dur-0.80:.2f}:d=0.75,"
            "scale=640:360:flags=bicubic[vout];"
            f"[1:a]atrim=0:{tot_dur:.3f},asetpts=PTS-STARTPTS,lowpass=f=9000,volume='{vol_expr}':eval=frame[bgm];"
            "[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0,volume=1.45[aout]"
        ),
        "-map", "[vout]", "-map", "[aout]",
        "-t", f"{tot_dur:.3f}",
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-crf", "20",
        "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(OUT_PILOT_360P)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    shutil.copy2(OUT_PILOT_360P, ART_PILOT_360P)
    print(f"🏆 PILOT S01E00 ('The 7D Way') 360p READY: {OUT_PILOT_360P} ({tot_dur:.2f}s | {OUT_PILOT_360P.stat().st_size/1e6:.2f} MB)", flush=True)
    return OUT_PILOT_360P


def render_qa_Verification_sheet(e01_mp4: Path, pilot_mp4: Path) -> Path:
    """Extracts 6 key frames from S01E01 and 3 from S01E00 to verify Side-by-Side HUD + @Me + Subtitles."""
    qa_jpg = CUR_BRAIN / "qa_s01e01_and_pilot_vedic_360p_sheet.jpg"
    canvas = Image.new("RGB", (1920, 1080), (12, 16, 26))
    draw = ImageDraw.Draw(canvas)
    f_lbl = ImageFont.truetype(FONT_BOLD, 16)

    samples = [
        (e01_mp4, 8.0, "S01E01 Beat 00 • Vedic 7D Intro Narration (Adult @Me)"),
        (e01_mp4, 17.0, "S01E01 Beat 01 • Primary Definition (4yo Bala-Rishi @Me)"),
        (e01_mp4, 32.0, "S01E01 Beat 03 • Why Family Life (Karma Margam) Is Safest & Fastest"),
        (e01_mp4, 62.0, "S01E01 Beat 07 • Age 4: 100% Play -> Physical Body Growth (Bala-Rishi)"),
        (e01_mp4, 145.0, "S01E01 Beat 18 • Adult Male 100% Porul Matrix (50/15/15/10/10)"),
        (e01_mp4, 152.5, "S01E01 Beat 19 • Adult Female 100% Arul & Daily Pooja Matrix"),
        (e01_mp4, 198.0, "S01E01 Beat 25 • Age 54: Blending Bhakti Margam (50% Thanking)"),
        (e01_mp4, 228.0, "S01E01 Beat 29 • Philosopher 1: Saint Thiruvalluvar (Kurals 46 & 293)"),
        (pilot_mp4, 8.0, "S01E00 Pilot Beat 00 • Vedic 7D Intro Narration + All 7 Maxims"),
    ]

    cw, ch = 620, 330
    for idx, (mp4, ts, title) in enumerate(samples):
        png = TEMP_DIR / f"qa_f_{idx:02d}.png"
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{ts:.2f}", "-i", str(mp4),
            "-frames:v", "1", "-vf", f"scale={cw}:{ch}", str(png)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        col, row = idx % 3, idx // 3
        x0 = 15 + col * (cw + 15)
        y0 = 18 + row * (ch + 24)
        canvas.paste(Image.open(png).convert("RGB"), (x0, y0))
        draw.rectangle([x0, y0, x0 + cw, y0 + 28], fill=(8, 12, 22))
        draw.text((x0 + 8, y0 + 5), title, font=f_lbl, fill=(255, 224, 140))

    canvas.save(qa_jpg, quality=92)
    print(f"🖼️ Saved Visual QA Sheet: {qa_jpg}", flush=True)
    return qa_jpg


def main():
    pools = collect_verified_me_clips()
    print(f"📦 Collected verified @Me clip pools: Host={len(pools['host'])}, Bala-Rishi={len(pools['bala'])}, Genie={len(pools['genie'])}", flush=True)
    e01_mp4 = build_s01e01_360p(pools)
    pilot_mp4 = build_pilot_s01e00_360p(pools)
    render_qa_Verification_sheet(e01_mp4, pilot_mp4)


if __name__ == "__main__":
    main()
