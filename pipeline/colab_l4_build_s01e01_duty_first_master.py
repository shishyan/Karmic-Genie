#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Colab L4 GPU Master Film Assembler — v3 Broadcast Edition (`h264_nvenc` + `faster-whisper`)
for The Karmic Genie Show — Season 1, Episode 1:
  "1. RESPECT YOUR DUTY FIRST." (The 7D Way — Virtues & Divinity Series)

v3 Broadcast Upgrades:
  1. Zero Dialogue Truncation (`Bala-Matha` & `Bala-Rishi` + all 48 shots):
     - Generous `+0.38s` post-speech breath cushion; whenever speech extends past `full_dur - 0.65s`,
       plays right to `full_dur` with a soft `0.10s` micro-fade before `apad` so zero final consonants clip.
  2. Zero Spoken "Scene 1..7" Numbers:
     - `SLOT_MIN_TRIM_START` trims `DF20`, `DF21`, `DF24`, `DF26` at their exact `-44 dB` silence valleys
       immediately after `"Scene One/Two/Five/Seven"`, and `DF25` is freshly generated without `"Scene Six"`.
  3. News-Channel 2-Line Rolling Bottom Banner (`y=1004..1080`, `76px` = strictly 2 lines max!):
     - Zero floating 3-line left boxes!
     - Line 1 (`y=1007..1042`): Centered bold news badge + headline across a rich royal-navy & 24k-gold bar.
     - Line 2 (`y=1042..1080`): Live television right-to-left rolling news ticker (`*_ticker.png`)!
     - Spoken single-line subtitles sit cleanly at `MarginV=92` (`y~948`) above the news bar with zero overlap!
  4. Introductory Karmic Genie Show 7D Theme Song at Major Scene Endings (~Every 2 Minutes):
     - Plays the sung vocal hook (`official_karmic_genie_7d_theme_song.wav`: *"The 7D Way — Duty, Dharma,
       Divine, Discipline, Dignity, Devout, Destiny — Karmic Genie Show!"*) at:
       • `00:00` Cold Open (`11.2s`, `theme_ss=3.0s`)
       • `~02:00` Act I/II Break after `DF12` (`9.2s`, `theme_ss=3.0s`)
       • `~04:10` Act III Break after `DF28` (`9.2s`, `theme_ss=18.8s`)
       • `~05:50` Act V Break after `DF36` (`9.2s`, `theme_ss=44.2s`)
       • `~07:25` Grand Finale Logo Card after `DF48` (`10.0s`, `theme_ss=50.5s`)
"""

import json
import os
import shutil
import subprocess
import sys
import time
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

WORK_ROOT = Path(os.environ.get("KG_COLAB_ROOT", "/content/kg_s01e01_work"))
MASTERS_DIR = WORK_ROOT / "assets" / "studio_v5_masters"
STAGES_DIR = WORK_ROOT / "assets" / "stages_7d"
THEME_WAV = WORK_ROOT / "assets" / "theme" / "official_karmic_genie_7d_theme_song.wav"
LOGO_JPG = WORK_ROOT / "assets" / "logo" / "official_karmic_genie_show_logo.jpg"
EP_DIR = WORK_ROOT / "episodes" / "S01E01_Respect_Your_Duty_First"
LEDGER_JSON = EP_DIR / "s01e01_48_shot_flow_ledger.json"
CLIPS_ROOT = EP_DIR / "flow_16x9_clips"
OVERLAYS_DIR = EP_DIR / "overlays"
TEMP_DIR = WORK_ROOT / "temp_gpu_build_v3"
OUT_MASTER_MP4 = WORK_ROOT / "Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_v3_Master_1080p.mp4"
OUT_WEB_MP4 = WORK_ROOT / "Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_v3_Web_1080p.mp4"

FULLSCREEN_SLOTS = {
    "DF07", "DF08", "DF09", "DF28",
    "DF37", "DF38", "DF39", "DF40", "DF41", "DF42",
    "DF43", "DF44", "DF45", "DF46", "DF47", "DF48",
}

# Exact -44 dB silence-valley start offsets that cleanly strip spoken "Scene 1/2/5/7" prefixes:
SLOT_MIN_TRIM_START = {
    "DF20": 1.42,  # strips "Scene One." -> starts cleanly at "Ten thousand engineers..."
    "DF21": 1.02,  # strips "Scene Two." -> starts cleanly at "Doctors give medicine..."
    "DF24": 1.52,  # strips "Scene Five," -> starts cleanly at "No billionaire..."
    "DF26": 1.24,  # strips "Scene Seven." -> starts cleanly at "Pour out your unique Swadharma..."
}

# Major Act-Ending 7D Theme Song Musical Interludes (~every 2 minutes across the episode):
ACT_BREAK_INTERLUDES = {
    "DF12": {
        "id": "il_01_after_df12",
        "theme_ss": 3.00,
        "dur": 9.20,
        "bg": "trinity",
        "title": "THE KARMIC GENIE SHOW  •  ACT II: SACRED FAMILY DHARMA (ILLARAM)",
        "sub": "♪  The 7D Way — Duty • Dharma • Divine • Discipline • Dignity • Devout • Destiny  ♪",
    },
    "DF28": {
        "id": "il_02_after_df28",
        "theme_ss": 18.80,
        "dur": 9.20,
        "bg": "portal",
        "title": "THE KARMIC GENIE SHOW  •  ACT III: RESPECT EVERY SOUL'S DUTY",
        "sub": "♪  1. Duty First  →  2. What ONLY YOU Can Do  →  Honor Every Honest Worker  ♪",
    },
    "DF36": {
        "id": "il_03_after_df36",
        "theme_ss": 44.20,
        "dur": 9.20,
        "bg": "trinity",
        "title": "THE KARMIC GENIE SHOW  •  GRAND FINALE: AWAKENING THE KARMIC GENIE",
        "sub": "♪  Clean Conscience • Full-Chest Sigh of Relief • The Tonight Pillow Test  ♪",
    },
}

SHOW_TEMPO = 0.90


def has_rubberband() -> bool:
    try:
        out = subprocess.check_output(["ffmpeg", "-hide_banner", "-filters"], stderr=subprocess.DEVNULL).decode()
        return "rubberband" in out
    except Exception:
        return False


USE_RUBBERBAND = has_rubberband()


def has_nvenc() -> bool:
    try:
        out = subprocess.check_output(["ffmpeg", "-hide_banner", "-encoders"], stderr=subprocess.DEVNULL).decode()
        return "h264_nvenc" in out
    except Exception:
        return False


USE_NVENC = has_nvenc()
V_ENC = (
    ["-c:v", "h264_nvenc", "-preset", "p5", "-rc", "vbr", "-cq", "18", "-b:v", "0"]
    if USE_NVENC
    else ["-c:v", "libx264", "-preset", "fast", "-crf", "18"]
)


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


def split_single_line_chunks(lines: list[str], max_chars: int = 64) -> list[str]:
    joined = " ".join(ln.strip() for ln in lines if ln.strip())
    words = joined.split()
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


def transcribe_clip(mp4_path: Path, model) -> tuple[str, float, float]:
    dur = probe_duration(mp4_path)
    if not has_audio_stream(mp4_path):
        return ("", 0.15, dur)
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
        st = max(0.0, words[0][0] - 0.14)
        # Generous +0.38s tail margin; if speech approaches end of clip, keep 100% of full_dur so ZERO words clip!
        raw_en = words[-1][1] + 0.38
        en = dur if (raw_en >= dur - 0.55) else min(dur, raw_en)
        if en - st >= 2.0:
            return (full_txt, st, en)
    return (full_txt, 0.08, dur)


def match_clips_to_ledger(shots: list[dict], model) -> list[tuple[dict, Path, float, float]]:
    groups: dict[tuple[str, str], list[dict]] = {}
    for sh in shots:
        groups.setdefault((sh["batch_id"], sh["file_prefix"]), []).append(sh)

    resolved = {}
    for (bsub, pref), rows in groups.items():
        bdir = CLIPS_ROOT / bsub
        mp4s = sorted(bdir.glob(f"{pref}_*.mp4"))
        if not mp4s:
            raise FileNotFoundError(f"Missing clips for {bsub}/{pref} in {bdir}")
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
            print(f"  [{pref}] {mp4.name}: speech=({sp_st:.2f}..{sp_en:.2f}s) txt='{txt[:85]}'", flush=True)

        for row in rows:
            sid = row["slot_id"]
            kws = row["keywords"]
            best_c = None
            best_score = -1
            for c in candidates:
                if c["used"]:
                    continue
                hay = c["txt"] + " " + c["lbl"]
                score = sum(3 for kw in kws if kw.lower() in hay)
                if sid.lower() in hay:
                    score += 8
                if len(c["txt"]) > 10:
                    score += 1
                if score > best_score:
                    best_score = score
                    best_c = c
            if best_c is not None:
                best_c["used"] = True
                resolved[sid] = (row, best_c["path"], best_c["sp_st"], best_c["sp_en"])

        unused = [c for c in candidates if not c["used"]]
        for row in rows:
            sid = row["slot_id"]
            if sid not in resolved:
                chosen = unused.pop(0) if unused else candidates[0]
                resolved[sid] = (row, chosen["path"], chosen["sp_st"], chosen["sp_en"])

    return [resolved[sh["slot_id"]] for sh in shots]


def render_cold_open(out_mp4: Path) -> float:
    """Renders the 11.2s Opening Sequence WITH the sung Introductory 7D Theme Song (`3.0s..14.2s`)!"""
    stage_img = STAGES_DIR / "s01e01_sb_scene01_opening_trinity.jpg"
    if not stage_img.exists():
        stage_img = MASTERS_DIR / "v8_pilot_7d_scorecard_stage_16x9.jpg"
    portal_img = EP_DIR / "storyboard" / "sb_08_white_wall_portal_transition.jpg"

    c1, c2 = TEMP_DIR / "co_01.mp4", TEMP_DIR / "co_02.mp4"
    d1 = 6.70
    d2 = 4.50
    tot = d1 + d2
    f1 = int(round(d1 * 30))
    f2 = int(round(d2 * 30))

    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(stage_img),
        "-vf", (
            "scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,"
            f"zoompan=z='min(zoom+0.00063,1.10)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={f1}:s=1920x1080:fps=30,"
            "format=yuv420p"
        ),
        "-t", f"{d1:.2f}", *V_ENC, "-r", "30", "-video_track_timescale", "30000", "-an", str(c1)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(portal_img),
        "-vf", (
            "scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,"
            f"zoompan=z='min(zoom+0.00108,1.14)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={f2}:s=1920x1080:fps=30,"
            "format=yuv420p"
        ),
        "-t", f"{d2:.2f}", *V_ENC, "-r", "30", "-video_track_timescale", "30000", "-an", str(c2)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ct = TEMP_DIR / "co_concat.txt"
    ct.write_text(f"file '{c1}'\nfile '{c2}'\n", encoding="utf-8")
    co_vid = TEMP_DIR / "co_vid_only.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(ct), "-c", "copy", str(co_vid)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Mux sung Introductory 7D Theme Song (3.00s..14.20s) directly with smooth fade-in/out!
    subprocess.run([
        "ffmpeg", "-y", "-i", str(co_vid), "-ss", "3.00", "-i", str(THEME_WAV),
        "-filter_complex",
        f"[1:a]atrim=0:{tot:.3f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.45,afade=t=out:st={tot-0.85:.2f}:d=0.80,"
        "volume=0.88,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[aout]",
        "-map", "0:v", "-map", "[aout]", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return probe_duration(out_mp4)


def render_theme_interlude(spec: dict, out_mp4: Path) -> float:
    """
    Renders a ~9.2s Musical Act-Ending Interlude (~every 2 minutes) playing the sung
    Introductory Karmic Genie Show 7D Theme Song over a majestic Sacred Studio crane sweep!
    """
    trinity_img = STAGES_DIR / "s01e01_sb_scene01_opening_trinity.jpg"
    if not trinity_img.exists():
        trinity_img = MASTERS_DIR / "v8_pilot_7d_scorecard_stage_16x9.jpg"
    portal_img = EP_DIR / "storyboard" / "sb_08_white_wall_portal_transition.jpg"
    bg_img = portal_img if spec["bg"] == "portal" and portal_img.exists() else trinity_img

    dur = float(spec["dur"])
    ss = float(spec["theme_ss"])
    frames = int(round(dur * 30))

    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(bg_img),
        "-ss", f"{ss:.2f}", "-i", str(THEME_WAV),
        "-filter_complex", (
            f"[0:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,"
            f"zoompan=z='min(zoom+0.00075,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps=30,"
            f"fade=t=in:st=0:d=0.45,fade=t=out:st={dur-0.55:.2f}:d=0.50,format=yuv420p[vout];"
            f"[1:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:st=0:d=0.55,afade=t=out:st={dur-0.85:.2f}:d=0.80,"
            "volume=0.86,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[aout]"
        ),
        "-map", "[vout]", "-map", "[aout]",
        "-t", f"{dur:.2f}", *V_ENC, "-r", "30", "-video_track_timescale", "30000",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return probe_duration(out_mp4)


def clean_logo_pure_white(src_logo: Path, dst_png: Path) -> Path:
    from PIL import Image
    im = Image.open(src_logo).convert("RGB")
    arr = np.array(im, dtype=np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    chroma = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    lum = (r + g + b) / 3.0
    arr[(chroma < 14.0) & (lum > 195.0)] = 255.0
    Image.fromarray(arr.astype(np.uint8)).save(dst_png)
    return dst_png


def render_finale_outro(out_mp4: Path) -> float:
    """Renders the 10.0s Pure-White Logo Finale WITH the closing 7D Theme Chorus (`50.5s..60.5s`)!"""
    d_out = 10.00
    frames = int(round(d_out * 30))
    pure_logo = clean_logo_pure_white(LOGO_JPG, TEMP_DIR / "logo_pure_white.png")
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(pure_logo),
        "-ss", "50.50", "-i", str(THEME_WAV),
        "-filter_complex", (
            f"[0:v]scale=880:880:force_original_aspect_ratio=decrease,"
            "pad=1920:1080:(ow-iw)/2:(oh-ih)/2-36:color=white,"
            f"zoompan=z='min(zoom+0.00036,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps=30,"
            "format=yuv420p[vout];"
            f"[1:a]atrim=0:{d_out:.3f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:st=0:d=0.55,afade=t=out:st={d_out-1.10:.2f}:d=1.05,"
            "volume=0.86,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[aout]"
        ),
        "-map", "[vout]", "-map", "[aout]",
        "-t", f"{d_out:.2f}", *V_ENC, "-r", "30", "-video_track_timescale", "30000",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return probe_duration(out_mp4)


def render_shot_worker(task: dict) -> tuple[int, Path, float]:
    idx = task["idx"]
    row = task["row"]
    src_mp4 = task["src_mp4"]
    sp_st = task["sp_st"]
    sp_en = task["sp_en"]
    out_mp4 = TEMP_DIR / f"part_{idx:02d}_{row['slot_id']}.mp4"

    sid = row["slot_id"]
    mode = row["speaker_mode"]
    ov_name = row["overlay_png"]
    pause_s = min(0.32, float(row.get("pause_after_s", 0.24)) / SHOW_TEMPO)

    full_dur = probe_duration(src_mp4)
    min_st = SLOT_MIN_TRIM_START.get(sid, 0.0)
    trim_st = max(min_st, max(0.0, sp_st))
    # Never cut off the end of speech: keep full_dur whenever sp_en is within 0.60s of clip end
    if sp_en >= full_dur - 0.60:
        trim_en = full_dur
    else:
        trim_en = min(full_dur, max(trim_st + 2.2, sp_en))

    raw_clip_dur = max(1.2, trim_en - trim_st)
    slowed_speech_dur = raw_clip_dur / SHOW_TEMPO
    seg_dur = slowed_speech_dur + pause_s

    is_full = sid in FULLSCREEN_SLOTS
    close_up = is_full and (idx % 2 == 0) and mode != "genie"

    stage_bg = STAGES_DIR / "s01e01_sb_scene01_opening_trinity.jpg"
    if not stage_bg.exists():
        stage_bg = MASTERS_DIR / "v8_pilot_7d_scorecard_stage_16x9.jpg"

    tempo_filter = (
        f"rubberband=tempo={SHOW_TEMPO}:pitch=1.0:formant=preserved"
        if USE_RUBBERBAND
        else f"atempo={SHOW_TEMPO}"
    )
    fade_out_st = max(0.2, slowed_speech_dur - 0.08)
    a_chain = (
        f"atrim={trim_st:.3f}:{trim_en:.3f},asetpts=PTS-STARTPTS,"
        f"{tempo_filter},"
        "highpass=f=75,lowpass=f=13500,"
        f"afade=t=in:st=0:d=0.05,afade=t=out:st={fade_out_st:.3f}:d=0.08,"
        f"apad=pad_dur={pause_s:.3f},aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"
    )

    ov_path = (OVERLAYS_DIR / ov_name) if (ov_name and (OVERLAYS_DIR / ov_name).exists()) else None
    tk_path = (OVERLAYS_DIR / f"{Path(ov_name).stem}_ticker.png") if ov_path else None
    if tk_path and not tk_path.exists():
        tk_path = None

    if is_full:
        if close_up:
            scale_crop = "scale=2342:1318:force_original_aspect_ratio=increase,crop=1920:1080:x='(iw-1920)/2':y='(ih-1080)*0.30'"
        else:
            scale_crop = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"
        v_core = (
            f"trim={trim_st:.3f}:{trim_en:.3f},setpts=(PTS-STARTPTS)/{SHOW_TEMPO},fps=30,"
            f"{scale_crop},tpad=stop_mode=clone:stop_duration={pause_s:.3f},setsar=1,format=yuv420p"
        )
        cmd = ["ffmpeg", "-y", "-i", str(src_mp4)]
        if ov_path and tk_path:
            cmd += [
                "-loop", "1", "-t", f"{seg_dur:.3f}", "-i", str(ov_path),
                "-loop", "1", "-t", f"{seg_dur:.3f}", "-i", str(tk_path),
                "-filter_complex",
                f"[0:v]{v_core}[vb];"
                f"[1:v][2:v]overlay=x='1920-mod(t*185,1920+w)':y=1043:format=auto,"
                f"fade=t=in:st=0.10:d=0.25:alpha=1,fade=t=out:st={max(1.0, seg_dur-0.40):.2f}:d=0.30:alpha=1[ov];"
                f"[vb][ov]overlay=0:0:format=auto,format=yuv420p[vout];[0:a]{a_chain}[aout]",
                "-map", "[vout]", "-map", "[aout]",
            ]
        elif ov_path:
            cmd += [
                "-loop", "1", "-t", f"{seg_dur:.3f}", "-i", str(ov_path),
                "-filter_complex",
                f"[0:v]{v_core}[vb];[1:v]fade=t=in:st=0.10:d=0.25:alpha=1,fade=t=out:st={max(1.0, seg_dur-0.40):.2f}:d=0.30:alpha=1[ov];"
                f"[vb][ov]overlay=0:0:format=auto,format=yuv420p[vout];[0:a]{a_chain}[aout]",
                "-map", "[vout]", "-map", "[aout]",
            ]
        else:
            cmd += ["-vf", v_core, "-af", a_chain]
    else:
        # pip75 Broadcast Compositing: 75% Story Window (1664x936 at y=28) leaving bottom 116px clear for Subtitles + 2-Line Rolling News Bar!
        bg_dir = 1 if idx % 2 == 0 else -1
        bg_x = (
            f"(iw-1920)*(0.18+0.64*(t/{seg_dur:.2f}))"
            if bg_dir > 0
            else f"(iw-1920)*(0.82-0.64*(t/{seg_dur:.2f}))"
        )
        fc = (
            f"[1:v]scale=2240:1260:force_original_aspect_ratio=increase,crop=1920:1080:x='{bg_x}':y='(ih-1080)*0.48',"
            f"trim=0:{seg_dur:.3f},setpts=PTS-STARTPTS,eq=brightness=-0.05:saturation=0.95,setsar=1,format=yuv420p[bg];"
            f"[0:v]trim={trim_st:.3f}:{trim_en:.3f},setpts=(PTS-STARTPTS)/{SHOW_TEMPO},fps=30,"
            f"scale=1656:928:force_original_aspect_ratio=increase,crop=1656:928,"
            f"tpad=stop_mode=clone:stop_duration={pause_s:.3f},"
            "pad=w=1664:h=936:x=4:y=4:color=#EBC670,setsar=1,format=yuv420p[pip];"
            "[bg][pip]overlay=(W-w)/2:28:shortest=1,format=yuv420p[st];"
        )
        cmd = [
            "ffmpeg", "-y", "-i", str(src_mp4),
            "-loop", "1", "-r", "30", "-t", f"{seg_dur + 0.2:.3f}", "-i", str(stage_bg),
        ]
        if ov_path and tk_path:
            cmd += [
                "-loop", "1", "-t", f"{seg_dur:.3f}", "-i", str(ov_path),
                "-loop", "1", "-t", f"{seg_dur:.3f}", "-i", str(tk_path),
                "-filter_complex",
                fc + f"[2:v][3:v]overlay=x='1920-mod(t*185,1920+w)':y=1043:format=auto,"
                     f"fade=t=in:st=0.10:d=0.25:alpha=1,fade=t=out:st={max(1.0, seg_dur-0.40):.2f}:d=0.30:alpha=1[ov];"
                     f"[st][ov]overlay=0:0:format=auto,format=yuv420p[vout];[0:a]{a_chain}[aout]",
                "-map", "[vout]", "-map", "[aout]",
            ]
        elif ov_path:
            cmd += [
                "-loop", "1", "-t", f"{seg_dur:.3f}", "-i", str(ov_path),
                "-filter_complex",
                fc + f"[2:v]fade=t=in:st=0.10:d=0.25:alpha=1,fade=t=out:st={max(1.0, seg_dur-0.40):.2f}:d=0.30:alpha=1[ov];"
                     f"[st][ov]overlay=0:0:format=auto,format=yuv420p[vout];[0:a]{a_chain}[aout]",
                "-map", "[vout]", "-map", "[aout]",
            ]
        else:
            cmd += [
                "-filter_complex", fc + f"[st]null[vout];[0:a]{a_chain}[aout]",
                "-map", "[vout]", "-map", "[aout]",
            ]

    cmd += [
        "-t", f"{seg_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
        *V_ENC, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return idx, out_mp4, probe_duration(out_mp4)


def build_master_ass(
    ass_path: Path,
    shot_timings: list[dict],
    interlude_timings: list[dict],
    cold_dur: float,
    finale_start: float,
    total_dur: float,
):
    # MarginV=92 lifts spoken single-line subtitles cleanly above the 76px bottom News-Channel Rolling Bar!
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TitleGold,Liberation Sans,34,&H00B8F2FF,&H00B8F2FF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.6,0,3,11.0,0.0,2,60,60,44,1
Style: CinemaWhite,Liberation Sans,30,&H00FFFFFF,&H00FFFFFF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.2,0,3,10.0,0.0,2,48,48,92,1
Style: GenieSaintGold,Liberation Sans,31,&H00B8F2FF,&H00B8F2FF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.2,0,3,10.0,0.0,2,48,48,92,1
Style: InterludeBanner,Liberation Sans,31,&H009CE6FF,&H009CE6FF,&H420A1428,&H420A1428,-1,0,0,0,100,100,0.5,0,3,11.0,0.0,2,60,60,52,1
Style: OutroSubtle,Liberation Sans,25,&H00486885,&H00486885,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,0.6,0,1,0.0,0.0,2,80,80,34,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = [
        "Dialogue: 0,0:00:00.45,0:00:05.60,TitleGold,,0,0,0,,THE KARMIC GENIE SHOW  •  S01E01: 1. RESPECT YOUR DUTY FIRST.",
        f"Dialogue: 0,0:00:05.80,{format_ass_time(cold_dur - 0.30)},InterludeBanner,,0,0,0,,♪  The 7D Way — Duty • Dharma • Divine • Discipline • Dignity • Devout • Destiny  ♪",
    ]

    for il in interlude_timings:
        s0 = il["abs_start"]
        s1 = il["abs_end"]
        mid = s0 + (s1 - s0) * 0.50
        events.append(
            f"Dialogue: 0,{format_ass_time(s0 + 0.35)},{format_ass_time(mid - 0.10)},TitleGold,,0,0,0,,{il['title']}"
        )
        events.append(
            f"Dialogue: 0,{format_ass_time(mid + 0.05)},{format_ass_time(s1 - 0.35)},InterludeBanner,,0,0,0,,{il['sub']}"
        )

    for st in shot_timings:
        chunks = split_single_line_chunks(st["lines"], max_chars=64)
        if not chunks:
            continue
        style = "GenieSaintGold" if st["mode"] == "genie" else "CinemaWhite"
        sp_s = st["abs_start"] + 0.06
        sp_e = max(sp_s + 0.80, st["abs_end"] - 0.10)
        tot_chars = max(1, sum(len(c) for c in chunks))
        cur = sp_s
        for i, c in enumerate(chunks):
            dur_c = (sp_e - sp_s) * (len(c) / tot_chars)
            nxt = sp_e if i == len(chunks) - 1 else (cur + dur_c)
            events.append(
                f"Dialogue: 0,{format_ass_time(cur)},{format_ass_time(max(cur + 0.35, nxt - 0.03))},{style},,0,0,0,,{c}"
            )
            cur = nxt

    events.append(
        f"Dialogue: 0,{format_ass_time(finale_start + 0.5)},{format_ass_time(total_dur - 0.6)},OutroSubtle,,0,0,0,,"
        "Respect Your DUTY First • Earn with DIGNITY Always • Practice Life DISCIPLINE • Live the 7D Way"
    )
    ass_path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")


def main():
    t_start = time.time()
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    print(f"🚀 Karmic Genie Show S01E01 v3 Colab GPU Builder | NVENC={USE_NVENC}", flush=True)

    shots = json.loads(LEDGER_JSON.read_text(encoding="utf-8"))["shots"]

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("📦 Installing faster-whisper on Colab VM...", flush=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "faster-whisper"], check=True)
        from faster_whisper import WhisperModel

    print("🎙️ Loading faster-whisper ('small.en' int8 on 8-core CPU; L4 GPU dedicated to h264_nvenc)...", flush=True)
    model = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=8)

    print("1️⃣ Aligning 48 Google Flow clips (`DF01..DF48`) via Whisper speech timestamps...", flush=True)
    matched = match_clips_to_ledger(shots, model)

    print("2️⃣ Rendering 16:9 7D Cold Open, 3 Musical Act-Ending Theme Interludes (~every 2m) & Finale Card...", flush=True)
    co_mp4 = TEMP_DIR / "part_00_cold_open.mp4"
    fin_mp4 = TEMP_DIR / "part_99_finale_logo.mp4"
    cold_dur = render_cold_open(co_mp4)
    fin_dur = render_finale_outro(fin_mp4)

    rendered_interludes: dict[str, tuple[Path, float, dict]] = {}
    for after_sid, il_spec in ACT_BREAK_INTERLUDES.items():
        il_p = TEMP_DIR / f"part_{il_spec['id']}.mp4"
        il_d = render_theme_interlude(il_spec, il_p)
        rendered_interludes[after_sid] = (il_p, il_d, il_spec)
        print(f"    🎵 Rendered 7D Theme Interlude after {after_sid}: {il_p.name} ({il_d:.2f}s)", flush=True)

    print("3️⃣ Parallel GPU compositing 48 cinema, pip75 & 2-line Rolling News Ticker shots (0.90x tempo)...", flush=True)
    tasks = [
        {"idx": idx, "row": row, "src_mp4": src_mp4, "sp_st": sp_st, "sp_en": sp_en}
        for idx, (row, src_mp4, sp_st, sp_en) in enumerate(matched, 1)
    ]
    results = [None] * len(tasks)
    with ThreadPoolExecutor(max_workers=6) as ex:
        for idx, out_p, d in ex.map(render_shot_worker, tasks):
            results[idx - 1] = (out_p, d)
            if idx % 6 == 0 or idx == len(tasks):
                print(f"    • [NVENC] Rendered {idx:02d}/48 shots ({tasks[idx-1]['row']['slot_id']}: {d:.2f}s)", flush=True)

    parts = [co_mp4]
    cursor = cold_dur
    shot_timings = []
    interlude_timings = []
    music_windows = [(0.0, cold_dur)]

    for idx, (out_p, d) in enumerate(results):
        row = tasks[idx]["row"]
        sid = row["slot_id"]
        shot_timings.append({
            "sid": sid,
            "mode": row["speaker_mode"],
            "lines": row["subtitles"],
            "abs_start": cursor,
            "abs_end": cursor + d,
        })
        parts.append(out_p)
        cursor += d

        if sid in rendered_interludes:
            il_p, il_d, il_spec = rendered_interludes[sid]
            print(f"    ⏱️  Act-Ending 7D Theme Song Interlude after {sid} placed at {int(cursor//60):02d}:{cursor%60:05.2f}!", flush=True)
            interlude_timings.append({
                "after_sid": sid,
                "title": il_spec["title"],
                "sub": il_spec["sub"],
                "abs_start": cursor,
                "abs_end": cursor + il_d,
            })
            music_windows.append((cursor, cursor + il_d))
            parts.append(il_p)
            cursor += il_d

    finale_start = cursor
    parts.append(fin_mp4)
    music_windows.append((finale_start, finale_start + fin_dur + 2.0))

    concat_txt = TEMP_DIR / "master_concat.txt"
    concat_txt.write_text("\n".join(f"file '{p}'" for p in parts) + "\n", encoding="utf-8")
    stitched_mp4 = TEMP_DIR / "stitched_master_raw.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(stitched_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    actual_total = probe_duration(stitched_mp4)
    print(f"4️⃣ Stitched timeline duration: {actual_total:.2f}s ({actual_total/60:.2f} mins)", flush=True)

    ass_path = TEMP_DIR / "s01e01_duty_first_master_v3.ass"
    build_master_ass(ass_path, shot_timings, interlude_timings, cold_dur, finale_start, actual_total)

    # Because Cold Open, the 3 Musical Act-Break Interludes, and Finale ALREADY contain crisp foreground
    # slices of `THEME_WAV`, mute the soft instrumental bed (`0.0`) inside `music_windows` so it never
    # double-plays against the foreground sung theme song, while keeping `0.032` warm bed under spoken dialogue!
    conds = " + ".join(f"between(t,{w0:.2f},{w1:.2f})" for (w0, w1) in music_windows)
    vol_expr = f"if(gt({conds},0), 0.0, 0.032)"

    if shutil.which("fc-match"):
        m = subprocess.check_output(["fc-match", "Liberation Sans"]).decode().lower()
        if "liberation" not in m and "dejavu" not in m:
            subprocess.run(["apt-get", "update", "-qq"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["apt-get", "install", "-y", "-qq", "fonts-liberation", "fonts-dejavu-core"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("5️⃣ Burning BorderStyle=3 dark-shaded subtitles + -14 LUFS 7D Theme master encode on L4 NVENC...", flush=True)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(stitched_mp4),
        "-ss", "4.00", "-stream_loop", "-1", "-i", str(THEME_WAV),
        "-filter_complex", (
            f"[0:v]ass={ass_path},fade=t=in:st=0:d=0.60,fade=t=out:st={actual_total-1.00:.2f}:d=0.95[vout];"
            f"[1:a]atrim=0:{actual_total:.3f},asetpts=PTS-STARTPTS,lowpass=f=8500,volume='{vol_expr}':eval=frame[bgm];"
            f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
        ),
        "-map", "[vout]", "-map", "[aout]",
        "-t", f"{actual_total:.3f}", "-r", "30",
        *V_ENC, "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-movflags", "+faststart", str(OUT_MASTER_MP4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("6️⃣ Encoding <95 MB web-streaming 1080p MP4 on NVENC...", flush=True)
    W_ENC = (
        ["-c:v", "h264_nvenc", "-preset", "p5", "-b:v", "1600k", "-maxrate", "2050k", "-bufsize", "4100k"]
        if USE_NVENC
        else ["-c:v", "libx264", "-preset", "fast", "-b:v", "1600k", "-maxrate", "2050k", "-bufsize", "4100k"]
    )
    subprocess.run([
        "ffmpeg", "-y", "-i", str(OUT_MASTER_MP4),
        *W_ENC, "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(OUT_WEB_MP4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    elapsed = time.time() - t_start
    print(f"\n🏆 S01E01 '1. RESPECT YOUR DUTY FIRST.' v3 COLAB L4 MASTER READY in {elapsed:.1f}s!")
    print(f"   • Master 1080p: {OUT_MASTER_MP4} ({OUT_MASTER_MP4.stat().st_size/1e6:.2f} MB)")
    print(f"   • Web 1080p:    {OUT_WEB_MP4} ({OUT_WEB_MP4.stat().st_size/1e6:.2f} MB)")
    print(f"   • Runtime:      {int(actual_total//60):02d}:{actual_total%60:05.2f} ({actual_total:.2f}s)", flush=True)


if __name__ == "__main__":
    main()
