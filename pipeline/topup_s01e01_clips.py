#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Surgical Top-Up & QA-Replacement Generator for Karmic Genie Show S01E01 (16:9).
1. Harvests already-generated `tu2_munich_coimbatore` (3 clips) and `tu3_host_ivory` (2 clips)
   using `.cdk-overlay-pane button` download selectors.
2. Runs & harvests `tu1_arjun_elena` (4 clips) and `tu4_saintly_genie` (4 clips) with verified
   `chips>=1` and `arrow_forward` submit click.
"""

import json
import shutil
import time
from pathlib import Path
from generate_s01e01_full_film_clips import FlowFilmRunner, EP_CLIPS_DIR, DL_DIR, DORMANT_IMG, SAINTLY_IMG

TOPUP_DIR = EP_CLIPS_DIR / "topup_clean"


def close_menus(runner: FlowFilmRunner):
    runner.js("""(() => {
        document.querySelectorAll('.cdk-overlay-backdrop').forEach(b => b.click());
        const dis = Array.from(document.querySelectorAll('button')).find(x => (x.innerText||'').trim() === 'Dismiss');
        if (dis) dis.click();
    })()""")
    time.sleep(0.45)


def download_project_cards(runner: FlowFilmRunner, out_dir: Path, prefix: str, max_cards: int) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    cards_all = runner.get_video_cards()
    cnt = min(len(cards_all), max_cards)
    for idx in range(cnt):
        close_menus(runner)
        cards = runner.get_video_cards()
        if idx >= len(cards):
            break
        c = cards[idx]
        dest = out_dir / f"{prefix}_{idx+1:02d}.mp4"
        before_mp4s = set(DL_DIR.glob("*.mp4"))
        runner.js(f"""(() => {{
            const b = Array.from(document.querySelectorAll('button, [role="button"]'))[{c['moreIdx']}];
            if (b) {{ b.scrollIntoView({{block: 'center'}}); b.click(); }}
        }})()""")
        time.sleep(0.85)
        runner.js("""(() => {
            const dl = Array.from(document.querySelectorAll('.cdk-overlay-pane button, [role="menuitem"]'))
                .find(i => (i.innerText||'').toLowerCase().includes('download'));
            if (dl) dl.click();
        })()""")
        time.sleep(0.85)
        runner.js("""(() => {
            const orig = Array.from(document.querySelectorAll('.cdk-overlay-pane button, [role="menuitem"]'))
                .find(i => (i.innerText||'').includes('720p') || (i.innerText||'').toLowerCase().includes('original'));
            if (orig) orig.click();
        })()""")
        for _ in range(28):
            time.sleep(0.6)
            crs = list(DL_DIR.glob("*.crdownload"))
            diff = [f for f in (set(DL_DIR.glob("*.mp4")) - before_mp4s) if f.stat().st_size > 200_000]
            if diff and not crs:
                newest = sorted(diff, key=lambda p: p.stat().st_mtime, reverse=True)[0]
                shutil.copy2(newest, dest)
                saved.append({"file": dest.name, "label": c["label"], "size_mb": round(dest.stat().st_size / 1e6, 2)})
                print(f"    ✅ Saved {dest.name} ({dest.stat().st_size/1e6:.2f} MB) <- {c['label']}", flush=True)
                break
        close_menus(runner)
    (out_dir / f"{prefix}_manifest.json").write_text(json.dumps(saved, indent=2), encoding="utf-8")
    return saved


def ensure_image_chip(runner: FlowFilmRunner, image_path: Path | None, include_me: bool):
    runner.attach_ingredients(image_path, include_me)
    if image_path is not None:
        has_img = runner.js("Array.from(document.querySelectorAll('flow-ingredient-chip')).some(c => !(c.innerText||'').includes('face'))")
        if not has_img:
            stem = image_path.stem
            idx = runner.js(f"""(() => {{
                const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                for (let i = 1; i < btns.length; i++) {{
                    const lbl = (btns[i].getAttribute('aria-label')||'') + ' ' + (btns[i].innerText||'');
                    if (lbl.includes({json.dumps(stem)})) {{
                        for (let j = i - 1; j >= Math.max(0, i - 3); j--) {{
                            if (btns[j].getAttribute('aria-label') === 'More options') return j;
                        }}
                    }}
                }}
                return -1;
            }})()""")
            if idx is not None and idx >= 0:
                runner.js(f"Array.from(document.querySelectorAll('button, [role=\"button\"]'))[{idx}].click()")
                time.sleep(0.8)
                runner.js("""(() => {
                    const add = Array.from(document.querySelectorAll('.cdk-overlay-pane button, [role="menuitem"]'))
                        .find(i => (i.innerText||'').includes('Add to prompt'));
                    if (add) add.click();
                })()""")
                time.sleep(0.8)
                close_menus(runner)
    chips = runner.js("document.querySelectorAll('flow-ingredient-chip').length")
    print(f"  Verified chips={chips} for image={image_path.name if image_path else 'None'}", flush=True)


def submit_reliable(runner: FlowFilmRunner, text: str):
    close_menus(runner)
    pm_pos = runner.js("""(() => {
        const el = document.querySelector('div.ProseMirror');
        if (!el) return null;
        const r = el.getBoundingClientRect();
        return {x: r.left + 40, y: r.top + 16};
    })()""")
    if pm_pos:
        runner.mouse_click(pm_pos["x"], pm_pos["y"])
        time.sleep(0.25)
    runner.js(f"""(() => {{
        const el = document.querySelector('div.ProseMirror');
        el.focus();
        document.execCommand('selectAll', false, null);
        document.execCommand('delete', false, null);
        document.execCommand('insertText', false, {json.dumps(text.strip())});
    }})()""")
    time.sleep(0.5)
    # Click button[aria-label="Start generation"] via real CDP mouse_click!
    sub_pos = runner.js("""(() => {
        const sub = document.querySelector('button[aria-label="Start generation"]') ||
                    Array.from(document.querySelectorAll('button')).filter(b => (b.innerText||'').trim() === 'arrow_forward').pop();
        if (!sub) return null;
        const rc = sub.getBoundingClientRect();
        return {x: rc.left + rc.width/2, y: rc.top + rc.height/2};
    })()""")
    if sub_pos:
        runner.mouse_click(sub_pos["x"], sub_pos["y"])
    else:
        runner.cdp("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
        runner.cdp("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
    time.sleep(1.2)


def harvest_existing(runner: FlowFilmRunner, prefix: str, proj_url: str, expected: int):
    existing = sorted(TOPUP_DIR.glob(f"{prefix}_*.mp4"))
    if len(existing) >= expected:
        print(f"⏭️  {prefix} already downloaded ({len(existing)}/{expected}).", flush=True)
        return
    print(f"📥 Harvesting existing generated cards for '{prefix}' from {proj_url}...", flush=True)
    runner.cdp("Page.navigate", {"url": proj_url})
    time.sleep(4.2)
    download_project_cards(runner, TOPUP_DIR, prefix, expected)


def run_and_harvest(runner: FlowFilmRunner, prefix: str, proj_url: str | None, image_path: Path | None, include_me: bool, prompt_text: str, expected: int):
    existing = sorted(TOPUP_DIR.glob(f"{prefix}_*.mp4"))
    if len(existing) >= expected:
        print(f"⏭️  {prefix} already downloaded ({len(existing)}/{expected}).", flush=True)
        return

    if proj_url:
        runner.cdp("Page.navigate", {"url": proj_url})
        time.sleep(4.2)
    else:
        runner.open_fresh_project()
    runner.configure_16x9()
    ensure_image_chip(runner, image_path, include_me)
    before_len = len(runner.get_video_cards())
    submit_reliable(runner, prompt_text)
    print(f"🎬 Submitted '{prefix}' ({expected} clips)...", flush=True)

    replied_go = False
    retried_timeout = 0
    t0 = time.time()
    while time.time() - t0 < 360:
        time.sleep(6)
        elapsed = int(time.time() - t0)
        tail = runner.js(r"document.body.innerText.slice(-900).replace(/\s+/g, ' ')") or ""
        if retried_timeout < 2 and ("The agent timed out" in tail or "Try again" in tail):
            clicked = runner.js("""(() => {
                const b = Array.from(document.querySelectorAll('button')).find(x => (x.innerText||'').trim() === 'Try again');
                if (b) { b.click(); return true; }
                return false;
            })()""")
            if clicked:
                retried_timeout += 1
                time.sleep(4)
                continue

        ask_triggers = ("Option B", "How would you like to proceed", "Would you like me to", "shall I proceed", "confirm before", "Let me know if")
        if not replied_go and any(k.lower() in tail.lower() for k in ask_triggers) and len(runner.get_video_cards()) == before_len:
            replied_go = True
            ensure_image_chip(runner, image_path, include_me)
            submit_reliable(runner, f"Proceed immediately—generate all {expected} widescreen 16:9 video clips right now in batch without asking any questions!")
            continue

        new_cnt = len(runner.get_video_cards()) - before_len
        is_running = ("\nstop\n" in (runner.js("document.body.innerText.toLowerCase()") or "")) or ("generating" in tail.lower())
        if elapsed % 18 == 0 or new_cnt >= expected:
            print(f"    [{elapsed:3d}s] {prefix}: newCards={new_cnt}/{expected} running={is_running}", flush=True)
        if new_cnt >= expected:
            time.sleep(3.0)
            break
        if new_cnt > 0 and not is_running and elapsed > 70:
            time.sleep(8.0)
            if (len(runner.get_video_cards()) - before_len) == new_cnt and ("\nstop\n" not in (runner.js("document.body.innerText.toLowerCase()") or "")):
                break

    download_project_cards(runner, TOPUP_DIR, prefix, max(0, len(runner.get_video_cards()) - before_len))


PROMPT_TU1 = """Generate 4 separate widescreen 16:9 photorealistic cinema video clips (8 seconds each, Omni 1.1 Flash with clear natural spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation:

1) S1_06_Arjun_Close: Intimate emotional close-up inside an elevated blue-seat modern studio-stadium row behind a curved glass barrier; 39-year-old Indian software engineer Arjun in a dark navy jacket speaks softly into a wireless mic: "I sent money home instead of presence—until one email erased everything."

