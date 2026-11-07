#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Widescreen (`--resolution 360p` 640x360 Preview Default | `--resolution 1080p` 1920x1080 Master,
30fps, -14 LUFS) Theatrical Cinema Pilot Assembler for:
  Karmic Genie Show — Season 1, Episode 0 (Pilot: "The 7D Way — Pioneers of the New World")
  Outputs:
    - `renders/Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_360p.mp4`
    - `renders/Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_16x9.mp4`

Approved Sample 2 Dual-@Me Visual & Narrative Architecture:
  1. Adult Narrator/Host (`@Me` in tailored ivory-white bandhgala suit) explains the deep details,
     conscience triggers, and real-world philosophy of EVERY SINGLE VIRTUE (`D1..D7`, `H01..H09`).
  2. Sample 2 Awakened Karmic Genie (`4-Year-Old Bala-Rishi @Me` with cute topknot, sacred tilak,
     tiny rudraksha mala, ivory silk kurta, and golden-saffron angavastram stole beside the ornate
     golden Genie lamp — `assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg`) delivers the
     opening 7D Scale greeting (`flow_me_4yo_360p_01.mp4`) and luminous child-sage wisdom for ALL
     7 Virtues (`G01..G07`).
  3. Dedicated deep, unhurried time (`~3:45–4:15` across 30 shots) for all 7 Virtues (`D1..D7`),
     pairing Adult `@Me`, visual Conscience & Dharma parables (`B01..B03` + timeless human stories),
     all 7 individual holographic curved-glass overlays (`ov_d1_duty.png`..`ov_d7_destiny.png`),
     and `4-Year-Old Bala-Rishi @Me`.
  4. Multi-Camera Revolving Orbit -> Intimate Cinema Close-Up Cut on EVERY Full Studio Shot (`full`)
     with 100% fluid 30fps lip-sync (zero `zoompan` live-video freeze, zero `rubberband`, zero `tpad`).
