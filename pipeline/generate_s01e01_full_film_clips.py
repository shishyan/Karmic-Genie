#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resumable Google Flow ULTRA (Omni 1.1 Flash, 16:9 Widescreen) Batch Cinematography Generator
for Karmic Genie Show — Season 1, Episode 1 (~7:15 Full Film):
  "Seven Chairs Around One Fire: Non-AI Teams, Hyperscaler Billions & The 2030 Clock"

Key guarantees:
  - Every speaking clip contains ONLY 14–18 words so Omni 1.1 Flash delivers unhurried,
    calm, natural movie dialogue right from generation (zero rushing!).
  - Karmic Genie clips explicitly specify an ultra-peaceful, soft-spoken, polite, humble
    wise-saint voice and cross-legged posture.
  - Real-life affected households across San Francisco, Mysuru/Seattle, London, São Paulo,
    Tokyo, Munich, and Coimbatore are filmed with cinematic documentary warmth.
  - Resumable per-batch so any single batch can be re-run or resumed cleanly.
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
EP_CLIPS_DIR = REPO_DIR / "episodes" / "S01E01_Employees_vs_Tech_CEO" / "flow_16x9_clips"
DL_DIR = Path.home() / "Downloads"

DORMANT_IMG = MASTERS_DIR / "v6_7d_dormant_stage_16x9.jpg"
SAINTLY_IMG = MASTERS_DIR / "v6_7d_saintly_genie_16x9.jpg"
FALLBACK_V5_IMG = MASTERS_DIR / "v6_7d_dormant_stage_16x9.jpg"


