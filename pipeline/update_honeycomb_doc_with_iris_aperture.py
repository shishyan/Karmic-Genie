from pathlib import Path

doc_path = Path("/home/antigravity/shishyan/Karmic-Genie-Show/docs/HONEYCOMB_7_STAGES_AND_EPISODE_SEQUENCE.md")
content = doc_path.read_text(encoding="utf-8")

aperture_section = """
---

## 1.1 The Dynamic Aperture Iris & Rotating Stagecraft (The Mini-Movie Solution)

To transform *The Karmic Genie Show* from a static podcast monologue into an **immersive cinematic storytelling mini-movie**, the Central White Stage utilizes a **Dynamic Theatrical Aperture Mechanism**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 IMMERSIVE REVEALED BIOME (THE MINI-MOVIE WORLD)             │
│            (Cascading Waterfalls / Root Canyon / Solar Peak / Starfield)     │
├───────────────────────┬─────────────────────────────┬───────────────────────┤
│  LEFT SLIDING WALL    │     OPEN APERTURE PORTAL    │   RIGHT SLIDING WALL  │
│  White Curved Shell   │                             │   White Curved Shell  │
│  Embossed 7D Virtues  │  [ Hosts / Trinity Remain ] │   Embossed 7D Virtues │
│  & Tamil Inscriptions │  [ Stationary On White Hub ]│   & KGS Golden Logo   │
└───────────────────────┴─────────────────────────────┴───────────────────────┘
                                       ▲
                        [ 360° Circular Camera Dolly Tracks ]
                        [ Audience Seating in White Rotunda ]
```

### How the Stage Operates End-to-End Across Episodes:
1. **The Conversational Anchor (The Sacred White Hub):**
   - The host discussion desk, Trinity chairs (@Me, Bala-Rishi, Bala-Matha), and studio audience remain anchored on the stationary, pristine ivory marble dais. This gives the audience a continuous sense of psychological safety, home, and familiarity.
2. **The Iris Aperture Split (The Theatrical Reveal):**
   - The curved white acoustic wall—where the **golden Karmic Genie Show logo**, Tamil Siddha mantras, and **7D Virtue phrases** (*Empathy, Gratitude, Resilience, Mindfulness, Truth, Integrity, Compassion*) are carved—is mechanically mounted on heavy curved motorized gantry tracks.
   - When the narrative shifts from conversation into storytelling, the central white wall **parts and slides open horizontally like a massive theatrical aperture portal**.
3. **The 360° Rotating Stage Carousel:**
   - Behind the parting white walls sits a **massive motorized turntable carousel** carrying the 6 physical/virtual mini-movie sets.
   - Depending on the story scene, the carousel rotates the exact environmental biome into position:
     * When discussing **Root Solvency**, the wall parts to reveal the subterranean **Root Canyon** with glowing amber geodes and moss.
     * When discussing **Supply Chain & ERP**, the wall parts to reveal the **Living Waterfall Gorge** with cascading cyan rapids.
     * When discussing **Clean Fusion**, the wall reveals the **Solar Caldera Peak**.
     * When discussing **Moksha & 2050 Singularity**, the wall reveals the **Cosmic Horizon** with Earth's glowing blue curve and the golden Abhaya Mudra.
4. **Cinematic Audience Retention:**
   - This architectural duality solves the viewer fatigue problem of monologue studio shows: viewers receive both the intimate, warm comfort of a prime-time talk show and the visual thrill of an epic sci-fi/fantasy motion picture.

"""

# Insert before Section 2
content = content.replace('## 2. Core Epiphany:', aperture_section + '## 2. Core Epiphany:')
doc_path.write_text(content, encoding="utf-8")
print("Successfully appended Dynamic Aperture Iris & Rotating Stagecraft section!")
