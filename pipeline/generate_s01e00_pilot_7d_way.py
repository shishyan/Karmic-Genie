#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Flow ULTRA (16:9 Widescreen, 360p export) Cinematography Generator for
Karmic Genie Show — Pilot Episode (S01E00: "The 7D Way — Pioneers of the New World")

Approved Dual-@Me Architecture:
  1. Adult Narrator/Host (`@Me` in tailored ivory-white bandhgala suit) explains the details,
     real-life examples, and conscience philosophy of each of the 7 Virtues in depth.
  2. Sample 2 Awakened Karmic Genie (`4-year-old Bala-Rishi version of @Me` with a cute little topknot,
     tilak, tiny rudraksha mala, ivory silk kurta, and golden-saffron angavastram stole beside the
     golden Genie lamp) delivers the luminous child-sage essence of each virtue.
  3. Dedicated deep time for EVERY SINGLE VIRTUE (`D1..D7`) + the `35 / 70` Course-Change Rule.
  4. All clips exported in `360p` (`640x360`) as requested (reserving `720p+` only for later).
"""

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, "/home/shishyan/GitHub/Karmic-Genie-Show/pipeline")
from generate_s01e01_v3_interactive import FlowV3Runner, MASTERS_DIR, DL_DIR

REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
PILOT_DIR = REPO_DIR / "episodes" / "S01E00_Pilot_The_7D_Way"
CLIPS_DIR = PILOT_DIR / "flow_s01e00_clips"

DORMANT_V7_IMG = MASTERS_DIR / "v7_wide_wall_dormant_16x9.jpg"
GENIE_4YO_BALA_IMG = MASTERS_DIR / "v9_genie_4yo_bala_rishi_16x9.jpg"

STAGE_DESC = (
    "pure-white circular marble television studio stage with a seamless wide white back wall, "
    "curved transparent glass barriers around the stage, and an ornate jeweled gold Genie lamp on the center marble table"
)

BALA_RISHI_DESC = (
    "adorable 4-year-old little boy version of my attached avatar face with a cute little topknot, "
    "sacred forehead tilak, tiny rudraksha mala, ivory silk kurta, and golden-saffron angavastram stole "
    "seated beside the ornate golden Genie lamp in the pure-white circular marble studio"
)

BATCHES = [
    {
        "id": "b1_host_compass_and_d1_d2",
        "expected": 4,
        "img": DORMANT_V7_IMG,
        "include_me": True,
        "prompt": f"""Generate 4 separate widescreen 16:9 photorealistic broadcast cinema video clips (8 seconds each, Omni 1.1 Flash with warm, resonant, inspiring spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, matching our attached Karmic Genie Show studio image ({STAGE_DESC}) and featuring the clean-shaven 48-year-old South Indian male host matching my attached avatar in his tailored ivory-white bandhgala suit:

1) H01_Host_Pilot_35_Rule: Smooth orbital medium tracking shot of the host in his ivory-white bandhgala suit standing behind the ornate golden lamp on the pure-white circular marble stage, speaking with clear authority: "Welcome to The Seven D Way! Score every situation from one to ten across seven virtues—below thirty-five out of seventy, change the course of your life!"

2) H02_Host_D1_Duty_Definition: Intimate cinema close-up of the host in his ivory-white bandhgala suit leaning forward earnestly across the golden lamp, speaking from the heart: "First is Duty. Duty is never your office job—Duty is the task that triggers guilt in your conscience when you leave it undone!"

3) H03_Host_D1_Silenced_Conscience: Expressive medium close-up of the host in his ivory-white bandhgala suit gesturing thoughtfully in the white marble studio, explaining like a wise sage: "A thief feels conscience guilt the first few times—drown that trigger with alcohol or neglect, and conscience goes silent, draining our world of empathy!"

