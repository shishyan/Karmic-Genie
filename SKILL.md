---
name: karmic-genie-show
description: Complete production bible, Grand-Design philosophical framework, v6 7D studio specification, Google Flow ULTRA (@Me avatar + 16:9/9:16) cinematography runbook, 75%-clip/25%-studio (pip75) broadcast compositing, 1.0x brisk FFmpeg + Whisper assembly, dark-shaded BorderStyle=3 subtitle standard, mandatory Host face-identity QA, and UNLISTED-first YouTube publishing pipeline for Karmic Genie Show (@karmicgenie and @influenzian). Activate this skill whenever scripting, generating, assembling, auditing, or publishing any Karmic Genie Show episode or Short.
---

# Karmic Genie Show — Official Production Skill & Multi-Agent Runbook

## Storage Policy — Google Drive Is the Central Repository

> Updated 2026-11-08 by owner decision: Drive-first, GitHub = code only, **no Git LFS**.

- **All media lives on Google Drive** (`nagaraj957@gmail.com`): renders, clips, audio, thumbnails, bundles, masters, build artifacts. Project folder `Karmic_Genie_Show_S01E01` (Drive ID `1Mf-4vffVo6RRBhNFqTjzW3RAcC2bpbCy`) is what Colab/remote agents read.
- **GitHub is for code sync only**: scripts, `SKILL.md`, docs and small web assets. Never add `filter=lfs` rules, never commit media, OAuth tokens or `.env`.
- **Every build ends on Drive**: upload outputs with `gdrive mutate upload <file> --parent <folder-id>`, confirm the Drive size equals the local size, and record the Drive file ID.
- Dated handoff drops go in `remote_agent_sync_YYYYMMDD/` inside that folder (source bundle + README handoff + published cuts). Colab inputs: `karmic_genie_7d_colab_bundle.tar.gz`.
- **Never delete or overwrite a local binary until its Drive copy is verified** (size match). When a file name is reused by a newer build, upload the older cut under a distinct name first.
- Repo `Karmic-Genie-Show` ignores media via `.gitignore`; see its `STORAGE.md`. Published YouTube IDs are recorded in each episode's `published_manifest.json`.

This skill is the single source of truth for **all agents and subagents** working on ***Karmic Genie Show*** (`@karmicgenie` / syndication on `@influenzian`). Every agent MUST read and enforce all rules in this document before writing scripts, generating clips, assembling video masters, or uploading to YouTube.

---

## 1. Core Philosophy & Editorial Rules (NEVER Violate)

1. **The Grand Design — Industries as Vital Organs of Earth's Living Body (`Body → Mind → Soul → Para-Soul`):**
   - **NEVER portray any company, industry, CEO, employee, city, or country in a bad spot.**
   - Never use adversarial, blame-heavy, or cynical framing (strictly **FORBIDDEN** phrases: `"corporate greed"`, `"record profits while cutting"`, `"heartless"`, `"villains"`).
   - **Core Worldview:** Every company, industry, executive, employee, city, and nation exists for a purpose inside a **Grand Design**. Each industry (Tech, Banking, Shipping/Logistics, Auto, Manufacturing, Retail, Support) is akin to a **critical organ, cell, or blood vessel in the human body**. Just as the human body does not exist merely to function mechanically—it exists to serve **mind, soul, and para-soul** (`purpose`)—so too does the global corporate system serve human evolution.
   - **Connecting the Dots (Minor Hiccups Relieve Deeper Pressure Points):** Industry shifts, AI restructurings, and voluntary buyouts are **minor circulation hiccups** that relieve much deeper, long-accumulated human pressure points—unlocking golden handcuffs, fulfilling postponed **Duties** to aging parents, restoring **Devotion** and daylight hours to families, granting **Dignity** to seasoned `40s & 50s` veterans, and inspiring **Discipline** and **Destiny** in young builders.
   - **The Three Canonical Karmic Analogies & The `>= 4 of 7D` Scorecard Rule:**
     1. **The Overgrown Forest Without Fruit or Flowers:** Every soul on this planet—including the corporate soul—has a **Duty** to fulfill first at every stage of its life, followed by the remaining 6 Dimensions of 7D. No one has come to Earth merely to earn money for 50 years just to survive and leave; that is akin to a **forest full of trees with overgrown limbs yielding zero fruits or flowers** for any living being to depend upon.
     2. **Industries as Roadways & Pathways (Never the Final Destination):** An infrastructure company is akin to the **roadways and highways of a country**—highways are not the end goal; they are the pathway that helps travelers reach their true destination. Every industry and employer is a vehicle/pathway, never the soul's final destination.
     3. **IT Connectedness & The Karmic Market Correction:** The very dharma of IT and technology is **Connectedness**. When IT and corporate employees themselves become disconnected from their real home, aging parents, and children, it defeats the industry's core purpose—triggering a swift buyout/restructuring wave **just like a healthy stock market correction** to prune overgrown limbs and reconnect people to their real homes and duties.
     4. **Mandatory Live 7D Scorecard Metric (`>= 4 of 7D` Tick-Check on Every Question):**
        - Every question and character dilemma MUST be visibly analyzed on screen against all **7 Dimensions (`1. DUTY`, `2. DIGNITY`, `3. DISCIPLINE`, `4. DHARMA`, `5. DEVOTION`, `6. DIVINE`, `7. DESTINY`)** alongside global/sector timeline metrics (`2025 → Today`).
        - **Decision Rule:** If a path ticks **at least `4` of the `7` Dimensions (`>= 4/7 D`)**, you are on the right path; if it ticks fewer than `4` (`< 4/7 D`, e.g., only paycheck + routine while failing `Duty` to parents and `Devotion` to family), **change your route**! Show the Before vs. After 7D Scorecard (`e.g., 2/7 D → 6/7 D`) in the top HUD bar above the `75%` video window.
