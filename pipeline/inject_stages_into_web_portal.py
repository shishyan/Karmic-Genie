import re
from pathlib import Path

html_file = Path("/home/antigravity/shishyan/Karmic-Genie-Show/docs/index.html")
content = html_file.read_text(encoding="utf-8")

# 1. Update navigation in sidebar to add Stages
nav_target = '<a class="nav-link" onclick="switchView(\'view-pipeline\')"><span>📽️</span> Film & Animation Production Audit</a>'
nav_replacement = '''<a class="nav-link" onclick="switchView('view-pipeline')"><span>📽️</span> Film & Animation Production Audit</a>
      <a class="nav-link" onclick="switchView('view-stages')"><span>🏟️</span> The 7 Sacred Stages & Stadiums</a>'''

content = content.replace(nav_target, nav_replacement)

# 2. Add Stages View Panel after view-pipeline
stages_section = '''
      <!-- VIEW: THE 7 SACRED STAGES & STADIUMS -->
      <section id="view-stages" class="view-panel">
        <div class="banner-hero">
          <div class="siddha-mantra">அண்டத்தில் உள்ளதே பிண்டம் • As in the Microcosm, So in the Macrocosm</div>
          <h2>The 7 Sacred Broadcast Stages & Stadiums</h2>
          <p>
            Designed for <b>YouTube Full-Length 4K Episodes (16:9)</b> and <b>YouTube Shorts (9:16)</b>. 
            Depending on the topic, vibrational frequency, and emotional mood of the episode, the show transitions between 
            7 magnificent architectural environments rooted in primal nature elements and human physiological systems.
          </p>
        </div>

        <!-- Stage Filter Buttons -->
        <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:1.5rem;">
          <button class="topbar-btn active-stage-btn" onclick="filterStages('ALL')" style="font-weight:700;">All 7 Stages</button>
          <button class="topbar-btn" onclick="filterStages('1')">Stage 1: Mountain Sanctuary</button>
          <button class="topbar-btn" onclick="filterStages('2')">Stage 2: Root Canyon</button>
          <button class="topbar-btn" onclick="filterStages('3')">Stage 3: Living Waterfall</button>
          <button class="topbar-btn" onclick="filterStages('4')">Stage 4: Solar Caldera</button>
          <button class="topbar-btn" onclick="filterStages('5')">Stage 5: Canopy Atrium</button>
          <button class="topbar-btn" onclick="filterStages('6')">Stage 6: Crystalline Cavern</button>
          <button class="topbar-btn" onclick="filterStages('7')">Stage 7: Cosmic Observatory</button>
        </div>

        <!-- 7 Stages Cards Grid -->
        <div class="episodes-grid" id="stages-grid-container" style="grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));">
        </div>
      </section>
'''

content = content.replace('<!-- VIEW 4: CORPORATE RATINGS -->', stages_section + '\n      <!-- VIEW 4: CORPORATE RATINGS -->')

# 3. Update titles dictionary in javascript
titles_target = "'view-pipeline': 'Film & Animation Production Audit',"
titles_replacement = """'view-pipeline': 'Film & Animation Production Audit',
        'view-stages': 'The 7 Sacred Stages & Stadiums',"""
content = content.replace(titles_target, titles_replacement)

