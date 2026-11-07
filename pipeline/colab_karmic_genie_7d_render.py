#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Karmic Genie Show — Remote Google Colab L4 GPU Renderer (`h264_nvenc` + 8-Thread Parallelism)
===============================================================================================
Renders both:
  1. `Karmic_Genie_Show_S01E01_Respect_Your_DUTY_First_360p.mp4` (and optional `1080p` master)
  2. `Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_360p.mp4` (and optional `1080p` master)
entirely on Google Colab GPU (`h264_nvenc`) with ZERO load on the local Linux machine!

Usage in Google Colab:
  !python3 "/content/drive/MyDrive/GuruKulaDesam/Tools/colab_karmic_genie_7d_render.py"
"""

import json
import os
import shutil
import subprocess
import sys
import tarfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# 1. Detect Google Drive Root in Colab
POSSIBLE_DRIVE_ROOTS = [
    Path("/content/drive/MyDrive/Karmic_Genie_Show_S01E01"),
    Path("/content/drive/My Drive/Karmic_Genie_Show_S01E01"),
    Path("/content/drive/MyDrive/GuruKulaDesam/Karmic_Genie_Show_S01E01"),
]

DRIVE_DIR = None
for p in POSSIBLE_DRIVE_ROOTS:
    if p.exists():
        DRIVE_DIR = p
        break

if DRIVE_DIR is None and Path("/content/drive").exists():
    for r, dirs, files in os.walk("/content/drive"):
        if "karmic_genie_7d_colab_bundle.tar.gz" in files:
            DRIVE_DIR = Path(r)
            break

if DRIVE_DIR is None:
    raise RuntimeError(
        "Could not locate 'Karmic_Genie_Show_S01E01' or 'karmic_genie_7d_colab_bundle.tar.gz' in /content/drive! "
        "Please mount Google Drive first: from google.colab import drive; drive.mount('/content/drive')"
    )

print(f"✅ Found Google Drive project folder: {DRIVE_DIR}", flush=True)

WORK_DIR = Path("/content/karmic_genie_7d_work")
BUNDLE_DIR = WORK_DIR / "karmic_genie_7d_colab_bundle"
TEMP_SEG_DIR = WORK_DIR / "segments"
WORK_DIR.mkdir(parents=True, exist_ok=True)
TEMP_SEG_DIR.mkdir(parents=True, exist_ok=True)

TAR_PATH = DRIVE_DIR / "karmic_genie_7d_colab_bundle.tar.gz"
if not (BUNDLE_DIR / "manifest.json").exists():
    print(f"📦 Extracting {TAR_PATH} to {WORK_DIR}...", flush=True)
    with tarfile.open(TAR_PATH, "r:gz") as tf:
        tf.extractall(WORK_DIR)


def has_nvenc() -> bool:
    try:
        out = subprocess.check_output(["ffmpeg", "-hide_banner", "-encoders"], stderr=subprocess.DEVNULL).decode()
        return "h264_nvenc" in out
    except Exception:
        return False


USE_NVENC = has_nvenc()
V_CODEC = ["-c:v", "h264_nvenc", "-preset", "p4", "-cq", "19"] if USE_NVENC else ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "20"]
print(f"🚀 Video Encoder Selected: {'NVIDIA GPU (h264_nvenc)' if USE_NVENC else 'CPU Fallback (libx264)'}", flush=True)


def probe_duration(path: Path) -> float:
    res = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)
    ]).decode())
    return float(res["format"]["duration"])


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


def build_ass_subtitles(ass_path: Path, timings: list[dict]):
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


def render_bookends(stage_jpg: Path, logo_jpg: Path) -> tuple[Path, Path]:
    co_mp4 = TEMP_SEG_DIR / "bookend_cold_open.mp4"
    fin_mp4 = TEMP_SEG_DIR / "bookend_finale_logo.mp4"
    if not co_mp4.exists():
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-r", "30", "-t", "5.00", "-i", str(stage_jpg),
            "-f", "lavfi", "-t", "5.00", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-vf", (
                "scale=2240:1260:force_original_aspect_ratio=increase,"
                "crop=1920:1080:x='(iw-1920)*(0.20+0.60*(t/5.0))':y='(ih-1080)*0.40',"
                "setsar=1,format=yuv420p"
            ),
            "-r", "30", "-video_track_timescale", "30000",
            *V_CODEC, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(co_mp4)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not fin_mp4.exists():
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-r", "30", "-t", "5.00", "-i", str(logo_jpg),
            "-f", "lavfi", "-t", "5.00", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-vf", (
                "scale=860:860:force_original_aspect_ratio=decrease,"
                "pad=1920:1080:(ow-iw)/2:(oh-ih)/2-36:color=white,"
                "setsar=1,format=yuv420p"
            ),
            "-r", "30", "-video_track_timescale", "30000",
            *V_CODEC, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(fin_mp4)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return co_mp4, fin_mp4


def render_single_segment_gpu(task: dict) -> tuple[int, Path, float]:
    idx = task["idx"]
    bid = task["bid"]
    video_clip = task["video_clip"]
    stage_jpg = task["stage_jpg"]
    audio_wav = task["audio_wav"]
    hud_png = task["hud_png"]
    target_dur = task["target_dur"]
    cam_dir = task["cam_dir"]

    out_mp4 = TEMP_SEG_DIR / f"seg_{bid}.mp4"
    if out_mp4.exists() and out_mp4.stat().st_size > 15000:
        return idx, out_mp4, probe_duration(out_mp4)

    v_dur = probe_duration(video_clip)
    ss = 0.25 if v_dur > 4.0 else 0.0

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
        "-loop", "1", "-r", "30", "-t", f"{target_dur + 0.15:.3f}", "-i", str(stage_jpg),
        "-i", str(audio_wav),
        "-loop", "1", "-r", "30", "-t", f"{target_dur + 0.15:.3f}", "-i", str(hud_png),
        "-filter_complex", (
            f"[1:v]scale=2160:1215:force_original_aspect_ratio=increase,crop=1920:1080:x='{bg_x}':y='(ih-1080)*0.50',"
            f"trim=0:{target_dur:.3f},setpts=PTS-STARTPTS,"
            "eq=brightness=-0.04:saturation=0.96,setsar=1,format=yuv420p[bg];"
            f"[0:v]trim=0:{target_dur:.3f},setpts=PTS-STARTPTS,fps=30,"
            f"scale=1520:855:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop=888:776:x='{crop_x}':y='(ih-776)*0.24',"
            "eq=contrast=1.03:saturation=1.04,"
            "pad=w=896:h=784:x=4:y=4:color=#EBC670,setsar=1,format=yuv420p[left_me];"
            "[bg][left_me]overlay=42:104:shortest=1,format=yuv420p[st];"
            f"[3:v]fade=t=in:st=0.06:d=0.18:alpha=1,fade=t=out:st={max(0.4, target_dur-0.22):.2f}:d=0.18:alpha=1[hud];"
            "[st][hud]overlay=0:0:format=auto,format=yuv420p[vout]"
        ),
        "-map", "[vout]", "-map", "2:a:0",
        "-t", f"{target_dur:.3f}", "-r", "30", "-video_track_timescale", "30000",
        *V_CODEC,
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(out_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return idx, out_mp4, probe_duration(out_mp4)


def render_episode_gpu(
    ep_label: str,
    beats: list[dict],
    pools: dict[str, list[Path]],
    stage_jpg: Path,
    logo_jpg: Path,
    theme_wav: Path,
    out_360p_name: str,
    out_1080p_name: str,
    render_1080p_also: bool = True,
):
    print(f"\n========================================================")
    print(f"🎬 Rendering {ep_label} on Remote Colab GPU ({len(beats)} beats)...")
    print(f"========================================================", flush=True)

    co_mp4, fin_mp4 = render_bookends(stage_jpg, logo_jpg)

    tasks = []
    h_idx, b_idx, g_idx = 0, 0, 0
    for idx, b in enumerate(beats):
        role = b["role"]
        bid = b["bid"]
        if role == "bala":
            v_clip = pools["bala"][b_idx % len(pools["bala"])]
            b_idx += 1
        elif role == "genie":
            v_clip = pools["genie"][g_idx % len(pools["genie"])]
            g_idx += 1
        else:
            v_clip = pools["host"][h_idx % len(pools["host"])]
            h_idx += 1

        aud_wav = BUNDLE_DIR / "audio" / f"aud_{bid}.wav"
        hud_png = BUNDLE_DIR / "hud_cards" / f"hud_{bid}.png"
        actual_a_dur = probe_duration(aud_wav)
        tasks.append({
            "idx": idx,
            "bid": bid,
            "role": role,
            "text": b["text"],
            "video_clip": v_clip,
            "stage_jpg": stage_jpg,
            "audio_wav": aud_wav,
            "hud_png": hud_png,
            "target_dur": actual_a_dur,
            "cam_dir": 1 if idx % 2 == 0 else -1,
        })

    seg_results = [None] * len(tasks)
    with ThreadPoolExecutor(max_workers=6) as ex:
        for idx, mp4_p, d in ex.map(render_single_segment_gpu, tasks):
            seg_results[idx] = (mp4_p, d)
            if (idx + 1) % 5 == 0 or idx == len(tasks) - 1:
                print(f"   • [GPU] Completed segment {idx+1:02d}/{len(tasks)} ({tasks[idx]['bid']})", flush=True)

    parts = [co_mp4]
    cursor = probe_duration(co_mp4)
    timings = []
    for idx, (mp4_p, seg_d) in enumerate(seg_results):
        timings.append({
            "bid": tasks[idx]["bid"],
            "role": tasks[idx]["role"],
            "text": tasks[idx]["text"],
            "start": cursor,
            "end": cursor + seg_d,
        })
        parts.append(mp4_p)
        cursor += seg_d

    fin_start = cursor
    parts.append(fin_mp4)

    concat_txt = TEMP_SEG_DIR / f"{ep_label}_concat.txt"
    concat_txt.write_text("\n".join(f"file '{p}'" for p in parts) + "\n", encoding="utf-8")
    stitched_mp4 = TEMP_SEG_DIR / f"{ep_label}_stitched_1080p.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-c", "copy", str(stitched_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    tot_dur = probe_duration(stitched_mp4)
    ass_path = TEMP_SEG_DIR / f"{ep_label}_subtitles.ass"
    build_ass_subtitles(ass_path, timings)
    vol_expr = f"if(lt(t,4.80), 0.52, if(gt(t,{fin_start-0.40:.2f}), 0.52, 0.036))"

    # 1. Final 360p Master
    out_360p = DRIVE_DIR / out_360p_name
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(stitched_mp4),
        "-ss", "4.00", "-stream_loop", "-1", "-i", str(theme_wav),
        "-filter_complex", (
            f"[0:v]ass={ass_path},fade=t=in:st=0:d=0.50,fade=t=out:st={tot_dur-0.80:.2f}:d=0.75,"
            "scale=640:360:flags=bicubic[vout];"
            f"[1:a]atrim=0:{tot_dur:.3f},asetpts=PTS-STARTPTS,lowpass=f=9000,volume='{vol_expr}':eval=frame[bgm];"
            "[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0,volume=1.45[aout]"
        ),
        "-map", "[vout]", "-map", "[aout]",
        "-t", f"{tot_dur:.3f}", "-r", "30",
        *V_CODEC, "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", str(out_360p)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"🏆 SAVED 360p TO GOOGLE DRIVE: {out_360p} ({tot_dur:.2f}s | {out_360p.stat().st_size/1e6:.2f} MB)", flush=True)

    # 2. Optional 1080p Broadcast Master on L4 GPU
    if render_1080p_also:
        out_1080p = DRIVE_DIR / out_1080p_name
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(stitched_mp4),
            "-ss", "4.00", "-stream_loop", "-1", "-i", str(theme_wav),
            "-filter_complex", (
                f"[0:v]ass={ass_path},fade=t=in:st=0:d=0.50,fade=t=out:st={tot_dur-0.80:.2f}:d=0.75[vout];"
                f"[1:a]atrim=0:{tot_dur:.3f},asetpts=PTS-STARTPTS,lowpass=f=9000,volume='{vol_expr}':eval=frame[bgm];"
                "[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0,volume=1.45[aout]"
            ),
            "-map", "[vout]", "-map", "[aout]",
            "-t", f"{tot_dur:.3f}", "-r", "30",
            *V_CODEC, "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart", str(out_1080p)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"🏆 SAVED 1080p TO GOOGLE DRIVE: {out_1080p} ({tot_dur:.2f}s | {out_1080p.stat().st_size/1e6:.2f} MB)", flush=True)


def main():
    manifest = json.loads((BUNDLE_DIR / "manifest.json").read_text(encoding="utf-8"))
    pools = {
        role: [BUNDLE_DIR / rel for rel in rel_list]
        for role, rel_list in manifest["pools"].items()
    }
    stage_jpg = BUNDLE_DIR / "assets" / "v8_pilot_7d_scorecard_stage_16x9.jpg"
    logo_jpg = BUNDLE_DIR / "assets" / "official_karmic_genie_show_logo.jpg"
    theme_wav = BUNDLE_DIR / "assets" / "official_karmic_genie_7d_theme_song.wav"

    render_1080p = "--360p-only" not in sys.argv

    render_episode_gpu(
        ep_label="S01E01_Respect_Your_DUTY_First",
        beats=manifest["s01e01_beats"],
        pools=pools,
        stage_jpg=stage_jpg,
        logo_jpg=logo_jpg,
        theme_wav=theme_wav,
        out_360p_name="Karmic_Genie_Show_S01E01_Respect_Your_DUTY_First_360p.mp4",
        out_1080p_name="Karmic_Genie_Show_S01E01_Respect_Your_DUTY_First_1080p.mp4",
        render_1080p_also=render_1080p,
    )

    render_episode_gpu(
        ep_label="S01E00_Pilot_The_7D_Way",
        beats=manifest["pilot_beats"],
        pools=pools,
        stage_jpg=stage_jpg,
        logo_jpg=logo_jpg,
        theme_wav=theme_wav,
        out_360p_name="Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_360p.mp4",
        out_1080p_name="Karmic_Genie_Show_S01E00_Pilot_The_7D_Way_1080p.mp4",
        render_1080p_also=render_1080p,
    )


if __name__ == "__main__":
    main()
