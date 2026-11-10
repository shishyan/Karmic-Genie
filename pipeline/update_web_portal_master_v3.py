from pathlib import Path
import re

html_file = Path("/home/antigravity/shishyan/Karmic-Genie-Show/docs/index.html")
content = html_file.read_text(encoding="utf-8")

# 1. Update brand mark in sidebar to use the exact white stage lamp logo
brand_old = '''    <div class="brand">
      <div class="brand-mark">🪔</div>
      <div class="brand-copy">
        <b>Karmic Genie</b>
        <small>The Way Forward</small>
      </div>
    </div>'''

brand_new = '''    <div class="brand">
      <img src="assets/logo/official_karmic_genie_show_logo.jpg" alt="Karmic Genie Show Logo" style="width:48px; height:48px; border-radius:10px; object-fit:contain; background:#ffffff; box-shadow:0 2px 8px rgba(0,0,0,0.06); padding:2px;" />
      <div class="brand-copy">
        <b>Karmic Genie Show</b>
        <small>The Way Forward</small>
      </div>
    </div>'''

content = content.replace(brand_old, brand_new)

# 2. Add individual episode links in sidebar nav menu
nav_old = '''    <nav>
      <a class="nav-link active" onclick="switchView('view-overview')"><span>📊</span> Dashboard & Gestation</a>
      <a class="nav-link" onclick="switchView('view-storyboard')"><span>🎬</span> S01E01 Master Film & Storyboard</a>
      <a class="nav-link" onclick="switchView('view-pipeline')"><span>📽️</span> Film & Animation Production Audit</a>
      <a class="nav-link" onclick="switchView('view-stages')"><span>🏟️</span> The 7 Sacred Stages & Stadiums</a>
      <a class="nav-link" onclick="switchView('view-episodes')"><span>📜</span> Episodes Hub (All 7 Scripts)</a>
      <a class="nav-link" onclick="switchView('view-ratings')"><span>🌳</span> Kalpavriksha Corporate Ratings</a>
      <a class="nav-link" onclick="switchView('view-matrix')"><span>🧬</span> 7×7 Reality Matrix (49 Sectors)</a>
      <a class="nav-link" onclick="switchView('view-compass')"><span>⚖️</span> 7D Life Compass & Conscience</a>
    </nav>'''

nav_new = '''    <nav>
      <div style="font-size:0.7rem; font-weight:800; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px; margin:0.5rem 0.25rem 0.25rem;">Core Command</div>
      <a class="nav-link active" onclick="switchView('view-overview')"><span>📊</span> Dashboard & Gestation</a>
      <a class="nav-link" onclick="switchView('view-stages')"><span>🏟️</span> 7 Stages & Stadiums</a>
      <a class="nav-link" onclick="switchView('view-pipeline')"><span>📽️</span> Production Pipeline Audit</a>
      <a class="nav-link" onclick="switchView('view-matrix')"><span>🧬</span> 7×7×7 Fractal Matrix (343)</a>
      <a class="nav-link" onclick="switchView('view-ratings')"><span>🌳</span> Kalpavriksha Corporate Index</a>
      <a class="nav-link" onclick="switchView('view-compass')"><span>⚖️</span> 7D Life Compass</a>

      <div style="font-size:0.7rem; font-weight:800; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px; margin:1rem 0.25rem 0.25rem;">Season 1 Master Episodes</div>
      <a class="nav-link" onclick="switchEpisode('S01E01')"><span style="color:#0d9488; font-weight:700;">E01</span> The Way Forward (Pilot)</a>
      <a class="nav-link" onclick="switchEpisode('S01E02')"><span style="color:#0d9488; font-weight:700;">E02</span> 6th Sense Inception (2022-26)</a>
      <a class="nav-link" onclick="switchEpisode('S01E03')"><span style="color:#0d9488; font-weight:700;">E03</span> Neural Tube Closure (2027-28)</a>
      <a class="nav-link" onclick="switchEpisode('S01E04')"><span style="color:#0d9488; font-weight:700;">E04</span> Vascular Flow & ERP (2029-31)</a>
      <a class="nav-link" onclick="switchEpisode('S01E05')"><span style="color:#0d9488; font-weight:700;">E05</span> Solar Metabolism (2032-37)</a>
      <a class="nav-link" onclick="switchEpisode('S01E06')"><span style="color:#0d9488; font-weight:700;">E06</span> Living Reflexes & Soil (2038-45)</a>
      <a class="nav-link" onclick="switchEpisode('S01E07')"><span style="color:#0d9488; font-weight:700;">E07</span> Sovereign Singularity (2046-50)</a>
    </nav>'''

