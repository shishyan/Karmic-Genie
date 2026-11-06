#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Flow ULTRA (Omni 1.1 Flash, 16:9 Widescreen) Cinematography Generator for
Karmic Genie Show — S01E01 v3.1 Interactive Master:
  "200,000 Cuts, 60,000 Buyouts & Why Every One Is a Blessing in Disguise"

Key guarantees:
  - Strictly ZERO company names and ZERO real/fictional person names!
  - Zero literal `@` symbols in ProseMirror text (prevents @mention popup swallowing chars).
  - Exact dual-chip verification: Stage Image chip (`add\\nface`) + Me Avatar chip (`cancel\\nface`) => 2 chips!
  - Single-person camera A / camera B interview reverse-shots across the dormant gold lamp (zero multi-face Likeness rejections).
"""

import json
import shutil
import sys
import time
import urllib.request
from pathlib import Path
import websocket

CDP_PORT = 9225
REPO_DIR = Path("/home/shishyan/GitHub/Karmic-Genie-Show")
MASTERS_DIR = REPO_DIR / "assets" / "studio_v5_masters"
CLIPS_DIR = REPO_DIR / "episodes" / "S01E01_Employees_vs_Tech_CEO" / "flow_v3_interactive_clips"
DL_DIR = Path.home() / "Downloads"

DORMANT_IMG = MASTERS_DIR / "v6_7d_dormant_stage_16x9.jpg"
SAINTLY_IMG = MASTERS_DIR / "v6_7d_saintly_genie_16x9.jpg"

STAGE_DESC = (
    "pure-white circular marble stage, mild dark violet-magenta vault ceiling, curved transparent "
    "OLED glass barriers separating the elevated blue-seat stadium audience, dormant gold Genie lamp "
    "on the center glass table, NO floating genie, centered `Karmic Genie Show` logo with generous "
    "clean white padding on both sides, flanked by subtle brushed-gold wall inscriptions "
    "`Respect Your DUTY First. / Earn with DIGNITY Always. / Practice Life DISCIPLINE.` on the left, "
    "`Uphold Karmic DHARMA. / Raise Family with DEVOTION. / Be Grateful to Your DIVINE.` on the right, "
    "and `Purposeful Life Is Your DESTINY.` centered below"
)

BATCHES = [
    {
        "id": "v3_b1_welcome",
        "expected": 3,  # W01, W02, W03 already verified & downloaded! W04 moved to v3_b2_interview_host.
        "img": DORMANT_IMG,
        "include_me": True,
        "prompt": "",
    },
    {
        "id": "v3_b2_interview_host",
        "expected": 4,
        "img": DORMANT_IMG,
        "include_me": True,
        "prompt": f"""Generate 4 separate widescreen 16:9 photorealistic broadcast interview video clips (8 seconds each, Omni 1.1 Flash with crisp conversational spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, matching our attached Karmic Genie Show studio image ({STAGE_DESC}) and featuring the male host matching my attached avatar in his tailored ivory-white bandhgala suit on camera:

1) W04_Introduce_CEO: Medium shot of the host in his ivory-white bandhgala suit gesturing warmly toward the guest chair beside the dormant gold Genie lamp on the pure-white stage, speaking respectfully: "Profits are booming, yet thousands received buyout offers. Welcome tonight—thank you for speaking openly."

2) I01_Host_Why_Buyouts: Medium close-up of the host seated in the pure-white sculptural chair leaning forward across the dormant gold Genie lamp, asking candidly: "Profits are near records—why offer sixty thousand buyouts while banks and shipping cut thousands?"

3) I03_Host_Seven_Layers: Engaging medium close-up of the host gesturing thoughtfully across the center lamp table during the live interview, asking sharply: "Why target managers seven layers down, workers in their fifties, and thirty thousand roles in India?"

