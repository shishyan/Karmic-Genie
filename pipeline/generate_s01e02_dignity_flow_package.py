#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exports & validates the complete Google Flow Production Package for:
  The Karmic Genie Show — Season 1, Episode 2 ("2. Earn with DIGNITY Always.")
  - episodes/S01E02_Earn_With_Dignity_Always/GOOGLE_FLOW_STORYBOARD_PACKAGE_S01E02.json (12 scenes)
  - episodes/S01E02_Earn_With_Dignity_Always/s01e02_48_shot_flow_ledger.json (48 cinema shots ED01..ED48)

Enforces Ironclad Narrator Separation:
  Narrators (@Me, 4yo Bala-Rishi, Bala-Matha) stay strictly unseen foreground/stage narrators
  addressing ONLY the camera/viewer—NEVER mixed up or perceived as characters inside the story.
"""

import json
import re
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
EP_DIR = REPO_DIR / "episodes" / "S01E02_Earn_With_Dignity_Always"
SCREENPLAY_PATH = EP_DIR / "S01E02_14_Page_Master_Screenplay_Earn_With_Dignity_Always.md"

STORYBOARD_SCENES = [
    {
        "scene": 1,
        "act": "ACT I — 11:45 PM UNWATCHED CROSSROADS (Page 1)",
        "title": "11:45 PM Empty Engineering Floor: The Easy Shortcut When No One Watches",
        "setting": "Foreground glass walkway outside an amber-lit engineering floor at 11:45 PM with rain streaks on windows.",
        "characters": "Story world: Engineer Karthik (34) & Division Head Vikram (46). Foreground unseen narrators: @Me + 4yo Bala-Rishi.",
        "narrator_separation_blocking": "STRICT SEPARATION: @Me and 4yo Bala-Rishi stand outside the acoustic glass partition facing ONLY the camera; Karthik and Vikram remain inside their room completely unaware of the narrators.",
        "time_pause_mechanic": "[SCENE TIME-PAUSE] freezes Karthik's pen two millimeters above the compromised signature line.",
        "dialogue_anchor": "One silent click hides the flaw, steals a junior's credit, and wins an easy bonus—since nobody sees!",
        "visual_asset": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_01_midnight_unwatched_test.jpg",
        "ref_ingredient": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_01_midnight_unwatched_test.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 2,
        "act": "ACT I — CONSCIENCE REJECTION (Pages 1–2)",
        "title": "1:30 AM Washroom Mirror Rejection & Bought Status at Breakfast",
        "setting": "Moonlit apartment balcony outside a warm-lit washroom mirror & crystal decanter.",
        "characters": "Story world: Lone Karthik (and wife Meera at breakfast). Foreground unseen narrators: @Me + Bala-Matha.",
        "narrator_separation_blocking": "STRICT SEPARATION: @Me and Bala-Matha stand outside on the moonlit balcony facing ONLY the camera; Karthik faces his washroom mirror inside, 100% unaware of the narrators.",
        "time_pause_mechanic": "Psychological mirror recoil showing how betraying integrity when unwatched triggers immediate self-rejection.",
        "dialogue_anchor": "No witness saw him—yet at one-thirty A.M., his own mirror rejects him! Drowning lost dignity only rots the soul.",
        "visual_asset": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_02_mirror_conscience_rejection.jpg",
        "ref_ingredient": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_02_mirror_conscience_rejection.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 3,
        "act": "ACT I — STUDIO PORTAL (Page 2)",
        "title": "White-Wall Zoom-Out: Duty (What) + Dignity (Integrity of How)",
        "setting": "Pure-white circular marble Karmic Genie Show amphitheater with brushed-gold '2. Earn with DIGNITY Always.'",
        "characters": "@Me, 4yo Bala-Rishi, and Bala-Matha on the central marble stage.",
        "narrator_separation_blocking": "Canonical studio host setting beside the dormant jeweled gold Genie lamp.",
        "time_pause_mechanic": "[WHITE-WALL ZOOM-OUT] onto the circular marble stage unveiling the Golden Axiom.",
        "dialogue_anchor": "Doing the right thing, at the right time, to the right people ALWAYS beats the easy thing in the dark!",
        "visual_asset": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_03_white_stage_dignity_portal.jpg",
        "ref_ingredient": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_03_white_stage_dignity_portal.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
            "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 4,
        "act": "ACT II — NATURE'S UNBOUGHT DIGNITY (Page 3)",
        "title": "Unstained Lotus, Upright Mountain Bamboo & Gentle Honeybee (100% Dignity)",
        "setting": "Sunlit morning stone path beside a white lotus pond and tall green mountain bamboo grove.",
        "characters": "Unseen narrators @Me + 4yo Bala-Rishi observing untouched nature.",
        "narrator_separation_blocking": "@Me and Bala-Rishi walk along the foreground stone path speaking exclusively to the lens.",
        "time_pause_mechanic": "[WHITE-WALL ZOOM-IN] into living nature demonstrating Thiruvalluvar's Maanam (Kural 969).",
        "dialogue_anchor": "Behold nature's unbought integrity: the lotus rises unstained, bamboo bends without breaking, and honeybees earn nectar without bruising petals!",
        "visual_asset": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_04_lotus_bamboo_nature_dignity.jpg",
        "ref_ingredient": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_04_lotus_bamboo_nature_dignity.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 5,
        "act": "ACT II — CHILDHOOD & YOUTH INTEGRITY (Page 4)",
        "title": "Age 4 Unshamed Play, Refusing an Exam Cheat Note & Proud of Honest Parents",
        "setting": "Open school veranda outside an arched classroom window where the teacher faces the blackboard.",
        "characters": "Story world: 13yo girl refusing cheat note; 22yo Arjun embracing tailor father. Foreground unseen narrators: @Me + 4yo Bala-Rishi.",
        "narrator_separation_blocking": "STRICT SEPARATION: @Me and Bala-Rishi stand on the outer veranda facing ONLY the camera; students inside the classroom look only at their desks, 100% unaware of the narrators.",
        "time_pause_mechanic": "Unwatched classroom integrity test when the teacher turns toward the blackboard.",
        "dialogue_anchor": "In school years, an honest score earned by your own sweat shines brighter than a hundred copied victories!",
        "visual_asset": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_05_age4_unshamed_play_youth_skill.jpg",
        "ref_ingredient": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_05_age4_unshamed_play_youth_skill.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 6,
        "act": "ACT II — ADULTHOOD PORUL & ARUL DIGNITY (Page 5)",
        "title": "Age 24 Unbuyable Spine, Spotless Porul (Samma Ajiva) & Sovereign Arul (Kural 241)",
        "setting": "Carved wooden courtyard arch outside a warm twilight South Indian Pooja sanctum.",
        "characters": "Story world: Mother lighting brass Kuthuvilakku lamp with husband and son. Foreground unseen narrators: @Me + Bala-Matha.",
        "narrator_separation_blocking": "STRICT SEPARATION: @Me and Bala-Matha stand outside the carved pillar arch facing ONLY the camera; the family inside folds palms toward the lamp, unaware of the narrators.",
        "time_pause_mechanic": "Golden Kuthuvilakku sanctuary glow illuminating 50% Clean Porul + 50% Sacred Arul.",
        "dialogue_anchor": "Thiruvalluvar crowns Arul the wealth of all wealths! A mother's sacred lamp and moral nurture hold royal dignity!",
        "visual_asset": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_06_age24_spine_porul_arul.jpg",
        "ref_ingredient": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_06_age24_spine_porul_arul.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 7,
        "act": "ACT II — LEADERSHIP & ELDER DIGNITY (Page 6)",
        "title": "Age 40 Putting Juniors' Names First, Age 54 Grateful Nandri & 60+ Silver Crown",
        "setting": "Garden stone border overlooking a sunlit Banyan courtyard.",
        "characters": "Story world: 55yo mentor thanking workers in Namaste & 76yo elder laughing with grandchild. Foreground unseen narrators: @Me + Bala-Matha.",
        "narrator_separation_blocking": "STRICT SEPARATION: @Me and Bala-Matha sit/stand along the foreground stone wall facing ONLY the camera; mentor, workers, and elder interact naturally behind them.",
        "time_pause_mechanic": "Warm golden morning continuity from upright bamboo leadership to humble Nandri.",
        "dialogue_anchor": "At fifty-four, boasting melts into grateful Nandri—and past sixty, an unstained conscience becomes your royal silver crown!",
        "visual_asset": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_07_shared_credit_elder_nandri.jpg",
        "ref_ingredient": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_07_shared_credit_elder_nandri.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 8,
        "act": "ACT III — FOUR UNWATCHED INTEGRITY PARABLES (Pages 7–8)",
        "title": "Returning Extra ₹500 Note at Dusk, Defending Absent Peer & Hidden Cradle Craft",
        "setting": "Rain-washed cobblestone lane at dusk opposite a lantern-lit elderly mango vendor's cart.",
        "characters": "Story world: Young commuter returning extra note to elderly vendor. Foreground unseen narrators: @Me + 4yo Bala-Rishi.",
        "narrator_separation_blocking": "STRICT SEPARATION: @Me and Bala-Rishi stand across the quiet curb facing ONLY the camera; commuter and elderly vendor interact under lantern glow, 100% unaware of the narrators.",
        "time_pause_mechanic": "Four real-world tests proving Right Thing + Right Time + Right People beats easy shortcuts.",
        "dialogue_anchor": "Test One: Returning an extra currency note to a tired vendor at dusk—nobody saw, yet Conscience smiled!",
        "visual_asset": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_08_unwatched_integrity_parables.jpg",
        "ref_ingredient": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_08_unwatched_integrity_parables.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 9,
        "act": "ACT V — 11:46 PM REDEMPTION STAND (Page 10)",
        "title": "Karthik Refuses the Unwatched Shortcut & Puts Junior Arjun's Name First",
        "setting": "Foreground dark-blue glass walkway outside the 11:46 PM amber-lit engineering room.",
        "characters": "Story world: Upright Karthik returning promotion offer to Vikram & logging Arjun's credit. Foreground unseen narrators: @Me + 4yo Bala-Rishi.",
        "narrator_separation_blocking": "STRICT SEPARATION: @Me and Bala-Rishi stand outside the glass corridor facing ONLY the camera; Karthik stands tall inside the office completely unaware of the narrators.",
        "time_pause_mechanic": "[TIME RESUMES FROM REWIND] Karthik chooses unbought bamboo integrity at 11:46 PM.",
        "dialogue_anchor": "Without anger or fear, he sets the pen down—refusing to endanger unseen families for any promotion on Earth!",
        "visual_asset": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_09_karthik_stands_tall_redemption.jpg",
        "ref_ingredient": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_09_karthik_stands_tall_redemption.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 10,
        "act": "ACT V — 9:00 AM BOARDROOM VINDICATION (Page 11)",
        "title": "Truth Protects Commuters, Lifts Young Arjun & Crowns Karthik with Unbought Trust",
        "setting": "Sunlit glass atrium balcony outside a bright 9:00 AM executive boardroom.",
        "characters": "Story world: Chief Safety Chairman shaking 25yo Arjun's hand while Karthik smiles half a step back. Foreground unseen narrators: @Me + 4yo Bala-Rishi.",
        "narrator_separation_blocking": "STRICT SEPARATION: @Me and Bala-Rishi stand on the outer atrium balcony facing ONLY the camera; Chairman, Arjun, and Karthik interact inside the glass boardroom unaware of the narrators.",
        "time_pause_mechanic": "Daylight vindication paired with the insight that the true victory already happened at midnight.",
        "dialogue_anchor": "External praise is just a bonus! His real victory happened at midnight—the instant he refused to sell his spine!",
        "visual_asset": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_10_boardroom_truth_wins.jpg",
        "ref_ingredient": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_10_boardroom_truth_wins.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 11,
        "act": "ACT V — CLEAN MIRROR & EMPEROR-LEVEL SLEEP (Page 12)",
        "title": "Simple Rice, Clean Midnight Mirror Sigh of Relief & Emperor-Level Sleep",
        "setting": "Open moonlit balcony veranda outside Karthik & Meera's serene bedroom.",
        "characters": "Story world: Karthik & Meera sleeping in deep unbroken peace. Foreground unseen narrators: @Me + Bala-Matha.",
        "narrator_separation_blocking": "STRICT SEPARATION: @Me and Bala-Matha stand on the outer veranda facing ONLY the camera; Karthik and Meera sleep peacefully inside the arched bedroom unaware of the narrators.",
        "time_pause_mechanic": "10/10 Conscience Peace contrasting Act I's 1:30 AM mirror torment.",
        "dialogue_anchor": "When nobody owns your conscience, no storm can steal your rest—tonight, unbought dignity sleeps like an emperor!",
        "visual_asset": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_11_emperor_peace_sleep.jpg",
        "ref_ingredient": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_11_emperor_peace_sleep.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 12,
        "act": "ACT VI & VII — CELESTIAL KARMIC GENIE & 35/70 MIRROR FINALE (Pages 13–14)",
        "title": "Awakening of the Celestial Maharishi Karmic Genie & Pillar #2 Locked in Gold",
        "setting": "Grand pure-white circular marble Karmic Genie Show amphitheater.",
        "characters": "Celestial Maharishi Karmic Genie floating cross-legged above the gold lamp + @Me, Bala-Rishi & Bala-Matha.",
        "narrator_separation_blocking": "Sacred studio finale with Pillar #1 (Duty) and Pillar #2 (Dignity) shining together on the pure-white wall.",
        "time_pause_mechanic": "Courteous Maharishi Genie blessing + 5-Question Tonight Mirror Audit (< 35/70 rule) + Episode 3 Discipline hook.",
        "dialogue_anchor": "Remember tomorrow morning: doing the right thing at the right time to the right people always wins!",
        "visual_asset": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_12_celestial_genie_dignity_finale.jpg",
        "ref_ingredient": "episodes/S01E02_Earn_With_Dignity_Always/storyboard/sb_e02_12_celestial_genie_dignity_finale.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v6_7d_saintly_genie_16x9.jpg",
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
        ],
        "include_me_avatar": True,
    },
]

BATCH_MAP = [
    (1, 5, "batch_01_midnight_shortcut_mirror_hook"),
    (6, 10, "batch_02_white_stage_lotus_bamboo"),
    (11, 16, "batch_03_youth_spine_porul_arul"),
    (17, 21, "batch_04_leadership_nandri_unwatched_tests_1_2"),
    (22, 26, "batch_05_unwatched_tests_3_4_sages_rewind"),
    (27, 32, "batch_06_karthik_bamboo_stand_emperor_sleep"),
    (33, 38, "batch_07_genie_awakening_mirror_audit"),
    (39, 43, "batch_08_homes_awakening_duty_dignity_lock"),
    (44, 46, "batch_09_arul_blessing_discipline_hook"),
    (47, 48, "batch_10_golden_memory_namaskaram_finale"),
]

OVERLAY_FOR_SHOT = {
    "ED01": "ov_ed_01_midnight_unwatched.png",
    "ED04": "ov_ed_02_mirror_conscience.png",
    "ED06": "ov_ed_03_white_stage_d2.png",
    "ED08": "ov_ed_03_white_stage_d2.png",
    "ED09": "ov_ed_04_nature_integrity.png",
    "ED11": "ov_ed_05_youth_integrity.png",
    "ED14": "ov_ed_06_spine_porul_arul.png",
    "ED16": "ov_ed_06_spine_porul_arul.png",
    "ED17": "ov_ed_07_shared_credit_nandri.png",
    "ED18": "ov_ed_07_shared_credit_nandri.png",
    "ED20": "ov_ed_08_four_unwatched_tests.png",
    "ED22": "ov_ed_08_four_unwatched_tests.png",
    "ED25": "ov_ed_09_eastern_sages_unite.png",
    "ED27": "ov_ed_10_karthik_bamboo_stand.png",
    "ED28": "ov_ed_10_karthik_bamboo_stand.png",
    "ED31": "ov_ed_11_emperor_peace_sleep.png",
    "ED32": "ov_ed_11_emperor_peace_sleep.png",
    "ED34": "ov_ed_12_genie_mirror_audit.png",
    "ED36": "ov_ed_12_genie_mirror_audit.png",
    "ED45": "ov_ed_03_white_stage_d2.png",
}


def get_batch(num: int) -> str:
    for lo, hi, bid in BATCH_MAP:
        if lo <= num <= hi:
            return bid
    raise ValueError(num)


def split_subtitle(line: str):
    clean = line.replace("*", "")
    words = clean.split()
    mid = len(words) // 2
    for offset in range(0, 4):
        for idx in (mid + offset, mid - offset):
            if 4 <= idx <= len(words) - 4 and any(
                words[idx - 1].endswith(p) for p in (",", "—", ":", ";", "!", "?")
            ):
                return [" ".join(words[:idx]), " ".join(words[idx:])]
    return [" ".join(words[:mid]), " ".join(words[mid:])]


def sanitize_for_flow(s: str) -> str:
    return s.replace("@Me", "Me").replace("@", "").replace("**", "").replace("`", "")


def export_all():
    md_text = SCREENPLAY_PATH.read_text(encoding="utf-8")

    storyboard_pkg = {
        "project_title": "The Karmic Genie Show — S01E02: Earn with DIGNITY Always. (Epic Movie Edition)",
        "series_format": "The 7D Way — Virtues & Divinity Theatrical Movie Series (White-Wall Portals + Strict Foreground Unseen Witness Narrators)",
        "target_platform": "Google Flow Storyboard Suite (MCP + CDP Port 9225/9222)",
        "account": "nagaraj957@gmail.com",
        "master_character_avatars": {
            "@Me": {
                "avatar_tag": "Me",
                "master_image": "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
                "canonical_look": "Exact likeness of @Me (swept-back dark hair, salt-and-pepper stubble, warm expressive eyes) wearing his tailored ivory-white bandhgala suit. STRICT NARRATOR ROLE: Speaks ONLY to the camera lens; never mixed up as a character inside the story.",
            },
            "Bala-Rishi": {
                "avatar_tag": "Bala-Rishi",
                "master_image": "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
                "canonical_look": "4-year-old boy sage Bala-Rishi (top-knot bun, Urdhva Pundra tilak, Rudraksha mala, cream silk kurta & golden-bordered shawl). STRICT NARRATOR ROLE: Speaks ONLY to the camera lens; unseen by story characters.",
            },
            "Bala-Matha": {
                "avatar_tag": "Bala-Matha",
                "master_image": "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
                "canonical_look": "Young divine girl sage Bala-Matha (vibhuti/kumkum on forehead, magenta-green silk pattu pavadai with golden zari border, fresh white jasmine garlands). STRICT NARRATOR ROLE: Speaks ONLY to the camera lens; unseen by story characters.",
            },
        },
        "signature_cinematic_mechanics": {
            "strict_narrator_separation_law": "Narrator (@Me) + ONE Child ONLY (Bala-Rishi OR Bala-Matha) stay strictly in an architecturally separated foreground/veranda witness zone addressing ONLY the camera/viewer—NEVER mixed up as story characters, never touching story props, and 100% unseen by story characters.",
            "bullet_time_freeze_frame_walkthrough": "[SCENE TIME-PAUSE] freezes the 11:45 PM signature line in 3D bullet-time while unseen foreground narrators @Me + 1 Child address the viewer.",
            "white_wall_zoom_portal": "Pure-white circular marble Karmic Genie Show studio wall acts as a seamless zoom-in/zoom-out cinema portal.",
        },
        "episode_2_storyboard_scenes": STORYBOARD_SCENES,
    }

    sb_out = EP_DIR / "GOOGLE_FLOW_STORYBOARD_PACKAGE_S01E02.json"
    sb_out.write_text(json.dumps(storyboard_pkg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    page_sections = re.split(r"(?=^## PAGE \d+\b)", md_text, flags=re.M)[1:]
    shots_list = []
    for p_sec in page_sections:
        p_num = int(re.match(r"^## PAGE (\d+)\b", p_sec).group(1))
        shot_blocks = re.split(r"(?=^### \[SHOT ED\d+)", p_sec, flags=re.M)[1:]
        for sb in shot_blocks:
            sid = re.match(r"^### \[SHOT (ED\d+)", sb).group(1)
            snum = int(sid[2:])
            sb_ref = re.search(r"- \*\*Storyboard Reference:\*\* `(.*?)`", sb).group(1)
            loc = re.search(r"- \*\*Location:\*\* (.*)", sb).group(1).strip()
            nb = re.search(r"- \*\*Narrator Separation Blocking:\*\* (.*)", sb).group(1).strip()
            vis = re.search(r"- \*\*Visual Action:\*\* (.*)", sb).group(1).strip()
            m_dlg = re.search(r"- \*\*Dialogue \((.*?)\):\*\*\n\s*> \"(.*?)\"", sb)
            sp_raw, spoken_raw = m_dlg.group(1), m_dlg.group(2)

            spoken_clean = spoken_raw.replace("*", "")
            w_count = len(re.findall(r"[A-Za-z0-9'-]+", spoken_clean))

            if "Celestial Karmic Genie" in sp_raw:
                speaker_mode = "genie"
                speaker_voice = "celestial_genie"
                cast_rule = "Celestial Maharishi Karmic Genie + Studio Trinity"
                include_me = False
            elif "Bala-Rishi" in sp_raw:
                speaker_mode = "human"
                speaker_voice = "bala_rishi"
                cast_rule = "Me + 4yo Bala-Rishi (Strictly Unseen Foreground Narrators — Never Story Characters)"
                include_me = True
            elif "Bala-Matha" in sp_raw:
                speaker_mode = "human"
                speaker_voice = "bala_matha"
                cast_rule = "Me + Bala-Matha (Strictly Unseen Foreground Narrators — Never Story Characters)"
                include_me = True
            else:
                speaker_mode = "human"
                speaker_voice = "host_me"
                if "Bala-Matha" in nb and "Bala-Rishi" not in nb:
                    cast_rule = "Me + Bala-Matha (Strictly Unseen Foreground Narrators — Never Story Characters)"
                elif "Bala-Rishi" in nb and "Bala-Matha" not in nb:
                    cast_rule = "Me + 4yo Bala-Rishi (Strictly Unseen Foreground Narrators — Never Story Characters)"
                else:
                    cast_rule = "Me + Studio Trinity (Pure-White Circular Marble Stage)"
                include_me = True

            nb_clean = sanitize_for_flow(nb)
            vis_clean = sanitize_for_flow(vis)
            flow_visual = (
                f"65mm photorealistic 16:9 cinema shot ({loc}). "
                f"STRICT NARRATOR SEPARATION: {nb_clean} "
                f"STORY ACTION: {vis_clean} "
                f"Story characters never look at or interact with the foreground narrators."
            )
            assert "@" not in flow_visual, f"Literal @ found in {sid}"

            ref_rel = f"episodes/S01E02_Earn_With_Dignity_Always/storyboard/{sb_ref}"
            assert (REPO_DIR / ref_rel).exists(), f"Missing storyboard plate {ref_rel}"

            kws = [
                w.strip(".,!?;:\"'()—").lower()
                for w in spoken_clean.split()
                if len(w.strip(".,!?;:\"'()—")) >= 5
            ][:5]
            b_id = get_batch(snum)
            shots_list.append(
                {
                    "slot_id": sid,
                    "batch_id": b_id,
                    "file_prefix": b_id,
                    "page": p_num,
                    "cast_rule": cast_rule,
                    "narrator_separation_verified": True,
                    "include_me": include_me,
                    "ref_image": ref_rel,
                    "speaker_mode": speaker_mode,
                    "speaker_voice": speaker_voice,
                    "overlay_png": OVERLAY_FOR_SHOT.get(sid),
                    "pause_after_s": 0.25,
                    "keywords": kws,
                    "visual": flow_visual,
                    "spoken": spoken_clean,
                    "word_count": w_count,
                    "subtitles": split_subtitle(spoken_clean),
                }
            )

    assert len(shots_list) == 48, f"Expected 48 shots, got {len(shots_list)}"

    ledger = {
        "episode": "S01E02",
        "series": "The Karmic Genie Show — The 7D Way (Virtues & Divinity)",
        "title": "2. Earn with DIGNITY Always.",
        "screenplay_path": "episodes/S01E02_Earn_With_Dignity_Always/S01E02_14_Page_Master_Screenplay_Earn_With_Dignity_Always.md",
        "total_batches": 10,
        "total_shots": 48,
        "target_aspect_ratio": "16:9",
        "clip_duration_seconds": 8,
        "estimated_master_runtime": "~07:45 (17.6s 7D Cold Open + 48 cinema shots ED01..ED48 + 14.5s Finale Card)",
        "rules_enforced": [
            "Virtue #2 Focus: '2. Earn with DIGNITY Always.' (Dignity = Unbought Integrity)",
            "Golden Moral Law: Doing the right thing at the right time to the right people ALWAYS wins over doing the easy thing when no one watches",
            "IRONCLAD NARRATOR SEPARATION: Narrators (Me, 4yo Bala-Rishi, Bala-Matha) stay strictly unseen foreground/stage narrators addressing ONLY the camera—never mixed up as characters in the story",
            "11:45 PM Unwatched Bridge-Safety Crossroads (Shadow Timeline 1:30 AM Mirror Conscience Rejection vs. 11:46 PM Upright Bamboo Stand & Putting Junior Arjun's Name First -> Emperor-Level Sleep)",
            "Lifecycle Integrity across Nature (Lotus, Bamboo, Honeybee) & Human Stages (Age 4 Unshamed Play -> Honest Exams -> Age 24 Unbuyable Spine -> Clean Porul & Royal Arul -> Age 40 Shared Credit -> Age 54 Grateful Nandri -> 60+ Silver Crown)",
            "Zero literal @ symbol inside Google Flow visual prompts + Official Me/Bala-Rishi/Bala-Matha reference ingredients",
        ],
        "shots": shots_list,
    }

    ledger_out = EP_DIR / "s01e02_48_shot_flow_ledger.json"
    ledger_out.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ Wrote {sb_out.relative_to(REPO_DIR)} ({len(STORYBOARD_SCENES)} scenes)")
    print(f"✅ Wrote {ledger_out.relative_to(REPO_DIR)} ({len(shots_list)} shots across 10 batches)")


if __name__ == "__main__":
    export_all()