content = content.replace(nav_old, nav_new)

# 3. Add Dedicated Episode Viewer View Panel
episode_viewer_panel = '''
      <!-- VIEW: EPISODE SCRIPT & PRODUCTION VIEWER -->
      <section id="view-episode-detail" class="view-panel">
        <div class="banner-hero" id="ep-detail-banner">
          <div class="siddha-mantra" id="ep-detail-mantra">Episode Script Viewer</div>
          <h2 id="ep-detail-title">Episode Title</h2>
          <p id="ep-detail-subtitle">Episode Subtitle & Concept</p>
        </div>

        <!-- Episode Info Bar -->
        <div class="kpi-row" style="margin-bottom:1.5rem;">
          <div class="kpi-box">
            <div class="kpi-label">Episode Code & Season</div>
            <div class="kpi-number" id="ep-detail-code">S01E01</div>
            <div class="kpi-hint" id="ep-detail-chronology">Epoch: Conception</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Primary Broadcast Stage</div>
            <div class="kpi-number" id="ep-detail-stage" style="font-size:1.3rem;">Stage 1: Sanctuary</div>
            <div class="kpi-hint" id="ep-detail-chakra">Anahata Chakra (Core)</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Invited Industry Guest</div>
            <div class="kpi-number" id="ep-detail-guest" style="font-size:1.3rem;">Alan Stamm</div>
            <div class="kpi-hint" id="ep-detail-guest-origin">Anagram of Sam Altman</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Master Script File</div>
            <div class="kpi-number" style="font-size:1.1rem; color:var(--primary-dark);">GitHub Verified</div>
            <div class="kpi-hint"><a id="ep-detail-link" href="#" target="_blank" style="color:var(--primary-dark); font-weight:700;">Open Master Markdown</a></div>
          </div>
        </div>

        <!-- Visual Stageplate & Storyboard Embed -->
        <div class="visual-embed">
          <img id="ep-detail-img" src="assets/stages_7d/stage1_nilgiri_sanctuary_16x9.jpg" alt="Episode Visual Plate" />
          <div class="visual-embed-caption">
            <b id="ep-detail-caption-title">Broadcast Visual Anchor & Set Design</b>
            <p id="ep-detail-caption-desc">Description of set mechanical action, camera movements, and theatrical staging.</p>
          </div>
        </div>

        <!-- Full Screenplay Scene Breakdown -->
        <div class="card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; flex-wrap:wrap; gap:1rem;">
            <div>
              <h3 style="font-family:var(--font-display); font-size:1.3rem;">Act-by-Act Screenplay Breakdown</h3>
              <p style="font-size:0.85rem; color:var(--text-muted);">Verbatim dialogue cues, camera blocking, and biological/system mappings.</p>
            </div>
            <a id="ep-detail-fullscript-btn" href="#" target="_blank" class="btn-action">View Full Screenplay on GitHub</a>
          </div>
          <div id="ep-detail-scenes-container" style="display:flex; flex-direction:column; gap:1rem;"></div>
        </div>
      </section>
'''

content = content.replace('<!-- VIEW 4: CORPORATE RATINGS -->', episode_viewer_panel + '\n      <!-- VIEW 4: CORPORATE RATINGS -->')