2) S2_01_Elena_Stairs: Evening 8:40 PM rainy London flat; 42-year-old British engineering manager Elena sits quietly on carpeted stairs outside her sleeping nine-year-old son's bedroom door holding a ceramic mug, speaking gently: "Our London team built enterprise workflows—nothing with AI on the slide."

3) S2_02_Elena_Lamp: Warm evening close-up of 42-year-old Elena in soft lamp light in her London living room, speaking candidly: "Flattening thirty-five percent of managers erased seven years of missed bedtimes overnight."

4) S2_03_Elena_Walk: Candid afternoon shot on a leafy London sidewalk after light rain as 42-year-old Elena walks hand-in-hand in daylight with her nine-year-old son carrying his school backpack; Elena's voice reflects softly: "Walking my son home in daylight, he whispered: 'Mum, are you back?'"
"""

PROMPT_TU4 = """Generate 4 separate widescreen 16:9 photorealistic broadcast-cinema video clips (8 seconds each, Omni 1.1 Flash, zero burned-in subtitle captions) right now in batch without asking confirmation, strictly matching our attached Karmic Genie Show pure-white circular marble studio image where the luminous Celestial Karmic Genie floats SEATED IN CROSS-LEGGED LOTUS POSTURE above the jeweled gold lamp in front of the padded `Karmic Genie Show` logo and subtle brushed-gold 7D wall maxims. STRICT VISUAL & VOICE RULE: In ALL 4 clips, the Genie's legs MUST remain folded CROSS-LEGGED in lotus meditation posture (NEVER standing, NEVER vertical legs), and his voice MUST be soft-spoken, polite, gentle, and unhurried:

