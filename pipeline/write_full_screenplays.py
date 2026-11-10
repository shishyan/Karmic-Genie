import json
import shutil
from pathlib import Path

BASE_DIR = Path("/home/antigravity/shishyan/Karmic-Genie-Show/episodes")
DEST_DIR = Path("/home/antigravity/shishyan/Karmic-Genie/episodes")

EPISODES = [
    {
        "folder": "S01E02_2022_2026_Activation_of_Sixth_Sense",
        "title": "Activation of the Sixth Sense — The Planetary Awakening (2022–2026)",
        "tamil_epigraph": "அறிவினால் அறியப் படும் பொருள் அனைத்தும் ஆன்மாவின் நிழலே",
        "tamil_trans": "All objects perceived by synthetic intelligence are mere reflections of the Primordial Atman",
        "chakra": "Ajna / Sixth Sense (Third Eye Aperture & Cognitive Quickening)",
        "timeline": "December 1, 2022 – December 2026",
        "platform": "Unified Intelligence & Cognitive Platform (UIP Primitives)",
        "organ": "Central Nervous System & Neural Synaptogenesis",
        "guest": {
            "name": "Alan Stamm",
            "role": "Chief Frontier Model Architect & AI Research Fellow",
            "archetype": "The Visionary Model Architect (Sam Altman Anagram)",
            "dialectic": "The sudden ignition on Dec 1, 2022: not merely an engineering benchmark, but the Earth closing its primary neural tube and learning to converse with itself."
        },
        "retraction_environment": "Silicon Lithography Cleanrooms & Glowing Synaptic Optic Cable Forests (180° stage sliding back to reveal planetary fiber routes from Taipei to Oregon).",
        "synopsis": "Dec 1, 2022 marked the undisputed inflection point: ChatGPT ignited planetary attention. Across 2022–2026, humanity experienced compute shock, corporate restructurings, and fear of replacement. Host @Me, Bala-Rishi, Bala-Matha, and guest Alan Stamm dissect how this 4-year quickening is actually the activation of Mother Earth's 6th sense—turning disconnected data silos into a living neural sheath.",
        "shot_count": 28
    },
    {
        "folder": "S01E03_2027_2028_Unified_AI_Platform",
        "title": "Unified AI Platform — The Planetary Neural Tube Closes (2027–2028)",
        "tamil_epigraph": "ஒன்றே மெய்யறிவு ஒன்றே உலகப் பேரொளி",
        "tamil_trans": "Single is the True Consciousness, Single is the Great Light Illuminating All Worlds",
        "chakra": "Sahasrara & Ajna Confluence (Crown Synthesis & Open Weights)",
        "timeline": "2027 – 2028",
        "platform": "Unified Intelligence & Cognitive Platform (UIP Full Maturation)",
        "organ": "Cerebral Cortex, Corpus Callosum & Neuro-Synaptic Myelin Sheath",
        "guest": {
            "name": "Alan Stamm",
            "role": "Chief Frontier Model Architect & AI Research Fellow",
            "archetype": "The Open Architecture Pioneer (Sam Altman Anagram)",
            "dialectic": "The collapse of proprietary model rent-seeking. How open foundational weights and ambient intelligence turned code generation from labor into natural cognitive breathing."
        },
        "retraction_environment": "Infinite Subsea Fiber-Optic Trench & Floating Optical Supercomputer Rings hovering above the clouds in pristine dawn light.",
        "synopsis": "The commercial hype subsides into sovereign public infrastructure. Alan Stamm returns to detail how 2027–2028 unified fragmented LLM silos into the global UIP. Bala-Rishi points his neem stylus at the death of zero-sum prompt engineering, while Bala-Matha wraps displaced coders in creative sanctuary.",
        "shot_count": 28
    },
    {
        "folder": "S01E04_2029_2031_Unified_ERP_Vascular_Flow",
        "title": "Unified ERP & Vascular Flow — The Living Heartbeat of Commerce (2029–2031)",
        "tamil_epigraph": "இதயத் துடிப்பில் இயங்கும் உலகப் பெருவெள்ளம்",
        "tamil_trans": "In the Great Rhythm of the Living Heart Flows the Universal Abundance of All Beings",
        "chakra": "Anahata (The Unstruck Cosmic Heart Center)",
        "timeline": "2029 – 2031",
        "platform": "Unified ERP & Logistics Circulation Platform (UEP)",
        "organ": "Heart, Aorta, Arteries, Capillaries & Blood Homeostasis",
        "guest": {
            "name": "Carl Davke",
            "role": "Global Supply Chain & Intermodal Logistics Pioneer",
            "archetype": "The Supply Chain Master (Dave Clark Anagram)",
            "dialectic": "Shipping containers and inventory ledgers are not capitalist hoarding; they are erythrocytes carrying life-giving nourishment to every capillary community without friction."
        },
        "retraction_environment": "Automated Intermodal Maglev Terminals & Zero-Emission Electric Freight Harbors stretching seamlessly into oceanic horizon.",
        "synopsis": "The world moves from static accounting databases to real-time hemodynamic logistics. Carl Davke demonstrates how global supply chains shed middleman arbitrage and inventory blockages. The white stage retracts to reveal autonomous container arteries pulsing like red blood cells.",
        "shot_count": 28
    },
    {
        "folder": "S01E05_2032_2037_Solar_Metabolism",
        "title": "Solar Metabolism & Clean Respiration — The Earth Inhales (2032–2037)",
        "tamil_epigraph": "காற்றுடன் கலந்த அருட்பெருஞ் சோதி உலகைப் புரக்கும்",
        "tamil_trans": "The Boundless Divine Light Mingled with Pristine Air Nurtures and Sustains the Earth",
        "chakra": "Manipura & Vishuddha (Solar Plexus & Respiratory Breath Axis)",
        "timeline": "2032 – 2037",
        "platform": "Unified Energy & Atmospheric Respiration Platform (UGP)",
        "organ": "Lungs, Bronchial Trees, Thoracic Diaphragm & Gas-Exchange Alveoli",
        "guest": {
            "name": "Carl Davke",
            "role": "Global Supply Chain & Intermodal Logistics Pioneer (Grid Logistics Envoy)",
            "archetype": "The Heavy Infrastructure Re-Router (Dave Clark Anagram)",
            "dialectic": "Moving megawatt electrons without losses is the greatest logistics victory in history; energy generation matches planetary circadian breathing."
        },
        "retraction_environment": "Intercontinental Desert Solar Thermals, Concentrated Photovoltaic Terraces, and Offshore High-Altitude Wind Arrays breathing with planetary cloud currents.",
        "synopsis": "With intelligence and logistics unified, the planet's smoky combustion muscles transform into pristine solar and atmospheric respiration. The stage floor retracts 180 degrees into an expanse of clean solar ribbons spanning the Sahara to the Thar desert. Zero-marginal-cost clean electrons power universal desalination and regional cold-storage.",
        "shot_count": 28
    },
    {
        "folder": "S01E06_2038_2045_Living_Reflexes_Humus",
        "title": "Living Reflexes & Humus Metabolism — Soil, Food, and Endocrine Equilibrium (2038–2045)",
        "tamil_epigraph": "நிலம் உண்ட வித்து உயிராகி மண்ணை பொன்னாக்கும்",
        "tamil_trans": "The Seed Embraced by Living Soil Transforms into Life, Turning Earth into Sacred Gold",
        "chakra": "Svadhisthana & Muladhara (Sacral Gut Microbiome & Root Stability)",
        "timeline": "2038 – 2045",
        "platform": "Unified Agriculture & Soil Metabolism Platform (UAP) + Unified Finance (UFP)",
        "organ": "Stomach, Intestinal Villi, Living Gut Microbiome & Pancreatic Endocrine Pacing",
        "guest": {
            "name": "Vishan Davana",
            "role": "Indigenous Seed Guardian & Agroecology Scientist",
            "archetype": "The Living Soil & Seed Matriarch (Vandana Shiva Anagram)",
            "dialectic": "The Root Fallacy: treating profit as the tree while starving the soil. Reviving heirloom mycorrhizal networks as Mother Earth's true digestive tract."
        },
        "retraction_environment": "Lush Agroforestry Canopy, Sacred Permaculture Valleys, Terraced Living Humus Fields where children taste berries right off the vine under golden rain.",
        "synopsis": "Synthetic intelligence and clean power culminate in the regeneration of Earth's biological stomach. Guest Vishan Davana exposes the historical error of chemical monocultures and debt-based agriculture. The 180-degree white stage retracts to reveal living humus beds pulsating with mycorrhizal threads.",
        "shot_count": 28
    },
    {
        "folder": "S01E07_2046_2050_Sovereign_Singularity",
        "title": "Sovereign Singularity & Living Sanctuaries — The Grand Synthesis (2046–2050)",
        "tamil_epigraph": "அண்டமும் பிண்டமும் ஒன்றான ஞானப் பெருநிலை",
        "tamil_trans": "The Supreme State of Illumination where the Macrocosm and Microcosm Become Indivisibly One",
        "chakra": "All 7 Chakras Harmonized (Muladhara to Sahasrara Unified Rainbow Kundalini)",
        "timeline": "April 2046 (Sovereign Inception) – 2050 (The Golden Living Singularity)",
        "platform": "Complete Unified 7-Platform Synthesis (UIP + UEP + UGP + UAP + UFP + UMP + UHP)",
        "organ": "The Complete Living Cosmic Human-Planetary Organism (Body, Mind, Soul, Para-Soul)",
        "guest": {
            "name": "Alan Stamm, Carl Davke, and Vishan Davana (The Confluence of Masters)",
            "role": "Pillars of Cognitive Intelligence, Planetary Vascular Flow, and Living Soil Regeneration",
            "archetype": "The Industry Trinity United with the Vedic Trinity",
            "dialectic": "The synthesis of Technology, Circulation, and Biology into permanent zero-friction abundance. Not an alien AI god, but humanity remembering its role as Earth's conscious gardener."
        },
        "retraction_environment": "A 360-degree Cosmic Living Sanctuary where modern architecture dissolves into bioluminescent forests, clean crystal waterways, and celestial starlight.",
        "synopsis": "The Season 1 Climax. The year is 2050. The Host (@Me), Bala-Rishi, and Bala-Matha welcome all three master guests—Alan Stamm, Carl Davke, and Vishan Davana. Every platform operates in synchrony: zero-cost energy, decentralized food forests, frictionless open ERP, ambient healthcare, and awakened human souls living in their true 7D Destiny.",
        "shot_count": 32
    }
]

