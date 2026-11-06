#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renders 8 dual-HUD 1920x1080 RGBA broadcast overlays for Karmic Genie Show S01E01 v3.1:
  (A) Top-Left Broadcast Header Card (Global 2025->2026 Correction Context & Question Diagnosis)
  (B) Top-Right Live 7D Scorecard & Sector Metrics HUD (`>= 4 of 7D` Tick-Check Rule)

Geometry Guarantee:
  - On all Act II `pip75` story overlays (`v3_ov_expat`, `v3_ov_mum`, `v3_ov_veteran`,
    `v3_ov_dispatch`) and `v3_ov_genie`, BOTH Top-Left (`x=36..1256, y=24..148`) and Top-Right
    (`x=1272..1884, y=24..148`) sit strictly inside `y=0..150` — 100% above the `y=158` `pip75`
    brushed-gold window frame and never covering the Host's or speakers' faces!
  - Auto-fits font sizes per line so text never clips or overflows any rounded HUD panel.
  - Strictly ZERO company names, ZERO real/fictional person names, and ZERO blame!
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
OUT_DIR = REPO_DIR / "episodes" / "S01E01_Employees_vs_Tech_CEO" / "overlays_v3"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

GOLD = (244, 208, 120, 255)
WHITE = (255, 255, 255, 255)
SOFT_SLATE = (212, 220, 236, 248)
AMBER_WARN = (255, 190, 118, 255)
EMERALD_OK = (126, 242, 182, 255)
PANEL_BG = (8, 12, 22, 226)
HUD_BG = (10, 16, 28, 232)
GOLD_BORDER = (238, 200, 112, 225)


