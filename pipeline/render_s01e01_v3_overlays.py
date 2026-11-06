#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renders 8 modern 1920x1080 RGBA Curved-Glass-Barrier Holographic Overlays for
Karmic Genie Show S01E01 v4.0:
  - ZERO top dark rectangular boxes (`y=0..150` is 100% clear — modern glass-display aesthetic!).
  - On Full-Studio clips (`v3_ov_poll`, `v3_ov_ceo`, `v3_ov_layers`, `v3_ov_genie`):
    renders sleek, glowing Curved-Glass-Barrier Holographic Text (`y=665..780` on the left
    `x=48..420` and right `x=1500..1872` curved glass barriers) with subtle cyan/gold
    glass-refraction lettering and soft Gaussian glow (zero opaque/dark background box!).
  - On `pip75` clips (`v3_ov_expat`, `v3_ov_mum`, `v3_ov_veteran`, `v3_ov_dispatch`):
    renders clean transparent RGBA plates so the native curved circular glass displays baked into
    `v7_wide_wall_dormant_16x9.jpg` remain naturally visible with zero box clutter!
  - Strictly ZERO company names, ZERO real/fictional person names, and ZERO blame!
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
OUT_DIR = REPO_DIR / "episodes" / "S01E01_Employees_vs_Tech_CEO" / "overlays_v3"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

ICE_CYAN = (205, 248, 255, 232)
GLASS_WHITE = (245, 252, 255, 238)
WARM_GOLD = (252, 220, 142, 236)
EMERALD_GLASS = (162, 252, 212, 235)
CYAN_GLOW = (32, 165, 210, 135)
DARK_HALO = (6, 14, 24, 155)


OVERLAY_SPECS = [
    {
        "fname": "v3_ov_poll.png",
        "transparent": False,
        "left": (48, 668, 424, [
            ("2025 → 2026 GLOBAL SHIFTS", ICE_CYAN, True),
            ("200,000+ ROLES • 60K BUYOUTS", GLASS_WHITE, True),
            ("Tech • Finance • Logistics • Auto", WARM_GOLD, False),
        ]),
        "right": (1560, 668, 1884, [
            ("VIEWER CIRCLE POLL", WARM_GOLD, True),
            ("9–12 MO VOLUNTARY BRIDGES", GLASS_WHITE, True),
            ("7+ Mgmt Layers & 50s Tier", ICE_CYAN, False),
        ]),
    },
    {
        "fname": "v3_ov_ceo.png",
        "transparent": False,
        "left": (48, 668, 424, [
            ("AI CIRCULATION & RENEWAL", ICE_CYAN, True),
            ("$720B/YR INFRASTRUCTURE", GLASS_WHITE, True),
            ("Highways = Pathways, Never Home", WARM_GOLD, False),
        ]),
        "right": (1560, 668, 1884, [
            ("7D PATHWAY SCORECARD", WARM_GOLD, True),
            ("✓ ≥ 4 OF 7D → STAY COURSE", EMERALD_GLASS, True),
            ("< 4 OF 7D → CHANGE ROUTE", ICE_CYAN, False),
        ]),
    },
    {
        "fname": "v3_ov_layers.png",
        "transparent": False,
        "left": (48, 668, 424, [
            ("KARMIC MARKET CORRECTION", ICE_CYAN, True),
            ("TECH = CONNECTEDNESS", GLASS_WHITE, True),
            ("Reconnecting Workers to Home", WARM_GOLD, False),
        ]),
        "right": (1560, 668, 1884, [
            ("BUYOUT BRIDGE METRICS", WARM_GOLD, True),
            ("9–12 MO RUNWAY • -20% LAYERS", EMERALD_GLASS, True),
            ("Prune Limbs → Bear Family Fruit", ICE_CYAN, False),
        ]),
    },
    {
        "fname": "v3_ov_expat.png",
        "transparent": True,
    },
    {
        "fname": "v3_ov_mum.png",
        "transparent": True,
    },
    {
        "fname": "v3_ov_veteran.png",
        "transparent": True,
    },
    {
        "fname": "v3_ov_dispatch.png",
        "transparent": True,
    },
    {
        "fname": "v3_ov_genie.png",
        "transparent": False,
        "left": (48, 668, 424, [
            ("KARMIC GENIE • THE 7D WAY", ICE_CYAN, True),
            ("BLESSING IN DISGUISE", WARM_GOLD, True),
            ("2-Yr Renewal Toward True Purpose", GLASS_WHITE, False),
        ]),
        "right": (1560, 668, 1884, [
            ("7D SCORE ≥ 4/7 RULE", WARM_GOLD, True),
            ("DUTY • DIGNITY • DISCIPLINE", EMERALD_GLASS, True),
            ("DHARMA • DEVOTION • DESTINY", GLASS_WHITE, False),
        ]),
    },
]


