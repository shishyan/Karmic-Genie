from pathlib import Path

html_file = Path("/home/antigravity/shishyan/Karmic-Genie-Show/docs/index.html")
content = html_file.read_text(encoding="utf-8")

# Add the 180° Full Retraction Cinematic Mini-Movie Set Section
full_retraction_html = '''
        <!-- 180° Panoramic Full Stage Retraction (Mini-Movie Immersion) -->
        <div class="card" style="margin-top:2rem;">
          <div class="siddha-mantra">180° Panoramic Theatrical Transformation</div>
          <h3 style="font-family:var(--font-display); font-size:1.35rem; margin-bottom:0.5rem;">
            Full Wall Retraction into Perimeter Wings (Uninterrupted Mini-Movie Biomes)
          </h3>
          <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:1.25rem;">
            When the narrative transitions from dialogue into full-scale cinematic worldbuilding, <b>both curved white side walls slide completely back 
            and recess into the stadium perimeter wings</b>. The entire 180-degree backdrop opens into an expansive, continuous physical/virtual biome 
            while the host platform, modern armchairs, brass lamp, and audience remain in place.
          </p>

          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(360px, 1fr)); gap:1.25rem;">
            <div class="storyboard-box">
              <img src="assets/stages_7d/full_stage_retract_waterfall_16x9.jpg" alt="180 Panoramic Waterfall" />
              <div class="storyboard-caption">
                <h4>Full Retraction: 180° Cascading Waterfalls</h4>
                <p>Walls slide into side pockets, opening the full stadium to living turquoise waterfalls and mist across the entire horizon.</p>
              </div>
            </div>
            <div class="storyboard-box">
              <img src="assets/stages_7d/full_stage_retract_root_canyon_16x9.jpg" alt="180 Panoramic Root Canyon" />
              <div class="storyboard-caption">
                <h4>Full Retraction: Subterranean Root Canyon</h4>
                <p>Walls fully retract to reveal the full banyan root arches, glowing amber geodes, and rich soil biome across the stadium width.</p>
              </div>
            </div>
            <div class="storyboard-box">
              <img src="assets/stages_7d/full_stage_retract_cosmic_16x9.jpg" alt="180 Panoramic Cosmic Horizon" />
              <div class="storyboard-caption">
                <h4>Full Retraction: Cosmic Horizon & Abhaya Mudra</h4>
                <p>Walls disappear, revealing the breathtaking blue limb of Earth, swirling auroras, and golden blessing across the cosmos.</p>
              </div>
            </div>
            <div class="storyboard-box">
              <img src="assets/stages_7d/full_stage_retract_solar_16x9.jpg" alt="180 Panoramic Solar Caldera" />
              <div class="storyboard-caption">
                <h4>Full Retraction: Sunlit Solar Caldera</h4>
                <p>Full panoramic mountain sunset with golden auroras and clean energy solar telemetry for deep energy discussions.</p>
              </div>
            </div>
            <div class="storyboard-box">
              <img src="assets/stages_7d/full_stage_retract_crystal_16x9.jpg" alt="180 Panoramic Crystal Cavern" />
              <div class="storyboard-caption">
                <h4>Full Retraction: Crystalline Amethyst Cavern</h4>
                <p>180° vaulted violet quartz geode with glowing neural synapses for AI, synthetic mind, and 6th sense activation.</p>
              </div>
            </div>
          </div>
        </div>
'''

target_anchor = '<!-- Honeycomb 7-Stage Mandala Architecture Visuals -->'
content = content.replace(target_anchor, full_retraction_html + '\n        ' + target_anchor)

html_file.write_text(content, encoding="utf-8")
print("Successfully injected Full Stage Retraction section into index.html!")