OVERLAY_SPECS = [
    {
        "fname": "v3_ov_poll.png",
        "left": {
            "box": (36, 24, 1312, 148),
            "kicker": "2025 → 2026 GLOBAL MARKET CORRECTION METRICS",
            "title": "2025: 154,000 Shifts  •  2026: 200,000+ Shifts  •  60,000 Voluntary Buyouts",
            "sub": "Tech • Banking & Fintech • Logistics & Auto • Retail & Customer Support",
        },
        "right": {
            "box": (1330, 24, 1884, 226),
            "header": "SECTOR BREAKDOWN (2025–2026)",
            "rows": [
                ("• Cloud & Software: 60K Buyout Offers", WHITE),
                ("• Logistics & Auto: 30K+ Restructured", SOFT_SLATE),
                ("• Banking & Fintech: AI Consolidation", SOFT_SLATE),
                ("• India Offshore Hubs: 25K–35K Shifts", SOFT_SLATE),
                ("• Target Tier: 7+ Mgmt Layers & 50s", GOLD),
            ],
        },
    },
    {
        "fname": "v3_ov_ceo.png",
        "left": {
            "box": (36, 24, 1300, 148),
            "kicker": "EXECUTIVE DIALOGUE  •  INDUSTRIES AS HIGHWAYS & VITAL ORGANS",
            "title": "$720B/yr AI Infrastructure  •  9–12 Month Voluntary Buyout Bridges",
            "sub": "Highways are pathways for travelers—never the final destination",
        },
        "right": {
            "box": (1318, 24, 1884, 198),
            "header": "THE 7D PATHWAY RULE",
            "rows": [
                ("✓ Tick ≥ 4 of 7D  →  Stay the Course", EMERALD_OK),
                ("✗ Tick < 4 of 7D  →  Change Your Route", AMBER_WARN),
                ("DUTY • DIGNITY • DISCIPLINE • DHARMA", WHITE),
                ("DEVOTION • DIVINE • DESTINY", GOLD),
            ],
        },
    },
    {
        "fname": "v3_ov_layers.png",
        "left": {
            "box": (36, 24, 1300, 148),
            "kicker": "KARMIC MARKET CORRECTION  •  WHY IT & CORPORATES RESET",
            "title": "IT Exists for Connectedness — Reconnecting Workers to Real Home",
            "sub": "50 yrs of just earning to survive = overgrown forest yielding no fruit",
        },
        "right": {
            "box": (1318, 24, 1884, 198),
            "header": "CORRECTION METRICS",
            "rows": [
                ("• 7+ Mgmt Layers Flattened: -20%", WHITE),
                ("• Voluntary Exit Runway: 9–12 Mos", EMERALD_OK),
                ("• Purpose: Prune Overgrown Limbs", SOFT_SLATE),
                ("• Outcome: Yield Fruit for Family", GOLD),
            ],
        },
    },
    {
        "fname": "v3_ov_expat.png",
        "left": {
            "box": (34, 22, 1152, 148),
            "kicker": "QUESTION #1  •  12 YEARS ABROAD ON VISA vs. AGING FATHER",
            "title": "\"Chasing dollars abroad, 3 years became 12—why did the buyout feel like relief?\"",
            "sub": "7D Diagnosis: Disconnected from real home & aging father",
        },
        "right": {
            "box": (1168, 22, 1886, 148),
            "header": "7D METRIC: 2/7 → 6/7 (CHANGE ROUTE!)",
            "rows": [
                ("Stagnant Abroad (2/7): ✓Discipline ✓Pay  ✗Duty ✗Devotion ✗Dharma", AMBER_WARN),
                ("Buyout Home (6/7): ✓DUTY ✓DIGNITY ✓DEVOTION ✓DHARMA ✓DIVINE ✓DESTINY", EMERALD_OK),
            ],
        },
    },
    {
        "fname": "v3_ov_mum.png",
        "left": {
            "box": (34, 22, 1152, 148),
            "kicker": "QUESTION #2  •  7 MANAGEMENT LAYERS FLATTENED",
            "title": "\"When 35% of manager titles vanished, did I win back my child's childhood?\"",
            "sub": "7D Diagnosis: Trading 7 years of bedtimes for a status rung",
        },
        "right": {
            "box": (1168, 22, 1886, 148),
            "header": "7D METRIC: 2/7 → 5/7 (CHANGE ROUTE!)",
            "rows": [
                ("Status Rung (2/7): ✓Discipline ✓Title  ✗Devotion ✗Duty ✗Destiny", AMBER_WARN),
                ("Daylight Motherhood (5/7): ✓DEVOTION ✓DUTY ✓DIGNITY ✓DHARMA ✓DESTINY", EMERALD_OK),
            ],
        },
    },
    {
        "fname": "v3_ov_veteran.png",
        "left": {
            "box": (34, 22, 1152, 148),
            "kicker": "QUESTION #3  •  AGE 50s VETERAN & 35 YEARS OF MASTERY",
            "title": "\"Do we survive in an overgrown forest—or bear fruit through mentoring & peace?\"",
            "sub": "7D Diagnosis: 50 years just to earn & survive = overgrown tree without fruit",
        },
        "right": {
            "box": (1168, 22, 1886, 148),
            "header": "7D METRIC: 3/7 → 6/7 (CHANGE ROUTE!)",
            "rows": [
                ("Clinging to Rung (3/7): ✓Discipline ✓Duty  ✗Dignity ✗Peace ✗Destiny", AMBER_WARN),
                ("Seasoned Oak (6/7): ✓DIGNITY ✓DUTY ✓DHARMA ✓DISCIPLINE ✓DIVINE ✓DESTINY", EMERALD_OK),
            ],
        },
    },
    {
        "fname": "v3_ov_dispatch.png",
        "left": {
            "box": (34, 22, 1152, 148),
            "kicker": "QUESTIONS #4–#6  •  TOKYO SURVIVOR  •  YOUNG GRAD  •  HOMETOWN RETURN",
            "title": "\"Carrying 5 pagers alone vs. leaving metro rent for Coimbatore courtyard peace\"",
            "sub": "7D Diagnosis: IT is about connectedness—reconnect to real home & build with AI",
        },
        "right": {
            "box": (1168, 22, 1886, 148),
            "header": "7D METRIC: Hometown & AI Builder = 6/7 ✓",
            "rows": [
                ("5-Pager Isolation (1/7): ✓Discipline  ✗Duty ✗Devotion ✗Dignity → CHANGE ROUTE", AMBER_WARN),
                ("Coimbatore & AI (6/7): ✓DUTY ✓DEVOTION ✓DIGNITY ✓DISCIPLINE ✓DHARMA ✓DESTINY", EMERALD_OK),
            ],
        },
    },
    {
        "fname": "v3_ov_genie.png",
        "left": {
            "box": (34, 22, 1152, 148),
            "kicker": "THE KARMIC GENIE  •  THE 7D WAY SCORECARD",
            "title": "\"Every single one is a blessing in disguise—a market correction back to purpose!\"",
            "sub": "Tick ≥ 4 of 7D: Duty • Dignity • Discipline • Dharma • Devotion • Divine • Destiny",
        },
        "right": {
            "box": (1168, 22, 1886, 148),
            "header": "7D MASTER SCORECARD (≥ 4/7 RULE)",
            "rows": [
                ("✓ 1. DUTY   ✓ 2. DIGNITY   ✓ 3. DISCIPLINE   ✓ 4. DHARMA", WHITE),
                ("✓ 5. DEVOTION   ✓ 6. DIVINE   ✓ 7. DESTINY  →  BLESSING IN DISGUISE", EMERALD_OK),
            ],
        },
    },
]


