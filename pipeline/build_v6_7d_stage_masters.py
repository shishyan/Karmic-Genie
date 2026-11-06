#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds pixel-seamless 2K (2752x1536) v6 7D Stage Wall Masters using multi-scale
Laplace harmonic inpainting (nabla^2 u = 0 with exact Dirichlet wall boundaries — zero box seams!)
followed by precision architectural typesetting of the user's exact 7D wall layout:

   Respect Your DUTY First.        [ Logo ]       Uphold Karmic DHARMA.
   Earn with DIGNITY Always.       [  Logo  ]       Raise Family with DEVOTION.
   Practice Life DISCIPLINE.       [  Logo    ]       Be Grateful to Your DIVINE.

                       Purposeful Life Is Your DESTINY.
"""

from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
MASTERS_DIR = REPO_DIR / "assets" / "studio_v5_masters"
LOGO_PATH = REPO_DIR / "assets" / "logo" / "official_karmic_genie_show_logo.jpg"
ARTIFACT_DIR = Path("/home/shishyan/.gemini/antigravity/brain/b55fc9ea-1a2e-45b9-8d71-a53ee11caf0c")

OLD_DORMANT = MASTERS_DIR / "s01e01_act1_dormant_stage_16x9.jpg"
OLD_GENIE = MASTERS_DIR / "s01e01_act2_saintly_genie_16x9.jpg"

OUT_DORMANT = MASTERS_DIR / "v6_7d_dormant_stage_16x9.jpg"
OUT_GENIE = MASTERS_DIR / "v6_7d_saintly_genie_16x9.jpg"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def harmonic_inpaint(img_patch: np.ndarray, mask_bool: np.ndarray) -> np.ndarray:
    """
    Multi-scale Laplace solver (nabla^2 u = 0) on `mask_bool` pixels while keeping all
    `~mask_bool` pixels 100.0% identical to `img_patch` (exact C^infty boundary continuity,
    zero rectangular seams).
    """
    u = img_patch.astype(np.float32).copy()
    # Build pyramid (scales: 1/8 -> 1/4 -> 1/2 -> 1) for instant global convergence!
    h, w, _ = u.shape
    scales = [8, 4, 2, 1]
    prev_sol = None

    for sc in scales:
        sh, sw = max(4, h // sc), max(4, w // sc)
        p_small = np.array(Image.fromarray(img_patch).resize((sw, sh), Image.Resampling.BILINEAR), dtype=np.float32)
        m_small = np.array(Image.fromarray((mask_bool.astype(np.uint8) * 255)).resize((sw, sh), Image.Resampling.NEAREST)) > 64

        if prev_sol is None:
            cur = p_small.copy()
            # Initialize masked pixels with global mean of unmasked wall
            valid = p_small[~m_small]
            init_col = np.median(valid, axis=0) if len(valid) else np.array([222.0, 220.0, 217.0])
            cur[m_small] = init_col
        else:
            up = np.array(Image.fromarray(np.clip(prev_sol, 0, 255).astype(np.uint8)).resize((sw, sh), Image.Resampling.BILINEAR), dtype=np.float32)
            cur = p_small.copy()
            cur[m_small] = up[m_small]

        iters = 320 if sc >= 4 else (200 if sc == 2 else 140)
        for _ in range(iters):
            nb = 0.25 * (
                np.roll(cur, 1, axis=0) + np.roll(cur, -1, axis=0) +
                np.roll(cur, 1, axis=1) + np.roll(cur, -1, axis=1)
            )
            cur[m_small] = nb[m_small]
        prev_sol = cur

    out = img_patch.astype(np.float32).copy()
    # Add tiny natural camera micro-grain (sigma=0.9) inside inpainted ink pixels so texture matches surrounding wall
    rng = np.random.default_rng(42)
    grain = rng.normal(0.0, 0.85, size=out.shape).astype(np.float32)
    out[mask_bool] = np.clip(prev_sol[mask_bool] + grain[mask_bool], 0, 255)
    return out.astype(np.uint8)


def erase_old_wall_elements(src_rgb: np.ndarray) -> np.ndarray:
    """
    Precisely masks ONLY the old stage-wall text, rainbow swirl, and wall lamp graphic
    inside the curved white stage wall while strictly protecting Marcus (left chair) and @Me (right chair).
    """
    out = src_rgb.copy()
    y0, y1 = 520, 935
    x0, x1 = 875, 1878
    patch = out[y0:y1, x0:x1]
    ph, pw, _ = patch.shape

    lum = patch.mean(axis=2)
    sat = patch.max(axis=2).astype(np.float32) - patch.min(axis=2).astype(np.float32)

    lum_u8 = np.clip(lum, 0, 255).astype(np.uint8)
    local_wall_lum = np.array(Image.fromarray(lum_u8).filter(ImageFilter.MaxFilter(55)).filter(ImageFilter.GaussianBlur(12)), dtype=np.float32)

    is_ink = ((local_wall_lum - lum) > 6.0) | (sat > 9.0)

    gy, gx = np.mgrid[y0:y1, x0:x1]

    in_graphics_boxes = (
        ((gx >= 1190) & (gx <= 1580) & (gy >= 528) & (gy <= 845)) |
        ((gx >= 885) & (gx <= 1255) & (gy >= 620) & (gy <= 852)) |
        ((gx >= 1575) & (gx <= 1874) & (gy >= 635) & (gy <= 835)) |
        ((gx >= 1106) & (gx <= 1641) & (gy >= 845) & (gy <= 926))
    )

    # Protect Marcus's head/hair (seated on left: gx <= 1108 when gy >= 845) and @Me's head/hair (gx >= 1640 when gy >= 848)
    marcus_head = (gx <= 1109) & (gy >= 844)
    host_head = (gx >= 1639) & (gy >= 848)

    raw_mask = is_ink & in_graphics_boxes & (~marcus_head) & (~host_head)

    dil_pil = Image.fromarray((raw_mask.astype(np.uint8) * 255)).filter(ImageFilter.MaxFilter(11))
    mask_final = (np.array(dil_pil) > 127) & (~marcus_head) & (~host_head)

    repaired_patch = harmonic_inpaint(patch, mask_final)
    out[y0:y1, x0:x1] = repaired_patch
    return out


def draw_styled_7d_sentence(draw: ImageDraw.ImageDraw, x: int, y: int, prefix: str, d_word: str, suffix: str, f_reg, f_bold, align="left"):
    w_pre = draw.textbbox((0, 0), prefix, font=f_reg)[2] if prefix else 0
    w_d = draw.textbbox((0, 0), d_word, font=f_bold)[2]
    w_suf = draw.textbbox((0, 0), suffix, font=f_reg)[2] if suffix else 0
    total_w = w_pre + w_d + w_suf

    if align == "center":
        cur_x = x - total_w // 2
    elif align == "right":
        cur_x = x - total_w
    else:
        cur_x = x

    hi_col = (255, 251, 244, 130)
    sh_col = (84, 62, 32, 70)
    reg_col = (134, 102, 55, 232)
    bold_col = (116, 84, 38, 248)

    for part, fnt, col, pw in [(prefix, f_reg, reg_col, w_pre), (d_word, f_bold, bold_col, w_d), (suffix, f_reg, reg_col, w_suf)]:
        if not part:
            continue
        draw.text((cur_x + 1, y + 1), part, font=fnt, fill=hi_col)
        draw.text((cur_x - 1, y - 1), part, font=fnt, fill=sh_col)
        draw.text((cur_x, y), part, font=fnt, fill=col)
        cur_x += pw


def apply_v6_wall(bare_rgb: np.ndarray) -> Image.Image:
    w, h = 2752, 1536
    # Visual center of the curved white stage wall (between left stair curve x=895 and right column x=1820): cx = 1358
    cx = 1358
    logo_size = 246
    logo_resized = Image.open(LOGO_PATH).convert("RGB").resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    lx = cx - logo_size // 2  # 1235 .. 1481
    ly = 554                  # 554 .. 800

    wall_arr = bare_rgb.astype(np.float32).copy()
    logo_arr = np.array(logo_resized, dtype=np.float32) / 255.0
    yy, xx = np.mgrid[0:logo_size, 0:logo_size]
    edge_dist = np.minimum(np.minimum(xx, logo_size - 1 - xx), np.minimum(yy, logo_size - 1 - yy))
    feather = np.clip(edge_dist / 16.0, 0.0, 1.0)[..., None]
    patch = wall_arr[ly:ly+logo_size, lx:lx+logo_size]
    wall_arr[ly:ly+logo_size, lx:lx+logo_size] = np.clip(patch * (1.0 - feather) + (patch * logo_arr) * feather, 0, 255)

    composed = Image.fromarray(wall_arr.astype(np.uint8)).convert("RGBA")
    txt_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)

    f_reg = ImageFont.truetype(FONT_REG, 19)
    f_bold = ImageFont.truetype(FONT_BOLD, 20)
    f_dest_reg = ImageFont.truetype(FONT_REG, 21)
    f_dest_bold = ImageFont.truetype(FONT_BOLD, 22)

    row_ys = [634, 680, 726]

    # Left Wall: x=914 .. ~1172 -> ~63px generous symmetric white padding before [ Logo ] (1235)!
    left_specs = [
        ("Respect Your ", "DUTY", " First."),
        ("Earn with ", "DIGNITY", " Always."),
        ("Practice Life ", "DISCIPLINE", "."),
    ]
    for ry, (pre, dw, suf) in zip(row_ys, left_specs):
        draw_styled_7d_sentence(draw, 914, ry, pre, dw, suf, f_reg, f_bold, align="left")

    # Right Wall: x=1544 .. ~1805 -> ~63px generous symmetric white padding after [ Logo ] (1481), cleanly inside curved wall!
    right_specs = [
        ("Uphold Karmic ", "DHARMA", "."),
        ("Raise Family with ", "DEVOTION", "."),
        ("Be Grateful to Your ", "DIVINE", "."),
    ]
    for ry, (pre, dw, suf) in zip(row_ys, right_specs):
        draw_styled_7d_sentence(draw, 1544, ry, pre, dw, suf, f_reg, f_bold, align="left")

    # Centered 7th Line below [ Logo ]: centered at cx=1358, y=848 (cleanly below Logo and above center table lamp!)
    draw_styled_7d_sentence(
        draw, cx, 848,
        "Purposeful Life Is Your ", "DESTINY", ".",
        f_dest_reg, f_dest_bold, align="center"
    )

    return Image.alpha_composite(composed, txt_layer).convert("RGB")


def build_v6_genie(v6_dormant: Image.Image) -> Image.Image:
    arr_old_dorm = np.array(Image.open(OLD_DORMANT).convert("RGB").resize((2752, 1536)), dtype=np.float32)
    arr_old_genie = np.array(Image.open(OLD_GENIE).convert("RGB").resize((2752, 1536)), dtype=np.float32)
    arr_v6_dorm = np.array(v6_dormant, dtype=np.float32)

    diff = np.abs(arr_old_genie - arr_old_dorm).max(axis=2)
    h, w = diff.shape
    zone = np.zeros((h, w), dtype=np.float32)
    zone[400:1536, 1220:1890] = 1.0
    zone[615:795, :1255] = 0.0
    zone_pil = Image.fromarray((zone * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))
    zone = np.array(zone_pil, dtype=np.float32) / 255.0

    alpha = np.clip((diff - 14.0) / 36.0, 0.0, 1.0) * zone
    gen_sat = arr_old_genie.max(axis=2) - arr_old_genie.min(axis=2)
    gen_lum = arr_old_genie.mean(axis=2)
    # Exclude any neutral dark old-wall letters ('Karmic Genie Show' / right-wall text) that have low saturation & darker lum
    old_dark_letters = (gen_sat < 20.0) & (gen_lum < 205.0)
    old_text_zone = np.zeros((h, w), dtype=bool)
    old_text_zone[620:925, 1100:1875] = True
    # Keep Genie's solid torso/legs core (x in 1365..1615, y in 420..855) intact
    genie_core = np.zeros((h, w), dtype=bool)
    genie_core[420:855, 1365:1615] = True
    alpha[old_dark_letters & old_text_zone & (~genie_core)] = 0.0

    alpha_pil = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.2))
    a3 = (np.array(alpha_pil, dtype=np.float32) / 255.0)[..., None]

    out_arr = arr_v6_dorm * (1.0 - a3) + arr_old_genie * a3
    return Image.fromarray(np.clip(out_arr, 0, 255).astype(np.uint8))


def main():
    src_rgb = np.array(Image.open(OLD_DORMANT).convert("RGB").resize((2752, 1536), Image.Resampling.LANCZOS))
    bare_rgb = erase_old_wall_elements(src_rgb)

    v6_dorm = apply_v6_wall(bare_rgb)
    v6_dorm.save(OUT_DORMANT, quality=95)
    v6_dorm.save(ARTIFACT_DIR / OUT_DORMANT.name, quality=95)
    print(f"✅ Saved {OUT_DORMANT} ({OUT_DORMANT.stat().st_size/1e6:.2f} MB)")

    v6_gen = build_v6_genie(v6_dorm)
    v6_gen.save(OUT_GENIE, quality=95)
    v6_gen.save(ARTIFACT_DIR / OUT_GENIE.name, quality=95)
    print(f"✅ Saved {OUT_GENIE} ({OUT_GENIE.stat().st_size/1e6:.2f} MB)")


if __name__ == "__main__":
    main()
