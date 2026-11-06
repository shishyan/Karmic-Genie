#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds the 70% Speed (-30% speed) Season 1, Episode 1 Vertical 9:16 Short:
  renders/Karmic_Genie_Show_S01E01_Tech_CEO_Short_70pct_9x16.mp4
Key engineering details:
  - Slows stitched_dialogue.mp4 cleanly to 70% speed (0.70x -> ~81.46s, well within YouTube's 3-min Shorts limit)
  - Uses `minterpolate=fps=30:mi_mode=blend` after `setpts=(1/0.70)*PTS` for smooth 30fps playback without frame judder
  - Uses `rubberband=tempo=0.70:pitchq=quality:formant=preserved:transients=smooth` so all voices keep natural human pitch & warmth
  - Softens high-mid harshness during the Karmic Genie's lines for a calmer, gentler tone
  - Mixes the Official 7D Theme Song at its natural 1.0x musical tempo (-23 dB gentle underscore)
  - Scales all verified caption timestamps cleanly by (1 / 0.70) with "SEASON 1 • EPISODE 1" opening title
"""

import json
import re
import subprocess
from pathlib import Path

BASE_DIR = Path("/home/shishyan/GitHub/Influenzian/Karmic_Genie_Show")
TEMP_DIR = BASE_DIR / "renders" / "temp_short_7d"
STITCHED_IN = TEMP_DIR / "stitched_dialogue.mp4"
SRC_ASS = TEMP_DIR / "captions_7d.ass"
OUT_ASS = TEMP_DIR / "captions_s01e01_70pct.ass"
THEME_WAV = BASE_DIR / "assets" / "official_karmic_genie_7d_theme_song.wav"
OUT_MP4 = BASE_DIR / "renders" / "Karmic_Genie_Show_S01E01_Tech_CEO_Short_70pct_9x16.mp4"

SPEED = 0.70
SCALE_FACTOR = 1.0 / SPEED  # 1.4285714286


def probe_duration(path: Path) -> float:
    res = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)
    ]).decode())
    return float(res["format"]["duration"])


def parse_ass_time(ts: str) -> float:
    h, m, s = ts.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def format_ass_time(sec: float) -> str:
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def build_scaled_ass():
    lines = SRC_ASS.read_text(encoding="utf-8").splitlines()
    out_lines = []
    first_dialogue_done = False
    for line in lines:
        if line.startswith("Dialogue:"):
            parts = line.split(",", 9)
            st = parse_ass_time(parts[1]) * SCALE_FACTOR
            en = parse_ass_time(parts[2]) * SCALE_FACTOR
            parts[1] = format_ass_time(st)
            parts[2] = format_ass_time(en)
            if not first_dialogue_done:
                parts[9] = r"SEASON 1  •  EPISODE 1\NKarmic Genie Show  —  The 7D Way"
                first_dialogue_done = True
            out_lines.append(",".join(parts))
        else:
            out_lines.append(line)
    OUT_ASS.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


def main():
    build_scaled_ass()
    orig_dur = probe_duration(STITCHED_IN)
    target_dur = orig_dur * SCALE_FACTOR
    print(f"Slowing S01E01 Short from {orig_dur:.2f}s (100%) -> {target_dur:.2f}s (70% speed)...")

    cold_end = 2.35 * SCALE_FACTOR
    outro_start = target_dur - 2.80
    vol_expr = f"if(lt(t,{cold_end:.2f}),0.52, if(gt(t,{outro_start:.2f}),0.38, 0.068))"

    # Step 1: Slow video + rubberband pitch/formant-preserved 0.70x dialogue
    slow_dialogue_mp4 = TEMP_DIR / "stitched_dialogue_70pct.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(STITCHED_IN),
        "-vf", f"setpts={SCALE_FACTOR:.6f}*PTS,minterpolate=fps=30:mi_mode=blend,format=yuv420p",
        "-af", "rubberband=tempo=0.70:pitchq=quality:formant=preserved:transients=smooth,lowpass=f=11500",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(slow_dialogue_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    actual_dur = probe_duration(slow_dialogue_mp4)

    # Step 2: Burn crisp 30fps captions + natural 1.0x 7D Theme Song underscore + gentle fade in/out
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(slow_dialogue_mp4),
        "-ss", "16.25", "-stream_loop", "-1", "-i", str(THEME_WAV),
        "-filter_complex",
        f"[0:v]ass={OUT_ASS},fade=t=in:st=0:d=0.45,fade=t=out:st={actual_dur-0.75:.2f}:d=0.70[vout];"
        f"[1:a]atrim=0:{actual_dur:.3f},asetpts=PTS-STARTPTS,volume='{vol_expr}':eval=frame[bgm];"
        f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]",
        "-map", "[vout]", "-map", "[aout]",
        "-t", f"{actual_dur:.3f}",
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(OUT_MP4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    fin_dur = probe_duration(OUT_MP4)
    print(f"🏆 S01E01 70%-SPEED SHORT READY: {OUT_MP4} ({fin_dur:.2f}s, {OUT_MP4.stat().st_size/1e6:.2f} MB)")


if __name__ == "__main__":
    main()
