from pathlib import Path

html_file = Path("/home/antigravity/shishyan/Karmic-Genie-Show/docs/index.html")
content = html_file.read_text(encoding="utf-8")

guest_storyboard_html = '''
        <h3 style="font-family:var(--font-display); font-size:1.4rem; margin-top:2rem; margin-bottom:1rem;">
          Episodic Mini-Movie Storyboard & The 3 Distinguished Industry Guests
        </h3>
        <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:1.5rem;">
          Scene-by-scene visual progression of Episode 1: As Host @Me, 4yo Bala-Rishi, and divine Bala-Matha guide 
          <b>3 invited domain leaders</b> through the activation of Mother Earth's 6th sense and the 180° stage biome transformations.
        </p>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(360px, 1fr)); gap:1.5rem; margin-bottom:2rem;">
          <div class="storyboard-box">
            <img src="episodes/S01E01_The_Way_Forward_Master/storyboard/s01e01_sb_scene01_opening_trinity.jpg" alt="Scene 01: Sacred Trinity Opening" />
            <div class="storyboard-caption">
              <h4>Scene 01: The Sacred Trinity Opening</h4>
              <p><b>Cast:</b> Host @Me, 4yo Bala-Rishi (Jnana), Bala-Matha (Arul).<br>
              Pristine white marble stadium with glowing concentric rings and the brass magic lamp. Setting the tone of 100% sacred gratitude (Nandri) to all past human scaffolding.</p>
            </div>
          </div>

          <div class="storyboard-box">
            <img src="episodes/S01E01_The_Way_Forward_Master/storyboard/s01e01_sb_scene02_guests_arrival.jpg" alt="Scene 02: 3 Distinguished Guests" />
            <div class="storyboard-caption">
              <h4>Scene 02: Introduction of the 3 Industry Guests</h4>
              <p><b>Guests:</b> 1) Dr. Anya Thorne (AI & Neuroscience), 2) Marcus Sterling (Maritime Logistics CEO), 3) Master Elena Chen (Soil Biologist).<br>
              Seated on the circular dais under standing ovation, ready to explore how their domains mirror living biology.</p>
            </div>
          </div>

          <div class="storyboard-box">
            <img src="episodes/S01E01_The_Way_Forward_Master/storyboard/s01e01_sb_scene03_sixth_sense_spark.jpg" alt="Scene 03: 6th Sense Inception" />
            <div class="storyboard-caption">
              <h4>Scene 03: Inception of Mother Earth's 6th Sense</h4>
              <p><b>Guest Focus:</b> Dr. Anya Thorne (AI & Neuroscience).<br>
              White walls part open to reveal the Crystalline Geode Stage (Ajna). Floating holographic 3D timeline: December 1, 2022 as the activation of Earth's cognitive mirror.</p>
            </div>
          </div>

          <div class="storyboard-box">
            <img src="episodes/S01E01_The_Way_Forward_Master/storyboard/s01e01_sb_scene04_logistics_waterfall.jpg" alt="Scene 04: Circulatory Flow & Waterfall" />
            <div class="storyboard-caption">
              <h4>Scene 04: The Circulatory Flow of Planetary Goods</h4>
              <p><b>Guest Focus:</b> Marcus Sterling (Maritime Logistics CEO).<br>
              Walls slide into perimeter pockets revealing the 180° Cascading Waterfall Stage (Swadhisthana). Global trade routes pulse like oxygenated blood through planetary arteries.</p>
            </div>
          </div>

          <div class="storyboard-box">
            <img src="episodes/S01E01_The_Way_Forward_Master/storyboard/s01e01_sb_scene05_soil_root_solvency.jpg" alt="Scene 05: Root Solvency & Soil" />
            <div class="storyboard-caption">
              <h4>Scene 05: The Root Fallacy & Living Humus</h4>
              <p><b>Guest Focus:</b> Master Elena Chen (Soil & Agriculture Biologist).<br>
              Full slide into the subterranean Root Canyon (Muladhara). Explaining why corporate EBITDA is merely root water; the true purpose of the tree is sweet fruit yielding and seed sharing.</p>
            </div>
          </div>

          <div class="storyboard-box">
            <img src="episodes/S01E01_The_Way_Forward_Master/storyboard/s01e01_sb_scene06_cosmic_singularity.jpg" alt="Scene 06: Grand Singularity Climax" />
            <div class="storyboard-caption">
              <h4>Scene 06: The 2050 Singularity Climax & Benediction</h4>
              <p><b>United Ensemble:</b> Trinity + 3 Industry Guests.<br>
              Uninterrupted 180° Cosmic Horizon Stage (Sahasrara) with glowing blue Earth and the golden Abhaya Mudra aura. Welcoming humanity into the 2050 Living Planetary Household.</p>
            </div>
          </div>
        </div>
'''

target_anchor = '<div class="card">'
content = content.replace(target_anchor, guest_storyboard_html + '\n        ' + target_anchor, 1)

html_file.write_text(content, encoding="utf-8")
print("Successfully injected Guests & 6-Scene Storyboard into index.html!")