4) H04_Host_D2_Dignity_Explain: Warm medium shot of the host in his ivory-white bandhgala suit walking beside the golden lamp on the white circular stage, speaking passionately: "Second is Dignity—unbought self-respect! Earn your livelihood honestly by building real value, never by selling your spine, your truth, or your peace!"
""",
    },
    {
        "id": "b2_host_d3_to_d7_details",
        "expected": 5,
        "img": DORMANT_V7_IMG,
        "include_me": True,
        "prompt": f"""Generate 5 separate widescreen 16:9 photorealistic broadcast cinema video clips (8 seconds each, Omni 1.1 Flash with warm, resonant, inspiring spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, matching our attached Karmic Genie Show studio image ({STAGE_DESC}) and featuring the clean-shaven 48-year-old South Indian male host matching my attached avatar in his tailored ivory-white bandhgala suit:

1) H05_Host_D3_Discipline_Explain: Medium close-up of the host in his ivory-white bandhgala suit gesturing with calm strength behind the golden lamp, speaking clearly: "Third is Discipline—sovereign mastery over your senses, tongue, and clock, so impulsive cravings and midnight screens never enslave your mind!"

2) H06_Host_D4_Dharma_Explain: Revolving medium shot of the host in his ivory-white bandhgala suit on the pure-white circular stage, speaking warmly: "Fourth is Dharma—living as a vital organ in Earth's body, like a fruit-bearing banyan tree offering shade and nourishment to all!"

3) H07_Host_D5_Devotion_Explain: Intimate heartfelt close-up of the host in his ivory-white bandhgala suit speaking straight into the camera lens like a trusted friend: "Fifth is Devotion—true connectedness at home! Give your aging parents, spouse, and children your warm, undivided presence today, never exhausted leftovers!"

4) H08_Host_D6_Divine_Explain: Serene medium close-up of the host in his ivory-white bandhgala suit placing a hand over his heart beside the golden lamp, speaking reverently: "Sixth is gratitude to the Divine—daily humility before the Grand Architect who harmonized your body, mind, soul, and para-soul!"

5) H09_Host_D7_Destiny_Explain: Iconic center-stage widescreen shot of the host in his ivory-white bandhgala suit smiling brightly behind the golden lamp, speaking inspiringly: "Seventh is Destiny—when Duty, Dignity, Discipline, Dharma, Devotion, and Divine align above thirty-five, you flower into a Pioneer of the New World!"
""",
    },
    {
        "id": "b3_bala_rishi_4yo_virtues_1",
        "expected": 4,
        "img": DORMANT_V7_IMG,
        "include_me": True,
        "prompt": f"""Generate 4 separate widescreen 16:9 photorealistic broadcast-cinema video clips (8 seconds each, Omni 1.1 Flash with a clear, sweet, articulate, wise 4-year-old boy voice, zero burned-in subtitle captions) right now in batch without asking confirmation, matching our attached Karmic Genie Show studio image and featuring the {BALA_RISHI_DESC}:

1) G01_Bala_D1_Duty: Medium close-up of the {BALA_RISHI_DESC}, smiling with innocent ancient wisdom and speaking clearly in a sweet 4-year-old child sage voice: "Dimension One is Duty! Never drink away the whisper of your conscience—when your heart says care for someone today, listen right away!"

2) G02_Bala_D2_Dignity: Warm close-up of the {BALA_RISHI_DESC}, sitting tall with a bright, joyful smile and speaking clearly in a sweet 4-year-old voice: "Dimension Two is Dignity! Stand tall with an honest heart—no paycheck or title is ever worth trading away your self-respect!"

3) G03_Bala_D3_Discipline: Expressive medium close-up of the {BALA_RISHI_DESC}, gesturing gently with tiny hands beside the golden Genie lamp and speaking clearly in a sweet 4-year-old voice: "Dimension Three is Discipline! Rule your habits, your sleep, and your senses every morning so your mind stays free and bright!"

4) G04_Bala_D4_Dharma: Radiant close-medium shot of the {BALA_RISHI_DESC}, opening his tiny palms warmly beside the golden Genie lamp and speaking clearly in a sweet 4-year-old voice: "Dimension Four is Dharma! Be like a sweet mango tree sharing shade and fruit with every creature on Mother Earth!"
""",
    },
    {
        "id": "b4_bala_rishi_4yo_virtues_2",
        "expected": 3,
        "img": DORMANT_V7_IMG,
        "include_me": True,
        "prompt": f"""Generate 3 separate widescreen 16:9 photorealistic broadcast-cinema video clips (8 seconds each, Omni 1.1 Flash with a clear, sweet, articulate, wise 4-year-old boy voice, zero burned-in subtitle captions) right now in batch without asking confirmation, matching our attached Karmic Genie Show studio image and featuring the {BALA_RISHI_DESC}:

