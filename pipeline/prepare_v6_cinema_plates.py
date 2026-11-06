#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds the 4 ultra-crisp 2K (2752x1536 -> 1920x1080) v6 Padded-Logo 7D Stage Cinema Plates
for Karmic Genie Show S01E01:
  1) s4_03_v6_wall_punchline.mp4: @Me's real spoken audio from tu3_host_ivory_02.mp4 paired with
     a reverent slow crane push onto the exact v6 Padded-Logo 7D Stage Wall & dormant gold lamp.
  2) s6_05b_blessing_stillness.mp4: 4.6s contemplative golden close-up push on the cross-legged
     v6 Saintly Genie Master right after "while aging parents still wait...", letting the open
     reflection "Could this shock be a blessing in disguise?" breathe in stillness.
  3) s7_03_lotus_dissolve.mp4: 6.4s pixel-locked 2K cross-dissolve from v6_7d_saintly_genie_16x9.jpg
     (strictly cross-legged Genie) smoothly into v6_7d_dormant_stage_16x9.jpg (dormant gold lamp)
     so ONLY the cross-legged Genie dissolves peacefully back into the jeweled lamp!
  4) s7_05_v6_wall_signoff.mp4: @Me's real spoken audio from tu3_host_ivory_01.mp4 paired with
     a wide architectural glide across the v6 7D Stage Wall ("Purposeful Life Is Your DESTINY.").
"""

import json
import subprocess
from pathlib import Path

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
MASTERS_DIR = REPO_DIR / "assets" / "studio_v5_masters"
DORMANT_IMG = MASTERS_DIR / "v6_7d_dormant_stage_16x9.jpg"
SAINTLY_IMG = MASTERS_DIR / "v6_7d_saintly_genie_16x9.jpg"
TU_DIR = REPO_DIR / "episodes" / "S01E01_Employees_vs_Tech_CEO" / "flow_16x9_clips" / "topup_clean"


def probe_dur(p: Path) -> float:
    res = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(p)
    ]).decode())
    return float(res["format"]["duration"])


def main():
    TU_DIR.mkdir(parents=True, exist_ok=True)

    # 1) S4_03: @Me voice ("Let's quiet the room and ask together: What does Genie say — the 7D way?")
    # over slow push into the v6 7D Wall & Dormant Gold Lamp
    src_s403 = TU_DIR / "tu3_host_ivory_02.mp4"
    d_s403 = probe_dur(src_s403)
    frames_s403 = int(round(d_s403 * 30)) + 5
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(DORMANT_IMG),
        "-i", str(src_s403),
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='1.18+0.16*(on/{frames_s403})':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.44':d={frames_s403}:s=1920x1080:fps=30,"
            "format=yuv420p"
        ),
        "-map", "0:v:0", "-map", "1:a:0",
        "-t", f"{d_s403:.3f}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-c:a", "aac", "-b:a", "192k",
        str(TU_DIR / "plate_s4_03_punchline.mp4")
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ Built plate_s4_03_punchline.mp4")

    # 2) S6_05b: 4.6s contemplative golden close-up push on cross-legged v6 Saintly Genie Master
    d_s605b = 4.60
    frames_605 = int(round(d_s605b * 30))
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(SAINTLY_IMG),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='1.28+0.09*(on/{frames_605})':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.40':d={frames_605}:s=1920x1080:fps=30,"
            "format=yuv420p"
        ),
        "-t", f"{d_s605b:.2f}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        str(TU_DIR / "plate_s6_05b_blessing.mp4")
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ Built plate_s6_05b_blessing.mp4")

    # 3) S7_03: 6.4s pixel-registered cross-dissolve from cross-legged v6 Saintly Genie -> v6 Dormant Lamp!
    # Both share identical studio geometry, so xfade dissolves ONLY the cross-legged Genie into the lamp!
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-t", "4.40", "-i", str(SAINTLY_IMG),
        "-loop", "1", "-t", "4.80", "-i", str(DORMANT_IMG),
        "-f", "lavfi", "-t", "6.40", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-filter_complex",
        (
            "[0:v]scale=2200:1238:force_original_aspect_ratio=increase,crop=1920:1080:140:70,fps=30,format=yuv420p[v0];"
            "[1:v]scale=2200:1238:force_original_aspect_ratio=increase,crop=1920:1080:140:70,fps=30,format=yuv420p[v1];"
            "[v0][v1]xfade=transition=fade:duration=2.80:offset=1.60,"
            "zoompan=z='1.0+0.04*(on/192)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30,"
            "format=yuv420p[vout]"
        ),
        "-map", "[vout]", "-map", "2:a:0",
        "-t", "6.40",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-c:a", "aac", "-b:a", "192k",
        str(TU_DIR / "plate_s7_03_lotus_dissolve.mp4")
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ Built plate_s7_03_lotus_dissolve.mp4")

    # 4) S7_05: @Me voice ("Only you know your quiet thunder tonight. What does Genie say — the 7D way?")
    # over gentle pull-back revealing the full v6 7D Stage Wall & elevated hushed stadium
    src_s705 = TU_DIR / "tu3_host_ivory_01.mp4"
    d_s705 = probe_dur(src_s705)
    frames_s705 = int(round(d_s705 * 30)) + 5
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(DORMANT_IMG),
        "-i", str(src_s705),
        "-vf", (
            "scale=2752:1536:force_original_aspect_ratio=increase,crop=2752:1536,"
            f"zoompan=z='1.28-0.18*(on/{frames_s705})':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.40':d={frames_s705}:s=1920x1080:fps=30,"
            "format=yuv420p"
        ),
        "-map", "0:v:0", "-map", "1:a:0",
        "-t", f"{d_s705:.3f}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-c:a", "aac", "-b:a", "192k",
        str(TU_DIR / "plate_s7_05_signoff.mp4")
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ Built plate_s7_05_signoff.mp4")


if __name__ == "__main__":
    main()