# 4. Inject stages data and render function in javascript
stages_injection = '''
    const stagesData = [
      {
        "id": "1",
        "name": "The Nilgiri Sacred Mountain Sanctuary",
        "element": "Ancient Earth & Mountain Canopy",
        "organ": "Central Nervous Axis & Spine",
        "vibe": "Sacred, Timeless, Grounded Dawn Light",
        "desc": "An open sandalwood and granite rotunda in the high Nilgiri shola forests. Used for foundational series declarations, Vedic time laws, and sacred Tamil Siddha principles.",
        "episodes": "S01E00 Pilot, S01E01 The Way Forward",
        "img16x9": "assets/stages_7d/stage1_nilgiri_sanctuary_16x9.jpg",
        "img9x16": "assets/stages_7d/stage1_nilgiri_sanctuary_9x16.jpg"
      },
      {
        "id": "2",
        "name": "The Subterranean Living Root Canyon",
        "element": "Deep Soil, Mycelium & Ancient Taproots",
        "organ": "Skeletal Marrow, Solvency Roots & Mineral Gut",
        "vibe": "Deep Bronze & Amber, Earthen Solvency, Anchoring Warmth",
        "desc": "Subterranean earthen amphitheater arched by glowing banyan taproots and amber geodes. Used for Level 1–2 corporate survival, financial solvency, balance sheets, and agriculture plumbing.",
        "episodes": "Corporate Survival & Root Architecture",
        "img16x9": "assets/stages_7d/stage2_root_canyon_16x9.jpg",
        "img9x16": "assets/stages_7d/stage2_root_canyon_9x16.jpg"
      },
      {
        "id": "3",
        "name": "The Cascading River & Living Waterfall Stage",
        "element": "Freshwater Springs, Glacial Brooks & Basalt Rapids",
        "organ": "Heart, Blood Vessels & Circulatory Pacing",
        "vibe": "Fresh, Invigorating, Cyan & Turquoise Rhythmic Flow",
        "desc": "Built into a sheer basalt river gorge with live waterfalls pouring into reflecting streams around an island dais. Used for global supply chain logistics, maritime shipping, and ERP circulation.",
        "episodes": "S01E06 Unified ERP Platform & Resource Circulation",
        "img16x9": "assets/stages_7d/stage3_living_waterfall_16x9.jpg",
        "img9x16": "assets/stages_7d/stage3_living_waterfall_9x16.jpg"
      },
      {
        "id": "4",
        "name": "The Solar Caldera Summit Amphitheater",
        "element": "Volcanic Sunlight, Thermal Plasma & Radiant Auroras",
        "organ": "Liver, Mitochondria & Energy Metabolism",
        "vibe": "Bold, Radiant Golden Hour, High-Power Fusion",
        "desc": "Open-air futuristic geodesic dome crowning a sunlit volcanic caldera with brass sundials and thermal plasma conduits. Used for clean energy grids, solar fusion breakthroughs, and industrial power.",
        "episodes": "S01E02 & S01E04 Energy Transitions & Power Grids",
        "img16x9": "assets/stages_7d/stage4_solar_summit_16x9.jpg",
        "img9x16": "assets/stages_7d/stage4_solar_summit_9x16.jpg"
      },
      {
        "id": "5",
        "name": "The Cloud Rainforest Canopy Atrium",
        "element": "Misty Cloud Forests, Tree Crowns & Orchid Blooms",
        "organ": "Lungs, Alveoli, Respiration & Oxygenated Prana",
        "vibe": "Light, Breezy, Fresh Emerald Jade, Botanical Fragrance",
        "desc": "Suspended curved glass pavilion amidst misty mountain treetops with blooming jasmine and live moss acoustic baffles. Used for Level 4–5 Leaf delight, humane workplace dignity, and developer tools.",
        "episodes": "Workplace Culture, Community Breathing Room & UX",
        "img16x9": "assets/stages_7d/stage5_canopy_atrium_16x9.jpg",
        "img9x16": "assets/stages_7d/stage5_canopy_atrium_9x16.jpg"
      },
      {
        "id": "6",
        "name": "The Crystalline Amethyst & Quartz Geode Cavern",
        "element": "Subterranean Prismatic Geodes & Neural Fibers",
        "organ": "Brain Cortex, Neural Synapses & Subconscious Mind",
        "vibe": "Deep Indigo & Sapphire, Prismatic Violet, Transcendent Clarity",
        "desc": "Vaulted amethyst geode cavern with floating glass dais and glowing overhead neural synapse light sculptures. Used for foundational AI reasoning models, neural platforms, and 7D conscience audits.",
        "episodes": "S01E05 Unified AI Platform & Synthetic Intelligence",
        "img16x9": "assets/stages_7d/stage6_crystal_cavern_16x9.jpg",
        "img9x16": "assets/stages_7d/stage6_crystal_cavern_9x16.jpg"
      },
      {
        "id": "7",
        "name": "The Cosmic Horizon Observatory (Moksha Stage)",
        "element": "Himalayan Summit, Earth Limb Curvature & Milky Way",
        "organ": "Crown Sahasrara, Sovereign Soul & Generative Moksha",
        "vibe": "Infinite, Silent Reverence, Sacred Golden Abhaya Blessing",
        "desc": "Perched on a high Himalayan peak looking out over Earth's blue curve and deep cosmos, with white marble lotus stage and glowing Abhaya Mudra. Used for public goods, open seed legacy, and 2050 Living Household.",
        "episodes": "Level 7 Moksha Seed Liberation & Grand Finales",
        "img16x9": "assets/stages_7d/stage7_cosmic_observatory_16x9.jpg",
        "img9x16": "assets/stages_7d/stage7_cosmic_observatory_9x16.jpg"
      }
    ];

    function renderStages(filterId = 'ALL') {
      const container = document.getElementById('stages-grid-container');
      if (!container) return;
      const list = filterId === 'ALL' ? stagesData : stagesData.filter(s => s.id === filterId);
      container.innerHTML = list.map(st => `
        <div class="episode-card">
          <div style="position:relative;">
            <img src="${st.img16x9}" alt="${st.name}" style="height:230px;" />
            <div style="position:absolute; top:10px; right:10px; display:flex; gap:0.4rem;">
              <span class="badge" style="background:rgba(15,23,42,0.85); color:#fff; font-size:0.7rem; backdrop-filter:blur(4px);">4K 16:9 Ep</span>
              <span class="badge" style="background:rgba(225,29,72,0.85); color:#fff; font-size:0.7rem; backdrop-filter:blur(4px);">9:16 Shorts</span>
            </div>
          </div>
          <div class="episode-body">
            <span class="ep-tag">Stage ${st.id} • ${st.element}</span>
            <div class="ep-title">${st.name}</div>
            <div class="ep-sub"><b>Organ:</b> ${st.organ}</div>
            <div class="ep-cast-box" style="margin-bottom:0.75rem;">
              <b>Atmospheric Vibe:</b> ${st.vibe}<br>
              <b>Topic Resonances:</b> ${st.episodes}
            </div>
            <p style="font-size:0.85rem; color:#475569; line-height:1.5;">${st.desc}</p>
          </div>
          <div class="ep-footer">
            <a href="${st.img16x9}" target="_blank" class="topbar-btn" style="font-size:0.75rem;">View 16:9 Studio</a>
            <a href="${st.img9x16}" target="_blank" class="btn-action" style="font-size:0.75rem;">View 9:16 Shorts Set</a>
          </div>
        </div>
      `).join('');
    }

    function filterStages(id) {
      document.querySelectorAll('#view-stages .topbar-btn').forEach(b => b.classList.remove('active-stage-btn'));
      event.target.classList.add('active-stage-btn');
      renderStages(id);
    }
'''

content = content.replace('function renderEpisodes() {', stages_injection + '\n    function renderEpisodes() {')

# 5. Call renderStages in window.onload
content = content.replace('renderShotLedger();', 'renderShotLedger();\n      renderStages();')

html_file.write_text(content, encoding="utf-8")
print("Successfully injected The 7 Sacred Stages & Stadiums into index.html!")
