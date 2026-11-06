#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renders crisp 1920x1080 RGBA transparent broadcast documentary badges (top-left cinema safe zone,
never colliding with bottom-center subtitles) for Season 1, Episode 1:
  - Prologue 2025 -> Today Global Timeline & Verified Metrics cards
  - 7 Human Hats (Role, Age, Non-AI Division & Global City) cards
  - Act II Subtle Upanishad Reading Note & 7D Reflection Pillars
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show/episodes/S01E01_Employees_vs_Tech_CEO/overlays")

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def make_badge(filename: str, kicker: str, headline: str, subline: str, accent_rgb=(218, 178, 92)):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    f_kick = ImageFont.truetype(FONT_BOLD, 19)
    f_head = ImageFont.truetype(FONT_BOLD, 26)
    f_sub = ImageFont.truetype(FONT_REG, 20)

    w1 = draw.textbbox((0, 0), kicker, font=f_kick)[2]
    w2 = draw.textbbox((0, 0), headline, font=f_head)[2]
    w3 = draw.textbbox((0, 0), subline, font=f_sub)[2]
    box_w = max(w1, w2, w3) + 64
    box_h = 118
    x0, y0 = 68, 48

    # Subtle dark translucent slate-glass panel with champagne-gold left accent bar
    draw.rounded_rectangle(
        [x0, y0, x0 + box_w, y0 + box_h],
        radius=14,
        fill=(18, 22, 34, 178),
        outline=(255, 255, 255, 48),
        width=1,
    )
    draw.rounded_rectangle(
        [x0, y0 + 14, x0 + 6, y0 + box_h - 14],
        radius=3,
        fill=(*accent_rgb, 235),
    )

    draw.text((x0 + 26, y0 + 14), kicker, font=f_kick, fill=(*accent_rgb, 245))
    draw.text((x0 + 26, y0 + 42), headline, font=f_head, fill=(255, 255, 255, 248))
    draw.text((x0 + 26, y0 + 78), subline, font=f_sub, fill=(210, 220, 235, 235))

    img.save(OUT_DIR / filename)


def main():
    cards = [
        (
            "ov_p1_2025.png",
            "GLOBAL TIMELINE  •  EARLY – OCT 2025",
            "$410B Hyperscaler CapEx  |  154,445 US Tech Cuts",
            "Record corporate profits  •  Oct 2025: 14,000 Devices & Retail corporate roles cut",
        ),
        (
            "ov_p2_q1_2026.png",
            "GLOBAL TIMELINE  •  Q1 2026 (JAN – MAR)",
            "80,000+ Global Tech Cuts in 90 Days (48% Cite AI)",
            "Amazon +16,000  •  Oracle ~21,000  •  Dell ~11,000  •  Cisco ~4,000",
        ),
        (
            "ov_p3_today_2026.png",
            "GLOBAL TIMELINE  •  TODAY (LATE 2026)",
            "$720B–$760B/yr AI CapEx ($201.9B in Q3 Alone)",
            "325,900+ US cuts since Jan '25  •  Cuts hit Non-Cloud, Non-AI & Entry-Level (-20%)",
        ),
        (
            "ov_hat1_marcus.png",
            "HAT #1  •  SAN FRANCISCO, USA",
            "Marcus Vance, 51  —  Hyperscaler Chief Executive",
            "$50B+/qtr GPU & power CapEx pushed quarterly Free Cash Flow negative",
        ),
        (
            "ov_hat2_arjun.png",
            "HAT #2  •  SEATTLE, USA  ↔  MYSURU, INDIA",
            "Arjun Rao, 39  —  Overseas Expat Engineer (Consumer Devices)",
            "12 years abroad chasing $ & visa renewals  •  Non-AI Devices floor eliminated",
        ),
        (
            "ov_hat3_elena.png",
            "HAT #3  •  LONDON, UNITED KINGDOM",
            "Elena Rostova-Chen, 42  —  Enterprise SaaS & HR-Ops Manager",
            "Swept out in the >35% flattening of non-AI small-team middle management",
        ),
        (
            "ov_hat4_mateo.png",
            "HAT #4  •  SÃO PAULO, BRAZIL",
            "Mateo Silva, 23  —  First-Generation CS Graduate",
            "Ages 22–25 dev employment down ~20%  •  New grads down to 7% of Big Tech hires",
        ),
        (
            "ov_hat5_kenji.png",
            "HAT #5  •  TOKYO, JAPAN (11:54 PM)",
            "Kenji Takahashi, 35  —  Non-Cloud Retail Billing Engineer",
            "Surviving 80% under non-AI hiring freeze  •  Carrying 5 engineers' midnight pagers",
        ),
        (
            "ov_hat6_heinrich.png",
            "HAT #6  •  MUNICH, GERMANY",
            "Heinrich Weber, 58  —  On-Premise Hardware & Networking Architect",
            "35 years of traditional hardware craft impacted by non-cloud infrastructure cuts",
        ),
        (
            "ov_hat7_kavitha.png",
            "HAT #7  •  COIMBATORE, INDIA",
            "Kavitha Sundaram, 33  —  Former Metro Ops Lead → Hometown Builder",
            "Left Bengaluru overhead before HR/internal-tools automation  •  Living debt-free",
        ),
        (
            "ov_genie_7d.png",
            "THE KARMIC GENIE  •  OPEN REFLECTIONS (ZERO PREACHING)",
            "Essence of the 'Single Thunderclap'  —  The 7D Way",
            "Duty • Dignity • Discipline • Dharma • Devotion • Divine • Destiny",
        ),
    ]
    for fn, k, h, s in cards:
        make_badge(fn, k, h, s)
    print(f"✅ Rendered {len(cards)} transparent 1920x1080 documentary badges in {OUT_DIR}")


if __name__ == "__main__":
    main()