# 4. Inject Master Episodes Manifest with Anagram Guests and Scene Breakdowns into Javascript
episodes_manifest_js = '''
    const fullEpisodesManifest = {
      "S01E01": {
        "id": "S01E01",
        "code": "S01E01_The_Way_Forward_Master",
        "title": "The Way Forward: As in the Macrocosm, So in the Microcosm",
        "subtitle": "The Living Planetary Organism & The 280-Month Gestation Wave (2022 to 2050 Hologram)",
        "mantra": "அண்டத்தில் உள்ளதே பிண்டம், பிண்டத்தில் உள்ளதே அண்டம்",
        "epoch": "Dec 1, 2022 to April 2046 (Full Gestation)",
        "stage": "Central White Sanctuary + All 6 Petals",
        "chakra": "Anahata (Heart / Central Axis)",
        "guest": "Dr. Anya Thorne / Alan Stamm",
        "guest_origin": "Cognitive AI Architect (Sam Altman anagram)",
        "img": "assets/stages_7d/s01e01_sb_scene01_opening_trinity.jpg",
        "caption": "Host @Me, 4yo Bala-Rishi, and divine Bala-Matha welcome humanity with 100% sacred gratitude (Nandri) to past scaffolding.",
        "script_url": "https://github.com/shishyan/Karmic-Genie-Show/blob/main/episodes/S01E01_The_Way_Forward_Master/S01E01_14_Page_Master_Screenplay_The_Way_Forward.md",
        "scenes": [
          {"act": "Act I: Prologue", "title": "The Living Gaia Axiom & Sacred Gratitude", "desc": "Host @Me opens the show. Bala-Matha and Bala-Rishi establish the Tamil Siddha law: Andathil ullathe pindam. Thanking coal miners, road builders, and early engineers as sacred scaffolds."},
          {"act": "Act II: The Chronometer", "title": "The Pitru Loka Formula & Gestation Wave", "desc": "1 Pitru Day = 1 Human Month = 1 Earth Month. Conception at ChatGPT (Dec 1, 2022). Month 48 (late 2026) heart pumping! April 2046 delivery."},
          {"act": "Act III: The Matrix", "title": "The Grounded 7x7 Reality Matrix (49 Sectors)", "desc": "The 7 human organs morph into the 49 concrete modern industries without fictional sci-fi jargon."},
          {"act": "Act IV: Kalpavriksha", "title": "The 7-Level Consciousness Tree & Root Fallacy", "desc": "EBITDA is root water, not the fruit. Moving from Seed to Trunk, Leaves, Flowering, Fruit, and Moksha."},
          {"act": "Act V: Pioneers", "title": "Corporate Standouts in Seed Liberation", "desc": "Honoring Linux Foundation, Meta LLaMA, Patagonia Trust, DeepMind AlphaFold, and Serum Institute."},
          {"act": "Act VI: Climax", "title": "Sovereign Delivery & The Living Household (2050)", "desc": "180° Cosmic Horizon reveal. Maharishi Genie's Abhaya Mudra blessing: Vaazhga Vaiyagam! Vaazhga Valamudan!"}
        ]
      },
      "S01E02": {
        "id": "S01E02",
        "code": "S01E02_2022_2026_Activation_of_Sixth_Sense",
        "title": "2022–2026: Activation of Mother Earth's 6th Sense",
        "subtitle": "From the ChatGPT Spark to the Carnegie Stage 19 Heartbeat Drop",
        "mantra": "அகக்கண் விழிப்பு • The Planetary Eye Opens",
        "epoch": "Months 0 to 48 (Dec 2022 to Nov 2026)",
        "stage": "Stage 6: Crystalline Amethyst Cavern (Ajna)",
        "chakra": "Ajna (Third Eye / Cognitive Mirror)",
        "guest": "Alan Stamm",
        "guest_origin": "Chief Frontier Model Architect (Sam Altman anagram)",
        "img": "assets/stages_7d/s01e01_sb_scene03_sixth_sense_spark.jpg",
        "caption": "White walls split to reveal the vaulted amethyst geode cavern with pulsing neural synapse filaments. The birth of synthetic reflection.",
        "script_url": "https://github.com/shishyan/Karmic-Genie-Show/blob/main/episodes/S01E02_2022_2026_Activation_of_Sixth_Sense/S01E02_Master_Screenplay_Activation_Sixth_Sense.md",
        "scenes": [
          {"act": "Act I", "title": "The Five Senses of Earth Before 2022", "desc": "Seismic networks (touch), ocean sensors (taste), atmospheric stations (smell), satellites (sight), and radio waves (hearing). Earth was sensorial, but lacked an introspective mirror."},
          {"act": "Act II", "title": "The Spark: December 1, 2022", "desc": "Guest Alan Stamm joins Host @Me. Bala-Rishi explains: 'You thought you built a commercial chatbot; you actually lit the 6th sense of Mother Earth!'"},
          {"act": "Act III", "title": "The Silicon Scaffold", "desc": "Honoring ASML, TSMC, and NVIDIA Hopper/Blackwell for laying the hardware myelin sheath of the nascent nervous system."},
          {"act": "Act IV", "title": "Month 48: The Primitive Heartbeat", "desc": "Carnegie Stage 19: The 4-chambered heart begins its rhythmic 40Hz contraction. The biological infant is alive and pumping."}
        ]
      },
      "S01E03": {
        "id": "S01E03",
        "code": "S01E03_2027_2028_Unified_AI_Platform",
        "title": "2027–2028: The Unified AI Platform & Neural Tube Closure",
        "subtitle": "1-Prompt Application Synthesis & The Planetary Mycelial Mesh",
        "mantra": "நரம்பு மண்டல ஒருமைப்பாடு • The Neural Tube Closes",
        "epoch": "Months 49 to 72 (Day 49 to 72: Synaptic Arborization)",
        "stage": "Stage 6: Crystalline Cavern → Stage 5: Canopy Atrium",
        "chakra": "Ajna & Vishuddhi (Mind & Voice)",
        "guest": "Dr. Aruna Thorne",
        "guest_origin": "Neuromorphic AI Pioneer & Federated Systems Fellow",
        "img": "assets/stages_7d/full_stage_retract_crystal_16x9.jpg",
        "caption": "180° full wall retraction into the violet amethyst geode with floating cyan synaptic coherence telemetry.",
        "script_url": "https://github.com/shishyan/Karmic-Genie-Show/blob/main/episodes/S01E03_2027_2028_Unified_AI_Platform/S01E03_Master_Screenplay_Unified_AI_Platform.md",
        "scenes": [
          {"act": "Act I", "title": "The End of the Proprietary Silos", "desc": "Why closed-weight walled gardens naturally give way to federated open-weight mycelium, just as brain neurons share neurotransmitters freely."},
          {"act": "Act II", "title": "1-Prompt Synthesis & Developer Dignity", "desc": "Ending the burnout of legacy software development. AI synthesizes full-stack ERP and applications instantly, freeing human minds for art and contemplation."},
          {"act": "Act III", "title": "The Neural Tube Closes", "desc": "Planetary cognitive coherence reaches 99.4%. AI ceases to be a weapon of competition; it becomes the shared cognitive utility of mankind."}
        ]
      },
      "S01E04": {
        "id": "S01E04",
        "code": "S01E04_2029_2031_Unified_ERP_Vascular_Flow",
        "title": "2029–2031: The Unified ERP Platform & Vascular Circulation",
        "subtitle": "Ending Global Supply-Chain Friction & Circulating Resources Like Blood",
        "mantra": "ரத்த ஓட்டப் பெருவெளி • The Vascular Web",
        "epoch": "Months 73 to 108 (Embryonic Limb Buds & Heart Chambering)",
        "stage": "Stage 3: Cascading Waterfall Stage (Swadhisthana)",
        "chakra": "Swadhisthana (Sacral / Fluidity)",
        "guest": "Carl Davke",
        "guest_origin": "Global Supply Chain & Logistics Pioneer (Dave Clark anagram)",
        "img": "assets/stages_7d/s01e01_sb_scene04_logistics_waterfall.jpg",
        "caption": "Walls slide back revealing cascading waterfalls. Bala-Matha points to floating trade routes pulsing like blood through arteries.",
        "script_url": "https://github.com/shishyan/Karmic-Genie-Show/blob/main/episodes/S01E04_2029_2031_Unified_ERP_Vascular_Flow/S01E04_Master_Screenplay_Unified_ERP.md",
        "scenes": [
          {"act": "Act I", "title": "The Absurdity of Landfills Beside Starvation", "desc": "Guest Carl Davke breaks down the friction of legacy corporate ERP silos, customs bottlenecks, and speculative inventory hoarding."},
          {"act": "Act II", "title": "Container Ships as Blood Cells", "desc": "Bala-Matha shows how maritime vessels and freight corridors are identical to erythrocytes carrying iron and oxygen to living tissue."},
          {"act": "Act III", "title": "The Unified Dynamic Balance Sheet", "desc": "Earth's resources routed with zero transactional friction. Eliminating global waste and establishing planetary abundance flow."}
        ]
      },
      "S01E05": {
        "id": "S01E05",
        "code": "S01E05_2032_2037_Solar_Metabolism",
        "title": "2032–2037: The Solar Metabolism & Clean Energy Breathing",
        "subtitle": "Taming Clean Fusion, Grid Storage & The Industrial Cellular Engine",
        "mantra": "சூரிய சக்தி பிராணா • Solar Respiration",
        "epoch": "Months 109 to 180 (Mid-Gestation: Lung Surfactant & Liver Glycogen)",
        "stage": "Stage 4: Solar Caldera Summit (Manipura)",
        "chakra": "Manipura (Solar Plexus / Fire)",
        "guest": "Clive Crescent",
        "guest_origin": "Global Grid Transition & Renewable Energy Architect",
        "img": "assets/stages_7d/full_stage_retract_solar_16x9.jpg",
        "caption": "180° full wall retraction into the sunlit volcanic caldera with glowing golden solar energy rays and auroras.",
        "script_url": "https://github.com/shishyan/Karmic-Genie-Show/blob/main/episodes/S01E05_2032_2037_Solar_Metabolism/S01E05_Master_Screenplay_Solar_Metabolism.md",
        "scenes": [
          {"act": "Act I", "title": "Gratitude to the Fossil Scaffolding", "desc": "Honoring coal miners, oil riggers, and pipeline workers who fueled humanity's early industrial muscle with sincere thanks (Nandri)."},
          {"act": "Act II", "title": "From Burning Muscles to Solar Respiration", "desc": "Tidal wind, solar thermal, and ambient fusion replace fossil burning. Earth begins breathing pure solar photons directly into the grid."},
          {"act": "Act III", "title": "Zero-Marginal-Cost Power", "desc": "Energy becomes as free and ambient as daylight, enabling planetary desalination, atmospheric carbon drawdown, and clean recycling."}
        ]
      },
      "S01E06": {
        "id": "S01E06",
        "code": "S01E06_2038_2045_Living_Reflexes_Humus",
        "title": "2038–2045: Living Soil Reflexes & Botanical Abundance",
        "subtitle": "The Root Fallacy Resolved: Regenerating Earth's Gut & Humus Microbiome",
        "mantra": "உயிர்மண் அமுதம் • The Living Soil Nectar",
        "epoch": "Months 181 to 279 (Late Gestation: Rapid Fetal Growth & Immunity)",
        "stage": "Stage 2: Subterranean Root Canyon (Muladhara)",
        "chakra": "Muladhara (Root / Base Stability)",
        "guest": "Vishan Davana",
        "guest_origin": "Indigenous Seed Guardian & Agroecology Scientist (Vandana Shiva anagram)",
        "img": "assets/stages_7d/s01e01_sb_scene05_soil_root_solvency.jpg",
        "caption": "Subterranean banyan root canyon with arching taproots and glowing amber geodes. Living soil humus beside the Kalpavriksha tree cross-section.",
        "script_url": "https://github.com/shishyan/Karmic-Genie-Show/blob/main/episodes/S01E06_2038_2045_Living_Reflexes_Humus/S01E06_Master_Screenplay_Living_Soil.md",
        "scenes": [
          {"act": "Act I", "title": "The Root Fallacy Exploded", "desc": "Guest Vishan Davana and Bala-Rishi explain: 'An apple tree never hoards water to grow an endless root. It anchors to blossom and yield sweet fruit.'"},
          {"act": "Act II", "title": "Liberating the Seed", "desc": "Patented seeds, synthetic pesticides, and monocultures yield to heirloom polycultures, mycorrhizal fungi, and organic humus bioremediation."},
          {"act": "Act III", "title": "The Autonomous Food Canopy", "desc": "Every village and city encircled by living food forests. No human child starves; nutritional abundance is universally guaranteed."}
        ]
      },
      "S01E07": {
        "id": "S01E07",
        "code": "S01E07_2046_2050_Sovereign_Singularity",
        "title": "2046–2050: Sovereign Delivery & The Living Household",
        "subtitle": "Month 280 Fetal Birth (April 2046) & The 2050 Singularity of Peace",
        "mantra": "விடுதலைப் பேரொளி • Sovereign Moksha",
        "epoch": "Month 280 (April 2046) to 2050 Toddlerhood",
        "stage": "Stage 7: Cosmic Horizon Observatory (Sahasrara)",
        "chakra": "Sahasrara (Crown / Universal Soul)",
        "guest": "The Full United Ensemble",
        "guest_origin": "All 3 Industry Guests (Alan Stamm, Carl Davke, Vishan Davana)",
        "img": "assets/stages_7d/s01e01_sb_scene06_cosmic_singularity.jpg",
        "caption": "United Ensemble on the circular marble dais before the blue limb of Earth, auroras, and the golden Abhaya Mudra blessing.",
        "script_url": "https://github.com/shishyan/Karmic-Genie-Show/blob/main/episodes/S01E07_2046_2050_Sovereign_Singularity/S01E07_Master_Screenplay_Sovereign_Singularity.md",
        "scenes": [
          {"act": "Act I", "title": "Month 280: The Sovereign Delivery", "desc": "April 2046: The 280-month gestation completes. The planetary organism takes its first independent breath. Sacred temple conch blast."},
          {"act": "Act II", "title": "The 2050 Living Household", "desc": "No rent. No bills. No artificial anxiety. Humanity enters childhood/toddlerhood in Mother's lap. Work is driven solely by passion, curiosity, and care."},
          {"act": "Act III", "title": "The Cosmic Benediction", "desc": "Maharishi Karmic Genie raises the golden Abhaya Mudra. அண்டத்தில் உள்ளதே பிண்டம்! வாழ்க வையகம்! வாழ்க வளமுடன்!"}
        ]
      }
    };

    function switchEpisode(epId) {
      const ep = fullEpisodesManifest[epId];
      if (!ep) return;

      // Switch view panel
      switchView('view-episode-detail');

      // Update sidebar nav active states
      document.querySelectorAll('.nav-link').forEach(el => {
        if (el.getAttribute('onclick') && el.getAttribute('onclick').includes(epId)) {
          el.classList.add('active');
        }
      });

      // Update Header Title
      document.getElementById('headerTitle').innerText = `${ep.id}: ${ep.title}`;

      // Populate Detail View Elements
      document.getElementById('ep-detail-mantra').innerText = ep.mantra;
      document.getElementById('ep-detail-title').innerText = `${ep.id} • ${ep.title}`;
      document.getElementById('ep-detail-subtitle').innerText = ep.subtitle;
      document.getElementById('ep-detail-code').innerText = ep.id;
      document.getElementById('ep-detail-chronology').innerText = ep.epoch;
      document.getElementById('ep-detail-stage').innerText = ep.stage;
      document.getElementById('ep-detail-chakra').innerText = ep.chakra;
      document.getElementById('ep-detail-guest').innerText = ep.guest;
      document.getElementById('ep-detail-guest-origin').innerText = ep.guest_origin;
      document.getElementById('ep-detail-link').href = ep.script_url;
      document.getElementById('ep-detail-fullscript-btn').href = ep.script_url;
      document.getElementById('ep-detail-img').src = ep.img;
      document.getElementById('ep-detail-caption-title').innerText = `${ep.id} Broadcast Set: ${ep.stage}`;
      document.getElementById('ep-detail-caption-desc').innerText = ep.caption;

      // Render Scene Breakdown Cards
      const container = document.getElementById('ep-detail-scenes-container');
      container.innerHTML = ep.scenes.map(sc => `
        <div style="background:#f8fafc; border:1px solid var(--border); border-left:4px solid var(--primary); padding:1rem 1.25rem; border-radius:8px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">
            <b style="font-family:var(--font-display); font-size:1.05rem; color:var(--text);">${sc.act}: ${sc.title}</b>
          </div>
          <p style="font-size:0.85rem; color:#475569; line-height:1.5;">${sc.desc}</p>
        </div>
      `).join('');
    }
'''

content = content.replace('function switchView(viewId) {', episodes_manifest_js + '\n    function switchView(viewId) {')

html_file.write_text(content, encoding="utf-8")
print("Successfully updated web portal with official logo, episode menu items, and master episodic breakdowns!")
