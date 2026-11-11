#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master 48-Shot (`DF01..DF48`) Full-HD (1920x1080, 30fps, -14 LUFS) & Web-Streaming (1280x720)
Epic Movie Builder for The Karmic Genie Show — Season 1, Episode 1 (`S01E01`):
  "1. RESPECT YOUR DUTY FIRST." (The 7D Way — Virtues & Divinity Series)

Assembles the complete 14-Page, 48-Shot Episode 1 Movie:
  • Cold Open: Official 14s Google Flow 7D Theme Opener (`Karmic_Genie_Show_Official_7D_Theme_Opener_16x9.mp4`)
  • Shots DF01..DF48:
      - Stage, Portal, Parable & Celestial Genie shots use genuine moving Google Flow video clips
        (clean @Me ivory bandhgala stage clips, 4yo Bala-Rishi clips, Celestial Genie clips, Banyan/Conscience
        live-action parable clips, and animated Three Wise Eastern Philosophers / Conscience Bell clips).
      - Location parable shots (Monsoon Day 1/Day 2 scooter accident, 2:30 AM bedroom conscience, Porul & Arul
        home lamp, 7 'Only You Can Do' scenes, Dawn street cleaner Namaste, Rainy rescue & peaceful sleep)
        use `@Me`-referenced 16:9 cinema storyboard plates with smooth 30fps cinema camera motion + side-by-side
        Picture-in-Picture active Google Flow narrator video (`@Me` or `4yo Bala-Rishi`) so every single beat
        features live speaking actor motion!
  • Multi-character spoken voices (`@Me` Host, `4yo Bala-Rishi`, `Bala-Matha`, and `Celestial Maharishi Genie`)
    shaped with `rubberband` pitch/formant processing + gentle `-27 dB` 7D Theme underscore + `-14 LUFS` loudness.
  • Composites the 12 RGBA cinema glass badges (`ov_df_01..12_*.png`) and clean ASS movie subtitles.
  • Exports:
      1. `renders/Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_Master_16x9.mp4` (1920x1080 Master)
      2. `docs/assets/videos/Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_Master_16x9.mp4` (1280x720 Web)
      3. `renders/Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_360p.mp4` (640x360 Fast Preview)
