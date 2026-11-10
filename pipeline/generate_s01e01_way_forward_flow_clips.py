#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resumable Google Flow ULTRA (Omni 1.1 Flash / Veo 3.1, 16:9 Widescreen) Batch Cinematography Generator
for Karmic Genie Show — Season 1, Episode 1:
  "THE WAY FORWARD (2026–2050): THE 280-MONTH GESTATION"

Key guarantees:
  - Uses the exact proven FlowFilmRunner CDP architecture from `generate_s01e01_full_film_clips.py`
    (connecting to Chrome DevTools Protocol on port 9225 or 9222).
  - Enforces the strict "Narrator (`Me`) + 1 Child ONLY" rule (`Me + Bala-Rishi` OR `Me + Bala-Matha`
    when a child speaks, NEVER both children together in the same scene).
  - Attaches each scene's canonical 16:9 storyboard reference image (`s01e01_flow_sb_01..12_*.jpg`)
    via `Page.setInterceptFileChooserDialog` + `DOM.setFileInputFiles` AND attaches the `Me` Avatar
    chip via `Avatars -> Me -> Add to prompt`.
  - Strips literal `@` characters from ProseMirror text insertion so Google Flow's ingredient parser
    never stalls on unresolved mentions.
  - Resumable per-scene/batch: skips any scene whose `.mp4` clips are already downloaded in
    `episodes/S01E01_The_Way_Forward_Master/flow_16x9_clips/`.
