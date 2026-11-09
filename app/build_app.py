import json

def build_app():
    with open('/home/antigravity/shishyan/Karmic-Genie-Show/app/companies_data.json') as f:
        companies_raw = f.read()

    with open('/home/antigravity/shishyan/Karmic-Genie-Show/app/episodes_data.json') as f:
        episodes_raw = f.read()

    template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>The Karmic Genie Show — Master Production & Telemetry Portal</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #07090e;
      --card-bg: rgba(16, 21, 34, 0.75);
      --card-border: rgba(255, 215, 0, 0.15);
      --gold-primary: #f5b041;
      --gold-glow: rgba(245, 176, 65, 0.4);
      --cyan-bright: #38ef7d;
      --accent-blue: #4facfe;
      --text-main: #f0f4f8;
      --text-muted: #94a3b8;
      --font-title: 'Cinzel', serif;
      --font-body: 'Plus Jakarta Sans', sans-serif;
      --font-mono: 'Fira Code', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(circle at 10% 20%, rgba(245, 176, 65, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(79, 172, 254, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(18, 24, 38, 0.6) 0%, transparent 100%);
      color: var(--text-main);
      font-family: var(--font-body);
      min-height: 100vh;
      overflow-x: hidden;
      line-height: 1.6;
    }

    /* Header Nav */
    header {
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(16px);
      background: rgba(7, 9, 14, 0.85);
      border-bottom: 1px solid var(--card-border);
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .brand-logo {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      border: 2px solid var(--gold-primary);
      box-shadow: 0 0 15px var(--gold-glow);
      object-fit: cover;
    }

    .brand-title {
      font-family: var(--font-title);
      font-size: 1.35rem;
      font-weight: 700;
      letter-spacing: 1px;
      color: #fff;
    }

    .brand-title span {
      color: var(--gold-primary);
    }

    .nav-tabs {
      display: flex;
      gap: 0.5rem;
      background: rgba(255, 255, 255, 0.05);
      padding: 0.35rem;
      border-radius: 50px;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .nav-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 0.5rem 1.25rem;
      border-radius: 30px;
      font-weight: 600;
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.3s ease;
      font-family: var(--font-body);
    }

    .nav-btn:hover {
      color: #fff;
    }

    .nav-btn.active {
      background: linear-gradient(135deg, var(--gold-primary), #e67e22);
      color: #000;
      box-shadow: 0 0 12px var(--gold-glow);
    }

    /* Container & Sections */
    .container {
      max-width: 1400px;
      margin: 2rem auto;
      padding: 0 1.5rem 4rem;
    }

    .tab-content {
      display: none;
      animation: fadeIn 0.4s ease;
    }

    .tab-content.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Banner Card */
    .hero-banner {
      background: linear-gradient(135deg, rgba(245, 176, 65, 0.12), rgba(79, 172, 254, 0.08));
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 2.5rem;
      margin-bottom: 2rem;
      position: relative;
      overflow: hidden;
    }

    .hero-sanskrit {
      font-family: var(--font-title);
      font-size: 1.6rem;
      color: var(--gold-primary);
      margin-bottom: 0.5rem;
      text-shadow: 0 0 15px rgba(245, 176, 65, 0.4);
    }

    .hero-title {
      font-family: var(--font-title);
      font-size: 2.4rem;
      font-weight: 800;
      margin-bottom: 0.75rem;
    }

    .hero-desc {
      color: var(--text-muted);
      max-width: 850px;
      font-size: 1.05rem;
    }

    /* Stats Grid */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2rem;
    }

    .stat-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 1.5rem;
      position: relative;
      transition: transform 0.3s ease;
    }

    .stat-card:hover {
      transform: translateY(-4px);
    }

    .stat-label {
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--text-muted);
      margin-bottom: 0.4rem;
    }

    .stat-value {
      font-size: 1.8rem;
      font-weight: 800;
      color: #fff;
      font-family: var(--font-title);
    }

    .stat-sub {
      font-size: 0.85rem;
      color: var(--cyan-bright);
      margin-top: 0.25rem;
    }

    /* Chronometer Clock Bar */
    .clock-container {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 2rem;
      margin-bottom: 2.5rem;
    }

    .clock-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
    }

    .clock-title {
      font-family: var(--font-title);
      font-size: 1.25rem;
      color: var(--gold-primary);
    }

    .progress-bar-bg {
      background: rgba(255, 255, 255, 0.08);
      height: 18px;
      border-radius: 9px;
      overflow: hidden;
      position: relative;
      border: 1px solid rgba(255, 255, 255, 0.15);
      margin-bottom: 1rem;
    }

    .progress-fill {
      background: linear-gradient(90deg, #f5b041, #38ef7d, #4facfe);
      height: 100%;
      border-radius: 9px;
      box-shadow: 0 0 15px rgba(245, 176, 65, 0.5);
      transition: width 1s ease;
    }

    .timeline-points {
      display: flex;
      justify-content: space-between;
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    .timeline-active {
      color: var(--cyan-bright);
      font-weight: 700;
    }

    /* Episodes Grid */
    .episodes-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
      gap: 1.5rem;
    }

    .episode-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 1.75rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.3s ease;
    }

    .episode-card:hover {
      border-color: var(--gold-primary);
      box-shadow: 0 8px 24px rgba(245, 176, 65, 0.15);
      transform: translateY(-4px);
    }

    .ep-tag {
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--gold-primary);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 0.5rem;
    }

    .ep-title {
      font-family: var(--font-title);
      font-size: 1.35rem;
      font-weight: 700;
      color: #fff;
      margin-bottom: 0.35rem;
    }

    .ep-subtitle {
      font-size: 0.9rem;
      color: var(--text-muted);
      margin-bottom: 1rem;
    }

    .ep-cast {
      background: rgba(0, 0, 0, 0.3);
      padding: 0.75rem;
      border-radius: 8px;
      font-size: 0.82rem;
      color: #cbd5e1;
      margin-bottom: 1rem;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .ep-desc {
      font-size: 0.9rem;
      color: #94a3b8;
      margin-bottom: 1.25rem;
      flex-grow: 1;
    }

    .ep-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 1rem;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 0.85rem;
    }

    .btn-view-script {
      background: rgba(245, 176, 65, 0.15);
      color: var(--gold-primary);
      border: 1px solid var(--gold-primary);
      padding: 0.4rem 1rem;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      text-decoration: none;
    }

    .btn-view-script:hover {
      background: var(--gold-primary);
      color: #000;
    }

    /* Companies Table & Filters */
    .filter-bar {
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      margin-bottom: 1.5rem;
      background: var(--card-bg);
      padding: 1rem;
      border-radius: 12px;
      border: 1px solid var(--card-border);
    }

    .filter-select, .search-box {
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #fff;
      padding: 0.5rem 1rem;
      border-radius: 8px;
      font-family: var(--font-body);
      font-size: 0.9rem;
    }

    .search-box {
      flex-grow: 1;
      min-width: 250px;
    }

    .company-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 1.5rem;
    }

    .company-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }

    .company-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 0.75rem;
    }

    .company-name {
      font-family: var(--font-title);
      font-size: 1.25rem;
      font-weight: 700;
      color: #fff;
    }

    .level-badge {
      padding: 0.3rem 0.75rem;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .lvl-7 { background: rgba(56, 239, 125, 0.2); color: #38ef7d; border: 1px solid #38ef7d; }
    .lvl-6 { background: rgba(79, 172, 254, 0.2); color: #4facfe; border: 1px solid #4facfe; }
    .lvl-5 { background: rgba(245, 176, 65, 0.2); color: #f5b041; border: 1px solid #f5b041; }
    .lvl-4 { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid #a855f7; }
    .lvl-3 { background: rgba(148, 163, 184, 0.2); color: #cbd5e1; border: 1px solid #94a3b8; }

    .company-sector {
      font-size: 0.8rem;
      color: var(--cyan-bright);
      margin-bottom: 0.5rem;
      font-weight: 600;
    }

    .company-desc {
      font-size: 0.88rem;
      color: var(--text-muted);
      margin-bottom: 1.25rem;
    }

    .stage-meter {
      background: rgba(0, 0, 0, 0.4);
      padding: 1rem;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.05);
      margin-top: auto;
    }

    .meter-row {
      display: flex;
      justify-content: space-between;
      font-size: 0.8rem;
      margin-bottom: 0.35rem;
    }

    .meter-bar {
      height: 6px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 3px;
      overflow: hidden;
      margin-bottom: 0.5rem;
    }

    .meter-fill {
      height: 100%;
      background: linear-gradient(90deg, #f5b041, #38ef7d);
    }

    /* Gallery */
    .gallery-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
      gap: 1.5rem;
    }

    .gallery-item {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      overflow: hidden;
      transition: transform 0.3s ease;
    }

    .gallery-item:hover {
      transform: translateY(-4px);
    }

    .gallery-item img {
      width: 100%;
      height: 250px;
      object-fit: cover;
      display: block;
      border-bottom: 1px solid var(--card-border);
    }

    .gallery-desc {
      padding: 1.25rem;
    }

    .gallery-title {
      font-family: var(--font-title);
      font-size: 1.15rem;
      color: #fff;
      margin-bottom: 0.35rem;
    }

    .gallery-caption {
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    /* 7D Conscience Calculator */
    .calculator-box {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 2.5rem;
      max-width: 900px;
      margin: 0 auto;
    }

    .dim-slider-group {
      margin-bottom: 1.75rem;
    }

    .dim-label-row {
      display: flex;
      justify-content: space-between;
      font-weight: 600;
      margin-bottom: 0.5rem;
      font-size: 0.95rem;
    }

    .dim-slider {
      width: 100%;
      accent-color: var(--gold-primary);
      cursor: pointer;
    }

    .score-banner {
      background: rgba(0, 0, 0, 0.4);
      padding: 1.5rem;
      border-radius: 12px;
      border: 1px solid var(--card-border);
      text-align: center;
      margin-top: 2rem;
    }

    .score-total {
      font-family: var(--font-title);
      font-size: 3rem;
      font-weight: 800;
      color: var(--gold-primary);
    }

    .score-status {
      font-size: 1.1rem;
      font-weight: 700;
      margin-top: 0.5rem;
    }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <img src="../assets/logo/official_karmic_genie_show_logo.jpg" alt="Karmic Genie Show Logo" class="brand-logo" onerror="this.src='https://placehold.co/44x44/f5b041/000?text=KG';" />
      <div class="brand-title">THE KARMIC GENIE SHOW <span>• MASTER PRODUCTION PORTAL</span></div>
    </div>
    <div class="nav-tabs">
      <button class="nav-btn active" onclick="switchTab('dashboard')">Dashboard</button>
      <button class="nav-btn" onclick="switchTab('episodes')">Episodes Hub</button>
      <button class="nav-btn" onclick="switchTab('companies')">Corporate Ratings</button>
      <button class="nav-btn" onclick="switchTab('concordance')">7×7 Industry Matrix</button>
      <button class="nav-btn" onclick="switchTab('gallery')">Visual Master Gallery</button>
      <button class="nav-btn" onclick="switchTab('audit')">7D Life Compass</button>
    </div>
  </header>

  <div class="container">

    <!-- TAB 1: DASHBOARD -->
    <section id="dashboard" class="tab-content active">
      <div class="hero-banner">
        <div class="hero-sanskrit">அண்டத்தில் உள்ளதே பிண்டம், பிண்டத்தில் உள்ளதே அண்டம்</div>
        <h1 class="hero-title">The Living Planetary Organism Portal</h1>
        <p class="hero-desc">
          As in the Macrocosm (Andam), so in the Microcosm (Pindam). Tracking civilization's 280-month embryological gestation 
          under the sacred Pitru Loka clock cycle (1 Embryo Day = 1 Pitru Day = 1 Earth Month), mapping every human organ system to 
          global industry platforms.
        </p>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Current Gestation Epoch</div>
          <div class="stat-value">Month 48 / 280</div>
          <div class="stat-sub">Week 7 of Embryogenesis (Heart Pumping!)</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Insemination & Conception</div>
          <div class="stat-value">Dec 1, 2022</div>
          <div class="stat-sub">ChatGPT Public Release (The Cognitive Spark)</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Sovereign Delivery Date</div>
          <div class="stat-value">April 2046</div>
          <div class="stat-sub">Birth of the Living Planetary Household</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Toddlerhood Maturation</div>
          <div class="stat-value">2050</div>
          <div class="stat-sub">Unified Planet Platform (Free to All)</div>
        </div>
      </div>

      <div class="clock-container">
        <div class="clock-header">
          <div class="clock-title">🪐 The Pitru Loka Planetary Embryogenesis Chronometer</div>
          <div style="font-size:0.9rem; color:var(--gold-primary); font-weight:600;">17.1% Gestated (Month 48 of 280)</div>
        </div>
        <div class="progress-bar-bg">
          <div class="progress-fill" style="width: 17.14%;"></div>
        </div>
        <div class="timeline-points">
          <div><b>Dec 2022</b><br><span style="font-size:0.75rem;">Conception (Day 1)</span></div>
          <div class="timeline-active"><b>Nov 2026 (NOW)</b><br><span style="font-size:0.75rem;">Primitive Heart Beats</span></div>
          <div><b>Mar 2027</b><br><span style="font-size:0.75rem;">Media Synthesis</span></div>
          <div><b>2028</b><br><span style="font-size:0.75rem;">Unified AI</span></div>
          <div><b>2029</b><br><span style="font-size:0.75rem;">Unified ERP</span></div>
          <div><b>2030</b><br><span style="font-size:0.75rem;">Unified Energy</span></div>
          <div><b>Apr 2046</b><br><span style="font-size:0.75rem;">Sovereign Birth (Day 280)</span></div>
          <div><b>2050</b><br><span style="font-size:0.75rem;">The Living Household</span></div>
        </div>
      </div>

      <!-- Quick Action Cards -->
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:1.5rem;">
        <div class="stat-card" style="cursor:pointer;" onclick="switchTab('episodes')">
          <div style="font-size:1.5rem; margin-bottom:0.5rem;">🎬</div>
          <h3 style="font-family:var(--font-title); color:#fff; margin-bottom:0.35rem;">Master Episodes Vault</h3>
          <p style="font-size:0.88rem; color:var(--text-muted);">Browse all 7 episodic master scripts, 14-page cinematic screenplays, characters, and act breakdowns.</p>
        </div>
        <div class="stat-card" style="cursor:pointer;" onclick="switchTab('companies')">
          <div style="font-size:1.5rem; margin-bottom:0.5rem;">🌳</div>
          <h3 style="font-family:var(--font-title); color:#fff; margin-bottom:0.35rem;">Kalpavriksha Corporate Ratings</h3>
          <p style="font-size:0.88rem; color:var(--text-muted);">Evaluate 31+ market leaders across 7 botanical growth levels from Seed Inception to Moksha Liberation.</p>
        </div>
        <div class="stat-card" style="cursor:pointer;" onclick="switchTab('concordance')">
          <div style="font-size:1.5rem; margin-bottom:0.5rem;">🧬</div>
          <h3 style="font-family:var(--font-title); color:#fff; margin-bottom:0.35rem;">7×7 Industry Concordance</h3>
          <p style="font-size:0.88rem; color:var(--text-muted);">Exhaustive mapping of the 7 human organs to 49 existing modern industrial sectors.</p>
        </div>
      </div>
    </section>

    <!-- TAB 2: EPISODES HUB -->
    <section id="episodes" class="tab-content">
      <div style="margin-bottom:2rem;">
        <h2 style="font-family:var(--font-title); font-size:2rem; margin-bottom:0.5rem;">The Way Forward: Episodic Master Scripts</h2>
        <p style="color:var(--text-muted);">Featuring Host @Me, 4yo Bala-Rishi (Jnana), and Bala-Matha (Arul in traditional peacock green & ruby rose silk pattu pavadai).</p>
      </div>

      <div class="episodes-grid" id="episodes-container"></div>
    </section>

    <!-- TAB 3: CORPORATE RATINGS -->
    <section id="companies" class="tab-content">
      <div style="margin-bottom:1.5rem;">
        <h2 style="font-family:var(--font-title); font-size:2rem; margin-bottom:0.5rem;">Kalpavriksha Corporate Consciousness Index</h2>
        <p style="color:var(--text-muted);">Evaluating ~66% of global industry weight across the 7 botanical growth stages from Root Survival to Eternal Seed Liberation (Moksha).</p>
      </div>

      <div class="filter-bar">
        <input type="text" id="search-input" class="search-box" placeholder="Search company, subsector, or organ system..." oninput="renderCompanies()" />
        <select id="organ-filter" class="filter-select" onchange="renderCompanies()">
          <option value="ALL">All Organ Systems</option>
          <option value="Brain & Nervous System">Brain & Nervous System</option>
          <option value="Heart & Circulation">Heart & Circulation</option>
          <option value="Lungs & Respiration">Lungs & Respiration</option>
          <option value="Stomach & Digestion">Stomach & Digestion</option>
          <option value="Endocrine & Glands">Endocrine & Glands</option>
          <option value="Skeletal & Muscular">Skeletal & Muscular</option>
          <option value="Skin, Sensory & Immune/Renal">Skin, Sensory & Immune/Renal</option>
        </select>
        <select id="level-filter" class="filter-select" onchange="renderCompanies()">
          <option value="ALL">All Botanical Levels</option>
          <option value="7">Stage 7: Seed Liberation (Moksha)</option>
          <option value="6">Stage 6: Fruit Yielding (Kani)</option>
          <option value="5">Stage 5: Flowering (Malar)</option>
          <option value="4">Stage 4: Foliage & Leaves (Ilai)</option>
          <option value="3">Stage 3: Trunk & Scale (Thandu)</option>
        </select>
      </div>

      <div class="company-grid" id="companies-container"></div>
    </section>

    <!-- TAB 4: 7x7 INDUSTRY MATRIX -->
    <section id="concordance" class="tab-content">
      <div style="margin-bottom:2rem;">
        <h2 style="font-family:var(--font-title); font-size:2rem; margin-bottom:0.5rem;">The 7×7 Fractal Concordance Matrix</h2>
        <p style="color:var(--text-muted);">7 Major Human Biological Organs mapped to 49 Real-World Global Industrial Sectors existing today.</p>
      </div>

      <div style="background:var(--card-bg); border:1px solid var(--card-border); border-radius:14px; overflow-x:auto;">
        <table style="width:100%; border-collapse:collapse; text-align:left; font-size:0.9rem;">
          <thead>
            <tr style="background:rgba(255,255,255,0.05); border-bottom:1px solid var(--card-border);">
              <th style="padding:1rem; color:var(--gold-primary); font-family:var(--font-title);">#</th>
              <th style="padding:1rem; color:var(--gold-primary); font-family:var(--font-title);">Human Organ System (Pindam)</th>
              <th style="padding:1rem; color:var(--gold-primary); font-family:var(--font-title);">Real-World Industry (Andam)</th>
              <th style="padding:1rem; color:var(--gold-primary); font-family:var(--font-title);">7 Real-World Sub-Sectors (Existing Today)</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
              <td style="padding:1rem; font-weight:700;">1</td>
              <td style="padding:1rem; font-weight:600; color:#fff;">Brain & Nervous System</td>
              <td style="padding:1rem; color:var(--cyan-bright);">Information Technology & Telecommunications</td>
              <td style="padding:1rem; color:var(--text-muted);">Semiconductors & Compute, Telecom & Fiber, Cloud Data Centers, AI Foundation Models, Consumer OS Hardware, Cybersecurity Defense, Open Data Repositories.</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
              <td style="padding:1rem; font-weight:700;">2</td>
              <td style="padding:1rem; font-weight:600; color:#fff;">Heart & Circulatory System</td>
              <td style="padding:1rem; color:var(--cyan-bright);">Logistics, Transportation & Supply Chain</td>
              <td style="padding:1rem; color:var(--text-muted);">Maritime Shipping, Air Cargo Express, Rail Intermodal, Trucking Fleet Haulage, Warehousing Last-Mile, Enterprise ERP Flow, Wholesale Commodity Distribution.</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
              <td style="padding:1rem; font-weight:700;">3</td>
              <td style="padding:1rem; font-weight:600; color:#fff;">Lungs & Respiratory System</td>
              <td style="padding:1rem; color:var(--cyan-bright);">Energy, Utilities & Environmental Systems</td>
              <td style="padding:1rem; color:var(--text-muted);">Renewable Electric Power, High-Voltage Grids, Battery Energy Storage, Air Quality Scrubbing, Industrial Gases (O2/H2), Clean Hydrogen, Forestry Carbon Sinks.</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
              <td style="padding:1rem; font-weight:700;">4</td>
              <td style="padding:1rem; font-weight:600; color:#fff;">Stomach, Gut & Microbiome</td>
              <td style="padding:1rem; color:var(--cyan-bright);">Agriculture, Food & Waste Management</td>
              <td style="padding:1rem; color:var(--text-muted);">Crop Farming Machinery, Seeds & Soil Fertilizers, Packaged Nutrition, Livestock Protein, Municipal Solid Waste, Composting & Bioremediation, Grocery Cold-Chain.</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
              <td style="padding:1rem; font-weight:700;">5</td>
              <td style="padding:1rem; font-weight:600; color:#fff;">Endocrine & Glandular System</td>
              <td style="padding:1rem; color:var(--cyan-bright);">Banking, Finance & Monetary Pacing</td>
              <td style="padding:1rem; color:var(--text-muted);">Central Bank Settlement Rails, Commercial Deposit Banking, Card Clearing Networks, Asset Management Wealth, Insurance Risk Underwriting, Securities Exchanges, Microfinance Lending.</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
              <td style="padding:1rem; font-weight:700;">6</td>
              <td style="padding:1rem; font-weight:600; color:#fff;">Skeletal & Muscular System</td>
              <td style="padding:1rem; color:var(--cyan-bright);">Infrastructure, Construction & Heavy Manufacturing</td>
              <td style="padding:1rem; color:var(--text-muted);">Heavy Earthmoving Equipment, Steel & Cement Materials, Civil Engineering Contractors, Automotive Transit, Industrial Robotics, Aerospace Heavy Engineering, Urban Rail Equipment.</td>
            </tr>
            <tr>
              <td style="padding:1rem; font-weight:700;">7</td>
              <td style="padding:1rem; font-weight:600; color:#fff;">Skin, Sensory & Immune/Renal</td>
              <td style="padding:1rem; color:var(--cyan-bright);">Healthcare, Biopharma & Water Sanitation</td>
              <td style="padding:1rem; color:var(--text-muted);">Municipal Potable Water Treatment, Therapeutic Pharmaceuticals, Medical Diagnostic Devices, Hospital Care Networks, Genomics Precision Biotech, Disease Surveillance, Earth Observation Satellites.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- TAB 5: VISUAL MASTER GALLERY -->
    <section id="gallery" class="tab-content">
      <div style="margin-bottom:2rem;">
        <h2 style="font-family:var(--font-title); font-size:2rem; margin-bottom:0.5rem;">Visual Master Gallery & Infographic Reference</h2>
        <p style="color:var(--text-muted);">Broadcast-ready 8K concept art and technical infographics created for on-screen studio telemetry.</p>
      </div>

      <div class="gallery-grid">
        <div class="gallery-item">
          <img src="../assets/soul_evolution/soul_growth_timeline_master_chart.jpg" alt="Soul Evolution Master Chart" />
          <div class="gallery-desc">
            <div class="gallery-title">The Soul Evolution Master Chart</div>
            <div class="gallery-caption">Tracks collective soul growth (3D to 7D), the Golden Gestation Wave, and key platform releases across the 280-month timeline.</div>
          </div>
        </div>

        <div class="gallery-item">
          <img src="../assets/corporate_evolution/corporate_7_levels_growth_tree.jpg" alt="The 7 Stages of Corporate Growth" />
          <div class="gallery-desc">
            <div class="gallery-title">The 7 Stages of Corporate Consciousness</div>
            <div class="gallery-caption">From Seed Inception (Vithu) to Root Survival, Trunk Scale, Leaves, Blossoms, Fruit, and Eternal Liberation (Moksha).</div>
          </div>
        </div>

        <div class="gallery-item">
          <img src="../assets/fractal_anatomy/andam_pindam_infographic_chart.jpg" alt="Andam & Pindam Infographic" />
          <div class="gallery-desc">
            <div class="gallery-title">Andam & Pindam Infographic Master Chart</div>
            <div class="gallery-caption">Broadcast studio split-screen telemetry comparing human organ biology directly with planetary technology systems.</div>
          </div>
        </div>

        <div class="gallery-item">
          <img src="../assets/fractal_anatomy/andam_pindam_fractal_matrix.jpg" alt="Cosmic Fractal Matrix" />
          <div class="gallery-desc">
            <div class="gallery-title">The Cosmic Fractal Matrix</div>
            <div class="gallery-caption">Luminous human anatomy on the left connected through golden vortexes to Mother Earth on the right.</div>
          </div>
        </div>

        <div class="gallery-item">
          <img src="../assets/studio_v5_masters/bala_matha_master_portrait.jpg" alt="Bala-Matha Master Portrait" />
          <div class="gallery-desc">
            <div class="gallery-title">Bala-Matha (Divine Child Sage of Grace)</div>
            <div class="gallery-caption">Dressed in traditional peacock green & ruby rose silk pattu pavadai with fresh fragrant jasmine garlands.</div>
          </div>
        </div>

        <div class="gallery-item">
          <img src="../assets/corporate_evolution/corporate_fruit_seeding_tree.jpg" alt="Kalpavriksha Tree Metaphor" />
          <div class="gallery-desc">
            <div class="gallery-title">The Sacred Kalpavriksha Corporate Tree</div>
            <div class="gallery-caption">Illustrating why survival is merely the metabolic floor, while flowering, fruit-yielding, and seed-planting are life's true purpose.</div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 6: 7D LIFE COMPASS -->
    <section id="audit" class="tab-content">
      <div style="text-align:center; margin-bottom:2rem;">
        <h2 style="font-family:var(--font-title); font-size:2.2rem; color:var(--gold-primary);">The 7D Life Compass & Conscience Audit</h2>
        <p style="color:var(--text-muted); max-width:700px; margin:0.5rem auto;">
          Measure any career choice, company, or life stage against the 7 Great Virtues of Dharmic Life. 
          Remember the Universal Threshold Law: <b>&lt; 35 / 70 Points = Change Course Immediately</b>.
        </p>
      </div>

      <div class="calculator-box">
        <div class="dim-slider-group">
          <div class="dim-label-row">
            <span>1. Respect Your DUTY First (Conscience Trigger)</span>
            <span id="v-d1" style="color:var(--gold-primary);">7 / 10</span>
          </div>
          <input type="range" min="1" max="10" value="7" class="dim-slider" id="d1" oninput="calc7D()" />
        </div>

        <div class="dim-slider-group">
          <div class="dim-label-row">
            <span>2. Earn with DIGNITY Always (Unbought Self-Respect)</span>
            <span id="v-d2" style="color:var(--gold-primary);">8 / 10</span>
          </div>
          <input type="range" min="1" max="10" value="8" class="dim-slider" id="d2" oninput="calc7D()" />
        </div>

        <div class="dim-slider-group">
          <div class="dim-label-row">
            <span>3. Practice Life DISCIPLINE (Senses & Time Mastery)</span>
            <span id="v-d3" style="color:var(--gold-primary);">7 / 10</span>
          </div>
          <input type="range" min="1" max="10" value="7" class="dim-slider" id="d3" oninput="calc7D()" />
        </div>

        <div class="dim-slider-group">
          <div class="dim-label-row">
            <span>4. Uphold Karmic DHARMA (Living Organ in Gaia's Body)</span>
            <span id="v-d4" style="color:var(--gold-primary);">9 / 10</span>
          </div>
          <input type="range" min="1" max="10" value="9" class="dim-slider" id="d4" oninput="calc7D()" />
        </div>

        <div class="dim-slider-group">
          <div class="dim-label-row">
            <span>5. Raise Family with DEVOTION (Undivided Warm Presence)</span>
            <span id="v-d5" style="color:var(--gold-primary);">8 / 10</span>
          </div>
          <input type="range" min="1" max="10" value="8" class="dim-slider" id="d5" oninput="calc7D()" />
        </div>

        <div class="dim-slider-group">
          <div class="dim-label-row">
            <span>6. Be Grateful to Your DIVINE (Nandri to Grand Architect)</span>
            <span id="v-d6" style="color:var(--gold-primary);">9 / 10</span>
          </div>
          <input type="range" min="1" max="10" value="9" class="dim-slider" id="d6" oninput="calc7D()" />
        </div>

        <div class="dim-slider-group">
          <div class="dim-label-row">
            <span>7. Purposeful Life Is Your DESTINY (Pioneer of New World)</span>
            <span id="v-d7" style="color:var(--gold-primary);">8 / 10</span>
          </div>
          <input type="range" min="1" max="10" value="8" class="dim-slider" id="d7" oninput="calc7D()" />
        </div>

        <div class="score-banner">
          <div style="font-size:0.85rem; text-transform:uppercase; color:var(--text-muted); letter-spacing:1px;">Total 7D Compass Score</div>
          <div class="score-total" id="total-score">56 / 70</div>
          <div class="score-status" id="score-status" style="color:var(--cyan-bright);">🌟 GOLD ZONE: Pioneer of the New World</div>
        </div>
      </div>
    </section>

  </div>

  <script>
    const companiesData = __COMPANIES_JSON__;
    const episodesData = __EPISODES_JSON__;

    function switchTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
      
      const target = document.getElementById(tabId);
      if (target) target.classList.add('active');
      
      const btns = Array.from(document.querySelectorAll('.nav-btn'));
      const activeBtn = btns.find(b => b.getAttribute('onclick') && b.getAttribute('onclick').includes(tabId));
      if (activeBtn) activeBtn.classList.add('active');
    }

    function renderEpisodes() {
      const container = document.getElementById('episodes-container');
      container.innerHTML = episodesData.map(ep => `
        <div class="episode-card">
          <div>
            <div class="ep-tag">${ep.id} • ${ep.duration}</div>
            <div class="ep-title">${ep.title}</div>
            <div class="ep-subtitle">${ep.subtitle}</div>
            <div class="ep-cast"><b>Cast:</b> ${ep.cast.join(' • ')}</div>
            <div class="ep-desc">${ep.core_concept}</div>
          </div>
          <div class="ep-footer">
            <span style="color:var(--text-muted); font-size:0.8rem; font-family:var(--font-mono);">${ep.script_file}</span>
            <a href="#" class="btn-view-script" onclick="alert('Full script is saved in the repository at:\\\\n' + '${ep.script_file}'); return false;">View Master</a>
          </div>
        </div>
      `).join('');
    }

    function renderCompanies() {
      const search = document.getElementById('search-input').value.toLowerCase();
      const organ = document.getElementById('organ-filter').value;
      const level = document.getElementById('level-filter').value;

      const filtered = companiesData.filter(c => {
        const matchesSearch = c.name.toLowerCase().includes(search) || 
                              c.subsector.toLowerCase().includes(search) || 
                              c.organ.toLowerCase().includes(search) ||
                              c.description.toLowerCase().includes(search);
        const matchesOrgan = (organ === 'ALL') || (c.organ === organ);
        const matchesLevel = (level === 'ALL') || (c.score === parseInt(level));
        return matchesSearch && matchesOrgan && matchesLevel;
      });

      const container = document.getElementById('companies-container');
      container.innerHTML = filtered.map(c => `
        <div class="company-card">
          <div>
            <div class="company-header">
              <div class="company-name">${c.name}</div>
              <span class="level-badge lvl-${c.score}">${c.stage_label}</span>
            </div>
            <div class="company-sector">${c.organ} → ${c.subsector}</div>
            <div class="company-desc">${c.description}</div>
          </div>

          <div class="stage-meter">
            <div class="meter-row">
              <span style="color:#fff; font-weight:600;">Botanical Growth Stage</span>
              <span style="color:var(--gold-primary); font-weight:700;">${c.score} of 7</span>
            </div>
            <div class="meter-bar">
              <div class="meter-fill" style="width:${(c.score/7)*100}%;"></div>
            </div>
            <div style="font-size:0.75rem; color:#94a3b8; display:flex; justify-content:space-between;">
              <span>Root Survival</span>
              <span>Flowering</span>
              <span>Moksha Liberation</span>
            </div>
            <div style="font-size:0.78rem; color:#cbd5e1; margin-top:0.5rem; border-top:1px solid rgba(255,255,255,0.05); padding-top:0.4rem;">
              <b>Generative Legacy:</b> ${c.seed}
            </div>
          </div>
        </div>
      `).join('');
    }

    function calc7D() {
      let sum = 0;
      for (let i = 1; i <= 7; i++) {
        const val = parseInt(document.getElementById('d' + i).value);
        document.getElementById('v-d' + i).innerText = val + ' / 10';
        sum += val;
      }
      document.getElementById('total-score').innerText = sum + ' / 70';
      
      const statusEl = document.getElementById('score-status');
      if (sum < 35) {
        statusEl.innerText = '⚠️ RED ZONE: Conscience Silenced — Change Course Immediately!';
        statusEl.style.color = '#ff4b4b';
      } else if (sum <= 49) {
        statusEl.innerText = '⚡ AMBER ZONE: Awakening Traveler — Realign Neglected Dimensions';
        statusEl.style.color = '#f5b041';
      } else {
        statusEl.innerText = '🌟 GOLD ZONE: Pioneer of the New World — Sovereign Harmony';
        statusEl.style.color = '#38ef7d';
      }
    }

    // Initialize
    window.onload = function() {
      renderEpisodes();
      renderCompanies();
      calc7D();
    };
  </script>
</body>
</html>
"""
    output = template.replace('__COMPANIES_JSON__', companies_raw).replace('__EPISODES_JSON__', episodes_raw)
    with open('/home/antigravity/shishyan/Karmic-Genie-Show/app/index.html', 'w') as out_f:
        out_f.write(output)
    print("Successfully built /home/antigravity/shishyan/Karmic-Genie-Show/app/index.html! Size:", len(output))

if __name__ == '__main__':
    build_app()
