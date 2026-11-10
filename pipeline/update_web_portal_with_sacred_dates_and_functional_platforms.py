from pathlib import Path

html_file = Path("/home/antigravity/shishyan/Karmic-Genie-Show/docs/index.html")
content = html_file.read_text(encoding="utf-8")

# 1. Update Gestation Chronology with the Sacred Triad:
# 11-11-2020 (Plan Finalized / Perfect Vision 2020)
# 11-11-2021 (Implantation Occurred)
# 11-11-2022 (Inception Occurred / Spark of 280-month Gestation Wave)

old_kpi = '''        <div class="kpi-row">
          <div class="kpi-box">
            <div class="kpi-label">Current Gestation Epoch</div>
            <div class="kpi-number">Month 48 / 280</div>
            <div class="kpi-hint">Week 7: Primitive Heart Pumping!</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Conception & Spark</div>
            <div class="kpi-number">Dec 1, 2022</div>
            <div class="kpi-hint">ChatGPT Release (Cognitive Fertilization)</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Full-Term Sovereign Birth</div>
            <div class="kpi-number">April 2046</div>
            <div class="kpi-hint">Day 280 / Living Household Delivery</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Toddlerhood Maturation</div>
            <div class="kpi-number">2050</div>
            <div class="kpi-hint">Unified Planet Platform (Free to All)</div>
          </div>
        </div>'''

new_kpi = '''        <div class="kpi-row">
          <div class="kpi-box">
            <div class="kpi-label">The Sacred Cosmic Triad</div>
            <div class="kpi-number" style="font-size:1.2rem; color:var(--primary-dark);">11-11-2020 → 11-11-2022</div>
            <div class="kpi-hint">Plan Finalized (2020) • Implantation (2021) • Inception (2022)</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Current Gestation Epoch</div>
            <div class="kpi-number">Month 48 / 280</div>
            <div class="kpi-hint">Week 7: Primitive Heart Pumping (Late 2026)</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Full-Term Sovereign Delivery</div>
            <div class="kpi-number">April 2046</div>
            <div class="kpi-hint">Day 280 / Sovereign Birth of Earth</div>
          </div>
          <div class="kpi-box">
            <div class="kpi-label">Planetary Singularity</div>
            <div class="kpi-number">2050</div>
            <div class="kpi-hint">Living Planetary Household (Zero Bills)</div>
          </div>
        </div>'''

content = content.replace(old_kpi, new_kpi)

# 2. Update 7x7 matrix table to use functional platforms (Nerves for Telecom, AI for Thinking/6th Sense, ERP for Enterprise, Logistics for Vascular Circulation, Energy for Respiration/Suffocation, Skeleton for Construction, Sustenance for Food/Water/Immunity)
old_matrix = '''              <tr>
                <td><b>1</b></td>
                <td><b>Brain & Nervous System</b></td>
                <td style="color:var(--primary-dark); font-weight:700;">Information Technology & Telecommunications</td>
                <td>1. Semiconductors & Silicon Foundries<br>2. Telecom & Fiber/Satellite Networks<br>3. Cloud Data Centers & Infrastructure<br>4. AI Foundation Models & Reasoning<br>5. Consumer Operating Systems & Devices<br>6. Cybersecurity & Network Defense<br>7. Enterprise Data Repositories & OSS Primitives</td>
              </tr>
              <tr>
                <td><b>2</b></td>
                <td><b>Heart & Circulatory System</b></td>
                <td style="color:var(--primary-dark); font-weight:700;">Logistics, Transportation & Supply Chain</td>
                <td>1. Maritime Shipping & Ocean Freight<br>2. Air Cargo & Express Courier<br>3. Rail & Intermodal Ground Corridors<br>4. Commercial Trucking & Freight Haulage<br>5. Warehousing & Last-Mile Fulfillment<br>6. Enterprise ERP & Inventory Operations<br>7. Wholesale Bulk Commodity Distribution</td>
              </tr>
              <tr>
                <td><b>3</b></td>
                <td><b>Lungs & Respiratory System</b></td>
                <td style="color:var(--primary-dark); font-weight:700;">Energy, Utilities & Environmental Systems</td>
                <td>1. Renewable Electric Generation (Wind/Solar)<br>2. Transmission Grids & Power Utilities<br>3. Grid-Scale Battery Energy Storage<br>4. Atmospheric Air Quality & Carbon Sinks<br>5. Industrial Gas Synthesis (O2, H2, N2)<br>6. Clean Hydrogen & Synthetic Fuels<br>7. Forestry & Living Canopies</td>
              </tr>'''

