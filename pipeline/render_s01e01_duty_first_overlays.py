#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renders crisp 1920x1080 RGBA transparent cinema glass badges (top-left safe zone,
never colliding with bottom-center subtitles) for:
  The Karmic Genie Show — Season 1, Episode 1 ("1. Respect Your DUTY First.")
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_DIR / "episodes" / "S01E01_Respect_Your_Duty_First" / "overlays"

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
        fill=(15, 23, 42, 178),
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
        "ov_df_01_day1_traffic.png",
        "DAY 1 • HEAVY 10-CAR EVENING TRAFFIC",
        "Minor Accident 15 Mins Earlier — 108 Already Called",
        "Zero Causation • Zero Neglect • Effortless Peaceful Sleep",
        (96, 198, 255),
    ),
    (
        "ov_df_02_day2_caused_accident.png",
        "DAY 2 • DUSK RAIN • [SCENE TIME-PAUSE]",
        "Same Minor Accident — Except HIS Car Caused It",
        "First Witness on Scene • Calling 108 & Rushing Away",
        (244, 168, 82),
    ),
    (
        "ov_df_03_conscience_230am.png",
        "2:30 A.M. • THE INNER WITNESS (MANASATCHI)",
        "Why Guilt Steals His Sleep Tonight",
        "Wife's Mirror: 'You Caused It — You Should Have Helped Him!'",
        (244, 196, 92),
    ),
    (
        "ov_df_04_white_stage_d1.png",
        "THE KARMIC GENIE SHOW • VIRTUE #1 OF 7D",
        "1. Respect Your DUTY First.",
        "True Duty = The Task Whose Neglect Awakens Guilt in Conscience",
        (218, 178, 92),
    ),
    (
        "ov_df_05_nature_100_duty.png",
        "COSMIC LAW • EVERY LIVING BEING",
        "Banyan Tree • Honeybee • Flowing River (100% Duty)",
        "Illaram (Loving Family Life) = Safest & Fastest Path for Soul Growth",
        (82, 214, 168),
    ),
    (
        "ov_df_06_lifecycle_stages.png",
        "VEDIC LIFECYCLE DUTY MATRIX",
        "Age 4: 100% Play (Body) → Ages 8–16: 50/50 Study & Play",
        "Age 24: Independent Thinking (Mind) → Age 54: Thanking (Soul)",
        (96, 198, 255),
    ),
    (
        "ov_df_07_porul_and_arul.png",
        "SACRED HOUSEHOLDER DHARMA (ILLARAM)",
        "Father: 50% Spotless Porul • Mother: 50% Sacred Arul & Pooja",
        "Turning Four Brick Walls into a Living Temple of Warmth",
        (244, 180, 92),
    ),
    (
        "ov_df_08_only_you_can_do.png",
        "AFTER TODAY'S DUTY IS DONE • 7 SCENES",
        "Do the Things That ONLY YOU Can Do",
        "Father • Mother • Child to Elders • Spouse • Body • Conscience • Swadharma",
        (218, 178, 92),
    ),
    (
        "ov_df_09_daily_golden_rule.png",
        "THE IRON DAILY LAW OF HUMAN TIME",
        "1. Duty First → 2. What ONLY YOU Can Do → NOTHING MORE",
        "Doing Anything Else Wastes Your Priceless Human Birth",
        (244, 196, 92),
    ),
    (
        "ov_df_10_respect_all_duty.png",
        "UNIVERSAL DIGNITY • ZERO DEMEANING",
        "Respect Your Own Duty — And Respect Everyone Else's Duty",
        "Every Honest 10/10 Worker Stands Noble Before the Divine",
        (82, 214, 168),
    ),
    (
        "ov_df_11_redemption_relief.png",
        "PUBLIC & ENVIRONMENTAL DUTY • REDEMPTION CUT",
        "Stopping in the Rain to Help the Wounded Stranger",
        "Conscience Rewards Completed Duty with a Deep Sigh of Relief",
        (96, 198, 255),
    ),
    (
        "ov_df_12_genie_pillow_test.png",
        "CELESTIAL KARMIC GENIE • 35 / 70 THRESHOLD",
        "The 5-Question Tonight Conscience & Pillow Test",
        "Fulfill Duty • Free Your Heart • Sleep in Unbroken Divine Peace",
        (244, 196, 92),
    ),
]


def main():
    for args in BADGES:
        p = make_badge(*args)
        print(f"✅ Rendered overlay badge: {p.relative_to(REPO_DIR)}")


if __name__ == "__main__":
    main()