BATCH_SPECS = [
    {
        "id": "batch_01_prologue",
        "expected": 6,
        "ref_type": "dormant",
        "include_me": True,
        "prompt": """Generate 6 separate widescreen 16:9 photorealistic broadcast-cinema video clips (8 seconds each, Omni 1.1 Flash with spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, strictly matching our attached Karmic Genie Show studio image (pure-white circular marble stage, mild dark violet-magenta vault ceiling, curved transparent OLED glass barriers separating the elevated blue-seat stadium crowd, dormant gold Genie lamp on the center glass table, NO floating genie yet, centered `Karmic Genie Show` logo with generous clean white padding on both sides, flanked by the subtle brushed-gold wall inscriptions `Respect Your DUTY First. / Earn with DIGNITY Always. / Practice Life DISCIPLINE.` on the left, `Uphold Karmic DHARMA. / Raise Family with DEVOTION. / Be Grateful to Your DIVINE.` on the right, and `Purposeful Life Is Your DESTINY.` centered below the logo) and using my attached @Me Avatar (in ivory-white tailored bandhgala suit) speaking slowly, calmly, and clearly:

1) P01_Narrator_Intro: @Me stands calmly beside the waist-high curved transparent OLED glass display barrier on the pure-white circular marble stage before the attentive stadium audience, walking unhurriedly as a glowing 2025-to-2026 timeline illuminates on the glass. @Me speaks slowly and warmly: "Before anyone speaks tonight, let's take sixty quiet seconds to see what happened since early twenty twenty-five."

2) P02_Narrator_2025: Medium tracking shot of @Me beside the glowing curved glass display barrier showing `2025: $410B CAPEX | 154,445 US CUTS` while the elevated stadium audience watches quietly. @Me speaks slowly and clearly: "In twenty twenty-five, tech giants earned record profits—yet over a hundred and fifty-four thousand US roles vanished."

3) P03_Narrator_Oct25: Close-medium shot of @Me gesturing gently toward the luminous timeline arc on the curved glass barrier before the pure-white stage and subtle brushed-gold 7D stage wall. @Me speaks unhurriedly: "That October, fourteen thousand corporate jobs disappeared in one morning, while Big Tech spending crossed four hundred billion."

4) P04_Narrator_Q1_2026: Smooth widescreen shot as @Me walks slowly past the next curved glass panel illuminating `Q1 2026: 80,000+ CUTS` before the hushed blue-seat stadium tiers. @Me speaks calmly: "By early twenty twenty-six, over eighty thousand workers were cut in ninety days across Seattle, Oracle, and Dell."

5) P05_Narrator_WorldMap_Today: Widescreen shot of @Me beside a luminous holographic World Map glowing across America, Europe, Brazil, Japan, and India on the curved glass barrier. @Me speaks slowly: "Today, hyperscaler spending exceeds seven hundred and twenty billion dollars—pushing quarterly free cash flow negative."

6) P06_Narrator_NonAI_Handoff: @Me turns gracefully from the glowing glass map toward his pure-white sculptural chair and the silver-templed Tech CEO seated in the dark chair beside the dormant gold Genie lamp. @Me speaks warmly and unhurriedly: "Cloud and AI didn't shrink—every cut hit non-cloud, non-AI teams. Seven lives sit behind those numbers. Marcus, begin."
""",
    },
    {
        "id": "batch_02_scene1_sf_mysuru",
        "expected": 6,
        "ref_type": "dormant",
        "include_me": False,
        "prompt": """Generate 6 separate widescreen 16:9 photorealistic cinema video clips (8 seconds each, Omni 1.1 Flash with slow, candid spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, matching our attached Karmic Genie Show studio image (dormant gold Genie lamp on center table, NO floating genie, pure-white circular marble stage, centered `Karmic Genie Show` logo with generous side padding, flanked by subtle brushed-gold 7D wall maxims `Respect Your DUTY First. / Earn with DIGNITY Always. / Practice Life DISCIPLINE.` on the left, `Uphold Karmic DHARMA. / Raise Family with DEVOTION. / Be Grateful to Your DIVINE.` on the right, and `Purposeful Life Is Your DESTINY.` centered below) for studio shots and authentic global locations for home cutaways:

1) S1_01_Marcus_3AM_SF: Cinematic 3:12 AM San Francisco high-rise boardroom overlooking rain-streaked glass and misty bay lights; 51-year-old silver-templed Tech CEO Marcus Vance in a dark navy suit stands quietly by the window looking at red cash-flow charts on a tablet, speaking slowly and candidly: "Cutting thirty thousand corporate roles during record profits looks heartless from the outside. Look at our cash flow."

2) S1_02_Marcus_Studio_Runway: Medium close-up inside the Karmic Genie Show pure-white circular marble studio as 51-year-old CEO Marcus Vance sits in the dark sculptural chair beside the dormant gold Genie lamp, speaking slowly and honestly: "Fifty billion dollars a quarter on GPUs flipped free cash flow negative. Cloud and AI demand every dollar now."

3) S1_03_Marcus_NonAI_Choice: Intimate close-up of CEO Marcus Vance on the pure-white stage with the subtle brushed-gold 7D wall maxims behind him, speaking softly with quiet gravity: "If I keep funding non-AI devices and middle layers, in four years ninety thousand jobs vanish instead of thirty."

4) S1_04_Arjun_Mysuru_Cutaway: Warm, poignant cinematic cutaway to a twilight veranda in Mysuru, South India where a 77-year-old elderly Indian father sits quietly alone beside an uncalled telephone looking down the street, as a gentle 39-year-old Indian male voiceover reflects slowly: "Millions of us work outside our home countries—telling ourselves we left just briefly to earn dollars."

5) S1_05_Arjun_Stadium_Ghost: Medium widescreen shot in Row Two of the Karmic Genie Show elevated blue stadium seats behind the curved glass barrier, where 39-year-old Indian software engineer Arjun Rao in an understated navy jacket holds a wireless mic, speaking slowly with raw candor: "I wasn't in AI—I built consumer devices for twelve years. Chasing dollars and visas, I became a ghost at home."

6) S1_06_Arjun_Neglected_Duty: Intimate emotional close-up of 39-year-old Arjun Rao in the stadium seat as listeners beside him nod quietly, speaking softly and slowly: "I sent wire transfers instead of standing beside my aging father, sister, and wife. Now one email erased everything."
""",
    },
    {
        "id": "batch_03_scene2_london_saopaulo",
        "expected": 5,
        "ref_type": None,
        "include_me": False,
        "prompt": """Generate 5 separate widescreen 16:9 photorealistic cinema video clips (8 seconds each, Omni 1.1 Flash with slow, gentle, candid spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, depicting real human households in London and São Paulo with unhurried documentary realism:

1) S2_01_Elena_London_Hallway: Intimate 8:40 PM London flat with rain droplets on the window; 42-year-old British-European engineering manager Elena sits quietly on carpeted hallway stairs outside her sleeping nine-year-old son's half-open bedroom door holding a warm ceramic mug, speaking softly and slowly: "Our London division built internal enterprise workflows and HR operations—nothing with AI on the slide."

2) S2_02_Elena_Flattened: Tender close-up of 42-year-old Elena in soft evening lamp light in her London home, speaking slowly and candidly: "When companies flattened over thirty-five percent of small-team managers, seven years of missed bedtimes vanished in one afternoon."

3) S2_03_Elena_Daylight_Walk: Warm candid afternoon shot on a leafy London sidewalk after light rain as 42-year-old Elena walks slowly hand-in-hand in daylight with her nine-year-old son carrying his school backpack; Elena's soft voice reflects slowly: "Walking my nine-year-old son home in daylight, he asked softly: 'Mum, did you finally come back to us?'"

4) S2_04_Mateo_SaoPaulo_Desk: Warm sunlit modest apartment in São Paulo, Brazil; 23-year-old Brazilian computer science graduate Mateo sits at a small wooden laptop desk while his aging tailor father quietly stitches dark suit fabric at a vintage sewing machine nearby. Mateo speaks slowly and earnestly: "In São Paulo, nobody laid me off—the first rung simply vanished before I could step on it."

5) S2_05_Mateo_7Percent_Funnel: Intimate close-up of 23-year-old Mateo in São Paulo looking honestly toward camera with his father's tailored suits hanging behind him, speaking slowly and thoughtfully: "New graduates dropped to seven percent of Big Tech hires. My father sewed suits twenty years—where do we start?"
""",
    },
    {
        "id": "batch_04_scene3_tokyo_munich_coimbatore",
        "expected": 6,
        "ref_type": None,
        "include_me": False,
        "prompt": """Generate 6 separate widescreen 16:9 photorealistic cinema video clips (8 seconds each, Omni 1.1 Flash with slow, natural, candid spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, portraying real lives in Tokyo, Munich, and Coimbatore with calm cinematic warmth:

1) S3_01_Kenji_Tokyo_Midnight: 11:54 PM inside a quiet Shinjuku, Tokyo corporate office; 35-year-old Japanese engineer Kenji sits alone in a white dress shirt before glowing server monitors surrounded by four dark, empty teammates' desks as city lights shimmer outside. Kenji speaks quietly, politely, and slowly: "In Tokyo, I maintain non-cloud retail billing inside the surviving eighty percent under a strict hiring freeze."

2) S3_02_Kenji_Five_Pagers: Intimate close-up of 35-year-old Kenji in the late-night Tokyo office glancing gently at two buzzing on-call phones beside a cold cup of tea, speaking softly and slowly: "Four teammates left with zero replacements approved. My wife eats alone every night while I carry five pagers."

3) S3_03_Heinrich_Munich_Park: Misty golden autumn morning in Munich's Englischer Garten; 58-year-old silver-haired German hardware architect Heinrich in a classic charcoal wool coat walks slowly along a peaceful leaf-strewn path, speaking in a warm, unhurried, dignified baritone: "Across Oracle, Dell, Cisco, and Intel, tens of thousands of traditional hardware roles were cleared out."

4) S3_04_Heinrich_Dignity_At_58: Medium close-up of 58-year-old Heinrich pausing calmly beside misty autumn trees in Munich, looking into the lens with quiet dignity and speaking slowly: "At fifty-eight in Munich, thirty-five years of craft gets called legacy. How do I step down with dignity?"

5) S3_05_Kavitha_Coimbatore_Courtyard: Golden-hour sunlit traditional courtyard home in Coimbatore, South India; 33-year-old South Indian woman Kavitha in a simple cotton kurta sits peacefully with her laptop surrounded by green courtyard plants while her smiling mother pours brass filter coffee behind her. Kavitha speaks serenely and slowly: "I led internal talent tools in Bengaluru—one of the first non-AI teams automated earlier this year."

6) S3_06_Kavitha_Quiet_Question: Warm close-up of 33-year-old Kavitha in the golden Coimbatore evening light smiling gently beside her peaceful elderly parents, speaking softly and unhurriedly: "Moving home to Coimbatore cut my pay, erased my rent, and brought peace—did I retreat, or arrive early?"
""",
    },
    {
        "id": "batch_05_scene4_punchline_and_awakening",
        "expected": 4,
        "ref_type": "dormant",
        "include_me": True,
        "prompt": """Generate 4 separate widescreen 16:9 photorealistic broadcast-cinema video clips (8 seconds each, Omni 1.1 Flash, zero burned-in subtitle captions) right now in batch without asking confirmation, matching our attached Karmic Genie Show pure-white circular marble studio image (centered `Karmic Genie Show` logo with generous side padding, subtle brushed-gold 7D wall maxims `Respect Your DUTY First. / Earn with DIGNITY Always. / Practice Life DISCIPLINE.` on the left, `Uphold Karmic DHARMA. / Raise Family with DEVOTION. / Be Grateful to Your DIVINE.` on the right, and `Purposeful Life Is Your DESTINY.` centered below, curved glass barriers, elevated blue-seat stadium crowd) and using my attached @Me Avatar in his ivory-white tailored bandhgala suit:

1) S4_01_Stadium_Contemplation: Slow, unhurried widescreen tracking shot drifting across the hushed Karmic Genie Show stadium-studio—hundreds of thoughtful listeners in the elevated blue seats behind the curved glass barriers, subtle brushed-gold 7D maxims gleaming on the pure-white stage wall around the padded center logo, and the ornate 24k gold Genie lamp giving a single soft warm golden shimmer on the center glass table. Pure quiet room ambience, no spoken dialogue.

2) S4_02_Host_Whole_Map: @Me rises calmly in his ivory-white bandhgala suit beside the center glass table and dormant gold Genie lamp on the pure-white circular marble stage, speaking warmly, slowly, and reflectively: "From two hundred billion dollars in San Francisco to a quiet courtyard in Coimbatore—no spreadsheet answers all seven chairs."

3) S4_03_Host_Punchline_7D: Iconic medium close-up of @Me standing poised beside the jeweled gold lamp with the centered `Karmic Genie Show` wall emblem and subtle brushed-gold 7D inscriptions behind him; @Me pauses calmly, looks warmly into the camera lens, and speaks slowly and clearly: "So let's quiet the room and ask together: What does Genie say — the 7D way?"

4) S5_01_Lamp_Awakens_Slowly: Reverent, peaceful widescreen shot across the center glass table on the pure-white stage as overhead golden Halo lights soften into tranquil amber, and slow, graceful ribbons of emerald, warm gold, soft magenta, and sapphire stardust drift gently upward out of the jeweled gold lamp, forming the serene cross-legged Celestial Karmic Genie with palms joined in humble namaste. Soft ethereal chime ambience only, no spoken dialogue.
""",
    },
    {
        "id": "batch_06_scene5_wise_saint_mirror",
        "expected": 6,
        "ref_type": "saintly",
        "include_me": False,
        "prompt": """Generate 6 separate widescreen 16:9 photorealistic broadcast-cinema video clips (8 seconds each, Omni 1.1 Flash with spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, strictly matching our attached Karmic Genie Show studio image where the luminous Celestial Karmic Genie floats CROSS-LEGGED above the jeweled lamp between the dark chair and white chair on the pure-white circular marble stage in front of the subtle brushed-gold 7D wall maxims (`Respect Your DUTY First. / Earn with DIGNITY Always. / Practice Life DISCIPLINE.` on the left, `Uphold Karmic DHARMA. / Raise Family with DEVOTION. / Be Grateful to Your DIVINE.` on the right, and `Purposeful Life Is Your DESTINY.` centered below the padded logo). CRITICAL VOICE & POSTURE RULE: In every clip, the Karmic Genie MUST remain seated CROSS-LEGGED like a serene wise saint, and MUST speak in an ultra-peaceful, soft-spoken, polite, humble, gentle, slow saintly voice—warm, soothing, unhurried, NEVER loud or booming:

1) S5_02_Genie_Polite_Greeting: Symmetrical widescreen shot on the pure-white stage as the floating cross-legged Celestial Karmic Genie bows gently with palms joined in polite namaste toward the guests and hushed stadium, speaking very softly, politely, and slowly: "Good evening, dear friends. Thank you for speaking without masks tonight. Rest easy—I bring no commandments."

2) S5_03_Genie_No_Solutions: Tranquil medium shot of the serene cross-legged Karmic Genie smiling gently above the jeweled lamp with subtle brushed-gold 7D wall maxims behind him, speaking softly, warmly, and unhurriedly: "No human heart welcomes someone else's ready-made solution; ego guards the door. We only need a quiet lantern."

3) S5_04_Genie_Upanishad_Hook: Slow, peaceful orbital camera drift around the cross-legged Celestial Karmic Genie glowing softly in warm gold, emerald, and sapphire light above the center table, speaking gently and conversationally: "Like the ancient Upanishad parable of the Single Thunderclap—a two-minute story you might enjoy reading quietly at home tonight..."

4) S5_05_Genie_Open_Echo: Wide contemplative shot from behind the curved glass barrier as the silent stadium listens to the peaceful cross-legged Karmic Genie hovering above the pure-white stage, speaking softly and slowly: "When one open sound echoes across a turning age, each heart hears what quietly belongs to it."

5) S5_06_Genie_Three_Mirrors: Serene close-medium shot of the cross-legged wise-saint Karmic Genie opening his palms gently with humble compassion, speaking very softly and unhurriedly: "Where power sits, graceful restraint. Where love was postponed for money, presence. Where tired shoulders ache, compassion."

6) S6_01_Genie_Why_2020_2030: Slow architectural camera glide past `Respect Your DUTY First. / Earn with DIGNITY Always. / Practice Life DISCIPLINE.` on the white stage wall toward the peaceful cross-legged Karmic Genie, who wonders aloud softly and slowly: "Consider gently why this decade from twenty twenty to twenty thirty had to move so fast."
""",
    },
    {
        "id": "batch_07_scene6_blessing_in_disguise",
        "expected": 6,
        "ref_type": "saintly",
        "include_me": False,
        "prompt": """Generate 6 separate widescreen 16:9 photorealistic broadcast-cinema video clips (8 seconds each, Omni 1.1 Flash with spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, strictly matching our attached Karmic Genie Show pure-white circular marble studio image with the peaceful CROSS-LEGGED Celestial Karmic Genie floating above the jeweled lamp and subtle brushed-gold 7D stage wall (`Respect Your DUTY First. / Earn with DIGNITY Always. / Practice Life DISCIPLINE.` on the left, `Uphold Karmic DHARMA. / Raise Family with DEVOTION. / Be Grateful to Your DIVINE.` on the right, and `Purposeful Life Is Your DESTINY.` centered below the padded logo). CRITICAL VOICE & POSTURE RULE: Keep the Genie strictly CROSS-LEGGED and speaking in an ultra-peaceful, soft-spoken, polite, humble, gentle wise-saint voice—slow, calm, soothing, zero preaching:

1) S6_02_Genie_2020_Pause: Peaceful medium-wide shot of the cross-legged Celestial Karmic Genie floating serenely above the jeweled lamp between the two chairs on the pure-white stage, speaking softly and slowly: "In twenty twenty, life paused the planet and reunited families—yet once doors reopened, everyone sprinted right back."

2) S6_03_Genie_NewAge_Intuition: Gentle stadium angle across attentive listeners behind the curved glass barrier looking toward the serene cross-legged Karmic Genie on the pure-white stage, speaking softly and unhurriedly: "Even forty years ago, peaceful wordless New Age melodies sensed that a quieter, less frantic human era was coming."

3) S6_04_Genie_Expat_Millions: Warm cinematic studio shot framing the compassionate cross-legged Karmic Genie above the lamp as 39-year-old Arjun listens with glistening eyes in the stadium row; the Genie speaks very gently and slowly: "For millions working oceans away from home just for stronger currency—how easily two years turns into twelve."

4) S6_05_Genie_Blessing_In_Disguise: Intimate, deeply peaceful close-medium shot of the saintly cross-legged Karmic Genie smiling with warm kindness, offering an open question softly and slowly: "When a closed non-AI floor loosens those golden handcuffs while aging parents still wait—could this be a blessing in disguise?"

5) S6_06_Genie_London_SP_Coimbatore: Smooth slow glide past `Uphold Karmic DHARMA. / Raise Family with DEVOTION. / Be Grateful to Your DIVINE.` on the right white stage wall beside the serene cross-legged Karmic Genie, speaking softly and reflectively: "When daylight walks return in London, boilerplate fades in São Paulo, and elders smile in Coimbatore—who truly fell behind?"

6) S6_07_Genie_Munich_Oak: Respectful medium shot as the cross-legged Celestial Karmic Genie inclines his head politely toward silver-haired 58-year-old Heinrich in the front stadium row, speaking gently and slowly: "And at fifty-eight in Munich—does a seasoned oak lose dignity in autumn, or turn gently toward mentoring and peace?"
""",
    },
    {
        "id": "batch_08_scene7_finale",
        "expected": 5,
        "ref_type": "mixed_finale",
        "include_me": True,
        "prompt": "",  # Split cleanly into 8A (saintly genie, 3 clips) + 8B (dormant stage + @Me, 2 clips) below!
    },
]


