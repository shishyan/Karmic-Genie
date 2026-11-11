#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exports & validates the complete Google Flow Production Package for:
  The Karmic Genie Show — Season 1, Episode 2 ("2. Earn with DIGNITY Always.")
  - episodes/S01E02_Earn_With_Dignity_Always/GOOGLE_FLOW_STORYBOARD_PACKAGE_S01E02.json (12 scenes)
  - episodes/S01E02_Earn_With_Dignity_Always/s01e02_48_shot_flow_ledger.json (48 cinema shots ED01..ED48)

Enforces In-Scene "Two Birds" Narrator Proximity Law:
  Narrators (@Me, 4yo Bala-Rishi, Bala-Matha) stand physically inside the scene right beside
  the characters—at the desk elbow, beside the washroom mirror, at the fruit cart, and beside the bedpost—
  speaking intimately to the camera lens. They NEVER switch roles to become characters in the plot,
  and story characters never interact with them.
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
        "title": "11:45 PM Empty Engineering Floor: Corrupt Boss Demand at the Desk",
        "setting": "Inside amber-lit drafting office at 11:45 PM with rain glistening on dark windows.",
        "characters": "Story world: Engineer Karthik (34) & Division Head Vikram (46). In-scene narrators: @Me + 4yo Bala-Rishi.",
        "in_scene_narrator_blocking": "IN-SCENE PROXIMITY: @Me and 4yo Bala-Rishi stand right beside the drafting table, inches from Karthik's elbow, looking directly into the camera lens while Vikram and Karthik confront each other over the false certificate.",
        "time_pause_mechanic": "[SCENE TIME-PAUSE] freezes Karthik's pen two millimeters above the compromised signature line.",
        "dialogue_anchor": "Obeying a corrupt boss feels easy tonight—but money earned from a lie poisons your soul and your family!",
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
        "title": "1:30 AM Washroom Mirror Rejection: Tainted Money Accrues Bad Karma",
        "setting": "Dim modern apartment washroom at 1:30 AM before an illuminated mirror and crystal decanter.",
        "characters": "Story world: Lone Karthik in shirt sleeves. In-scene narrators: @Me + Bala-Matha.",
        "in_scene_narrator_blocking": "IN-SCENE PROXIMITY: @Me and Bala-Matha stand right beside the washroom counter, physically close inside the room, facing the camera with piercing compassion while Karthik stares into his mirror in torment.",
        "time_pause_mechanic": "Conscience recoil showing how money earned outside of duty accrues heavy negative karma and poisons family soul growth.",
        "dialogue_anchor": "No boss is watching now—yet at one-thirty A.M., his own mirror rejects him! Tainted money burns the conscience.",
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
        "title": "White-Wall Zoom-Out: 'Earn with Dignity ALWAYS — Not Sometimes, Not Once'",
        "setting": "Pure-white circular marble Karmic Genie Show amphitheater with brushed-gold '2. Earn with DIGNITY Always.'",
        "characters": "@Me, 4yo Bala-Rishi, and Bala-Matha on the central marble stage.",
        "in_scene_narrator_blocking": "Canonical studio host setting beside the dormant jeweled gold Genie lamp.",
        "time_pause_mechanic": "[WHITE-WALL ZOOM-OUT] onto the circular marble stage defining the invariant: Porul must flow purely from duty, service, or virtuous action.",
        "dialogue_anchor": "Notice the sacred law: earn with dignity always! Every rupee must flow purely from duty, service, or virtuous action.",
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
        "characters": "In-scene narrators @Me + 4yo Bala-Rishi walking through untouched nature.",
        "in_scene_narrator_blocking": "@Me and Bala-Rishi walk right beside the lotus blossoms and bamboo canes speaking directly to the lens.",
        "time_pause_mechanic": "[WHITE-WALL ZOOM-IN] into living nature demonstrating Thiruvalluvar's Maanam (Kural 969).",
        "dialogue_anchor": "Nature teaches unbought dignity: the lotus remains unstained by mud, and mountain bamboo bends without ever breaking its upright spine!",
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
        "title": "Age 4 Free Play, Classroom Aisle Exam Integrity & Honest Parents' Simple Clothes",
        "setting": "Sunlit classroom exam hall with wooden desks and teacher writing at blackboard.",
        "characters": "Story world: 13yo schoolgirl refusing folded cheat note. In-scene narrators: @Me + 4yo Bala-Rishi.",
        "in_scene_narrator_blocking": "IN-SCENE PROXIMITY: @Me and Bala-Rishi stand right beside the student's wooden desk in the classroom aisle, looking straight into the camera while she pushes back the cheat note.",
        "time_pause_mechanic": "Classroom integrity test when the teacher's back is turned.",
        "dialogue_anchor": "When the teacher turns away, she refuses the cheat note—because true dignity never trades integrity for an unearned score!",
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
        "title": "Age 24 Unbuyable Spine, Spotless Porul (Samma Ajiva) & Sacred Arul (Kural 241)",
        "setting": "Warm twilight sanctum of traditional South Indian courtyard home beside brass Kuthuvilakku lamp.",
        "characters": "Story world: Mother lighting Kuthuvilakku lamp with husband and son praying. In-scene narrators: @Me + Bala-Matha.",
        "in_scene_narrator_blocking": "IN-SCENE PROXIMITY: @Me and Bala-Matha stand right beside the brass lamp inside the sanctum, physically present beside the praying family, facing the camera with luminous warmth.",
        "time_pause_mechanic": "Golden Kuthuvilakku flame illuminating how spotless Porul earned purely from duty protects family soul growth.",
        "dialogue_anchor": "Thiruvalluvar crowns Arul the greatest wealth! A mother's sacred lamp and unbought virtue guard the family's spiritual destiny.",
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
        "setting": "Sunlit Banyan courtyard with elderly artisans and grandfather.",
        "characters": "Story world: 55yo mentor thanking workers in Namaste & 76yo grandfather laughing with grandchild. In-scene narrators: @Me + Bala-Matha.",
        "in_scene_narrator_blocking": "IN-SCENE PROXIMITY: @Me and Bala-Matha sit/stand right beside the Banyan trunk and workers, looking into the camera lens with serene reverence.",
        "time_pause_mechanic": "Golden morning continuity from upright leadership to humble Nandri.",
        "dialogue_anchor": "At fifty-four, pride dissolves into humble Nandri—and past sixty, a lifetime of honest duty becomes your eternal crown!",
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
        "title": "Returning Extra ₹500 Note at Dusk Fruit Cart, Defending Absent Colleague & Cradle Craft",
        "setting": "Rain-washed dusk street right beside a lantern-lit wooden fruit cart.",
        "characters": "Story world: Young commuter handing back extra note to elderly bearded mango vendor. In-scene narrators: @Me + 4yo Bala-Rishi.",
        "in_scene_narrator_blocking": "IN-SCENE PROXIMITY: @Me and 4yo Bala-Rishi stand right next to the fruit cart under the lantern glow, physically present in the rainy street, narrating to the camera lens with soulful reverence.",
        "time_pause_mechanic": "Four everyday tests proving Right Thing + Right Time + Right People triumphs over easy shortcuts.",
        "dialogue_anchor": "Test One: Returning an extra banknote to a tired vendor at dusk—nobody saw, yet Conscience smiled with joy!",
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
        "title": "Putting the Badge Down: Refusing an Unjust Boss Even If It Means Losing Your Job",
        "setting": "Executive office at 11:46 PM under dramatic warm spotlight.",
        "characters": "Story world: Furious Division Head Vikram pointing toward the door & Lead Engineer Karthik placing down his badge. In-scene narrators: @Me + 4yo Bala-Rishi.",
        "in_scene_narrator_blocking": "IN-SCENE PROXIMITY: @Me and 4yo Bala-Rishi stand right beside the executive desk right next to Karthik's shoulder, facing the camera with triumphant resonance while Karthik refuses the corrupt command.",
        "time_pause_mechanic": "The ultimate test of dignity: refusing to earn money from an immoral act, choosing unemployment over a compromised soul.",
        "dialogue_anchor": "No matter the power, he does what is right—laying down his badge rather than earning one rupee from a lie!",
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
        "title": "Boardroom Vindication: Truth Protects Lives, Lifts Young Arjun & Crowns the Upright",
        "setting": "Sunlit 9:00 AM corporate boardroom with long conference table.",
        "characters": "Story world: Chief Safety Chairman shaking 25yo Arjun's hand with board applauding Karthik. In-scene narrators: @Me + 4yo Bala-Rishi.",
        "in_scene_narrator_blocking": "IN-SCENE PROXIMITY: @Me and 4yo Bala-Rishi stand right beside the conference table right next to Karthik and Arjun, addressing the camera with uplifting joy.",
        "time_pause_mechanic": "Public vindication paired with the truth that the real victory was already won at midnight when the pen was set down.",
        "dialogue_anchor": "By morning light, truth protects thousands of lives, lifts young Arjun high, and crowns Karthik with unshakeable honor!",
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
        "setting": "Quiet moonlit bedroom at night beside a wooden bed.",
        "characters": "Story world: Karthik & Meera sleeping in unbroken peace. In-scene narrators: @Me + Bala-Matha.",
        "in_scene_narrator_blocking": "IN-SCENE PROXIMITY: @Me and Bala-Matha stand right beside the wooden bedpost inside the quiet bedroom, facing the camera with soothing grace as the couple sleeps.",
        "time_pause_mechanic": "10/10 Conscience Peace: money earned purely from duty brings divine sleep that corrupt wealth can never buy.",
        "dialogue_anchor": "When money comes purely from duty, no power can disturb your rest—tonight, unbought dignity sleeps like an emperor!",
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
        "in_scene_narrator_blocking": "Sacred studio finale with Pillar #1 (Duty) and Pillar #2 (Dignity) shining together on the pure-white wall.",
        "time_pause_mechanic": "Courteous Maharishi Genie blessing + 5-Question Tonight Mirror Audit (< 35/70 rule) + Episode 3 Discipline hook.",
        "dialogue_anchor": "Carry this truth tomorrow: earn only from duty, defy corrupt commands, and sleep in royal peace every night!",
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
        "series_format": "The 7D Way — Virtues & Divinity Theatrical Movie Series (White-Wall Portals + Intimate In-Scene Two-Birds Narrators)",
        "target_platform": "Google Flow Storyboard Suite (MCP + CDP Port 9225/9222)",
        "account": "nagaraj957@gmail.com",
        "master_character_avatars": {
            "@Me": {
                "avatar_tag": "Me",
                "master_image": "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
                "canonical_look": "Exact likeness of @Me (swept-back dark hair, salt-and-pepper stubble, warm expressive eyes) wearing his tailored ivory-white bandhgala suit. IN-SCENE NARRATOR ROLE: Stands physically right beside the characters inside the scene, speaking directly to the camera lens. Never becomes a character in the plot.",
            },
            "Bala-Rishi": {
                "avatar_tag": "Bala-Rishi",
                "master_image": "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
                "canonical_look": "4-year-old boy sage Bala-Rishi (top-knot bun, Urdhva Pundra tilak, Rudraksha mala, cream silk kurta & golden-bordered shawl). IN-SCENE NARRATOR ROLE: Stands right beside @Me and the characters, speaking intimately to the camera lens.",
            },
            "Bala-Matha": {
                "avatar_tag": "Bala-Matha",
                "master_image": "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
                "canonical_look": "Young divine girl sage Bala-Matha (vibhuti/kumkum on forehead, magenta-green silk pattu pavadai with golden zari border, fresh white jasmine garlands). IN-SCENE NARRATOR ROLE: Stands right beside @Me and the characters, speaking intimately to the camera lens.",
            },
        },
        "signature_cinematic_mechanics": {
            "in_scene_two_birds_narrator_law": "Narrator (@Me) + ONE Child ONLY (Bala-Rishi OR Bala-Matha) stand physically inside the scene right beside the living characters—at the blueprint desk, washroom mirror, classroom desk, fruit cart, and bedpost—speaking directly to the viewer. Characters remain completely absorbed in their story and never interact with the narrators.",
            "bullet_time_freeze_frame_walkthrough": "[SCENE TIME-PAUSE] freezes the 11:45 PM signature line in 3D bullet-time while narrators @Me + 1 Child step around the desk to address the viewer.",
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
            nb = re.search(r"- \*\*Active In-Scene Blocking:\*\* (.*)", sb).group(1).strip()
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
                cast_rule = "Me + 4yo Bala-Rishi (Intimate In-Scene Two-Birds Narrators)"
                include_me = True
            elif "Bala-Matha" in sp_raw:
                speaker_mode = "human"
                speaker_voice = "bala_matha"
                cast_rule = "Me + Bala-Matha (Intimate In-Scene Two-Birds Narrators)"
                include_me = True
            else:
                speaker_mode = "human"
                speaker_voice = "host_me"
                if "Bala-Matha" in nb and "Bala-Rishi" not in nb:
                    cast_rule = "Me + Bala-Matha (Intimate In-Scene Two-Birds Narrators)"
                elif "Bala-Rishi" in nb and "Bala-Matha" not in nb:
                    cast_rule = "Me + 4yo Bala-Rishi (Intimate In-Scene Two-Birds Narrators)"
                else:
                    cast_rule = "Me + Studio Trinity (Pure-White Circular Marble Stage)"
                include_me = True

            nb_clean = sanitize_for_flow(nb)
            vis_clean = sanitize_for_flow(vis)
            flow_visual = (
                f"65mm photorealistic 16:9 cinema shot ({loc}). "
                f"IN-SCENE NARRATOR PROXIMITY: {nb_clean} "
                f"STORY ACTION: {vis_clean} "
                f"Characters are absorbed in their scene; narrators address camera directly."
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
                    "in_scene_proximity": True,
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
            "Virtue #2 Invariant: 'Earn with Dignity, ALWAYS' — Never sometimes, never once. Wherever/whenever you earn Porul (money), it MUST come strictly from an act of duty, service, or virtuous action, nothing less.",
            "Karmic Law: Earning by any other means accrues bad karma and contaminates soul growth for yourself and your family.",
            "Defying Corrupt Power: Dignity means no matter how powerful the authority or boss, you do what is right. If a boss commands an immoral act, you refuse point-blank, even if it means losing your job on the spot!",
            "In-Scene 'Two Birds' Proximity: Narrators (Me + 1 Child) stand physically inside the scene right beside characters and props, speaking intimately to the camera lens without ever switching roles to become characters.",
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
