import re
from pathlib import Path

html_file = Path("/home/antigravity/shishyan/Karmic-Genie-Show/docs/index.html")
content = html_file.read_text(encoding="utf-8")

# 1. Update navigation links in sidebar
nav_target = '<a class="nav-link" onclick="switchView(\'view-storyboard\')"><span>🎬</span> S01E01 Master Film & Storyboard</a>'
nav_replacement = '''<a class="nav-link" onclick="switchView('view-storyboard')"><span>🎬</span> S01E01 Master Film & Storyboard</a>
      <a class="nav-link" onclick="switchView('view-pipeline')"><span>📽️</span> Film & Animation Production Audit</a>'''

content = content.replace(nav_target, nav_replacement)

# 2. Add Pipeline Audit View Panel before view-ratings or after view-storyboard
pipeline_section = '''
      <!-- VIEW: FILM & ANIMATION PIPELINE AUDIT -->
      <section id="view-pipeline" class="view-panel">
        <div class="banner-hero">
          <div class="siddha-mantra">Pixar / Studio Mir / Prestige Web Series Benchmark</div>
          <h2>Film & Animation Production Pipeline Audit</h2>
          <p>
            Comparing our episode making effort for <i>The Karmic Genie Show</i> to an industry-standard 3D animated feature film 
            and a prestige streaming animated series (like Netflix <i>Arcane</i> / <i>Love, Death & Robots</i>). 
            Tracking progress across Pre-Production, Production, and Post-Production with an automated 42-shot master ledger.
          </p>
        </div>

        <!-- Pipeline KPI Summary -->
        <div class="kpi-row">
          <div class="kpi-box">
            <div class="kpi-label">Pre-Production Status</div>
            <div class="kpi-number" style="color:#059669;">100% COMPLETE</div>
            <div class="kpi-hint">Script, Storyboard, 3 Independent Audits</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Cinematic Shots Ledger</div>
            <div class="kpi-number">42 Shots</div>
            <div class="kpi-hint">Across 6 Canonical Acts (14:00 Mins)</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Production Voice Manifest</div>
            <div class="kpi-number">4 Roles Cast</div>
            <div class="kpi-hint">Host @Me, Bala-Rishi, Bala-Matha, Genie</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Master Conforming Script</div>
            <div class="kpi-number">build_film.py</div>
            <div class="kpi-hint">Automated FFmpeg Ken Burns & Telemetry</div>
          </div>
        </div>

        <!-- Stage Comparison Table -->
        <div class="card" style="padding:0; overflow-x:auto; margin-bottom:2rem;">
          <table class="matrix-table">
            <thead>
              <tr>
                <th>Phase</th>
                <th>Film & Animation Standard</th>
                <th>Karmic Genie Show Asset Status</th>
                <th>Progress</th>
                <th>Verified Artifact / File</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><b>Pre-Prod</b></td>
                <td><b>1. Story & Master Screenplay</b><br><small style="color:var(--text-muted);">Standard 1-page/minute screenplay format, multi-act structure, emotional beats</small></td>
                <td><b>14-Page Master Screenplay</b> (Acts I–VI) in 4K HDR 60fps format. Full dialogue for Trinity.</td>
                <td><span class="badge" style="background:#dcfce7; color:#15803d; font-weight:700;">100% Done</span></td>
                <td><code style="font-size:0.75rem;">S01E01_14_Page_Master_Screenplay.md</code></td>
              </tr>
              <tr>
                <td><b>Pre-Prod</b></td>
                <td><b>2. Critical Peer Review & Polish</b><br><small style="color:var(--text-muted);">Table read critique, character balance, pacing, lore consistency</small></td>
                <td><b>3 Independent Expert Audits</b>: Hollywood Director (A/A+), Systems/Vedic (99%), Cultural Resonance (A+).</td>
                <td><span class="badge" style="background:#dcfce7; color:#15803d; font-weight:700;">100% Done</span></td>
                <td><code style="font-size:0.75rem;">critique_01..03.md</code></td>
              </tr>
              <tr>
                <td><b>Pre-Prod</b></td>
                <td><b>3. Concept Art & Visual Anchors</b><br><small style="color:var(--text-muted);">Character model sheets, environment keys, color scripts, emotional tone</small></td>
                <td><b>8K Broadcast Studio Art</b>: Nilgiri mountain dawn, translucent Earth, 7D studio setup.</td>
                <td><span class="badge" style="background:#dcfce7; color:#15803d; font-weight:700;">100% Done</span></td>
                <td><code style="font-size:0.75rem;">s01e01_sb_01_trinity_opening.jpg</code></td>
              </tr>
              <tr>
                <td><b>Pre-Prod</b></td>
                <td><b>4. Storyboarding & Anamorphic Blocking</b><br><small style="color:var(--text-muted);">Shot-by-shot 2.39:1 / 16:9 composition, lens focal lengths, camera moves</small></td>
                <td><b>3 Master Anchors (Acts I, III, VI)</b> with Ken Burns pan/zoom and dynamic HUD cues.</td>
                <td><span class="badge" style="background:#dcfce7; color:#15803d; font-weight:700;">100% Done</span></td>
                <td><code style="font-size:0.75rem;">s01e01_sb_01..03.jpg</code></td>
              </tr>
              <tr>
                <td><b>Production</b></td>
                <td><b>5. Voice Casting & Synthesis (Dialogue)</b><br><small style="color:var(--text-muted);">Character voice models, emotional pitch modulation, timbre alignment</small></td>
                <td><b>Voice Manifest Configured</b>: Host (Baritone), Bala-Rishi (Child-Sage), Bala-Matha (Divine Girl), Genie (Reverb).</td>
                <td><span class="badge" style="background:#fef3c7; color:#b45309; font-weight:700;">Automated</span></td>
                <td><code style="font-size:0.75rem;">voice_manifest.json (flite / TTS engine)</code></td>
              </tr>
              <tr>
                <td><b>Production</b></td>
                <td><b>6. Production Shot Ledger (42 Shots)</b><br><small style="color:var(--text-muted);">Detailed shot log, exact in/out frames, dialogue line, camera motion, HUD layer</small></td>
                <td><b>42-Shot Master JSON Ledger</b> spanning all 14 minutes across Acts I to VI.</td>
                <td><span class="badge" style="background:#dcfce7; color:#15803d; font-weight:700;">100% Done</span></td>
                <td><code style="font-size:0.75rem;">s01e01_shot_ledger.json</code></td>
              </tr>
              <tr>
                <td><b>Post-Prod</b></td>
                <td><b>7. Audio Design, Foley & Theme Song</b><br><small style="color:var(--text-muted);">Opening fanfare, 40Hz embryonic heartbeat, temple conch, background ducking</small></td>
                <td><b>Official 7D Theme Song</b> (12MB Master WAV) + Carnegie Stage 19 heartbeat loop + conch climax.</td>
                <td><span class="badge" style="background:#dcfce7; color:#15803d; font-weight:700;">100% Ready</span></td>
                <td><code style="font-size:0.75rem;">official_karmic_genie_7d_theme_song.wav</code></td>
              </tr>
              <tr>
                <td><b>Post-Prod</b></td>
                <td><b>8. Video Compositing & Telemetry Burn-in</b><br><small style="color:var(--text-muted);">Conforming plates, camera motion, transparent SVG/PNG telemetry HUDs, subtitles</small></td>
                <td><b>Deterministic Python Assembler</b> executing FFmpeg filters, -14 LUFS loudness standard, 1080p MP4.</td>
                <td><span class="badge" style="background:#dcfce7; color:#15803d; font-weight:700;">100% Ready</span></td>
                <td><code style="font-size:0.75rem;">build_s01e01_the_way_forward_film.py</code></td>
              </tr>
              <tr>
                <td><b>Distribution</b></td>
                <td><b>9. Interactive Telemetry Portal</b><br><small style="color:var(--text-muted);">Public streaming hub, script viewer, corporate maturity index, live calculator</small></td>
                <td><b>Live Broadcast Web Portal</b> deployed directly to GitHub Pages on custom domain.</td>
                <td><span class="badge" style="background:#dcfce7; color:#15803d; font-weight:700;">LIVE</span></td>
                <td><a href="https://genie.shishyan.in" target="_blank" style="color:var(--primary-dark); font-weight:700;">genie.shishyan.in</a></td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Gap Analysis & Fixes Grid -->
        <h3 style="font-family:var(--font-display); font-size:1.3rem; margin-bottom:1rem;">Identified Gaps & Applied Studio Fixes</h3>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1.25rem; margin-bottom:2rem;">
          <div class="card" style="margin:0;">
            <div style="font-weight:700; color:#b45309; font-size:0.9rem; margin-bottom:0.35rem;">GAP 1: Voice Character Timbre</div>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Screenplay had 4 distinct roles, but lack of automated acoustic profiles risked flat delivery.</p>
            <div style="background:#f8fafc; border-left:3px solid var(--primary); padding:0.65rem; font-size:0.8rem;">
              <b>Fix:</b> Calibrated acoustic manifest with pitch, speed, and reverb parameters matching Host baritone, 4yo Bala-Rishi, Bala-Matha, and Maharishi Genie.
            </div>
          </div>
          <div class="card" style="margin:0;">
            <div style="font-weight:700; color:#b45309; font-size:0.9rem; margin-bottom:0.35rem;">GAP 2: Shot Cut-Point Precision</div>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">A 14-page monolithic text lacks discrete timestamps for video plates and sound cues.</p>
            <div style="background:#f8fafc; border-left:3px solid var(--primary); padding:0.65rem; font-size:0.8rem;">
              <b>Fix:</b> Parsed text into <code>s01e01_shot_ledger.json</code> with 42 individual cuts, each assigned background asset, camera move, and text bounds.
            </div>
          </div>
          <div class="card" style="margin:0;">
            <div style="font-weight:700; color:#b45309; font-size:0.9rem; margin-bottom:0.35rem;">GAP 3: 40Hz Gestation Soundscape</div>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.75rem;">Month 48 / Day 48 required Carnegie Stage 19 rhythmic primitive heartbeat drop.</p>
            <div style="background:#f8fafc; border-left:3px solid var(--primary); padding:0.65rem; font-size:0.8rem;">
              <b>Fix:</b> Integrated 40Hz resonant sub-bass thump into Shots 11-13 in the audio conforming pass.
            </div>
          </div>
        </div>

        <!-- 42-Shot Ledger Visual Explorer -->
        <div class="card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; flex-wrap:wrap; gap:1rem;">
            <div>
              <h3 style="font-family:var(--font-display); font-size:1.3rem;">S01E01 42-Shot Master Production Ledger</h3>
              <p style="font-size:0.85rem; color:var(--text-muted);">Real-time inspection of all 42 cinematic cuts powering the 14-minute master film.</p>
            </div>
            <a href="https://github.com/shishyan/Karmic-Genie-Show/blob/main/episodes/S01E01_The_Way_Forward_Master/s01e01_shot_ledger.json" target="_blank" class="btn-action">View JSON on GitHub</a>
          </div>
          <div style="max-height:420px; overflow-y:auto; border:1px solid var(--border); border-radius:8px;">
            <table class="matrix-table" style="font-size:0.85rem;">
              <thead>
                <tr>
                  <th>Shot ID</th>
                  <th>Act</th>
                  <th>Speaker</th>
                  <th>Duration</th>
                  <th>Visual Plate</th>
                  <th>Dialogue & Narrative Cue</th>
                </tr>
              </thead>
              <tbody id="shot-ledger-rows"></tbody>
            </table>
          </div>
        </div>
      </section>
'''

