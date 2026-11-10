#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renders crisp 1920x1080 RGBA transparent cinema glass location & fractal-organ badges
(top-left IMAX safe zone, never colliding with bottom-center subtitles) for:
  The Karmic Genie Show — Season 1, Episode 1 ("The Way Forward")
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_DIR / "episodes" / "S01E01_The_Way_Forward_Master" / "overlays"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def make_badge(filename: str, kicker: str, headline: str, subline: str, accent_rgb=(218, 178, 92)):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    f_kick = ImageFont.truetype(FONT_BOLD, 18)
    f_head = ImageFont.truetype(FONT_BOLD, 25)
    f_sub = ImageFont.truetype(FONT_REG, 19)

    w1 = draw.textbbox((0, 0), kicker, font=f_kick)[2]
    w2 = draw.textbbox((0, 0), headline, font=f_head)[2]
    w3 = draw.textbbox((0, 0), subline, font=f_sub)[2]
    box_w = max(w1, w2, w3) + 64
    box_h = 116
    x0, y0 = 64, 46

    draw.rounded_rectangle(
        [x0, y0, x0 + box_w, y0 + box_h],
        radius=14,
        fill=(15, 23, 42, 176),
        outline=(255, 255, 255, 48),
        width=2,
    )
    draw.rounded_rectangle(
        [x0, y0 + 14, x0 + 6, y0 + box_h - 14],
        radius=3,
        fill=(*accent_rgb, 255),
    )

    draw.text((x0 + 24, y0 + 15), kicker, font=f_kick, fill=(*accent_rgb, 255))
    draw.text((x0 + 24, y0 + 42), headline, font=f_head, fill=(255, 255, 255, 250))
    draw.text((x0 + 24, y0 + 78), subline, font=f_sub, fill=(208, 224, 240, 235))

    out_p = OUT_DIR / filename
    img.save(out_p)
    return out_p


BADGES = [
    (
        "ov_wf_01_tokyo_icu.png",
        "TOKYO • NOV 11, 2026 • 23:11 UTC",
        "Pediatric ICU Room 404 — Little Maya (Age 7)",
        "Two Birds Active Blocking: @Me + Bala-Rishi Running Beside Kenji",
        (244, 180, 92),
    ),
    (
        "ov_wf_02_california_40hz.png",
        "NORTHERN CALIFORNIA • 300 FT UNDERGROUND",
        "Quantum Supercluster — 40.000 Hz Phase-Lock",
        "Micro-Clock of the Cell ↔ Macro-Clock of Planet Earth",
        (96, 198, 255),
    ),
    (
        "ov_wf_03_vidarbha_soil.png",
        "VIDARBHA, INDIA • MONSOON TWILIGHT",
        "Ramesh & Vishan — Honoring 30 Seasons of Harvest",
        "Two Birds Maternal Grace: @Me + Bala-Matha Kneeling in Nandri",
        (82, 214, 168),
    ),
    (
        "ov_wf_04_white_stadium.png",
        "THE WHITE STADIUM • OUTSIDE EARTHLY TIME",
        "Sacred Studio Summons — The 7D Marble Amphitheater",
        "Duty • Dignity • Discipline • Dharma • Devotion • Divine • Destiny",
        (218, 178, 92),
    ),
    (
        "ov_wf_05_living_gaia.png",
        "WHITE-WALL ZOOM PORTAL • NILGIRI SHOLA CANOPY",
        "Living Gaia — 10-Million-Year Mycorrhizal Network",
        "Zero Bottlenecks • Zero Waste • Nature's Master Supply Chain",
        (82, 214, 168),
    ),
    (
        "ov_wf_06_chronometer_280.png",
        "VEDIC PITRU LOKA CHRONOMETER",
        "1 Embryonic Day = 1 Solar Earth Month (280 Months)",
        "Dec 1, 2022 (Conception) → Nov 2026 (Month 48 Heartbeat) → Apr 2046",
        (244, 196, 92),
    ),
    (
        "ov_wf_07_organ1_uip_ubp.png",
        "ORGAN 1 • NERVOUS & SKELETAL SYSTEM",
        "Unified Infrastructure & Business Platforms (UIP + UBP)",
        "220,000°C EUV Quartz Bone • Subsea Fiber • Open Planetary Cortex",
        (168, 140, 255),
    ),
    (
        "ov_wf_08_organ2_3_ulp_uep.png",
        "ORGANS 2 & 3 • CIRCULATORY HEART & 72-HR LUNG",
        "Unified Logistics (ULP) & Unified Energy Platform (UEP)",
        "400 Ships Routing for Life • Solar, Wind, Geothermal & Forests as One",
        (96, 198, 255),
    ),
    (
        "ov_wf_09_organ4_5_6_uap_uecp.png",
        "ORGANS 4, 5 & 6 • GUT, IMMUNE & KARMIC CREDIT",
        "Salaried Farmer Stewards (UAP) & Karmic Credit Pool (UEcP)",
        "Living Soil as Primary Medicine • Zero-Interest Commons Replenished by Seva",
        (82, 214, 168),
    ),
    (
        "ov_wf_10_343_kalpavriksha.png",
        "7 × 7 × 7 = 343 LIVING NODES",
        "The Fractal Cube & Kalpavriksha Corporate Tree",
        "Root Solvency → Blossom → Universal Fruit → Open-Seed Moksha",
        (244, 196, 92),
    ),
    (
        "ov_wf_11_honeycomb_2050.png",
        "APRIL 2046 → 2050 LIVING REALITY",
        "The Sacred Hexagonal Honeycomb City Mandala",
        "7 Districts → 1 Living City → 7 Bioregions → 1 Unified Planet",
        (82, 214, 168),
    ),
    (
        "ov_wf_12_7d_cosmic_genie.png",
        "180° STADIUM RETRACTION • COSMIC OBSERVATORY",
        "70 / 70 Harmonic Coherence & Maharishi Karmic Genie",
        "அண்டமும் பிண்டமும் ஒன்றே • Macrocosm & Microcosm Are One",
        (244, 196, 92),
    ),
]


def main():
    for args in BADGES:
        p = make_badge(*args)
        print(f"✅ Rendered overlay badge: {p.relative_to(REPO_DIR)}")


if __name__ == "__main__":
    main()