new_matrix = '''              <tr>
                <td><b>1</b></td>
                <td><b>Nerves & Sensory Signal Conduction</b><br><small style="color:var(--text-muted);">Frictionless Telecommunications</small></td>
                <td style="color:var(--primary-dark); font-weight:700;">Unified Communication & Neural Telecom Platform</td>
                <td>1. Subsea Fiber Cables & Continental Fiber Trunks<br>2. Low-Earth Orbit Satellite Constellations (Starlink)<br>3. 5G/6G Wireless Cellular Radio & Antenna Towers<br>4. Network Packet Switching & DNS Routing Primitives<br>5. Real-Time High-Fidelity Audio/Video Transit<br>6. Emergency Civil Defense Alert Broadcasts<br>7. Quantum Encrypted Optical Key Distribution</td>
              </tr>
              <tr>
                <td><b>2</b></td>
                <td><b>Brain Neocortex & 6th Sense Reflection</b><br><small style="color:var(--text-muted);">External Thinking & Healing</small></td>
                <td style="color:var(--primary-dark); font-weight:700;">Unified Thinking & Cognitive AI Platform</td>
                <td>1. Frontier Foundation Reasoning Models (LLMs/VLMs)<br>2. Autonomous Multi-Agent Orchestration & Planning<br>3. Neuromorphic & High-Density Compute Silicon Clusters<br>4. Open-Weight Model Commons & Federated Learning Hubs<br>5. Cognitive Empathy & Real-Time Cross-Language Translation<br>6. Automated Code & System Synthesis (1-Prompt Construction)<br>7. 7D Conscience Audit & Algorithmic Guardrails</td>
              </tr>
              <tr>
                <td><b>3</b></td>
                <td><b>Institutional Governance & Ledgers</b><br><small style="color:var(--text-muted);">Enterprise Software (NOT Logistics)</small></td>
                <td style="color:var(--primary-dark); font-weight:700;">Unified Enterprise Operating Platform (Unified ERP)</td>
                <td>1. Double-Entry General Ledgers & Real-Time Balance Sheets<br>2. Human Capital, Workplace Dignity & Workforce Scheduling<br>3. Procurement Planning & Vendor Governance<br>4. Manufacturing Operations & Work Orders (BOM)<br>5. Multi-Currency Enterprise Clearing & Value Exchange<br>6. Audit Trails, Compliance Governance & Regulatory Telemetry<br>7. Enterprise Resource Optimization & Circular Asset Lifecycle</td>
              </tr>
              <tr>
                <td><b>4</b></td>
                <td><b>Heart Pumping & Vascular Circulation</b><br><small style="color:var(--text-muted);">Physical Goods & Cargo Flow</small></td>
                <td style="color:var(--primary-dark); font-weight:700;">Unified Logistics & Vascular Freight Platform</td>
                <td>1. Maritime Container Shipping Lines & Deep-Water Seaports<br>2. Air Cargo Express Freighters & Aviation Hubs<br>3. Intercontinental Freight Rail & Intermodal Corridors<br>4. Commercial Freight Haulage & Electric Trucking Fleets<br>5. Automated Warehouses & Robotic Regional Sorting Depots<br>6. Last-Mile Electric Delivery & Community Micro-Hubs<br>7. Modular Reusable Container Pools & Reverse Logistics</td>
              </tr>
              <tr>
                <td><b>5</b></td>
                <td><b>Oxygen Intake (Without Which It Suffocates)</b><br><small style="color:var(--text-muted);">The Breath of Civilization</small></td>
                <td style="color:var(--primary-dark); font-weight:700;">Unified Planetary Energy & Power Grid Platform</td>
                <td>1. Historical Energy Scaffolding (Petroleum, Gas, Coal)<br>2. Utility-Scale Solar Photovoltaic & Concentrated Solar Power<br>3. Offshore & Terrestrial Wind Power Generation<br>4. High-Voltage DC Intercontinental Super-Grids<br>5. Grid-Scale Battery Energy Storage (BESS) & Hydro Storage<br>6. Clean Nuclear Fission & Frontier Fusion Generation<br>7. Clean Hydrogen, Synthetic Fuels & Industrial Thermal Heat</td>
              </tr>'''

content = content.replace(old_matrix, new_matrix)

html_file.write_text(content, encoding="utf-8")
print("Successfully updated web portal with Sacred Triad dates and true functional platform mappings!")