def fit_font(draw: ImageDraw.ImageDraw, text: str, font_path: str, start_px: int, min_px: int, max_w: int):
    for sz in range(start_px, min_px - 1, -1):
        f = ImageFont.truetype(font_path, sz)
        w = draw.textbbox((0, 0), text, font=f)[2]
        if w <= max_w:
            return f
    return ImageFont.truetype(font_path, min_px)


def draw_glass_wing(base: Image.Image, x0: int, y0: int, x1: int, rows: list, align_right: bool):
    max_w = x1 - x0
    glow_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    halo_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    txt_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))

    dg = ImageDraw.Draw(glow_layer)
    dh = ImageDraw.Draw(halo_layer)
    dt = ImageDraw.Draw(txt_layer)

    # Ultra-subtle glass rim hairline (no dark box!)
    rim_y = y0 - 8
    dg.line([(x0, rim_y), (x1, rim_y)], fill=(150, 235, 255, 110), width=2)
    dt.line([(x0, rim_y), (x1, rim_y)], fill=(215, 248, 255, 135), width=1)

    step_y = 33
    for idx, (line_txt, col, is_bold) in enumerate(rows):
        fpath = FONT_BOLD if is_bold else FONT_REG
        start_sz = 20 if idx == 1 else (16 if idx == 0 else 15)
        f = fit_font(dt, line_txt, fpath, start_sz, 12, max_w)
        tw = dt.textbbox((0, 0), line_txt, font=f)[2]
        tx = (x1 - tw) if align_right else x0
        ty = y0 + idx * step_y

        # Soft dark optical contrast halo + cyan glass refraction glow (zero rectangular fill!)
        dh.text((tx + 1, ty + 2), line_txt, font=f, fill=DARK_HALO)
        dh.text((tx - 1, ty), line_txt, font=f, fill=DARK_HALO)
        dg.text((tx, ty), line_txt, font=f, fill=CYAN_GLOW)
        dt.text((tx, ty), line_txt, font=f, fill=col)

    halo_blur = halo_layer.filter(ImageFilter.GaussianBlur(radius=3.2))
    glow_blur = glow_layer.filter(ImageFilter.GaussianBlur(radius=5.5))

    out = Image.alpha_composite(base, halo_blur)
    out = Image.alpha_composite(out, glow_blur)
    out = Image.alpha_composite(out, txt_layer)
    return out


def render_overlay(spec: dict):
    im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    if not spec.get("transparent", False):
        lx0, ly0, lx1, lrows = spec["left"]
        rx0, ry0, rx1, rrows = spec["right"]
        im = draw_glass_wing(im, lx0, ly0, lx1, lrows, align_right=False)
        im = draw_glass_wing(im, rx0, ry0, rx1, rrows, align_right=True)

    out_path = OUT_DIR / spec["fname"]
    im.save(out_path)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for spec in OVERLAY_SPECS:
        render_overlay(spec)
    print(f"✅ Rendered {len(OVERLAY_SPECS)} Curved-Glass-Barrier holographic overlays (ZERO top boxes!) in {OUT_DIR}")


if __name__ == "__main__":
    main()
