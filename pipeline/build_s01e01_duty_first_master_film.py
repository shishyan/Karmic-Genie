#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Widescreen (16:9, 1920x1080, 30fps, -14 LUFS) Film Assembler for:
  The Karmic Genie Show — Season 1, Episode 1 (~07:45 Full Epic Movie)
  "1. RESPECT YOUR DUTY FIRST." (The 7D Way — Virtues & Divinity Series)

Architecture:
  1. Loads the single-source-of-truth 48-shot ledger (`s01e01_48_shot_flow_ledger.json`) exported by
     `generate_s01e01_duty_first_flow_clips.py` (never recycling clips from unrelated episodes).
  2. Deterministically maps every downloaded Google Flow `.mp4` clip to its exact screenplay slot (`DF01..DF48`)
     via `faster-whisper` word-timestamp speech fingerprinting regardless of Flow card completion order.
  3. Applies pitch/formant-preserved `rubberband` cinema pacing (`0.87x` human speakers, `0.84x` + warm saintly
     EQ for the cross-legged Celestial Maharishi Karmic Genie) + `minterpolate` 30fps frame blending.
  4. Composites top-left RGBA glass cinema badges (`ov_df_01..12_*.png`) and burns clean borderless ASS
     movie subtitles (`BorderStyle=1`) timed to exact speech boundaries.
  5. Prepends the Official 7D Theme Cold Open, mixes a gentle `-27.5 dB` meditative underscore beneath spoken
     scenes, appends the pure-white Jeweled-Lamp Logo Finale Card at `-14 LUFS`, and writes both:
       • Full Master (`renders/Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_Master_16x9.mp4`)
       • Web Portal Master (`docs/assets/videos/Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_Master_16x9.mp4`)

Usage:
  python3 pipeline/build_s01e01_duty_first_master_film.py --check   # Verify ledger, overlays, assets & clip status
  python3 pipeline/build_s01e01_duty_first_master_film.py           # Assemble the full 48-shot Google Flow film