1) S5_06_Genie_Mirrors: Serene close-medium shot of the cross-legged wise-saint Karmic Genie opening his palms gently above the gold lamp, speaking softly and clearly: "Where power sits, restraint. Where love waited, presence. Where shoulders ache, compassion."

2) S6_05_Genie_Blessing: Intimate peaceful close-medium shot of the cross-legged Karmic Genie smiling kindly above the lamp, offering an open question softly and clearly: "When golden handcuffs loosen while aging parents still wait—is this a blessing in disguise?"

3) S6_06_Genie_Who_Behind: Smooth gentle glide past the brushed-gold 7D stage wall beside the floating cross-legged Karmic Genie, who asks softly and clearly: "With daylight walks in London and smiling elders in Coimbatore—who fell behind?"

4) S7_03_Genie_Lotus_Dissolve: Symmetrical studio shot of the Celestial Karmic Genie remaining strictly SEATED IN CROSS-LEGGED LOTUS MEDITATION POSTURE floating above the gold lamp; while staying cross-legged with palms joined in a grateful namaste bow, his cross-legged form dissolves directly into gentle ribbons of gold, emerald, and sapphire stardust drifting back inside the jeweled lamp on the glass table (strictly no standing up, no spoken dialogue, soft chime ambience only).
"""


def wait_and_harvest_active(runner: FlowFilmRunner, prefix: str, image_path: Path | None, include_me: bool, expected: int):
    print(f"⏳ Waiting on active Flow project for '{prefix}' ({expected} clips)...", flush=True)
    replied_go = False
    t0 = time.time()
    while time.time() - t0 < 240:
        time.sleep(6)
        elapsed = int(time.time() - t0)
        tail = runner.js(r"document.body.innerText.slice(-900).replace(/\s+/g, ' ')") or ""
        ask_triggers = ("Option B", "How would you like to proceed", "Would you like me to", "shall I proceed", "confirm before", "Let me know if")
        if not replied_go and any(k.lower() in tail.lower() for k in ask_triggers) and len(runner.get_video_cards()) == 0:
            replied_go = True
            ensure_image_chip(runner, image_path, include_me)
            submit_reliable(runner, f"Proceed immediately—generate all {expected} widescreen 16:9 video clips right now in batch without asking any questions!")
            continue
        cnt = len(runner.get_video_cards())
        is_running = ("\nstop\n" in (runner.js("document.body.innerText.toLowerCase()") or "")) or ("generating" in tail.lower())
        if elapsed % 18 == 0 or cnt >= expected:
            print(f"    [{elapsed:3d}s] {prefix}: cards={cnt}/{expected} running={is_running}", flush=True)
        if cnt >= expected:
            time.sleep(3.0)
            break
        if cnt > 0 and not is_running and elapsed > 55:
            time.sleep(8.0)
            if len(runner.get_video_cards()) == cnt:
                break
    download_project_cards(runner, TOPUP_DIR, prefix, len(runner.get_video_cards()))


def main():
    TOPUP_DIR.mkdir(parents=True, exist_ok=True)
    runner = FlowFilmRunner()
    try:
        # 1. Wait for already-submitted tu4_saintly_genie on current tab!
        if len(sorted(TOPUP_DIR.glob("tu4_saintly_genie_*.mp4"))) < 4 and "c56bfc02-3eed-4378-adcc-10c967ab42e4" in (runner.js("location.href") or ""):
            wait_and_harvest_active(runner, "tu4_saintly_genie", SAINTLY_IMG, False, 4)
        # 2. Ensure tu2 & tu3 harvested
        harvest_existing(runner, "tu2_munich_coimbatore", "https://flow.google.com/u/0/project/fa372938-c128-4688-8796-502d267c5d4d", 3)
        harvest_existing(runner, "tu3_host_ivory", "https://flow.google.com/u/0/project/895f38ac-4ec1-4d94-b51f-b1f8d005f677", 2)
        # 3. Submit & harvest tu1_arjun_elena (4 clips)
        run_and_harvest(runner, "tu1_arjun_elena", "https://flow.google.com/u/0/project/a194ab9a-fb7d-4d99-bd10-fb103ef526de", None, False, PROMPT_TU1, 4)
        # 4. Fallback check for tu4 if needed
        run_and_harvest(runner, "tu4_saintly_genie", "https://flow.google.com/u/0/project/c56bfc02-3eed-4378-adcc-10c967ab42e4", SAINTLY_IMG, False, PROMPT_TU4, 4)
        print("\n🏆 ALL 13 TOP-UP CLIPS DOWNLOADED TO topup_clean!", flush=True)
    finally:
        runner.close()


if __name__ == "__main__":
    main()