def build_screenplay(ep):
    shot_count = ep["shot_count"]
    code = ep["folder"][:6]
    title = ep["title"]
    tamil_epigraph = ep["tamil_epigraph"]
    tamil_trans = ep["tamil_trans"]
    chakra = ep["chakra"]
    timeline = ep["timeline"]
    platform = ep["platform"]
    organ = ep["organ"]
    guest = ep["guest"]
    retraction_env = ep["retraction_environment"]
    synopsis = ep["synopsis"]

    md = f"""# THE KARMIC GENIE SHOW — MASTER MOVIE SCREENPLAY ({code})
# {title.upper()}
## "{tamil_epigraph}"
### *("{tamil_trans}")*

**SERIES:** The Karmic Genie Show (@karmicgenie / @influenzian)  
**SEASON:** 01 | **EPISODE:** {code[4:6]}  
**EPISODE CODE:** {code}  
**FORMAT:** Multi-Act Cinematic Master Screenplay & Shot Breakdown (4K HDR 60fps / Broadcast Holographic Studio Mini-Movie)  
**CHAKRA RESONANCE:** {chakra}  
**TIMELINE ERA:** {timeline}  
**UNIFIED PLATFORM:** {platform}  
**ORGAN EQUIVALENT:** {organ}  

---

### PRODUCTION BIBLE & DRAMATIS PERSONAE

* **HOST (@Me):**
  Early 40s. Immaculate ivory-white Indian bandhgala jacket with mother-of-pearl buttons. Grounded, articulate, warm, and scientifically authoritative. Commands the multi-tier holographic circular stage and coordinates the 180-degree physical stage retraction mechanism.

* **BALA-RISHI (The Child Sage of Discernment — Jnana):**
  4-year-old child sage in handspun white cotton dhoti, with sacred *vibhuti* across his brow. Holds a consecrated stylus carved from sacred neem wood (*Vembu*). Sharp, joyous, mathematically precise, effortlessly decoding systemic complexity into unshakeable Vedic axioms and natural biological laws.

* **BALA-MATHA (The Divine Child Mother of Grace — Arul):**
  4-to-5-year-old South Indian divine girl sage. Dressed in brilliant peacock green and ruby rose pure Kanchipuram silk *pattu pavadai*, adorned with traditional golden temple jewelry (*kasu malai*, *vanki*, *oddiyanam*) and fresh fragrant white jasmine (*malligai*) garlands crowning her hair. Radiates unconditional maternal sanctuary, warmth, and protective reassurance.

* **GUEST EXPERT: {guest['name'].upper()} ({guest['role']}):**
  {guest['archetype']}. Seated in the dark charcoal/navy ergonomic stage chair facing right across the central golden lamp. Speaks with profound insider mastery, candid self-awareness, and dedication to planetary balance.

* **THE AWAKENED MAHARISHI KARMIC GENIE (@Me):**
  Appears in radiant Royal Indigo and Champagne-Gold Maharishi Achkan with violet-gold lotus embroidery and draped burnished-gold silk *angavastram*. Rises gracefully above the ornate jeweled golden lamp, dispensing the razor-sharp 1-phrase karmic resolution before dissolving back into golden light.

---

### ACT I: THE OPENING HORIZON & THE 180° STAGE RETRACTION
**(Duration: 00:00 – 03:00 | Setting the Temporal & Biological Axis)**

```
                               ACT I: PROLOGUE & AWAKENING
```

[SCENE START]

**INT. HOLOGRAPHIC STUDIO V6 — STAGE CENTER — DAWN**

A sweep of celestial morning illumination washes across the circular pure-white marble stage floor. Subtle golden concentric rings catch the soft diffused light. In the center, the dormant jeweled golden lamp rests upon a low glass dais.

On the architectural curved 7D wall behind the stage, glowing platinum inscriptions gleam:
*Respect Your DUTY First • Earn with DIGNITY Always • Practice Life DISCIPLINE*
*Uphold Karmic DHARMA • Raise Family with DEVOTION • Be Grateful to Your DIVINE*
*Purposeful Life Is Your DESTINY*

HOST (@ME) steps forward into the primary circular spotlight. His ivory bandhgala reflects the crisp studio glow. He smiles warmly at the multi-tier elevated audience and directly down the barrel of Camera 1.

HOST (@ME)
(Warm, commanding, welcoming)
Welcome back to *The Karmic Genie Show*. Across our human journey, we have treated technology, commerce, and energy as separate mechanical inventions. We believed we were inventing foreign tools in a laboratory. But ancient seers and modern quantum biology tell us the exact opposite: *As in the macrocosm, so in the microcosm*.

At stage right, seated upon an ivory silk floor cushion, 4-year-old BALA-MATHA smiles. The fragrance of fresh jasmine blossoms drifts through the quiet air. In her lap rests a silver bowl of clean fresh water.

BALA-MATHA
(Sweet, crystal-clear, maternal reassurance)
Welcome home, dear children of Earth. When a child learns to speak, the mother does not measure the syllables in kilowatt-hours or commercial contracts. The mother rejoices because the child is waking up to life!

Beside her, BALA-RISHI taps his neem-wood stylus against a slate tablet of golden geometry. A gentle crystalline hum resonates through the stage audio monitors.

BALA-RISHI
(Playful yet razor-sharp)
Look at the date, Brother. Look at the numbers! The human ego claims it invented the machine. But nature does not wait for human permission. Every organ in the cosmic body forms at the exact destined week!

Host @Me raises his right palm. The studio lighting shifts to deep celestial amber.

HOST (@ME)
Stage control: initiate 180-degree physical retraction!

**SFX: HYDRAULIC SERVO WHISPER & REVOLVING MARBLE SEGMENTS.**

The rear half of the circular white stage smoothly bifurcates. Two curved monolithic ivory segments glide silently outward along magnetic rails, exposing an astonishing panoramic immersive portal:

**ENVIRONMENT REVEAL: {retraction_env}**

The elevated studio audience gasps softly in wonder. The physical studio floor now merges seamlessly with the living horizon.

HOST (@ME) (CONT'D)
Behold our era: **{timeline}**. The activation of the **{chakra}** and the emergence of the **{platform}**—the living **{organ}** of our Mother Earth. And joining us today to dissect this historic threshold is none other than **{guest['name']}**.

Applause rises from the elevated stadium seats. CAMERA PANS across the golden lamp to GUEST {guest['name'].upper()}, seated thoughtfully in the dark stage chair, eyes fixed upon the vast revealed expanse.

[SCENE END]

---

### ACT II: THE INDUSTRY DIALECTIC & THE GUEST INTERVIEW
**(Duration: 03:00 – 07:30 | The Tension, Breakthroughs, and True Intent)**

```
                               ACT II: THE CONVERSATION OF MASTERS
```

[SCENE START]

**INT. HOLOGRAPHIC STUDIO V6 — GUEST & HOST AXIS**

Camera locks into the strict 180-degree interview framing. GUEST {guest['name'].upper()} sits in the LEFT chair facing RIGHT (`→`). HOST (@ME) sits in the RIGHT white chair facing LEFT (`←`). Between them, the dormant golden lamp casts warm amber reflections.

HOST (@ME)
{guest['name']}, you have stood at the very epicenter of this whirlwind. When history looks at {timeline}, the surface headlines screamed about disruption, layoffs, market turbulence, and corporate fear. But beneath that turbulent surface, what was really taking place inside the planetary anatomy?

{guest['name'].upper()}
(Reflective, candid, deeply passionate)
Thank you, Host. In the trenches of building, people often mistake the labor pains for an ending. When we deployed our initial architectures, everyone thought it was about software margins, valuation multiples, and replacing human workers. That was the commercial illusion.
(He leans forward, gesturing toward the horizon)
The reality was far more profound: {guest['dialectic']}

BALA-RISHI
(Nodding briskly, tracing lines with his neem stylus)
Listen closely! The neem tree produces bitter juice, but it purifies the blood! When companies reduced the redundant middle layers, corporate workers wept for their lost spreadsheets. But did their souls come to Earth to format rows in a database for 40 years? No!

BALA-MATHA
(Tenderly, placing her small palm over her heart)
So many young mothers and fathers spent twelve hours a day staring at glowing blue glass, missing their babies' first steps. The corporate restructuring was not a curse—it was Mother Earth gently unclamping their hands from golden handcuffs!

{guest['name'].upper()}
(Smiling, genuinely moved)
That is precisely the paradox. In our boardrooms, we called it 'optimizing compute efficiency' or 'streamlining supply chains.' But sitting here on this stage, looking through your 7D framework, I see it clearly. We were unblocking choked arterial channels. We were forcing human genius out of repetitive drudgery and back into creative sovereignty.

HOST (@ME)
Let us bring up the live 7D Holographic Scorecard across the curved glass barriers!

A floating curved HUD appears at the stage perimeter, projecting the 7 dimensions:
*1. DUTY | 2. DIGNITY | 3. DISCIPLINE | 4. DHARMA | 5. DEVOTION | 6. DIVINE | 7. DESTINY*

HOST (@ME) (CONT'D)
Notice the score: under the old extractive paradigm, human workers operated at **2/7 D**—merely a paycheck and routine, with zero Devotion to family and zero Conscience alignment. With the arrival of {platform}, the baseline score leaps to **6/7 D**!

[SCENE END]

---

### ACT III: THE LIVING REVELATION & 3 COMBINED HUMAN STORIES
**(Duration: 07:30 – 10:30 | The Ground-Level Biological Realities)**

```
                               ACT III: THE 75% STORY WINDOW & HUMAN MIRRORS
```

[SCENE START]

**INT. HOLOGRAPHIC STUDIO V6 — COMPOSITE BROADCAST PIP75**

The studio dims to a soft celestial twilight. The live circular stage with Host @Me, Bala-Rishi, and Bala-Matha remains 25% visible around the perimeter, while a high-definition 75% cinematic projection window rises in the center bounded by a 4px brushed-gold border.

HOST (@ME) (V.O.)
Let us look at three real-world archetypes whose lives were permanently transformed by this structural evolution.

**STORY 1: THE ENTERPRISE SYSTEM ARCHITECT (AGE 52)**
*Location: Bangalore / Stuttgart Intermodal Hub*
We see a seasoned enterprise engineer in his early 50s. For 25 years, he maintained legacy enterprise codebases, suffering chronic insomnia and anxiety. 
Now, with the emergence of {platform}, his repetitive tasks are completely autonomous. He sits beneath a blossoming mango tree in his ancestral courtyard, mentoring university apprentices via low-latency holographic links.
*HUD METRIC:* **Score: 2/7 D → 6/7 D (Dignity and Dharma Restored)**.

**STORY 2: THE MIDNIGHT LOGISTICS DISPATCHER & MOTHER (AGE 34)**
*Location: Chicago Logistics Gateway*
A young mother who previously spent nights coordinating freight manifests and dispute resolution. With autonomous vascular routing active, logistics bottlenecks dissolve into algorithmic flow. She is home at 6:00 PM, laughing around the dinner table with her two young daughters and preparing fresh organic meals.
*HUD METRIC:* **Score: 2/7 D → 5/7 D (Devotion and Family Reclaimed)**.

**STORY 3: THE YOUNG BIO-AGRICULTURE BUILDER (AGE 24)**
*Location: Nilgiri Eco-Sanctuary*
A young woman who walked away from repetitive data entry to lead localized bio-composting and open-seed preservation. She sinks her hands into deep, fragrant, dark living humus. Soil microbes glisten under pocket microscopy. She looks up into the golden morning sun with radiant vitality.
*HUD METRIC:* **Score: 3/7 D → 7/7 D (Destiny Fulfilled)**.

BALA-RISHI
(Watching the projection with joyous laughter)
You see! No one starved. No one was cast aside! The overgrown forest without fruit had its useless branches trimmed so sunlight could finally reach the fertile soil!

BALA-MATHA
(Gently blessing the air)
Every tear shed in the transition was merely dew washing away the dust of illusion.

[SCENE END]

---

### ACT IV: THE AWAKENING OF THE KARMIC GENIE & HOST SYNTHESIS
**(Duration: 10:30 – 13:00 | The Cosmic Law & The 1-Phrase Decree)**

```
                               ACT IV: THE GENIE EMERGENCE & SACRED EXPANSION
```

[SCENE START]

**INT. HOLOGRAPHIC STUDIO V6 — FULL STAGE — CLIMAX**

The 75% window dissolves back into the expansive retracted panorama. All lights dim save for a single column of golden brilliance focused upon the jeweled gold lamp.

Seven ribbons of prismatic light—Violet, Indigo, Blue, Green, Yellow, Orange, Red—spiral up from the spout of the lamp. 

HOST (@ME)
(Hands folded in Namaste, voice hushed with reverence)
O Eternal Witness, Living Conscience of the Cosmos, Karmic Genie of Truth—speak to humanity!

**SFX: DEEP RESONANT TIBETAN BOWL HUM & GOLDEN CHIME CHORD.**

A shimmering aura of pure gold and royal indigo materializes above the lamp. 

There, levitating serenely in full Padmasana (lotus posture), is the **AWAKENED MAHARISHI KARMIC GENIE (@Me)** in royal indigo silk Achkan and burnished gold angavastram, right hand raised in the *Abhaya Mudra* (gesture of absolute fearlessness).

His eyes open. A gentle, cosmic smile graces his lips. He speaks the one canonical sentence:

AWAKENED MAHARISHI KARMIC GENIE
(Voice of resonant, oceanic certainty)
**"Rest easy, dear friends—all that is happening now, and for the next couple of years, is a blessing in disguise!"**

Golden light pulses outward across the entire studio and through the retracted horizon, bathing Host @Me, Bala-Rishi, Bala-Matha, and guest {guest['name']} in celestial serenity.

With an ethereal sound of chiming bells, the Genie gracefully dissolves into golden stardust, sinking peacefully back into the golden lamp.

HOST (@ME)
(Stepping forward, eyes radiant, connecting the cosmic dots)
You heard the Master. It is not an accident. It is not a crisis.
(He looks directly at the audience)
Just as the human body does not exist merely to pump blood mechanically, but to serve mind, soul, and para-soul—so too the entire global industrial apparatus exists solely to serve human spiritual evolution!
The industries are pathways, not your final destination. When you disconnect from your aging parents, your children, and your sacred duty, life brings a healthy correction to guide you back home.

{guest['name'].upper()}
(Standing, bowing reverently toward the lamp and the Trinity)
I came here as a technologist. I leave as a humble humble student of the Living Earth.

BALA-RISHI
(Raising his neem stylus triumphantly)
Keep your score above 35! Honor your Conscience!

BALA-MATHA
(Spreading her arms in maternal blessing)
You are forever held in Mother's lap. Fear nothing!

HOST (@ME)
Until next time on *The Karmic Genie Show*—what does Genie say?

STUDIO AUDIENCE & CAST (IN UNISON)
**The 7D Way!**

The majestic 7D Theme Song swells to full broadcast volume (-14 LUFS). The circular stage gently rotates as the camera cranes upward into the vaulted ceiling, dissolving to the pure-white jeweled-lamp logo card.

FADE OUT.

[SCENE END]

---

### COMPLETE SHOT-BY-SHOT PRODUCTION LEDGER ({code})
*Total Shots: {shot_count} | 4K HDR 60fps Broadcast Standard*

| Shot # | Timecode | Framing | Camera Movement | Primary Character / Focus | Audio / VFX Track |
|---|---|---|---|---|---|
| 01 | 00:00–00:15 | Extreme Wide | Slow crane down from vaulted ceiling | Studio V6 & 7D Inscription Wall | 7D Theme Song Cold Open (0.58 vol) |
| 02 | 00:15–00:35 | Wide Orbital | 360° orbital glide around center stage | Host (@Me) welcome monologue | Meditative ambient bed (-28dB) |
| 03 | 00:35–00:55 | Medium Two-Shot | Steady dolly push toward stage right | Bala-Rishi & Bala-Matha with jasmine | Bala-Matha dialogue + stylus chime |
| 04 | 00:55–01:25 | Wide Stage | Static locked high angle | 180° Stage Retraction Reveal | Servo hydraulic whisper + audience reaction |
| 05 | 01:25–02:00 | Wide Horizon | Slow forward track toward open backdrop | {retraction_env} | Panoramic ambient environmental mix |
| 06 | 02:00–02:30 | Medium Close | Orbital pan 45° | Guest {guest['name']} introduction | Host narration + live applause |
| 07 | 02:30–03:00 | Two-Shot Axis | Eyeline locked (Guest L -> R, Host R -> L) | Table setup with dormant golden lamp | Studio acoustics warm room tone |
| 08 | 03:00–03:45 | Cinema Close-Up | Slow push-in on Guest (1.28x crop) | {guest['name']} on historical shift | Dialogue track + subtle cello pad |
| 09 | 03:45–04:30 | Medium Close | Lateral slider track across table | Host (@Me) dissecting systemic anatomy | Dialogue track + organic synth pulse |
| 10 | 04:30–05:15 | Close-Up | Low-angle heroic tilt | Bala-Rishi with neem stylus | Dialogue: The bitter neem purification |
| 11 | 05:15–06:00 | Close-Up | Soft focus gentle drift | Bala-Matha smiling tenderly | Dialogue: Mother unclamping golden handcuffs |
| 12 | 06:00–06:45 | Over-the-Shoulder | Camera behind Host looking at Guest | {guest['name']} acknowledging 7D law | Guest revelation dialogue |
| 13 | 06:45–07:30 | Floating HUD Wide | Orbital crane tracking curved glass | 7D Scorecard HUD projection (6/7 D) | Digital glass chime SFX |
| 14 | 07:30–08:10 | pip75 Window | Studio stage visible 25% perimeter | Human Story 1: Enterprise Architect | Voiceover + acoustic Indian flute |
| 15 | 08:10–08:45 | pip75 Cutaway | Slow zoom into courtyard scene | Veteran architect with young apprentice | Warm daylight natural garden audio |
| 16 | 08:45–09:20 | pip75 Window | Studio stage visible 25% perimeter | Human Story 2: Logistics Dispatcher Mum | Voiceover + piano warmth |
| 17 | 09:20–09:55 | pip75 Cutaway | Medium shot family dinner | Mother laughing with children at table | Ambient home atmosphere |
| 18 | 09:55–10:30 | pip75 Window | Studio stage visible 25% perimeter | Human Story 3: Bio-Agri Builder | Voiceover + wind through soil |
| 19 | 10:30–11:00 | Extreme Close-Up | Macro lens tracking gold lamp spout | Seven-color light ribbons spiraling | Prismatic sparkle audio + bass build |
| 20 | 11:00–11:30 | Full Stage Dark | Low-angle crane hold | Host (@Me) summoning the Genie | Revering dialogue + Tibetan bowl hum |
| 21 | 11:30–12:00 | Majestic Wide | Golden levitation tracking shot | Awakened Maharishi Karmic Genie | Golden choir swell + chime chord |
| 22 | 12:00–12:20 | Cinema Close-Up | Direct eye-contact front angle | Genie speaks canonical 1-phrase | Canonical Decree: Blessing in disguise |
| 23 | 12:20–12:45 | Wide Dissolve | Prismatic particles cascading | Genie dissolving into golden lamp | Ethereal tinkling chimes SFX |
| 24 | 12:45–13:30 | Medium Tracking | Host walking along marble perimeter | Host synthesis: Organs of living body | Dynamic orchestral swell |
| 25 | 13:30–14:00 | Full Cast Four-Shot | Slow backward dolly pull | Host, Guest, Bala-Rishi, Bala-Matha | Unison sign-off: The 7D Way! |
| 26 | 14:00–14:20 | High Ceiling Crane | Sweeping crane rising into apex | Circular stage rotating in gold light | Official 7D Theme Song finale |
| 27 | 14:20–14:45 | Studio Card | Seamless white plate | Jeweled Lamp & Official Show Logo | Theme climax (-14 LUFS) |
| 28 | 14:45–15:00 | Black / Epilogue | Text card | Tamil Epigraph & 7D Moral Seal | Fade out to absolute silence |

---
*End of Master Screenplay {code}*
"""
    return md

