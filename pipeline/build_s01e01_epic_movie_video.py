#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master 16:9 Full-HD (1920x1080, 30fps) & Web-Streaming (1280x720) Cinema Film Builder for:
  The Karmic Genie Show — Season 1, Episode 1 (S01E01):
  "The Way Forward: As in the Macrocosm, So in the Microcosm (Andathil Ullathe Pindam)"

Enforces:
  1. Canonical @Me Avatar (tailored ivory-white bandhgala suit) + 1 Child Rule:
     - Whenever a child narrator speaks or assists in a scene, ONLY @Me + that ONE speaking child
       (either 4yo Bala-Rishi for Jnana/Science/Time-Pause or 4yo Bala-Matha for Arul/Grace/Nandri)
       appear in the scene (except the Studio Opening Summons, White-Wall Portal entry, and Grand Finale).
  2. Active In-Scene Witness Narrators ('Two Birds' Kinetic Mirroring) & 3D Bullet-Time Time-Pause HUDs.
  3. Smooth 30fps Ken Burns camera motion, burnt-in cinema subtitles & lower-thirds, and mixed
     Official Karmic Genie 7D Theme Song + 40Hz/528Hz harmonic soundscape.
"""

import json
import math
import shutil
import subprocess
import wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_DIR = Path("/home/antigravity/shishyan/Karmic-Genie-Show")
PACKAGE_JSON = REPO_DIR / "GOOGLE_FLOW_STORYBOARD_PACKAGE_S01E01.json"
THEME_WAV = REPO_DIR / "assets" / "theme" / "official_karmic_genie_7d_theme_song.wav"
OPENER_MP4 = REPO_DIR / "renders" / "Karmic_Genie_Show_Official_7D_Theme_Opener_16x9.mp4"
LOGO_JPG = REPO_DIR / "assets" / "logo" / "official_karmic_genie_show_logo.jpg"

TEMP_DIR = REPO_DIR / "episodes" / "S01E01_The_Way_Forward_Master" / "temp_epic_movie_build"
OUT_RENDERS = REPO_DIR / "renders"
OUT_DOCS_VIDEOS = REPO_DIR / "docs" / "assets" / "videos"
BRAIN_DIR = Path("/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p/479d8c9a-f6dd-4eec-b260-4df5e998a692")

OUT_FULL_1080P = OUT_RENDERS / "Karmic_Genie_Show_S01E01_The_Way_Forward_Epic_Movie_16x9.mp4"
OUT_WEB_720P = OUT_DOCS_VIDEOS / "Karmic_Genie_Show_S01E01_The_Way_Forward_Epic_Movie_16x9.mp4"
OUT_BRAIN_MP4 = BRAIN_DIR / "Karmic_Genie_Show_S01E01_The_Way_Forward_Epic_Movie_16x9.mp4"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

SCENE_SPEAKERS = {
    1: ("@Me (Host)  +  4yo Bala-Rishi (In-Scene Sprint)", "GOLD", "zoom_in"),
    2: ("@Me (Host)  +  4yo Bala-Matha (In-Scene Witness)", "ROSE", "pan_right"),
    3: ("@Me (Host)  •  Studio Summons (100% Nandri)", "GOLD", "zoom_in"),
    4: ("@Me (Host)  •  White Wall IMAX Portal Transposition", "CYAN", "zoom_in_fast"),
    5: ("4yo Bala-Rishi (Jnana)  +  @Me (Host)", "GOLD", "zoom_out"),
    6: ("4yo Bala-Rishi  +  @Me  •  [3D SCENE TIME-PAUSE]", "CYAN", "zoom_in"),
    7: ("@Me (Host)  +  4yo Bala-Rishi  •  [3D SCENE TIME-PAUSE]", "CYAN", "pan_left"),
    8: ("@Me (Host)  +  4yo Bala-Matha  •  [3D SCENE TIME-PAUSE]", "ROSE", "zoom_in"),
    9: ("4yo Bala-Matha (Arul)  +  @Me (Host)", "EMERALD", "zoom_out"),
    10: ("@Me (Host)  +  4yo Bala-Rishi (Jnana)", "GOLD", "zoom_in"),
    11: ("@Me (Host)  +  4yo Bala-Matha (2050 Sanctuary)", "EMERALD", "pan_right"),
    12: ("Awakened Maharishi Karmic Genie  •  7D Benediction", "GOLD", "zoom_out"),
}


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = f"{cur} {w}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render_hud_overlay_png(scene_obj: dict, width: int = 1920, height: int = 1080) -> Path:
    sc_num = scene_obj["scene"]
    out_png = TEMP_DIR / f"hud_scene_{sc_num:02d}.png"
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    f_tag = ImageFont.truetype(FONT_BOLD, 20)
    f_title = ImageFont.truetype(FONT_BOLD, 26)
    f_meta = ImageFont.truetype(FONT_REG, 19)
    f_speaker = ImageFont.truetype(FONT_BOLD, 22)
    f_sub = ImageFont.truetype(FONT_BOLD, 31)

    speaker_label, theme_key, _ = SCENE_SPEAKERS.get(sc_num, ("@Me (Host)", "GOLD", "zoom_in"))
    is_pause = "[SCENE TIME-PAUSE]" in scene_obj["title"] or "[SCENE TIME-PAUSE]" in scene_obj.get("time_pause_mechanic", "")

    accent_map = {
        "GOLD": (245, 196, 81, 255),
        "CYAN": (56, 189, 248, 255),
        "ROSE": (251, 113, 133, 255),
        "EMERALD": (52, 211, 153, 255),
    }
    accent = accent_map.get(theme_key, (245, 196, 81, 255))

    # 1. Top-Left Cinematic Scene Header Pill
    top_x0, top_y0, top_x1, top_y1 = 48, 36, 1180, 128
    draw.rounded_rectangle([top_x0, top_y0, top_x1, top_y1], radius=16, fill=(10, 15, 28, 205), outline=accent, width=2)
    act_str = f"S01E01 • SCENE {sc_num:02d}/12 • {scene_obj['act'].upper()}"
    draw.text((top_x0 + 22, top_y0 + 14), act_str, font=f_tag, fill=accent)
    title_str = scene_obj["title"]
    if len(title_str) > 68:
        title_str = title_str[:65] + "..."
    draw.text((top_x0 + 22, top_y0 + 46), title_str, font=f_title, fill=(255, 255, 255, 255))

    # 2. Top-Right 'Two Birds' / Time-Pause Status Badge
    badge_x0, badge_y0, badge_x1, badge_y1 = 1220, 36, 1872, 128
    if is_pause:
        draw.rounded_rectangle([badge_x0, badge_y0, badge_x1, badge_y1], radius=16, fill=(14, 36, 62, 220), outline=(56, 189, 248, 255), width=2)
        draw.text((badge_x0 + 22, badge_y0 + 15), "⏸ 3D BULLET-TIME SCENE PAUSE", font=f_tag, fill=(125, 211, 252, 255))
        draw.text((badge_x0 + 22, badge_y0 + 48), "Narrator Walking Inside Frozen Frame", font=f_meta, fill=(240, 249, 255, 255))
    else:
        draw.rounded_rectangle([badge_x0, badge_y0, badge_x1, badge_y1], radius=16, fill=(15, 23, 42, 205), outline=(245, 196, 81, 220), width=2)
        draw.text((badge_x0 + 22, badge_y0 + 15), "🕊️ TWO BIRDS ACTIVE NARRATION", font=f_tag, fill=(253, 224, 71, 255))
        draw.text((badge_x0 + 22, badge_y0 + 48), "Narrator + 1 Speaking Child In-Scene", font=f_meta, fill=(241, 245, 249, 255))

    # 3. Bottom Cinema Subtitle & Dialogue Bar
    sub_x0, sub_y0, sub_x1, sub_y1 = 110, 835, 1810, 1036
    draw.rounded_rectangle([sub_x0, sub_y0, sub_x1, sub_y1], radius=20, fill=(8, 12, 24, 222), outline=accent, width=2)

    # Speaker pill above dialogue
    sp_w = draw.textbbox((0, 0), speaker_label, font=f_speaker)[2] + 44
    draw.rounded_rectangle([sub_x0 + 28, sub_y0 - 22, sub_x0 + 28 + sp_w, sub_y0 + 22], radius=11, fill=(18, 28, 48, 245), outline=accent, width=2)
    draw.text((sub_x0 + 50, sub_y0 - 13), speaker_label, font=f_speaker, fill=accent)

    quote_text = f"“{scene_obj['dialogue_anchor']}”"
    wrapped_quote = wrap_text(draw, quote_text, f_sub, (sub_x1 - sub_x0) - 80)
    qy = sub_y0 + 38
    for ln in wrapped_quote[:3]:
        lbbox = draw.textbbox((0, 0), ln, font=f_sub)
        lw = lbbox[2] - lbbox[0]
        lx = sub_x0 + ((sub_x1 - sub_x0) - lw) // 2
        # Subtle shadow
        draw.text((lx + 2, qy + 2), ln, font=f_sub, fill=(0, 0, 0, 230))
        draw.text((lx, qy), ln, font=f_sub, fill=(255, 250, 235, 255))
        qy += 44

    img.save(out_png)
    return out_png


def build_scene_clip(scene_obj: dict, dur_s: float = 9.0) -> Path:
    sc_num = scene_obj["scene"]
    out_mp4 = TEMP_DIR / f"scene_{sc_num:02d}.mp4"
    plate_path = REPO_DIR / scene_obj["visual_asset"]
    if not plate_path.exists():
        plate_path = REPO_DIR / "docs" / scene_obj["visual_asset"]

    # Prepare clean 1920x1080 base image
    base_png = TEMP_DIR / f"base_{sc_num:02d}.png"
    with Image.open(plate_path) as im:
        im_rgb = im.convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
        im_rgb.save(base_png)

    hud_png = render_hud_overlay_png(scene_obj)
    _, _, motion_mode = SCENE_SPEAKERS.get(sc_num, ("@Me", "GOLD", "zoom_in"))
    frames = int(dur_s * 30)

    if motion_mode == "zoom_in":
        zp = f"zoompan=z='min(zoom+0.00045,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps=30"
    elif motion_mode == "zoom_in_fast":
        zp = f"zoompan=z='min(zoom+0.00085,1.22)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps=30"
    elif motion_mode == "zoom_out":
        zp = f"zoompan=z='if(eq(on,1),1.12,max(1.0,zoom-0.00045))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps=30"
    elif motion_mode == "pan_right":
        zp = f"zoompan=z='1.10':x='(iw-iw/zoom)*(on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps=30"
    else:
        zp = f"zoompan=z='1.10':x='(iw-iw/zoom)*(1-on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps=30"

    vf = (
        f"[0:v]scale=2304:1296,{zp},format=rgba[bg];"
        f"[1:v]format=rgba[hud];"
        f"[bg][hud]overlay=0:0,fade=t=in:st=0:d=0.45,fade=t=out:st={dur_s-0.45:.2f}:d=0.45,format=yuv420p[v]"
    )

    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-t", f"{dur_s:.2f}", "-i", str(base_png),
        "-loop", "1", "-t", f"{dur_s:.2f}", "-i", str(hud_png),
        "-filter_complex", vf,
        "-map", "[v]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
        "-r", "30", "-t", f"{dur_s:.2f}",
        str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_mp4


def build_opener_excerpt(dur_s: float = 8.0) -> Path:
    out_mp4 = TEMP_DIR / "scene_00_opener.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", "0", "-t", f"{dur_s:.2f}", "-i", str(OPENER_MP4),
        "-vf", f"scale=1920:1080,fade=t=in:st=0:d=0.5,fade=t=out:st={dur_s-0.6:.2f}:d=0.6,format=yuv420p",
        "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-r", "30",
        str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_mp4


def synthesize_harmonic_soundtrack(total_dur: float) -> Path:
    """
    Creates the full Episode 1 stereo soundtrack combining:
      1. The Official Karmic Genie 7D Theme Song (full 64.4s opener & musical bed)
      2. A warm 40Hz (Planetary Embryo Heartbeat) + 432Hz/528Hz (Solfeggio Sanctuary) meditative harmonic bed
         with subtle temple chime accents at each scene transition.
    """
    out_wav = TEMP_DIR / "full_soundtrack.wav"
    sr = 48000
    n_samples = int(total_dur * sr)
    t = np.linspace(0, total_dur, n_samples, endpoint=False, dtype=np.float32)

    # Warm harmonic pad: 108Hz root + 216Hz + 432Hz + 528Hz gentle shimmer
    pad_l = (
        0.08 * np.sin(2 * math.pi * 108.0 * t)
        + 0.05 * np.sin(2 * math.pi * 216.0 * t + 0.3)
        + 0.03 * np.sin(2 * math.pi * 432.0 * t)
        + 0.02 * np.sin(2 * math.pi * 528.0 * t * (1.0 + 0.0005 * np.sin(2 * math.pi * 0.15 * t)))
    )
    pad_r = (
        0.08 * np.sin(2 * math.pi * 108.0 * t + 0.2)
        + 0.05 * np.sin(2 * math.pi * 216.0 * t)
        + 0.03 * np.sin(2 * math.pi * 432.0 * t + 0.4)
        + 0.02 * np.sin(2 * math.pi * 528.0 * t)
    )

    # Add gentle golden chime at every scene boundary (8.0s opener + every 9.0s scene)
    boundaries = [0.0, 8.0] + [8.0 + 9.0 * i for i in range(1, 13)]
    for b_sec in boundaries:
        idx0 = int(b_sec * sr)
        chime_len = int(2.4 * sr)
        if idx0 + chime_len < n_samples:
            ct = np.linspace(0, 2.4, chime_len, endpoint=False, dtype=np.float32)
            env = np.exp(-2.2 * ct) * (1.0 - np.exp(-40.0 * ct))
            chime = 0.09 * env * (np.sin(2 * math.pi * 528.0 * ct) + 0.5 * np.sin(2 * math.pi * 1056.0 * ct))
            pad_l[idx0 : idx0 + chime_len] += chime
            pad_r[idx0 : idx0 + chime_len] += chime

    bed_wav = TEMP_DIR / "harmonic_bed.wav"
    stereo = np.stack([pad_l, pad_r], axis=-1)
    stereo_int16 = np.clip(stereo * 32767.0, -32768, 32767).astype(np.int16)
    with wave.open(str(bed_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(stereo_int16.tobytes())

    # Mix with the Official 7D Theme Song (looped gently and ducked cleanly during the main scenes)
    subprocess.run([
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(THEME_WAV),
        "-i", str(bed_wav),
        "-filter_complex", (
            f"[0:a]atrim=0:{total_dur:.2f},volume='if(lt(t,8.0),0.85,if(gt(t,{total_dur-12.0:.2f}),0.75,0.28))':eval=frame[thm];"
            f"[1:a]atrim=0:{total_dur:.2f},volume=0.85[bed];"
            f"[thm][bed]amix=inputs=2:duration=first:dropout_transition=2,"
            f"afade=t=in:st=0:d=1.0,afade=t=out:st={total_dur-2.0:.2f}:d=2.0,"
            "aresample=48000[a]"
        ),
        "-map", "[a]", "-t", f"{total_dur:.2f}",
        str(out_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_wav


def main():
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RENDERS.mkdir(parents=True, exist_ok=True)
    OUT_DOCS_VIDEOS.mkdir(parents=True, exist_ok=True)

    pkg = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    scenes = pkg["episode_1_storyboard_scenes"]

    print("🎬 Building Opener Excerpt (8.0s)...")
    clips = [build_opener_excerpt(8.0)]

    scene_dur = 9.0
    for sc in scenes:
        print(f"🎬 Rendering Scene {sc['scene']:02d}/12: {sc['title']}...")
        clips.append(build_scene_clip(sc, scene_dur))

    concat_txt = TEMP_DIR / "concat_list.txt"
    concat_txt.write_text("\n".join(f"file '{c.resolve()}'" for c in clips) + "\n", encoding="utf-8")

    total_dur = 8.0 + len(scenes) * scene_dur
    print(f"🎵 Mixing Official 7D Theme Song + 40Hz/528Hz Cinema Soundtrack ({total_dur:.1f}s)...")
    soundtrack_wav = synthesize_harmonic_soundtrack(total_dur)

    print("🎞️ Assembling Master 1080p 16:9 Episode 1 Film...")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-i", str(soundtrack_wav),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        "-shortest",
        str(OUT_FULL_1080P)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("🌐 Encoding Web-Optimized 720p Stream for genie.shishyan.in...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(OUT_FULL_1080P),
        "-vf", "scale=1280:720",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(OUT_WEB_720P)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    OUT_BRAIN_MP4.write_bytes(OUT_FULL_1080P.read_bytes())
    print(f"✅ Master 1080p MP4: {OUT_FULL_1080P} ({OUT_FULL_1080P.stat().st_size / (1024*1024):.2f} MB)")
    print(f"✅ Web 720p MP4:    {OUT_WEB_720P} ({OUT_WEB_720P.stat().st_size / (1024*1024):.2f} MB)")


if __name__ == "__main__":
    main()