2. **Strictly ZERO Company Names & ZERO Real or Fictional Person Names:**
   - Never name specific corporations (`Amazon`, `Microsoft`, `Google`, `Meta`, `Oracle`, `Dell`, `Cisco`, `Intel`, `UPS`, `Barclays`, `Uber`, `TCS`, `Infosys`, etc.).
   - Never use real or fictional character names (`Marcus`, `Arjun`, `Elena`, `Mateo`, `Kenji`, `Heinrich`, `Kavitha`, etc.).
   - Refer strictly to authentic **real-world roles and archetypes** (*Chief Executive*, *Overseas Visa Engineer*, *Seasoned 50s Enterprise Architect*, *Flattened Middle-Manager Mum*, *Midnight Operations Survivor*, *Young Graduate Builder*, *Hometown Tech Lead*).
3. **Interactive, Welcoming Broadcast Show Format (`3-Section Structure`: Interview FIRST → 3 Combined Issues → 1-Phrase Genie → Host 7D Expansion):**
   - **Warm Audience Welcome + Visual `2025 → 2026` Glass Metrics Montage (`00:00–00:30`):**
     - Open by welcoming the live studio circle and home viewers (`show of hands` + comments).
     - **CRITICAL VISUAL RULE:** When the narrator (`@Me`) explains what happened from `2025` to today, **do NOT just show the narrator talking on camera!** Cut immediately to **visual clips of curved circular glass holographic displays & global data metrics** while `@Me`'s voiceover narrates the numbers (`2025: 154,000 shifts` → `2026: 200,000+ shifts`, `60,000 voluntary buyouts`, `$720B AI infrastructure`).
   - **Section 1 (Act I) — Real 3-Part Executive Interview FIRST (`~55s`, Eyelines Matched!):**
     - **Camera Angle & Eyeline Law:** On the studio stage, the **Guest/Tech CEO sits in the LEFT dark chair facing RIGHT (`→`)**, and **Host `@Me` sits in the RIGHT white chair facing LEFT (`←`)** across the dormant gold Genie lamp. Always match eyelines (`hflip` any mismatched single shot so CEO faces RIGHT and Host faces LEFT during their dialogue!).
     - **3-Part Interview Arc:**
       1. **All the Good Things First (AI Breakthroughs):** The Tech CEO first explains the positive breakthroughs of the AI revolution (accelerating medical cures, removing repetitive drudgery, empowering human creativity, and how every industry acts as a vital organ in Earth's living body).
       2. **The Honest Issues & Circulation Shift:** The `$50B/qtr` GPU/infrastructure shift and why non-AI corporate/support layers are being streamlined.
       3. **Cautions & Preparation for Better Change:** Why routine middle layers are shrinking and how employees can use `9–12` month voluntary buyout bridges to prepare, upskill, and own AI tools now—followed by Host `@Me` introducing the **`>= 4 of 7D` Scorecard Rule**.
   - **Section 2 (Act II) — Only 3 Combined Core Human Issues (`~40s`, `75%` Clip Window / `25%` Studio Visible + Metrics on Curved Circular Glass):**
     - Never drag out 7 separate repetitive character videos! Combine human stories into **3 tight, universal issues** (`~12–14s` each):
       1. **Issue #1 — Connectedness to Home & Aging Parents (`Duty`):** 12-Year Overseas Visa Engineer (aging father beside the phone in India) + Hometown Courtyard Return (`7D Glass Score: 2/7 → 6/7 D`).
       2. **Issue #2 — Family Devotion vs. Status Titles & Burnout (`Devotion` & `Discipline`):** Flattened Middle-Manager Mum (`7` years of missed bedtimes restored) + Midnight 5-Pager Survivor (`7D Glass Score: 2/7 → 5/7 D`).
       3. **Issue #3 — Seasoned `50s` Mastery & Young `20s` AI Builders (`Dignity` & `Destiny`):** Age-58 Veteran Architect (`35` years of mastery turning to mentoring) + Young Graduate Builder (`7D Glass Score: 3/7 → 6/7 D`).
   - **Section 3 (Act III & IV) — Ultra-Crisp `1-Phrase` Cross-Legged Karmic Genie (`~12s`) → Host (`@Me`) Connects the Dots (`~45s`):**
     - **NO long Genie lectures!** The Cross-Legged Karmic Genie awakens from the gold lamp, smiles serenely in `padmasana`, and speaks **ONLY the single core phrase**:
       > ***"Rest easy, dear friends—all that is happening now, and for the next couple of years, is a blessing in disguise!"***
       before dissolving gracefully back into the gold lamp!
     - **The Host (`@Me`) expands the details**—connecting the Grand Design (`Body, Mind, Soul, Para-Soul`), the **Overgrown Forest Without Fruit Analogy**, the **Highways as Pathways Analogy**, and the **IT Connectedness / Stock-Market Correction Law**, ending with:
       > ***"What does Genie say — the 7D way?"***

---

## 2. Official Studio Architecture (`v6` Symmetrical Padded-Logo 7D Wall)

### 2.1 Master Reference Plates (`/home/shishyan/GitHub/Karmic-Genie-Show/assets/studio_v5_masters/`)
- **Act I/II/IV Wide-Wall Dormant Lamp Studio (`16:9`, `2752×1536`):** `assets/studio_v5_masters/v7_wide_wall_dormant_16x9.jpg` (Seamless ultra-wide pure-white architectural back wall occupying the former steps area so there is generous white space on both sides of the logo and ZERO paint-patch seams!)
- **Canonical Awakened Karmic Genie Persona (`v8` — Narrator `@Me` as *The Royal Indigo & Gold Maharishi*, `16:9`, `2752×1536`):** `assets/studio_v5_masters/v8_genie_royal_indigo_sage_16x9.jpg`
  - **CRITICAL IDENTITY RULE (`Narrator = Karmic Genie in Regal Costume`):** Never use a literal cartoon blue genie! The **Karmic Genie IS the Narrator (`@Me` / Nagarajan himself)** appearing in his awakened **Royal Indigo & Champagne-Gold Maharishi costume** (midnight-indigo silk Achkan with violet-gold lotus embroidery, draped burnished-gold silk *angavastram* stole over the left shoulder, and ruby-emerald jeweled golden lamp brooch over the heart, seated/standing behind the ornate jeweled golden lamp as 7-color light ribbons rise from the spout).
  - **Host Persona vs. Genie Persona:** As the studio **Host / Narrator**, `@Me` wears his crisp **ivory-white modern bandhgala suit**. As the **Karmic Genie**, `@Me` wears the **Royal Indigo & Gold Maharishi Achkan (`Sample A`)**!
- **Universal `70-Point` (`1–10` per Dimension, `< 35 = Change Your Life's Course`) 7D Scorecard Law:**
  - Every dimension (`1. DUTY`, `2. DIGNITY`, `3. DISCIPLINE`, `4. DHARMA`, `5. DEVOTION`, `6. DIVINE`, `7. DESTINY`) is scored on a scale of **`1` to `10`** (`Max = 70`).
  - **Decision Threshold:** If any situation in your life scores **below `35 / 70`**, you must **change the course of your life**.
  - **Canonical Sage Definition of `DUTY`:** Duty is **NOT** an office job; Duty is anything that matters to your soul's growth—and its simplest test is **Conscience**: *Duty is the task that triggers guilt inside you (activating your conscience) when you fail to do it*. Most people drown this conscience trigger with alcohol, intoxicants, or distractions; like a thief who feels guilt the first few times and then normalizes it, repeatedly ignoring the conscience silences it completely—draining the world of empathy, sympathy, and compassion.
- **Official Show Logo (`Pure White`):** `assets/logo/official_karmic_genie_show_logo.jpg`
- **Official 7D Theme Song (`WAV`):** `assets/theme/official_karmic_genie_7d_theme_song.wav`
- **STRICT BAN ON FAKE DARK TOP OVERLAY BOXES:** Never render dark-backgrounded rectangular PIL boxes at the top of the screen (`y=0..150`)! All metrics and 7D Scorecards MUST be integrated **directly onto the studio's curved circular glass displays** (using glowing glass-projection typography along the lower left/right curved glass barriers, or shown inside the `2025 → 2026` holographic glass metrics clips!).

### 2.2 Exact `v6` 7D Wall Inscription Layout (Always Include Verbatim in Studio Prompts)
Never summarize this as `"7D maxims"` in prompts (summarizing causes video models to write literal `"7D maxims"` on the wall!). Always include the exact verbatim strings:
```text
   Respect Your DUTY First.        [ Logo ]       Uphold Karmic DHARMA.
   Earn with DIGNITY Always.       [  Logo  ]       Raise Family with DEVOTION.
   Practice Life DISCIPLINE.       [  Logo    ]       Be Grateful to Your DIVINE.

                       Purposeful Life Is Your DESTINY.
```
- **Stage Geometry:** Pure-white circular marble stage floor with subtle gold concentric inlay rings; mild dark violet-magenta vaulted ceiling; curved transparent OLED glass barriers separating the elevated blue-seat stadium audience; center glass table holding the ornate jeweled gold Genie lamp flanked by two sculptural chairs (dark navy/charcoal chair on the left for the guest executive; pure-white chair on the right for Host `@Me`).

---

## 3. Broadcast Visual Layout Rules (`Full Studio` vs. `pip75` 75% Clip / 25% Studio)

1. **Full-Screen Studio (`layout = "full"`):**
   - Used ONLY for live in-studio shots on the pure-white `v6` stage: Host (`@Me`) welcome, Host-to-CEO studio interview, Host summoning the Genie, the Cross-Legged Karmic Genie (`Act III`), and Host (`@Me`) Act IV expansion & sign-off.
2. **Mandatory 75% Clip Window / 25% Studio Visible (`layout = "pip75"` or `"split_*"`):**
   - **Rule:** Whenever playing external story clips, location dispatches, home call-ins, or B-roll cutaways, **NEVER go 100% full-screen and lose the studio!**
   - Keep **`~25%` of the live studio stage visible around the clip** (`v6_7d_dormant_stage_16x9.jpg` scaled to `1920×1080` with subtle slow camera drift and `eq=brightness=-0.06:saturation=0.95`), and composite the story clip at **`75%` screen size (`1480×832`)** with a **`4px` brushed-gold border (`#EBC670`)** at `(x=216, y=158)`:
     - **Top (`y=0..158`):** Vaulted studio ceiling + top-left translucent glass broadcast badge (`overlays_v3/v3_ov_*.png`).
     - **Left & Right (`x=0..216` & `x=1704..1920`):** Elevated blue-seat stadium audience rows watching the story.
     - **Bottom (`y=998..1080`):** Pure-white circular marble stage floor + high-contrast dark-shaded subtitle bar (`MarginV=28`).
3. **Mandatory Host Face Identity QA (`ZERO Stranger Mix-Ups`):**
   - **Rule:** Every single clip where the Host (`@Me`) appears on camera MUST be visually verified via a contact sheet (`ffmpeg` frame extraction + `read_file`) to confirm it shows the **true clean-shaven `@Me` Avatar (Nagarajan in his ivory-white bandhgala suit)**—NEVER a bearded generic actor!
   - If a newly generated Flow clip has clean `@Me` audio but Flow dropped the `Me` Likeness chip and rendered a generic bearded face, **NEVER use that clip's video stream**: either regenerate with the `Me` Avatar chip verified, OR pair its audio stream with a verified `@Me` studio video plate (`v3_gd_01.mp4`, `v3_b1_welcome_02.mp4`, `v3_b1_welcome_03.mp4`, `batch_05_03.mp4`, `s7b_host_01.mp4`) + `pip75` B-roll window!
4. **Theatrical Movie Cinematography (`v4.1` Multi-Cam Close-Ups, Revolving Orbits & 180-Degree Rule):**
   - **Never Leave Any Shot Static (`Zero Flat TV Framing`):** Every episode must feel like an A-list theatrical motion picture with continuous orbital camera movement, emotional close-ups, and multi-angle editing:
     - **Two-Camera Movie Cut on Every Studio Shot (`Medium Orbital Drift` → `1.26x Emotional Close-Up`):** Split every full-screen studio talking clip (`~7.5s`) at `~48%` of its duration into two distinct camera angles:
       - **Camera A (`0..48%`):** Moving/revolving medium-wide orbital dolly across the studio (`scale=2208:1242` with smooth horizontal + sinusoidal vertical animated `crop` across `t`).
       - **Camera B (`48%..100%`):** Instant Hollywood Multi-Cam Cut to an **Intimate Cinema Close-Up (`1.25x–1.42x` animated `crop` calibrated per shot `(cu_fx, cu_fy)` on the speaker's eyes/face)** with gentle lateral dolly push and subtle anamorphic edge vignette (`vignette=PI/6.5`).
       - **FFmpeg Live-Video Law:** On live `30fps` talking video, always use oversampled `scale` + time-animated `crop=1920:1080:x='...t...':y='...t...'` (never `zoompan=d>1`, which freezes live video lips onto frame 0!); reserve `zoompan` for high-resolution `2752×1536` still master plates (`v7_wide_wall_*.jpg`).
     - **Strict 180-Degree Interview Eyeline Rule:** On the circular stage, the **Guest / Tech CEO sits on the LEFT chair and MUST face RIGHT (`→`)**, while **Host `@Me` sits on the RIGHT chair and faces LEFT (`←`)**. Apply `hflip` (with clean crop) whenever an archival guest clip faces left so conversational eyelines lock across the golden lamp.
     - **Multi-Angle Cuts & Revolving Studio Background on `pip75` Human Stories:** Behind the `75%` (`1440×810`) story window, keep the `25%` `v7_wide_wall_dormant_16x9.jpg` studio background continuously revolving/gliding so the left and right curved circular glass displays stay alive. Inside the `75%` window itself, cut mid-story from an establishing shot to an emotional Close-Up (`1.22x`) or complementary B-roll angle!
     - **360-Degree Revolving Lamp Awakening & Multi-Angle Genie Climax:** Pair the Host's summons with the 3D revolving rainbow-gold lamp awakening clip (`batch_05_02.mp4`), followed by a two-angle crane-to-close-up sequence on the cross-legged Karmic Genie (`v7_wide_wall_genie_16x9.jpg`).
     - **Seamless Ultra-Wide Back Wall (`v7`) & Curved-Glass Metrics Only:** Always use `v7_wide_wall_dormant_16x9.jpg` and `v7_wide_wall_genie_16x9.jpg` (where the pure-white back wall spans seamlessly across the former side staircases with generous whitespace around the logo). **NEVER draw fake dark-backgrounded overlay boxes at the top of the screen**—all metrics and 7D Scorecards (`>= 4 of 7D`) must live on the studio's curved circular glass displays (`y=660..840`) or inside dedicated curved-glass holographic B-roll clips (`v4_ig_02.mp4`).

---

## 4. Pacing, Audio Mastering & Dark-Shaded Subtitle Standard

1. **Brisk `1.0x` Broadcast Pacing (Zero Dragging!):**
   - **NO `rubberband` slow-down** (`1.0x` natural conversational speech speed for all speakers and the Genie).
   - **NO `tpad` freeze-frames** at the end of clips.
   - Extract `16kHz` mono WAV to a `numpy.float32` array and run `faster_whisper` (`tiny.en`, `word_timestamps=True`, filtering out non-speech hallucinations like `APPLAUSE` or `MUSIC`) to trim each clip tightly to `[max(0.0, sp_st - 0.16), min(dur, sp_en + 0.22)]`.
2. **100% Readable Dark-Shaded Subtitles (`BorderStyle=3`):**
   - White-on-white subtitles without a dark backing box are unreadable over the pure-white marble floor and ivory bandhgala suit.
   - Always use `libass` **`BorderStyle=3`** (opaque/translucent dark charcoal box behind text):
     ```ass
     Style: BroadcastWhite,DejaVu Sans,34,&H00FFFFFF,&H0000D7FF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.3,0,3,11.0,0.0,2,110,110,28,1
     Style: GenieGold,DejaVu Sans,34,&H00B8F2FF,&H0000D7FF,&H38080A10,&H38080A10,-1,0,0,0,100,100,0.3,0,3,11.0,0.0,2,110,110,28,1
     ```
   - Emit each subtitle line as a **single-line sequential event** (split multi-line shot text proportionally by character length) so `BorderStyle=3` boxes never stack or overlap vertically.
3. **Master Loudness & 7D Theme Mix (`-14 LUFS`):**
   - Cold Open (`~9.5s` crane + 7D wall glide): Official 7D Theme Song at `0.58` volume.
   - Episode Body: Ducked meditative ambient bed at `0.038` (`~ -28 dB`) beneath crystal-clear dialogue.
   - Finale Pure-White Jeweled-Lamp Logo Card (`~11s`): Swells to `0.54` volume, mastered via `loudnorm=I=-14:TP=-1.5:LRA=11`.

---

## 5. Google Flow ULTRA (`CDP Port 9225`) Automation Rules

1. **Reuse Existing Verified Clips First:**
   - Before generating new clips on Google Flow, audit existing clips in `episodes/<EPISODE_DIR>/flow_16x9_clips/` and `flow_v3_interactive_clips/`. Reuse any clip that fits the narrative and passes editorial purity.
2. **Distinguishing Stage Image Chip vs. `@Me` Avatar Chip in Flow DOM:**
   - Both uploaded images and likeness avatars use `<flow-ingredient-chip>` containing `<flow-likeness-ingredient-chip>`.
   - **Uploaded Stage Image Chip (`v6_7d_dormant_stage_16x9.jpg`):** `chip.innerText` contains `'add'` (`'add\nface'`).
   - **`Me` Likeness Avatar Chip:** `chip.innerText` contains `'cancel'` (`'cancel\nface'`).
   - When both Stage Image AND `Me` Avatar are required, verify `chips == 2` (`hasImg=True` AND `hasMe=True`).
3. **Human-Paced Prompt Submission & Zero `@` Character Corruption:**
   - Never put the literal `@` character in prompt text sent via `Input.insertText` (typing `@Me` triggers ProseMirror's `@mention` popup and swallows adjacent characters). Write `matching my attached Me avatar` instead.
   - Insert text in `120-char` chunks with `0.05s` pauses, wait `0.75s`, press `Enter`, and rest `8s` between batches.
   - Use **single-person reverse-shots** when `Me` Avatar is attached (Host camera A looking across the dormant gold lamp; Guest camera B in a separate batch without `Me` Avatar) to avoid multi-face Likeness safety rejections.
4. **Menu & Download Selectors:**
   - Flow overlays use `.cdk-overlay-pane button` (not `[role="menuitem"]`). Always call `scrollIntoView({block: 'center'})` before clicking `More options` -> `Download` -> `720p Original size`, and dismiss snackbars (`Dismiss`) before clicking.

---

## 6. YouTube Publishing (`UNLISTED` First!), Drive Storage & Code-Only GitHub Sync

1. **NEVER Publish Directly to `public` While Testing the Waters:**
   - Every upload script MUST enforce `assert body["status"]["privacyStatus"] == "unlisted"`.
   - Only switch a video from `unlisted` to `public` when the user explicitly commands it after reviewing the `UNLISTED` link.
2. **Verified Channel OAuth Credentials (`/home/shishyan/GitHub/Shishyan/GuruKulaDesam/data/credentials/`):**
   - **Prime Channel — `@karmicgenie` (*Karmic Genie Show*, ID: `UCmixCKV4uTv3wIp634IRLXg`):**
     `tokens_karmicgenie/token_942198183044.json` (supports custom thumbnails `< 2MB`). *Never use `token_839236964216.json` (`@gurukuladesam2`).*
   - **Syndication Channel — `@influenzian` (*Influenzian*, ID: `UCcJFqC7z0f-ARNcJadKiKpQ`):**
     `token_influenzian.json`.
3. **Repository Structure (`/home/shishyan/GitHub/Karmic-Genie-Show` → `https://github.com/shishyan/Karmic-Genie-Show`):**
   - `assets/logo/`, `assets/studio_v5_masters/`, `assets/theme/`
   - `episodes/S01E01_Employees_vs_Tech_CEO/` (`S01E01_v3_Interactive_Screenplay.md`, `overlays_v3/`, `s01e01_v3_thumbnail_16x9.jpg`)
   - `pipeline/` (`render_s01e01_v3_overlays.py`, `generate_s01e01_v3_interactive.py`, `build_s01e01_v3_interactive.py`, `render_v3_thumbnail_and_publish_unlisted.py`)
   - Keep raw clip folders (`flow_*_clips/`) and `>100MB` `.mp4` renders in `.gitignore`.