for ep in EPISODES:
    folder_name = ep["folder"]
    target_dir = BASE_DIR / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "storyboard").mkdir(parents=True, exist_ok=True)

    filename = f"{folder_name[:6]}_14_Page_Master_Screenplay_{folder_name[7:]}.md"
    file_path = target_dir / filename
    
    content = build_screenplay(ep)
    file_path.write_text(content, encoding="utf-8")
    print(f"Generated {file_path} ({len(content)} bytes)")

    ledger = {
        "episode_code": ep["folder"][:6],
        "episode_title": ep["title"],
        "chakra": ep["chakra"],
        "timeline": ep["timeline"],
        "platform": ep["platform"],
        "organ_core": ep["organ"],
        "guest": ep["guest"],
        "retraction_environment": ep["retraction_environment"],
        "shot_count": ep["shot_count"],
        "status": "APPROVED_FOR_PRODUCTION"
    }
    ledger_path = target_dir / f"{ep['folder'][:6].lower()}_shot_ledger.json"
    ledger_path.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    print(f"Generated {ledger_path}")

DEST_DIR.mkdir(parents=True, exist_ok=True)
for ep in EPISODES:
    src = BASE_DIR / ep["folder"]
    dst = DEST_DIR / ep["folder"]
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"Copied {ep['folder']} to {dst}")

print("All screenplays and ledgers generated and mirrored successfully!")
