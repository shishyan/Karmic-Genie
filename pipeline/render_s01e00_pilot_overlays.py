#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renders 11 modern 1920x1080 RGBA Curved-Glass-Barrier Holographic Overlays for
Karmic Genie Show — Season 1, Episode 0 (Pilot: "The 7D Way: Pioneers of the New World"):
  - ZERO top dark rectangular boxes (`y=0..150` is 100% clear — modern glass-display aesthetic!).
  - Frameless, glowing Curved-Glass-Barrier Holographic Refraction Typography at `y=668..768`
    (`Left: x=42..436`, `Right: x=1484..1878`) for all 7 Dimensions (`D1 DUTY 1–10` through
    `D7 DESTINY 1–10`) and the `TOTAL < 35 / 70 -> CHANGE YOUR COURSE!` threshold rule.
  - Strictly ZERO company names, ZERO real/fictional person names, and ZERO blame!
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
OUT_DIR = REPO_DIR / "episodes" / "S01E00_Pilot_The_7D_Way" / "overlays_s01e00"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

ICE_CYAN = (205, 248, 255, 234)
GLASS_WHITE = (246, 252, 255, 240)
WARM_GOLD = (252, 220, 142, 238)
EMERALD_GLASS = (162, 252, 212, 236)
AMBER_GLASS = (255, 204, 136, 236)
CYAN_GLOW = (32, 165, 210, 135)
DARK_HALO = (6, 14, 24, 158)