"""

import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

REPO_DIR = Path(__file__).resolve().parent.parent
MASTERS_DIR = REPO_DIR / "assets" / "studio_v5_masters"
THEME_WAV = REPO_DIR / "assets" / "theme" / "official_karmic_genie_7d_theme_song.wav"
LOGO_JPG = REPO_DIR / "assets" / "logo" / "official_karmic_genie_show_logo.jpg"
EP_DIR = REPO_DIR / "episodes" / "S01E01_Respect_Your_Duty_First"
LEDGER_JSON = EP_DIR / "s01e01_48_shot_flow_ledger.json"
CLIPS_ROOT = EP_DIR / "flow_16x9_clips"
OVERLAYS_DIR = EP_DIR / "overlays"
TEMP_DIR = EP_DIR / "temp_film_build"

OUT_MASTER_MP4 = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_Master_16x9.mp4"
OUT_WEB_MP4 = REPO_DIR / "docs" / "assets" / "videos" / "Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_Master_16x9.mp4"


def load_shot_ledger() -> list[dict]:
    if not LEDGER_JSON.exists():
        subprocess.run(
            [sys.executable, str(REPO_DIR / "pipeline" / "generate_s01e01_duty_first_flow_clips.py"), "--export-ledger"],
            check=True,
        )
    data = json.loads(LEDGER_JSON.read_text(encoding="utf-8"))
    return data["shots"]


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


def check_readiness(shots: list[dict]) -> tuple[int, int]:
    """Prints complete pre-flight status of assets, overlays, and downloaded Google Flow MP4 clips."""
    print("=== S01E01 'RESPECT YOUR DUTY FIRST' MASTER FILM PRE-FLIGHT CHECK ===")
    for label, p in [
        ("7D Theme WAV", THEME_WAV),
        ("Official Logo JPG", LOGO_JPG),
        ("Dormant Stage Master", MASTERS_DIR / "v6_7d_dormant_stage_16x9.jpg"),
        ("Saintly Genie Master", MASTERS_DIR / "v6_7d_saintly_genie_16x9.jpg"),
        ("48-Shot Flow Ledger", LEDGER_JSON),
    ]:
        status = "OK" if p.exists() else "MISSING"
        print(f"  [{status}] {label}: {p.relative_to(REPO_DIR)}")

    missing_ov = [s["overlay_png"] for s in shots if s["overlay_png"] and not (OVERLAYS_DIR / s["overlay_png"]).exists()]
    if missing_ov:
        print(f"  Rendering {len(missing_ov)} missing overlay badges...")
        subprocess.run([sys.executable, str(REPO_DIR / "pipeline" / "render_s01e01_duty_first_overlays.py")], check=True)

    groups: dict[tuple[str, str], int] = {}
    for s in shots:
        key = (s["batch_id"], s["file_prefix"])
        groups[key] = groups.get(key, 0) + 1

    ready_clips = 0
    total_clips = len(shots)
    print("\n  Batch Clip Inventory (`episodes/S01E01_Respect_Your_Duty_First/flow_16x9_clips/`):")
    for (bid, pref), expected in groups.items():
        bdir = CLIPS_ROOT / bid
        found = len(list(bdir.glob(f"{pref}_*.mp4"))) if bdir.exists() else 0
        ready_clips += min(found, expected)
        mark = "✅" if found >= expected else "⏳"
        print(f"    {mark} {bid} / {pref}: {found}/{expected} Flow MP4 clips downloaded")

    print(f"\n  Total Genuine Google Flow Clips Ready: {ready_clips}/{total_clips}")
    return ready_clips, total_clips


def transcribe_clip(mp4_path: Path, model) -> tuple[str, float, float]:
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


def match_clips_to_ledger(shots: list[dict], model) -> list[tuple[dict, Path, float, float]]:
    groups: dict[tuple[str, str], list[dict]] = {}
    for sh in shots:
        groups.setdefault((sh["batch_id"], sh["file_prefix"]), []).append(sh)

    resolved = {}
    for (bsub, pref), rows in groups.items():
        bdir = CLIPS_ROOT / bsub
        mp4s = sorted(bdir.glob(f"{pref}_*.mp4"))
        if not mp4s:
            raise FileNotFoundError(
                f"Missing Google Flow clips for {bsub}/{pref} in {bdir}.\n"
                f"Run `python3 pipeline/generate_s01e01_duty_first_flow_clips.py {bsub}` first."
            )
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

        for row in rows:
            sid = row["slot_id"]
            kws = row["keywords"]
            if kws and kws[0].startswith("__VISUAL"):
                continue
            best_c = None
            best_score = -1
            for c in candidates:
                if c["used"]:
                    continue
                hay = c["txt"] + " " + c["lbl"]
                score = sum(3 for kw in kws if kw.lower() in hay)
                if sid.lower() in hay:
                    score += 5
                if len(c["txt"]) > 12:
                    score += 1
                if score > best_score:
                    best_score = score
                    best_c = c
            if best_c is not None:
                best_c["used"] = True
                resolved[sid] = (row, best_c["path"], best_c["sp_st"], best_c["sp_en"])

        unused = [c for c in candidates if not c["used"]]
        unused.sort(key=lambda x: len(x["txt"]))
        for row in rows:
            sid = row["slot_id"]
            if sid in resolved:
                continue
            chosen = unused.pop(0) if unused else candidates[0]
            resolved[sid] = (row, chosen["path"], chosen["sp_st"], chosen["sp_en"])

    return [resolved[sh["slot_id"]] for sh in shots]


def render_cold_open(out_mp4: Path) -> float:
    """Builds the 17.6s 16:9 7D Theme Cold Open (Dormant Stage Crane + 7D Wall Pan + White-Wall Portal)."""
    dormant_img = MASTERS_DIR / "v6_7d_dormant_stage_16x9.jpg"
    portal_img = EP_DIR / "storyboard" / "sb_08_white_wall_portal_transition.jpg"
    if not portal_img.exists():
        portal_img = dormant_img

    c1 = TEMP_DIR / "co_01.mp4"
    c2 = TEMP_DIR / "co_02.mp4"
    c3 = TEMP_DIR / "co_03.mp4"

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

    frames3 = int(round(4.2 * 30))
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", str(portal_img),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='min(zoom+0.0012,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames3}:s=1920x1080:fps=30,"
            "format=yuv420p"
        ),
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


def normalize_story_shot(row: dict, src_mp4: Path, out_mp4: Path) -> tuple[float, float]:
    mode = row["speaker_mode"]
    ov_name = row["overlay_png"]
    pause_s = float(row["pause_after_s"])
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


def build_master_ass(ass_path: Path, shot_timings: list[dict], finale_start: float, total_dur: float):
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
        "Dialogue: 0,0:00:00.80,0:00:05.20,TitleGold,,0,0,0,,THE KARMIC GENIE SHOW  •  SEASON 1, EPISODE 1",
        r"Dialogue: 0,0:00:05.40,0:00:11.40,CinemaWhite,,0,0,0,,1. RESPECT YOUR DUTY FIRST.\NThe 7D Way — Virtues, Conscience & Divine Peace",
        r"Dialogue: 0,0:00:11.60,0:00:17.10,TitleGold,,0,0,0,,Do Your Duty First  •  Do What Only You Can Do  •  Sleep in Peace",
    ]

    for st in shot_timings:
        lines = st["lines"]
        if not lines:
            continue
        style = "GenieSaintGold" if st["mode"] == "genie" else "CinemaWhite"
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
            total_chars = sum(max(1, len(x)) for x in lines)
            cur = sp_s
            for i, ln in enumerate(lines):
                frac = max(1, len(ln)) / total_chars
                nxt = sp_e if i == len(lines) - 1 else (cur + (sp_e - sp_s) * frac)
                events.append(f"Dialogue: 0,{format_ass_time(cur)},{format_ass_time(max(cur + 0.6, nxt - 0.04))},{style},,0,0,0,,{ln}")
                cur = nxt

    events.append(
        f"Dialogue: 0,{format_ass_time(finale_start + 0.8)},{format_ass_time(total_dur - 1.0)},OutroSubtle,,0,0,0,,"
        r"Respect Your DUTY First.  •  Earn with DIGNITY Always.  •  Practice Life DISCIPLINE.\N"
        r"Uphold Karmic DHARMA.  •  Raise Family with DEVOTION.  •  Be Grateful to Your DIVINE.  •  Purposeful Life Is Your DESTINY."
    )
    ass_path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")


def main():
    shots = load_shot_ledger()
    ready_cnt, total_cnt = check_readiness(shots)
    if "--check" in sys.argv or "--dry-run" in sys.argv:
        return

    if ready_cnt < total_cnt:
        raise SystemExit(
            f"\n⚠️  {total_cnt - ready_cnt} of {total_cnt} genuine Google Flow clips have not been generated yet.\n"
            "Run `python3 pipeline/generate_s01e01_duty_first_flow_clips.py` on your workstation with Chrome open at "
            "`https://flow.google.com/u/0/` (`--remote-debugging-port=9225`), then re-run this script!"
        )

    from faster_whisper import WhisperModel

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUT_MASTER_MP4.parent.mkdir(parents=True, exist_ok=True)
    OUT_WEB_MP4.parent.mkdir(parents=True, exist_ok=True)

    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")

    print("\n1️⃣ Matching all 48 generated Google Flow clips (`DF01..DF48`) to canonical screenplay ledger...", flush=True)
    matched = match_clips_to_ledger(shots, model)

    print("2️⃣ Rendering 16:9 7D Cold Open & Finale Logo Cards...", flush=True)
    co_mp4 = TEMP_DIR / "part_00_cold_open.mp4"
    cold_dur = render_cold_open(co_mp4)

    fin_mp4 = TEMP_DIR / "part_99_finale_logo.mp4"
    fin_dur = render_finale_outro(fin_mp4)

    print("3️⃣ Normalizing, pitch-preserving slowing & compositing badges across all 48 cinema shots...", flush=True)
    parts = [co_mp4]
    cursor = cold_dur
    shot_timings = []

    for idx, (row, src_mp4, sp_st, sp_en) in enumerate(matched, 1):
        out_p = TEMP_DIR / f"part_{idx:02d}_{row['slot_id']}.mp4"
        dur, tempo = normalize_story_shot(row, src_mp4, out_p)
        scale = 1.0 / tempo
        shot_timings.append({
            "sid": row["slot_id"],
            "mode": row["speaker_mode"],
            "lines": row["subtitles"],
            "abs_start": cursor,
            "abs_end": cursor + dur,
            "sp_st_scaled": sp_st * scale,
            "sp_en_scaled": sp_en * scale,
        })
        parts.append(out_p)
        cursor += dur
        print(f"    [{idx:02d}/48] {row['slot_id']} <- {src_mp4.name} ({dur:.2f}s, total={cursor:.1f}s)", flush=True)

    finale_start = cursor
    parts.append(fin_mp4)

    concat_txt = TEMP_DIR / "master_concat.txt"
    concat_txt.write_text("\n".join(f"file '{p}'" for p in parts) + "\n", encoding="utf-8")
    stitched_mp4 = TEMP_DIR / "stitched_master_raw.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy", str(stitched_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    actual_total = probe_duration(stitched_mp4)
    print(f"4️⃣ Stitched raw film duration: {actual_total:.2f}s ({actual_total/60:.2f} mins)", flush=True)

    ass_path = TEMP_DIR / "s01e01_duty_first_master.ass"
    build_master_ass(ass_path, shot_timings, finale_start, actual_total)

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
        str(OUT_MASTER_MP4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("6️⃣ Encoding <90 MB web-streaming copy for docs/assets/videos/...", flush=True)
    subprocess.run([
        "ffmpeg", "-y", "-i", str(OUT_MASTER_MP4),
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "25",
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
        str(OUT_WEB_MP4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    final_d = probe_duration(OUT_MASTER_MP4)
    print("\n🏆 S01E01 'RESPECT YOUR DUTY FIRST' 48-SHOT GOOGLE FLOW MASTER FILM READY!")
    print(f"   • Full Master: {OUT_MASTER_MP4} ({OUT_MASTER_MP4.stat().st_size/1e6:.2f} MB)")
    print(f"   • Web Master:  {OUT_WEB_MP4} ({OUT_WEB_MP4.stat().st_size/1e6:.2f} MB)")
    print(f"   • Runtime:     {int(final_d//60):02d}:{final_d%60:05.2f} ({final_d:.2f}s)", flush=True)


if __name__ == "__main__":
    main()
