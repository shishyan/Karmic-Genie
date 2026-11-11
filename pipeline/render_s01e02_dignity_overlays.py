#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renders crisp 1920x1080 RGBA transparent cinema glass badges (top-left safe zone,
never colliding with bottom-center subtitles) for:
  The Karmic Genie Show — Season 1, Episode 2 ("2. Earn with DIGNITY Always.")
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_DIR / "episodes" / "S01E02_Earn_With_Dignity_Always" / "overlays"

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
        "ov_ed_01_midnight_unwatched.png",
        "11:45 P.M. • WHEN NO ONE ON EARTH WATCHES",
        "The Easy Shortcut vs. Unbought Integrity",
        "Hiding One Safety Flaw & Stealing Junior Arjun's Credit",
        (244, 168, 82),
    ),
    (
        "ov_ed_02_mirror_conscience.png",
        "1:30 A.M. • CONSCIENCE REJECTION (MANASATCHI)",
        "No Witness Saw — Yet His Own Mirror Rejects Him",
        "Bought Status Collapses Before Conscience & Loving Home",
        (244, 196, 92),
    ),
    (
        "ov_ed_03_white_stage_d2.png",
        "THE KARMIC GENIE SHOW • VIRTUE #2 OF 7D",
        "2. Earn with DIGNITY Always.",
        "Right Thing • Right Time • Right People > Easy Thing Unwatched",
        (218, 178, 92),
    ),
    (
        "ov_ed_04_nature_integrity.png",
        "NATURE'S 100% UNBOUGHT DIGNITY",
        "Unstained Lotus • Upright Bamboo • Gentle Honeybee",
        "Thiruvalluvar's Maanam (Kural 969) Guarded Safest in Family Life",
        (82, 214, 168),
    ),
    (
        "ov_ed_05_youth_integrity.png",
        "LIFECYCLE INTEGRITY • AGES 4 TO 24",
        "Age 4 Unshamed Play → Honest Exam Effort → Debt-Free Skill",
        "Never Turning Children into Trophies • Proud of Honest Parents",
        (96, 198, 255),
    ),
    (
        "ov_ed_06_spine_porul_arul.png",
        "ADULTHOOD DIGNITY • ILLARAM COVENANT",
        "Age 24 Unbuyable Spine • Clean Porul • Royal Arul (Kural 241)",
        "Right Livelihood (Samma Ajiva) & Sacred Home Lamp Grace",
        (244, 180, 92),
    ),
    (
        "ov_ed_07_shared_credit_nandri.png",
        "LEADERSHIP & ELDER NOBILITY • AGES 36 TO 84+",
        "Age 40: Put Juniors' Names First • Age 54: 50% Grateful Nandri",
        "Past 60: An Unstained Conscience Is Your Royal Silver Crown",
        (82, 214, 168),
    ),
    (
        "ov_ed_08_four_unwatched_tests.png",
        "FOUR UNWATCHED INTEGRITY TESTS",
        "Extra Note Returned • Absent Peer Defended • Hidden Joint Rebuilt",
        "Gentle Respect Behind Closed Doors > Digital Persona Filters",
        (96, 198, 255),
    ),
    (
        "ov_ed_09_eastern_sages_unite.png",
        "TIMELESS EASTERN WISDOM CONVERGENCE",
        "Thiruvalluvar (Maanam) • Buddha (Hiri-Ottappa) • Confucius & Laozi",
        "Coarse Rice & Pure Water with Integrity > Dishonest Floating Gold",
        (218, 178, 92),
    ),
    (
        "ov_ed_10_karthik_bamboo_stand.png",
        "11:46 P.M. REDEMPTION • UPRIGHT BAMBOO SPINE",
        "Refusing the Lie & Putting Junior Arjun's Name First",
        "Right Thing • Right Time (11:48 P.M.) • Right People",
        (82, 214, 168),
    ),
    (
        "ov_ed_11_emperor_peace_sleep.png",
        "CLEAN MIDNIGHT MIRROR • 10 / 10 PEACE OF MIND",
        "Deep Sigh of Relief • Simple Rice & Emperor-Level Sleep",
        "When Nobody Owns Your Conscience, No Storm Steals Your Rest",
        (96, 198, 255),
    ),
    (
        "ov_ed_12_genie_mirror_audit.png",
        "CELESTIAL KARMIC GENIE • 35 / 70 THRESHOLD",
        "The 5-Question Tonight Mirror & Integrity Audit",
        "Duty (What) + Dignity (How) = Unshakeable 7D Foundation",
        (244, 196, 92),
    ),
]


def main():
    for args in BADGES:
        p = make_badge(*args)
        print(f"✅ Rendered S01E02 overlay badge: {p.relative_to(REPO_DIR)}")


if __name__ == "__main__":
    main()
