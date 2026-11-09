from pathlib import Path

html_file = Path("/home/antigravity/shishyan/Karmic-Genie-Show/docs/index.html")
content = html_file.read_text(encoding="utf-8")

# In view-stages, add the Aperture Stagecraft and Honeycomb section
aperture_html = '''
        <!-- The Dynamic Aperture Iris Stagecraft Section (Mini-Movie Mechanism) -->
        <div class="card" style="margin-top:2rem;">
          <div class="siddha-mantra">The Mini-Movie Storytelling Mechanism</div>
          <h3 style="font-family:var(--font-display); font-size:1.35rem; margin-bottom:0.5rem;">
            Stationary Host Hub + Dynamic Parting Wall (Aperture Iris Stagecraft)
          </h3>
          <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:1.25rem;">
            To transform the show from a static monologue into an <b>immersive cinematic mini-movie</b>, the host seating, brass lamp, 
            and audience stay anchored on the familiar white marble stadium. The curved white back wall containing the <b>7D Virtues</b> 
            mechanically splits and slides open horizontally—revealing the rotating environmental biomes behind to match the exact story scene.
          </p>

          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(360px, 1fr)); gap:1.25rem;">
            <div class="storyboard-box">
              <img src="assets/stages_7d/kgs_white_stage_aperture_waterfall_16x9.jpg" alt="Waterfall Stage Aperture" />
              <div class="storyboard-caption">
                <h4>Stage Aperture: Waterfall & Circulation</h4>
                <p>Curved white wall splits to reveal cascading turquoise waterfalls when discussing logistics, blood flow, and ERP trade circulation.</p>
              </div>
            </div>
            <div class="storyboard-box">
              <img src="assets/stages_7d/kgs_white_stage_aperture_root_canyon_16x9.jpg" alt="Root Canyon Stage Aperture" />
              <div class="storyboard-caption">
                <h4>Stage Aperture: Earthen Root Canyon</h4>
                <p>White wall glides open to reveal subterranean banyan roots and amber geodes when exploring corporate solvency and grounding.</p>
              </div>
            </div>
            <div class="storyboard-box">
              <img src="assets/stages_7d/kgs_white_stage_aperture_cosmic_16x9.jpg" alt="Cosmic Horizon Stage Aperture" />
              <div class="storyboard-caption">
                <h4>Stage Aperture: Cosmic Horizon & Abhaya Mudra</h4>
                <p>The wall parts completely to reveal the blue curve of Earth, auroras, and golden blessing for the 2050 Singularity finale.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Honeycomb 7-Stage Mandala Architecture Visuals -->
        <div class="card" style="margin-top:1.5rem;">
          <div class="siddha-mantra">Honeycomb 7-Stage Architectural Mandala</div>
          <h3 style="font-family:var(--font-display); font-size:1.35rem; margin-bottom:0.5rem;">
            1 Central White Sanctuary + 6 Surrounding Elemental Pavilions
          </h3>
          <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:1.25rem;">
            Arranged symmetrically like a sacred bee honeycomb (6 surrounding hexagons connected by translucent glass bridges to the central hub), 
            mapping directly to the <b>7 Chakras</b> and the <b>7 Major Platform Releases (2022 to 2050)</b>.
          </p>
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(420px, 1fr)); gap:1.25rem;">
            <div class="storyboard-box">
              <img src="assets/stages_7d/honeycomb_7_stages_mandala_aerial.jpg" alt="Honeycomb Aerial Mandala" />
              <div class="storyboard-caption">
                <h4>Master Honeycomb Studio Complex (Aerial Perspective)</h4>
                <p>Central white rotunda projecting a vertical golden beam of light, flanked by 6 biophilic hexagonal studio pavilions in the Nilgiri hills.</p>
              </div>
            </div>
            <div class="storyboard-box">
              <img src="assets/stages_7d/honeycomb_central_sanctuary_interior.jpg" alt="Central Hub Interior View" />
              <div class="storyboard-caption">
                <h4>Central White Sanctuary (360° Interior Sightlines)</h4>
                <p>Looking out through the 6 grand hexagonal glass archways into each elemental stage world while maintaining the clean white brand core.</p>
              </div>
            </div>
          </div>
        </div>
'''

target_anchor = '<!-- Stage Filter Buttons -->'
content = content.replace(target_anchor, aperture_html + '\n        ' + target_anchor)

html_file.write_text(content, encoding="utf-8")
print("Successfully injected Aperture Stagecraft and Honeycomb sections into index.html!")
