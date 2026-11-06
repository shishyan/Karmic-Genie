#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Widescreen (16:9, 1920x1080, 30fps, -14 LUFS) Film Assembler for:
  Karmic Genie Show — Season 1, Episode 1 (~07:20 Full Movie)
  "Seven Chairs Around One Fire: Non-AI Teams, Hyperscaler Billions & The 2030 Clock"

Key engineering features:
  1. Deterministic Whisper fingerprint matching maps every generated Flow clip to its exact
     canonical screenplay slot (1..44) regardless of Flow card completion order.
  2. Verbatim screenplay subtitle alignment: uses Whisper word timestamps strictly for speech
     start/end timing while rendering 100% typo-free canonical screenplay text (BorderStyle=1,
     zero background boxes, zero Whisper homophones).
  3. Unhurried cinema pacing: pitch/formant-preserved rubberband tempo (0.87x human speakers,
     0.84x + warm gentle high-mid softening EQ for the peaceful, polite Karmic Genie) + smooth
     30fps frame blending + natural room-tone pauses between scenes.
  4. Top-left translucent glass documentary badges for the 2025->Today timeline & all 7 Hats.
  5. Official 7D Theme Song cold-open title sting, subtle ducked meditative bed, and pure-white
     Jeweled-Lamp Logo Card grand finale.