OVERLAY_SPECS = [
    {
        "fname": "ov_p00_compass.png",
        "left": (42, 668, 436, [
            ("THE 7D WAY • LIFE COMPASS", ICE_CYAN, True),
            ("SCORE EACH VIRTUE 1–10", GLASS_WHITE, True),
            ("7 Great Virtues • Maximum 70", WARM_GOLD, False),
        ]),
        "right": (1484, 668, 1878, [
            ("35 / 70 THRESHOLD LAW", WARM_GOLD, True),
            ("TOTAL < 35 → CHANGE COURSE!", AMBER_GLASS, True),
            ("50–70 → Pioneer of New World", EMERALD_GLASS, False),
        ]),
    },
    {
        "fname": "ov_d1_duty.png",
        "left": (42, 668, 436, [
            ("DIMENSION 1 • SCORE 1–10", ICE_CYAN, True),
            ("D1: RESPECT YOUR DUTY FIRST", WARM_GOLD, True),
            ("Conscience Trigger & Soul Growth", GLASS_WHITE, False),
        ]),
        "right": (1484, 668, 1878, [
            ("THE CONSCIENCE TEST", WARM_GOLD, True),
            ("GUILT WHEN UNDONE = DUTY", EMERALD_GLASS, True),
            ("Silence Conscience → Lose Empathy", ICE_CYAN, False),
        ]),
    },
    {
        "fname": "ov_d2_dignity.png",
        "left": (42, 668, 436, [
            ("DIMENSION 2 • SCORE 1–10", ICE_CYAN, True),
            ("D2: EARN WITH DIGNITY ALWAYS", WARM_GOLD, True),
            ("Unbought Self-Respect & Truth", GLASS_WHITE, False),
        ]),
        "right": (1484, 668, 1878, [
            ("7D SCORECARD CHECK", WARM_GOLD, True),
            ("HONEST SWEAT • STRAIGHT SPINE", EMERALD_GLASS, True),
            ("Total < 35 / 70 → Change Course!", AMBER_GLASS, False),
        ]),
    },
    {
        "fname": "ov_d3_discipline.png",
        "left": (42, 668, 436, [
            ("DIMENSION 3 • SCORE 1–10", ICE_CYAN, True),
            ("D3: PRACTICE LIFE DISCIPLINE", WARM_GOLD, True),
            ("Master Senses, Breath & Clock", GLASS_WHITE, False),
        ]),
        "right": (1484, 668, 1878, [
            ("TUNING THE INSTRUMENT", WARM_GOLD, True),
            ("MIND SERVES SOUL • ZERO ESCAPISM", EMERALD_GLASS, True),
            ("Total < 35 / 70 → Change Course!", AMBER_GLASS, False),
        ]),
    },
    {
        "fname": "ov_d2_d3_dignity_discipline.png",
        "left": (42, 668, 436, [
            ("VIRTUE 2 • SCORE 1–10", ICE_CYAN, True),
            ("D2: DIGNITY (UNBOUGHT WORTH)", WARM_GOLD, True),
            ("Earn Honestly • Straight Spine", GLASS_WHITE, False),
        ]),
        "right": (1484, 668, 1878, [
            ("VIRTUE 3 • SCORE 1–10", WARM_GOLD, True),
            ("D3: DISCIPLINE (SENSE MASTERY)", EMERALD_GLASS, True),
            ("Zero Escapism • Own Your Clock", GLASS_WHITE, False),
        ]),
    },
    {
        "fname": "ov_d4_dharma.png",
        "left": (42, 668, 436, [
            ("DIMENSION 4 • SCORE 1–10", ICE_CYAN, True),
            ("D4: UPHOLD KARMIC DHARMA", WARM_GOLD, True),
            ("Fruit-Bearing Tree for Earth's Body", GLASS_WHITE, False),
        ]),
        "right": (1484, 668, 1878, [
            ("THE PATHWAY PRINCIPLE", WARM_GOLD, True),
            ("HIGHWAYS = PATHWAYS, NOT HOME", EMERALD_GLASS, True),
            ("Total < 35 / 70 → Change Course!", AMBER_GLASS, False),
        ]),
    },
    {
        "fname": "ov_d5_devotion.png",
        "left": (42, 668, 436, [
            ("DIMENSION 5 • SCORE 1–10", ICE_CYAN, True),
            ("D5: RAISE FAMILY IN DEVOTION", WARM_GOLD, True),
            ("Undivided Heart & Presence Today", GLASS_WHITE, False),
        ]),
        "right": (1484, 668, 1878, [
            ("SACRED CONNECTEDNESS", WARM_GOLD, True),
            ("PARENTS • SPOUSE • CHILDREN", EMERALD_GLASS, True),
            ("Give Your Best Today, Not Leftovers", ICE_CYAN, False),
        ]),
    },
    {
        "fname": "ov_d4_d5_dharma_devotion.png",
        "left": (42, 668, 436, [
            ("VIRTUE 4 • SCORE 1–10", ICE_CYAN, True),
            ("D4: DHARMA (FRUIT & SHADE)", WARM_GOLD, True),
            ("Every Organ Serves Earth's Body", GLASS_WHITE, False),
        ]),
        "right": (1484, 668, 1878, [
            ("VIRTUE 5 • SCORE 1–10", WARM_GOLD, True),
            ("D5: DEVOTION (WARM PRESENCE)", EMERALD_GLASS, True),
            ("Parents, Spouse & Children Today", GLASS_WHITE, False),
        ]),
    },
    {
        "fname": "ov_d6_divine.png",
        "left": (42, 668, 436, [
            ("DIMENSION 6 • SCORE 1–10", ICE_CYAN, True),
            ("D6: GRATEFUL TO YOUR DIVINE", WARM_GOLD, True),
            ("Body • Mind • Soul • Para-Soul", GLASS_WHITE, False),
        ]),
        "right": (1484, 668, 1878, [
            ("THE GRAND ARCHITECT", WARM_GOLD, True),
            ("HUMILITY • GRATITUDE • TRUST", EMERALD_GLASS, True),
            ("Closed Doors Redirect to Purpose", ICE_CYAN, False),
        ]),
    },
    {
        "fname": "ov_d7_destiny.png",
        "left": (42, 668, 436, [
            ("DIMENSION 7 • SCORE 1–10", ICE_CYAN, True),
            ("D7: PURPOSEFUL DESTINY", WARM_GOLD, True),
            ("Flowering of All 6 Virtues", GLASS_WHITE, False),
        ]),
        "right": (1484, 668, 1878, [
            ("CROWN OF HUMAN BIRTH", WARM_GOLD, True),
            ("PIONEER OF THE NEW WORLD", EMERALD_GLASS, True),
            ("50–70 / 70 → Gold Zone Harmony", GLASS_WHITE, False),
        ]),
    },
    {
        "fname": "ov_d6_d7_divine_destiny.png",
        "left": (42, 668, 436, [
            ("VIRTUE 6 • SCORE 1–10", ICE_CYAN, True),
            ("D6: DIVINE (GRAND ARCHITECT)", WARM_GOLD, True),
            ("Body • Mind • Soul • Para-Soul", GLASS_WHITE, False),
        ]),
        "right": (1484, 668, 1878, [
            ("VIRTUE 7 • SCORE 1–10", WARM_GOLD, True),
            ("D7: DESTINY (NEW WORLD PIONEER)", EMERALD_GLASS, True),
            ("Total < 35 / 70 → Change Course!", AMBER_GLASS, False),
        ]),
    },
    {
        "fname": "ov_p99_audit_blessing.png",
        "left": (42, 668, 436, [
            ("7D CONSCIENCE SCORECARD", ICE_CYAN, True),
            ("SCORE 1–10 × 7 VIRTUES = /70", GLASS_WHITE, True),
            ("Duty • Dignity • Discipline • Dharma", WARM_GOLD, False),
        ]),
        "right": (1484, 668, 1878, [
            ("COURSE-CHANGE THRESHOLD", WARM_GOLD, True),
            ("TOTAL < 35 / 70 → CHANGE COURSE!", AMBER_GLASS, True),
            ("Devotion • Divine • Destiny", EMERALD_GLASS, False),
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

    rim_y = y0 - 8
    dg.line([(x0, rim_y), (x1, rim_y)], fill=(150, 235, 255, 110), width=2)
    dt.line([(x0, rim_y), (x1, rim_y)], fill=(215, 248, 255, 135), width=1)

    step_y = 33
    for idx, (line_txt, col, is_bold) in enumerate(rows):
        fpath = FONT_BOLD if is_bold else FONT_REG
        start_sz = 19 if idx == 1 else (15 if idx == 0 else 14)
        f = fit_font(dt, line_txt, fpath, start_sz, 11, max_w)
        tw = dt.textbbox((0, 0), line_txt, font=f)[2]
        tx = (x1 - tw) if align_right else x0
        ty = y0 + idx * step_y

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
    lx0, ly0, lx1, lrows = spec["left"]
    rx0, ry0, rx1, rrows = spec["right"]
    im = draw_glass_wing(im, lx0, ly0, lx1, lrows, align_right=False)
    im = draw_glass_wing(im, rx0, ry0, rx1, rrows, align_right=True)
    im.save(OUT_DIR / spec["fname"])


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for spec in OVERLAY_SPECS:
        render_overlay(spec)
    print(f"✅ Rendered {len(OVERLAY_SPECS)} Pilot S01E00 Curved-Glass-Barrier holographic overlays in {OUT_DIR}")


if __name__ == "__main__":
    main()