4) I05_Host_Open_Floor: Medium tracking shot as the host rises warmly from his white chair on the pure-white stage before the brushed-gold 7D wall, smiling welcomingly: "Let's bring our studio and home viewers right in—hear the questions keeping families awake."
""",
    },
    {
        "id": "v3_b3_interview_ceo",
        "expected": 5,
        "img": DORMANT_IMG,
        "include_me": False,
        "prompt": f"""Generate 5 separate widescreen 16:9 photorealistic broadcast interview video clips (8 seconds each, Omni 1.1 Flash with candid, articulate spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, matching our attached Karmic Genie Show studio image ({STAGE_DESC}) featuring a distinguished 52-year-old silver-templed Chief Executive in a dark navy suit seated in the dark sculptural chair beside the dormant gold Genie lamp on the pure-white stage:

1) I02_CEO_Cashflow_Flip: Medium close-up of the 52-year-old Chief Executive leaning forward candidly in the dark sculptural chair beside the dormant gold Genie lamp, speaking directly in an interview: "Fifty billion a quarter on AI infrastructure drained cash flow—boards are funding machines from payroll."

2) I02B_CEO_Voluntary_Exit: Over-the-shoulder interview shot onto the 52-year-old Chief Executive on the pure-white stage before the brushed-gold 7D wall, explaining openly: "Voluntary buyouts paying up to twelve months trim non-AI corporate and support teams without lockouts."

3) I04_CEO_2027_Mandates: Close-up of the 52-year-old Chief Executive speaking honestly across the glass lamp table: "AI replaced status layers and back-offices. Declining a buyout brings hub relocations and tighter quotas."

4) S03_CEO_Human_Reaction: Empathetic studio shot as the 52-year-old Chief Executive turns toward the elevated blue stadium audience rows nodding with genuine humility, speaking sincerely: "Spreadsheets call it optimization—we never measure missed years with aging parents or decades of pride."

5) H06_CEO_Final_Takeaway: Warm closing close-up of the 52-year-old Chief Executive smiling thoughtfully in the dark studio chair beside the dormant gold lamp, speaking from the heart: "A company is a contract, never family. People deserve generous runway so their next chapter thrives."
""",
    },
    {
        "id": "v3_b4_audience_and_callin",
        "expected": 5,
        "img": None,
        "include_me": False,
        "prompt": """Generate 5 separate widescreen 16:9 photorealistic broadcast & documentary video clips (8 seconds each, Omni 1.1 Flash with authentic emotional spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation:

1) S01A_Expat_Mic: Medium shot in Row Two of an elevated blue-seat modern talk-show stadium behind a curved glass barrier; a 38-year-old Indian engineer stands holding a wireless microphone, speaking earnestly: "Twelve years chasing dollars and visas abroad, my father grew old through a phone screen."

2) S01B_Expat_Question: Intimate close-up of the same 38-year-old Indian engineer in the blue stadium row as audience members nod empathetically around him, asking honestly: "Why did opening this buyout feel like relief—even if peers call going home failing?"

3) S02_Veteran_54_Mic: Dignified medium shot in the front blue stadium row as a 54-year-old silver-templed enterprise architect in a blazer stands with a wireless mic, asking calmly: "At fifty-four after thirty years—do I beg young recruiters, or take twelve months' pay with dignity?"

4) S04A_Mum_CallIn: Authentic live home video-call shot of a warm 42-year-old British woman sitting in her cozy rainy-day UK kitchen speaking directly into her laptop camera: "When AI flattened seven manager layers, I panicked—without my big title, who am I?"

