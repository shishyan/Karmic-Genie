#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renders crisp Broadcast News-Channel Bottom Banner + Smooth Rolling News Ticker assets
(strictly <= 2 lines height max at the very bottom of the 1920x1080 frame, y=1004..1080,
leaving zero floating left boxes and zero background in the center!) for:
  The Karmic Genie Show — Season 1, Episode 1 ("1. Respect Your DUTY First.")

Outputs per `ov_df_XX_*.png` in `episodes/S01E01_Respect_Your_Duty_First/overlays/`:
  1. `<stem>.png` (1920x1080 RGBA):
     - Clean borderless/backgroundless centered subtle top-of-scene kicker OR pure clear canvas above y=1004,
       plus the prominent 2-Line Broadcast News-Channel Bottom Bar (`y=1004..1080`, `76px` tall):
       • Line 1 (`y=1007..1041`, `34px`): Centered bold gold-and-white Broadcast News Headline with a live pill tag.
       • Line 2 (`y=1042..1080`, `38px`): Deep broadcast ticker track (`#102347`) where the animated rolling
         news strip (`<stem>_ticker.png`) scrolls smoothly right-to-left during video compositing!
  2. `<stem>_ticker.png` (`W_tick x 36` RGBA):
     - Crisp single-line news-ticker ribbon rendered once at high DPI so FFmpeg scrolls it smoothly
       at 60fps/30fps (`overlay=x='1920-mod(t*165, 1920+tw)':y=1043`) like a live television news channel!
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_DIR / "episodes" / "S01E01_Respect_Your_Duty_First" / "overlays"

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
if not Path(FONT_BOLD).exists():
    FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def make_news_banner(filename: str, kicker: str, headline: str, subline: str, accent_rgb=(242, 201, 76)):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    f_tag = ImageFont.truetype(FONT_BOLD, 17)
    f_head = ImageFont.truetype(FONT_BOLD, 21)
    f_tick = ImageFont.truetype(FONT_BOLD, 19)

    # === STRICTLY 2-LINE PROMINENT BROADCAST NEWS BAR AT BOTTOM (y=1004..1080, height=76px) ===
    bar_y0 = 1004
    line1_y0 = 1007
    line2_y0 = 1042

    # Prominent 3px 24k-gold top attention border across full 1920px width
    draw.rectangle([0, bar_y0, 1920, bar_y0 + 3], fill=(242, 201, 76, 255))

    # Line 1 background (y=1007..1042): Rich Royal Midnight Navy (#0A1733, alpha 246)
    draw.rectangle([0, line1_y0, 1920, line2_y0], fill=(10, 23, 51, 246))

    # Line 2 background (y=1042..1080): High-attention Deep Crimson-Indigo News Ticker Track (#142B59, alpha 250)
    draw.rectangle([0, line2_y0, 1920, 1080], fill=(18, 39, 78, 250))
    draw.rectangle([0, line2_y0, 1920, line2_y0 + 1], fill=(242, 201, 76, 130))

    # Centered Line 1 composition: [ GOLD/CRIMSON NEWS BADGE ]  Headline Text Centered!
    tag_txt = kicker.split("•")[0].strip()
    rest_kicker = kicker.split("•", 1)[1].strip() if "•" in kicker else ""
    full_line1_head = f"{rest_kicker} — {headline}" if rest_kicker else headline

    tb_tag = draw.textbbox((0, 0), tag_txt, font=f_tag)
    tag_w = (tb_tag[2] - tb_tag[0]) + 28
    tb_hd = draw.textbbox((0, 0), full_line1_head, font=f_head)
    hd_w = tb_hd[2] - tb_hd[0]

    total_w = tag_w + 18 + hd_w
    start_x = max(24, (1920 - total_w) // 2)

    # Prominent Live News Pill on Line 1
    draw.rounded_rectangle(
        [start_x, line1_y0 + 4, start_x + tag_w, line2_y0 - 4],
        radius=6,
        fill=(188, 32, 46, 255),
        outline=(242, 201, 76, 230),
        width=1,
    )
    draw.text((start_x + 14, line1_y0 + 7), tag_txt, font=f_tag, fill=(255, 255, 255, 255))

    # Crisp centered Headline right beside the pill
    draw.text(
        (start_x + tag_w + 18, line1_y0 + 6),
        full_line1_head,
        font=f_head,
        fill=(255, 246, 214, 255),
    )

    out_p = OUT_DIR / filename
    img.save(out_p)

    # === LINE 2 ROLLING NEWS TICKER STRIP (`<stem>_ticker.png`) ===
    # Repeat ticker message twice with bullet separators so long & short shots always have rich rolling news!
    unit_msg = f"   •   {kicker}: {subline.upper()}   •   {headline.upper()}"
    repeated_msg = (unit_msg * 3) + "   •   "
    tb_tk = draw.textbbox((0, 0), repeated_msg, font=f_tick)
    tk_w = (tb_tk[2] - tb_tk[0]) + 64
    tk_img = Image.new("RGBA", (tk_w, 36), (0, 0, 0, 0))
    tk_draw = ImageDraw.Draw(tk_img)
    tk_draw.text((24, 7), repeated_msg, font=f_tick, fill=(255, 255, 255, 255))

    tk_out = OUT_DIR / f"{Path(filename).stem}_ticker.png"
    tk_img.save(tk_out)
    return out_p, tk_out


BADGES = [
    (
        "ov_df_01_day1_traffic.png",
        "DAY 1 • EVENING TRAFFIC",
        "Minor Accident 15 Mins Earlier — 108 Already Called",
        "Zero Causation • Zero Neglect • Effortless Peaceful Sleep Tonight",
        (96, 198, 255),
    ),
    (
        "ov_df_02_day2_caused_accident.png",
        "DAY 2 • TIME-PAUSE",
        "Same Minor Accident — Except HIS Car Caused It",
        "First Witness on Scene • Calling 108 & Rushing Away Without Helping",
        (244, 168, 82),
    ),
    (
        "ov_df_03_conscience_230am.png",
        "2:30 A.M. • MANASATCHI",
        "Why Burning Guilt Steals His Sleep Tonight",
        "Wife's Mirror: 'You Caused It — Helping Him Became YOUR Duty!'",
        (244, 196, 92),
    ),
    (
        "ov_df_04_white_stage_d1.png",
        "7D VIRTUE #1 • STUDIO",
        "1. Respect Your DUTY First.",
        "True Duty = The Sacred Task Whose Neglect Awakens Guilt in Conscience",
        (218, 178, 92),
    ),
    (
        "ov_df_05_nature_100_duty.png",
        "COSMIC LAW • 100% DUTY",
        "Banyan Tree • Honeybee • Flowing River",
        "Illaram (Loving Family Life) = Safest & Fastest Highway for Soul Growth",
        (82, 214, 168),
    ),
    (
        "ov_df_06_lifecycle_stages.png",
        "VEDIC LIFECYCLE MATRIX",
        "Age 4: 100% Play → Ages 8–16: 50/50 Study & Teamwork",
        "Age 24: Independent Thinking (Mind) → Age 54: Pure Nandri Gratitude (Soul)",
        (96, 198, 255),
    ),
    (
        "ov_df_07_porul_and_arul.png",
        "ILLARAM • FAMILY DHARMA",
        "Father: 50% Spotless Porul • Mother: 50% Sacred Arul & Pooja",
        "Turning Four Brick Walls into a Living Temple of Warmth & Divinity",
        (244, 180, 92),
    ),
    (
        "ov_df_08_only_you_can_do.png",
        "BEYOND DAILY DUTY",
        "Do the Sacred Things That ONLY YOU Can Do",
        "Father • Mother • Child to Elders • Life-Partner • Body • Conscience • Swadharma",
        (218, 178, 92),
    ),
    (
        "ov_df_09_daily_golden_rule.png",
        "IRON DAILY TIME LAW",
        "1. Duty First → 2. What ONLY YOU Can Do → NOTHING ELSE",
        "Doing Anything Outside Those Two Wastes Your Priceless Human Birth",
        (244, 196, 92),
    ),
    (
        "ov_df_10_respect_all_duty.png",
        "UNIVERSAL DIGNITY",
        "Respect Your Duty — And Respect Everyone Else's Duty",
        "Every Honest 10/10 Worker Stands Noble as Any King Before the Divine",
        (82, 214, 168),
    ),
    (
        "ov_df_11_redemption_relief.png",
        "REDEMPTION IN THE RAIN",
        "Stopping to Bandage & Help the Wounded Stranger",
        "Conscience Rewards Completed Duty with a Full-Chest Sigh of Relief",
        (96, 198, 255),
    ),
    (
        "ov_df_12_genie_pillow_test.png",
        "KARMIC GENIE • 35/70",
        "The 5-Question Tonight Conscience & Pillow Test",
        "Fulfill Duty • Free Your Heart • Sleep in Unbroken Divine Peace",
        (244, 196, 92),
    ),
]


def main():
    for args in BADGES:
        p, tk = make_news_banner(*args)
        print(f"✅ Rendered 2-line news banner + rolling ticker: {p.name} + {tk.name}")


if __name__ == "__main__":
    main()