"""

import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from gtts import gTTS
from PIL import Image, ImageDraw

REPO_DIR = Path(__file__).resolve().parent.parent
EP_DIR = REPO_DIR / "episodes" / "S01E01_Respect_Your_Duty_First"
LEDGER_JSON = EP_DIR / "s01e01_48_shot_flow_ledger.json"
OVERLAYS_DIR = EP_DIR / "overlays"
THEME_WAV = REPO_DIR / "assets" / "theme" / "official_karmic_genie_7d_theme_song.wav"
LOGO_JPG = REPO_DIR / "assets" / "logo" / "official_karmic_genie_show_logo.jpg"
OPENER_MP4 = REPO_DIR / "renders" / "Karmic_Genie_Show_Official_7D_Theme_Opener_16x9.mp4"

BUNDLE_ROOT = Path("/tmp/flow_bundle/karmic_genie_7d_colab_bundle")
PILOT_SRC_ROOT = Path("/tmp/flow_bundle/episodes/S01E00_Pilot_The_7D_Way")

TEMP_DIR = EP_DIR / "temp_duty_first_48shot_build"
AUD_DIR = TEMP_DIR / "audio"
SEG_DIR = TEMP_DIR / "segments"

OUT_MASTER_1080P = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_Master_16x9.mp4"
OUT_WEB_720P = REPO_DIR / "docs" / "assets" / "videos" / "Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_Master_16x9.mp4"
OUT_PREVIEW_360P = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_360p.mp4"

# Clean, verified genuine Google Flow live-action clips (zero rival show titles or unrelated tickers)
CLEAN_HOST_STAGE_CLIPS = [
    BUNDLE_ROOT / "clips/host/host_12_v3_phil_03.mp4",
    BUNDLE_ROOT / "clips/host/host_13_v3_gd_01.mp4",
    BUNDLE_ROOT / "clips/host/host_10_v3_phil_01.mp4",
    BUNDLE_ROOT / "clips/host/host_09_v3_b1_welcome_03.mp4",
    BUNDLE_ROOT / "clips/host/host_04_b2_host_d3_to_d7_details_05.mp4",
    BUNDLE_ROOT / "clips/host/host_06_b2_host_d3_to_d7_details_01.mp4",
    BUNDLE_ROOT / "clips/host/host_01_b1_host_compass_and_d1_d2_04.mp4",
]

CLEAN_BALA_CLIPS = [
    BUNDLE_ROOT / "clips/bala/bala_01_b3_bala_rishi_4yo_virtues_1_01.mp4",
    BUNDLE_ROOT / "clips/bala/bala_02_b3_bala_rishi_4yo_virtues_1_03.mp4",
    BUNDLE_ROOT / "clips/bala/bala_03_b3_bala_rishi_4yo_virtues_1_04.mp4",
    BUNDLE_ROOT / "clips/bala/bala_04_b3_bala_rishi_4yo_virtues_1_02.mp4",
    BUNDLE_ROOT / "clips/bala/bala_05_b4_bala_rishi_4yo_virtues_2_01.mp4",
    BUNDLE_ROOT / "clips/bala/bala_06_b4_bala_rishi_4yo_virtues_2_03.mp4",
    BUNDLE_ROOT / "clips/bala/bala_07_b4_bala_rishi_4yo_virtues_2_02.mp4",
]

CLEAN_GENIE_CLIPS = [
    BUNDLE_ROOT / "clips/genie/genie_00_flow_me_sample_01.mp4",
    BUNDLE_ROOT / "clips/genie/genie_01_flow_me_sample_02.mp4",
]

SPECIAL_FLOW_CLIPS = {
    "DF09": PILOT_SRC_ROOT / "flow_s01e00_clips/b5_conscience_parables/b5_conscience_parables_01.mp4",
    "DF28": PILOT_SRC_ROOT / "sketches_7d_philosophers/animated_parables/sketch_parable_d1_duty.mp4",
    "DF40": PILOT_SRC_ROOT / "sketches_7d_philosophers/animated_parables/sketch_d1_duty_2a.mp4",
}

STAGE_FULL_FLOW_SLOTS = {
    "DF07", "DF08", "DF09", "DF28",
    "DF37", "DF38", "DF39", "DF40", "DF41", "DF42",
    "DF43", "DF44", "DF45", "DF46", "DF47", "DF48",
}


def has_nvenc() -> bool:
    try:
        subprocess.run(
            [
                "ffmpeg", "-nostdin", "-hide_banner", "-v", "error",
                "-f", "lavfi", "-i", "color=black:s=128x128:d=0.05",
                "-c:v", "h264_nvenc", "-f", "null", "-",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception:
        return False


USE_NVENC = has_nvenc()
V_CODEC_SEG = (
    ["-c:v", "h264_nvenc", "-preset", "p4", "-cq", "19"]
    if USE_NVENC
    else ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19"]
)


def probe_duration(path: Path) -> float:
    res = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)
    ]).decode())
    return float(res["format"]["duration"])


def detect_speaker_role(shot: dict) -> str:
    slot = shot["slot_id"]
    vis = shot["visual"].lower()
    if shot.get("speaker_mode") == "genie" or slot in {"DF38", "DF39"}:
        return "genie"
    if slot in {"DF06", "DF16", "DF21", "DF30", "DF42", "DF46"} or any(
        k in vis for k in ["bala-matha speaks", "bala-matha whispers", "bala-matha asks"]
    ):
        return "bala_matha"
    if slot in {"DF02", "DF11", "DF18", "DF28", "DF41", "DF45"} or any(
        k in vis for k in ["bala-rishi speaks", "bala-rishi asks", "bala-rishi beams", "bala-rishi counts"]
    ):
        return "bala_rishi"
    return "host"


def synthesize_shot_audio(idx: int, shot: dict) -> tuple[Path, float, str]:
    slot = shot["slot_id"]
    role = detect_speaker_role(shot)
    out_wav = AUD_DIR / f"{slot}_{role}.wav"
    if out_wav.exists() and out_wav.stat().st_size > 8000:
        return out_wav, probe_duration(out_wav), role

    raw_mp3 = AUD_DIR / f"raw_{slot}.mp3"
    spoken_clean = (
        shot["spoken"]
        .replace("—", ", ")
        .replace("–", ", ")
        .replace("Porul", "Porul wealth")
        .replace("Illaram", "Illaram family dharma")
    )
    # Keep exact spoken text except em-dash pause smoothing
    spoken_tts = shot["spoken"].replace("—", ", ").replace("–", ", ")
    gTTS(spoken_tts, lang="en", tld="co.in", slow=False).save(str(raw_mp3))

    if role == "genie":
        rb = "tempo=0.98:pitch=0.84:formant=preserved"
        eq = "equalizer=f=140:width_type=o:width=1.2:g=3.2,equalizer=f=2800:width_type=o:width=1.0:g=1.5,aecho=0.8:0.88:35:0.12"
    elif role == "bala_rishi":
        rb = "tempo=1.08:pitch=1.20:formant=shifted"
        eq = "equalizer=f=260:width_type=o:width=1.2:g=1.4,equalizer=f=3600:width_type=o:width=1.0:g=1.8"
    elif role == "bala_matha":
        rb = "tempo=1.06:pitch=1.26:formant=shifted"
        eq = "equalizer=f=280:width_type=o:width=1.2:g=1.2,equalizer=f=3800:width_type=o:width=1.0:g=2.0"
    else:
        rb = "tempo=1.06:pitch=0.92:formant=preserved"
        eq = "equalizer=f=175:width_type=o:width=1.2:g=2.2,equalizer=f=3100:width_type=o:width=1.0:g=1.5"

    pause_s = float(shot.get("pause_after_s", 0.28))
    subprocess.run([
        "ffmpeg", "-nostdin", "-y", "-i", str(raw_mp3),
        "-af", (
            "silenceremove=start_periods=1:start_threshold=-42dB:stop_periods=-1:stop_duration=0.35:stop_threshold=-42dB,"
            f"rubberband={rb},{eq},highpass=f=75,lowpass=f=13500,"
            f"adelay=140|140,apad=pad_dur={pause_s + 0.18:.2f},"
            "aresample=48000,aformat=sample_fmts=s16:channel_layouts=stereo"
        ),
        str(out_wav),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_wav, probe_duration(out_wav), role


def make_rounded_pip_mask(w: int = 408, h: int = 230, radius: int = 22) -> tuple[Path, Path]:
    mask_png = TEMP_DIR / "pip_alpha_mask.png"
    frame_png = TEMP_DIR / "pip_gold_border.png"
    if not mask_png.exists():
        m = Image.new("L", (w, h), 0)
        d = ImageDraw.Draw(m)
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
        m.save(mask_png)
    if not frame_png.exists():
        fr = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
        df = ImageDraw.Draw(fr)
        df.rounded_rectangle([1, 1, w + 6, h + 6], radius=radius + 3, outline=(245, 196, 81, 235), width=3)
        fr.save(frame_png)
    return mask_png, frame_png


def format_ass_time(sec: float) -> str:
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def write_shot_ass(ass_path: Path, subtitles: list[str], role: str, dur: float):
    style_name = {
        "host": "HostStyle",
        "bala_rishi": "BalaRishiStyle",
        "bala_matha": "BalaMathaStyle",
        "genie": "GenieStyle",
    }.get(role, "HostStyle")

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HostStyle,DejaVu Sans,34,&H00FFFFFF,&H00FFFFFF,&H00101522,&H96080C16,-1,0,0,0,100,100,0.2,0,1,3.2,1.6,2,90,90,38,1
Style: BalaRishiStyle,DejaVu Sans,34,&H008CF2FF,&H008CF2FF,&H00101522,&H96080C16,-1,0,0,0,100,100,0.2,0,1,3.2,1.6,2,90,90,38,1
Style: BalaMathaStyle,DejaVu Sans,34,&H00D4B8FF,&H00D4B8FF,&H00101522,&H96080C16,-1,0,0,0,100,100,0.2,0,1,3.2,1.6,2,90,90,38,1
Style: GenieStyle,DejaVu Sans,35,&H0075E6FF,&H0075E6FF,&H000A1428,&H96080C16,-1,0,0,0,100,100,0.3,0,1,3.5,1.8,2,90,90,38,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    joined = "\\N".join(s.replace("{", "").replace("}", "") for s in subtitles if s.strip())
    ev = f"Dialogue: 0,{format_ass_time(0.10)},{format_ass_time(max(0.5, dur - 0.12))},{style_name},,0,0,0,,{joined}\n"
    ass_path.write_text(header + ev, encoding="utf-8")


def render_single_shot(idx: int, shot: dict, mask_png: Path, border_png: Path) -> tuple[int, Path, float]:
    slot = shot["slot_id"]
    seg_mp4 = SEG_DIR / f"seg_{idx:02d}_{slot}.mp4"
    aud_wav, dur, role = synthesize_shot_audio(idx, shot)
    if seg_mp4.exists() and seg_mp4.stat().st_size > 25000:
        return idx, seg_mp4, dur

    ass_path = TEMP_DIR / f"sub_{slot}.ass"
    write_shot_ass(ass_path, shot.get("subtitles") or [shot["spoken"]], role, dur)
    ass_esc = str(ass_path).replace("\\", "/").replace(":", "\\:")

    ov_name = shot.get("overlay_png")
    ov_path = (OVERLAYS_DIR / ov_name) if ov_name and (OVERLAYS_DIR / ov_name).exists() else None

    # Choose motion clip
    if slot in SPECIAL_FLOW_CLIPS and SPECIAL_FLOW_CLIPS[slot].exists():
        flow_mp4 = SPECIAL_FLOW_CLIPS[slot]
        use_full_flow = True
    elif slot in STAGE_FULL_FLOW_SLOTS:
        if role == "genie":
            flow_mp4 = CLEAN_GENIE_CLIPS[idx % len(CLEAN_GENIE_CLIPS)]
        elif role in {"bala_rishi", "bala_matha"}:
            flow_mp4 = CLEAN_BALA_CLIPS[idx % len(CLEAN_BALA_CLIPS)]
        else:
            flow_mp4 = CLEAN_HOST_STAGE_CLIPS[idx % len(CLEAN_HOST_STAGE_CLIPS)]
        use_full_flow = True
    else:
        use_full_flow = False
        if role in {"bala_rishi"}:
            flow_mp4 = CLEAN_BALA_CLIPS[idx % len(CLEAN_BALA_CLIPS)]
        else:
            flow_mp4 = CLEAN_HOST_STAGE_CLIPS[idx % len(CLEAN_HOST_STAGE_CLIPS)]

    fade_out_st = max(0.25, dur - 0.25)

    if use_full_flow:
        # Full-frame 100% genuine moving Google Flow clip (looped smoothly if shot audio > 8.04s)
        inputs = [
            "-stream_loop", "-1", "-i", str(flow_mp4),
            "-i", str(aud_wav),
        ]
        fc_parts = [
            f"[0:v]trim=duration={dur:.3f},setpts=PTS-STARTPTS,"
            "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,"
            "crop=1920:1080,fps=30,setsar=1,format=rgba[base]"
        ]
        cur_v = "[base]"
        if ov_path is not None:
            inputs.extend(["-loop", "1", "-t", f"{dur:.3f}", "-i", str(ov_path)])
            fc_parts.append("[2:v]format=rgba[ov];[base][ov]overlay=0:0[vov]")
            cur_v = "[vov]"
        fc_parts.append(
            f"{cur_v}ass='{ass_esc}',"
            f"fade=t=in:st=0:d=0.22,fade=t=out:st={fade_out_st:.3f}:d=0.22,format=yuv420p[vout]"
        )
        cmd = [
            "ffmpeg", "-nostdin", "-y",
            *inputs,
            "-filter_complex", ";".join(fc_parts),
            "-map", "[vout]", "-map", "1:a",
            *V_CODEC_SEG,
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-r", "30", "-t", f"{dur:.3f}",
            str(seg_mp4),
        ]
    else:
        # Cinematic 16:9 @Me Storyboard Plate with smooth 30fps camera drift + live speaking Google Flow PiP window!
        plate_jpg = REPO_DIR / shot["ref_image"]
        direction = idx % 4
        if direction == 0:
            x_expr = f"(iw-1920)*(0.18+0.64*(t/{dur:.3f}))"
            y_expr = "(ih-1080)*0.35"
        elif direction == 1:
            x_expr = f"(iw-1920)*(0.82-0.64*(t/{dur:.3f}))"
            y_expr = "(ih-1080)*0.40"
        elif direction == 2:
            x_expr = "(iw-1920)*0.50"
            y_expr = f"(ih-1080)*(0.22+0.55*(t/{dur:.3f}))"
        else:
            x_expr = f"(iw-1920)*(0.30+0.40*(t/{dur:.3f}))"
            y_expr = f"(ih-1080)*(0.65-0.40*(t/{dur:.3f}))"

        inputs = [
            "-loop", "1", "-r", "30", "-t", f"{dur:.3f}", "-i", str(plate_jpg),
            "-stream_loop", "-1", "-i", str(flow_mp4),
            "-loop", "1", "-t", f"{dur:.3f}", "-i", str(mask_png),
            "-loop", "1", "-t", f"{dur:.3f}", "-i", str(border_png),
            "-i", str(aud_wav),
        ]
        fc_parts = [
            f"[0:v]scale=2220:1249:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop=1920:1080:x='{x_expr}':y='{y_expr}',fps=30,setsar=1,format=rgba[bg]",
            f"[1:v]trim=duration={dur:.3f},setpts=PTS-STARTPTS,"
            "scale=408:230:force_original_aspect_ratio=increase:flags=lanczos,crop=408:230,fps=30,format=rgba[pipraw]",
            "[2:v]format=gray[mask]",
            "[pipraw][mask]alphamerge[pip]",
            "[bg][pip]overlay=1468:44[bgpip]",
            "[3:v]format=rgba[bdr]",
            "[bgpip][bdr]overlay=1464:40[withpip]",
        ]
        cur_v = "[withpip]"
        if ov_path is not None:
            inputs.extend(["-loop", "1", "-t", f"{dur:.3f}", "-i", str(ov_path)])
            fc_parts.append("[5:v]format=rgba[ov];[withpip][ov]overlay=0:0[vov]")
            cur_v = "[vov]"
        fc_parts.append(
            f"{cur_v}ass='{ass_esc}',"
            f"fade=t=in:st=0:d=0.22,fade=t=out:st={fade_out_st:.3f}:d=0.22,format=yuv420p[vout]"
        )
        cmd = [
            "ffmpeg", "-nostdin", "-y",
            *inputs,
            "-filter_complex", ";".join(fc_parts),
            "-map", "[vout]", "-map", "4:a",
            *V_CODEC_SEG,
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-r", "30", "-t", f"{dur:.3f}",
            str(seg_mp4),
        ]

    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return idx, seg_mp4, dur


def render_opener_and_finale() -> tuple[Path, Path]:
    opener_seg = SEG_DIR / "seg_000_opener.mp4"
    finale_seg = SEG_DIR / "seg_999_finale.mp4"

    if not opener_seg.exists():
        subprocess.run([
            "ffmpeg", "-nostdin", "-y",
            "-ss", "0", "-t", "14.00", "-i", str(OPENER_MP4),
            "-vf", "scale=1920:1080,fps=30,setsar=1,fade=t=in:st=0:d=0.5,fade=t=out:st=13.4:d=0.6,format=yuv420p",
            "-af", "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,afade=t=in:st=0:d=0.4,afade=t=out:st=13.4:d=0.6",
            *V_CODEC_SEG, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-r", "30", "-t", "14.00",
            str(opener_seg),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not finale_seg.exists():
        subprocess.run([
            "ffmpeg", "-nostdin", "-y",
            "-loop", "1", "-r", "30", "-t", "8.00", "-i", str(LOGO_JPG),
            "-ss", "0", "-t", "8.00", "-i", str(THEME_WAV),
            "-vf", (
                "scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos,"
                "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:white,fps=30,setsar=1,"
                "fade=t=in:st=0:d=0.5,fade=t=out:st=7.1:d=0.9,format=yuv420p"
            ),
            "-af", "aresample=48000,volume=0.42,afade=t=in:st=0:d=0.4,afade=t=out:st=6.8:d=1.2",
            *V_CODEC_SEG, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-r", "30", "-t", "8.00",
            str(finale_seg),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return opener_seg, finale_seg


def main():
    AUD_DIR.mkdir(parents=True, exist_ok=True)
    SEG_DIR.mkdir(parents=True, exist_ok=True)
    OUT_MASTER_1080P.parent.mkdir(parents=True, exist_ok=True)
    OUT_WEB_720P.parent.mkdir(parents=True, exist_ok=True)

    shots = json.loads(LEDGER_JSON.read_text(encoding="utf-8"))["shots"]
    print(f"🎬 Building S01E01 '1. Respect Your DUTY First.' — {len(shots)} Shots (Encoder: {'NVENC GPU' if USE_NVENC else 'CPU libx264'})", flush=True)

    mask_png, border_png = make_rounded_pip_mask()
    opener_seg, finale_seg = render_opener_and_finale()

    # Step 1: Synthesize all 48 spoken lines (4 parallel workers to be polite to gTTS)
    print("1️⃣ Synthesizing 48 spoken narration lines (Host @Me, 4yo Bala-Rishi, Bala-Matha & Celestial Genie)...", flush=True)
    with ThreadPoolExecutor(max_workers=4) as ex:
        list(ex.map(lambda pair: synthesize_shot_audio(pair[0], pair[1]), enumerate(shots)))

    # Step 2: Render all 48 HD video segments in parallel
    print("2️⃣ Rendering 48 1080p widescreen cinema segments with Google Flow motion & RGBA glass overlays...", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(render_single_shot, idx, sh, mask_png, border_png) for idx, sh in enumerate(shots)]
        for fut in futs:
            idx, seg_p, dur = fut.result()
            results.append((idx, seg_p, dur))
            if (idx + 1) % 8 == 0 or idx + 1 == len(shots):
                print(f"   ✅ Rendered {idx + 1}/{len(shots)} shots (latest {shots[idx]['slot_id']}: {dur:.2f}s)", flush=True)

    results.sort(key=lambda x: x[0])
    body_concat_txt = TEMP_DIR / "body_concat.txt"
    body_concat_txt.write_text("\n".join(f"file '{p}'" for _, p, _ in results) + "\n", encoding="utf-8")

    body_raw_mp4 = TEMP_DIR / "body_raw_1080p.mp4"
    print("3️⃣ Concatenating 48 spoken shots & mixing -26 dB 7D meditative theme underscore...", flush=True)
    subprocess.run([
        "ffmpeg", "-nostdin", "-y",
        "-f", "concat", "-safe", "0", "-i", str(body_concat_txt),
        "-c", "copy", str(body_raw_mp4),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    body_dur = probe_duration(body_raw_mp4)
    body_scored_mp4 = TEMP_DIR / "body_scored_1080p.mp4"
    subprocess.run([
        "ffmpeg", "-nostdin", "-y",
        "-i", str(body_raw_mp4),
        "-stream_loop", "-1", "-i", str(THEME_WAV),
        "-filter_complex", (
            f"[1:a]atrim=duration={body_dur:.3f},asetpts=PTS-STARTPTS,aresample=48000,"
            "lowpass=f=3200,volume=0.055[bgm];"
            "[0:a]aresample=48000,volume=1.0[vox];"
            "[vox][bgm]amix=inputs=2:duration=first:dropout_transition=0,"
            "loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
        ),
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(body_scored_mp4),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    full_concat_txt = TEMP_DIR / "full_concat.txt"
    full_concat_txt.write_text(
        f"file '{opener_seg}'\nfile '{body_scored_mp4}'\nfile '{finale_seg}'\n",
        encoding="utf-8",
    )

    print("4️⃣ Stitching Final 1080p Master Film (`Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_Master_16x9.mp4`)...", flush=True)
    subprocess.run([
        "ffmpeg", "-nostdin", "-y",
        "-f", "concat", "-safe", "0", "-i", str(full_concat_txt),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(OUT_MASTER_1080P),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("5️⃣ Exporting 720p Web Portal Edition & 360p Fast Preview...", flush=True)
    subprocess.run([
        "ffmpeg", "-nostdin", "-y", "-i", str(OUT_MASTER_1080P),
        "-vf", "scale=1280:720,format=yuv420p",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "fast", "-crf", "26",
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
        "-movflags", "+faststart",
        str(OUT_WEB_720P),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run([
        "ffmpeg", "-nostdin", "-y", "-i", str(OUT_MASTER_1080P),
        "-vf", "scale=640:360,format=yuv420p",
        "-c:v", "libx264", "-profile:v", "main", "-preset", "fast", "-crf", "25",
        "-c:a", "aac", "-b:a", "96k", "-ar", "48000",
        "-movflags", "+faststart",
        str(OUT_PREVIEW_360P),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for p in (OUT_MASTER_1080P, OUT_WEB_720P, OUT_PREVIEW_360P):
        d = probe_duration(p)
        mb = p.stat().st_size / 1e6
        print(f"🎉 READY: {p.relative_to(REPO_DIR)} -> {d:.1f}s ({d/60:.2f} min) | {mb:.2f} MB", flush=True)


if __name__ == "__main__":
    main()