5) S04B_Mum_Daylight_Walk: Warm candid afternoon documentary shot on a leafy UK sidewalk after rain as the 42-year-old mother walks hand-in-hand in daylight with her smiling nine-year-old son carrying his school backpack; her gentle voiceover says: "Walking home from school in daylight, my nine-year-old asked: 'Mum, did we get you back?'"
""",
    },
    {
        "id": "v3_b5_crisp_genie",
        "expected": 2,
        "img": SAINTLY_IMG,
        "include_me": False,
        "prompt": """Generate 2 separate widescreen 16:9 photorealistic broadcast-cinema video clips (8 seconds each, Omni 1.1 Flash with warm, gentle, peaceful saintly spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, strictly matching our attached Karmic Genie Show pure-white circular marble studio image where the luminous Celestial Karmic Genie floats SEATED IN CROSS-LEGGED LOTUS POSTURE above the jeweled gold lamp in front of the padded `Karmic Genie Show` logo and subtle brushed-gold 7D wall maxims (`Respect Your DUTY First. / Earn with DIGNITY Always. / Practice Life DISCIPLINE.` on the left, `Uphold Karmic DHARMA. / Raise Family with DEVOTION. / Be Grateful to Your DIVINE.` on the right, and `Purposeful Life Is Your DESTINY.` centered below). STRICT RULE: Keep the Genie strictly CROSS-LEGGED and speaking warmly, gently, and clearly:

1) G01_Genie_Thunderclap_Greeting: Symmetrical studio shot as the floating cross-legged Celestial Karmic Genie smiles warmly like a dear friend and bows gently in namaste, speaking softly and clearly: "Namaste, dear friends. Like the two-minute Single Thunderclap story to read quietly at home tonight..."

2) G02_Genie_Blessing_Truth: Luminous close-medium shot of the serene cross-legged Karmic Genie opening his palms with a reassuring, joyful smile above the gold lamp, speaking warmly and clearly: "The buyout, the flattened title, the closed floor—every single one is a blessing in disguise!"
""",
    },
    {
        "id": "v3_b6a_host_dispatch",
        "expected": 4,
        "img": DORMANT_IMG,
        "include_me": True,
        "prompt": f"""Generate 4 separate widescreen 16:9 photorealistic broadcast talk-show video clips (8 seconds each, Omni 1.1 Flash with warm, engaging spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, matching our attached Karmic Genie Show studio image ({STAGE_DESC}) and featuring the male host matching my attached avatar in his tailored ivory-white bandhgala suit:

1) N01_Host_India_Dispatch: Medium tracking shot as the host walks across the pure-white circular marble stage addressing the camera warmly: "Across India's tech hubs, one team lead escaped metro rent—building peacefully beside her parents."

2) N02_Host_Tokyo_Grad: Medium shot as the host gestures thoughtfully beside the dormant gold Genie lamp on the pure-white stage, speaking briskly: "Midnight survivors carry four empty desks, while young grads ask: why not build directly ourselves?"

3) N03_Host_Summon_Genie: Symmetrical center-stage widescreen shot of the host standing poised beside the dormant gold Genie lamp before the padded `Karmic Genie Show` wall logo and brushed-gold 7D maxims: "Let's quiet the room and ask together: What does Genie say — the 7D way?"

4) H01_Host_Why_Lighter: Energetic medium shot as the host smiles brightly on the pure-white stage before the brushed-gold 7D wall, speaking with infectious clarity: "Every single one is a blessing in disguise! Why? Nobody unlocks golden handcuffs on their own!"
""",
    },
    {
        "id": "v3_b6b_host_expand_7d",
        "expected": 5,
        "img": DORMANT_IMG,
        "include_me": True,
        "prompt": f"""Generate 5 separate widescreen 16:9 photorealistic broadcast talk-show video clips (8 seconds each, Omni 1.1 Flash with warm, inspiring conversational spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, matching our attached Karmic Genie Show studio image ({STAGE_DESC}) and featuring the male host matching my attached avatar in his tailored ivory-white bandhgala suit:

1) H02_Host_Expat_Home: Close-medium shot of the host speaking passionately straight into the camera lens like a trusted friend on the pure-white stage: "Millions abroad postpone duty to aging parents—twelve months' buyout pay brings you home guilt-free!"

2) H03_Host_50s_Dignity: Wide-medium shot as the host gestures warmly toward the brushed-gold 7D maxims on the pure-white stage wall behind him, speaking encouragingly: "In your fifties with a buyout? Lead with Dignity—consult and own your clock in health!"

3) H04_Host_Managers_Grads: Medium tracking shot as the host walks engagingly past the curved glass barrier on the pure-white stage, smiling warmly: "Flattened managers shed a mask—and disciplined young grads can build with AI from day one!"

4) H05_Host_Ask_CEO: Medium close-up of the host turning warmly toward the guest chair beside the dormant gold lamp on the pure-white stage, asking sincerely: "Before we close tonight—hearing this circle, what stays with you most?"