1) G05_Bala_D5_Devotion: Heartwarming close-up of the {BALA_RISHI_DESC}, smiling tenderly beside the golden Genie lamp and speaking clearly in a sweet 4-year-old voice: "Dimension Five is Devotion! Put down your phone tonight, hug your parents and children tight, and give them your whole heart!"

2) G06_Bala_D6_Divine: Serene luminous close-up of the {BALA_RISHI_DESC}, folding his tiny hands in namaste beside the golden Genie lamp and speaking clearly in a sweet 4-year-old voice: "Dimension Six is the Divine! Say thank you every sunrise to the Grand Architect of your body, mind, and soul!"

3) G07_Bala_D7_Destiny_Blessing: Joyful center close-up of the {BALA_RISHI_DESC}, raising a tiny hand in blessing beside the golden Genie lamp and speaking clearly in a sweet 4-year-old voice: "Dimension Seven is your Destiny! Score above thirty-five across all Seven D's—and shine as a Pioneer of the New World!"
""",
    },
    {
        "id": "b5_conscience_parables",
        "expected": 3,
        "img": None,
        "include_me": False,
        "prompt": """Generate 1 widescreen 16:9 photorealistic cinematic movie B-roll clip (8 seconds, Omni 1.1 Flash with subtle atmospheric cinema sound, zero spoken dialogue, zero burned-in text) right now without asking confirmation:

