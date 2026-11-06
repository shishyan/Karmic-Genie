#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harvests s01e01_act1_dormant_stage_16x9.jpg and generates s01e01_act2_saintly_genie_16x9.jpg
using the verified 'More options -> Add to prompt' + 'Enter key' submission flow.
"""

import json
import shutil
import time
import urllib.request
from pathlib import Path
import websocket

CDP_PORT = 9225
REPO_MASTERS_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show/assets/studio_v5_masters")
ARTIFACT_DIR = Path("/home/shishyan/.gemini/antigravity/brain/b55fc9ea-1a2e-45b9-8d71-a53ee11caf0c")
DL_DIR = Path.home() / "Downloads"


class FlowMasterHarvester:
    def __init__(self):
        tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/list", timeout=5).read())
        page_tabs = [t for t in tabs if t.get("type") == "page" and "flow.google" in t.get("url", "")]
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

    def get_generated_cards(self) -> list[dict]:
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

    def clear_ingredients(self):
        for _ in range(5):
            removed = self.js("""(() => {
                const btns = Array.from(document.querySelectorAll('flow-ingredient-chip button, flow-ingredient-bar button'));
                const rm = btns.find(b => (b.innerText||'').includes('cancel') || (b.getAttribute('aria-label')||'').toLowerCase().includes('remove'));
                if (rm) { rm.click(); return true; }
                return false;
            })()""")
            if not removed:
                break
            time.sleep(0.25)

    def attach_card_by_name(self, name_substr: str):
        self.clear_ingredients()
        idx = self.js(f"""(() => {{
            const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
            for (let i = 1; i < btns.length; i++) {{
                const lbl = (btns[i].getAttribute('aria-label')||'') + ' ' + (btns[i].innerText||'');
                if (lbl.includes({json.dumps(name_substr)})) {{
                    for (let j = i - 1; j >= Math.max(0, i - 3); j--) {{
                        if (btns[j].getAttribute('aria-label') === 'More options') return j;
                    }}
                }}
            }}
            return -1;
        }})()""")
        if idx >= 0:
            self.js(f"Array.from(document.querySelectorAll('button, [role=\"button\"]'))[{idx}].click()")
            time.sleep(0.7)
            self.js("Array.from(document.querySelectorAll('[role=\"menuitem\"]')).find(i => (i.innerText||'').includes('Add to prompt')).click()")
            time.sleep(0.8)
        print("  Attached chip count:", self.js("document.querySelectorAll('flow-ingredient-chip').length"), flush=True)

    def submit_enter(self, text: str):
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

    def download_top_image(self, out_name: str):
        c0 = self.get_generated_cards()[0]
        before_files = set(DL_DIR.glob("*"))
        self.js(f"Array.from(document.querySelectorAll('button, [role=\"button\"]'))[{c0['moreIdx']}].click()")
        time.sleep(0.7)
        self.js("""(() => {
            const dl = Array.from(document.querySelectorAll('[role="menuitem"]')).find(i => (i.innerText||'').toLowerCase().includes('download'));
            if (dl) dl.click();
        })()""")
        time.sleep(0.7)
        self.js("""(() => {
            const items = Array.from(document.querySelectorAll('[role="menuitem"]'));
            const orig = items.find(i => (i.innerText||'').includes('2K')) || items.find(i => (i.innerText||'').includes('1K')) || items.find(i => (i.innerText||'').toLowerCase().includes('original'));
            if (orig) orig.click();
        })()""")
        for _ in range(25):
            time.sleep(0.5)
            crs = list(DL_DIR.glob("*.crdownload"))
            diff = [f for f in (set(DL_DIR.glob("*")) - before_files) if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp") and f.stat().st_size > 80_000]
            if diff and not crs:
                newest = sorted(diff, key=lambda p: p.stat().st_mtime, reverse=True)[0]
                dest = REPO_MASTERS_DIR / out_name
                shutil.copy2(newest, dest)
                shutil.copy2(newest, ARTIFACT_DIR / out_name)
                print(f"  ✅ Saved {out_name} ({dest.stat().st_size/1e3:.0f} KB) <- {c0['label']}", flush=True)
                break
        self.js("document.body.click()")
        time.sleep(0.4)

    def close(self):
        self.ws.close()


def main():
    h = FlowMasterHarvester()
    try:
        # 1. Wait for dormant stage card that is currently generating (or ready!)
        for _ in range(30):
            cards = h.get_generated_cards()
            if len(cards) >= 1:
                time.sleep(1.5)
                break
            tail = h.js("document.body.innerText.slice(-500)") or ""
            if "Would you like" in tail or "proceed" in tail.lower():
                h.attach_card_by_name("v5_subtle_7d_stadium_16x9")
                h.submit_enter("Proceed immediately—generate the single 16:9 image right now without asking questions!")
            time.sleep(3.0)

        h.download_top_image("s01e01_act1_dormant_stage_16x9.jpg")

        # 2. Generate s01e01_act2_saintly_genie_16x9.jpg
        before_cnt = len(h.get_generated_cards())
        h.attach_card_by_name("v5_subtle_7d_stadium_16x9")
        prompt_saintly = (
            "Generate 1 photorealistic 2K widescreen 16:9 image right now without asking questions by editing this attached studio image: "
            "Keep 100% of the exact same Karmic Genie Show stadium-studio architecture, pure-white circular marble floor, mild dark violet-magenta vault ceiling, "
            "elevated blue-seat stadium audience, Marcus in the left chair, the bearded Host in the ivory-white bandhgala suit on the right chair, "
            "and the subtle brushed-gold side-wall inscriptions (`Do Your DUTY. Practice DHARMA. Remember the DIVINE. Live by DISCIPLINE.` on the left wall and `Keep Your DIGNITY. Be DEVOUT. Respect DESTINY.` on the right wall). "
            "Refine two details cleanly: "
            "1) Give the floating cross-legged Celestial Karmic Genie above the center jeweled lamp an ultra-peaceful, humble, compassionate wise-saint expression with palms gently joined in a polite namaste greeting, glowing softly in warm gold, emerald, sapphire, and soft magenta light. "
            "2) Fix the text on the curved waist-high glass barriers so the left barrier cleanly reads `$720B+ AI CAPEX  |  NON-AI TEAMS` and the right barrier cleanly reads `THE 7D WAY  |  OPEN REFLECTIONS` (zero typos)."
        )
        h.submit_enter(prompt_saintly)
        print("  Submitted s01e01_act2_saintly_genie_16x9.jpg...", flush=True)

        for _ in range(35):
            time.sleep(3.0)
            if len(h.get_generated_cards()) > before_cnt:
                time.sleep(1.5)
                break
        h.download_top_image("s01e01_act2_saintly_genie_16x9.jpg")
    finally:
        h.close()


if __name__ == "__main__":
    main()
