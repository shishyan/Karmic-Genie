#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
7D Virtues — 30-Second Spoken Philosophical Explainer & Storyboard Sketch Builder
for Karmic Genie Show (Season 1, Episode 0: "The 7D Way — Pioneers of the New World")

Expands each of the 7 Dimensions (`D1 DUTY` through `D7 DESTINY`) into a **100% spoken,
zero-dead-air 30.0-second video** synthesizing the timeless Eastern philosophical wisdom of:
  1. **Thiruvalluvar (*Thirukkural*)** — Conscience (*Manasatchi*), Unbought Honor (*Maanam*),
     The Five-Sense Tortoise (*Adakkam*), The Village Well & Medicine Tree (*Ooruni*),
     Living Family Love (*Anbu*), Gratitude to the First Source, and Persistent Effort (*Uzhai*).
  2. **Gautama Buddha (*Dhammapada* & *Suttas*)** — Right Livelihood (*Samma Ajiva*), Irrigators
     Channeling the Mind, Cherishing Parents & Family (*Mangala Sutta*), Supreme Gratitude
     (*Katannuta*), and the 5-Link Chain (`Thought -> Action -> Habit -> Character -> Destiny`).
  3. **Laozi (*Tao Te Ching*) & Confucius (*Analects*)** — Filial Duty as the Root of Virtue (*Xiao*),
     Dishonest Wealth as Floating Clouds, Upright Bamboo Integrity, Water Nourishing All Without
     Competing (*Shang Shan Ruo Shui*), and the Thousand-Mile Journey Beginning Today.

Visual & Audio Structure of Every 30.0-Second Virtue Video (`D1`–`D7`):
  - **Beat 1 (0.0s – ~7.4s):** Adult Host (`@Me`) in the pure-white 7D Studio (`full` orbital -> close-up)
  - **Beat 2A (~7.4s – ~15.0s):** Spoken Philosophical Expansion Part A + **Concept Sketch A** in `pip75`
    (live charcoal pencil stroke drawing reveal -> ink & gold visual metaphor pan from Left to Right)
  - **Beat 2B (~15.0s – ~22.4s):** Spoken Philosophical Expansion Part B + **Concept Sketch B** in `pip75`
    (live charcoal pencil stroke drawing reveal -> ink & gold visual metaphor focus)
  - **Beat 3 (~22.4s – 30.0s):** 4-Year-Old Bala-Rishi (`@Me`) in the 7D Studio (`full` orbital -> close-up)