"""

import json
import os
import shutil
import sys
import time
import urllib.request
from pathlib import Path

try:
    import websocket
except ImportError:
    websocket = None

CDP_PORTS = [int(os.environ.get("FLOW_CDP_PORT", "9225")), 9222]
REPO_DIR = Path(__file__).resolve().parent.parent
STORYBOARD_JSON = REPO_DIR / "GOOGLE_FLOW_STORYBOARD_PACKAGE_S01E01.json"
EP_CLIPS_DIR = REPO_DIR / "episodes" / "S01E01_The_Way_Forward_Master" / "flow_16x9_clips"
DL_DIR = Path.home() / "Downloads"


def load_storyboard_batches() -> list[dict]:
    pkg = json.loads(STORYBOARD_JSON.read_text(encoding="utf-8"))
    batches = []
    for sc in pkg["episode_1_storyboard_scenes"]:
        sc_num = sc["scene"]
        sid = f"scene_{sc_num:02d}"
        img_rel = sc["visual_asset"]
        img_path = REPO_DIR / img_rel
        if not img_path.exists():
            img_path = REPO_DIR / "docs" / img_rel
        # Sanitize literal '@' from prompt text so ProseMirror relies cleanly on the attached Me avatar chip
        clean_prompt = sc["google_flow_veo_prompt"].replace("@Me", "Me")
        batches.append({
            "id": f"batch_{sid}",
            "scene_id": f"S{sc_num:02d}",
            "title": sc["title"],
            "expected": 2,
            "image_path": img_path,
            "include_me": sc.get("include_me_avatar", True),
            "narrator_pairing": sc["characters"],
            "prompt": (
                f"Generate 2 separate widescreen 16:9 photorealistic IMAX cinema video clips "
                f"(8 seconds each, Omni 1.1 Flash with slow, clear spoken audio, zero burned-in subtitle captions) "
                f"right now in batch without asking confirmation, strictly matching our attached reference image "
                f"and my attached Me Avatar (in tailored ivory-white bandhgala suit):\n\n"
                f"Clip 1 (S{sc_num:02d}_A — Action & Motion): {clean_prompt}\n\n"
                f"Clip 2 (S{sc_num:02d}_B — Spoken Dialogue Close-Up): Camera glides into a warm medium close-up "
                f"matching the exact lighting and wardrobe of Clip 1 as the speaker delivers clearly and unhurriedly: "
                f"\"{sc['dialogue_anchor']}\""
            ),
        })
    return batches


class FlowFilmRunner:
    def __init__(self):
        if websocket is None:
            raise RuntimeError("websocket-client is required (`pip install websocket-client`).")
        page_tabs = []
        active_port = None
        for port in CDP_PORTS:
            try:
                tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=3).read())
                page_tabs = [t for t in tabs if t.get("type") == "page" and "flow.google" in t.get("url", "")]
                if page_tabs:
                    active_port = port
                    break
            except Exception:
                continue
        if not page_tabs:
            raise RuntimeError(
                f"No active Google Flow browser tab found on CDP ports {CDP_PORTS}. "
                "Start Chrome with `--remote-debugging-port=9225` logged into https://flow.google.com/u/0/"
            )
        print(f"Connected to Google Flow CDP on port {active_port}: {page_tabs[0].get('url')}", flush=True)
        self.ws = websocket.create_connection(page_tabs[0]["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)
        self.mid = 1
        self.cdp("DOM.enable")
        self.cdp("Page.enable")
        self.cdp("Browser.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": str(DL_DIR),
            "eventsEnabled": True,
        })

    def cdp(self, method: str, params: dict | None = None) -> dict:
        mid = self.mid
        self.mid += 1
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                return msg

    def js(self, expr: str):
        r = self.cdp("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        return r.get("result", {}).get("result", {}).get("value")

    def mouse_click(self, x: float, y: float):
        for ev in ("mousePressed", "mouseReleased"):
            self.cdp("Input.dispatchMouseEvent", {
                "type": ev, "x": float(x), "y": float(y), "button": "left", "clickCount": 1
            })

    def open_fresh_project(self):
        self.cdp("Page.navigate", {"url": "https://flow.google.com/u/0/"})
        time.sleep(4.5)
        self.js("""(() => {
            const btns = Array.from(document.querySelectorAll('button, a, [role="button"]'));
            const nb = btns.find(b => (b.innerText || '').includes('New project')) || btns.find(b => (b.innerText || '').includes('Start Creating'));
            if (nb) nb.click();
        })()""")
        for _ in range(20):
            time.sleep(1.0)
            if self.js("Boolean(location.href.includes('/project/') && document.querySelector('div.ProseMirror'))"):
                break
        time.sleep(1.0)
        for _ in range(4):
            c = self.js("""(() => {
                const b = Array.from(document.querySelectorAll('button')).find(x => ['Get started', 'Got it', 'Next'].includes((x.innerText||'').trim()));
                if (b) { b.click(); return b.innerText.trim(); }
                return null;
            })()""")
            if not c:
                break
            time.sleep(0.5)
        print("Opened project:", self.js("location.href"), flush=True)

    def configure_16x9(self):
        self.js("""(() => {
            const t = Array.from(document.querySelectorAll('button')).find(b => (b.innerText||'').trim() === 'tune');
            if (t) t.click();
        })()""")
        time.sleep(0.8)
        never_pos = self.js("""(() => {
            const nv = Array.from(document.querySelectorAll('mat-radio-button, [role="radio"]')).find(r => (r.innerText||'').includes('Never'));
            if (!nv) return null;
            const r = nv.getBoundingClientRect();
            return {x: r.left + 20, y: r.top + r.height/2};
        })()""")
        if never_pos:
            self.mouse_click(never_pos["x"], never_pos["y"])
            time.sleep(0.3)
        self.js("""(() => {
            const btns = Array.from(document.querySelectorAll('mat-button-toggle button, button')).filter(b => (b.innerText||'').includes('16:9'));
            btns.forEach(b => b.click());
            const x1s = Array.from(document.querySelectorAll('mat-button-toggle button, button')).filter(b => (b.innerText||'').trim() === 'x1');
            x1s.forEach(b => b.click());
        })()""")
        time.sleep(0.4)
        save_pos = self.js("""(() => {
            const sb = Array.from(document.querySelectorAll('button')).find(b => (b.innerText||'').trim() === 'Save');
            if (!sb) return null;
            const r = sb.getBoundingClientRect();
            return {x: r.left + r.width/2, y: r.top + r.height/2};
        })()""")
        if save_pos:
            self.mouse_click(save_pos["x"], save_pos["y"])
            time.sleep(0.8)
        self.js("document.querySelectorAll('.cdk-overlay-backdrop').forEach(b => b.click())")
        time.sleep(0.8)
        print("Configured Agent Settings: Never, 16:9, x1", flush=True)

    def close_overlays(self):
        self.js("document.querySelectorAll('.cdk-overlay-backdrop').forEach(b => b.click())")
        time.sleep(0.6)

    def clear_ingredients(self):
        self.close_overlays()
        for _ in range(6):
            removed = self.js("""(() => {
                const btns = Array.from(document.querySelectorAll('flow-ingredient-chip button, flow-ingredient-bar button'));
                const rm = btns.find(b => (b.innerText||'').includes('cancel') || (b.getAttribute('aria-label')||'').toLowerCase().includes('remove'));
                if (rm) { rm.click(); return true; }
                return false;
            })()""")
            if not removed:
                break
            time.sleep(0.25)

    def open_plus_menu(self):
        self.close_overlays()
        add_pos = self.js("""(() => {
            const b = document.querySelector('button[aria-label="Add ingredients to the prompt box"]');
            if (!b) return null;
            const r = b.getBoundingClientRect();
            return {x: r.left + r.width/2, y: r.top + r.height/2};
        })()""")
        if add_pos:
            self.mouse_click(add_pos["x"], add_pos["y"])
            time.sleep(1.0)

    def attach_ingredients(self, image_path: Path | None, include_me: bool):
        self.clear_ingredients()
        if image_path is not None and image_path.exists():
            stem = image_path.stem
            has_card = self.js(f"""(() => {{
                const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                return btns.some(b => ((b.getAttribute('aria-label')||'') + ' ' + (b.innerText||'')).includes({json.dumps(stem)}));
            }})()""")
            if not has_card:
                self.cdp("Page.setInterceptFileChooserDialog", {"enabled": True})
                self.open_plus_menu()
                self.js("""(() => {
                    const pop = document.querySelector('.cdk-overlay-pane, .add-menu-popover-container');
                    if (!pop) return;
                    const allTab = Array.from(pop.querySelectorAll('button, [role="button"], [role="tab"]')).find(b => (b.innerText||'').includes('dashboard') || (b.innerText||'').trim() === 'All');
                    if (allTab) allTab.click();
                })()""")
                time.sleep(0.6)
                up_pos = self.js("""(() => {
                    const pop = document.querySelector('.cdk-overlay-pane, .add-menu-popover-container');
                    if (!pop) return null;
                    const up = Array.from(pop.querySelectorAll('button, [role="button"]')).find(b => (b.innerText||'').includes('Upload media'));
                    if (!up) return null;
                    const r = up.getBoundingClientRect();
                    return {x: r.left + r.width/2, y: r.top + r.height/2};
                })()""")
                if up_pos:
                    self.mouse_click(up_pos["x"], up_pos["y"])

                t0 = time.time()
                while time.time() - t0 < 6:
                    self.ws.settimeout(1.0)
                    try:
                        ev = json.loads(self.ws.recv())
                        if ev.get("method") == "Page.fileChooserOpened":
                            bnid = ev["params"]["backendNodeId"]
                            self.ws.settimeout(30.0)
                            self.cdp("DOM.setFileInputFiles", {"backendNodeId": bnid, "files": [str(image_path)]})
                            break
                    except Exception:
                        pass
                self.ws.settimeout(30.0)
                self.cdp("Page.setInterceptFileChooserDialog", {"enabled": False})

                for _ in range(25):
                    time.sleep(1.0)
                    chips_now = self.js("document.querySelectorAll('flow-ingredient-chip').length") or 0
                    busy = self.js("Boolean(document.querySelector('flow-ingredient-chip [aria-busy=\"true\"]'))")
                    now_card = self.js(f"""(() => {{
                        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                        return btns.some(b => ((b.getAttribute('aria-label')||'') + ' ' + (b.innerText||'')).includes({json.dumps(stem)}));
                    }})()""")
                    if (chips_now >= 1 and not busy) or now_card:
                        break
                time.sleep(1.2)
                self.close_overlays()

            has_img_chip = self.js("""(() => {
                return Array.from(document.querySelectorAll('flow-ingredient-chip')).some(c => !(c.innerText||'').includes('face'));
            })()""")
            if not has_img_chip:
                idx = self.js(f"""(() => {{
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
                    self.js(f"Array.from(document.querySelectorAll('button, [role=\"button\"]'))[{idx}].click()")
                    time.sleep(0.7)
                    self.js("""(() => {
                        const add = Array.from(document.querySelectorAll('[role="menuitem"]')).find(i => (i.innerText||'').includes('Add to prompt'));
                        if (add) add.click();
                    })()""")
                    time.sleep(0.8)
                    self.close_overlays()

        if include_me:
            has_me_now = self.js("""(() => {
                return Array.from(document.querySelectorAll('flow-ingredient-chip, flow-likeness-ingredient-chip')).some(c => (c.innerText||'').includes('face') || c.tagName.includes('LIKENESS'));
            })()""")
            if not has_me_now:
                self.open_plus_menu()
                self.js("""(() => {
                    const pop = document.querySelector('.cdk-overlay-pane, .add-menu-popover-container');
                    if (!pop) return;
                    const avTab = Array.from(pop.querySelectorAll('button, [role="button"], [role="tab"]')).find(b => (b.innerText||'').includes('Avatars'));
                    if (avTab) avTab.click();
                })()""")
                time.sleep(0.9)
                self.js("""(() => {
                    const pop = document.querySelector('.cdk-overlay-pane, .add-menu-popover-container');
                    if (!pop) return;
                    const btns = Array.from(pop.querySelectorAll('button, [role="button"]'));
                    for (let i = 0; i < btns.length - 1; i++) {
                        if ((btns[i].innerText || '').trim() === 'Me' && (btns[i+1].innerText || '').includes('Add to prompt')) {
                            btns[i+1].click();
                            return;
                        }
                    }
                })()""")
                time.sleep(0.8)
                self.close_overlays()

        chips = self.js("document.querySelectorAll('flow-ingredient-chip').length")
        has_me = self.js("Array.from(document.querySelectorAll('flow-ingredient-chip')).some(c => (c.innerText||'').includes('face'))")
        print(f"  Ingredients ready: ref={image_path.name if image_path else 'None'}, chips={chips}, hasMe={has_me}", flush=True)

    def get_video_cards(self) -> list[dict]:
        return self.js("""(() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
            const out = [];
            for (let i = 0; i < btns.length - 1; i++) {
                if (btns[i].getAttribute('aria-label') === 'Reuse prompt' &&
                    !(btns[i].innerText || '').includes('keyboard_return') &&
                    btns[i+1].getAttribute('aria-label') === 'More options') {
                    out.push({
                        moreIdx: i + 1,
                        label: btns[i+2] ? (btns[i+2].getAttribute('aria-label') || btns[i+2].innerText || '') : ''
                    });
                }
            }
            return out;
        })()""") or []

    def submit_prompt(self, text: str):
        self.js(f"""(() => {{
            const el = document.querySelector('div.ProseMirror');
            el.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
            document.execCommand('insertText', false, {json.dumps(text.strip())});
        }})()""")
        time.sleep(0.4)
        self.cdp("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
        self.cdp("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
        time.sleep(0.6)

    def run_sub_batch(self, batch_dir: Path, prefix: str, image_path: Path | None, include_me: bool, prompt_text: str, expected_count: int):
        batch_dir.mkdir(parents=True, exist_ok=True)
        existing = sorted(batch_dir.glob(f"{prefix}_*.mp4"))
        if len(existing) >= expected_count:
            print(f"Skipping '{prefix}' — already has {len(existing)}/{expected_count} clips.", flush=True)
            return existing

        self.open_fresh_project()
        self.configure_16x9()
        self.attach_ingredients(image_path, include_me)
        before_len = len(self.get_video_cards())
        self.submit_prompt(prompt_text)
        print(f"Submitted '{prefix}' ({expected_count} widescreen 16:9 clips)...", flush=True)

        replied_go = False
        retried_timeout = 0
        t0 = time.time()
        while time.time() - t0 < 480:
            time.sleep(6)
            elapsed = int(time.time() - t0)
            tail = self.js(r"document.body.innerText.slice(-900).replace(/\s+/g, ' ')") or ""
            if retried_timeout < 2 and ("The agent timed out" in tail or "Try again" in tail):
                clicked_retry = self.js("""(() => {
                    const b = Array.from(document.querySelectorAll('button')).find(x => (x.innerText||'').trim() === 'Try again');
                    if (b) { b.click(); return true; }
                    return false;
                })()""")
                if clicked_retry:
                    retried_timeout += 1
                    print(f"    [{elapsed:3d}s] Flow transient timeout — clicked 'Try again' ({retried_timeout}/2)...", flush=True)
                    time.sleep(4)
                    continue

            ask_triggers = (
                "Option B", "How would you like to proceed", "Would you like me to",
                "shall I proceed", "confirm before", "ready for me to generate", "Let me know if"
            )
            if not replied_go and any(k.lower() in tail.lower() for k in ask_triggers) and len(self.get_video_cards()) == before_len:
                replied_go = True
                print(f"    [{elapsed:3d}s] Flow asked confirmation — sending immediate batch go-ahead...", flush=True)
                self.attach_ingredients(image_path, include_me)
                self.submit_prompt(f"Proceed immediately—generate all {expected_count} widescreen 16:9 video clips right now in batch without asking any questions!")
                continue

            cards_now = self.get_video_cards()
            new_cnt = len(cards_now) - before_len
            is_running = ("\nstop\n" in (self.js("document.body.innerText.toLowerCase()") or "")) or ("generating" in tail.lower())
            if elapsed % 18 == 0 or new_cnt >= expected_count:
                print(f"    [{elapsed:3d}s] {prefix}: newCards={new_cnt}/{expected_count} running={is_running}", flush=True)
            if new_cnt >= expected_count:
                time.sleep(3.0)
                break
            if new_cnt > 0 and not is_running and elapsed > 75:
                time.sleep(8.0)
                cards_recheck = len(self.get_video_cards()) - before_len
                still_running = "\nstop\n" in (self.js("document.body.innerText.toLowerCase()") or "")
                if cards_recheck == new_cnt and not still_running:
                    print(f"    [{elapsed+8:3d}s] {prefix}: generation settled with {new_cnt}/{expected_count} clips.", flush=True)
                    break

        cards_final = self.get_video_cards()
        new_cnt = max(0, len(cards_final) - before_len)
        saved = []
        for idx in range(new_cnt):
            c = self.get_video_cards()[idx]
            dest = batch_dir / f"{prefix}_{idx+1:02d}.mp4"
            before_mp4s = set(DL_DIR.glob("*.mp4"))
            self.js(f"Array.from(document.querySelectorAll('button, [role=\"button\"]'))[{c['moreIdx']}].click()")
            time.sleep(0.7)
            self.js("""(() => {
                const dl = Array.from(document.querySelectorAll('[role="menuitem"]')).find(i => (i.innerText||'').toLowerCase().includes('download'));
                if (dl) dl.click();
            })()""")
            time.sleep(0.7)
            self.js("""(() => {
                const orig = Array.from(document.querySelectorAll('[role="menuitem"]')).find(i => (i.innerText||'').includes('720p') || (i.innerText||'').toLowerCase().includes('original'));
                if (orig) orig.click();
            })()""")
            for _ in range(22):
                time.sleep(0.6)
                crs = list(DL_DIR.glob("*.crdownload"))
                diff = [f for f in (set(DL_DIR.glob("*.mp4")) - before_mp4s) if f.stat().st_size > 200_000]
                if diff and not crs:
                    newest = sorted(diff, key=lambda p: p.stat().st_mtime, reverse=True)[0]
                    shutil.copy2(newest, dest)
                    saved.append({"file": dest.name, "label": c["label"], "size_mb": round(dest.stat().st_size / 1e6, 2)})
                    print(f"    Saved {dest.name} ({dest.stat().st_size/1e6:.2f} MB) <- {c['label']}", flush=True)
                    break
            self.js("document.body.click()")
            time.sleep(0.3)

        (batch_dir / f"{prefix}_manifest.json").write_text(json.dumps(saved, indent=2), encoding="utf-8")
        return saved

    def close(self):
        self.ws.close()


def main():
    only_filter = sys.argv[1] if len(sys.argv) > 1 else None
    batches = load_storyboard_batches()
    print(f"Loaded {len(batches)} Google Flow batches from {STORYBOARD_JSON.name}", flush=True)
    runner = FlowFilmRunner()
    try:
        for b in batches:
            bid = b["id"]
            if only_filter and only_filter.lower() not in bid.lower():
                continue
            bdir = EP_CLIPS_DIR / bid
            print(f"\n=== [{b['scene_id']}] {b['title']} | Pairing: {b['narrator_pairing']} ===", flush=True)
            runner.run_sub_batch(bdir, bid, b["image_path"], b["include_me"], b["prompt"], b["expected"])
        print("\nALL 12 S01E01 'THE WAY FORWARD' GOOGLE FLOW BATCHES GENERATED & DOWNLOADED!", flush=True)
    finally:
        runner.close()


if __name__ == "__main__":
    main()