PROMPT_8A_GENIE_CLOSE = """Generate 3 separate widescreen 16:9 photorealistic broadcast-cinema video clips (8 seconds each, Omni 1.1 Flash, zero burned-in subtitle captions) right now in batch without asking confirmation, strictly matching our attached Karmic Genie Show studio image with the peaceful CROSS-LEGGED Celestial Karmic Genie hovering above the jeweled lamp on the pure-white circular marble stage before the padded `Karmic Genie Show` logo and subtle brushed-gold 7D wall maxims (`Respect Your DUTY First. / Earn with DIGNITY Always. / Practice Life DISCIPLINE.` on the left, `Uphold Karmic DHARMA. / Raise Family with DEVOTION. / Be Grateful to Your DIVINE.` on the right, and `Purposeful Life Is Your DESTINY.` centered below). Keep the Genie strictly CROSS-LEGGED and speaking in an ultra-peaceful, soft-spoken, polite, humble wise-saint voice:

1) S7_01_Genie_Tokyo_And_SF: Peaceful medium shot on the pure-white stage as the cross-legged Celestial Karmic Genie bows politely toward silver-templed CEO Marcus in the dark chair, speaking softly, courteously, and slowly: "Every era needs stewards to lay new rails, Marcus—no one faults a captain steering through a storm."

2) S7_02_Genie_Ten_Years_Question: Intimate, tranquil shot of the saintly cross-legged Karmic Genie offering one gentle open reflection while CEO Marcus listens quietly with softened eyes; the Genie speaks very softly and slowly: "Ten years from now, what brings peace—how fast old floors were cleared, or how humanely the bridge held everyone?"

3) S7_03_Genie_Grateful_Bow_Return: Serene visual farewell on the pure-white circular marble stage: the cross-legged Celestial Karmic Genie presses his palms together in a humble, grateful namaste bow, smiles warmly at the stadium, and dissolves peacefully back into a slow, graceful ribbon of gold, sapphire, emerald, and soft magenta stardust flowing gently back inside the jeweled lamp on the center glass table. Soft tranquil chime ambience only, no spoken dialogue.
"""