"""

import asyncio
import json
import shutil
import subprocess
import wave
from pathlib import Path
import edge_tts
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
PILOT_DIR = REPO_DIR / "episodes" / "S01E00_Pilot_The_7D_Way"
SKETCH_DIR = PILOT_DIR / "sketches_7d_philosophers"
ANIM_CLIPS_DIR = SKETCH_DIR / "animated_parables"
VIRTUES_30S_DIR = PILOT_DIR / "virtues_30s"
OVERLAYS_DIR = PILOT_DIR / "overlays_s01e00"
CLIP_MAP_JSON = PILOT_DIR / "pilot_clip_map.json"
TEMP_DIR = PILOT_DIR / "temp_sketch_build"

MASTERS_DIR = REPO_DIR / "assets" / "studio_v5_masters"
PILOT_STAGE_JPG = MASTERS_DIR / "v8_pilot_7d_scorecard_stage_16x9.jpg"
THEME_WAV = REPO_DIR / "assets" / "theme" / "official_karmic_genie_7d_theme_song.wav"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

VIRTUE_SPECS = [
    {
        "id": "d1_duty",
        "num": 1,
        "title": "D1 • RESPECT YOUR DUTY FIRST",
        "sketch_a": "d1_a_conscience_bell.png",
        "sketch_b": "d1_b_filial_root.png",
        "banner_a": "EASTERN WISDOM I • EVEN WHEN HIDDEN FROM THE WORLD, CONSCIENCE RINGS WITHIN",
        "banner_b": "EASTERN WISDOM II • FILIAL DUTY IS THE LIVING ROOT FROM WHICH ALL VIRTUE GROWS",
        "host_key": "H02_Host_D1_Duty_Definition",
        "beat_a_clip_key": "H03_Host_D1_Silenced_Conscience",
        "bala_key": "G01_Bala_D1_Duty",
        "overlay": "ov_d1_duty.png",
        "host_lines": [
            "First is Duty. Duty is never your office job—",
            "Duty is the task that triggers guilt in your conscience when you leave it undone!",
        ],
        "beat_a_tts": (
            "A thief feels conscience guilt the first few times—drown that trigger with alcohol "
            "or neglect, and conscience goes silent, draining our world of empathy!"
        ),
        "beat_a_lines": [
            "A thief feels conscience guilt the first few times—drown that trigger with alcohol",
            "or neglect, and conscience goes silent, draining our world of empathy!",
        ],
        "beat_b_tts": (
            "Eastern sages teach that caring for aging parents and family is the living root of humanity: "
            "when the root is watered first, every branch of life blossoms naturally."
        ),
        "beat_b_lines": [
            "Caring for aging parents and family is the living root of humanity:",
            "when the root is watered first, every branch of life blossoms naturally!",
        ],
        "bala_lines": [
            "Dimension One is Duty! Never drink away the whisper of your conscience—",
            "when your heart says care for someone today, listen right away!",
        ],
    },
    {
        "id": "d2_dignity",
        "num": 2,
        "title": "D2 • EARN WITH DIGNITY ALWAYS",
        "sketch_a": "d2_a_bamboo_spine.png",
        "sketch_b": "d2_b_right_livelihood_pillow.png",
        "banner_a": "EASTERN WISDOM I • UNBOUGHT HONOR STANDS LIKE BAMBOO IN THE STORM",
        "banner_b": "EASTERN WISDOM II • RIGHT LIVELIHOOD GRANTS AN UNBURDENED PILLOW AT NIGHT",
        "host_key": "H04_Host_D2_Dignity_Explain",
        "beat_a_clip_key": None,
        "bala_key": "G02_Bala_D2_Dignity",
        "overlay": "ov_d2_dignity.png",
        "host_lines": [
            "Second is Dignity—unbought self-respect! Earn your livelihood honestly",
            "by building real value, never by selling your spine, your truth, or your peace!",
        ],
        "beat_a_tts": (
            "Ancient wisdom teaches that wealth and rank won by bending your truth are mere floating clouds. "
            "True dignity stands like bamboo in a storm—flexible, yet never surrendering its spine."
        ),
        "beat_a_lines": [
            "Wealth and rank won by bending your truth are mere floating clouds;",
            "true Dignity stands like bamboo in a storm—flexible, yet never surrendering its spine!",
        ],
        "beat_b_tts": (
            "Right livelihood means earning through honest skill without harming a single soul—"
            "giving you the one treasure no gold can buy: deep, unburdened sleep every night."
        ),
        "beat_b_lines": [
            "Right Livelihood earns through honest skill without harming a single soul—",
            "granting the one treasure no gold can buy: deep, unburdened sleep every night!",
        ],
        "bala_lines": [
            "Dimension Two is Dignity! Stand tall with an honest heart—",
            "no paycheck or title is ever worth trading away your self-respect!",
        ],
    },
    {
        "id": "d3_discipline",
        "num": 3,
        "title": "D3 • PRACTICE LIFE DISCIPLINE",
        "sketch_a": "d3_a_tortoise_five_senses.png",
        "sketch_b": "d3_b_irrigated_mind_river.png",
        "banner_a": "EASTERN WISDOM I • GUARD THE FIVE SENSES LIKE A TORTOISE WITHIN ITS SHELL",
        "banner_b": "EASTERN WISDOM II • IRRIGATORS CHANNEL WATER; WISE SOULS CHANNEL THE MIND",
        "host_key": "H05_Host_D3_Discipline_Explain",
        "beat_a_clip_key": None,
        "bala_key": "G03_Bala_D3_Discipline",
        "overlay": "ov_d3_discipline.png",
        "host_lines": [
            "Third is Discipline—sovereign mastery over your senses, tongue, and clock,",
            "so impulsive cravings and midnight screens never enslave your mind!",
        ],
        "beat_a_tts": (
            "Like a wise tortoise drawing all five limbs inside its shell when danger approaches, "
            "guarding your five senses and your tongue in one day protects your peace for seven lifetimes."
        ),
        "beat_a_lines": [
            "Like a wise tortoise drawing all five limbs inside its shell against danger,",
            "guarding your five senses and tongue protects your peace for seven lifetimes!",
        ],
        "beat_b_tts": (
            "Irrigators channel wild floods into fertile fields, and fletchers straighten crooked arrows; "
            "conquering others is mere force, but mastering your own morning rhythm is true power."
        ),
        "beat_b_lines": [
            "Irrigators channel wild floods into fertile fields; fletchers straighten arrows—",
            "conquering others is force, but mastering your own morning mind is true power!",
        ],
        "bala_lines": [
            "Dimension Three is Discipline! Rule your habits, your sleep, and your senses",
            "every morning so your mind stays free and bright!",
        ],
    },
    {
        "id": "d4_dharma",
        "num": 4,
        "title": "D4 • UPHOLD KARMIC DHARMA",
        "sketch_a": "d4_a_ooruni_well_and_tree.png",
        "sketch_b": "d4_b_vital_organs_highway.png",
        "banner_a": "EASTERN WISDOM I • BE AN OVERFLOWING VILLAGE WELL & MEDICINE TREE FOR ALL",
        "banner_b": "EASTERN WISDOM II • INDUSTRIES ARE HIGHWAYS & PATHWAYS, NEVER YOUR DESTINATION",
        "host_key": "H06_Host_D4_Dharma_Explain",
        "beat_a_clip_key": None,
        "bala_key": "G04_Bala_D4_Dharma",
        "overlay": "ov_d4_dharma.png",
        "host_lines": [
            "Fourth is Dharma—living as a vital organ in Earth's body,",
            "like a fruit-bearing banyan tree offering shade and nourishment to all!",
        ],
        "beat_a_tts": (
            "Prosperity in the hands of a dharmic soul is never a locked vault—it is an overflowing "
            "village drinking well, a ripe fruit tree in the town square, and a medicine tree that heals all."
        ),
        "beat_a_lines": [
            "Prosperity in a dharmic soul is an overflowing village drinking well",
            "and a medicinal tree whose every leaf and fruit heals the world!",
        ],
        "beat_b_tts": (
            "The highest good is like water that nourishes all things without competing. "
            "Every industry is a highway and pathway to serve life—never the soul's final home."
        ),
        "beat_b_lines": [
            "The highest good is like water that nourishes all things without competing—",
            "every industry is a pathway to serve life, never the soul's final home!",
        ],
        "bala_lines": [
            "Dimension Four is Dharma! Be like a sweet mango tree",
            "sharing shade and fruit with every creature on Mother Earth!",
        ],
    },
    {
        "id": "d5_devotion",
        "num": 5,
        "title": "D5 • RAISE FAMILY WITH DEVOTION",
        "sketch_a": "d5_a_screens_vs_presence.png",
        "sketch_b": "d5_b_three_generation_hearth.png",
        "banner_a": "EASTERN WISDOM I • A BODY WITHOUT WARM FAMILY LOVE IS BONES WRAPPED IN SKIN",
        "banner_b": "EASTERN WISDOM II • CHERISHING PARENTS, SPOUSE & CHILDREN IS THE HIGHEST BLESSING",
        "host_key": "H07_Host_D5_Devotion_Explain",
        "beat_a_clip_key": None,
        "bala_key": "G05_Bala_D5_Devotion",
        "overlay": "ov_d5_devotion.png",
        "host_lines": [
            "Fifth is Devotion—true connectedness at home! Give your aging parents,",
            "spouse, and children your warm, undivided presence today, never exhausted leftovers!",
        ],
        "beat_a_tts": (
            "Eastern wisdom declares that a body with living love is the true seat of the soul, "
            "while a life that walls out its own family behind screens is merely bones wrapped in skin."
        ),
        "beat_a_lines": [
            "A body with living love is the true seat of the soul—",
            "walling out your own family behind screens leaves only bones wrapped in skin!",
        ],
        "beat_b_tts": (
            "Cherishing mother and father, and holding spouse and children with warm, unhurried eyes tonight—"
            "when love and virtue dwell at home, no greater treasure exists on Earth."
        ),
        "beat_b_lines": [
            "Cherishing parents, spouse, and children with warm, unhurried eyes tonight—",
            "when love dwells at home, no greater treasure exists on Earth!",
        ],
        "bala_lines": [
            "Dimension Five is Devotion! Put down your phone tonight,",
            "hug your parents and children tight, and give them your whole heart!",
        ],
    },
    {
        "id": "d6_divine",
        "num": 6,
        "title": "D6 • BE GRATEFUL TO YOUR DIVINE",
        "sketch_a": "d6_a_four_rings_harmony.png",
        "sketch_b": "d6_b_closed_door_higher_arch.png",
        "banner_a": "EASTERN WISDOM I • BODY SERVES MIND -> MIND SERVES SOUL -> SOUL SERVES PARA-SOUL",
        "banner_b": "EASTERN WISDOM II • GRATITUDE TURNS EVERY CLOSED DOOR INTO A HIGHER PATH",
        "host_key": "H08_Host_D6_Divine_Explain",
        "beat_a_clip_key": None,
        "bala_key": "G06_Bala_D6_Divine",
        "overlay": "ov_d6_divine.png",
        "host_lines": [
            "Sixth is gratitude to the Divine—daily humility before the Grand Architect",
            "who harmonized your body, mind, soul, and para-soul!",
        ],
        "beat_a_tts": (
            "What use is vast intellect if it never bows to the First Source of the cosmos? "
            "Just as cells serve the body, your body serves mind, mind serves soul, and soul serves Para-Soul."
        ),
        "beat_a_lines": [
            "What use is vast intellect if it never bows to the Source of the cosmos?",
            "Your body serves mind, mind serves soul, and soul serves the Para-Soul!",
        ],
        "beat_b_tts": (
            "Daily gratitude at sunrise melts away ego and fear—revealing that every closed door "
            "in your career is the Grand Architect redirecting you toward your true purpose."
        ),
        "beat_b_lines": [
            "Daily gratitude at sunrise melts away ego and fear—revealing that",
            "every closed door is the Grand Architect redirecting you to higher purpose!",
        ],
        "bala_lines": [
            "Dimension Six is the Divine! Say thank you every sunrise",
            "to the Grand Architect of your body, mind, and soul!",
        ],
    },
    {
        "id": "d7_destiny",
        "num": 7,
        "title": "D7 • PURPOSEFUL LIFE IS YOUR DESTINY",
        "sketch_a": "d7_a_seed_to_destiny_chain.png",
        "sketch_b": "d7_b_seven_pillars_pioneer.png",
        "banner_a": "EASTERN WISDOM I • THOUGHT -> ACTION -> HABIT -> CHARACTER -> DESTINY",
        "banner_b": "EASTERN WISDOM II • SCORE ABOVE 35 / 70 TO SHINE AS A PIONEER OF THE NEW WORLD",
        "host_key": "H09_Host_D7_Destiny_Explain",
        "beat_a_clip_key": None,
        "bala_key": "G07_Bala_D7_Destiny_Blessing",
        "overlay": "ov_d7_destiny.png",
        "host_lines": [
            "Seventh is Destiny—when Duty, Dignity, Discipline, Dharma, Devotion, and Divine",
            "align above thirty-five, you flower into a Pioneer of the New World!",
        ],
        "beat_a_tts": (
            "Watch your thoughts, for they become actions; actions become daily habits; "
            "habits forge character; and your character becomes your Destiny."
        ),
        "beat_a_lines": [
            "Watch your thoughts, for they become actions; actions become daily habits;",
            "habits forge your character; and character becomes your Destiny!",
        ],
        "beat_b_tts": (
            "A journey of a thousand miles begins beneath your feet today. "
            "Score every choice across all seven virtues—rise above thirty-five out of seventy, and claim your Destiny!"
        ),
        "beat_b_lines": [
            "A journey of a thousand miles begins beneath your feet today—",
            "score above thirty-five out of seventy across all Seven D's and claim your Destiny!",
        ],
        "bala_lines": [
            "Dimension Seven is your Destiny! Score above thirty-five across all Seven D's—",
            "and shine as a Pioneer of the New World!",
        ],
    },
]


def probe_duration(path: Path) -> float:
    res = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)
    ]).decode())
    return float(res["format"]["duration"])


def detect_speech_bounds_rms(mp4_path: Path, fallback: tuple[float, float] = (0.25, 7.65)) -> tuple[float, float, float]:
    """Detects speech `(sp_st, sp_en, raw_dur)` directly from 16kHz mono WAV RMS energy."""
    raw_dur = probe_duration(mp4_path)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    wav_tmp = TEMP_DIR / f"rms_{mp4_path.stem}.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(mp4_path), "-vn", "-ac", "1", "-ar", "16000", str(wav_tmp)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(str(wav_tmp), "rb") as wf:
        arr = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    win = 800  # 50ms windows
    if len(arr) < win * 4:
        return (fallback[0], min(raw_dur, fallback[1]), raw_dur)
    n_wins = len(arr) // win
    rms = np.sqrt(np.mean(arr[: n_wins * win].reshape(n_wins, win) ** 2, axis=1))
    peak = float(np.percentile(rms, 95))
    thresh = max(0.012, peak * 0.16)
    active = np.where(rms >= thresh)[0]
    if len(active) < 4:
        return (fallback[0], min(raw_dur, fallback[1]), raw_dur)
    sp_st = max(0.08, float(active[0] * 0.05))
    sp_en = min(raw_dur - 0.08, float((active[-1] + 1) * 0.05))
    if sp_en - sp_st < 2.0:
        return (fallback[0], min(raw_dur, fallback[1]), raw_dur)
    return (sp_st, sp_en, raw_dur)


async def _synth_edge_tts(text: str, out_mp3: Path):
    comm = edge_tts.Communicate(text, voice="en-IN-PrabhatNeural", rate="+4%", pitch="-2Hz")
    await comm.save(str(out_mp3))


def synthesize_philosophical_narration_wav(
    text: str,
    target_dur: float,
    out_wav: Path,
    clip_override: Path | None = None,
) -> tuple[float, float]:
    """
    Produces a broadcast-mastered 48kHz stereo WAV of exact duration `target_dur`
    with continuous spoken philosophical wisdom (using `clip_override` audio if provided,
    otherwise neural South Indian English voiceover matched to the studio broadcast EQ).
    Returns `(rel_sp_st, rel_sp_en)`.
    """
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    if clip_override and clip_override.exists():
        sp_st, sp_en, raw_dur = detect_speech_bounds_rms(clip_override, (0.20, 7.60))
        trim_st = max(0.0, sp_st - 0.14)
        trim_en = min(raw_dur, sp_en + 0.18)
        sp_len = max(1.0, trim_en - trim_st)
        tempo = np.clip(sp_len / max(1.5, target_dur - 0.20), 0.88, 1.18)
        subprocess.run([
            "ffmpeg", "-y", "-i", str(clip_override),
            "-af", (
                f"atrim=start={trim_st:.3f}:end={trim_en:.3f},asetpts=PTS-STARTPTS,"
                f"atempo={tempo:.4f},highpass=f=80,lowpass=f=12500,"
                f"apad=whole_dur={target_dur:.3f},"
                f"afade=t=in:st=0:d=0.06,afade=t=out:st={max(0.2, target_dur-0.10):.3f}:d=0.10,"
                "aresample=48000,aformat=sample_fmts=s16:channel_layouts=stereo"
            ),
            "-t", f"{target_dur:.3f}", str(out_wav)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return (0.12, max(1.0, target_dur - 0.14))

    raw_mp3 = out_wav.with_suffix(".raw.mp3")
    asyncio.run(_synth_edge_tts(text, raw_mp3))
    sp_st, sp_en, raw_dur = detect_speech_bounds_rms(raw_mp3, (0.05, 9.50))
    trim_st = max(0.0, sp_st - 0.08)
    trim_en = min(raw_dur, sp_en + 0.12)
    sp_len = max(1.0, trim_en - trim_st)

    # Fit cleanly inside `target_dur - 0.24s` (0.12s lead-in, 0.12s tail)
    usable = max(2.0, target_dur - 0.24)
    tempo = float(np.clip(sp_len / usable, 0.88, 1.25))
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_mp3),
        "-af", (
            f"atrim=start={trim_st:.3f}:end={trim_en:.3f},asetpts=PTS-STARTPTS,"
            f"atempo={tempo:.4f},"
            "equalizer=f=165:width_type=o:width=1.2:g=2.5,"
            "equalizer=f=3200:width_type=o:width=1.0:g=1.5,"
            "highpass=f=75,lowpass=f=12500,"
            "adelay=120|120,"
            f"apad=whole_dur={target_dur:.3f},"
            f"afade=t=in:st=0:d=0.06,afade=t=out:st={max(0.2, target_dur-0.10):.3f}:d=0.10,"
            "aresample=48000,aformat=sample_fmts=s16:channel_layouts=stereo"
        ),
        "-t", f"{target_dur:.3f}", str(out_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return (0.12, max(1.0, target_dur - 0.14))


def build_sketch_layers_with_banner(src_png: Path, banner_text: str, out_prefix: Path) -> tuple[Path, Path, Path]:
    """
    Converts a 16:9 concept sketch (`src_png`) into 3 precision 1432x802 plates for the `pip75` window:
      1. `parchment_jpg`: Warm aged Eastern parchment canvas + subtle bottom-top philosophical header strip
      2. `lineart_jpg`: Crisp hand-drawn charcoal/graphite contour lines on parchment
      3. `master_jpg`: Full Sumi-e ink wash + warm champagne-gold highlights + philosophical header strip
    """
    w, h = 1432, 802
    im = Image.open(src_png).convert("RGB").resize((w, h), Image.Resampling.LANCZOS)

    # 1. Warm aged ivory parchment base
    rng = np.random.default_rng(108)
    yy, xx = np.mgrid[0:h, 0:w]
    vignette = 1.0 - 0.12 * (((xx - w / 2.0) / (w / 2.0)) ** 2 + ((yy - h / 2.0) / (h / 2.0)) ** 2)
    base_rgb = np.array([245.0, 236.0, 218.0], dtype=np.float32)[None, None, :]
    grain = rng.normal(0.0, 2.5, size=(h, w, 1)).astype(np.float32)
    parchment_arr = np.clip(base_rgb * vignette[..., None] + grain, 0, 255).astype(np.uint8)

    # 2. Extract crisp charcoal pencil contour lines
    gray = ImageOps.grayscale(im)
    g_s = np.asarray(gray.filter(ImageFilter.GaussianBlur(radius=0.8)), dtype=np.float32)
    g_l = np.asarray(gray.filter(ImageFilter.GaussianBlur(radius=4.2)), dtype=np.float32)
    dog = np.clip((g_l - g_s) * 4.4, 0.0, 255.0) / 255.0
    ink_darkness = np.clip((215.0 - g_s) / 145.0, 0.0, 1.0) ** 1.35
    stroke_strength = np.clip(0.70 * dog + 0.50 * ink_darkness, 0.0, 1.0)

    charcoal_color = np.array([42.0, 32.0, 24.0], dtype=np.float32)[None, None, :]
    lineart_arr = (
        parchment_arr.astype(np.float32) * (1.0 - stroke_strength[..., None])
        + charcoal_color * stroke_strength[..., None]
    )

    parchment_im = Image.fromarray(parchment_arr)
    lineart_im = Image.fromarray(np.clip(lineart_arr, 0, 255).astype(np.uint8))
    master_im = ImageEnhance.Contrast(im).enhance(1.05)

    # Add a sleek, museum-grade translucent charcoal-and-gold philosophical scroll header at top of the sketch window
    f_ban = ImageFont.truetype(FONT_BOLD, 17)
    for target_im in (parchment_im, lineart_im, master_im):
        rgba = target_im.convert("RGBA")
        bar = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(bar)
        d.rectangle([0, 0, w, 36], fill=(16, 14, 12, 205))
        d.line([(0, 36), (w, 36)], fill=(235, 198, 112, 235), width=2)
        tw = d.textbbox((0, 0), banner_text, font=f_ban)[2]
        d.text(((w - tw) // 2, 8), banner_text, font=f_ban, fill=(252, 226, 152, 255))
        merged = Image.alpha_composite(rgba, bar).convert("RGB")
        target_im.paste(merged)

    p_path = out_prefix.parent / f"{out_prefix.name}_parchment.jpg"
    l_path = out_prefix.parent / f"{out_prefix.name}_lineart.jpg"
    m_path = out_prefix.parent / f"{out_prefix.name}_master.jpg"

    parchment_im.save(p_path, quality=95)
    lineart_im.save(l_path, quality=95)
    master_im.save(m_path, quality=95)
    return (p_path, l_path, m_path)


def render_spoken_sketch_beat(
    sketch_png: Path,
    banner_text: str,
    overlay_png: Path,
    audio_wav: Path,
    target_dur: float,
    orbit_dir: int,
    pan_dir: int,
    out_mp4: Path,
    preset: str = "fast",
) -> float:
    """
    Renders a single ~7.5s Spoken Storyboard Sketch Beat in `pip75`:
      - Audio: Continuous spoken philosophical narration (`audio_wav`)
      - Video:
          * 0.0s .. 1.8s: Diagonal hand-drawn charcoal stroke reveal (`parchment` -> `lineart`)
          * 1.8s .. target_dur: Smooth transition into the full Sumi-e & Gold Master with dynamic
            storyboard camera drift across the visual metaphor (`Left -> Right` or `Right -> Left`)
            inside the 75% gold-framed window while the 25% 7D studio revolves behind it!
    """
    prefix = TEMP_DIR / f"plate_{out_mp4.stem}"
    p_jpg, l_jpg, m_jpg = build_sketch_layers_with_banner(sketch_png, banner_text, prefix)

    frames = max(45, int(round(target_dur * 30)) + 4)
    d_draw = min(2.10, round(target_dur * 0.28, 2))
    d_main = max(2.50, round(target_dur - d_draw + 0.65, 2))
    f_draw = max(20, int(round(d_draw * 30)) + 2)
    f_main = max(30, int(round(d_main * 30)) + 4)

    bg_x = (
        f"(iw-1920)*(0.10+0.80*(on/{frames}))"
        if orbit_dir >= 0
        else f"(iw-1920)*(0.90-0.80*(on/{frames}))"
    )
    fg_x = (
        f"(iw-iw/zoom)*(0.12+0.76*(on/{f_main}))"
        if pan_dir >= 0
        else f"(iw-iw/zoom)*(0.88-0.76*(on/{f_main}))"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", "1.0", "-i", str(p_jpg),
        "-loop", "1", "-t", "1.0", "-i", str(l_jpg),
        "-loop", "1", "-t", "1.0", "-i", str(m_jpg),
        "-loop", "1", "-t", "1.0", "-i", str(PILOT_STAGE_JPG),
        "-i", str(audio_wav),
        "-loop", "1", "-t", f"{target_dur + 0.30:.3f}", "-i", str(overlay_png),
    ]

    fc = [
        # Revolving 25% Studio Background
        f"[3:v]scale=2140:1204:force_original_aspect_ratio=increase,crop=2140:1204,"
        f"zoompan=z='1.00':x='{bg_x}':y='(ih-1080)*(0.52-0.14*sin(PI*on/{frames}))':d={frames}:s=1920x1080:fps=30,"
        f"trim=0:{target_dur:.3f},setpts=PTS-STARTPTS,"
        "eq=brightness=-0.03:saturation=0.98,vignette=PI/9,setsar=1,format=yuv420p[bg]",

        # Phase 1: Parchment -> Charcoal Lineart diagonal drawing wipe
        f"[0:v]scale=1560:874,zoompan=z='1.02':x='(iw-iw/zoom)*0.20':y='(ih-ih/zoom)*0.45':d={f_draw}:s=1432x802:fps=30,"
        f"trim=0:{d_draw:.3f},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[s_parch]",

        f"[1:v]scale=1560:874,zoompan=z='1.04':x='(iw-iw/zoom)*0.22':y='(ih-ih/zoom)*0.45':d={f_draw}:s=1432x802:fps=30,"
        f"trim=0:{d_draw:.3f},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[s_line]",

        f"[s_parch][s_line]xfade=transition=diagtl:duration={min(1.10, d_draw*0.65):.2f}:offset=0.18,setsar=1,format=yuv420p[s_phase1]",

        # Phase 2: Full Ink & Champagne-Gold Master panning across the Left->Right visual metaphor
        f"[2:v]scale=1660:930,zoompan=z='1.08+0.06*(on/{f_main})':x='{fg_x}':y='(ih-ih/zoom)*0.46':d={f_main}:s=1432x802:fps=30,"
        f"trim=0:{d_main:.3f},setpts=PTS-STARTPTS,eq=contrast=1.04:saturation=1.05,setsar=1,format=yuv420p[s_phase2]",

        f"[s_phase1][s_phase2]xfade=transition=fade:duration=0.55:offset={max(0.5, d_draw - 0.55):.2f},"
        f"trim=0:{target_dur:.3f},setpts=PTS-STARTPTS,"
        "pad=w=1440:h=810:x=4:y=4:color=#EBC670,setsar=1,format=yuv420p[fg]",

        "[bg][fg]overlay=240:135:shortest=1,format=yuv420p[comp]",

        f"[5:v]fade=t=in:st=0.15:d=0.25:alpha=1,fade=t=out:st={max(0.6, target_dur - 0.30):.2f}:d=0.25:alpha=1[ov]",
        "[comp][ov]overlay=0:0:format=auto,format=yuv420p[vout]",
    ]

    cmd += [
        "-filter_complex", ";".join(fc),
        "-map", "[vout]", "-map", "4:a:0",
        "-t", f"{target_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
        "-c:v", "libx264", "-profile:v", "high", "-preset", preset, "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return probe_duration(out_mp4)


def format_ass_time(sec: float) -> str:
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def append_two_line_events(
    events: list[tuple[float, float, str, str]],
    seg_start: float,
    rel_st: float,
    rel_en: float,
    seg_dur: float,
    style: str,
    lines: list[str],
):
    s_t = seg_start + rel_st
    e_t = min(seg_start + seg_dur - 0.05, seg_start + rel_en)
    if len(lines) == 1:
        events.append((s_t, e_t, style, lines[0]))
        return
    tot_c = sum(max(1, len(x)) for x in lines)
    mid_t = s_t + (e_t - s_t) * (len(lines[0]) / tot_c)
    events.append((s_t, max(s_t + 0.5, mid_t - 0.04), style, lines[0]))
    events.append((mid_t + 0.02, max(mid_t + 0.5, e_t), style, lines[1]))


def build_single_virtue_ass(ass_path: Path, events: list[tuple[float, float, str, str]]):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: CinemaWhite,DejaVu Sans,34,&H00FFFFFF,&H00FFFFFF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.2,0,3,11.0,0.0,2,56,56,26,1
Style: SageParchment,DejaVu Sans,34,&H00D4F4FF,&H00D4F4FF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.2,0,3,11.0,0.0,2,56,56,26,1
Style: BalaGold,DejaVu Sans,34,&H00B8F2FF,&H00B8F2FF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.2,0,3,11.0,0.0,2,56,56,26,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for s_t, e_t, style, txt in events:
        lines.append(f"Dialogue: 0,{format_ass_time(s_t)},{format_ass_time(e_t)},{style},,0,0,0,,{txt}")
    ass_path.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")


def build_contact_sheet_14(out_jpg: Path):
    """Renders a 1920x1260 showcase grid of all 14 Philosophical Concept & Metaphor Sketches (D1A..D7B)."""
    canvas = Image.new("RGB", (1920, 1260), (14, 16, 24))
    draw = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype(FONT_BOLD, 22)
    f_lbl = ImageFont.truetype(FONT_BOLD, 13)

    draw.text(
        (36, 16),
        "KARMIC GENIE SHOW • PILOT S01E00: 14 PHILOSOPHICAL CONCEPT & VISUAL METAPHOR SKETCHES (THIRUKKURAL • DHAMMAPADA • TAO/ANALECTS)",
        font=f_title,
        fill=(252, 222, 142),
    )

    items = []
    for spec in VIRTUE_SPECS:
        items.append((SKETCH_DIR / spec["sketch_a"], f"D{spec['num']}A • {spec['banner_a'].split('•')[-1].strip()}"))
        items.append((SKETCH_DIR / spec["sketch_b"], f"D{spec['num']}B • {spec['banner_b'].split('•')[-1].strip()}"))

    # 4 columns x 4 rows (14 cells)
    cw, ch = 456, 268
    for idx, (p, lbl) in enumerate(items):
        if not p.exists():
            continue
        col, row = idx % 4, idx // 4
        x0 = 24 + col * (cw + 16)
        y0 = 60 + row * (ch + 24)
        im = Image.open(p).convert("RGB").resize((cw, ch), Image.Resampling.LANCZOS)
        canvas.paste(im, (x0, y0))
        draw.rectangle([x0, y0, x0 + cw, y0 + ch], outline=(235, 198, 112), width=2)
        draw.rectangle([x0, y0 + ch - 26, x0 + cw, y0 + ch], fill=(10, 12, 20))
        draw.text((x0 + 8, y0 + ch - 21), lbl[:54], font=f_lbl, fill=(255, 232, 165))

    canvas.save(out_jpg, quality=92)
    print(f"🖼️ Saved 14-Panel Philosophical Concept Sketch Contact Sheet: {out_jpg}", flush=True)


def main():
    import sys
    sys.path.insert(0, str(REPO_DIR / "pipeline"))
    import build_s01e00_pilot_7d_way as pilot_mod

    VIRTUES_30S_DIR.mkdir(parents=True, exist_ok=True)
    ANIM_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    saved_map = json.loads(CLIP_MAP_JSON.read_text(encoding="utf-8"))["clips"]
    clip_map = {k: Path(v) for k, v in saved_map.items()}

    sheet_jpg = SKETCH_DIR / "7d_eastern_philosophers_contact_sheet.jpg"
    build_contact_sheet_14(sheet_jpg)

    for spec in VIRTUE_SPECS:
        vid_id = spec["id"]
        num = spec["num"]
        print(f"\n🎨 Building 100%-Spoken 30.0s Virtue Video for Dimension {num}: {spec['title']}...", flush=True)

        # 1. Beat 1: Adult Host @Me in Studio
        host_mp4 = Path(clip_map[spec["host_key"]])
        sp_st, sp_en, raw_dur = detect_speech_bounds_rms(host_mp4, (0.25, 7.65))
        h_out = TEMP_DIR / f"v30_{vid_id}_01_host.mp4"
        h_entry = {
            "sid": f"H_{vid_id}",
            "src": host_mp4,
            "layout": "full",
            "orbit_dir": 1 if num % 2 == 1 else -1,
            "cu_zoom": 1.28,
            "cu_fx": 0.50,
            "cu_fy": 0.22,
            "voice": "human",
            "overlay": spec["overlay"],
            "lines": spec["host_lines"],
        }
        h_dur, h_rel_st, h_rel_en = pilot_mod.render_pilot_shot(h_entry, sp_st, sp_en, raw_dur, h_out, preset="fast")

        # 2. Beat 3: 4yo Bala-Rishi @Me in Studio
        bala_mp4 = Path(clip_map[spec["bala_key"]])
        b_sp_st, b_sp_en, b_raw_dur = detect_speech_bounds_rms(bala_mp4, (0.25, 7.65))
        b_out = TEMP_DIR / f"v30_{vid_id}_04_bala.mp4"
        b_entry = {
            "sid": f"B_{vid_id}",
            "src": bala_mp4,
            "layout": "full",
            "orbit_dir": -1 if num % 2 == 1 else 1,
            "cu_zoom": 1.22,
            "cu_fx": 0.54,
            "cu_fy": 0.20,
            "voice": "bala_genie",
            "overlay": spec["overlay"],
            "lines": spec["bala_lines"],
        }
        b_dur, b_rel_st, b_rel_en = pilot_mod.render_pilot_shot(b_entry, b_sp_st, b_sp_en, b_raw_dur, b_out, preset="fast")

        # 3. Compute exact durations for Spoken Philosophical Sketch Beats 2A & 2B so total == 30.00s!
        rem_dur = max(12.0, round(30.00 - h_dur - b_dur, 3))
        dur_a = round(rem_dur * 0.50, 3)
        dur_b = max(5.5, round(rem_dur - dur_a, 3))

        wav_a = TEMP_DIR / f"aud_{vid_id}_2a.wav"
        wav_b = TEMP_DIR / f"aud_{vid_id}_2b.wav"
        override_a = Path(clip_map[spec["beat_a_clip_key"]]) if spec.get("beat_a_clip_key") else None

        a_rel_st, a_rel_en = synthesize_philosophical_narration_wav(spec["beat_a_tts"], dur_a, wav_a, clip_override=override_a)
        b2_rel_st, b2_rel_en = synthesize_philosophical_narration_wav(spec["beat_b_tts"], dur_b, wav_b, clip_override=None)

        sketch_a_mp4 = ANIM_CLIPS_DIR / f"sketch_{vid_id}_2a.mp4"
        sketch_b_mp4 = ANIM_CLIPS_DIR / f"sketch_{vid_id}_2b.mp4"
        ov_png = OVERLAYS_DIR / spec["overlay"]

        d_2a = render_spoken_sketch_beat(
            sketch_png=SKETCH_DIR / spec["sketch_a"],
            banner_text=spec["banner_a"],
            overlay_png=ov_png,
            audio_wav=wav_a,
            target_dur=dur_a,
            orbit_dir=1,
            pan_dir=1,
            out_mp4=sketch_a_mp4,
            preset="fast",
        )
        d_2b = render_spoken_sketch_beat(
            sketch_png=SKETCH_DIR / spec["sketch_b"],
            banner_text=spec["banner_b"],
            overlay_png=ov_png,
            audio_wav=wav_b,
            target_dur=dur_b,
            orbit_dir=-1,
            pan_dir=-1,
            out_mp4=sketch_b_mp4,
            preset="fast",
        )

        # 4. Concatenate Beat 1 (Host) + Beat 2A (Spoken Sketch A) + Beat 2B (Spoken Sketch B) + Beat 3 (4yo Bala-Rishi)
        concat_txt = TEMP_DIR / f"concat_{vid_id}.txt"
        concat_txt.write_text(
            f"file '{h_out}'\nfile '{sketch_a_mp4}'\nfile '{sketch_b_mp4}'\nfile '{b_out}'\n",
            encoding="utf-8",
        )
        raw_30s = TEMP_DIR / f"raw_30s_{vid_id}.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
            "-c", "copy", str(raw_30s)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        tot_dur = probe_duration(raw_30s)

        # 5. Build single-line sequential BorderStyle=3 ASS subtitles synced across all 4 spoken beats
        ev: list[tuple[float, float, str, str]] = []
        t0 = 0.0
        append_two_line_events(ev, t0, h_rel_st, h_rel_en, h_dur, "CinemaWhite", spec["host_lines"])
        t0 += h_dur
        append_two_line_events(ev, t0, a_rel_st, a_rel_en, d_2a, "SageParchment", spec["beat_a_lines"])
        t0 += d_2a
        append_two_line_events(ev, t0, b2_rel_st, b2_rel_en, d_2b, "SageParchment", spec["beat_b_lines"])
        t0 += d_2b
        append_two_line_events(ev, t0, b_rel_st, b_rel_en, b_dur, "BalaGold", spec["bala_lines"])

        ass_p = TEMP_DIR / f"sub_{vid_id}.ass"
        build_single_virtue_ass(ass_p, ev)

        # 6. Mix with ducked 7D Theme Bed (`0.038` beneath continuous spoken dialogue!) and master to -14 LUFS
        out_30s = VIRTUES_30S_DIR / f"D{num}_{vid_id.split('_')[1].capitalize()}_30s_360p.mp4"
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(raw_30s),
            "-ss", f"{num * 6.0:.2f}", "-stream_loop", "-1", "-i", str(THEME_WAV),
            "-filter_complex", (
                f"[0:v]ass={ass_p},fade=t=in:st=0:d=0.30,fade=t=out:st={tot_dur-0.40:.2f}:d=0.35,"
                "scale=640:360:flags=lanczos[vout];"
                f"[1:a]atrim=0:{tot_dur:.3f},asetpts=PTS-STARTPTS,lowpass=f=9000,volume=0.038[bgm];"
                "[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
            ),
            "-map", "[vout]", "-map", "[aout]",
            "-t", "30.00",
            "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            "-r", "30",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart",
            str(out_30s)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        final_d = probe_duration(out_30s)
        print(
            f"   ✅ Saved {out_30s.name}: {final_d:.2f}s "
            f"(Host={h_dur:.2f}s + Spoken Sketch A={d_2a:.2f}s + Spoken Sketch B={d_2b:.2f}s + Bala-Rishi={b_dur:.2f}s)",
            flush=True,
        )


if __name__ == "__main__":
    main()
