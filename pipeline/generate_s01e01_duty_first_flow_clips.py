#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resumable Google Flow ULTRA (Omni 1.1 Flash / Veo 3.1, 16:9 Widescreen) 48-Shot Full-Film Generator
for The Karmic Genie Show — Season 1, Episode 1 (~7m 45s Epic Theatrical Film):
  "RESPECT YOUR DUTY FIRST" (Virtue #1 of The 7D Way — Virtues & Divinity Series)

Aligned 100% with User Strategy & Creative Architecture:
  1. Readable 14-Page Epic Movie Structure (`S01E01_14_Page_Master_Screenplay_Respect_Your_Duty_First.md`),
     preserving earlier scripts in `BACKUP_*`.
  2. True Definition of Duty: A task whose neglect triggers guilt inside your ever-watching Conscience
     (*Manasatchi*) — across all living beings (Banyan, Honeybee, River) and all human ages (Age 4 Play,
     Age 8–16 50/50, Age 24 Independent Thinking, Male 50% Porul, Female 50% Arul + Pooja, Age 54 Thanking,
     Age 60+ Para-Soul Canopy).
  3. After Duty -> "DO THE THINGS THAT ONLY YOU CAN DO" (7 distinct cinematic scenes + Daily Time Law:
     Duty First -> What Only You Can Do -> NOTHING MORE).
  4. "Respect Your Duty First" AND "Respect Everyone Else's Duty" (never demean any honest worker).
  5. Duty to Strangers, Public & Environment — anchored by the Two-Day Car Accident Master Parable
     (Day 1 peaceful sleep -> Day 2 caused accident & fled -> 2:30 AM sleepless guilt -> Wife's "You should
     have helped him!" -> Redemption in the rain -> Deep sigh of relief -> Blissful good night's sleep).
  6. Active "Two Birds" In-Scene Narrators (`Me` + ONE Child ONLY per movie scene: `Bala-Rishi` OR `Bala-Matha`),
     3D Bullet-Time `[SCENE TIME-PAUSE]`, White-Wall Zoom-In/Zoom-Out portals, and `Me` Google Flow Avatar chip
     with ZERO literal `@` in ProseMirror text.

Usage (on local workstation with Chrome open at https://flow.google.com/u/0/ on `--remote-debugging-port=9225`):
  python3 pipeline/generate_s01e01_duty_first_flow_clips.py                 # Run/resume all 10 batches (48 clips)
  python3 pipeline/generate_s01e01_duty_first_flow_clips.py batch_01        # Run a specific batch
  python3 pipeline/generate_s01e01_duty_first_flow_clips.py --export-ledger # Export 48-shot JSON + Storyboard Package
"""

import json
import os
import shutil
import sys
import time
import urllib.request
from pathlib import Path

try:
    import websocket
except ImportError:
    websocket = None

CDP_PORTS = [int(os.environ.get("FLOW_CDP_PORT", "9225")), 9222]
REPO_DIR = Path(__file__).resolve().parent.parent
EP_DIR = REPO_DIR / "episodes" / "S01E01_Respect_Your_Duty_First"
SB_DIR = EP_DIR / "storyboard"
EP_CLIPS_DIR = EP_DIR / "flow_16x9_clips"
LEDGER_JSON_PATH = EP_DIR / "s01e01_48_shot_flow_ledger.json"
PACKAGE_JSON_PATH = REPO_DIR / "GOOGLE_FLOW_STORYBOARD_PACKAGE_S01E01.json"
DL_DIR = Path.home() / "Downloads"


STORYBOARD_SCENES = [
    {
        "scene": 1,
        "act": "ACT I — COLD OPEN (Page 1)",
        "title": "Day 1 vs. Day 2 Monsoon Scooter Accident (3D Bullet-Time Time-Pause)",
        "setting": "Rain-slicked dusk suburban bend in South India; frozen raindrops & amber brake-light reflections.",
        "characters": "Commuter driver Raghav, fallen scooter rider, Narrator @Me (ivory bandhgala) + 4yo Bala-Rishi.",
        "two_birds_blocking": "NARRATOR + 1 CHILD (Bala-Rishi): @Me and 4yo Bala-Rishi walk calmly through suspended raindrops beside the open sedan door and wounded scooter rider.",
        "time_pause_mechanic": "[SCENE TIME-PAUSE] freezes the monsoon drizzle right as Raghav considers driving away after causing the minor clip.",
        "dialogue_anchor": "Next evening—same minor accident. Except tonight, his car caused it, and nobody else is around.",
        "visual_asset": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_01_accident_day2_pause.jpg",
        "ref_ingredient": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_01_accident_day2_pause.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 2,
        "act": "ACT I — CONSCIENCE AWAKENS (Page 2)",
        "title": "2:30 AM Sleepless Guilt & The Wife's Mirror ('You Should Have Helped Him!')",
        "setting": "Moonlit South Indian bedroom at 2:30 AM with warm amber bedside lamp.",
        "characters": "Sleepless Raghav, his wife Ananya, Narrator @Me + Bala-Matha.",
        "two_birds_blocking": "NARRATOR + 1 CHILD (Bala-Matha): @Me and Bala-Matha stand quietly in soft golden conscience light by the bedpost as Ananya speaks the piercing truth.",
        "time_pause_mechanic": "Intimate psychological stillness contrasting Day 1's effortless sleep with Day 2's burning guilt.",
        "dialogue_anchor": "Yesterday his wife said nothing. Tonight she cries, 'You should have helped him!' Why? Because helping became HIS DUTY!",
        "visual_asset": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_02_sleepless_conscience.jpg",
        "ref_ingredient": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_02_sleepless_conscience.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 3,
        "act": "ACT I — STUDIO PORTAL (Page 2)",
        "title": "White-Wall Zoom-Out to The Karmic Genie Show Circular Marble Stage",
        "setting": "Pure-white circular marble amphitheater with brushed-gold '1. Respect Your DUTY First.' inscription & dormant gold Genie lamp.",
        "characters": "@Me, 4yo Bala-Rishi, and Bala-Matha on the central marble stage.",
        "two_birds_blocking": "The Sacred Trinity welcomes the audience and defines True Duty as the task whose neglect awakens guilt inside Conscience (Manasatchi).",
        "time_pause_mechanic": "[WHITE-WALL ZOOM-OUT] from bedroom window straight onto the luminous circular marble stage.",
        "dialogue_anchor": "True Duty is never an office contract. Duty is the sacred task whose neglect awakens guilt inside your Conscience!",
        "visual_asset": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_03_white_stage_duty_portal.jpg",
        "ref_ingredient": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_03_white_stage_duty_portal.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
            "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 4,
        "act": "ACT II — NATURE & CHILDHOOD DUTY (Pages 3–4)",
        "title": "Banyan, Bee & River (100% Duty) + Age 4 Barefoot Outdoor Play",
        "setting": "Golden sunlit sacred Banyan tree with aerial roots, lotus honeybees, and crystal river puddles.",
        "characters": "4-year-old child splashing barefoot in golden puddles, Narrator @Me + 4yo Bala-Rishi.",
        "two_birds_blocking": "NARRATOR + 1 CHILD (Bala-Rishi): @Me and Bala-Rishi walk barefoot along the sunlit riverbank right beside the playing 4-year-old child.",
        "time_pause_mechanic": "[WHITE-WALL ZOOM-IN] into living nature showing 100% unapplauded duty across Banyan, Bee, River, and Childhood Play.",
        "dialogue_anchor": "At age four, a child's one hundred percent duty is pure outdoor PLAY—building fearless lungs, bones, and vitality!",
        "visual_asset": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_04_banyan_age4_play.jpg",
        "ref_ingredient": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_04_banyan_age4_play.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 5,
        "act": "ACT II — HOUSEHOLDER ILLARAM (Page 5)",
        "title": "Sacred Family Duty: Father's 50% Spotless Porul & Mother's 50% Arul Pooja Lamp",
        "setting": "Traditional-modern South Indian courtyard home at twilight glowing with a brass Kuthuvilakku oil lamp.",
        "characters": "Mother lighting the sacred Pooja lamp with child, Father arriving warmly with honest provision, Narrator @Me + Bala-Matha.",
        "two_birds_blocking": "NARRATOR + 1 CHILD (Bala-Matha): @Me and Bala-Matha walk gently through the courtyard beside the glowing Kuthuvilakku lamp.",
        "time_pause_mechanic": "Warm golden oil-lamp illumination revealing why loving Family Life (Karma Margam / Illaram) is both safest and fastest for Soul Growth.",
        "dialogue_anchor": "And a mother's sacred Arul—nurturing life and lighting the daily Pooja lamp—turns four brick walls into a living temple!",
        "visual_asset": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_05_porul_arul_home.jpg",
        "ref_ingredient": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_05_porul_arul_home.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 6,
        "act": "ACT III — ONLY YOU CAN DO #1 (Page 7)",
        "title": "Things ONLY YOU Can Do (Scene 1 of 7): Being Father to Your Own Child",
        "setting": "Rain-washed sunlit cobblestone tree-lined walkway in golden afternoon light.",
        "characters": "5-year-old boy sprinting into his kneeling father's open arms, Narrator @Me + 4yo Bala-Rishi.",
        "two_birds_blocking": "NARRATOR + 1 CHILD (Bala-Rishi): @Me and Bala-Rishi walk in stride right beside the joyful reunion.",
        "time_pause_mechanic": "Slow-motion emotional embrace proving 'Only You Can Do' is sacred responsibility, never arrogance.",
        "dialogue_anchor": "Scene One: Ten thousand engineers can replace your office chair—not one human on Earth can be father to your child!",
        "visual_asset": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_06_only_you_father_hug.jpg",
        "ref_ingredient": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_06_only_you_father_hug.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 7,
        "act": "ACT III — ONLY YOU CAN DO #3 & ELDER NANDRI (Pages 6–7)",
        "title": "Things ONLY YOU Can Do (Scene 3 of 7): Kneeling Before Your Aging Parents",
        "setting": "Warm pillared ancestral veranda at golden sunset with brass lantern glow.",
        "characters": "40-year-old son holding his 78-year-old father and mother's hands, Narrator @Me + Bala-Matha.",
        "two_birds_blocking": "NARRATOR + 1 CHILD (Bala-Matha): @Me and Bala-Matha walk softly beside the carved teak veranda pillars.",
        "time_pause_mechanic": "Golden sunset glow illuminating tears of parental joy that bank transfers alone can never buy.",
        "dialogue_anchor": "Scene Three: Money hires nurses, never kinship—your aging parents' eyes wait at the gate only for you, their child!",
        "visual_asset": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_07_only_you_elder_parents.jpg",
        "ref_ingredient": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_07_only_you_elder_parents.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 8,
        "act": "ACT III–IV — WHITE-WALL PORTAL & DAILY TIME LAW (Pages 7–9)",
        "title": "White-Wall Portal Transition: Duty First -> What Only You Can Do -> Nothing Else",
        "setting": "Luminous curved white marble Karmic Genie Show portal opening into lived human dharma.",
        "characters": "@Me, 4yo Bala-Rishi, and Bala-Matha before the glowing White Wall aperture.",
        "two_birds_blocking": "@Me proclaims the Iron Daily Law of Human Time before stepping back through the White Wall.",
        "time_pause_mechanic": "[WHITE-WALL PORTAL] bridging the 7 'Only You Can Do' scenes with 'Respect Everyone Else's Duty'.",
        "dialogue_anchor": "Every day: do your Duty first, then what ONLY YOU can do—nothing else! Anything outside those two wastes your priceless life!",
        "visual_asset": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_08_white_wall_portal_transition.jpg",
        "ref_ingredient": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_08_white_wall_portal_transition.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
            "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 9,
        "act": "ACT IV — RESPECT EVERYONE ELSE'S DUTY (Page 10)",
        "title": "Dawn Boulevard Namaste: Honoring the Street Cleaner & Night Watchman",
        "setting": "Golden sunrise tree-lined Indian avenue bathed in volumetric morning rays.",
        "characters": "Car commuter bowing in respectful Namaste to an elderly municipal street cleaner, Narrator @Me + Bala-Matha.",
        "two_birds_blocking": "NARRATOR + 1 CHILD (Bala-Matha): @Me and Bala-Matha pause the honking hand, then smile beside the mutual Namaste bow.",
        "time_pause_mechanic": "[SCENE TIME-PAUSE] freezes the impatient horn before transforming arrogance into mutual reverence.",
        "dialogue_anchor": "Before the Divine, a street cleaner or night watchman fulfilling honest duty at ten-on-ten stands as noble as any king!",
        "visual_asset": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_09_respect_everyones_duty.jpg",
        "ref_ingredient": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_09_respect_everyones_duty.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 10,
        "act": "ACT V — PUBLIC DUTY & REDEMPTION IN THE RAIN (Pages 11–12)",
        "title": "Day 2 Rewind: Stopping in the Rain to Bandage & Help the Wounded Stranger",
        "setting": "Dusk rain-wet avenue as golden sunset rays break through parting monsoon clouds; hazard lights & ambulance arriving.",
        "characters": "Raghav kneeling with umbrella and first-aid cloth tending the injured scooter rider, Narrator @Me + 4yo Bala-Rishi.",
        "two_birds_blocking": "NARRATOR + 1 CHILD (Bala-Rishi): @Me rests a warm hand on Bala-Rishi's shoulder right beside the redemptive roadside rescue.",
        "time_pause_mechanic": "Golden storm-break rewind transforming Day 2's guilty flight into courageous public duty.",
        "dialogue_anchor": "He parks, runs into the rain, bandages the stranger's knee, and stays beside him until medical hands take over!",
        "visual_asset": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_10_redemption_help_rider.jpg",
        "ref_ingredient": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_10_redemption_help_rider.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 11,
        "act": "ACT V — THE REWARD OF CONSCIENCE (Page 12)",
        "title": "The Full-Chest Sigh of Relief & A Blissful Good Night's Sleep",
        "setting": "Serene lamp-lit South Indian bedroom at night filled with tranquil peace.",
        "characters": "Raghav and Ananya sleeping deeply and peacefully with gentle smiles, Narrator @Me + Bala-Matha.",
        "two_birds_blocking": "NARRATOR + 1 CHILD (Bala-Matha): @Me and Bala-Matha smile softly in gentle golden conscience glow near the bedroom doorway.",
        "time_pause_mechanic": "Warm lullaby glow illustrating how Conscience rewards completed duty with a sigh of relief and unbroken sleep.",
        "dialogue_anchor": "No sleeping pill on Earth equals a clean conscience—tonight, fulfilled duty gifts him the sweetest good night's sleep!",
        "visual_asset": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_11_peaceful_sleep_relief.jpg",
        "ref_ingredient": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_11_peaceful_sleep_relief.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
            "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
        ],
        "include_me_avatar": True,
    },
    {
        "scene": 12,
        "act": "ACT VI–VII — KARMIC GENIE SUMMONS & PILLOW TEST FINALE (Pages 13–14)",
        "title": "Awakening the Celestial Maharishi Karmic Genie & The 35/70 Pillow Test",
        "setting": "Grand pure-white circular marble stage with golden-sapphire stardust & Celestial Maharishi Karmic Genie.",
        "characters": "Cross-legged Celestial Maharishi Karmic Genie, @Me, 4yo Bala-Rishi, and Bala-Matha.",
        "two_birds_blocking": "Full Sacred Studio Finale locking '1. Respect Your DUTY First.' in radiant gold and previewing Virtue #2 ('Earn with DIGNITY Always').",
        "time_pause_mechanic": "Golden-sapphire stardust emergence from the center lamp + 5-Question Tonight Pillow Test.",
        "dialogue_anchor": "Respect your duty, honor every soul's duty, and sleep in divine peace. Nandri, Vanakkam—live the Seven-D Way!",
        "visual_asset": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_12_celestial_karmic_genie_finale.jpg",
        "ref_ingredient": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_12_celestial_karmic_genie_finale.jpg",
        "avatar_refs": [
            "assets/studio_v5_masters/v6_7d_saintly_genie_16x9.jpg",
            "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
        ],
        "include_me_avatar": True,
    },
]


# Master 48-Shot Shooting Ledger across 10 Resumable Google Flow Batches (`DF01`..`DF48`):
# Zero literal '@' characters appear in `visual` or `spoken` so ProseMirror never triggers a mention popup.
BATCH_SPECS = [
    {
        "id": "batch_01_accident_parable_hook",
        "title": "Page 1: Day 1 Traffic Calm vs. Day 2 Caused Rainy Scooter Accident (Bullet-Time Hook)",
        "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_01_accident_day2_pause.jpg",
        "include_me": True,
        "cast_rule": "Me + Bala-Rishi (Narrator + 1 Child)",
        "shots": [
            {
                "slot_id": "DF01",
                "page": 1,
                "speaker_mode": "human",
                "overlay_png": "ov_df_01_day1_traffic.png",
                "pause_after_s": 0.25,
                "keywords": ["yesterday", "ten cars", "scooter", "fifteen minutes"],
                "visual": "65mm widescreen Steadicam tracking beside ten commuter cars inching past a minor roadside scooter fender-bender from fifteen minutes ago where bystanders already help; Me (in ivory bandhgala) and 4-year-old Bala-Rishi walk effortlessly beside commuter Raghav's rolling sedan window looking into the lens.",
                "spoken": "Yesterday evening, ten cars crawled past a minor scooter accident that happened fifteen minutes earlier.",
                "subtitles": [
                    "Yesterday evening, ten cars crawled past a minor scooter accident",
                    "that happened fifteen minutes earlier.",
                ],
            },
            {
                "slot_id": "DF02",
                "page": 1,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["one-zero-eight", "drove home", "wife", "slept", "baby"],
                "visual": "Warm evening home transition: commuter Raghav casually mentions traffic at dinner while his wife Ananya nods calmly, then Raghav lays his head on his pillow and sleeps deeply while Me and 4-year-old Bala-Rishi observe quietly from the moonlit doorway; Bala-Rishi speaks warmly.",
                "spoken": "Someone already called one-zero-eight. He drove home, told his wife, and slept like a baby!",
                "subtitles": [
                    "Someone already called 108. He drove home, told his wife,",
                    "and slept like a baby!",
                ],
            },
            {
                "slot_id": "DF03",
                "page": 1,
                "speaker_mode": "human",
                "overlay_png": "ov_df_02_day2_caused_accident.png",
                "pause_after_s": 0.25,
                "keywords": ["next evening", "same minor", "his car", "caused", "nobody"],
                "visual": "3D Bullet-Time Time-Pause on a rain-slicked dusk suburban bend matching our reference plate: Raghav's dark sedan has just clipped a fallen commuter scooter and raindrops hang frozen in mid-air while ONLY Me (in ivory bandhgala) and 4-year-old Bala-Rishi walk calmly through suspended raindrops toward the camera.",
                "spoken": "Next evening—same minor accident. Except tonight, his car caused it, and nobody else is around.",
                "subtitles": [
                    "Next evening—same minor accident.",
                    "Except tonight, HIS car caused it, and nobody else is around.",
                ],
            },
            {
                "slot_id": "DF04",
                "page": 1,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.30,
                "keywords": ["just like yesterday", "dials", "rushes away", "helping"],
                "visual": "Time resumes in dusk rain: panicking inside his sedan, Raghav hastily dials 108 on his phone, avoids the wounded scooter rider's eyes in his wet side-mirror, and speeds away splashing rain while Me and 4-year-old Bala-Rishi watch his red tail-lights vanish.",
                "spoken": "Telling himself it is just like yesterday, he dials one-zero-eight and rushes away without helping!",
                "subtitles": [
                    "Telling himself it is 'just like yesterday,'",
                    "he dials 108 and rushes away without helping!",
                ],
            },
        ],
    },
    {
        "id": "batch_02_sleepless_conscience_and_portal",
        "title": "Page 2: 2:30 AM Sleepless Guilt, Wife's Mirror & White-Wall Studio Portal",
        "cast_rule": "Me + Bala-Matha (Bedroom) -> Studio Trinity Portal",
        "mixed_sub_batches": [
            {
                "sub_prefix": "batch_02a_bedroom_guilt",
                "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_02_sleepless_conscience.jpg",
                "include_me": True,
                "shots": [
                    {
                        "slot_id": "DF05",
                        "page": 2,
                        "speaker_mode": "human",
                        "overlay_png": "ov_df_03_conscience_230am.png",
                        "pause_after_s": 0.25,
                        "keywords": ["two-thirty", "same bed", "burning guilt", "steals", "sleep"],
                        "visual": "Dimly lit South Indian bedroom at 2:30 AM matching our reference plate: troubled husband Raghav sits awake on the mattress edge pressing both hands to his chest in sleepless guilt while ONLY Me (in ivory bandhgala) and young girl Bala-Matha (silk pattu pavadai, jasmine braid) stand quietly in soft golden conscience light.",
                        "spoken": "Two-thirty A.M. Same man, same bed, same minor scrape—yet tonight, burning guilt steals every breath of sleep!",
                        "subtitles": [
                            "2:30 A.M. Same man, same bed, same minor scrape—",
                            "yet tonight, burning guilt steals every breath of sleep!",
                        ],
                    },
                    {
                        "slot_id": "DF06",
                        "page": 2,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.30,
                        "keywords": ["yesterday", "wife", "nothing", "helped him", "his duty"],
                        "visual": "Under the warm amber bedside lamp, wife Ananya sits up earnestly gripping Raghav's shoulder ('You should have helped him!') while Bala-Matha (standing beside silent Me in ivory bandhgala) turns toward the camera and speaks clearly.",
                        "spoken": "Yesterday his wife said nothing. Tonight she cries, You should have helped him! Why? Because helping became HIS DUTY!",
                        "subtitles": [
                            "Yesterday his wife said nothing. Tonight she cries: 'You should have helped him!'",
                            "Why? Because helping became HIS DUTY!",
                        ],
                    },
                ],
            },
            {
                "sub_prefix": "batch_02b_white_stage_definition",
                "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_03_white_stage_duty_portal.jpg",
                "include_me": True,
                "shots": [
                    {
                        "slot_id": "DF07",
                        "page": 2,
                        "speaker_mode": "human",
                        "overlay_png": "ov_df_04_white_stage_d1.png",
                        "pause_after_s": 0.25,
                        "keywords": ["welcome", "karmic genie", "virtue one", "respect your duty"],
                        "visual": "Seamless White-Wall Zoom-Out from the bedroom through a glowing pure-white marble portal onto the circular Karmic Genie Show stage with brushed-gold wall inscription 'Respect Your DUTY First' and dormant gold Genie lamp; Me stands center stage in ivory bandhgala welcoming the audience.",
                        "spoken": "Welcome to The Karmic Genie Show! Virtue One of our Seven-D Way: Respect Your DUTY First.",
                        "subtitles": [
                            "Welcome to The Karmic Genie Show!",
                            "Virtue #1 of our 7D Way: Respect Your DUTY First.",
                        ],
                    },
                    {
                        "slot_id": "DF08",
                        "page": 2,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.30,
                        "keywords": ["office contract", "sacred task", "neglect", "guilt", "conscience"],
                        "visual": "Medium close-up on the pure-white circular marble stage: golden concentric floor rings shimmer softly as Me (in ivory bandhgala beside the dormant gold Genie lamp) places his right hand over his heart and defines true Duty.",
                        "spoken": "True Duty is never an office contract. Duty is the sacred task whose neglect awakens guilt inside your Conscience!",
                        "subtitles": [
                            "True Duty is never an office contract—",
                            "Duty is the sacred task whose neglect awakens guilt in your Conscience!",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "batch_03_cosmic_nature_and_childhood_play",
        "title": "Pages 3–4: Banyan/Bee/River 100% Duty, Safe Family Illaram, Age 4 Play & School 50/50",
        "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_04_banyan_age4_play.jpg",
        "include_me": True,
        "cast_rule": "Me + Bala-Rishi (Narrator + 1 Child)",
        "shots": [
            {
                "slot_id": "DF09",
                "page": 3,
                "speaker_mode": "human",
                "overlay_png": "ov_df_05_nature_100_duty.png",
                "pause_after_s": 0.25,
                "keywords": ["banyan", "honeybee", "flowing river", "one hundred percent", "applause"],
                "visual": "White-Wall Zoom-In into a golden sunlit riverbank beneath an ancient Banyan tree with lotus honeybees and crystal flowing water matching our reference plate; ONLY Me (in ivory bandhgala) and 4-year-old Bala-Rishi walk barefoot along the sunlit bank.",
                "spoken": "Look at the Banyan tree, the honeybee, and this flowing river—every living being performs one hundred percent duty without applause!",
                "subtitles": [
                    "Look at the Banyan tree, the honeybee, and this flowing river—",
                    "every living being performs 100% duty without applause!",
                ],
            },
            {
                "slot_id": "DF10",
                "page": 3,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["lonely caves", "shock-absorbers", "family life", "illaram", "safest", "fastest"],
                "visual": "Sunlit ridge overlooking a warm three-generation courtyard home nestled beside the river; 4-year-old Bala-Rishi walks cheerfully beside silent Me (in ivory bandhgala) gesturing warmly toward the family home and speaking clearly.",
                "spoken": "Lonely caves have zero shock-absorbers! Loving family life—Illaram—is the safest and fastest highway for your soul!",
                "subtitles": [
                    "Lonely caves have zero shock-absorbers!",
                    "Loving family life (Illaram) is the safest, fastest highway for your soul!",
                ],
            },
            {
                "slot_id": "DF11",
                "page": 4,
                "speaker_mode": "human",
                "overlay_png": "ov_df_06_lifecycle_stages.png",
                "pause_after_s": 0.25,
                "keywords": ["age four", "one hundred percent", "outdoor play", "lungs", "bones", "vitality"],
                "visual": "Golden morning sunlight under the Banyan tree matching our reference plate: a happy 4-year-old village child splashes barefoot in shallow golden puddles and climbs a low root while ONLY Me and 4-year-old Bala-Rishi walk joyfully beside him.",
                "spoken": "At age four, a child's one hundred percent duty is pure outdoor PLAY—building fearless lungs, bones, and vitality!",
                "subtitles": [
                    "At Age 4, a child's 100% duty is pure outdoor PLAY—",
                    "building fearless lungs, bones, and physical vitality!",
                ],
            },
            {
                "slot_id": "DF12",
                "page": 4,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["eight to sixteen", "curious study", "outdoor teamwork", "discipline", "sibling"],
                "visual": "Warm afternoon village courtyard & green playing field: cheerful 12-year-old children share notebooks on a veranda then sprint together passing a ball and helping a teammate up while Bala-Rishi jogs in stride beside silent Me along the touchline.",
                "spoken": "From eight to sixteen, half sharpens curious study and half builds outdoor teamwork, discipline, and sibling care!",
                "subtitles": [
                    "Ages 8 to 16: 50% sharpens curious study,",
                    "and 50% builds outdoor teamwork, discipline, and sibling care!",
                ],
            },
        ],
    },
    {
        "id": "batch_04_adulthood_porul_arul_and_elder_nandri",
        "title": "Pages 4–6: Youth First Paycheck, Age 24 Jnana, Male Porul, Female Arul Pooja & Elder Nandri",
        "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_05_porul_arul_home.jpg",
        "include_me": True,
        "cast_rule": "Me + Bala-Matha (Narrator + 1 Child)",
        "shots": [
            {
                "slot_id": "DF13",
                "page": 4,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["twenty-four", "honest mastery", "first pure earnings", "parents", "gratitude"],
                "visual": "Sunset courtyard threshold: a 22-year-old young craftsman returns home from honest work and places his first earnings reverently into his tearful parents' hands before bowing to touch their feet while ONLY Me (in ivory bandhgala) and Bala-Matha watch warmly.",
                "spoken": "By twenty-four, youth forges honest mastery—and places its first pure earnings into parents' hands with gratitude!",
                "subtitles": [
                    "By 24, youth forges honest skill—",
                    "placing its first pure earnings into parents' hands with gratitude!",
                ],
            },
            {
                "slot_id": "DF14",
                "page": 5,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["twenty-four", "independent thinking", "jnana buddhi", "illusions", "mind"],
                "visual": "Twilight courtyard archway: a clear-eyed 25-year-old householder calmly waves goodbye to boastful crowd conformity and steps peacefully into his lamp-lit family courtyard while Me and Bala-Matha walk beside him.",
                "spoken": "At twenty-four, blend independent thinking—Jnana Buddhi—into family life, questioning herd illusions so your Mind truly grows!",
                "subtitles": [
                    "At Age 24, blend independent thinking (Jnana Buddhi) into family life,",
                    "questioning herd illusions so your Mind truly grows!",
                ],
            },
            {
                "slot_id": "DF15",
                "page": 5,
                "speaker_mode": "human",
                "overlay_png": "ov_df_07_porul_and_arul.png",
                "pause_after_s": 0.25,
                "keywords": ["father", "fifty percent", "porul", "loving presence", "husband", "citizen"],
                "visual": "Serene twilight courtyard home matching our reference plate: a devoted father places a basket of fresh fruit and honest provision on the hearth table, silences his phone, and warmly greets his family while ONLY Me and Bala-Matha walk beside him.",
                "spoken": "A father's duty is fifty percent spotless Porul, and fifty percent loving presence as husband, father, son, and citizen!",
                "subtitles": [
                    "A father's duty: 50% spotless Porul (honest wealth),",
                    "and 50% loving presence as husband, father, son, and citizen!",
                ],
            },
            {
                "slot_id": "DF16",
                "page": 5,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["mother", "sacred arul", "pooja lamp", "brick walls", "living temple"],
                "visual": "Heart of the twilight courtyard home matching our reference plate: a graceful mother in silk saree lights the tall brass Kuthuvilakku oil lamp in the Pooja sanctum beside her praying child while Bala-Matha (holding silent Me's hand) speaks luminously.",
                "spoken": "And a mother's sacred Arul—nurturing life and lighting the daily Pooja lamp—turns four brick walls into a living temple!",
                "subtitles": [
                    "And a mother's sacred Arul—nurturing life and lighting the daily Pooja lamp—",
                    "turns four brick walls into a living temple!",
                ],
            },
            {
                "slot_id": "DF17",
                "page": 6,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["fifty-four", "nandri", "fifty percent", "thanking", "grievance", "soul"],
                "visual": "Golden dawn courtyard garden: a serene 55-year-old couple stands with folded palms in deep Nandri gratitude toward the rising sun while warmly passing household keys to their grown son; Me and Bala-Matha walk softly beside them.",
                "spoken": "At fifty-four, duty ripens into Nandri—fifty percent pure thanking that melts every grievance and grows your Soul!",
                "subtitles": [
                    "At Age 54, duty ripens into Nandri—",
                    "50% pure thanking that melts every grievance and grows your Soul!",
                ],
            },
        ],
    },
    {
        "id": "batch_05_para_soul_and_only_you_father",
        "title": "Pages 6–7: Elder Para-Soul Canopy, 'Only You Can Do' Question & Scene 1 (Father)",
        "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_06_only_you_father_hug.jpg",
        "include_me": True,
        "cast_rule": "Me + Bala-Rishi (Narrator + 1 Child)",
        "shots": [
            {
                "slot_id": "DF18",
                "page": 6,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["elders", "banyan canopy", "arul blessings", "guarding", "four-year-old", "play"],
                "visual": "Sunlit garden beneath a spreading Banyan canopy: a radiant 75-year-old grandfather and grandmother smile in peaceful blessing as their 4-year-old grandchild plays barefoot on the grass while Bala-Rishi beams beside silent Me (in ivory bandhgala).",
                "spoken": "And elders become a living Banyan canopy—radiating Arul blessings while guarding the next four-year-old's barefoot play!",
                "subtitles": [
                    "Elders become a living Banyan canopy—",
                    "radiating Arul blessings while guarding the next 4-year-old's play!",
                ],
            },
            {
                "slot_id": "DF19",
                "page": 7,
                "speaker_mode": "human",
                "overlay_png": "ov_df_08_only_you_can_do.png",
                "pause_after_s": 0.25,
                "keywords": ["duty is done", "what next", "only you can do", "arrogant", "father your child"],
                "visual": "Dynamic White-Wall Portal transition onto a sunlit tree-lined stone walkway: Me (in ivory bandhgala) walks briskly toward the camera with 4-year-old Bala-Rishi at his side, asking and answering the pivotal question with warm clarity.",
                "spoken": "Once today's duty is done, what next? Do the things ONLY YOU can do! Arrogant? Never—can anyone else father your child?",
                "subtitles": [
                    "Once today's duty is done, what next? Do what ONLY YOU can do!",
                    "Arrogant? Never—can anyone else be the father of your child?",
                ],
            },
            {
                "slot_id": "DF20",
                "page": 7,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.30,
                "keywords": ["scene one", "ten thousand engineers", "office chair", "father to your child"],
                "visual": "Golden rain-washed cobblestone walkway matching our reference plate: a joyful 5-year-old boy with a small backpack runs past blurred commuters and leaps into his kneeling father's open arms while ONLY Me and 4-year-old Bala-Rishi walk warmly beside them.",
                "spoken": "Scene One: Ten thousand engineers can replace your office chair—not one human on Earth can be father to your child!",
                "subtitles": [
                    "Scene 1 of 7: 10,000 engineers can replace your office chair—",
                    "not one human on Earth can be father to YOUR child!",
                ],
            },
        ],
    },
    {
        "id": "batch_06_only_you_mother_parents_spouse",
        "title": "Pages 7–8: 'Only You Can Do' Scenes 2, 3 & 4 (Mother, Aging Parents, Spouse)",
        "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_07_only_you_elder_parents.jpg",
        "include_me": True,
        "cast_rule": "Me + Bala-Matha (Narrator + 1 Child)",
        "shots": [
            {
                "slot_id": "DF21",
                "page": 7,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["scene two", "doctors", "medicine", "mother", "heartbeat", "prayer"],
                "visual": "Warm lamp-lit bedroom corner: a mother cradles her feverish toddler against her shoulder whispering a soothing prayer until the child relaxes into calm sleep, while Bala-Matha (standing beside silent Me in ivory bandhgala) speaks tenderly.",
                "spoken": "Scene Two: Doctors give medicine, yet only a mother's heartbeat and whispered Arul prayer calm her child's trembling soul!",
                "subtitles": [
                    "Scene 2 of 7: Doctors give medicine, yet only a mother's heartbeat",
                    "and whispered Arul prayer calm her child's trembling soul!",
                ],
            },
            {
                "slot_id": "DF22",
                "page": 7,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["scene three", "money hires nurses", "aging parents", "eyes wait", "their child"],
                "visual": "Pillared South Indian ancestral veranda at golden sunset matching our reference plate: a 40-year-old son kneels warmly holding the wrinkled hands of his joyful 78-year-old father and mother while ONLY Me and Bala-Matha walk softly beside the teak pillar.",
                "spoken": "Scene Three: Money hires nurses, never kinship—your aging parents' eyes wait at the gate only for you, their child!",
                "subtitles": [
                    "Scene 3 of 7: Money hires nurses, never kinship—",
                    "your aging parents' eyes wait at the gate only for YOU!",
                ],
            },
            {
                "slot_id": "DF23",
                "page": 8,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["scene four", "applause fades", "midnight", "life-partner", "husband or wife"],
                "visual": "Quiet lantern-lit home dining table late at night: a devoted husband gently holds both hands of his overwhelmed wife listening with complete tenderness while Bala-Matha (beside silent Me in ivory bandhgala) speaks softly.",
                "spoken": "Scene Four: When applause fades at midnight, only you can hold your life-partner's hand as true husband or wife!",
                "subtitles": [
                    "Scene 4 of 7: When applause fades at midnight,",
                    "only YOU can hold your partner's hand as true husband or wife!",
                ],
            },
        ],
    },
    {
        "id": "batch_07_only_you_body_conscience_gift_and_rule",
        "title": "Pages 8–9: 'Only You' Scenes 5–7, Iron Daily Time Law, Never Skip Duty & 3 Sages",
        "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_08_white_wall_portal_transition.jpg",
        "include_me": True,
        "cast_rule": "Me + Bala-Rishi (Narrator + 1 Child)",
        "shots": [
            {
                "slot_id": "DF24",
                "page": 8,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["scene five", "billionaire", "assistant", "exercise", "lungs", "sleep"],
                "visual": "Golden sunrise garden terrace: a healthy man breathes deeply in morning pranayama and stretches joyfully in sunlight while 4-year-old Bala-Rishi mirrors his stretch beside silent Me (in ivory bandhgala) and speaks brightly.",
                "spoken": "Scene Five: No billionaire can hire an assistant to exercise his lungs, digest his food, or sleep on his behalf!",
                "subtitles": [
                    "Scene 5 of 7: No billionaire can hire an assistant",
                    "to exercise his lungs, digest his food, or sleep on his behalf!",
                ],
            },
            {
                "slot_id": "DF25",
                "page": 8,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["scene six", "no proxy", "apologize", "forgive", "brother", "gratitude"],
                "visual": "Warm morning courtyard: two brothers embrace in tearful forgiveness before bowing with folded palms at a glowing brass oil lamp while ONLY Me (in ivory bandhgala) and 4-year-old Bala-Rishi stand beside them.",
                "spoken": "Scene Six: No proxy can apologize for your mistake, forgive your brother, or bow your heart in gratitude before God!",
                "subtitles": [
                    "Scene 6 of 7: No proxy can apologize for your mistake,",
                    "forgive your brother, or bow your heart before God!",
                ],
            },
            {
                "slot_id": "DF26",
                "page": 8,
                "speaker_mode": "human",
                "overlay_png": "ov_df_09_daily_golden_rule.png",
                "pause_after_s": 0.25,
                "keywords": ["scene seven", "swadharma", "every day", "duty first", "only you", "nothing else"],
                "visual": "Sunlit master artisan guiding a young apprentice's chisel before transitioning to the luminous White-Wall studio portal where Me (in ivory bandhgala) and 4-year-old Bala-Rishi proclaim the Iron Daily Time Rule.",
                "spoken": "Scene Seven: Pour out your unique Swadharma! Every day: do your Duty first, then what ONLY YOU can do—nothing else!",
                "subtitles": [
                    "Scene 7 of 7: Pour out your unique Swadharma!",
                    "Daily Rule: Duty first → What ONLY YOU can do → NOTHING ELSE!",
                ],
            },
            {
                "slot_id": "DF27",
                "page": 9,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["wastes your priceless", "truly know", "respect it", "never skipping"],
                "visual": "Pre-dawn 5:15 AM rain outside a warm kitchen window: a devoted son quietly prepares warm milk for his elder parents without anyone watching while Me (in ivory bandhgala) and Bala-Rishi walk beside him.",
                "spoken": "Doing anything outside those two wastes your priceless life! When you truly know your duty, you respect it—never skipping it!",
                "subtitles": [
                    "Doing anything outside those two wastes your priceless life!",
                    "When you know true duty, you respect it—never skipping it!",
                ],
            },
            {
                "slot_id": "DF28",
                "page": 9,
                "speaker_mode": "human",
                "overlay_png": None,
                "pause_after_s": 0.25,
                "keywords": ["thiruvalluvar", "inner torch", "buddha", "six directions", "laozi", "sacred"],
                "visual": "On the pure-white circular marble stage before the glowing White Wall portal, three subtle golden wisdom medallions shimmer behind silent Me and 4-year-old Bala-Rishi as Bala-Rishi speaks clearly.",
                "spoken": "Thiruvalluvar's inner torch, Buddha's Six Directions, and Laozi's living Tao all teach one truth—guard today's duty as sacred!",
                "subtitles": [
                    "Thiruvalluvar's inner torch, Buddha's Six Directions, and Laozi's Tao",
                    "all teach one truth—guard today's duty as sacred!",
                ],
            },
        ],
    },
    {
        "id": "batch_08_respect_everyones_duty_and_public_scope",
        "title": "Pages 10–11: Respect Everyone Else's Duty (Dawn Namaste) & Public/Environmental Scope",
        "cast_rule": "Me + Bala-Matha (Dawn Street) -> Me + Bala-Rishi (Public Path & Accident Rewind)",
        "mixed_sub_batches": [
            {
                "sub_prefix": "batch_08a_dawn_street_namaste",
                "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_09_respect_everyones_duty.jpg",
                "include_me": True,
                "shots": [
                    {
                        "slot_id": "DF29",
                        "page": 10,
                        "speaker_mode": "human",
                        "overlay_png": "ov_df_10_respect_all_duty.png",
                        "pause_after_s": 0.25,
                        "keywords": ["respecting duty", "everyone else", "never demean", "honest worker", "ego"],
                        "visual": "3D Bullet-Time Time-Pause on a golden sunrise tree-lined avenue matching our reference plate: a car commuter's hand freezes above his horn behind an elderly street cleaner while ONLY Me (in ivory bandhgala) and Bala-Matha walk calmly beside the open car window.",
                        "spoken": "And respecting duty means respecting everyone else's duty too! Never demean any honest worker whose task looks small to ego!",
                        "subtitles": [
                            "Respecting duty means respecting EVERYONE ELSE'S duty too!",
                            "Never demean any honest worker whose task looks small to ego!",
                        ],
                    },
                    {
                        "slot_id": "DF30",
                        "page": 10,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.25,
                        "keywords": ["divine", "street cleaner", "night watchman", "ten-on-ten", "noble", "king"],
                        "visual": "Golden sunrise avenue matching our reference plate: the commuter steps out of his parked car and folds both palms in a warm respectful Namaste bow to the smiling elderly street cleaner while Bala-Matha (beside silent Me) speaks warmly.",
                        "spoken": "Before the Divine, a street cleaner or night watchman fulfilling honest duty at ten-on-ten stands as noble as any king!",
                        "subtitles": [
                            "Before the Divine, a street cleaner or night watchman",
                            "fulfilling honest duty at 10/10 stands as noble as any king!",
                        ],
                    },
                ],
            },
            {
                "sub_prefix": "batch_08b_public_environment_and_rewind",
                "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_01_accident_day2_pause.jpg",
                "include_me": True,
                "shots": [
                    {
                        "slot_id": "DF31",
                        "page": 11,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.25,
                        "keywords": ["beyond family", "strangers", "public paths", "mother earth", "danger", "protecting"],
                        "visual": "Sunlit public footpath beside a clean river: a thoughtful citizen safely clears broken glass before barefoot children pass and waters a young roadside sapling while ONLY Me (in ivory bandhgala) and 4-year-old Bala-Rishi walk beside her.",
                        "spoken": "Duty reaches beyond family—to strangers, public paths, and Mother Earth! When your eyes spot danger first, protecting life becomes yours!",
                        "subtitles": [
                            "Duty reaches beyond family—to strangers, public paths, and Mother Earth!",
                            "When your eyes spot danger first, protecting life becomes yours!",
                        ],
                    },
                    {
                        "slot_id": "DF32",
                        "page": 11,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.30,
                        "keywords": ["watch what happens", "rainy road", "raghav", "conscience", "running away"],
                        "visual": "Golden-streaked time-rewind back to the rain-slicked dusk suburban scooter accident matching our reference plate: raindrops freeze around Raghav's sedan door as 4-year-old Bala-Rishi (standing beside silent Me) points toward Raghav's awakened heart.",
                        "spoken": "Now watch what happens on that rainy road when Raghav listens to his Conscience instead of running away!",
                        "subtitles": [
                            "Now watch what happens on that rainy road",
                            "when Raghav listens to his Conscience instead of running away!",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "batch_09_redemption_sigh_of_relief_and_sleep",
        "title": "Page 12: Stopping in the Rain, Bandaging the Stranger, Sigh of Relief & Good Night's Sleep",
        "cast_rule": "Me + Bala-Rishi (Roadside Rescue) -> Me + Bala-Matha (Peaceful Sleep)",
        "mixed_sub_batches": [
            {
                "sub_prefix": "batch_09a_rain_rescue",
                "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_10_redemption_help_rider.jpg",
                "include_me": True,
                "shots": [
                    {
                        "slot_id": "DF33",
                        "page": 12,
                        "speaker_mode": "human",
                        "overlay_png": "ov_df_11_redemption_relief.png",
                        "pause_after_s": 0.25,
                        "keywords": ["parks", "runs into the rain", "bandages", "stranger", "medical hands"],
                        "visual": "Dusk rain-wet avenue as golden sunbeams break through storm clouds matching our reference plate: Raghav parks with hazard lights, kneels under an umbrella bandaging the injured scooter rider's knee as an ambulance arrives while ONLY Me and 4-year-old Bala-Rishi stand warmly beside them.",
                        "spoken": "He parks, runs into the rain, bandages the stranger's knee, and stays beside him until medical hands take over!",
                        "subtitles": [
                            "He parks, runs into the rain, bandages the stranger's knee,",
                            "and stays beside him until medical hands take over!",
                        ],
                    },
                    {
                        "slot_id": "DF34",
                        "page": 12,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.25,
                        "keywords": ["no court", "inner witness", "fear vanishes", "stand up", "honor your duty"],
                        "visual": "Under clearing amber twilight clouds, the grateful scooter rider clasps Raghav's wet hands in warm forgiveness while Raghav bows humbly; 4-year-old Bala-Rishi (standing beside silent Me in ivory bandhgala) smiles into the camera.",
                        "spoken": "No court forced him—only his watchful inner witness! Fear vanishes the instant you stand up and honor your duty.",
                        "subtitles": [
                            "No court forced him—only his watchful inner witness!",
                            "Fear vanishes the instant you stand up and honor your duty.",
                        ],
                    },
                ],
            },
            {
                "sub_prefix": "batch_09b_sigh_of_relief_sleep",
                "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_11_peaceful_sleep_relief.jpg",
                "include_me": True,
                "shots": [
                    {
                        "slot_id": "DF35",
                        "page": 12,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.25,
                        "keywords": ["conscience", "punishes", "guilt", "rewards", "sigh of relief"],
                        "visual": "Warm lamp-lit South Indian home at night: returning in a rain-damp shirt, Raghav tells Ananya he stayed to help the rider; Ananya smiles with deep pride as Raghav closes his eyes and exhales a deep, full-chest sigh of relief while ONLY Me and Bala-Matha watch warmly.",
                        "spoken": "Conscience punishes neglect with guilt—and rewards completed duty with that priceless, full-chest sigh of relief!",
                        "subtitles": [
                            "Conscience punishes neglect with guilt—",
                            "and rewards completed duty with a priceless, full-chest sigh of relief!",
                        ],
                    },
                    {
                        "slot_id": "DF36",
                        "page": 12,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.30,
                        "keywords": ["sleeping pill", "clean conscience", "fulfilled duty", "sweetest", "good night"],
                        "visual": "Serene South Indian bedroom at night matching our reference plate: Raghav and Ananya sleep deeply and peacefully with gentle smiles under warm brass oil-lamp glow while Bala-Matha (beside silent Me near the doorway) whispers warmly.",
                        "spoken": "No sleeping pill on Earth equals a clean conscience—tonight, fulfilled duty gifts him the sweetest good night's sleep!",
                        "subtitles": [
                            "No sleeping pill on Earth equals a clean conscience—",
                            "fulfilled duty gifts him the sweetest good night's sleep!",
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "batch_10_karmic_genie_summons_pillow_test_finale",
        "title": "Pages 13–14: Summoning the Karmic Genie, 35/70 Pillow Test Scorecard & Grand Finale",
        "cast_rule": "Studio Trinity + Celestial Maharishi Karmic Genie",
        "mixed_sub_batches": [
            {
                "sub_prefix": "batch_10a_genie_awakening",
                "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_12_celestial_karmic_genie_finale.jpg",
                "include_me": False,
                "extra_header": "Featuring the serene cross-legged Celestial Maharishi Karmic Genie floating above the jeweled gold lamp on the pure-white circular marble stage.",
                "shots": [
                    {
                        "slot_id": "DF38",
                        "page": 13,
                        "speaker_mode": "genie",
                        "overlay_png": "ov_df_12_genie_pillow_test.png",
                        "pause_after_s": 0.25,
                        "keywords": ["blessed souls", "guilt", "enemy", "divine bell", "sorrow"],
                        "visual": "Pure-white circular marble Karmic Genie Show stage matching our reference plate: golden-sapphire stardust rises from the jeweled gold lamp into the serene cross-legged Celestial Maharishi Karmic Genie raising his blessing palm and speaking with warm cosmic resonance.",
                        "spoken": "Blessed souls! Guilt is never your enemy—it is the Divine Bell waking you before karma hardens into sorrow!",
                        "subtitles": [
                            "Blessed souls! Guilt is never your enemy—",
                            "it is the Divine Bell waking you before karma hardens into sorrow!",
                        ],
                    },
                    {
                        "slot_id": "DF39",
                        "page": 13,
                        "speaker_mode": "genie",
                        "overlay_png": None,
                        "pause_after_s": 0.30,
                        "keywords": ["each sunrise", "rightful duty", "only you can do", "bow", "honest worker"],
                        "visual": "Floating serenely cross-legged in golden-sapphire light above the circular white marble stage, the Celestial Maharishi Karmic Genie sweeps his luminous hand tracing three golden rings of Duty, Swadharma, and Mutual Reverence.",
                        "spoken": "Each sunrise, complete your rightful duty first, then do what only you can do, and bow to every honest worker!",
                        "subtitles": [
                            "Each sunrise: complete your rightful duty first,",
                            "do what only you can do, and bow to every honest worker!",
                        ],
                    },
                ],
            },
            {
                "sub_prefix": "batch_10b_scorecard_questions",
                "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_03_white_stage_duty_portal.jpg",
                "include_me": True,
                "shots": [
                    {
                        "slot_id": "DF37",
                        "page": 13,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.25,
                        "keywords": ["conscience watches", "every breath", "what does genie say", "seven-d way"],
                        "visual": "White-Wall Zoom-Out onto the hushed pure-white circular marble Karmic Genie Show stage: Me (in ivory bandhgala) steps beside the glowing gold Genie lamp at stage center and invokes the Karmic Genie.",
                        "spoken": "Your Conscience watches every breath! Now let us ask together: What does Genie say — the Seven-D way?",
                        "subtitles": [
                            "Your Conscience watches every breath!",
                            "Now let us ask together: What does Genie say — the 7D way?",
                        ],
                    },
                    {
                        "slot_id": "DF40",
                        "page": 13,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.25,
                        "keywords": ["tonight", "score your duty", "one to ten", "five quiet questions", "pillow"],
                        "visual": "On the circular white marble stage beneath a luminous golden 'DUTY: 1–10 (Target >= 35/70)' pillar light, Me (in ivory bandhgala) addresses the audience directly with empowering warmth.",
                        "spoken": "Tonight, score your Duty honestly from one to ten! Five quiet questions before your head touches the pillow:",
                        "subtitles": [
                            "Tonight, score your Duty honestly from 1 to 10!",
                            "Five quiet questions before your head touches the pillow:",
                        ],
                    },
                    {
                        "slot_id": "DF41",
                        "page": 13,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.25,
                        "keywords": ["honor elders", "undivided warmth", "spouse and children", "humble worker", "respect"],
                        "visual": "On the pure-white circular marble stage beside silent Me, 4-year-old Bala-Rishi counts warmly on his fingers with sparkling eyes.",
                        "spoken": "Did you honor elders, give undivided warmth to spouse and children, and treat every humble worker's duty with respect?",
                        "subtitles": [
                            "1–3: Did you honor elders, give undivided warmth to family,",
                            "and treat every humble worker's duty with respect?",
                        ],
                    },
                    {
                        "slot_id": "DF42",
                        "page": 13,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.25,
                        "keywords": ["walking away", "guilt", "exhale tonight", "peaceful", "unbroken sleep"],
                        "visual": "On the pure-white circular marble stage beside silent Me, young girl Bala-Matha (in silk pattu pavadai with jasmine braid) folds her hands gently over her heart and asks the Pillow Test.",
                        "spoken": "Did you help where walking away would bring guilt—and can your heart exhale tonight into peaceful, unbroken sleep?",
                        "subtitles": [
                            "4–5 (The Pillow Test): Did you help where walking away brings guilt—",
                            "and can your heart exhale tonight into peaceful sleep?",
                        ],
                    },
                    {
                        "slot_id": "DF43",
                        "page": 14,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.25,
                        "keywords": ["undone duty", "whispers", "make that call", "offer that help", "tonight"],
                        "visual": "Warm close-up on the circular white marble stage: Me (in ivory bandhgala) leans forward earnestly inspiring immediate tonight action.",
                        "spoken": "If one undone duty whispers inside your chest right now—make that call, offer that help, and free your heart tonight!",
                        "subtitles": [
                            "If one undone duty whispers inside your chest right now—",
                            "make that call, offer that help, and free your heart tonight!",
                        ],
                    },
                ],
            },
            {
                "sub_prefix": "batch_10c_grand_trinity_finale",
                "ref_rel": "episodes/S01E01_Respect_Your_Duty_First/storyboard/sb_03_white_stage_duty_portal.jpg",
                "include_me": True,
                "shots": [
                    {
                        "slot_id": "DF44",
                        "page": 14,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.25,
                        "keywords": ["pillar one", "shines within", "respect your duty first", "inner peace", "guard"],
                        "visual": "Wide majestic shot of the pure-white circular marble stage as '1. Respect Your DUTY First.' glows in permanent 24k gold on the curved back wall behind Me, Bala-Rishi, and Bala-Matha.",
                        "spoken": "Pillar One now shines within you: Respect Your DUTY First—and watch inner peace guard your home day and night!",
                        "subtitles": [
                            "Pillar #1 now shines within you: Respect Your DUTY First—",
                            "and watch inner peace guard your home day and night!",
                        ],
                    },
                    {
                        "slot_id": "DF45",
                        "page": 14,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.20,
                        "keywords": ["play when young", "think with truth", "duty first", "never waste", "precious life"],
                        "visual": "Medium close-up beside the gleaming gold Genie lamp on the white marble stage: 4-year-old Bala-Rishi folds his palms in joyful Namaste and speaks clearly.",
                        "spoken": "Play when young, think with truth, complete your duty first, and never waste one drop of your precious life!",
                        "subtitles": [
                            "Play when young, think with truth, complete your duty first,",
                            "and never waste one drop of your precious life!",
                        ],
                    },
                    {
                        "slot_id": "DF46",
                        "page": 14,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.20,
                        "keywords": ["home lamp", "shine with arul", "nandri", "peaceful sleep", "pillow"],
                        "visual": "Medium close-up on the white marble stage: young girl Bala-Matha (jasmine braid, silk pattu pavadai) folds her palms in serene Arul blessing and smiles warmly.",
                        "spoken": "May your home lamp shine with Arul, may Nandri fill your breath, and may peaceful sleep bless your pillow!",
                        "subtitles": [
                            "May your home lamp shine with Arul, may Nandri fill your breath,",
                            "and may peaceful sleep bless your pillow!",
                        ],
                    },
                    {
                        "slot_id": "DF47",
                        "page": 14,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.25,
                        "keywords": ["next on", "karmic genie", "virtue two", "spotless porul", "dignity always"],
                        "visual": "Graceful crane shot across the circular white marble stage as subtle golden light touches '2. Earn with DIGNITY Always.' on the curved wall behind Me, Bala-Rishi, and Bala-Matha.",
                        "spoken": "Next on The Karmic Genie Show, Virtue Two awaits: how spotless Porul multiplies grace—Earn with DIGNITY Always!",
                        "subtitles": [
                            "Next on The Karmic Genie Show — Virtue #2 awaits:",
                            "How spotless Porul multiplies grace: Earn with DIGNITY Always!",
                        ],
                    },
                    {
                        "slot_id": "DF48",
                        "page": 14,
                        "speaker_mode": "human",
                        "overlay_png": None,
                        "pause_after_s": 0.45,
                        "keywords": ["respect your duty", "honor every soul", "divine peace", "nandri", "seven-d way"],
                        "visual": "Grand rising symphonic crane finale over the pure-white circular marble amphitheater: Me (in ivory bandhgala), 4-year-old Bala-Rishi, and Bala-Matha bow together in synchronized Namaskaram behind the glowing gold Genie lamp.",
                        "spoken": "Respect your duty, honor every soul's duty, and sleep in divine peace. Nandri, Vanakkam—live the Seven-D Way!",
                        "subtitles": [
                            "Respect your duty, honor every soul's duty, and sleep in divine peace.",
                            "Nandri, Vanakkam — Live the 7D Way!",
                        ],
                    },
                ],
            },
        ],
    },
]


def resolve_repo_image(rel_path: str | None) -> Path | None:
    if not rel_path:
        return None
    p = REPO_DIR / rel_path
    if p.exists():
        return p
    p_docs = REPO_DIR / "docs" / rel_path
    if p_docs.exists():
        return p_docs
    return p


def build_batch_prompt(shots: list[dict], include_me: bool, extra_header: str = "") -> str:
    n = len(shots)
    me_clause = (
        " and using my attached Me Avatar (in tailored ivory-white bandhgala suit)"
        if include_me
        else ""
    )
    header = (
        f"Generate {n} separate widescreen 16:9 photorealistic theatrical cinema video clips "
        f"(8 seconds each, Omni 1.1 Flash with slow, clear, natural spoken audio, zero burned-in text captions) "
        f"right now in batch without asking confirmation, strictly matching our attached reference image{me_clause}."
    )
    if extra_header:
        header += " " + extra_header

    blocks = [header]
    for idx, sh in enumerate(shots, 1):
        vis = sh["visual"].replace("@Me", "Me").replace("@", "")
        spk = sh["spoken"].replace("@Me", "Me").replace("@", "").strip()
        if spk:
            blocks.append(f'{idx}) {sh["slot_id"]}: {vis} Spoken clearly, warmly, and unhurriedly: "{spk}"')
        else:
            blocks.append(f'{idx}) {sh["slot_id"]}: {vis}')
    return "\n\n".join(blocks) + "\n"


def flatten_shot_ledger() -> list[dict]:
    """Exports the flat 48-shot canonical ledger (`DF01..DF48`) sorted in screenplay order."""
    flat = []
    for b in BATCH_SPECS:
        bid = b["id"]
        if "mixed_sub_batches" in b:
            for sub in b["mixed_sub_batches"]:
                for sh in sub["shots"]:
                    flat.append({
                        "slot_id": sh["slot_id"],
                        "batch_id": bid,
                        "file_prefix": sub["sub_prefix"],
                        "page": sh["page"],
                        "cast_rule": b["cast_rule"],
                        "include_me": sub["include_me"],
                        "ref_image": sub["ref_rel"],
                        "speaker_mode": sh["speaker_mode"],
                        "overlay_png": sh["overlay_png"],
                        "pause_after_s": sh["pause_after_s"],
                        "keywords": sh["keywords"],
                        "visual": sh["visual"],
                        "spoken": sh["spoken"],
                        "word_count": len(sh["spoken"].split()) if sh["spoken"] else 0,
                        "subtitles": sh["subtitles"],
                    })
        else:
            for sh in b["shots"]:
                flat.append({
                    "slot_id": sh["slot_id"],
                    "batch_id": bid,
                    "file_prefix": bid,
                    "page": sh["page"],
                    "cast_rule": b["cast_rule"],
                    "include_me": b["include_me"],
                    "ref_image": b["ref_rel"],
                    "speaker_mode": sh["speaker_mode"],
                    "overlay_png": sh["overlay_png"],
                    "pause_after_s": sh["pause_after_s"],
                    "keywords": sh["keywords"],
                    "visual": sh["visual"],
                    "spoken": sh["spoken"],
                    "word_count": len(sh["spoken"].split()) if sh["spoken"] else 0,
                    "subtitles": sh["subtitles"],
                })
    flat.sort(key=lambda r: int(r["slot_id"].replace("DF", "")))
    return flat


def export_storyboard_package_json() -> Path:
    pkg = {
        "project_title": "The Karmic Genie Show — S01E01: Respect Your DUTY First. (Epic Movie Edition)",
        "series_format": "The 7D Way — Virtues & Divinity Theatrical Movie Series (White-Wall Portals + Active Two-Birds In-Scene Narrators)",
        "target_platform": "Google Flow Storyboard Suite (MCP + CDP Port 9225/9222)",
        "account": "nagaraj957@gmail.com",
        "mcp_server_command": "python3 pipeline/google_flow_mcp_s01e01_storyboard.py",
        "master_character_avatars": {
            "@Me": {
                "avatar_tag": "Me",
                "master_image": "assets/studio_v5_masters/v9_host_adult_ivory_bandhgala_16x9.jpg",
                "canonical_look": "Exact likeness of @Me (swept-back dark hair, salt-and-pepper stubble, warm expressive eyes) wearing his tailored ivory-white bandhgala suit.",
            },
            "Bala-Rishi": {
                "avatar_tag": "Bala-Rishi",
                "master_image": "assets/studio_v5_masters/v9_genie_4yo_bala_rishi_16x9.jpg",
                "canonical_look": "4-year-old boy sage Bala-Rishi (top-knot bun, Urdhva Pundra tilak, Rudraksha mala, cream silk kurta & golden-bordered shawl).",
            },
            "Bala-Matha": {
                "avatar_tag": "Bala-Matha",
                "master_image": "assets/studio_v5_masters/bala_matha_master_portrait.jpg",
                "canonical_look": "Young divine girl sage Bala-Matha (vibhuti/kumkum on forehead, magenta-green silk pattu pavadai with golden zari border, fresh white jasmine garlands).",
            },
        },
        "signature_cinematic_mechanics": {
            "two_birds_active_narrator_law": "Narrator (@Me) + ONE Child ONLY (Bala-Rishi OR Bala-Matha) live physically inside each movie scene—walking, kneeling, or riding beside characters to narrate inner conscience.",
            "bullet_time_freeze_frame_walkthrough": "[SCENE TIME-PAUSE] freezes raindrops, traffic horns, and moral crossroads in 3D bullet-time while @Me + 1 Child walk calmly through the frozen frame.",
            "white_wall_zoom_portal": "Pure-white circular marble Karmic Genie Show studio wall acts as a seamless zoom-in/zoom-out cinema portal.",
        },
        "episode_1_storyboard_scenes": STORYBOARD_SCENES,
    }
    PACKAGE_JSON_PATH.write_text(json.dumps(pkg, ensure_ascii=False, indent=2), encoding="utf-8")
    (REPO_DIR / "docs" / "GOOGLE_FLOW_STORYBOARD_PACKAGE_S01E01.json").write_text(
        json.dumps(pkg, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (EP_DIR / "GOOGLE_FLOW_STORYBOARD_PACKAGE_S01E01.json").write_text(
        json.dumps(pkg, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return PACKAGE_JSON_PATH


def export_ledger_json() -> Path:
    flat = flatten_shot_ledger()
    missing_refs = []
    for item in flat:
        rp = resolve_repo_image(item["ref_image"])
        if rp is None or not rp.exists():
            missing_refs.append((item["slot_id"], item["ref_image"]))
        if "@" in item["visual"] or "@" in item["spoken"]:
            raise ValueError(f"Literal '@' found in {item['slot_id']} — must use 'Me' with Avatar chip!")
    if missing_refs:
        raise FileNotFoundError(f"Missing reference images: {missing_refs}")

    payload = {
        "episode": "S01E01",
        "series": "The Karmic Genie Show — The 7D Way (Virtues & Divinity)",
        "title": "1. Respect Your DUTY First.",
        "screenplay_path": "episodes/S01E01_Respect_Your_Duty_First/S01E01_14_Page_Master_Screenplay_Respect_Your_Duty_First.md",
        "total_batches": len(BATCH_SPECS),
        "total_shots": len(flat),
        "target_aspect_ratio": "16:9",
        "clip_duration_seconds": 8,
        "estimated_master_runtime": "~07:45 (17.6s 7D Cold Open + 48 slowed cinema shots + 14.5s Finale Card)",
        "rules_enforced": [
            "Virtue #1 Focus: 'Respect Your DUTY First' (True Duty = task whose neglect causes guilt in Conscience)",
            "Lifecycle Duty across Nature (Banyan, Bee, River) & Human Stages (Age 4 Play -> Age 24 Think -> Porul/Arul -> Age 54 Thank -> Elder Para-Soul)",
            "7 Distinct 'Things ONLY YOU Can Do' Movie Scenes + Iron Daily Time Rule (Duty First -> Only You -> Nothing Else)",
            "Respect Everyone Else's Duty (Zero demeaning of any honest worker)",
            "Two-Day Car Accident Master Parable (Day 1 calm vs. Day 2 sleepless guilt & Wife's mirror -> Rain rescue -> Sigh of relief & Good night's sleep)",
            "Strict Narrator (Me) + ONE Child ONLY per movie scene + Official Me Google Flow Avatar chip (zero literal @)",
        ],
        "shots": flat,
    }
    LEDGER_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (REPO_DIR / "docs" / "s01e01_48_shot_flow_ledger.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    export_storyboard_package_json()
    return LEDGER_JSON_PATH


class FlowFilmRunner:
    def __init__(self):
        if websocket is None:
            raise RuntimeError("websocket-client is required (`pip install websocket-client`).")
        page_tabs = []
        active_port = None
        for port in CDP_PORTS:
            try:
                tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=3).read())
                page_tabs = [t for t in tabs if t.get("type") == "page" and "flow.google" in t.get("url", "")]
                if page_tabs:
                    active_port = port
                    break
            except Exception:
                continue
        if not page_tabs:
            raise RuntimeError(
                f"No active Google Flow browser tab found on local CDP ports {CDP_PORTS}.\n"
                "Open Chrome on your workstation with `--remote-debugging-port=9225` logged into https://flow.google.com/u/0/ "
                "and re-run `bash pipeline/run_s01e01_duty_first_end_to_end.sh`."
            )
        print(f"Connected to Google Flow CDP on port {active_port}: {page_tabs[0].get('url')}", flush=True)
        self.ws = websocket.create_connection(page_tabs[0]["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)
        self.mid = 1
        self.cdp("DOM.enable")
        self.cdp("Page.enable")
        self.cdp("Browser.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": str(DL_DIR),
            "eventsEnabled": True,
        })

    def cdp(self, method: str, params: dict | None = None) -> dict:
        mid = self.mid
        self.mid += 1
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                return msg

    def js(self, expr: str):
        r = self.cdp("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        return r.get("result", {}).get("result", {}).get("value")

    def mouse_click(self, x: float, y: float):
        for ev in ("mousePressed", "mouseReleased"):
            self.cdp("Input.dispatchMouseEvent", {
                "type": ev, "x": float(x), "y": float(y), "button": "left", "clickCount": 1
            })

    def open_fresh_project(self):
        self.cdp("Page.navigate", {"url": "https://flow.google.com/u/0/"})
        time.sleep(4.5)
        self.js("""(() => {
            const btns = Array.from(document.querySelectorAll('button, a, [role="button"]'));
            const nb = btns.find(b => (b.innerText || '').includes('New project')) || btns.find(b => (b.innerText || '').includes('Start Creating'));
            if (nb) nb.click();
        })()""")
        for _ in range(20):
            time.sleep(1.0)
            if self.js("Boolean(location.href.includes('/project/') && document.querySelector('div.ProseMirror'))"):
                break
        time.sleep(1.0)
        for _ in range(4):
            c = self.js("""(() => {
                const b = Array.from(document.querySelectorAll('button')).find(x => ['Get started', 'Got it', 'Next'].includes((x.innerText||'').trim()));
                if (b) { b.click(); return b.innerText.trim(); }
                return null;
            })()""")
            if not c:
                break
            time.sleep(0.5)
        print("Opened project:", self.js("location.href"), flush=True)

    def configure_16x9(self):
        self.js("""(() => {
            const t = Array.from(document.querySelectorAll('button')).find(b => (b.innerText||'').trim() === 'tune');
            if (t) t.click();
        })()""")
        time.sleep(0.8)
        never_pos = self.js("""(() => {
            const nv = Array.from(document.querySelectorAll('mat-radio-button, [role="radio"]')).find(r => (r.innerText||'').includes('Never'));
            if (!nv) return null;
            const r = nv.getBoundingClientRect();
            return {x: r.left + 20, y: r.top + r.height/2};
        })()""")
        if never_pos:
            self.mouse_click(never_pos["x"], never_pos["y"])
            time.sleep(0.3)
        self.js("""(() => {
            const btns = Array.from(document.querySelectorAll('mat-button-toggle button, button')).filter(b => (b.innerText||'').includes('16:9'));
            btns.forEach(b => b.click());
            const x1s = Array.from(document.querySelectorAll('mat-button-toggle button, button')).filter(b => (b.innerText||'').trim() === 'x1');
            x1s.forEach(b => b.click());
        })()""")
        time.sleep(0.4)
        save_pos = self.js("""(() => {
            const sb = Array.from(document.querySelectorAll('button')).find(b => (b.innerText||'').trim() === 'Save');
            if (!sb) return null;
            const r = sb.getBoundingClientRect();
            return {x: r.left + r.width/2, y: r.top + r.height/2};
        })()""")
        if save_pos:
            self.mouse_click(save_pos["x"], save_pos["y"])
            time.sleep(0.8)
        self.js("document.querySelectorAll('.cdk-overlay-backdrop').forEach(b => b.click())")
        time.sleep(0.8)
        print("Configured Agent Settings: Never, 16:9, x1", flush=True)

    def close_overlays(self):
        self.js("document.querySelectorAll('.cdk-overlay-backdrop').forEach(b => b.click())")
        time.sleep(0.6)

    def clear_ingredients(self):
        self.close_overlays()
        for _ in range(6):
            removed = self.js("""(() => {
                const btns = Array.from(document.querySelectorAll('flow-ingredient-chip button, flow-ingredient-bar button'));
                const rm = btns.find(b => (b.innerText||'').includes('cancel') || (b.getAttribute('aria-label')||'').toLowerCase().includes('remove'));
                if (rm) { rm.click(); return true; }
                return false;
            })()""")
            if not removed:
                break
            time.sleep(0.25)

    def open_plus_menu(self):
        self.close_overlays()
        add_pos = self.js("""(() => {
            const b = document.querySelector('button[aria-label="Add ingredients to the prompt box"]');
            if (!b) return null;
            const r = b.getBoundingClientRect();
            return {x: r.left + r.width/2, y: r.top + r.height/2};
        })()""")
        if add_pos:
            self.mouse_click(add_pos["x"], add_pos["y"])
            time.sleep(1.0)

    def attach_ingredients(self, image_path: Path | None, include_me: bool):
        self.clear_ingredients()
        if image_path is not None and image_path.exists():
            stem = image_path.stem
            has_card = self.js(f"""(() => {{
                const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                return btns.some(b => ((b.getAttribute('aria-label')||'') + ' ' + (b.innerText||'')).includes({json.dumps(stem)}));
            }})()""")
            if not has_card:
                self.cdp("Page.setInterceptFileChooserDialog", {"enabled": True})
                self.open_plus_menu()
                self.js("""(() => {
                    const pop = document.querySelector('.cdk-overlay-pane, .add-menu-popover-container');
                    if (!pop) return;
                    const allTab = Array.from(pop.querySelectorAll('button, [role="button"], [role="tab"]')).find(b => (b.innerText||'').includes('dashboard') || (b.innerText||'').trim() === 'All');
                    if (allTab) allTab.click();
                })()""")
                time.sleep(0.6)
                up_pos = self.js("""(() => {
                    const pop = document.querySelector('.cdk-overlay-pane, .add-menu-popover-container');
                    if (!pop) return null;
                    const up = Array.from(pop.querySelectorAll('button, [role="button"]')).find(b => (b.innerText||'').includes('Upload media'));
                    if (!up) return null;
                    const r = up.getBoundingClientRect();
                    return {x: r.left + r.width/2, y: r.top + r.height/2};
                })()""")
                if up_pos:
                    self.mouse_click(up_pos["x"], up_pos["y"])

                t0 = time.time()
                while time.time() - t0 < 6:
                    self.ws.settimeout(1.0)
                    try:
                        ev = json.loads(self.ws.recv())
                        if ev.get("method") == "Page.fileChooserOpened":
                            bnid = ev["params"]["backendNodeId"]
                            self.ws.settimeout(30.0)
                            self.cdp("DOM.setFileInputFiles", {"backendNodeId": bnid, "files": [str(image_path)]})
                            break
                    except Exception:
                        pass
                self.ws.settimeout(30.0)
                self.cdp("Page.setInterceptFileChooserDialog", {"enabled": False})

                for _ in range(25):
                    time.sleep(1.0)
                    chips_now = self.js("document.querySelectorAll('flow-ingredient-chip').length") or 0
                    busy = self.js("Boolean(document.querySelector('flow-ingredient-chip [aria-busy=\"true\"]'))")
                    now_card = self.js(f"""(() => {{
                        const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                        return btns.some(b => ((b.getAttribute('aria-label')||'') + ' ' + (b.innerText||'')).includes({json.dumps(stem)}));
                    }})()""")
                    if (chips_now >= 1 and not busy) or now_card:
                        break
                time.sleep(1.2)
                self.close_overlays()

            has_img_chip = self.js("""(() => {
                return Array.from(document.querySelectorAll('flow-ingredient-chip')).some(c => !(c.innerText||'').includes('face'));
            })()""")
            if not has_img_chip:
                idx = self.js(f"""(() => {{
                    const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
                    for (let i = 1; i < btns.length; i++) {{
                        const lbl = (btns[i].getAttribute('aria-label')||'') + ' ' + (btns[i].innerText||'');
                        if (lbl.includes({json.dumps(stem)})) {{
                            for (let j = i - 1; j >= Math.max(0, i - 3); j--) {{
                                if (btns[j].getAttribute('aria-label') === 'More options') return j;
                            }}
                        }}
                    }}
                    return -1;
                }})()""")
                if idx is not None and idx >= 0:
                    self.js(f"Array.from(document.querySelectorAll('button, [role=\"button\"]'))[{idx}].click()")
                    time.sleep(0.7)
                    self.js("""(() => {
                        const add = Array.from(document.querySelectorAll('[role="menuitem"]')).find(i => (i.innerText||'').includes('Add to prompt'));
                        if (add) add.click();
                    })()""")
                    time.sleep(0.8)
                    self.close_overlays()

        if include_me:
            has_me_now = self.js("""(() => {
                return Array.from(document.querySelectorAll('flow-ingredient-chip, flow-likeness-ingredient-chip')).some(c => (c.innerText||'').includes('face') || c.tagName.includes('LIKENESS'));
            })()""")
            if not has_me_now:
                self.open_plus_menu()
                self.js("""(() => {
                    const pop = document.querySelector('.cdk-overlay-pane, .add-menu-popover-container');
                    if (!pop) return;
                    const avTab = Array.from(pop.querySelectorAll('button, [role="button"], [role="tab"]')).find(b => (b.innerText||'').includes('Avatars'));
                    if (avTab) avTab.click();
                })()""")
                time.sleep(0.9)
                self.js("""(() => {
                    const pop = document.querySelector('.cdk-overlay-pane, .add-menu-popover-container');
                    if (!pop) return;
                    const btns = Array.from(pop.querySelectorAll('button, [role="button"]'));
                    for (let i = 0; i < btns.length - 1; i++) {
                        if ((btns[i].innerText || '').trim() === 'Me' && (btns[i+1].innerText || '').includes('Add to prompt')) {
                            btns[i+1].click();
                            return;
                        }
                    }
                })()""")
                time.sleep(0.8)
                self.close_overlays()

        chips = self.js("document.querySelectorAll('flow-ingredient-chip').length")
        has_me = self.js("Array.from(document.querySelectorAll('flow-ingredient-chip')).some(c => (c.innerText||'').includes('face'))")
        print(f"  Ingredients ready: ref={image_path.name if image_path else 'None'}, chips={chips}, hasMe={has_me}", flush=True)

    def get_video_cards(self) -> list[dict]:
        return self.js("""(() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
            const out = [];
            for (let i = 0; i < btns.length - 1; i++) {
                if (btns[i].getAttribute('aria-label') === 'Reuse prompt' &&
                    !(btns[i].innerText || '').includes('keyboard_return') &&
                    btns[i+1].getAttribute('aria-label') === 'More options') {
                    out.push({
                        moreIdx: i + 1,
                        label: btns[i+2] ? (btns[i+2].getAttribute('aria-label') || btns[i+2].innerText || '') : ''
                    });
                }
            }
            return out;
        })()""") or []

    def submit_prompt(self, text: str):
        safe_text = text.replace("@Me", "Me").replace("@", "").strip()
        self.js(f"""(() => {{
            const el = document.querySelector('div.ProseMirror');
            el.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);
            document.execCommand('insertText', false, {json.dumps(safe_text)});
        }})()""")
        time.sleep(0.4)
        self.cdp("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
        self.cdp("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
        time.sleep(0.6)

    def run_sub_batch(self, batch_dir: Path, prefix: str, image_path: Path | None, include_me: bool, prompt_text: str, expected_count: int):
        batch_dir.mkdir(parents=True, exist_ok=True)
        existing = sorted(batch_dir.glob(f"{prefix}_*.mp4"))
        if len(existing) >= expected_count:
            print(f"⏭️  Skipping '{prefix}' — already has {len(existing)}/{expected_count} clips.", flush=True)
            return existing

        self.open_fresh_project()
        self.configure_16x9()
        self.attach_ingredients(image_path, include_me)
        before_len = len(self.get_video_cards())
        self.submit_prompt(prompt_text)
        print(f"🎬 Submitted '{prefix}' ({expected_count} widescreen 16:9 clips)...", flush=True)

        replied_go = False
        retried_timeout = 0
        t0 = time.time()
        while time.time() - t0 < 520:
            time.sleep(6)
            elapsed = int(time.time() - t0)
            tail = self.js(r"document.body.innerText.slice(-900).replace(/\s+/g, ' ')") or ""
            if retried_timeout < 2 and ("The agent timed out" in tail or "Try again" in tail):
                clicked_retry = self.js("""(() => {
                    const b = Array.from(document.querySelectorAll('button')).find(x => (x.innerText||'').trim() === 'Try again');
                    if (b) { b.click(); return true; }
                    return false;
                })()""")
                if clicked_retry:
                    retried_timeout += 1
                    print(f"    [{elapsed:3d}s] Flow transient timeout — clicked 'Try again' ({retried_timeout}/2)...", flush=True)
                    time.sleep(4)
                    continue

            ask_triggers = (
                "Option B", "How would you like to proceed", "Would you like me to",
                "shall I proceed", "confirm before", "ready for me to generate", "Let me know if"
            )
            if not replied_go and any(k.lower() in tail.lower() for k in ask_triggers) and len(self.get_video_cards()) == before_len:
                replied_go = True
                print(f"    [{elapsed:3d}s] Flow asked confirmation — sending immediate batch go-ahead...", flush=True)
                self.attach_ingredients(image_path, include_me)
                self.submit_prompt(f"Proceed immediately—generate all {expected_count} widescreen 16:9 video clips right now in batch without asking any questions!")
                continue

            cards_now = self.get_video_cards()
            new_cnt = len(cards_now) - before_len
            is_running = ("\nstop\n" in (self.js("document.body.innerText.toLowerCase()") or "")) or ("generating" in tail.lower())
            if elapsed % 18 == 0 or new_cnt >= expected_count:
                print(f"    [{elapsed:3d}s] {prefix}: newCards={new_cnt}/{expected_count} running={is_running}", flush=True)
            if new_cnt >= expected_count:
                time.sleep(3.0)
                break
            if new_cnt > 0 and not is_running and elapsed > 75:
                time.sleep(8.0)
                cards_recheck = len(self.get_video_cards()) - before_len
                still_running = "\nstop\n" in (self.js("document.body.innerText.toLowerCase()") or "")
                if cards_recheck == new_cnt and not still_running:
                    print(f"    [{elapsed+8:3d}s] {prefix}: generation settled with {new_cnt}/{expected_count} clips.", flush=True)
                    break

        cards_final = self.get_video_cards()
        new_cnt = max(0, len(cards_final) - before_len)
        saved = []
        for idx in range(new_cnt):
            c = self.get_video_cards()[idx]
            dest = batch_dir / f"{prefix}_{idx+1:02d}.mp4"
            before_mp4s = set(DL_DIR.glob("*.mp4"))
            self.js(f"Array.from(document.querySelectorAll('button, [role=\"button\"]'))[{c['moreIdx']}].click()")
            time.sleep(0.7)
            self.js("""(() => {
                const dl = Array.from(document.querySelectorAll('[role="menuitem"]')).find(i => (i.innerText||'').toLowerCase().includes('download'));
                if (dl) dl.click();
            })()""")
            time.sleep(0.7)
            self.js("""(() => {
                const orig = Array.from(document.querySelectorAll('[role="menuitem"]')).find(i => (i.innerText||'').includes('1080p') || (i.innerText||'').includes('720p') || (i.innerText||'').toLowerCase().includes('original'));
                if (orig) orig.click();
            })()""")
            for _ in range(24):
                time.sleep(0.6)
                crs = list(DL_DIR.glob("*.crdownload"))
                diff = [f for f in (set(DL_DIR.glob("*.mp4")) - before_mp4s) if f.stat().st_size > 200_000]
                if diff and not crs:
                    newest = sorted(diff, key=lambda p: p.stat().st_mtime, reverse=True)[0]
                    shutil.copy2(newest, dest)
                    saved.append({"file": dest.name, "label": c["label"], "size_mb": round(dest.stat().st_size / 1e6, 2)})
                    print(f"    ✅ Saved {dest.name} ({dest.stat().st_size/1e6:.2f} MB) <- {c['label']}", flush=True)
                    break
            self.js("document.body.click()")
            time.sleep(0.3)

        (batch_dir / f"{prefix}_manifest.json").write_text(json.dumps(saved, indent=2), encoding="utf-8")
        return saved

    def close(self):
        self.ws.close()


def main():
    ledger_path = export_ledger_json()
    flat = flatten_shot_ledger()
    if "--export-ledger" in sys.argv or "--dry-run" in sys.argv:
        spoken_shots = [s for s in flat if s["word_count"] > 0]
        min_w = min(s["word_count"] for s in spoken_shots)
        max_w = max(s["word_count"] for s in spoken_shots)
        print(f"✅ Exported 48-Shot Episode 1 ('Respect Your DUTY First') Ledger -> {ledger_path}")
        print(f"✅ Exported 12-Scene Storyboard Package -> {PACKAGE_JSON_PATH}")
        print(f"   Batches: {len(BATCH_SPECS)} | Total Shots: {len(flat)} | Spoken Word Range: {min_w}..{max_w} words/clip")
        for b in BATCH_SPECS:
            cnt = sum(len(sub["shots"]) for sub in b["mixed_sub_batches"]) if "mixed_sub_batches" in b else len(b["shots"])
            print(f"   • {b['id']} ({cnt} clips) — {b['cast_rule']}")
        return

    only_filter = sys.argv[1] if len(sys.argv) > 1 else None
    runner = FlowFilmRunner()
    try:
        for b in BATCH_SPECS:
            bid = b["id"]
            if only_filter and only_filter not in bid:
                continue
            bdir = EP_CLIPS_DIR / bid
            print(f"\n=== [{bid}] {b['title']} ({b['cast_rule']}) ===", flush=True)
            if "mixed_sub_batches" in b:
                for sub in b["mixed_sub_batches"]:
                    ref_img = resolve_repo_image(sub["ref_rel"])
                    prompt_txt = build_batch_prompt(sub["shots"], sub["include_me"], sub.get("extra_header", ""))
                    runner.run_sub_batch(bdir, sub["sub_prefix"], ref_img, sub["include_me"], prompt_txt, len(sub["shots"]))
            else:
                ref_img = resolve_repo_image(b["ref_rel"])
                prompt_txt = build_batch_prompt(b["shots"], b["include_me"])
                runner.run_sub_batch(bdir, bid, ref_img, b["include_me"], prompt_txt, len(b["shots"]))
        print("\n🏆 ALL 48 S01E01 'RESPECT YOUR DUTY FIRST' 16:9 GOOGLE FLOW CLIPS GENERATED & DOWNLOADED!", flush=True)
    finally:
        runner.close()


if __name__ == "__main__":
    main()