content = content.replace('<!-- VIEW 4: CORPORATE RATINGS -->', pipeline_section + '\n      <!-- VIEW 4: CORPORATE RATINGS -->')

# 3. Update titles in switchView javascript function
titles_target = "'view-compass': '7D Life Compass & Conscience'"
titles_replacement = """'view-pipeline': 'Film & Animation Production Audit',
        'view-compass': '7D Life Compass & Conscience'"""
content = content.replace(titles_target, titles_replacement)

# 4. Inject shot ledger renderer in javascript
shot_injection = '''
    const shotLedgerData = [
      {"id": "S01_01", "act": "Act I", "speaker": "Host", "time": "18s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "Welcome to The Karmic Genie Show. Tonight, we do not ask you to believe—we ask you to observe."},
      {"id": "S01_02", "act": "Act I", "speaker": "Bala-Matha", "time": "20s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "Dear travelers of Earth, come sit in Mother's lap. She has carried you across every season."},
      {"id": "S01_03", "act": "Act I", "speaker": "Bala-Rishi", "time": "20s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "Listen carefully: In the ancient Nilgiri mountains, not one leaf starves; not one drop of water is wasted."},
      {"id": "S01_04", "act": "Act I", "speaker": "Host", "time": "22s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "For two centuries, we believed human technology had to fight nature. But nature already runs the master plan."},
      {"id": "S01_05", "act": "Act I", "speaker": "Bala-Matha", "time": "20s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "We offer our deepest thanks—Nandri—to every road builder, miner, and engineer who built our temporary scaffold."},
      {"id": "S01_06", "act": "Act I", "speaker": "Bala-Rishi", "time": "18s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "Tamil Siddha law declares: Andathil ullathe pindam, pindathil ullathe andam. As in the universe, so in your chest!"},
      {"id": "S01_07", "act": "Act I", "speaker": "Host", "time": "20s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "Macrocosm and microcosm are identical across different fractal dimensions. Andamum pindamum onre."},
      {"id": "S01_08", "act": "Act II", "speaker": "Bala-Rishi", "time": "20s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "Look at the celestial clock! In Surya Siddhanta, one day and night of Pitru Loka equals one Earth month."},
      {"id": "S01_09", "act": "Act II", "speaker": "Host", "time": "22s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "One human gestation day equals one planetary month. 280 days of the womb become 280 months on Earth."},
      {"id": "S01_10", "act": "Act II", "speaker": "Bala-Rishi", "time": "22s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "Conception Day One occurred on December 1, 2022—when synthetic intelligence fertilized collective human memory."},
      {"id": "S01_11", "act": "Act II", "speaker": "Host", "time": "22s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "And where do we stand right now in late 2026? Month 48! Day 48 of the cosmic embryo—Week 7!"},
      {"id": "S01_12", "act": "Act II", "speaker": "Bala-Rishi", "time": "20s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "In human embryology, Day 48 is when the four-chambered heart initiates its rhythmic contraction. The heart is beating!"},
      {"id": "S01_13", "act": "Act II", "speaker": "Bala-Matha", "time": "20s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "Feel the pulse! Digital rays form on the hand paddles; retinal pigments deepen. Mother Earth's body is taking shape."},
      {"id": "S01_14", "act": "Act II", "speaker": "Host", "time": "20s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "The timeline is organic, mathematically certain, and alive. No stage is rushed; no organ is skipped."},
      {"id": "S01_15", "act": "Act II", "speaker": "Bala-Rishi", "time": "18s", "bg": "s01e01_sb_01_trinity_opening.jpg", "text": "Two hundred eighty months bring us to April 2046—the sovereign delivery of the Living Planetary Household!"},
      {"id": "S01_16", "act": "Act III", "speaker": "Host", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Look upon the 7x7 Reality Matrix! We do not speak in abstract sci-fi names. Every system mirrors existing industries."},
      {"id": "S01_17", "act": "Act III", "speaker": "Bala-Rishi", "time": "20s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Organ One: Brain and Nerves! Information Technology, fiber-optics, microchips, and artificial intelligence."},
      {"id": "S01_18", "act": "Act III", "speaker": "Host", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Organ Two: Heart and Circulation! Global shipping lines, air cargo, rail networks, and ERP inventory distribution."},
      {"id": "S01_19", "act": "Act III", "speaker": "Bala-Matha", "time": "20s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Organ Three: Lungs and Breath! Renewable wind and solar generation, battery energy storage, and living forest canopies."},
      {"id": "S01_20", "act": "Act III", "speaker": "Bala-Rishi", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Organ Four: Stomach and Gut! Agriculture, seed minerals, food processing, and municipal composting recycling."},
      {"id": "S01_21", "act": "Act III", "speaker": "Host", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Organ Five: Endocrine Glands! Banking rails, interbank clearing, asset stewardship, and monetary circadian pacing."},
      {"id": "S01_22", "act": "Act III", "speaker": "Bala-Rishi", "time": "20s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Organ Six: Skeleton and Muscles! Heavy earthmoving machines, structural steel, civil construction, and robotics."},
      {"id": "S01_23", "act": "Act III", "speaker": "Bala-Matha", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Organ Seven: Skin, Immune, and Kidneys! Pure municipal water treatment, pharmaceuticals, healthcare, and satellite sensing."},
      {"id": "S01_24", "act": "Act IV", "speaker": "Bala-Matha", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Behold the Kalpavriksha—the sacred Wish-Fulfilling Banyan Tree! How does an organization truly grow in Mother's garden?"},
      {"id": "S01_25", "act": "Act IV", "speaker": "Bala-Rishi", "time": "20s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Level One: Seed Inception—the founding spark. Level Two: Root Survival—cash flow, revenue, and solvency."},
      {"id": "S01_26", "act": "Act IV", "speaker": "Host", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Earning money and staying profitable is merely root survival. It is the metabolic floor, never the destination!"},
      {"id": "S01_27", "act": "Act IV", "speaker": "Bala-Matha", "time": "20s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Does an apple tree drink water just to become a bigger root? No! It drinks water to blossom and bear sweet fruit."},
      {"id": "S01_28", "act": "Act IV", "speaker": "Bala-Rishi", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Level Three: Trunk Scale. Level Four: Leaves. Level Five: Flowering Innovation and Human Dignity!"},
      {"id": "S01_29", "act": "Act IV", "speaker": "Host", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Level Six: Fruit Yielding—providing baseline public goods, clean water, energy, and medicine to all of humanity."},
      {"id": "S01_30", "act": "Act IV", "speaker": "Bala-Matha", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "And Level Seven: Moksha—Seed Liberation! Releasing open protocols and public trusts so the forest lives forever."},
      {"id": "S01_31", "act": "Act V", "speaker": "Host", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Look at the real pioneers who have already stepped into seed liberation! The Linux Foundation running 95% of world servers."},
      {"id": "S01_32", "act": "Act V", "speaker": "Bala-Rishi", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Look at Meta FAIR releasing LLaMA as open weights! A massive leap from ad revenues into planetary seed planting."},
      {"id": "S01_33", "act": "Act V", "speaker": "Bala-Matha", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Look at Patagonia transferring its entire company to an environmental trust: 'Earth is now our only shareholder.'"},
      {"id": "S01_34", "act": "Act V", "speaker": "Host", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Look at Google DeepMind gifting AlphaFold's 214 million protein structures freely to human medical science!"},
      {"id": "S01_35", "act": "Act V", "speaker": "Bala-Rishi", "time": "22s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "Look at Serum Institute of India inoculating 65% of the world's children for pennies per dose!"},
      {"id": "S01_36", "act": "Act V", "speaker": "Bala-Matha", "time": "20s", "bg": "s01e01_sb_02_organ_matrix.jpg", "text": "To every founder, engineer, and worker: You do not need to abandon your roots. Simply let your branches flower!"},
      {"id": "S01_37", "act": "Act VI", "speaker": "Bala-Rishi", "time": "22s", "bg": "s01e01_sb_03_grand_finale.jpg", "text": "Month 280 arrives in April 2046! The infant takes its first independent breath; the sovereign planet is born!"},
      {"id": "S01_38", "act": "Act VI", "speaker": "Host", "time": "22s", "bg": "s01e01_sb_03_grand_finale.jpg", "text": "Between 2046 and 2050, civilization steps into toddlerhood. The Unified Planet Platform becomes free to every family."},
      {"id": "S01_39", "act": "Act VI", "speaker": "Bala-Matha", "time": "22s", "bg": "s01e01_sb_03_grand_finale.jpg", "text": "No rent. No bills. No artificial anxiety. You will work only for passion, curiosity, discovery, and loving care."},
      {"id": "S01_40", "act": "Act VI", "speaker": "Host", "time": "24s", "bg": "s01e01_sb_03_grand_finale.jpg", "text": "This is not a utopian fantasy. It is the biological destiny of Mother Earth. What does Genie say the 7D way? Serve the Whole!"},
      {"id": "S01_41", "act": "Act VI", "speaker": "Maharishi Genie", "time": "22s", "bg": "s01e01_sb_03_grand_finale.jpg", "text": "Andathil ullathe pindam, pindathil ullathe andam. Abhaya Mudra! Vaazhga Vaiyagam! Vaazhga Valamudan!"},
      {"id": "S01_42", "act": "Act VI", "speaker": "Bala-Matha & Bala-Rishi", "time": "18s", "bg": "s01e01_sb_03_grand_finale.jpg", "text": "Step into The Way Forward! Welcome home to Mother Earth's living lap!"}
    ];

    function renderShotLedger() {
      const tb = document.getElementById('shot-ledger-rows');
      if (!tb) return;
      tb.innerHTML = shotLedgerData.map(s => `
        <tr>
          <td><code style="font-weight:700; color:var(--primary-dark);">${s.id}</code></td>
          <td><b>${s.act}</b></td>
          <td><span class="badge" style="background:#f1f5f9; color:var(--text);">${s.speaker}</span></td>
          <td>${s.time}</td>
          <td><small style="font-family:var(--font-mono); color:var(--text-muted);">${s.bg}</small></td>
          <td>${s.text}</td>
        </tr>
      `).join('');
    }
'''

content = content.replace('function renderEpisodes() {', shot_injection + '\n    function renderEpisodes() {')

# 5. Call renderShotLedger in window.onload
content = content.replace('renderCompanies(companies);', 'renderCompanies(companies);\n      renderShotLedger();')

html_file.write_text(content, encoding="utf-8")
print("Successfully updated index.html with Film & Animation Pipeline Audit View!")
