import json

def build_light_app():
    with open('/home/antigravity/shishyan/Karmic-Genie-Show/app/companies_data.json') as f:
        companies_raw = f.read()

    with open('/home/antigravity/shishyan/Karmic-Genie-Show/app/episodes_data.json') as f:
        episodes_raw = f.read()

    template = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#edf7f3">
  <meta name="description" content="The Karmic Genie Show — Master Production & Telemetry Portal (The Way Forward)">
  <title>Karmic Genie • The Way Forward</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Cinzel:wght@600;700;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #edf7f3;
      --card-bg: #ffffff;
      --sidebar-bg: #f4fbf8;
      --sidebar-border: #d4e8df;
      --primary: #0f766e;
      --primary-light: #ccfbf1;
      --accent: #f59e0b;
      --text: #1e293b;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --radius: 12px;
      --font-main: 'Manrope', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-title: 'Cinzel', serif;
      --font-mono: 'Fira Code', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-main);
      display: flex;
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* Sidebar - Matching Home Manager / Divine Nest layout */
    #sidebar {
      width: 270px;
      background: var(--sidebar-bg);
      border-right: 1px solid var(--sidebar-border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      height: 100vh;
      position: sticky;
      top: 0;
      padding: 1.5rem 1rem;
      transition: all 0.3s ease;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.85rem;
      padding-bottom: 1.5rem;
      border-bottom: 1px solid var(--sidebar-border);
      margin-bottom: 1.5rem;
    }

    .brand-mark {
      width: 40px;
      height: 40px;
      background: linear-gradient(135deg, var(--primary), var(--accent));
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-size: 1.25rem;
      font-weight: 800;
      box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25);
    }

    .brand-copy b {
      font-size: 1.05rem;
      display: block;
      color: var(--primary);
      font-weight: 800;
      line-height: 1.2;
    }

    .brand-copy small {
      font-size: 0.75rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    nav {
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      flex-grow: 1;
    }

    .nav-link {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.65rem 0.85rem;
      color: var(--text-muted);
      border-radius: 8px;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s ease;
    }

    .nav-link:hover {
      background: rgba(15, 118, 110, 0.08);
      color: var(--primary);
    }

    .nav-link.active {
      background: var(--primary);
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(15, 118, 110, 0.25);
    }

    .sidebar-footer {
      padding-top: 1rem;
      border-top: 1px solid var(--sidebar-border);
      font-size: 0.78rem;
      color: var(--text-muted);
      text-align: center;
    }

    /* Main App Shell */
    .app-shell {
      flex-grow: 1;
      display: flex;
      flex-direction: column;
      min-width: 0;
      overflow-y: auto;
    }

    header.app-header {
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 50;
    }

    .topbar-left {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .topbar-left h1 {
      font-size: 1.35rem;
      font-weight: 800;
      color: var(--text);
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .topbar-quick-link {
      padding: 0.45rem 0.85rem;
      border-radius: 8px;
      background: var(--bg);
      border: 1px solid var(--sidebar-border);
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--primary);
      text-decoration: none;
      transition: all 0.2s;
    }

    .topbar-quick-link:hover {
      background: var(--primary);
      color: #fff;
    }

    main#content {
      padding: 2rem;
      max-width: 1400px;
      margin: 0 auto;
      width: 100%;
    }

    /* Cards & Grids */
    .hero-box {
      background: #ffffff;
      border: 1px solid var(--sidebar-border);
      border-radius: var(--radius);
      padding: 2rem;
      margin-bottom: 2rem;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    }

    .siddha-badge {
      display: inline-block;
      background: var(--primary-light);
      color: var(--primary);
      padding: 0.35rem 0.85rem;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 700;
      margin-bottom: 0.75rem;
    }

    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2rem;
    }

    .kpi-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.25rem;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    .kpi-title {
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 0.35rem;
    }

    .kpi-value {
      font-size: 1.75rem;
      font-weight: 800;
      color: var(--primary);
    }

    .kpi-sub {
      font-size: 0.8rem;
      color: #059669;
      margin-top: 0.25rem;
      font-weight: 600;
    }

    /* Views */
    .view-panel { display: none; }
    .view-panel.active { display: block; animation: fadeIn 0.25s ease; }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Episodes Cards */
    .grid-cards {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 1.25rem;
    }

    .clean-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s ease;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    .clean-card:hover {
      border-color: var(--primary);
      box-shadow: 0 6px 16px rgba(15, 118, 110, 0.08);
      transform: translateY(-2px);
    }

    .badge-pill {
      display: inline-block;
      padding: 0.25rem 0.65rem;
      border-radius: 12px;
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
    }

    .b-7 { background: #dcfce7; color: #15803d; }
    .b-6 { background: #e0f2fe; color: #0369a1; }
    .b-5 { background: #fef3c7; color: #b45309; }
    .b-4 { background: #f3e8ff; color: #7e22ce; }
    .b-3 { background: #f1f5f9; color: #475569; }

    /* Tables */
    .table-container {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow-x: auto;
    }

    table.clean-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.88rem;
    }

    table.clean-table th {
      background: #f8fafc;
      padding: 0.85rem 1rem;
      font-weight: 700;
      color: var(--text-muted);
      border-bottom: 1px solid var(--border);
    }

    table.clean-table td {
      padding: 0.85rem 1rem;
      border-bottom: 1px solid #f1f5f9;
    }

    /* Slider Calc */
    .calc-slider-card {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 2rem;
      max-width: 800px;
      margin: 0 auto;
    }

    .slider-row {
      margin-bottom: 1.25rem;
    }

    .slider-head {
      display: flex;
      justify-content: space-between;
      font-size: 0.9rem;
      font-weight: 700;
      margin-bottom: 0.35rem;
    }

    input[type=range] {
      width: 100%;
      accent-color: var(--primary);
    }

    /* Responsive */
    @media (max-width: 850px) {
      body { flex-direction: column; }
      #sidebar { width: 100%; height: auto; position: static; }
    }
  </style>
</head>
<body>

  <!-- Sidebar -->
  <aside id="sidebar">
    <div class="brand">
      <div class="brand-mark">🪔</div>
      <div class="brand-copy">
        <b>Karmic Genie</b>
        <small>The Way Forward</small>
      </div>
    </div>

    <nav>
      <a class="nav-link active" onclick="switchView('view-overview')"><span>📊</span> Dashboard</a>
      <a class="nav-link" onclick="switchView('view-episodes')"><span>🎬</span> Episodes Hub</a>
      <a class="nav-link" onclick="switchView('view-ratings')"><span>🌳</span> Corporate Ratings</a>
      <a class="nav-link" onclick="switchView('view-matrix')"><span>🧬</span> 7×7 Industry Matrix</a>
      <a class="nav-link" onclick="switchView('view-compass')"><span>⚖️</span> 7D Life Compass</a>
    </nav>

    <div class="sidebar-footer">
      <b>genie.shishyan.in</b><br>
      Pitru Loka Chronometry Clock<br>
      © 2026 Shishyan
    </div>
  </aside>

  <!-- App Shell -->
  <div class="app-shell">
    <header class="app-header">
      <div class="topbar-left">
        <h1 id="headerTitle">Dashboard & Telemetry</h1>
      </div>
      <div class="header-actions">
        <a href="https://extensions.shishyan.in" class="topbar-quick-link" target="_blank">Extensions</a>
        <a href="https://exams.shishyan.in" class="topbar-quick-link" target="_blank">Certifications</a>
        <a href="https://guru.shishyan.in" class="topbar-quick-link" target="_blank">Guru Kula Desam</a>
        <a href="https://github.com/shishyan/Karmic-Genie-Show" class="topbar-quick-link" target="_blank">GitHub</a>
      </div>
    </header>

    <main id="content">

      <!-- VIEW 1: OVERVIEW -->
      <section id="view-overview" class="view-panel active">
        <div class="hero-box">
          <div class="siddha-badge">அண்டத்தில் உள்ளதே பிண்டம் • அண்டமும் பிண்டமும் ஒன்றே</div>
          <h2 style="font-size:1.8rem; font-weight:800; color:var(--primary); margin-bottom:0.5rem;">The Living Planetary Organism</h2>
          <p style="color:var(--text-muted); font-size:1rem; line-height:1.6;">
            As in the Macrocosm (Andam), so in the Microcosm (Pindam). Tracking civilization's 280-month embryological gestation 
            under the sacred Pitru Loka clock cycle (1 Embryo Day = 1 Pitru Day = 1 Earth Month).
          </p>
        </div>

        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-title">Current Epoch</div>
            <div class="kpi-value">Month 48</div>
            <div class="kpi-sub">Week 7: Primitive Heart Pumping!</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-title">Insemination Spark</div>
            <div class="kpi-value">Dec 1, 2022</div>
            <div class="kpi-sub">ChatGPT Public Insemination</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-title">Sovereign Delivery</div>
            <div class="kpi-value">Apr 2046</div>
            <div class="kpi-sub">Day 280 / Birth of Living Gaia</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-title">The Living Household</div>
            <div class="kpi-value">2050</div>
            <div class="kpi-sub">Unified Planet Platform (Free to All)</div>
          </div>
        </div>

        <div class="hero-box">
          <h3 style="margin-bottom:1rem; color:var(--text);">Embryological Gestation Progress: 17.1% (Month 48 / 280)</h3>
          <div style="background:#e2e8f0; height:12px; border-radius:6px; overflow:hidden; margin-bottom:1rem;">
            <div style="width:17.14%; height:100%; background:linear-gradient(90deg, var(--primary), var(--accent));"></div>
          </div>
          <div style="display:flex; justify-content:space-between; font-size:0.82rem; color:var(--text-muted);">
            <span>Dec 2022 (Conception)</span>
            <span style="font-weight:700; color:var(--primary);">Nov 2026 (Heart Beats)</span>
            <span>2028 (Unified AI)</span>
            <span>2029 (Unified ERP)</span>
            <span>2030 (Energy)</span>
            <span>Apr 2046 (Birth)</span>
            <span>2050 (Household)</span>
          </div>
        </div>
      </section>

      <!-- VIEW 2: EPISODES -->
      <section id="view-episodes" class="view-panel">
        <h2 style="font-size:1.6rem; font-weight:800; color:var(--primary); margin-bottom:1.5rem;">Master Episodes Vault</h2>
        <div class="grid-cards" id="episodes-list"></div>
      </section>

      <!-- VIEW 3: CORPORATE RATINGS -->
      <section id="view-ratings" class="view-panel">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem; flex-wrap:wrap; gap:1rem;">
          <h2 style="font-size:1.6rem; font-weight:800; color:var(--primary);">Kalpavriksha Corporate Ratings (1 to 7)</h2>
          <div style="display:flex; gap:0.5rem;">
            <input type="text" id="light-search" placeholder="Search company..." oninput="renderLightCompanies()" style="padding:0.45rem 0.85rem; border:1px solid var(--border); border-radius:8px; font-size:0.88rem;">
            <select id="light-filter" onchange="renderLightCompanies()" style="padding:0.45rem 0.85rem; border:1px solid var(--border); border-radius:8px; font-size:0.88rem;">
              <option value="ALL">All Levels</option>
              <option value="7">Stage 7: Moksha (Liberation)</option>
              <option value="6">Stage 6: Kani (Fruit-Bearing)</option>
              <option value="5">Stage 5: Malar (Flowering)</option>
              <option value="4">Stage 4: Ilai (Leaves)</option>
              <option value="3">Stage 3: Thandu (Trunk)</option>
            </select>
          </div>
        </div>
        <div class="grid-cards" id="companies-list"></div>
      </section>

      <!-- VIEW 4: MATRIX -->
      <section id="view-matrix" class="view-panel">
        <h2 style="font-size:1.6rem; font-weight:800; color:var(--primary); margin-bottom:1.5rem;">The Grounded 7×7 Fractal Matrix</h2>
        <div class="table-container">
          <table class="clean-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Human Organ System (Pindam)</th>
                <th>Existing Modern Industry (Andam)</th>
                <th>7 Real-World Concrete Sub-Sectors</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><b>1</b></td>
                <td><b>Brain & Nerves</b></td>
                <td style="color:var(--primary); font-weight:700;">IT & Telecommunications</td>
                <td>Semiconductors, Telecom & Fiber, Cloud Data Centers, AI Models, Consumer OS/Hardware, Cybersecurity, Open Repositories</td>
              </tr>
              <tr>
                <td><b>2</b></td>
                <td><b>Heart & Circulation</b></td>
                <td style="color:var(--primary); font-weight:700;">Logistics & Supply Chain</td>
                <td>Maritime Ocean Freight, Air Cargo Express, Rail Intermodal, Trucking Fleet Haulage, Warehousing Last-Mile, ERP Flow, Wholesale Distribution</td>
              </tr>
              <tr>
                <td><b>3</b></td>
                <td><b>Lungs & Respiration</b></td>
                <td style="color:var(--primary); font-weight:700;">Energy & Utilities</td>
                <td>Renewable Power (Wind/Solar), Transmission Grids, Battery Storage, Air Quality Scrubbing, Industrial Gases, Clean Hydrogen, Forest Canopies</td>
              </tr>
              <tr>
                <td><b>4</b></td>
                <td><b>Stomach & Digestion</b></td>
                <td style="color:var(--primary); font-weight:700;">Agriculture, Food & Waste</td>
                <td>Crop Farming Machinery, Seeds & Fertilizers, Packaged Nutrition, Livestock Protein, Municipal Solid Waste, Composting & Bioremediation, Cold-Chain Grocery</td>
              </tr>
              <tr>
                <td><b>5</b></td>
                <td><b>Endocrine Glands</b></td>
                <td style="color:var(--primary); font-weight:700;">Banking & Finance</td>
                <td>Central Bank Settlement Rails, Commercial Deposit Banking, Card Clearing Networks, Asset Management, Insurance Underwriting, Securities Exchanges, Microfinance</td>
              </tr>
              <tr>
                <td><b>6</b></td>
                <td><b>Skeletal & Muscles</b></td>
                <td style="color:var(--primary); font-weight:700;">Construction & Heavy Manufacturing</td>
                <td>Earthmoving Machinery, Steel & Cement, Civil Engineering Contractors, Automotive Transit, Industrial Robotics, Aerospace/Marine, Rail Transit</td>
              </tr>
              <tr>
                <td><b>7</b></td>
                <td><b>Skin & Immune/Renal</b></td>
                <td style="color:var(--primary); font-weight:700;">Healthcare & Sanitation</td>
                <td>Municipal Potable Water, Therapeutic Pharmaceuticals, Medical Devices, Hospital Care Networks, Genomics Precision Biotech, Disease Control, Earth Observation</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- VIEW 5: COMPASS -->
      <section id="view-compass" class="view-panel">
        <h2 style="font-size:1.6rem; font-weight:800; color:var(--primary); text-align:center; margin-bottom:0.5rem;">7D Conscience Self-Audit</h2>
        <p style="text-align:center; color:var(--text-muted); margin-bottom:2rem;">The Universal Threshold Law: &lt; 35 / 70 Points = Change Course Immediately.</p>

        <div class="calc-slider-card">
          <div class="slider-row">
            <div class="slider-head"><span>1. Respect Your DUTY First</span><span id="lv-1" style="color:var(--primary);">7 / 10</span></div>
            <input type="range" min="1" max="10" value="7" id="s-1" oninput="calcLight7D()">
          </div>
          <div class="slider-row">
            <div class="slider-head"><span>2. Earn with DIGNITY Always</span><span id="lv-2" style="color:var(--primary);">8 / 10</span></div>
            <input type="range" min="1" max="10" value="8" id="s-2" oninput="calcLight7D()">
          </div>
          <div class="slider-row">
            <div class="slider-head"><span>3. Practice Life DISCIPLINE</span><span id="lv-3" style="color:var(--primary);">7 / 10</span></div>
            <input type="range" min="1" max="10" value="7" id="s-3" oninput="calcLight7D()">
          </div>
          <div class="slider-row">
            <div class="slider-head"><span>4. Uphold Karmic DHARMA</span><span id="lv-4" style="color:var(--primary);">9 / 10</span></div>
            <input type="range" min="1" max="10" value="9" id="s-4" oninput="calcLight7D()">
          </div>
          <div class="slider-row">
            <div class="slider-head"><span>5. Raise Family with DEVOTION</span><span id="lv-5" style="color:var(--primary);">8 / 10</span></div>
            <input type="range" min="1" max="10" value="8" id="s-5" oninput="calcLight7D()">
          </div>
          <div class="slider-row">
            <div class="slider-head"><span>6. Be Grateful to Your DIVINE</span><span id="lv-6" style="color:var(--primary);">9 / 10</span></div>
            <input type="range" min="1" max="10" value="9" id="s-6" oninput="calcLight7D()">
          </div>
          <div class="slider-row">
            <div class="slider-head"><span>7. Purposeful Life Is Your DESTINY</span><span id="lv-7" style="color:var(--primary);">8 / 10</span></div>
            <input type="range" min="1" max="10" value="8" id="s-7" oninput="calcLight7D()">
          </div>

          <div style="background:#f8fafc; border:1px solid var(--border); border-radius:10px; padding:1.5rem; text-align:center; margin-top:2rem;">
            <div style="font-size:0.8rem; text-transform:uppercase; color:var(--text-muted);">Total 7D Life Compass Score</div>
            <div style="font-size:2.5rem; font-weight:800; color:var(--primary);" id="light-total">56 / 70</div>
            <div id="light-status" style="font-weight:700; color:#059669; margin-top:0.35rem;">🌟 GOLD ZONE: Pioneer of the New World</div>
          </div>
        </div>
      </section>

    </main>
  </div>

  <script>
    const companies = __COMPANIES_JSON__;
    const episodes = __EPISODES_JSON__;

    function switchView(viewId) {
      document.querySelectorAll('.view-panel').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));

      const target = document.getElementById(viewId);
      if (target) target.classList.add('active');

      const links = Array.from(document.querySelectorAll('.nav-link'));
      const activeLink = links.find(l => l.getAttribute('onclick') && l.getAttribute('onclick').includes(viewId));
      if (activeLink) activeLink.classList.add('active');

      const titles = {
        'view-overview': 'Dashboard & Telemetry',
        'view-episodes': 'Master Episodes Vault',
        'view-ratings': 'Corporate Consciousness Ratings',
        'view-matrix': '7×7 Fractal Matrix',
        'view-compass': '7D Conscience Audit'
      };
      document.getElementById('headerTitle').innerText = titles[viewId] || 'Command Center';
    }

    function renderLightEpisodes() {
      const container = document.getElementById('episodes-list');
      container.innerHTML = episodes.map(ep => `
        <div class="clean-card">
          <div>
            <span style="font-size:0.75rem; font-weight:800; color:var(--primary); text-transform:uppercase;">${ep.id} • ${ep.duration}</span>
            <h3 style="font-size:1.15rem; font-weight:800; margin:0.35rem 0;">${ep.title}</h3>
            <p style="font-size:0.82rem; color:var(--text-muted); margin-bottom:0.75rem;">${ep.subtitle}</p>
            <div style="background:#f8fafc; padding:0.6rem; border-radius:6px; font-size:0.78rem; margin-bottom:0.75rem;">
              <b>Cast:</b> ${ep.cast.join(' • ')}
            </div>
            <p style="font-size:0.85rem; color:#475569; line-height:1.5;">${ep.core_concept}</p>
          </div>
          <div style="margin-top:1.25rem; padding-top:0.75rem; border-top:1px solid #f1f5f9; display:flex; justify-content:space-between; align-items:center;">
            <small style="color:var(--text-muted); font-family:var(--font-mono); font-size:0.75rem;">${ep.script_file}</small>
            <a href="#" class="topbar-quick-link" onclick="alert('Script is in repository at:\\n' + '${ep.script_file}'); return false;">View</a>
          </div>
        </div>
      `).join('');
    }

    function renderLightCompanies() {
      const q = document.getElementById('light-search').value.toLowerCase();
      const lvl = document.getElementById('light-filter').value;

      const filtered = companies.filter(c => {
        const matchesQ = c.name.toLowerCase().includes(q) || c.subsector.toLowerCase().includes(q) || c.organ.toLowerCase().includes(q);
        const matchesL = (lvl === 'ALL') || (c.score === parseInt(lvl));
        return matchesQ && matchesL;
      });

      const container = document.getElementById('companies-list');
      container.innerHTML = filtered.map(c => `
        <div class="clean-card">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="font-size:1.1rem; font-weight:800;">${c.name}</h3>
              <span class="badge-pill b-${c.score}">${c.stage_label}</span>
            </div>
            <div style="font-size:0.78rem; color:var(--primary); font-weight:700; margin-bottom:0.5rem;">${c.organ} → ${c.subsector}</div>
            <p style="font-size:0.82rem; color:#64748b; margin-bottom:1rem; line-height:1.5;">${c.description}</p>
          </div>
          <div style="background:#f8fafc; border:1px solid var(--border); border-radius:8px; padding:0.75rem; font-size:0.78rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
              <b>Stage ${c.score} of 7</b>
              <span style="color:var(--primary); font-weight:700;">${Math.round((c.score/7)*100)}%</span>
            </div>
            <div style="height:6px; background:#e2e8f0; border-radius:3px; overflow:hidden; margin-bottom:0.5rem;">
              <div style="width:${(c.score/7)*100}%; height:100%; background:var(--primary);"></div>
            </div>
            <div style="color:#334155;"><b>Seed Legacy:</b> ${c.seed}</div>
          </div>
        </div>
      `).join('');
    }

    function calcLight7D() {
      let sum = 0;
      for (let i = 1; i <= 7; i++) {
        const val = parseInt(document.getElementById('s-' + i).value);
        document.getElementById('lv-' + i).innerText = val + ' / 10';
        sum += val;
      }
      document.getElementById('light-total').innerText = sum + ' / 70';
      const st = document.getElementById('light-status');
      if (sum < 35) {
        st.innerText = '⚠️ RED ZONE: Conscience Silenced — Change Course!';
        st.style.color = '#dc2626';
      } else if (sum <= 49) {
        st.innerText = '⚡ AMBER ZONE: Awakening Traveler — Realign Neglected Virtues';
        st.style.color = '#d97706';
      } else {
        st.innerText = '🌟 GOLD ZONE: Pioneer of the New World — Sovereign Harmony';
        st.style.color = '#059669';
      }
    }

    window.onload = function() {
      renderLightEpisodes();
      renderLightCompanies();
      calcLight7D();
    };
  </script>
</body>
</html>
"""
    output = template.replace('__COMPANIES_JSON__', companies_raw).replace('__EPISODES_JSON__', episodes_raw)
    with open('/home/antigravity/shishyan/Karmic-Genie-Show/docs/light.html', 'w') as out_f:
        out_f.write(output)
    with open('/home/antigravity/shishyan/Karmic-Genie-Show/app/light.html', 'w') as out_f:
        out_f.write(output)
    print("Successfully built light version at docs/light.html and app/light.html! Size:", len(output))

if __name__ == '__main__':
    build_light_app()