PROMPT_8B_HOST_SIGNOFF = """Generate 2 separate widescreen 16:9 photorealistic broadcast-cinema video clips (8 seconds each, Omni 1.1 Flash with spoken audio, zero burned-in subtitle captions) right now in batch without asking confirmation, strictly matching our attached Karmic Genie Show pure-white circular marble studio image (dormant gold Genie lamp on the center glass table, NO floating genie, centered `Karmic Genie Show` logo with generous side padding, subtle brushed-gold 7D wall maxims `Respect Your DUTY First. / Earn with DIGNITY Always. / Practice Life DISCIPLINE.` on the left, `Uphold Karmic DHARMA. / Raise Family with DEVOTION. / Be Grateful to Your DIVINE.` on the right, and `Purposeful Life Is Your DESTINY.` centered below) and using my attached @Me Avatar in his ivory-white tailored bandhgala suit speaking warmly, softly, and unhurriedly:

1) S7_04_Host_Closing_Reflection: Calm medium close-up of @Me seated poised in the pure-white sculptural chair beside the now-dormant gold Genie lamp on the pure-white stage, looking warmly into the camera lens and speaking slowly: "No single answer fits twenty-three in São Paulo, thirty-nine in Seattle, fifty-eight in Munich, or San Francisco."

2) S7_05_Host_Final_Punchline: Intimate cinema close-up of @Me on the pure-white stage with the centered `Karmic Genie Show` wall emblem and subtle brushed-gold 7D maxims glowing softly behind him; @Me smiles gently and speaks slowly and clearly: "Only you know what your quiet thunder said tonight. What does Genie say — the 7D way?"
"""


