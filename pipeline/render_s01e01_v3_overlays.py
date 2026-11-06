#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renders 8 crisp, unnamed, compassionate 1920x1080 RGBA broadcast glass badges
for Karmic Genie Show S01E01 v3.1 ("The Grand Design & Blessings in Disguise").

Editorial & Philosophical Guarantees:
  - Strictly ZERO company names and ZERO real/fictional person names!
  - NEVER portrays any company, executive, city, or worker in a bad spot (zero "record profits"
    or blame); honors every industry and city as a vital organ in Earth's Grand Design!
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
OUT_DIR = REPO_DIR / "episodes" / "S01E01_Employees_vs_Tech_CEO" / "overlays_v3"

BADGES = [
    ("v3_ov_poll.png",
     "LIVE VIEWER CIRCLE  •  THE GRAND DESIGN IN MOTION",
     "200,000+ Shifts Across Tech, Banking, Shipping & Auto",
     "Every industry as a vital organ of Earth's living system • 60,000 Voluntary Buyout bridges"),
    ("v3_ov_ceo.png",
     "EXECUTIVE DIALOGUE  •  STEERING THE VITAL ORGANS",
     "Chief Executive — Reallocating Circulation for the AI Era",
     "$50B/qtr infrastructure renewal • 9–12 month Voluntary Buyout bridges for transitioning teams"),
    ("v3_ov_layers.png",
     "STRUCTURAL RENEWAL  •  CELLS, ORGANS & PURPOSE",
     "Streamlining Layers  •  Seasoned Veterans  •  Global Hubs",
     "Moving from routine administration to higher-purpose creation across every city and nation"),
    ("v3_ov_expat.png",
     "OVERSEAS REFLECTION  •  12 YEARS AWAY FROM HOME",
     "\"Chasing visas abroad, how easily three years became twelve.\"",
     "Aging father waiting beside the phone • Releasing postponed family duty & overdue reunion"),
    ("v3_ov_veteran.png",
     "SEASONED WISDOM  •  AGE 58  •  35-YEAR ARCHITECT",
     "\"How do we step into our next chapter gracefully?\"",
     "Built the enterprise foundations powering today • Turning toward mentoring, dignity & peace"),
    ("v3_ov_mum.png",
     "WORKING PARENT  •  STREAMLINED MANAGEMENT LAYER",
     "\"Seven years of missed bedtimes suddenly returned.\"",
     "Stepping beyond a corporate title • Reclaiming presence & afternoon walks at home"),
    ("v3_ov_dispatch.png",
     "GLOBAL PULSE  •  TOKYO, SÃO PAULO & COIMBATORE",
     "Surviving Teams  •  New Graduates  •  Hometown Returnees",
     "Every city and generation finding fresh equilibrium & purpose in a changing era"),
    ("v3_ov_genie.png",
     "THE KARMIC GENIE  •  THE 7D WAY",
     "\"Every single one is a blessing in disguise.\"",
     "Inspired by the 2-minute 'Single Thunderclap' parable • Serving mind, soul & higher purpose"),
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    f_kicker = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    f_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    f_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)

    for fname, kicker, title, sub in BADGES:
        low_all = f"{kicker} {title} {sub}".lower()
        assert "record profit" not in low_all and "greed" not in low_all and "heartless" not in low_all

        im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        w1 = d.textbbox((0, 0), kicker, font=f_kicker)[2]
        w2 = d.textbbox((0, 0), title, font=f_title)[2]
        w3 = d.textbbox((0, 0), sub, font=f_sub)[2]
        box_w = max(w1, w2, w3) + 64
        x0, y0 = 54, 34
        x1, y1 = x0 + box_w, y0 + 116

        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=(10, 14, 24, 218), outline=(235, 198, 112, 220), width=2)
        d.rounded_rectangle([x0, y0 + 12, x0 + 6, y1 - 12], radius=3, fill=(242, 204, 118, 255))
        d.text((x0 + 26, y0 + 14), kicker, font=f_kicker, fill=(242, 206, 122, 255))
        d.text((x0 + 26, y0 + 42), title, font=f_title, fill=(255, 255, 255, 255))
        d.text((x0 + 26, y0 + 79), sub, font=f_sub, fill=(208, 216, 232, 245))

        im.save(OUT_DIR / fname)
    print(f"✅ Rendered {len(BADGES)} Grand-Design v3 badges in {OUT_DIR}")


if __name__ == "__main__":
    main()