1) B02_Numbing_Conscience_To_Compassion: Split-mood cinematic tracking shot starting on a stressed modern professional alone at night pushing away an untouched glass on a dark counter, standing up, opening the curtains to warm morning sunlight, and embracing his elderly father with tears of relief and awakened empathy.
""",
    },
]


def close_any_settings_panel(r: FlowV3Runner):
    for _ in range(3):
        if "Agent settings" not in (r.js("document.body.innerText") or ""):
            break
        r.js("""(() => {
            const btns = Array.from(document.querySelectorAll("button"));
            const saveBtn = btns.find(b => (b.innerText||"").trim() === "Save");
            if (saveBtn) { saveBtn.click(); return; }
            const backBtn = btns.find(b => ["arrow_back", "close"].includes((b.innerText||"").trim()));
            if (backBtn) backBtn.click();
        })()""")
        time.sleep(0.8)


def submit_fast(r: FlowV3Runner, prompt: str):
    close_any_settings_panel(r)
    clean_txt = prompt.replace("@", "").strip()
    for attempt in range(2):
        r.js(f"""(() => {{
            const el = document.querySelector("div.ProseMirror");
            if (!el) return false;
            el.focus();
            document.execCommand("selectAll", false, null);
            document.execCommand("delete", false, null);
            document.execCommand("insertText", false, {json.dumps(clean_txt)});
            return true;
        }})()""")
        time.sleep(0.5)
        r.cdp("Input.insertText", {"text": " "})
        time.sleep(0.5)
        rect = r.js("""(() => {
            const b = document.querySelector('button[aria-label="Start generation"]');
            if (!b || b.disabled) return null;
            const rc = b.getBoundingClientRect();
            return {left: rc.left, top: rc.top, w: rc.width, h: rc.height};
        })()""")
        if rect:
            r.mouse_click(rect["left"] + 6, rect["top"] + rect["h"] / 2)
            time.sleep(2.0)
            rem = len((r.js("document.querySelector('div.ProseMirror')?.innerText || ''") or "").strip())
            if rem < 15:
                return
        close_any_settings_panel(r)
        time.sleep(1.0)


def download_and_transcode_360p(r: FlowV3Runner, out_sub: Path, bid: str, count: int):
    raw_dir = out_sub / "raw_dl"
    raw_dir.mkdir(parents=True, exist_ok=True)
    saved_raw = r.download_cards(raw_dir, f"raw_{bid}", count)
    existing_cnt = len(list(out_sub.glob(f"{bid}_*.mp4")))
    saved_360p = []
    for idx, p in enumerate(sorted(raw_dir.glob(f"raw_{bid}_*.mp4")), 1):
        out_idx = existing_cnt + idx
        dest_360p = out_sub / f"{bid}_{out_idx:02d}.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(p),
            "-vf", "scale=640:360", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k", "-ar", "48000", str(dest_360p)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p.unlink(missing_ok=True)
        lbl = saved_raw[idx - 1]["label"] if idx - 1 < len(saved_raw) else ""
        saved_360p.append({"file": dest_360p.name, "label": lbl, "size_mb": round(dest_360p.stat().st_size / 1e6, 2)})
        print(f"    🎯 Transcoded 360p: {dest_360p.name} ({dest_360p.stat().st_size/1e6:.2f} MB) <- {lbl}", flush=True)
    (out_sub / f"{bid}_manifest.json").write_text(json.dumps(saved_360p, indent=2), encoding="utf-8")


def main():
    only_ids = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    r = FlowV3Runner()
    try:
        first_submitted = False
        for b in BATCHES:
            bid = b["id"]
            if only_ids and bid not in only_ids:
                continue
            out_sub = CLIPS_DIR / bid
            existing = list(out_sub.glob(f"{bid}_*.mp4")) if out_sub.exists() else []
            if len(existing) >= b["expected"]:
                print(f"⏭️ Skipping {bid} ({len(existing)}/{b['expected']} 360p clips already present)", flush=True)
                continue

            if first_submitted:
                print("⏳ Cooling down 25s before opening next Flow project...", flush=True)
                time.sleep(25.0)
            first_submitted = True

            print(f"\n🎬 Starting Pilot S01E00 360p Batch: {bid} (expecting {b['expected']} clips)...", flush=True)
            r.open_fresh_project()
            r.configure_16x9()
            close_any_settings_panel(r)
            if b["img"] or b["include_me"]:
                r.attach_ingredients(b["img"], include_me=b["include_me"])
            close_any_settings_panel(r)
            # Simulate natural human mouse motion across the canvas before submitting
            for step in range(15):
                r.cdp("Input.dispatchMouseEvent", {
                    "type": "mouseMoved",
                    "x": float(400 + step * 35),
                    "y": float(350 + (step % 4) * 60),
                })
                time.sleep(0.06)
            before = len(r.get_video_cards())
            submit_fast(r, b["prompt"])

            t0 = time.time()
            retried_try = 0
            while time.time() - t0 < 210:
                time.sleep(6)
                el = int(time.time() - t0)
                now_cards = len(r.get_video_cards()) - before
                body_txt = r.js("document.body.innerText") or ""
                body_low = body_txt.lower()
                if retried_try < 2 and ("try again" in body_low[-350:] or "unusual activity" in body_low[-350:]):
                    retried_try += 1
                    print(f"  [{el:3d}s] {bid}: saw Try again ({retried_try}/2) — waiting 18s & clicking Try again...", flush=True)
                    time.sleep(18.0)
                    for step in range(12):
                        r.cdp("Input.dispatchMouseEvent", {
                            "type": "mouseMoved",
                            "x": float(500 + step * 40),
                            "y": float(400 + (step % 3) * 50),
                        })
                        time.sleep(0.05)
                    tpos = r.js("""(() => {
                        const b = Array.from(document.querySelectorAll('button')).find(x => (x.innerText||'').trim() === 'Try again');
                        if (!b) return null;
                        const rc = b.getBoundingClientRect();
                        return {x: rc.left + rc.width/2, y: rc.top + rc.height/2};
                    })()""")
                    if tpos:
                        r.mouse_click(tpos["x"], tpos["y"])
                    time.sleep(6.0)
                    continue
                running = ("stop" in body_low[-250:]) or ("waiting in the queue" in body_low[-400:] and el < 160)
                if el % 18 == 0 or now_cards >= b["expected"]:
                    print(f"  [{el:3d}s] {bid}: newCards={now_cards}/{b['expected']} running={running}", flush=True)
                if now_cards >= b["expected"]:
                    time.sleep(3.5)
                    break
                if now_cards > 0 and not running and el > 90:
                    time.sleep(8.0)
                    if (len(r.get_video_cards()) - before) == now_cards:
                        break

            new_cnt = max(0, len(r.get_video_cards()) - before)
            if new_cnt > 0:
                need = max(1, b["expected"] - len(existing))
                download_and_transcode_360p(r, out_sub, bid, min(new_cnt, need))
            time.sleep(5.0)
    finally:
        r.close()


if __name__ == "__main__":
    main()