class FlowFilmRunner:
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
                # Ensure 'All' tab is selected inside .cdk-overlay-pane so 'Upload media' is visible
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

                # Wait until uploaded image chip finishes uploading (aria-busy != "true") or card appears
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

            # If upload landed in grid without chip in prompt bar, attach via More options -> Add to prompt
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
            print(f"⏭️  Skipping '{prefix}' — already has {len(existing)}/{expected_count} clips.", flush=True)
            return existing

        self.open_fresh_project()
        self.configure_16x9()
        self.attach_ingredients(image_path, include_me)
        before_len = len(self.get_video_cards())
        self.submit_prompt(prompt_text)
        print(f"🎬 Submitted '{prefix}' ({expected_count} widescreen 16:9 clips)...", flush=True)

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
                # Double check 8s later that generation truly settled
                time.sleep(8.0)
                cards_recheck = len(self.get_video_cards()) - before_len
                still_running = "\nstop\n" in (self.js("document.body.innerText.toLowerCase()") or "")
                if cards_recheck == new_cnt and not still_running:
                    print(f"    [{elapsed+8:3d}s] {prefix}: generation settled with {new_cnt}/{expected_count} clips.", flush=True)
                    break

        cards_final = self.get_video_cards()
        new_cnt = max(0, len(cards_final) - before_len)
        saved = []
        # Note: Flow inserts newest cards at the top (0..new_cnt-1), so we download them all and record labels!
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
                    print(f"    ✅ Saved {dest.name} ({dest.stat().st_size/1e6:.2f} MB) <- {c['label']}", flush=True)
                    break
            self.js("document.body.click()")
            time.sleep(0.3)

        (batch_dir / f"{prefix}_manifest.json").write_text(json.dumps(saved, indent=2), encoding="utf-8")
        return saved

    def close(self):
        self.ws.close()