"""

import argparse
import json
import re
import shutil
import subprocess
import wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
MASTERS_DIR = REPO_DIR / "assets" / "studio_v5_masters"
PILOT_STAGE_JPG = MASTERS_DIR / "v8_pilot_7d_scorecard_stage_16x9.jpg"
GENIE_BALA_JPG = MASTERS_DIR / "v9_genie_4yo_bala_rishi_16x9.jpg"
THEME_WAV = REPO_DIR / "assets" / "theme" / "official_karmic_genie_7d_theme_song.wav"
LOGO_JPG = REPO_DIR / "assets" / "logo" / "official_karmic_genie_show_logo.jpg"

PILOT_DIR = REPO_DIR / "episodes" / "S01E00_Pilot_The_7D_Way"
PILOT_CLIPS_ROOT = PILOT_DIR / "flow_s01e00_clips"
OVERLAYS_DIR = PILOT_DIR / "overlays_s01e00"
CLIP_MAP_JSON = PILOT_DIR / "pilot_clip_map.json"
QA_CONTACT_JPG = PILOT_DIR / "qa_s01e00_clips_contact_sheet.jpg"
TEMP_DIR = PILOT_DIR / "temp_s01e00_pilot_build"

ARTIFACT_DIR = Path("/home/shishyan/.gemini/antigravity/brain/b55fc9ea-1a2e-45b9-8d71-a53ee11caf0c")
BALA_SAMPLE2_MP4 = ARTIFACT_DIR / "scratch" / "flow_me_4yo_samples" / "flow_me_4yo_360p_01.mp4"

EP01_DIR = REPO_DIR / "episodes" / "S01E01_Employees_vs_Tech_CEO"
V3_CLIPS_ROOT = EP01_DIR / "flow_v3_interactive_clips"
V1_CLIPS_ROOT = EP01_DIR / "flow_16x9_clips"

OUT_360P_MP4 = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_360p.mp4"
OUT_16X9_MP4 = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_16x9.mp4"
ARTIFACT_360P_MP4 = ARTIFACT_DIR / "Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_360p.mp4"
ARTIFACT_16X9_MP4 = ARTIFACT_DIR / "Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_16x9.mp4"

FORBIDDEN_NAMES = (
    "marcus", "arjun", "elena", "mateo", "kenji", "heinrich", "kavitha",
    "amazon", "google", "alphabet", "microsoft", "meta", "apple", "oracle",
    "dell", "cisco", "intel", "ups", "tcs", "infosys", "wipro", "hsbc", "citi",
)

FORBIDDEN_BLAME_PHRASES = (
    "record profit", "corporate greed", "heartless",
)

NON_SPEECH_HALLUCINATIONS = {"applause", "[applause]", "(applause)", "music", "[music]"}

# Spoken-clip keyword signatures across all 4 spoken batches (16 clips: H01..H09 + G01..G07):
SPOKEN_BATCH_SPECS = {
    "b1_host_compass_and_d1_d2": [
        ("H01_Host_Pilot_35_Rule", ["welcome", "score", "situation", "ten", "thirty", "seventy", "course"]),
        ("H02_Host_D1_Duty_Definition", ["first", "duty", "never", "office", "job", "triggers", "undone"]),
        ("H03_Host_D1_Silenced_Conscience", ["thief", "first", "alcohol", "neglect", "silent", "draining", "empathy"]),
        ("H04_Host_D2_Dignity_Explain", ["second", "dignity", "unbought", "livelihood", "spine", "truth", "peace"]),
    ],
    "b2_host_d3_to_d7_details": [
        ("H05_Host_D3_Discipline_Explain", ["third", "discipline", "sovereign", "mastery", "senses", "tongue", "cravings", "screens", "enslave"]),
        ("H06_Host_D4_Dharma_Explain", ["fourth", "dharma", "vital", "organ", "banyan", "shade", "nourishment"]),
        ("H07_Host_D5_Devotion_Explain", ["fifth", "devotion", "connectedness", "parents", "spouse", "children", "undivided", "leftovers"]),
        ("H08_Host_D6_Divine_Explain", ["sixth", "gratitude", "divine", "humility", "architect", "harmonized", "para"]),
        ("H09_Host_D7_Destiny_Explain", ["seventh", "destiny", "align", "thirty", "flower", "pioneer"]),
    ],
    "b3_bala_rishi_4yo_virtues_1": [
        ("G01_Bala_D1_Duty", ["one", "duty", "drink", "whisper", "conscience", "care", "listen"]),
        ("G02_Bala_D2_Dignity", ["two", "dignity", "stand", "tall", "paycheck", "title", "trading", "respect"]),
        ("G03_Bala_D3_Discipline", ["three", "discipline", "rule", "habits", "sleep", "senses", "morning", "bright"]),
        ("G04_Bala_D4_Dharma", ["four", "dharma", "mango", "sharing", "shade", "fruit", "creature", "mother"]),
    ],
    "b4_bala_rishi_4yo_virtues_2": [
        ("G05_Bala_D5_Devotion", ["five", "devotion", "phone", "tonight", "hug", "parents", "children", "tight"]),
        ("G06_Bala_D6_Divine", ["six", "divine", "thank", "sunrise", "architect", "body", "mind"]),
        ("G07_Bala_D7_Destiny_Blessing", ["seven", "destiny", "score", "thirty", "shine", "pioneer"]),
    ],
}


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
    to detect exact `(sp_st, sp_en)` speech timestamps (filtering non-speech tags).
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
    if words and (words[-1][1] - words[0][0]) >= 1.8:
        sp_st = float(words[0][0])
        sp_en = float(words[-1][1])
    else:
        sp_st, sp_en = float(fallback_bounds[0]), min(dur, float(fallback_bounds[1]))

    return (full_txt, sp_st, sp_en, dur)


def sample_rgb_stats(mp4_path: Path, t_sec: float) -> tuple[float, float, float]:
    """Extracts a tiny 160x90 frame at `t_sec` and returns mean `(R, G, B)` in `0..255`."""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    png = TEMP_DIR / f"rgb_{mp4_path.stem}_{int(t_sec*100):04d}.png"
    dur = probe_duration(mp4_path)
    ts = max(0.1, min(dur - 0.15, t_sec))
    subprocess.run([
        "ffmpeg", "-y", "-ss", f"{ts:.2f}", "-i", str(mp4_path),
        "-frames:v", "1", "-vf", "scale=160:90", str(png)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    arr = np.asarray(Image.open(png).convert("RGB"), dtype=np.float32)
    return (float(arr[:, :, 0].mean()), float(arr[:, :, 1].mean()), float(arr[:, :, 2].mean()))


def resolve_pilot_clips(model, force_rescan: bool = False) -> dict[str, Path]:
    """
    Resolves all 19 newly generated Pilot clips (`H01..H09`, `G01..G07`, `B01..B03`) across
    `b1_host_compass_and_d1_d2`, `b2_host_d3_to_d7_details`, `b3_bala_rishi_4yo_virtues_1`,
    `b4_bala_rishi_4yo_virtues_2`, and `b5_conscience_parables`, plus `G00_Bala_Opening_Sample2`,
    and persists `episodes/S01E00_Pilot_The_7D_Way/pilot_clip_map.json`.
    """
    expected_keys = {
        "G00_Bala_Opening_Sample2",
        "H01_Host_Pilot_35_Rule", "H02_Host_D1_Duty_Definition",
        "H03_Host_D1_Silenced_Conscience", "H04_Host_D2_Dignity_Explain",
        "H05_Host_D3_Discipline_Explain", "H06_Host_D4_Dharma_Explain",
        "H07_Host_D5_Devotion_Explain", "H08_Host_D6_Divine_Explain",
        "H09_Host_D7_Destiny_Explain",
        "G01_Bala_D1_Duty", "G02_Bala_D2_Dignity", "G03_Bala_D3_Discipline", "G04_Bala_D4_Dharma",
        "G05_Bala_D5_Devotion", "G06_Bala_D6_Divine", "G07_Bala_D7_Destiny_Blessing",
        "B01_Thief_Conscience_Alert", "B02_Numbing_Conscience_To_Compassion", "B03_Fruit_Bearing_Banyan_Tree",
    }

    if CLIP_MAP_JSON.exists() and not force_rescan:
        saved = json.loads(CLIP_MAP_JSON.read_text(encoding="utf-8"))
        clips_dict = saved.get("clips", {})
        if expected_keys.issubset(clips_dict.keys()) and all(Path(clips_dict[k]).exists() for k in expected_keys):
            return {k: Path(v) for k, v in clips_dict.items()}

    if not BALA_SAMPLE2_MP4.exists():
        raise FileNotFoundError(f"Missing Sample 2 4yo Bala-Rishi greeting clip: {BALA_SAMPLE2_MP4}")

    resolved: dict[str, str] = {"G00_Bala_Opening_Sample2": str(BALA_SAMPLE2_MP4)}
    diagnostics: dict[str, dict] = {
        "G00_Bala_Opening_Sample2": {"file": BALA_SAMPLE2_MP4.name, "note": "Approved Sample 2 4yo Bala-Rishi"}
    }

    # 1. Resolve all 16 spoken clips across `b1`..`b4`
    for batch_id, role_specs in SPOKEN_BATCH_SPECS.items():
        b_dir = PILOT_CLIPS_ROOT / batch_id
        mp4s = sorted(b_dir.glob(f"{batch_id}_*.mp4")) if b_dir.exists() else []
        if not mp4s and b_dir.exists():
            mp4s = sorted(p for p in b_dir.glob("*.mp4") if not p.name.startswith("raw_"))
        if len(mp4s) < len(role_specs):
            raise FileNotFoundError(
                f"Batch '{batch_id}' incomplete in {b_dir}: found {len(mp4s)}/{len(role_specs)} MP4s"
            )

        clip_txts = {}
        for mp4 in mp4s:
            txt, sp_st, sp_en, dur = transcribe_clip_whisper(mp4, model, (0.2, 7.6))
            clip_txts[mp4] = (txt, sp_st, sp_en, dur)

        # Greedy highest-score one-to-one keyword assignment
        pairs = []
        for role_key, kw_list in role_specs:
            for mp4 in mp4s:
                txt = clip_txts[mp4][0]
                score = sum(1 for kw in kw_list if kw in txt)
                pairs.append((score, role_key, mp4))
        pairs.sort(key=lambda x: x[0], reverse=True)

        assigned_roles = set()
        assigned_mp4s = set()
        for score, role_key, mp4 in pairs:
            if role_key not in assigned_roles and mp4 not in assigned_mp4s:
                assigned_roles.add(role_key)
                assigned_mp4s.add(mp4)
                resolved[role_key] = str(mp4)
                diagnostics[role_key] = {
                    "file": mp4.name,
                    "keyword_hits": score,
                    "transcript": clip_txts[mp4][0],
                }

        rem_roles = [rk for rk, _ in role_specs if rk not in assigned_roles]
        rem_mp4s = [m for m in mp4s if m not in assigned_mp4s]
        for rk, m in zip(rem_roles, rem_mp4s):
            resolved[rk] = str(m)
            diagnostics[rk] = {"file": m.name, "keyword_hits": 0, "transcript": clip_txts[m][0]}

    # 2. Resolve visual parable batch (`b5_conscience_parables`: B01, B02, B03)
    b5_dir = PILOT_CLIPS_ROOT / "b5_conscience_parables"
    b5_mp4s = sorted(b5_dir.glob("b5_conscience_parables_*.mp4")) if b5_dir.exists() else []
    if not b5_mp4s and b5_dir.exists():
        b5_mp4s = sorted(p for p in b5_dir.glob("*.mp4") if not p.name.startswith("raw_"))
    if len(b5_mp4s) < 3:
        raise FileNotFoundError(f"Batch 'b5_conscience_parables' incomplete in {b5_dir}: found {len(b5_mp4s)}/3 MP4s")

    # First check if Flow's manifest labels contain prompt keywords (`lockbox`, `amber`/`curtains`, `banyan`/`orchard`)
    manifest_p = b5_dir / "b5_conscience_parables_manifest.json"
    label_map: dict[str, str] = {}
    if manifest_p.exists():
        try:
            for item in json.loads(manifest_p.read_text(encoding="utf-8")):
                label_map[item.get("file", "")] = item.get("label", "").lower()
        except Exception:
            label_map = {}

    b5_stats = {}
    for mp4 in b5_mp4s[:3]:
        r0, g0, b0 = sample_rgb_stats(mp4, 0.9)
        rm, gm, bm = sample_rgb_stats(mp4, 3.8)
        r1, g1, b1 = sample_rgb_stats(mp4, 6.6)
        lum0 = 0.299 * r0 + 0.587 * g0 + 0.114 * b0
        lumm = 0.299 * rm + 0.587 * gm + 0.114 * bm
        lum1 = 0.299 * r1 + 0.587 * g1 + 0.114 * b1
        mean_lum = (lum0 + lumm + lum1) / 3.0
        foliage_score = ((g0 + gm + g1) / 3.0) + 0.45 * mean_lum - 0.20 * ((b0 + bm + b1) / 3.0)
        dawn_jump = lum1 - lum0
        lbl = label_map.get(mp4.name, "")
        if "banyan" in lbl or "orchard" in lbl:
            foliage_score += 500.0
        if "curtain" in lbl or "amber" in lbl or "father" in lbl:
            dawn_jump += 500.0
        b5_stats[mp4] = {
            "lum0": round(lum0, 1),
            "lumm": round(lumm, 1),
            "lum1": round(lum1, 1),
            "mean_lum": round(mean_lum, 1),
            "foliage_score": round(foliage_score, 1),
            "dawn_jump": round(dawn_jump, 1),
        }

    b03_mp4 = max(b5_stats.keys(), key=lambda m: b5_stats[m]["foliage_score"])
    rem_b5 = [m for m in b5_stats.keys() if m != b03_mp4]
    b02_mp4 = max(rem_b5, key=lambda m: b5_stats[m]["dawn_jump"] + 0.35 * b5_stats[m]["lum1"])
    b01_mp4 = [m for m in rem_b5 if m != b02_mp4][0]

    resolved["B01_Thief_Conscience_Alert"] = str(b01_mp4)
    resolved["B02_Numbing_Conscience_To_Compassion"] = str(b02_mp4)
    resolved["B03_Fruit_Bearing_Banyan_Tree"] = str(b03_mp4)
    for rk, m in [
        ("B01_Thief_Conscience_Alert", b01_mp4),
        ("B02_Numbing_Conscience_To_Compassion", b02_mp4),
        ("B03_Fruit_Bearing_Banyan_Tree", b03_mp4),
    ]:
        diagnostics[rk] = {"file": m.name, **b5_stats[m]}

    payload = {"verified": False, "clips": resolved, "diagnostics": diagnostics}
    CLIP_MAP_JSON.parent.mkdir(parents=True, exist_ok=True)
    CLIP_MAP_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"✅ Resolved & saved all 20 Pilot clips -> {CLIP_MAP_JSON}", flush=True)
    for k, d in diagnostics.items():
        print(f"   • {k:36s} <- {d['file']} | {d}", flush=True)
    return {k: Path(v) for k, v in resolved.items()}


def render_qa_contact_sheet(clip_map: dict[str, Path], out_jpg: Path = QA_CONTACT_JPG) -> Path:
    """
    Renders a 4x5 visual QA contact sheet (`1920x1350`) showing all 20 resolved Pilot clips
    (`Sample 2` + `H01..H09` + `G01..G07` + `B01..B03`) so Adult `@Me` face identity, `4-Year-Old
    Bala-Rishi @Me` likeness, and `B01..B03` parable order can be inspected in one glance!
    """
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    ordered_keys = [
        "G00_Bala_Opening_Sample2",
        "H01_Host_Pilot_35_Rule",
        "H02_Host_D1_Duty_Definition",
        "H03_Host_D1_Silenced_Conscience",
        "H04_Host_D2_Dignity_Explain",
        "H05_Host_D3_Discipline_Explain",
        "H06_Host_D4_Dharma_Explain",
        "H07_Host_D5_Devotion_Explain",
        "H08_Host_D6_Divine_Explain",
        "H09_Host_D7_Destiny_Explain",
        "G01_Bala_D1_Duty",
        "G02_Bala_D2_Dignity",
        "G03_Bala_D3_Discipline",
        "G04_Bala_D4_Dharma",
        "G05_Bala_D5_Devotion",
        "G06_Bala_D6_Divine",
        "G07_Bala_D7_Destiny_Blessing",
        "B01_Thief_Conscience_Alert",
        "B02_Numbing_Conscience_To_Compassion",
        "B03_Fruit_Bearing_Banyan_Tree",
    ]
    cell_w, cell_h = 480, 270
    sheet = Image.new("RGB", (cell_w * 4, cell_h * 5), (14, 16, 24))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)

    for idx, key in enumerate(ordered_keys):
        mp4 = clip_map[key]
        dur = probe_duration(mp4)
        p1 = TEMP_DIR / f"qa20_{idx:02d}_a.png"
        p_mid = TEMP_DIR / f"qa20_{idx:02d}_m.png"
        p2 = TEMP_DIR / f"qa20_{idx:02d}_b.png"
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{min(dur-0.2, 1.0):.2f}", "-i", str(mp4),
            "-frames:v", "1", "-vf", "scale=128:72", str(p1)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{min(dur-0.2, 3.6):.2f}", "-i", str(mp4),
            "-frames:v", "1", "-vf", f"scale={cell_w}:{cell_h}", str(p_mid)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{min(dur-0.2, 6.3):.2f}", "-i", str(mp4),
            "-frames:v", "1", "-vf", "scale=128:72", str(p2)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        col, row = idx % 4, idx // 4
        x0, y0 = col * cell_w, row * cell_h
        sheet.paste(Image.open(p_mid).convert("RGB"), (x0, y0))
        sheet.paste(Image.open(p1).convert("RGB"), (x0 + 4, y0 + cell_h - 76))
        sheet.paste(Image.open(p2).convert("RGB"), (x0 + cell_w - 132, y0 + cell_h - 76))
        draw.rectangle([x0, y0, x0 + cell_w, y0 + 24], fill=(8, 10, 20))
        draw.text((x0 + 6, y0 + 4), f"{key} ({mp4.name})", font=font, fill=(255, 220, 120))

    sheet.save(out_jpg, format="JPEG", quality=90)
    print(f"🖼️ Saved 20-clip Pilot QA contact sheet: {out_jpg}", flush=True)
    return out_jpg


def build_pilot_shot_ledger(cm: dict[str, Path]) -> list[dict]:
    """
    Constructs the rich, unhurried 30-shot Theatrical Cinema Pilot Shot Ledger (`~3:50–4:10` runtime)
    dedicating deep time to EVERY SINGLE VIRTUE (`D1..D7`), pairing Adult Narrator `@Me` (`H01..H09`),
    visual parables (`B01..B03` + human stories), all 7 individual holographic overlays
    (`ov_d1_duty.png`..`ov_d7_destiny.png`), and `4-Year-Old Bala-Rishi @Me` (`Sample 2` + `G01..G07`).
    """
    return [
        # === PROLOGUE: THE GRAND QUESTION, 35/70 COMPASS & AWAKENING THE BALA-RISHI ===
        {
            "sid": "01_Welcome_Circle",
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
            "sid": "02_Host_Overgrown_Forest",
            "src": V3_CLIPS_ROOT / "v3_7d_philosophy_me" / "v3_phil_02.mp4",
            "hint_sp": (0.00, 7.54),
            "layout": "full",
            "orbit_dir": -1,
            "cu_zoom": 1.30,
            "cu_fx": 0.44,
            "cu_fy": 0.22,
            "voice": "human",
            "overlay": "ov_p00_compass.png",
            "lines": [
                "Earning fifty years just to survive is an overgrown forest yielding no fruit—",
                "industries, like highways, are pathways, never your destination!",
            ],
        },
        {
            "sid": "03_Host_Pilot_35_Rule",
            "src": cm["H01_Host_Pilot_35_Rule"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": 1,
            "cu_zoom": 1.28,
            "cu_fx": 0.50,
            "cu_fy": 0.22,
            "voice": "human",
            "overlay": "ov_p00_compass.png",
            "lines": [
                "Welcome to The Seven D Way! Score every situation from one to ten across seven virtues—",
                "below thirty-five out of seventy, change the course of your life!",
            ],
        },
        {
            "sid": "04_Stage_Glass_35_WhipPan",
            "src": PILOT_STAGE_JPG,
            "layout": "glass_whip_pan",
            "visual_dur": 3.40,
            "voice": "human",
            "overlay": None,
            "lines": [
                "Below 35 / 70: Conscience Silenced  •  50–70 / 70: Pioneer of the New World",
            ],
        },
        {
            "sid": "05_Summon_Bala_Rishi_Genie",
            "src": V1_CLIPS_ROOT / "topup_clean" / "plate_s4_03_punchline.mp4",
            "image_src": PILOT_STAGE_JPG,
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
            "sid": "06_Reveal_4yo_Bala_Rishi",
            "src": PILOT_STAGE_JPG,
            "dst_img": GENIE_BALA_JPG,
            "layout": "image_dissolve",
            "visual_dur": 2.20,
            "voice": "bala_genie",
            "overlay": None,
            "lines": [],
        },
        {
            "sid": "07_Bala_Opening_7D_Scale",
            "src": cm["G00_Bala_Opening_Sample2"],
            "hint_sp": (0.78, 7.48),
            "layout": "full",
            "orbit_dir": 1,
            "cu_zoom": 1.22,
            "cu_fx": 0.54,
            "cu_fy": 0.20,
            "voice": "bala_genie",
            "overlay": "ov_p00_compass.png",
            "lines": [
                "Earn with Dignity and practice Discipline—",
                "score your life on the 7D scale!",
            ],
        },

        # === VIRTUE 1: D1 DUTY (CONSCIENCE TRIGGER VS. OFFICE JOB) ===
        {
            "sid": "08_Host_D1_Duty_Definition",
            "src": cm["H02_Host_D1_Duty_Definition"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": -1,
            "cu_zoom": 1.28,
            "cu_fx": 0.50,
            "cu_fy": 0.22,
            "voice": "human",
            "overlay": "ov_d1_duty.png",
            "lines": [
                "First is Duty. Duty is never your office job—",
                "Duty is the task that triggers guilt in your conscience when you leave it undone!",
            ],
        },
        {
            "sid": "09_Parable_Thief_Conscience_PiP",
            "src": cm["B01_Thief_Conscience_Alert"],
            "layout": "pip75_visual_beat",
            "visual_ss": 0.25,
            "visual_dur": 5.80,
            "orbit_dir": 1,
            "pip_zoom": 1.26,
            "pip_fx": 0.50,
            "pip_fy": 0.38,
            "voice": "human",
            "overlay": None,
            "lines": [
                "Every soul is born with a sacred watchman: the inner alarm of Conscience.",
                "Step back from shadow into light the moment your conscience speaks.",
            ],
        },
        {
            "sid": "10_Host_D1_Silenced_Conscience",
            "src": cm["H03_Host_D1_Silenced_Conscience"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": 1,
            "cu_zoom": 1.28,
            "cu_fx": 0.50,
            "cu_fy": 0.22,
            "voice": "human",
            "overlay": "ov_d1_duty.png",
            "lines": [
                "A thief feels conscience guilt the first few times—drown that trigger with alcohol",
                "or neglect, and conscience goes silent, draining our world of empathy!",
            ],
        },
        {
            "sid": "11_Parable_Awakened_Empathy_PiP",
            "src": cm["B02_Numbing_Conscience_To_Compassion"],
            "layout": "pip75_visual_beat",
            "visual_ss": 0.25,
            "visual_dur": 5.80,
            "orbit_dir": -1,
            "pip_zoom": 1.24,
            "pip_fx": 0.50,
            "pip_fy": 0.36,
            "voice": "bala_genie",
            "overlay": None,
            "lines": [
                "Push away whatever numbs your inner guilt—",
                "open the curtains to morning light, and awaken living compassion!",
            ],
        },
        {
            "sid": "12_Bala_D1_Duty",
            "src": cm["G01_Bala_D1_Duty"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": -1,
            "cu_zoom": 1.22,
            "cu_fx": 0.54,
            "cu_fy": 0.20,
            "voice": "bala_genie",
            "overlay": "ov_d1_duty.png",
            "lines": [
                "Dimension One is Duty! Never drink away the whisper of your conscience—",
                "when your heart says care for someone today, listen right away!",
            ],
        },

        # === VIRTUE 2: D2 DIGNITY (UNBOUGHT SELF-RESPECT) ===
        {
            "sid": "13_Host_D2_Dignity_Explain",
            "src": cm["H04_Host_D2_Dignity_Explain"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": 1,
            "cu_zoom": 1.28,
            "cu_fx": 0.50,
            "cu_fy": 0.22,
            "voice": "human",
            "overlay": "ov_d2_dignity.png",
            "lines": [
                "Second is Dignity—unbought self-respect! Earn your livelihood honestly",
                "by building real value, never by selling your spine, your truth, or your peace!",
            ],
        },
        {
            "sid": "14_Bala_D2_Dignity",
            "src": cm["G02_Bala_D2_Dignity"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": -1,
            "cu_zoom": 1.22,
            "cu_fx": 0.54,
            "cu_fy": 0.20,
            "voice": "bala_genie",
            "overlay": "ov_d2_dignity.png",
            "lines": [
                "Dimension Two is Dignity! Stand tall with an honest heart—",
                "no paycheck or title is ever worth trading away your self-respect!",
            ],
        },

        # === VIRTUE 3: D3 DISCIPLINE (MASTERY OVER SENSES & CLOCK) ===
        {
            "sid": "15_Host_D3_Discipline_Explain",
            "src": cm["H05_Host_D3_Discipline_Explain"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": 1,
            "cu_zoom": 1.28,
            "cu_fx": 0.50,
            "cu_fy": 0.22,
            "voice": "human",
            "overlay": "ov_d3_discipline.png",
            "lines": [
                "Third is Discipline—sovereign mastery over your senses, tongue, and clock,",
                "so impulsive cravings and midnight screens never enslave your mind!",
            ],
        },
        {
            "sid": "16_Parable_Five_Pagers_Imbalance_PiP",
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
        {
            "sid": "17_Bala_D3_Discipline",
            "src": cm["G03_Bala_D3_Discipline"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": 1,
            "cu_zoom": 1.22,
            "cu_fx": 0.54,
            "cu_fy": 0.20,
            "voice": "bala_genie",
            "overlay": "ov_d3_discipline.png",
            "lines": [
                "Dimension Three is Discipline! Rule your habits, your sleep, and your senses",
                "every morning so your mind stays free and bright!",
            ],
        },

        # === VIRTUE 4: D4 DHARMA (FRUIT-BEARING TREE IN EARTH'S LIVING BODY) ===
        {
            "sid": "18_Host_D4_Dharma_Explain",
            "src": cm["H06_Host_D4_Dharma_Explain"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": -1,
            "cu_zoom": 1.28,
            "cu_fx": 0.50,
            "cu_fy": 0.22,
            "voice": "human",
            "overlay": "ov_d4_dharma.png",
            "lines": [
                "Fourth is Dharma—living as a vital organ in Earth's body,",
                "like a fruit-bearing banyan tree offering shade and nourishment to all!",
            ],
        },
        {
            "sid": "19_Parable_Fruit_Bearing_Banyan_PiP",
            "src": cm["B03_Fruit_Bearing_Banyan_Tree"],
            "layout": "pip75_visual_beat",
            "visual_ss": 0.25,
            "visual_dur": 5.80,
            "orbit_dir": 1,
            "pip_zoom": 1.22,
            "pip_fx": 0.50,
            "pip_fy": 0.40,
            "voice": "bala_genie",
            "overlay": None,
            "lines": [
                "No tree stands in nature merely to hoard sunlight for itself—",
                "a purposeful life bears sweet fruit and cooling shade for others.",
            ],
        },
        {
            "sid": "20_Bala_D4_Dharma",
            "src": cm["G04_Bala_D4_Dharma"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": -1,
            "cu_zoom": 1.22,
            "cu_fx": 0.54,
            "cu_fy": 0.20,
            "voice": "bala_genie",
            "overlay": "ov_d4_dharma.png",
            "lines": [
                "Dimension Four is Dharma! Be like a sweet mango tree",
                "sharing shade and fruit with every creature on Mother Earth!",
            ],
        },

        # === VIRTUE 5: D5 DEVOTION (UNDIVIDED HEART AT HOME TODAY) ===
        {
            "sid": "21_Host_D5_Devotion_Explain",
            "src": cm["H07_Host_D5_Devotion_Explain"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": 1,
            "cu_zoom": 1.28,
            "cu_fx": 0.50,
            "cu_fy": 0.22,
            "voice": "human",
            "overlay": "ov_d5_devotion.png",
            "lines": [
                "Fifth is Devotion—true connectedness at home! Give your aging parents,",
                "spouse, and children your warm, undivided presence today, never exhausted leftovers!",
            ],
        },
        {
            "sid": "22_Parable_Home_Reunion_PiP",
            "src": V1_CLIPS_ROOT / "batch_02_scene1_sf_mysuru" / "batch_02_scene1_sf_mysuru_03.mp4",
            "broll_mp4": V1_CLIPS_ROOT / "batch_04_scene3_tokyo_munich_coimbatore" / "batch_04_scene3_tokyo_munich_coimbatore_01.mp4",
            "broll_ss": 2.10,
            "broll_dur": 2.50,
            "hint_sp": (0.92, 7.60),
            "layout": "pip75_broll_cut",
            "orbit_dir": -1,
            "voice": "human",
            "overlay": None,
            "lines": [
                "Millions of us work outside our home countries—",
                "telling ourselves we left just briefly to earn dollars.",
            ],
        },
        {
            "sid": "23_Bala_D5_Devotion",
            "src": cm["G05_Bala_D5_Devotion"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": 1,
            "cu_zoom": 1.22,
            "cu_fx": 0.54,
            "cu_fy": 0.20,
            "voice": "bala_genie",
            "overlay": "ov_d5_devotion.png",
            "lines": [
                "Dimension Five is Devotion! Put down your phone tonight,",
                "hug your parents and children tight, and give them your whole heart!",
            ],
        },

        # === VIRTUE 6: D6 DIVINE (GRATITUDE TO THE GRAND ARCHITECT) ===
        {
            "sid": "24_Host_Body_Mind_Soul_ParaSoul",
            "src": V3_CLIPS_ROOT / "v3_grand_design" / "v3_gd_01.mp4",
            "hint_sp": (0.18, 7.70),
            "layout": "full",
            "orbit_dir": -1,
            "cu_zoom": 1.36,
            "cu_fx": 0.64,
            "cu_fy": 0.34,
            "voice": "human",
            "overlay": "ov_d6_divine.png",
            "lines": [
                "Just as human cells renew to serve mind, soul, and para-soul—",
                "every company and career shift serves a grander design!",
            ],
        },
        {
            "sid": "25_Host_D6_Divine_Explain",
            "src": cm["H08_Host_D6_Divine_Explain"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": 1,
            "cu_zoom": 1.28,
            "cu_fx": 0.50,
            "cu_fy": 0.22,
            "voice": "human",
            "overlay": "ov_d6_divine.png",
            "lines": [
                "Sixth is gratitude to the Divine—daily humility before the Grand Architect",
                "who harmonized your body, mind, soul, and para-soul!",
            ],
        },
        {
            "sid": "26_Bala_D6_Divine",
            "src": cm["G06_Bala_D6_Divine"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": -1,
            "cu_zoom": 1.22,
            "cu_fx": 0.54,
            "cu_fy": 0.20,
            "voice": "bala_genie",
            "overlay": "ov_d6_divine.png",
            "lines": [
                "Dimension Six is the Divine! Say thank you every sunrise",
                "to the Grand Architect of your body, mind, and soul!",
            ],
        },

        # === VIRTUE 7: D7 DESTINY & VIEWER'S FIRST 7D LIFE AUDIT ===
        {
            "sid": "27_Host_D7_Destiny_Explain",
            "src": cm["H09_Host_D7_Destiny_Explain"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": 1,
            "cu_zoom": 1.28,
            "cu_fx": 0.50,
            "cu_fy": 0.22,
            "voice": "human",
            "overlay": "ov_d7_destiny.png",
            "lines": [
                "Seventh is Destiny—when Duty, Dignity, Discipline, Dharma, Devotion, and Divine",
                "align above thirty-five, you flower into a Pioneer of the New World!",
            ],
        },
        {
            "sid": "28_Bala_D7_Destiny_Blessing",
            "src": cm["G07_Bala_D7_Destiny_Blessing"],
            "hint_sp": (0.25, 7.65),
            "layout": "full",
            "orbit_dir": -1,
            "cu_zoom": 1.22,
            "cu_fx": 0.54,
            "cu_fy": 0.20,
            "voice": "bala_genie",
            "overlay": "ov_p99_audit_blessing.png",
            "lines": [
                "Dimension Seven is your Destiny! Score above thirty-five across all Seven D's—",
                "and shine as a Pioneer of the New World!",
            ],
        },
        {
            "sid": "29_Stage_Return_Dissolve",
            "src": GENIE_BALA_JPG,
            "dst_img": PILOT_STAGE_JPG,
            "layout": "image_dissolve",
            "visual_dur": 1.80,
            "voice": "bala_genie",
            "overlay": None,
            "lines": [],
        },
        {
            "sid": "30_Host_Closing_Compass_Call",
            "src": V3_CLIPS_ROOT / "v3_7d_philosophy_me" / "v3_phil_03.mp4",
            "hint_sp": (0.00, 7.76),
            "layout": "full",
            "orbit_dir": 1,
            "cu_zoom": 1.28,
            "cu_fx": 0.48,
            "cu_fy": 0.20,
            "voice": "human",
            "overlay": "ov_p99_audit_blessing.png",
            "lines": [
                "Measure every question against all Seven D's—if your life ticks at least four,",
                "stay the course; otherwise, change your route!",
            ],
        },
    ]


def render_cold_open_pilot(out_mp4: Path, preset: str = "fast") -> float:
    """
    Builds the 3-Angle Theatrical Movie Pilot Cold Open (10.2s):
      - Angle 1 (3.6s): Sweeping orbital crane descent across `v8_pilot_7d_scorecard_stage_16x9.jpg`
      - Angle 2 (3.6s): Low-angle whip-glide across the Pilot Curved Glass Displays (`SCORE 1–10` -> `< 35 / 70`)
      - Angle 3 (3.0s): Luminous preview dolly push onto `v9_genie_4yo_bala_rishi_16x9.jpg` (`4yo Bala-Rishi @Me` + lamp)
    """
    c1 = TEMP_DIR / "co_pilot_v2_01.mp4"
    c2 = TEMP_DIR / "co_pilot_v2_02.mp4"
    c3 = TEMP_DIR / "co_pilot_v2_03.mp4"

    f1 = int(round(3.6 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(PILOT_STAGE_JPG),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='1.12-0.09*(on/{f1})':x='(iw-iw/zoom)*(0.35+0.30*(on/{f1}))':y='(ih-ih/zoom)*(0.25+0.25*(on/{f1}))':d={f1}:s=1920x1080:fps=30,"
            "eq=contrast=1.03:saturation=1.04,vignette=PI/8.5,setsar=1,format=yuv420p"
        ),
        "-t", "3.60", "-r", "30", "-video_track_timescale", "30000",
        "-c:v", "libx264", "-profile:v", "high", "-preset", preset, "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(c1)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    f2 = int(round(3.6 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(PILOT_STAGE_JPG),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='1.36':x='(iw-iw/zoom)*(0.05+0.90*(on/{f2}))':y='(ih-ih/zoom)*0.76':d={f2}:s=1920x1080:fps=30,"
            "eq=contrast=1.04:saturation=1.05,vignette=PI/8,setsar=1,format=yuv420p"
        ),
        "-t", "3.60", "-r", "30", "-video_track_timescale", "30000",
        "-c:v", "libx264", "-profile:v", "high", "-preset", preset, "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(c2)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    f3 = int(round(3.0 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(GENIE_BALA_JPG),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='1.12+0.12*(on/{f3})':x='(iw-iw/zoom)*(0.48+0.06*(on/{f3}))':y='(ih-ih/zoom)*0.26':d={f3}:s=1920x1080:fps=30,"
            "eq=contrast=1.04:saturation=1.05,vignette=PI/7.5,setsar=1,format=yuv420p"
        ),
        "-t", "3.00", "-r", "30", "-video_track_timescale", "30000",
        "-c:v", "libx264", "-profile:v", "high", "-preset", preset, "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(c3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ct = TEMP_DIR / "co_pilot_v2_concat.txt"
    ct.write_text(f"file '{c1}'\nfile '{c2}'\nfile '{c3}'\n", encoding="utf-8")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(ct),
        "-c", "copy", str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return probe_duration(out_mp4)


def render_finale_outro_pilot(out_mp4: Path, preset: str = "fast") -> float:
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
        "-c:v", "libx264", "-profile:v", "high", "-preset", preset, "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return probe_duration(out_mp4)


def render_pilot_shot(
    entry: dict,
    sp_st: float,
    sp_en: float,
    raw_dur: float,
    out_mp4: Path,
    preset: str = "fast",
) -> tuple[float, float, float]:
    """
    Renders a single 1.0x Theatrical Cinema Pilot shot at internal 1920x1080 precision so all
    overlays and ASS subtitles align identically across 360p and 1080p outputs.
    """
    src_mp4 = Path(entry["src"])
    layout = entry["layout"]
    voice = entry["voice"]
    ov_name = entry.get("overlay")
    ov_path = (OVERLAYS_DIR / ov_name) if (ov_name and (OVERLAYS_DIR / ov_name).exists()) else None

    if layout == "image_dissolve":
        target_dur = float(entry["visual_dur"])
        dst_img = Path(entry["dst_img"])
        frames = max(30, int(round(target_dur * 30)))
        fade_st = max(0.30, target_dur * 0.30)
        fade_d = max(0.55, target_dur - fade_st - 0.08)
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-t", f"{target_dur:.3f}", "-i", str(src_mp4),
            "-loop", "1", "-t", f"{target_dur:.3f}", "-i", str(dst_img),
            "-f", "lavfi", "-t", f"{target_dur:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-filter_complex", (
                f"[0:v]scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
                f"zoompan=z='1.20-0.12*(on/{frames})':x='(iw-iw/zoom)*(0.52-0.06*(on/{frames}))':y='(ih-ih/zoom)*0.32':d={frames}:s=1920x1080:fps=30,"
                "vignette=PI/8,setsar=1,format=rgba[v0];"
                f"[1:v]scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
                f"zoompan=z='1.08+0.10*(on/{frames})':x='(iw-iw/zoom)*(0.48+0.06*(on/{frames}))':y='(ih-ih/zoom)*0.28':d={frames}:s=1920x1080:fps=30,"
                f"vignette=PI/7.5,setsar=1,format=rgba,fade=t=in:st={fade_st:.2f}:d={fade_d:.2f}:alpha=1[v1];"
                "[v0][v1]overlay=0:0:format=auto,format=yuv420p[vout]"
            ),
            "-map", "[vout]", "-map", "2:a:0",
            "-t", f"{target_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
            "-c:v", "libx264", "-profile:v", "high", "-preset", preset, "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, 0.10, max(0.60, d - 0.10))

    if layout == "glass_whip_pan":
        target_dur = float(entry["visual_dur"])
        seg1_dur = round(target_dur * 0.50, 3)
        seg2_dur = max(0.80, target_dur - seg1_dur)
        f1 = max(20, int(round(seg1_dur * 30)) + 2)
        f2 = max(20, int(round(seg2_dur * 30)) + 2)
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-t", f"{seg1_dur + 0.20:.3f}", "-i", str(src_mp4),
            "-loop", "1", "-t", f"{seg2_dur + 0.20:.3f}", "-i", str(src_mp4),
            "-f", "lavfi", "-t", f"{target_dur:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-filter_complex", (
                f"[0:v]scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
                f"zoompan=z='1.58+0.08*(on/{f1})':x='(iw-iw/zoom)*(0.03+0.19*(on/{f1}))':y='(ih-ih/zoom)*0.78':d={f1}:s=1920x1080:fps=30,"
                f"trim=0:{seg1_dur:.3f},setpts=PTS-STARTPTS,eq=contrast=1.04:saturation=1.05,vignette=PI/7.5,setsar=1,format=yuv420p[g1];"
                f"[1:v]scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
                f"zoompan=z='1.58+0.08*(on/{f2})':x='(iw-iw/zoom)*(0.78+0.18*(on/{f2}))':y='(ih-ih/zoom)*0.78':d={f2}:s=1920x1080:fps=30,"
                f"trim=0:{seg2_dur:.3f},setpts=PTS-STARTPTS,eq=contrast=1.04:saturation=1.05,vignette=PI/7.5,setsar=1,format=yuv420p[g2];"
                "[g1][g2]concat=n=2:v=1:a=0,format=yuv420p[vout]"
            ),
            "-map", "[vout]", "-map", "2:a:0",
            "-t", f"{target_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
            "-c:v", "libx264", "-profile:v", "high", "-preset", preset, "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, 0.15, max(0.80, d - 0.15))

    if layout == "pip75_visual_beat":
        v_ss = float(entry.get("visual_ss", 0.25))
        req_dur = float(entry.get("visual_dur", 5.80))
        clip_dur = min(max(2.50, raw_dur - v_ss - 0.08), req_dur)
        frames = max(30, int(round(clip_dur * 30)) + 5)
        orbit_dir = int(entry.get("orbit_dir", -1))
        bg_x = f"(iw-1920)*(0.08+0.84*(on/{frames}))" if orbit_dir >= 0 else f"(iw-1920)*(0.92-0.84*(on/{frames}))"
        has_aud = has_audio_stream(src_mp4)

        seg1_dur = round(clip_dur * 0.48, 3)
        seg2_dur = max(0.80, clip_dur - seg1_dur)
        pip_zoom = float(entry.get("pip_zoom", 1.24))
        pip_fx = float(entry.get("pip_fx", 0.50))
        pip_fy = float(entry.get("pip_fy", 0.36))
        pw_a, ph_a = even_px(1432 * 1.12), even_px(802 * 1.12)
        pw_b, ph_b = even_px(1432 * pip_zoom), even_px(802 * pip_zoom)
        fg_xa = f"(iw-1432)*(0.20+0.60*(t/{seg1_dur:.3f}))" if orbit_dir >= 0 else f"(iw-1432)*(0.80-0.60*(t/{seg1_dur:.3f}))"
        fg_xb = f"clip((iw-1432)*({pip_fx:.3f}-0.04+0.08*(t/{seg2_dur:.3f})),0,iw-1432)"
        fg_yb = f"clip((ih-802)*({pip_fy:.3f}-0.02*(t/{seg2_dur:.3f})),0,ih-802)"

        cmd = [
            "ffmpeg", "-y",
            "-i", str(src_mp4),
            "-loop", "1", "-t", f"{clip_dur + 0.25:.3f}", "-i", str(PILOT_STAGE_JPG),
        ]
        if not has_aud:
            cmd += ["-f", "lavfi", "-t", f"{clip_dur:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
        fc = [
            f"[1:v]scale=2140:1204:force_original_aspect_ratio=increase,crop=2140:1204,"
            f"zoompan=z='1.00':x='{bg_x}':y='(ih-1080)*(0.52-0.16*sin(PI*on/{frames}))':d={frames}:s=1920x1080:fps=30,"
            f"trim=0:{clip_dur:.3f},setpts=PTS-STARTPTS,"
            "eq=brightness=-0.03:saturation=0.98,vignette=PI/9,setsar=1,format=yuv420p[bg]",
            f"[0:v]trim=start={v_ss:.3f}:end={v_ss + clip_dur:.3f},setpts=PTS-STARTPTS,fps=30,"
            "scale=1432:802:force_original_aspect_ratio=increase,crop=1432:802,split=2[fraw1][fraw2]",
            f"[fraw1]trim=0:{seg1_dur:.3f},setpts=PTS-STARTPTS,"
            f"scale={pw_a}:{ph_a},crop=1432:802:x='{fg_xa}':y='(ih-802)*0.46',"
            "eq=contrast=1.03:saturation=1.04,setsar=1,format=yuv420p[fa]",
            f"[fraw2]trim={seg1_dur:.3f}:{clip_dur:.3f},setpts=PTS-STARTPTS,"
            f"scale={pw_b}:{ph_b},crop=1432:802:x='{fg_xb}':y='{fg_yb}',"
            "eq=contrast=1.05:saturation=1.06,vignette=PI/7,setsar=1,format=yuv420p[fb]",
            "[fa][fb]concat=n=2:v=1:a=0,pad=w=1440:h=810:x=4:y=4:color=#EBC670,setsar=1,format=yuv420p[fg]",
            "[bg][fg]overlay=240:135:shortest=1,format=yuv420p[vout]",
        ]
        if has_aud:
            fc.append(
                f"[0:a]atrim=start={v_ss:.3f}:end={v_ss + clip_dur:.3f},asetpts=PTS-STARTPTS,"
                f"highpass=f=90,lowpass=f=7500,volume=0.20,"
                f"afade=t=in:st=0:d=0.12,afade=t=out:st={max(0.2, clip_dur - 0.18):.3f}:d=0.18,"
                "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[aout]"
            )
            a_map = "[aout]"
        else:
            a_map = "2:a:0"

        cmd += [
            "-filter_complex", ";".join(fc),
            "-map", "[vout]", "-map", a_map,
            "-t", f"{clip_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
            "-c:v", "libx264", "-profile:v", "high", "-preset", preset, "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, 0.20, max(1.00, d - 0.20))

    # Spoken shots (`full`, `summon_lamp_awakening`, `pip75_broll_cut`)
    trim_st = max(0.0, sp_st - 0.16)
    trim_en = min(raw_dur, sp_en + 0.22)
    if trim_en - trim_st < 1.50:
        trim_st = 0.0
        trim_en = max(2.0, raw_dur - 0.10)
    clip_dur = trim_en - trim_st
    rel_sp_st = max(0.04, sp_st - trim_st)
    rel_sp_en = min(clip_dur - 0.04, sp_en - trim_st)

    if voice == "bala_genie":
        # Pure, crystal-clear EQ preserving the sweet, articulate 4-year-old child-sage voice!
        a_eq = "highpass=f=95,lowpass=f=13500"
    else:
        a_eq = "highpass=f=75,lowpass=f=12500"

    a_chain = (
        f"atrim=start={trim_st:.3f}:end={trim_en:.3f},asetpts=PTS-STARTPTS,"
        f"{a_eq},"
        f"afade=t=in:st=0:d=0.04,afade=t=out:st={max(0.10, clip_dur - 0.05):.3f}:d=0.05,"
        "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"
    )

    if layout == "full":
        seg1_dur = round(clip_dur * 0.48, 3)
        seg2_dur = max(0.80, clip_dur - seg1_dur)
        orbit_dir = int(entry.get("orbit_dir", 1))
        cu_zoom = float(entry.get("cu_zoom", 1.26))
        cu_fx = float(entry.get("cu_fx", 0.50))
        cu_fy = float(entry.get("cu_fy", 0.22))
        cu_w, cu_h = even_px(1920 * cu_zoom), even_px(1080 * cu_zoom)

        x_orb = f"(iw-1920)*(0.20+0.60*(t/{seg1_dur:.3f}))" if orbit_dir >= 0 else f"(iw-1920)*(0.80-0.60*(t/{seg1_dur:.3f}))"
        y_orb = f"(ih-1080)*(0.42-0.16*sin(PI*t/{seg1_dur:.3f}))"
        x_cu = f"clip((iw-1920)*({cu_fx:.3f}-0.040+0.080*(t/{seg2_dur:.3f})),0,iw-1920)"
        y_cu = f"clip((ih-1080)*({cu_fy:.3f}-0.018*(t/{seg2_dur:.3f})),0,ih-1080)"

        cmd = ["ffmpeg", "-y", "-i", str(src_mp4)]
        fc = [
            f"[0:v]trim=start={trim_st:.3f}:end={trim_en:.3f},setpts=PTS-STARTPTS,fps=30,"
            "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,split=2[vraw1][vraw2]",
            f"[vraw1]trim=start=0:end={seg1_dur:.3f},setpts=PTS-STARTPTS,"
            f"scale=2208:1242,crop=1920:1080:x='{x_orb}':y='{y_orb}',"
            "eq=contrast=1.02:saturation=1.03,vignette=PI/8.5,setsar=1,format=yuv420p[cam_a_raw]",
            f"[vraw2]trim=start={seg1_dur:.3f}:end={clip_dur:.3f},setpts=PTS-STARTPTS,"
            f"scale={cu_w}:{cu_h},crop=1920:1080:x='{x_cu}':y='{y_cu}',"
            "eq=contrast=1.04:saturation=1.05,vignette=PI/6.5,setsar=1,format=yuv420p[cam_b]",
        ]
        if ov_path:
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
            "-c:v", "libx264", "-profile:v", "high", "-preset", preset, "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, rel_sp_st, min(d - 0.04, rel_sp_en))

    if layout == "summon_lamp_awakening":
        img_src = Path(entry["image_src"])
        lamp_mp4 = Path(entry["lamp_mp4"])
        lamp_ss = float(entry.get("lamp_ss", 0.60))

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
            "-c:v", "libx264", "-profile:v", "high", "-preset", preset, "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, rel_sp_st, min(d - 0.04, rel_sp_en))

    if layout == "pip75_broll_cut":
        broll_mp4 = Path(entry["broll_mp4"])
        broll_ss = float(entry.get("broll_ss", 1.20))
        seg2_dur = min(float(entry.get("broll_dur", 2.40)), max(1.40, clip_dur - 1.80))
        seg1_dur = clip_dur - seg2_dur
        frames = max(30, int(round(clip_dur * 30)) + 5)
        orbit_dir = int(entry.get("orbit_dir", 1))

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
            "-loop", "1", "-t", f"{clip_dur + 0.25:.3f}", "-i", str(PILOT_STAGE_JPG),
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
            "-c:v", "libx264", "-profile:v", "high", "-preset", preset, "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = probe_duration(out_mp4)
        return (d, rel_sp_st, min(d - 0.04, rel_sp_en))

    raise ValueError(f"Unsupported layout mode: {layout}")


def build_pilot_ass(
    ass_path: Path,
    cold_dur: float,
    shot_timings: list[dict],
    finale_start: float,
    total_dur: float,
    resolution: str = "360p",
):
    """
    Builds the dark-shaded (`BorderStyle=3`, `OutlineColour=&H38080A10`, `BackColour=&H38080A10`)
    ASS subtitle file using strictly single-line sequential events placed cleanly at `MarginV=26..28`.
    Uses slightly larger font size (`35pt`) when downscaling to `360p` (`640x360`) for effortless clarity.
    """
    fs_title = 35 if resolution == "360p" else 33
    fs_body = 34 if resolution == "360p" else 32
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TitleGold,DejaVu Sans,{fs_title},&H00B8F2FF,&H00B8F2FF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.4,0,3,11.0,0.0,2,56,56,28,1
Style: CinemaWhite,DejaVu Sans,{fs_body},&H00FFFFFF,&H00FFFFFF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.2,0,3,11.0,0.0,2,56,56,26,1
Style: BalaGold,DejaVu Sans,{fs_body},&H00B8F2FF,&H00B8F2FF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.2,0,3,11.0,0.0,2,56,56,26,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    raw_events: list[tuple[float, float, str, str]] = []

    if cold_dur >= 8.5:
        raw_events.extend([
            (0.45, 3.45, "TitleGold", "KARMIC GENIE SHOW  •  PILOT EPISODE (SEASON 1, EPISODE 0)"),
            (3.60, 7.05, "CinemaWhite", "THE 7D WAY  •  Score Each Virtue 1–10 (Max 70) — Below 35, Change Your Course!"),
            (7.20, min(cold_dur - 0.20, 10.00), "TitleGold", "7 Great Virtues to Awaken Your Conscience & Become a Pioneer of the New World"),
        ])

    for st in shot_timings:
        lines = st["lines"]
        if not lines:
            continue
        style = "BalaGold" if st["voice"] == "bala_genie" else "CinemaWhite"
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

    if total_dur - finale_start >= 6.0:
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
    parser = argparse.ArgumentParser(description="Build Karmic Genie Show Pilot S01E00 (360p Preview / 1080p Master)")
    parser.add_argument(
        "--resolution",
        default="360p",
        choices=["360p", "1080p"],
        help="Target output resolution: '360p' (640x360 preview default) or '1080p' (1920x1080 master).",
    )
    parser.add_argument("--rescan-clips", action="store_true", help="Force re-resolving flow_s01e00_clips via Whisper & RGB stats")
    parser.add_argument("--qa-only", action="store_true", help="Only resolve clips and render 20-clip QA contact sheet")
    args = parser.parse_args()

    from faster_whisper import WhisperModel

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUT_360P_MP4.parent.mkdir(parents=True, exist_ok=True)

    # Ensure all 12 curved-glass holographic refraction overlays exist
    if not (OVERLAYS_DIR / "ov_p00_compass.png").exists():
        import render_s01e00_pilot_overlays
        render_s01e00_pilot_overlays.main()

    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")

    print("1️⃣ Resolving all 20 Pilot S01E00 clips (`Sample 2` + `H01..H09` + `G01..G07` + `B01..B03`)...", flush=True)
    clip_map = resolve_pilot_clips(model, force_rescan=args.rescan_clips)
    render_qa_contact_sheet(clip_map, QA_CONTACT_JPG)

    if args.qa_only:
        return

    ledger = build_pilot_shot_ledger(clip_map)
    total_slots = len(ledger)
    shot_preset = "veryfast" if args.resolution == "360p" else "fast"

    print(f"2️⃣ Verifying Pilot S01E00 assets & Editorial Purity across all {total_slots} shots ({args.resolution})...", flush=True)
    for entry in ledger:
        src = Path(entry["src"])
        if not src.exists():
            raise FileNotFoundError(f"Missing clip/image for {entry['sid']}: {src}")
        for extra_k in ("image_src", "dst_img", "broll_mp4", "lamp_mp4"):
            if extra_k in entry and not Path(entry[extra_k]).exists():
                raise FileNotFoundError(f"Missing {extra_k} for {entry['sid']}: {entry[extra_k]}")
        for ln in entry["lines"]:
            assert_editorial_purity(ln, entry["sid"])

    print("3️⃣ Rendering 3-Angle Theatrical Pilot Cold Open (10.2s) & Finale Logo Card (11.0s)...", flush=True)
    co_mp4 = TEMP_DIR / "part_00_cold_open_v2.mp4"
    cold_dur = render_cold_open_pilot(co_mp4, preset=shot_preset)

    fin_mp4 = TEMP_DIR / "part_99_finale_logo_v2.mp4"
    render_finale_outro_pilot(fin_mp4, preset=shot_preset)

    print(f"4️⃣ Directing all {total_slots} Pilot shots (Adult @Me + 4yo Bala-Rishi @Me across D1..D7)...", flush=True)
    parts = [co_mp4]
    cursor = cold_dur
    shot_timings = []

    for idx, entry in enumerate(ledger, 1):
        sid = entry["sid"]
        src = Path(entry["src"])
        layout = entry["layout"]

        if layout in ("image_dissolve", "glass_whip_pan"):
            raw_dur = float(entry["visual_dur"])
            sp_st, sp_en = 0.0, raw_dur
        elif layout == "pip75_visual_beat":
            raw_dur = probe_duration(src)
            sp_st, sp_en = 0.20, raw_dur - 0.20
        else:
            txt, sp_st, sp_en, raw_dur = transcribe_clip_whisper(src, model, entry["hint_sp"])
            assert_editorial_purity(txt, f"{sid}_audio_transcript")

        out_p = TEMP_DIR / f"pilot_v2_{idx:02d}_{sid}.mp4"
        dur, rel_st, rel_en = render_pilot_shot(
            entry=entry,
            sp_st=sp_st,
            sp_en=sp_en,
            raw_dur=raw_dur,
            out_mp4=out_p,
            preset=shot_preset,
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
        cu_tag = f" [Orbit->CU {entry['cu_zoom']:.2f}x]" if "cu_zoom" in entry else ""
        print(
            f"    [{idx:02d}/{total_slots}] {sid} [{layout}]{cu_tag} <- {src.name} "
            f"({dur:.2f}s, cum={cursor:.1f}s){ov_tag}",
            flush=True,
        )

    finale_start = cursor
    parts.append(fin_mp4)

    concat_txt = TEMP_DIR / "master_pilot_v2_concat.txt"
    concat_txt.write_text("\n".join(f"file '{p}'" for p in parts) + "\n", encoding="utf-8")
    stitched_mp4 = TEMP_DIR / "stitched_pilot_v2_raw.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy", str(stitched_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    actual_total = probe_duration(stitched_mp4)
    print(
        f"5️⃣ Stitched raw Pilot S01E00 runtime: {actual_total:.2f}s "
        f"({int(actual_total//60):02d}:{actual_total%60:05.2f})",
        flush=True,
    )

    ass_path = TEMP_DIR / "s01e00_pilot_7d_way_v2.ass"
    build_pilot_ass(ass_path, cold_dur, shot_timings, finale_start, actual_total, resolution=args.resolution)

    vol_expr = (
        f"if(lt(t,{cold_dur-0.35:.2f}), 0.56, "
        f"if(gt(t,{finale_start-0.60:.2f}), 0.54, 0.038))"
    )

    if args.resolution == "360p":
        primary_out = OUT_360P_MP4
        scale_tail = ",scale=640:360:flags=lanczos"
        final_crf = "20"
        audio_br = "192k"
    else:
        primary_out = OUT_16X9_MP4
        scale_tail = ""
        final_crf = "18"
        audio_br = "256k"

    print(f"6️⃣ Burning dark-shaded BorderStyle=3 subtitles + mixing 7D Theme at -14 LUFS ({args.resolution})...", flush=True)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(stitched_mp4),
        "-ss", "4.00", "-stream_loop", "-1", "-i", str(THEME_WAV),
        "-filter_complex", (
            f"[0:v]ass={ass_path},fade=t=in:st=0:d=0.60,fade=t=out:st={actual_total-1.10:.2f}:d=1.05{scale_tail}[vout];"
            f"[1:a]atrim=0:{actual_total:.3f},asetpts=PTS-STARTPTS,lowpass=f=9000,volume='{vol_expr}':eval=frame[bgm];"
            "[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
        ),
        "-map", "[vout]", "-map", "[aout]",
        "-t", f"{actual_total:.3f}",
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", final_crf,
        "-r", "30",
        "-c:a", "aac", "-b:a", audio_br, "-ar", "48000",
        "-movflags", "+faststart",
        str(primary_out)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Mirror outputs so both `_360p.mp4` and `_16x9.mp4` + artifact directory stay in sync
    if primary_out == OUT_360P_MP4:
        shutil.copy2(OUT_360P_MP4, OUT_16X9_MP4)
    if ARTIFACT_DIR.exists():
        if OUT_360P_MP4.exists():
            shutil.copy2(OUT_360P_MP4, ARTIFACT_360P_MP4)
        shutil.copy2(primary_out, ARTIFACT_16X9_MP4)

    final_d = probe_duration(primary_out)
    print(f"\n🏆 S01E00 PILOT ({args.resolution.upper()}) MASTER READY: {primary_out}")
    print(f"   Runtime: {int(final_d//60):02d}:{final_d%60:05.2f} ({final_d:.2f}s) | Size: {primary_out.stat().st_size/1e6:.2f} MB", flush=True)


if __name__ == "__main__":
    main()