5) H07_Host_Interactive_Signoff: Iconic warm close-up of the host on the pure-white stage before the padded `Karmic Genie Show` emblem, smiling directly at viewers watching at home: "Comment your blessing in disguise, hug your family tonight—What does Genie say, the 7D way?"
""",
    },
]


class FlowV3Runner:
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

    def mouse_click(self, x: float, y: float):
        for ev in ("mousePressed", "mouseReleased"):
            self.cdp("Input.dispatchMouseEvent", {
                "type": ev, "x": float(x), "y": float(y), "button": "left", "clickCount": 1
            })

    def close_menus(self):
        self.js("""(() => {
            document.querySelectorAll('.cdk-overlay-backdrop').forEach(b => b.click());
            const dis = Array.from(document.querySelectorAll('button')).find(x => (x.innerText||'').trim() === 'Dismiss');
            if (dis) dis.click();
        })()""")
        time.sleep(0.5)

    def open_fresh_project(self):
        self.cdp("Page.navigate", {"url": "https://flow.google.com/u/0/"})
        time.sleep(4.5)
        self.js("""(() => {
            const btns = Array.from(document.querySelectorAll('button, a, [role="button"]'));
            const nb = btns.find(b => (b.innerText || '').includes('New project')) || btns.find(b => (b.innerText || '').includes('Start Creating'));
            if (nb) nb.click();
        })()""")
        for _ in range(22):
            time.sleep(1.0)
            if self.js("Boolean(location.href.includes('/project/') && document.querySelector('div.ProseMirror'))"):
                break
        time.sleep(1.2)
        for _ in range(3):
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
        time.sleep(0.9)
        never_pos = self.js("""(() => {
            const nv = Array.from(document.querySelectorAll('mat-radio-button, [role="radio"]')).find(r => (r.innerText||'').includes('Never'));
            if (!nv) return null;
            const r = nv.getBoundingClientRect();
            return {x: r.left + 20, y: r.top + r.height/2};
        })()""")
        if never_pos:
            self.mouse_click(never_pos["x"], never_pos["y"])
            time.sleep(0.35)
        self.js("""(() => {
            Array.from(document.querySelectorAll('mat-button-toggle button, button')).filter(b => (b.innerText||'').includes('16:9')).forEach(b => b.click());
            Array.from(document.querySelectorAll('mat-button-toggle button, button')).filter(b => (b.innerText||'').trim() === 'x1').forEach(b => b.click());
        })()""")
        time.sleep(0.45)
        save_pos = self.js("""(() => {
            const sb = Array.from(document.querySelectorAll('button')).find(b => (b.innerText||'').trim() === 'Save');
            if (!sb) return null;
            const r = sb.getBoundingClientRect();
            return {x: r.left + r.width/2, y: r.top + r.height/2};
        })()""")
        if save_pos:
            self.mouse_click(save_pos["x"], save_pos["y"])
            time.sleep(0.8)
        self.close_menus()

    def open_plus_menu(self):
        self.close_menus()
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
        self.close_menus()

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

                # Wait until uploaded image chip appears (`add\nface`) OR card finishes uploading
                for _ in range(25):
                    time.sleep(1.0)
                    has_img_chip = self.js("Array.from(document.querySelectorAll('flow-ingredient-chip')).some(c => (c.innerText||'').includes('add'))")
                    if has_img_chip:
                        break
                time.sleep(1.0)
                self.close_menus()

            # Ensure image chip (`add\nface`) is attached in prompt box!
            has_img_chip = self.js("Array.from(document.querySelectorAll('flow-ingredient-chip')).some(c => (c.innerText||'').includes('add'))")
            if not has_img_chip:
                self.js(f"""(() => {{
                    const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                    for (let i = 1; i < btns.length; i++) {{
                        const lbl = (btns[i].getAttribute('aria-label')||'') + ' ' + (btns[i].innerText||'');
                        if (lbl.includes({json.dumps(stem)})) {{
                            for (let j = i - 1; j >= Math.max(0, i - 3); j--) {{
                                if (btns[j].getAttribute('aria-label') === 'More options') {{ btns[j].click(); return; }}
                            }}
                        }}
                    }}
                }})()""")
                time.sleep(0.8)
                self.js("""(() => {
                    const add = Array.from(document.querySelectorAll('.cdk-overlay-pane button, [role="menuitem"]'))
                        .find(i => (i.innerText||'').includes('Add to prompt'));
                    if (add) add.click();
                })()""")
                time.sleep(0.8)
                self.close_menus()

        if include_me:
            # Me Avatar chip specifically has `cancel\nface`!
            has_me_now = self.js("Array.from(document.querySelectorAll('flow-ingredient-chip')).some(c => (c.innerText||'').includes('cancel'))")
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
                self.close_menus()

        chips = self.js("document.querySelectorAll('flow-ingredient-chip').length")
        has_img = self.js("Array.from(document.querySelectorAll('flow-ingredient-chip')).some(c => (c.innerText||'').includes('add'))")
        has_me = self.js("Array.from(document.querySelectorAll('flow-ingredient-chip')).some(c => (c.innerText||'').includes('cancel'))")
        print(f"  Ingredients ready: img={image_path.name if image_path else 'None'}, chips={chips} (hasImg={has_img}, hasMe={has_me})", flush=True)

    def get_video_cards(self) -> list[dict]:
        return self.js("""(() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
            const out = [];
            for (let i = 0; i < btns.length - 1; i++) {
                if (btns[i].getAttribute('aria-label') === 'Reuse prompt' &&
                    !(btns[i].innerText || '').includes('keyboard_return') &&
                    !(btns[i].innerText || '').includes('undo') &&
                    btns[i+1].getAttribute('aria-label') === 'More options') {
                    out.push({
                        moreIdx: i + 1,
                        label: btns[i+2] ? (btns[i+2].getAttribute('aria-label') || btns[i+2].innerText || '') : ''
                    });
                }
            }
            return out;
        })()""") or []

    def submit_human_paced(self, text: str):
        self.close_menus()
        pm_pos = self.js("""(() => {
            const el = document.querySelector('div.ProseMirror');
            if (!el) return null;
            const r = el.getBoundingClientRect();
            return {x: r.left + 48, y: r.top + 18};
        })()""")
        if pm_pos:
            self.mouse_click(pm_pos["x"], pm_pos["y"])
            time.sleep(0.35)

        self.js("""(() => {
            const el = document.querySelector('div.ProseMirror');
            if (el) {
                el.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);
            }
        })()""")
        time.sleep(0.25)

        clean_txt = text.replace("@", "").strip()
        chunk_sz = 120
        for i in range(0, len(clean_txt), chunk_sz):
            self.cdp("Input.insertText", {"text": clean_txt[i:i + chunk_sz]})
            time.sleep(0.05)

        time.sleep(0.75)
        self.cdp("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
        self.cdp("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
        time.sleep(1.2)

        rem = len((self.js("document.querySelector('div.ProseMirror')?.innerText || ''") or "").strip())
        if rem > 15:
            sub_pos = self.js("""(() => {
                const sub = document.querySelector('button[aria-label="Start generation"]');
                if (!sub) return null;
                const rc = sub.getBoundingClientRect();
                return {x: rc.left + rc.width/2, y: rc.top + rc.height/2};
            })()""")
            if sub_pos:
                self.mouse_click(sub_pos["x"], sub_pos["y"])
                time.sleep(1.0)

    def download_cards(self, out_dir: Path, prefix: str, count: int) -> list[dict]:
        out_dir.mkdir(parents=True, exist_ok=True)
        saved = []
        for idx in range(count):
            self.close_menus()
            cards = self.get_video_cards()
            if idx >= len(cards):
                break
            c = cards[idx]
            dest = out_dir / f"{prefix}_{idx+1:02d}.mp4"
            before_mp4s = set(DL_DIR.glob("*.mp4"))
            self.js(f"""(() => {{
                const b = Array.from(document.querySelectorAll('button, [role="button"]'))[{c['moreIdx']}];
                if (b) {{ b.scrollIntoView({{block: 'center'}}); b.click(); }}
            }})()""")
            time.sleep(0.85)
            self.js("""(() => {
                const dl = Array.from(document.querySelectorAll('.cdk-overlay-pane button, [role="menuitem"]'))
                    .find(i => (i.innerText||'').toLowerCase().includes('download'));
                if (dl) dl.click();
            })()""")
            time.sleep(0.85)
            self.js("""(() => {
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
            self.close_menus()
        (out_dir / f"{prefix}_manifest.json").write_text(json.dumps(saved, indent=2), encoding="utf-8")
        return saved

    def run_batch(self, b: dict):
        bid = b["id"]
        exp = b["expected"]
        bdir = CLIPS_DIR / bid
        existing = sorted(bdir.glob(f"{bid}_*.mp4"))
        if len(existing) >= exp:
            print(f"⏭️  Skipping {bid} — already has {len(existing)}/{exp} clips.", flush=True)
            return

        self.open_fresh_project()
        self.configure_16x9()
        self.attach_ingredients(b["img"], b["include_me"])
        before_len = len(self.get_video_cards())
        self.submit_human_paced(b["prompt"])
        print(f"🎬 Submitted '{bid}' ({exp} clips)...", flush=True)

        replied_go = False
        retried_try = 0
        t0 = time.time()
        while time.time() - t0 < 420:
            time.sleep(6)
            elapsed = int(time.time() - t0)
            tail = self.js(r"document.body.innerText.slice(-1100).replace(/\s+/g, ' ')") or ""

            if retried_try < 1 and ("Try again" in tail or "timed out" in tail):
                time.sleep(5.0)
                clicked = self.js("""(() => {
                    const b = Array.from(document.querySelectorAll('button')).find(x => (x.innerText||'').trim() === 'Try again');
                    if (b) { b.click(); return true; }
                    return false;
                })()""")
                if clicked:
                    retried_try += 1
                    print(f"    [{elapsed:3d}s] Clicked 'Try again' ({retried_try}/1)...", flush=True)
                    time.sleep(5.0)
                    continue

            ask_triggers = ("Option B", "How would you like to proceed", "Would you like me to", "shall I proceed", "confirm before", "Let me know if")
            if not replied_go and any(k.lower() in tail.lower() for k in ask_triggers) and len(self.get_video_cards()) == before_len:
                replied_go = True
                print(f"    [{elapsed:3d}s] Flow asked confirmation — sending go-ahead...", flush=True)
                self.attach_ingredients(b["img"], b["include_me"])
                self.submit_human_paced(f"Proceed immediately—generate all {exp} widescreen 16:9 video clips right now in batch without asking any questions!")
                continue

            new_cnt = len(self.get_video_cards()) - before_len
            low_body = (self.js("document.body.innerText.toLowerCase()") or "")
            is_running = ("\nstop\n" in low_body) or ("generating" in tail.lower()) or ("waiting in the queue" in tail.lower() and elapsed < 150)
            if elapsed % 18 == 0 or new_cnt >= exp:
                print(f"    [{elapsed:3d}s] {bid}: newCards={new_cnt}/{exp} running={is_running}", flush=True)
            if new_cnt >= exp:
                time.sleep(3.0)
                break
            if new_cnt > 0 and not is_running and elapsed > 95:
                time.sleep(10.0)
                if (len(self.get_video_cards()) - before_len) == new_cnt:
                    print(f"    [{elapsed+10:3d}s] {bid}: settled with {new_cnt}/{exp} clips.", flush=True)
                    break

        total_new = max(0, len(self.get_video_cards()) - before_len)
        self.download_cards(bdir, bid, total_new)
        time.sleep(8.0)

    def close(self):
        self.ws.close()


def main():
    filt = sys.argv[1] if len(sys.argv) > 1 else None
    runner = FlowV3Runner()
    try:
        for b in BATCHES:
            if filt and filt not in b["id"]:
                continue
            runner.run_batch(b)
        print("\n🏆 ALL V3.1 INTERACTIVE S01E01 BATCHES COMPLETED!", flush=True)
    finally:
        runner.close()


if __name__ == "__main__":
    main()