def resolve_ref(ref_type: str | None) -> Path | None:
    if ref_type == "dormant":
        return DORMANT_IMG if DORMANT_IMG.exists() else FALLBACK_V5_IMG
    if ref_type == "saintly":
        return SAINTLY_IMG if SAINTLY_IMG.exists() else FALLBACK_V5_IMG
    return None


def main():
    only_filter = sys.argv[1] if len(sys.argv) > 1 else None
    runner = FlowFilmRunner()
    try:
        for b in BATCH_SPECS:
            bid = b["id"]
            if only_filter and only_filter not in bid:
                continue
            bdir = EP_CLIPS_DIR / bid
            if b["ref_type"] == "mixed_finale":
                runner.run_sub_batch(bdir, "s7a_genie", resolve_ref("saintly"), False, PROMPT_8A_GENIE_CLOSE, 3)
                runner.run_sub_batch(bdir, "s7b_host", resolve_ref("dormant"), True, PROMPT_8B_HOST_SIGNOFF, 2)
            else:
                runner.run_sub_batch(bdir, bid, resolve_ref(b["ref_type"]), b["include_me"], b["prompt"], b["expected"])
        print("\n🏆 ALL S01E01 16:9 FULL-FILM BATCHES GENERATED & DOWNLOADED!", flush=True)
    finally:
        runner.close()


if __name__ == "__main__":
    main()