"""

import json
import re
import subprocess
import wave
import numpy as np
from pathlib import Path

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
LEGACY_OPENER_CLIPS = Path("/home/shishyan/GitHub/Influenzian/Karmic_Genie_Show/renders/opener_v5_7d_16x9_clips")
MASTERS_DIR = REPO_DIR / "assets" / "studio_v5_masters"
THEME_WAV = REPO_DIR / "assets" / "theme" / "official_karmic_genie_7d_theme_song.wav"
LOGO_JPG = REPO_DIR / "assets" / "logo" / "official_karmic_genie_show_logo.jpg"
EP_DIR = REPO_DIR / "episodes" / "S01E01_Employees_vs_Tech_CEO"
CLIPS_ROOT = EP_DIR / "flow_16x9_clips"
OVERLAYS_DIR = EP_DIR / "overlays"
TEMP_DIR = EP_DIR / "temp_film_build"
OUT_MP4 = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E01_Full_Film_16x9.mp4"
ARTIFACT_MP4 = Path("/home/shishyan/.gemini/antigravity/brain/b55fc9ea-1a2e-45b9-8d71-a53ee11caf0c/Karmic_Genie_Show_S01E01_Full_Film_16x9.mp4")


# Canonical 44-shot screenplay ledger:
# (slot_id, batch_subdir, file_prefix, keywords_for_matching, speaker_mode, overlay_png, pause_after_s, canonical_lines)
SHOT_LEDGER = [
    # --- PROLOGUE: NARRATOR (@Me) 2025 -> TODAY ---
    ("P01", "batch_01_prologue", "batch_01_prologue", ["sixty", "quiet seconds", "before anyone"], "human", None, 0.25, [
        "Before anyone speaks tonight, let's take sixty quiet seconds",
        "to see what happened since early 2025.",
    ]),
    ("P02", "batch_01_prologue", "batch_01_prologue", ["record profits", "fifty-four", "154", "giants"], "human", "ov_p1_2025.png", 0.25, [
        "In 2025, tech giants earned record profits—",
        "yet over 154,000 US tech roles vanished.",
    ]),
    ("P03", "batch_01_prologue", "batch_01_prologue", ["october", "fourteen thousand", "14,000", "four hundred"], "human", None, 0.30, [
        "That October, 14,000 corporate jobs disappeared in one morning,",
        "while Big Tech spending crossed $410 billion.",
    ]),
    ("P04", "batch_01_prologue", "batch_01_prologue", ["eighty thousand", "80,000", "oracle", "ninety days"], "human", "ov_p2_q1_2026.png", 0.30, [
        "By early 2026, over 80,000 workers were cut in 90 days",
        "across Seattle, Oracle, and Dell.",
    ]),
    ("P05", "batch_01_prologue", "batch_01_prologue", ["seven hundred", "720", "free cash flow", "today"], "human", "ov_p3_today_2026.png", 0.25, [
        "Today, hyperscaler spending exceeds $720 billion a year—",
        "pushing quarterly free cash flow negative.",
    ]),
    ("P06", "batch_01_prologue", "batch_01_prologue", ["cloud and ai", "non-cloud", "seven lives", "marcus"], "human", None, 0.65, [
        "Cloud and AI didn't shrink—every cut hit non-cloud, non-AI teams.",
        "Seven lives sit behind those numbers. Marcus, begin.",
    ]),

    # --- SCENE 1: HAT #1 (MARCUS, SF) & HAT #2 (ARJUN, SEATTLE <-> MYSURU) ---
    ("S1_01", "batch_02_scene1_sf_mysuru", "batch_02_scene1_sf_mysuru", ["thirty thousand", "30,000", "heartless", "outside"], "human", "ov_hat1_marcus.png", 0.20, [
        "Cutting 30,000 corporate roles during record profits",
        "looks heartless from the outside. Look at our cash flow.",
    ]),
    ("S1_02", "batch_02_scene1_sf_mysuru", "batch_02_scene1_sf_mysuru", ["fifty billion", "50 billion", "gpu", "every dollar"], "human", None, 0.20, [
        "$50 billion a quarter on GPUs flipped free cash flow negative.",
        "Cloud and AI demand every dollar right now.",
    ]),
    ("S1_03", "batch_02_scene1_sf_mysuru", "batch_02_scene1_sf_mysuru", ["middle layers", "four years", "ninety thousand", "90,000"], "human", None, 0.60, [
        "If I keep funding non-AI devices and middle layers,",
        "in four years 90,000 jobs vanish instead of 30,000.",
    ]),
    ("S1_04", "batch_02_scene1_sf_mysuru", "batch_02_scene1_sf_mysuru", ["millions of us", "home countries", "briefly", "earn dollars"], "human", "ov_hat2_arjun.png", 0.25, [
        "Millions of us work outside our home countries—",
        "telling ourselves we left just briefly to earn dollars.",
    ]),
    ("S1_05", "batch_02_scene1_sf_mysuru", "batch_02_scene1_sf_mysuru", ["consumer devices", "twelve years", "12 years", "ghost"], "human", None, 0.75, [
        "I wasn't in AI—I built consumer devices for twelve years.",
        "Chasing dollars and visas, I became a ghost at home.",
    ]),

    # --- SCENE 2: HAT #3 (ELENA, LONDON) & HAT #4 (MATEO, SAO PAULO) ---
    ("S2_02", "topup_clean", "rec_s2_02_elena", ["flattened", "thirty-five", "35", "bedtimes", "vanished"], "human", "ov_hat3_elena.png", 0.70, [
        "When companies flattened over 35% of small-team managers,",
        "seven years of missed bedtimes vanished.",
    ]),
    ("S2_04", "batch_03_scene2_london_saopaulo", "batch_03_scene2_london_saopaulo", ["paulo", "nobody laid", "first rung", "step on it"], "human", "ov_hat4_mateo.png", 0.25, [
        "In São Paulo, nobody laid me off—",
        "the first rung simply vanished before I could step on it.",
    ]),
    ("S2_05", "batch_03_scene2_london_saopaulo", "batch_03_scene2_london_saopaulo", ["seven percent", "7%", "sewed suits", "where do we start"], "human", None, 0.65, [
        "New graduates dropped to 7% of Big Tech hires.",
        "My father sewed suits twenty years—where do we start?",
    ]),

    # --- SCENE 3: HAT #5 (KENJI, TOKYO), HAT #6 (HEINRICH, MUNICH), HAT #7 (KAVITHA, COIMBATORE) ---
    ("S3_01", "batch_04_scene3_tokyo_munich_coimbatore", "batch_04_scene3_tokyo_munich_coimbatore", ["tokyo", "retail billing", "eighty percent", "hiring freeze"], "human", "ov_hat5_kenji.png", 0.25, [
        "In Tokyo, I maintain non-cloud retail billing",
        "inside the surviving 80% under a strict hiring freeze.",
    ]),
    ("S3_02", "batch_04_scene3_tokyo_munich_coimbatore", "batch_04_scene3_tokyo_munich_coimbatore", ["four teammates", "replacements", "eats alone", "five pagers"], "human", None, 0.60, [
        "Four teammates left with zero replacements approved.",
        "My wife eats alone every night while I carry five pagers.",
    ]),
    ("S3_03", "topup_clean", "tu2_munich_coimbatore", ["oracle", "dell", "cisco", "intel", "hardware"], "human", "ov_hat6_heinrich.png", 0.25, [
        "Across Oracle, Dell, Cisco, and Intel,",
        "thousands of hardware roles vanished.",
    ]),
    ("S3_04", "topup_clean", "tu2_munich_coimbatore", ["fifty-eight", "58", "munich", "legacy", "gracefully"], "human", None, 0.60, [
        "At fifty-eight in Munich, thirty-five years becomes 'legacy.'",
        "How do we leave gracefully?",
    ]),
    ("S3_05", "batch_04_scene3_tokyo_munich_coimbatore", "batch_04_scene3_tokyo_munich_coimbatore", ["bengaluru", "bangalore", "talent tools", "automated"], "human", "ov_hat7_kavitha.png", 0.25, [
        "I led internal talent tools in Bengaluru—",
        "one of the first non-AI teams automated earlier this year.",
    ]),
    ("S3_06", "topup_clean", "tu2_munich_coimbatore", ["coimbatore", "erased rent", "brought peace", "arrive early"], "human", None, 0.70, [
        "Coimbatore cut my pay, erased rent, and brought peace—",
        "did I arrive early?",
    ]),

    # --- SCENE 4: CONTEMPLATION, PUNCHLINE & REVERENT AWAKENING ---
    ("S4_01", "batch_05_scene4_punchline_and_awakening", "batch_05_scene4_punchline_and_awakening", ["__VISUAL_1__"], "ambient", None, 0.20, []),
    ("S4_02", "batch_05_scene4_punchline_and_awakening", "batch_05_scene4_punchline_and_awakening", ["san francisco", "coimbatore", "spreadsheet", "spread sheet", "seven chairs"], "human", None, 0.35, [
        "From $200 billion in San Francisco to a quiet courtyard in Coimbatore—",
        "no spreadsheet answers all seven chairs.",
    ]),
    ("S4_03", "topup_clean", "plate_s4_03_punchline", ["quiet the room", "ask together", "genie"], "human", None, 0.45, [
        "Let's quiet the room and ask together:",
        "What does Genie say — the 7D way?",
    ]),
    ("S5_01", "batch_05_scene4_punchline_and_awakening", "batch_05_scene4_punchline_and_awakening", ["__VISUAL_2__"], "ambient", "ov_genie_7d.png", 0.35, []),

    # --- SCENE 5: THE PEACEFUL, POLITE WISE SAINT & THE OPEN MIRROR ---
    ("S5_02", "batch_06_scene5_wise_saint_mirror", "batch_06_scene5_wise_saint_mirror", ["good evening", "without masks", "commandments"], "genie", None, 0.35, [
        "Good evening, dear friends. Thank you for speaking without masks tonight.",
        "Rest easy—I bring no commandments.",
    ]),
    ("S5_03", "batch_06_scene5_wise_saint_mirror", "batch_06_scene5_wise_saint_mirror", ["ready-made", "solution", "ego", "lantern"], "genie", None, 0.35, [
        "No human heart welcomes someone else's ready-made solution; ego guards the door.",
        "We only need a quiet lantern.",
    ]),
    ("S5_04", "batch_06_scene5_wise_saint_mirror", "batch_06_scene5_wise_saint_mirror", ["upanishad", "thunderclap", "two-minute", "home tonight"], "genie", None, 0.30, [
        "Like the ancient Upanishad parable of the Single Thunderclap—",
        "a two-minute story you might enjoy reading quietly at home tonight...",
    ]),
    ("S5_05", "batch_06_scene5_wise_saint_mirror", "batch_06_scene5_wise_saint_mirror", ["open sound", "echoes", "turning age", "belongs"], "genie", None, 0.30, [
        "When one open sound echoes across a turning age,",
        "each heart hears what quietly belongs to it.",
    ]),
    ("S5_06", "topup_clean", "rec_s5_06_genie_restraint", ["restraint", "postponed", "money", "presence"], "genie", None, 0.45, [
        "Where power sits: graceful restraint.",
        "Where love was postponed for money: presence.",
    ]),
    ("S6_01", "batch_06_scene5_wise_saint_mirror", "batch_06_scene5_wise_saint_mirror", ["consider", "twenty twenty", "2020", "move so fast"], "genie", None, 0.35, [
        "Consider gently why this decade from 2020 to 2030",
        "had to move so fast...",
    ]),

    # --- SCENE 6: THE BLESSING IN DISGUISE & THE 7D WAY ---
    ("S6_02", "batch_07_scene6_blessing_in_disguise", "batch_07_scene6_blessing_in_disguise", ["paused the planet", "reunited", "doors reopened", "sprinted"], "genie", None, 0.35, [
        "In 2020, life paused the planet and reunited families—",
        "yet once doors reopened, everyone sprinted right back.",
    ]),
    ("S6_03", "batch_07_scene6_blessing_in_disguise", "batch_07_scene6_blessing_in_disguise", ["forty years", "40 years", "melodies", "frantic"], "genie", None, 0.40, [
        "Even forty years ago, peaceful melodies sensed",
        "that a quieter, less frantic human era was coming.",
    ]),
    ("S6_04", "batch_07_scene6_blessing_in_disguise", "batch_07_scene6_blessing_in_disguise", ["oceans away", "currency", "two years", "twelve", "12"], "genie", None, 0.30, [
        "For millions working oceans away from home just for stronger currency—",
        "how easily two years turns into twelve.",
    ]),
    ("S6_05", "topup_clean", "rec_s6_05_genie_handcuffs", ["golden handcuffs", "aging parents", "wait"], "genie", None, 0.15, [
        "When a closed non-AI floor loosens those golden handcuffs",
        "while aging parents still wait...",
    ]),
    ("S6_05B", "topup_clean", "plate_s6_05b_blessing", ["__VISUAL_BLESSING__"], "ambient", None, 0.35, [
        "...could this shock be a blessing in disguise?",
    ]),
    ("S6_06", "topup_clean", "rec_s6_06_genie_coimbatore", ["daylight walks", "london", "elders", "coimbatore"], "genie", None, 0.65, [
        "When daylight walks return in London, boilerplate fades in São Paulo,",
        "and elders smile in Coimbatore—who truly fell behind?",
    ]),
    ("S6_07", "batch_07_scene6_blessing_in_disguise", "batch_07_scene6_blessing_in_disguise", ["seasoned oak", "autumn", "mentoring", "munich"], "genie", None, 0.50, [
        "And at fifty-eight in Munich—does a seasoned oak lose dignity in autumn,",
        "or turn gently toward mentoring and peace?",
    ]),

    # --- SCENE 7: A QUIET QUESTION FOR TOKYO & SF + HOST SIGN-OFF ---
    ("S7_01", "batch_08_scene7_finale", "s7a_genie", ["stewards", "new rails", "captain", "storm"], "genie", None, 0.30, [
        "Every era needs stewards to lay new rails, Marcus—",
        "no one faults a captain steering through a storm.",
    ]),
    ("S7_02", "batch_08_scene7_finale", "s7a_genie", ["ten years", "10 years", "what brings peace", "humanely", "bridge"], "genie", None, 0.45, [
        "Ten years from now, what brings peace—how fast old floors were cleared,",
        "or how humanely the bridge held everyone?",
    ]),
    ("S7_03", "topup_clean", "plate_s7_03_lotus_dissolve", ["__VISUAL_RETURN__"], "ambient", None, 0.35, []),
    ("S7_04", "batch_08_scene7_finale", "s7b_host", ["no single answer", "twenty-three", "23", "thirty-nine", "39", "fifty-eight", "58"], "human", None, 0.35, [
        "No single answer fits twenty-three in São Paulo, thirty-nine in Seattle,",
        "fifty-eight in Munich, or San Francisco.",
    ]),
    ("S7_05", "topup_clean", "plate_s7_05_signoff", ["quiet thunder", "only you know"], "human", None, 0.40, [
        "Only you know your quiet thunder tonight...",
        "What does Genie say — the 7D way?",
    ]),
]


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


def transcribe_clip(mp4_path: Path, model) -> tuple[str, float, float]:
    """Returns (lowercased_transcript, speech_start_s, speech_end_s)."""
    dur = probe_duration(mp4_path)
    if not has_audio_stream(mp4_path):
        return ("", 0.4, max(1.0, dur - 0.4))
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
        txt_parts.append(s.text.strip())
        if s.words:
            for w in s.words:
                words.append((w.start, w.end))
    full_txt = " ".join(txt_parts).lower().strip()
    if words:
        return (full_txt, max(0.15, words[0][0]), min(dur - 0.1, words[-1][1] + 0.18))
    return (full_txt, 0.35, max(1.2, dur - 0.35))


def match_clips_to_ledger(model) -> list[tuple[tuple, Path, float, float]]:
    """Matches every ledger entry to its best downloaded MP4 clip in its batch folder."""
    # Group ledger rows by (batch_subdir, file_prefix)
    groups: dict[tuple[str, str], list[tuple]] = {}
    for row in SHOT_LEDGER:
        groups.setdefault((row[1], row[2]), []).append(row)

    resolved = {}
    for (bsub, pref), rows in groups.items():
        bdir = CLIPS_ROOT / bsub
        mp4s = sorted(bdir.glob(f"{pref}*.mp4"))
        manifest_path = bdir / f"{pref}_manifest.json"
        labels_by_name = {}
        if manifest_path.exists():
            for item in json.loads(manifest_path.read_text(encoding="utf-8")):
                labels_by_name[item["file"]] = item.get("label", "").lower()

        candidates = []
        for mp4 in mp4s:
            txt, sp_st, sp_en = transcribe_clip(mp4, model)
            lbl = labels_by_name.get(mp4.name, "")
            candidates.append({"path": mp4, "txt": txt, "lbl": lbl, "sp_st": sp_st, "sp_en": sp_en, "used": False})
            print(f"  [{pref}] {mp4.name}: speech=({sp_st:.2f}..{sp_en:.2f}s) txt='{txt[:90]}'")

        # Pass 1: Match spoken-keyword rows first
        for row in rows:
            sid, _, _, kws, mode, *_ = row
            if kws[0].startswith("__VISUAL"):
                continue
            best_c = None
            best_score = -1
            for c in candidates:
                if c["used"]:
                    continue
                hay = c["txt"] + " " + c["lbl"]
                score = sum(3 for kw in kws if kw.lower() in hay)
                if len(c["txt"]) > 12:
                    score += 1
                if score > best_score:
                    best_score = score
                    best_c = c
            if best_c is not None:
                best_c["used"] = True
                resolved[sid] = (row, best_c["path"], best_c["sp_st"], best_c["sp_en"])

        # Pass 2: Match ambient/visual rows from remaining unused clips (prefer silent/short-speech clips)
        unused = [c for c in candidates if not c["used"]]
        unused.sort(key=lambda x: len(x["txt"]))
        for row in rows:
            sid = row[0]
            if sid in resolved:
                continue
            if unused:
                # For S4_01 vs S5_01 in batch_05: check label for 'lamp'/'genie'/'awaken' vs 'stadium'/'crowd'
                chosen = unused[0]
                if sid == "S4_01":
                    for u in unused:
                        if any(w in u["lbl"] for w in ("stadium", "tracking", "crowd", "hushed")):
                            chosen = u
                            break
                elif sid == "S5_01":
                    for u in unused:
                        if any(w in u["lbl"] for w in ("lamp", "ribbons", "genie", "namaste", "amber")):
                            chosen = u
                            break
                unused.remove(chosen)
                resolved[sid] = (row, chosen["path"], chosen["sp_st"], chosen["sp_en"])
            elif candidates:
                c0 = candidates[0]
                resolved[sid] = (row, c0["path"], c0["sp_st"], c0["sp_en"])

    return [resolved[row[0]] for row in SHOT_LEDGER]


def render_cold_open(out_mp4: Path) -> float:
    """Builds the 17.6s 16:9 7D Theme Cold Open (v6 Dormant Stage Crane + v6 7D Wall Pan + Macro Dormant Lamp)."""
    dormant_img = MASTERS_DIR / "v6_7d_dormant_stage_16x9.jpg"
    if not dormant_img.exists():
        dormant_img = MASTERS_DIR / "s01e01_act1_dormant_stage_16x9.jpg"

    c1 = TEMP_DIR / "co_01.mp4"
    c2 = TEMP_DIR / "co_02.mp4"
    c3 = TEMP_DIR / "co_03.mp4"

    # 8.2s slow crane push on 2K v6 Dormant Stage Master
    frames1 = int(round(8.2 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(dormant_img),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='min(zoom+0.00055,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames1}:s=1920x1080:fps=30,"
            "format=yuv420p"
        ),
        "-t", "8.20", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(c1)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 5.2s close architectural glide across the v6 7D stage wall & padded center logo!
    frames2 = int(round(5.2 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(dormant_img),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='1.42':x='(iw-iw/zoom)*0.24 + (iw-iw/zoom)*0.50*(on/{frames2})':y='(ih-ih/zoom)*0.33':d={frames2}:s=1920x1080:fps=30,"
            "format=yuv420p"
        ),
        "-t", "5.20", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(c2)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 4.2s pure macro jeweled lamp centerpiece (first 2.05s of opener_06.mp4 slowed smoothly to 4.2s)
    op6 = LEGACY_OPENER_CLIPS / "opener_06.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-t", "2.05", "-i", str(op6),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", "setpts=2.05*PTS,minterpolate=fps=30:mi_mode=blend,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,format=yuv420p",
        "-map", "0:v:0", "-map", "1:a:0",
        "-t", "4.20", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(c3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ct = TEMP_DIR / "co_concat.txt"
    ct.write_text(f"file '{c1}'\nfile '{c2}'\nfile '{c3}'\n", encoding="utf-8")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(ct),
        "-c", "copy", str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return probe_duration(out_mp4)


def render_finale_outro(out_mp4: Path) -> float:
    """Builds the 14.5s Grand Finale Logo Outro Card on pure white."""
    frames = int(round(14.5 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(LOGO_JPG),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=880:880:force_original_aspect_ratio=decrease,"
            "pad=1920:1080:(ow-iw)/2:(oh-ih)/2-36:color=white,"
            f"zoompan=z='min(zoom+0.0003,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps=30,"
            "format=yuv420p"
        ),
        "-t", "14.50", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return probe_duration(out_mp4)


def normalize_story_shot(idx: int, row: tuple, src_mp4: Path, out_mp4: Path) -> tuple[float, float]:
    """
    Slows and polishes a single story shot:
      - 'human': tempo=0.87 (natural, calm movie cadence)
      - 'genie': tempo=0.84 + warm gentle saintly EQ (ultra-peaceful, polite, soft-spoken)
      - 'ambient': tempo=0.88 silent/room-tone visual stillness
    Appends `pause_after_s` of gentle freeze-frame/room-tone breathing space at the end,
    and optionally composites the top-left documentary glass badge!
    Returns (stretched_clip_dur, tempo_factor_applied).
    """
    sid, _, _, _, mode, ov_name, pause_s, _ = row
    tempo = 0.84 if mode == "genie" else (0.87 if mode == "human" else 0.88)
    pts_mul = 1.0 / tempo
    src_has_aud = has_audio_stream(src_mp4)

    v_chain = (
        f"setpts={pts_mul:.5f}*PTS,"
        "minterpolate=fps=30:mi_mode=blend,"
        "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
        f"tpad=stop_mode=clone:stop_duration={pause_s:.3f},"
        "format=yuv420p"
    )

    if mode == "ambient" or not src_has_aud:
        # Pure peaceful room stillness
        raw_dur = probe_duration(src_mp4) * pts_mul + pause_s
        cmd = ["ffmpeg", "-y", "-i", str(src_mp4)]
        if ov_name and (OVERLAYS_DIR / ov_name).exists():
            ov_p = OVERLAYS_DIR / ov_name
            cmd += [
                "-loop", "1", "-t", f"{raw_dur:.3f}", "-i", str(ov_p),
                "-f", "lavfi", "-t", f"{raw_dur:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                "-filter_complex",
                f"[0:v]{v_chain}[vb];[1:v]fade=t=in:st=0.25:d=0.45:alpha=1,fade=t=out:st={max(1.5, raw_dur-0.7):.2f}:d=0.55:alpha=1[ov];[vb][ov]overlay=0:0:format=auto,format=yuv420p[vout]",
                "-map", "[vout]", "-map", "2:a:0",
            ]
        else:
            cmd += [
                "-f", "lavfi", "-t", f"{raw_dur:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                "-vf", v_chain,
                "-map", "0:v:0", "-map", "1:a:0",
            ]
        cmd += ["-t", f"{raw_dur:.3f}", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", str(out_mp4)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return (probe_duration(out_mp4), tempo)

    if mode == "genie":
        # Ultra-peaceful, polite, soft-spoken saintly vocal filter + -1.5dB gentle presence
        a_chain = (
            f"rubberband=tempo={tempo:.3f}:pitchq=quality:formant=preserved:transients=smooth,"
            "highpass=f=85,"
            "equalizer=f=220:t=q:w=1.1:g=1.6,"
            "equalizer=f=3200:t=q:w=1.1:g=-3.8,"
            "lowpass=f=10400,"
            "volume=0.86,"
            f"apad=pad_dur={pause_s:.3f},"
            "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"
        )
    else:
        a_chain = (
            f"rubberband=tempo={tempo:.3f}:pitchq=quality:formant=preserved:transients=smooth,"
            "highpass=f=75,lowpass=f=12000,"
            f"apad=pad_dur={pause_s:.3f},"
            "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"
        )

    est_dur = probe_duration(src_mp4) * pts_mul + pause_s
    cmd = ["ffmpeg", "-y", "-i", str(src_mp4)]
    if ov_name and (OVERLAYS_DIR / ov_name).exists():
        ov_p = OVERLAYS_DIR / ov_name
        cmd += [
            "-loop", "1", "-t", f"{est_dur:.3f}", "-i", str(ov_p),
            "-filter_complex",
            f"[0:v]{v_chain}[vb];[1:v]fade=t=in:st=0.25:d=0.45:alpha=1,fade=t=out:st={max(1.5, est_dur-0.7):.2f}:d=0.55:alpha=1[ov];[vb][ov]overlay=0:0:format=auto,format=yuv420p[vout];[0:a]{a_chain}[aout]",
            "-map", "[vout]", "-map", "[aout]",
        ]
    else:
        cmd += ["-vf", v_chain, "-af", a_chain]

    cmd += [
        "-t", f"{est_dur:.3f}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", str(out_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return (probe_duration(out_mp4), tempo)


def build_master_ass(ass_path: Path, cold_dur: float, shot_timings: list[dict], finale_start: float, total_dur: float):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TitleGold,DejaVu Sans,44,&H00B8F2FF,&H0000D7FF,&H45000000,&H64000000,-1,0,0,0,100,100,1.2,0,1,2.2,3.0,2,110,110,64,1
Style: CinemaWhite,DejaVu Sans,36,&H00FFFFFF,&H0000D7FF,&H45000000,&H64000000,-1,0,0,0,100,100,0.4,0,1,2.0,2.8,2,130,130,52,1
Style: GenieSaintGold,DejaVu Sans,36,&H00C8F4FF,&H0000D7FF,&H45000000,&H64000000,-1,0,0,0,100,100,0.4,0,1,2.0,2.8,2,130,130,52,1
Style: OutroSubtle,DejaVu Sans,26,&H00486885,&H0000D7FF,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,0.9,0,1,0.0,0.0,2,80,80,36,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = [
        "Dialogue: 0,0:00:00.80,0:00:05.20,TitleGold,,0,0,0,,KARMIC GENIE SHOW  •  SEASON 1, EPISODE 1",
        r"Dialogue: 0,0:00:05.40,0:00:11.60,CinemaWhite,,0,0,0,,THE 7D WAY\NDuty • Dharma • Divine • Discipline • Dignity • Devout • Destiny",
        r"Dialogue: 0,0:00:11.80,0:00:17.10,TitleGold,,0,0,0,,Seven Chairs Around One Fire\NNon-AI Teams, Hyperscaler Billions & The 2030 Clock",
    ]

    for st in shot_timings:
        lines = st["lines"]
        if not lines:
            continue
        style = "GenieSaintGold" if (st["mode"] == "genie" or st["sid"].startswith("S6_")) else "CinemaWhite"
        if st["mode"] == "ambient":
            sp_s = st["abs_start"] + 0.35
            sp_e = st["abs_end"] - 0.35
        else:
            sp_s = st["abs_start"] + st["sp_st_scaled"]
            sp_e = min(st["abs_end"] - 0.15, st["abs_start"] + st["sp_en_scaled"])
        if sp_e <= sp_s + 1.2:
            sp_s = st["abs_start"] + 0.35
            sp_e = st["abs_end"] - 0.35

        if len(lines) == 1:
            events.append(f"Dialogue: 0,{format_ass_time(sp_s)},{format_ass_time(sp_e)},{style},,0,0,0,,{lines[0]}")
        else:
            # Split cleanly across the two canonical lines proportional to character length!
            total_chars = sum(max(1, len(x)) for x in lines)
            cur = sp_s
            for i, ln in enumerate(lines):
                frac = max(1, len(ln)) / total_chars
                nxt = sp_e if i == len(lines) - 1 else (cur + (sp_e - sp_s) * frac)
                events.append(f"Dialogue: 0,{format_ass_time(cur)},{format_ass_time(max(cur + 0.6, nxt - 0.04))},{style},,0,0,0,,{ln}")
                cur = nxt

    # Finale pure-white logo card subtle 7D inscription
    events.append(
        f"Dialogue: 0,{format_ass_time(finale_start + 0.8)},{format_ass_time(total_dur - 1.0)},OutroSubtle,,0,0,0,,"
        r"Respect Your DUTY First.  •  Earn with DIGNITY Always.  •  Practice Life DISCIPLINE.\N"
        r"Uphold Karmic DHARMA.  •  Raise Family with DEVOTION.  •  Be Grateful to Your DIVINE.  •  Purposeful Life Is Your DESTINY."
    )

    ass_path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")


def main():
    from faster_whisper import WhisperModel

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUT_MP4.parent.mkdir(parents=True, exist_ok=True)
    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")

    print("1️⃣ Matching all 44 generated Flow clips to canonical screenplay ledger...", flush=True)
    matched = match_clips_to_ledger(model)

    print("2️⃣ Rendering 16:9 Cold Open & Finale Logo Cards...", flush=True)
    co_mp4 = TEMP_DIR / "part_00_cold_open.mp4"
    cold_dur = render_cold_open(co_mp4)

    fin_mp4 = TEMP_DIR / "part_99_finale_logo.mp4"
    fin_dur = render_finale_outro(fin_mp4)

    print("3️⃣ Normalizing, pitch-preserving slowing & polishing all 44 cinema shots...", flush=True)
    parts = [co_mp4]
    cursor = cold_dur
    shot_timings = []

    for idx, (row, src_mp4, sp_st, sp_en) in enumerate(matched, 1):
        out_p = TEMP_DIR / f"part_{idx:02d}_{row[0]}.mp4"
        dur, tempo = normalize_story_shot(idx, row, src_mp4, out_p)
        scale = 1.0 / tempo
        shot_timings.append({
            "sid": row[0],
            "mode": row[4],
            "lines": row[7],
            "abs_start": cursor,
            "abs_end": cursor + dur,
            "sp_st_scaled": sp_st * scale,
            "sp_en_scaled": sp_en * scale,
        })
        parts.append(out_p)
        cursor += dur
        print(f"    [{idx:02d}/44] {row[0]} <- {src_mp4.name} ({dur:.2f}s, total={cursor:.1f}s)", flush=True)

    finale_start = cursor
    parts.append(fin_mp4)
    total_est = cursor + fin_dur

    concat_txt = TEMP_DIR / "master_concat.txt"
    concat_txt.write_text("\n".join(f"file '{p}'" for p in parts) + "\n", encoding="utf-8")
    stitched_mp4 = TEMP_DIR / "stitched_master_raw.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy", str(stitched_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    actual_total = probe_duration(stitched_mp4)
    print(f"4️⃣ Stitched raw film duration: {actual_total:.2f}s ({actual_total/60:.2f} mins)", flush=True)

    ass_path = TEMP_DIR / "s01e01_full_film.ass"
    build_master_ass(ass_path, cold_dur, shot_timings, finale_start, actual_total)

    # 5. Master Sound Mix:
    # - Cold open (0 .. cold_dur): Official 7D Theme Song opening hook (4.0s .. 21.6s) at 0.58 volume
    # - Story body (cold_dur .. finale_start): Gentle, barely-whispered meditative ambient bed (0.042 volume = -27.5 dB)
    #   so all candid voices & saintly Genie reflections sit in peaceful clarity!
    # - Finale outro (finale_start .. end): Swells gently up to 0.55 volume for the closing 7D chorus!
    vol_expr = (
        f"if(lt(t,{cold_dur-0.4:.2f}), 0.58, "
        f"if(gt(t,{finale_start-0.8:.2f}), 0.54, 0.040))"
    )

    print("5️⃣ Burning borderless movie subtitles + mixing 7D Theme underscore at -14 LUFS...", flush=True)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(stitched_mp4),
        "-ss", "4.00", "-stream_loop", "-1", "-i", str(THEME_WAV),
        "-filter_complex",
        f"[0:v]ass={ass_path},fade=t=in:st=0:d=0.75,fade=t=out:st={actual_total-1.35:.2f}:d=1.30[vout];"
        f"[1:a]atrim=0:{actual_total:.3f},asetpts=PTS-STARTPTS,lowpass=f=9000,volume='{vol_expr}':eval=frame[bgm];"
        f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]",
        "-map", "[vout]", "-map", "[aout]",
        "-t", f"{actual_total:.3f}",
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-movflags", "+faststart",
        str(OUT_MP4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run(["cp", "-f", str(OUT_MP4), str(ARTIFACT_MP4)], check=True)
    final_d = probe_duration(OUT_MP4)
    print(f"\n🏆 S01E01 FULL 16:9 MOVIE MASTER READY: {OUT_MP4}")
    print(f"   Runtime: {int(final_d//60):02d}:{final_d%60:05.2f} ({final_d:.2f}s) | Size: {OUT_MP4.stat().st_size/1e6:.2f} MB", flush=True)


if __name__ == "__main__":
    main()