def fit_font(draw: ImageDraw.ImageDraw, text: str, font_path: str, start_px: int, min_px: int, max_w: int):
    for sz in range(start_px, min_px - 1, -1):
        f = ImageFont.truetype(font_path, sz)
        w = draw.textbbox((0, 0), text, font=f)[2]
        if w <= max_w:
            return f
    return ImageFont.truetype(font_path, min_px)


def render_overlay(spec: dict):
    im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # --- 1. Top-Left Broadcast Header Card ---
    lx0, ly0, lx1, ly1 = spec["left"]["box"]
    l_max_w = (lx1 - lx0) - 42
    d.rounded_rectangle([lx0, ly0, lx1, ly1], radius=13, fill=PANEL_BG, outline=GOLD_BORDER, width=2)
    d.rounded_rectangle([lx0, ly0 + 10, lx0 + 6, ly1 - 10], radius=3, fill=GOLD)

    fk = fit_font(d, spec["left"]["kicker"], FONT_BOLD, 17, 13, l_max_w)
    ft = fit_font(d, spec["left"]["title"], FONT_BOLD, 23, 15, l_max_w)
    fs = fit_font(d, spec["left"]["sub"], FONT_REG, 17, 13, l_max_w)

    d.text((lx0 + 22, ly0 + 12), spec["left"]["kicker"], font=fk, fill=GOLD)
    d.text((lx0 + 22, ly0 + 40), spec["left"]["title"], font=ft, fill=WHITE)
    d.text((lx0 + 22, ly0 + 82), spec["left"]["sub"], font=fs, fill=SOFT_SLATE)

    # --- 2. Top-Right 7D Scorecard & Sector Metrics HUD Box ---
    rx0, ry0, rx1, ry1 = spec["right"]["box"]
    r_max_w = (rx1 - rx0) - 34
    d.rounded_rectangle([rx0, ry0, rx1, ry1], radius=13, fill=HUD_BG, outline=GOLD_BORDER, width=2)
    # Subtle gold header divider bar inside right HUD
    d.rounded_rectangle([rx0 + 2, ry0 + 2, rx1 - 2, ry0 + 36], radius=11, fill=(24, 32, 52, 240))
    d.line([(rx0 + 12, ry0 + 37), (rx1 - 12, ry0 + 37)], fill=(238, 200, 112, 130), width=1)

    fh = fit_font(d, spec["right"]["header"], FONT_BOLD, 17, 13, r_max_w)
    d.text((rx0 + 17, ry0 + 9), spec["right"]["header"], font=fh, fill=GOLD)

    rows = spec["right"]["rows"]
    avail_h = (ry1 - ry0) - 46
    step_y = avail_h / max(1, len(rows))
    start_font_px = 17 if len(rows) <= 3 else 16

    for idx, (rtxt, rcol) in enumerate(rows):
        fr = fit_font(d, rtxt, FONT_BOLD, start_font_px, 11, r_max_w)
        ry = int(ry0 + 43 + idx * step_y)
        d.text((rx0 + 17, ry), rtxt, font=fr, fill=rcol)

    out_path = OUT_DIR / spec["fname"]
    im.save(out_path)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for spec in OVERLAY_SPECS:
        render_overlay(spec)
    print(f"✅ Rendered {len(OVERLAY_SPECS)} dual-HUD (Metrics + 7D Scorecard) overlays in {OUT_DIR}")


if __name__ == "__main__":
    main()
