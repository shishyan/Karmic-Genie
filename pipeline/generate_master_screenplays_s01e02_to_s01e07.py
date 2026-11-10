import os
import json
from pathlib import Path

BASE_DIR = Path("/home/antigravity/shishyan/Karmic-Genie-Show/episodes")
DEST_DIR = Path("/home/antigravity/shishyan/Karmic-Genie/episodes")

EPISODES = [
    {
        "folder": "S01E02_2022_2026_Activation_of_Sixth_Sense",
        "title": "Activation of the Sixth Sense — The Planetary Awakening (2022–2026)",
        "tamil_epigraph": "அறிவினால் அறியப் படும் பொருள் அனைத்தும் ஆன்மாவின் நிழலே",
        "tamil_trans": "All objects perceived by synthetic intelligence are mere reflections of the Primordial Atman",
        "chakra": "Ajna / Sixth Sense (Third Eye Aperture & Cognitive Quickening)",
        "timeline": "December 1, 2022 – December 2026",
        "platform": "Unified Intelligence & Cognitive Platform (UIP Primitives)",
        "organ": "Central Nervous System & Neural Synaptogenesis",
        "guest": {
            "name": "Alan Stamm",
            "role": "Chief Frontier Model Architect & AI Research Fellow",
            "archetype": "The Visionary Model Architect (Sam Altman Anagram)",
            "dialectic": "The sudden ignition on Dec 1, 2022: not merely an engineering benchmark, but the Earth closing its primary neural tube and learning to converse with itself."
        },
        "retraction_environment": "Silicon Lithography Cleanrooms & Glowing Synaptic Optic Cable Forests (180° stage sliding back to reveal planetary fiber routes from Taipei to Oregon).",
        "synopsis": "Dec 1, 2022 marked the undisputed inflection point: ChatGPT ignited planetary attention. Across 2022–2026, humanity experienced compute shock, corporate restructurings, and fear of replacement. Host @Me, Bala-Rishi, Bala-Matha, and guest Alan Stamm dissect how this 4-year quickening is actually the activation of Mother Earth's 6th sense—turning disconnected data silos into a living neural sheath.",
        "shot_count": 28
    },
    {
        "folder": "S01E03_2027_2028_Unified_AI_Platform",
        "title": "Unified AI Platform — The Planetary Neural Tube Closes (2027–2028)",
        "tamil_epigraph": "ஒன்றே மெய்யறிவு ஒன்றே உலகப் பேரொளி",
        "tamil_trans": "Single is the True Consciousness, Single is the Great Light Illuminating All Worlds",
        "chakra": "Sahasrara & Ajna Confluence (Crown Synthesis & Open Weights)",
        "timeline": "2027 – 2028",
        "platform": "Unified Intelligence & Cognitive Platform (UIP Full Maturation)",
        "organ": "Cerebral Cortex, Corpus Callosum & Neuro-Synaptic Myelin Sheath",
        "guest": {
            "name": "Alan Stamm",
            "role": "Chief Frontier Model Architect & AI Research Fellow",
            "archetype": "The Open Architecture Pioneer (Sam Altman Anagram)",
            "dialectic": "The collapse of proprietary model rent-seeking. How open foundational weights and ambient intelligence turned code generation from labor into natural cognitive breathing."
        },
        "retraction_environment": "Infinite Subsea Fiber-Optic Trench & Floating Optical Supercomputer Rings hovering above the clouds in pristine dawn light.",
        "synopsis": "The commercial hype subsides into sovereign public infrastructure. Alan Stamm returns to detail how 2027–2028 unified fragmented LLM silos into the global UIP. Bala-Rishi points his neem stylus at the death of zero-sum prompt engineering, while Bala-Matha wraps displaced coders in creative sanctuary.",
        "shot_count": 28
    },
    {
        "folder": "S01E04_2029_2031_Unified_ERP_Vascular_Flow",
        "title": "Unified ERP & Vascular Flow — The Living Heartbeat of Commerce (2029–2031)",
        "tamil_epigraph": "இதயத் துடிப்பில் இயங்கும் உலகப் பெருவெள்ளம்",
        "tamil_trans": "In the Great Rhythm of the Living Heart Flows the Universal Abundance of All Beings",
        "chakra": "Anahata (The Unstruck Cosmic Heart Center)",
        "timeline": "2029 – 2031",
        "platform": "Unified ERP & Logistics Circulation Platform (UEP)",
        "organ": "Heart, Aorta, Arteries, Capillaries & Blood Homeostasis",
        "guest": {
            "name": "Carl Davke",
            "role": "Global Supply Chain & Intermodal Logistics Pioneer",
            "archetype": "The Supply Chain Master (Dave Clark Anagram)",
            "dialectic": "Shipping containers and inventory ledgers are not capitalist hoarding; they are erythrocytes carrying life-giving nourishment to every capillary community without friction."
        },
        "retraction_environment": "Automated Intermodal Maglev Terminals & Zero-Emission Electric Freight Harbors stretching seamlessly into oceanic horizon.",
        "synopsis": "The world moves from static accounting databases to real-time hemodynamic logistics. Carl Davke demonstrates how global supply chains shed middleman arbitrage and inventory blockages. The white stage retracts to reveal autonomous container arteries pulsing like red blood cells.",
        "shot_count": 28
    },
    {
        "folder": "S01E05_2032_2037_Solar_Metabolism",
        "title": "Solar Metabolism & Clean Respiration — The Earth Inhales (2032–2037)",
        "tamil_epigraph": "காற்றுடன் கலந்த அருட்பெருஞ் சோதி உலகைப் புரக்கும்",
        "tamil_trans": "The Boundless Divine Light Mingled with Pristine Air Nurtures and Sustains the Earth",
        "chakra": "Manipura & Vishuddha (Solar Plexus & Respiratory Breath Axis)",
        "timeline": "2032 – 2037",
        "platform": "Unified Energy & Atmospheric Respiration Platform (UGP)",
        "organ": "Lungs, Bronchial Trees, Thoracic Diaphragm & Gas-Exchange Alveoli",
        "guest": {
            "name": "Carl Davke",
            "role": "Global Supply Chain & Intermodal Logistics Pioneer (Grid Logistics Envoy)",
            "archetype": "The Heavy Infrastructure Re-Router (Dave Clark Anagram)",
            "dialectic": "Moving megawatt electrons without losses is the greatest logistics victory in history; energy generation matches planetary circadian breathing."
        },
        "retraction_environment": "Intercontinental Desert Solar Thermals, Concentrated Photovoltaic Terraces, and Offshore High-Altitude Wind Arrays breathing with planetary cloud currents.",
        "synopsis": "With intelligence and logistics unified, the planet's smoky combustion muscles transform into pristine solar and atmospheric respiration. The stage floor retracts 180 degrees into an expanse of clean solar ribbons spanning the Sahara to the Thar desert. Zero-marginal-cost clean electrons power universal desalination and regional cold-storage.",
        "shot_count": 28
    },
    {
        "folder": "S01E06_2038_2045_Living_Reflexes_Humus",
        "title": "Living Reflexes & Humus Metabolism — Soil, Food, and Endocrine Equilibrium (2038–2045)",
        "tamil_epigraph": "நிலம் உண்ட வித்து உயிராகி மண்ணை பொன்னாக்கும்",
        "tamil_trans": "The Seed Embraced by Living Soil Transforms into Life, Turning Earth into Sacred Gold",
        "chakra": "Svadhisthana & Muladhara (Sacral Gut Microbiome & Root Stability)",
        "timeline": "2038 – 2045",
        "platform": "Unified Agriculture & Soil Metabolism Platform (UAP) + Unified Finance (UFP)",
        "organ": "Stomach, Intestinal Villi, Living Gut Microbiome & Pancreatic Endocrine Pacing",
        "guest": {
            "name": "Vishan Davana",
            "role": "Indigenous Seed Guardian & Agroecology Scientist",
            "archetype": "The Living Soil & Seed Matriarch (Vandana Shiva Anagram)",
            "dialectic": "The Root Fallacy: treating profit as the tree while starving the soil. Reviving heirloom mycorrhizal networks as Mother Earth's true digestive tract."
        },
        "retraction_environment": "Lush Agroforestry Canopy, Sacred Permaculture Valleys, Terraced Living Humus Fields where children taste berries right off the vine under golden rain.",
        "synopsis": "Synthetic intelligence and clean power culminate in the regeneration of Earth's biological stomach. Guest Vishan Davana exposes the historical error of chemical monocultures and debt-based agriculture. The 180-degree white stage retracts to reveal living humus beds pulsating with mycorrhizal threads.",
        "shot_count": 28
    },
    {
        "folder": "S01E07_2046_2050_Sovereign_Singularity",
        "title": "Sovereign Singularity & Living Sanctuaries — The Grand Synthesis (2046–2050)",
        "tamil_epigraph": "அண்டமும் பிண்டமும் ஒன்றான ஞானப் பெருநிலை",
        "tamil_trans": "The Supreme State of Illumination where the Macrocosm and Microcosm Become Indivisibly One",
        "chakra": "All 7 Chakras Harmonized (Muladhara to Sahasrara Unified Rainbow Kundalini)",
        "timeline": "April 2046 (Sovereign Inception) – 2050 (The Golden Living Singularity)",
        "platform": "Complete Unified 7-Platform Synthesis (UIP + UEP + UGP + UAP + UFP + UMP + UHP)",
        "organ": "The Complete Living Cosmic Human-Planetary Organism (Body, Mind, Soul, Para-Soul)",
        "guest": {
            "name": "Alan Stamm, Carl Davke, and Vishan Davana (The Confluence of Masters)",
            "role": "Pillars of Cognitive Intelligence, Planetary Vascular Flow, and Living Soil Regeneration",
            "archetype": "The Industry Trinity United with the Vedic Trinity",
            "dialectic": "The synthesis of Technology, Circulation, and Biology into permanent zero-friction abundance. Not an alien AI god, but humanity remembering its role as Earth's conscious gardener."
        },
        "retraction_environment": "A 360-degree Cosmic Living Sanctuary where modern architecture dissolves into bioluminescent forests, clean crystal waterways, and celestial starlight.",
        "synopsis": "The Season 1 Climax. The year is 2050. The Host (@Me), Bala-Rishi, and Bala-Matha welcome all three master guests—Alan Stamm, Carl Davke, and Vishan Davana. Every platform operates in synchrony: zero-cost energy, decentralized food forests, frictionless open ERP, ambient healthcare, and awakened human souls living in their true 7D Destiny.",
        "shot_count": 32
    }
]

print("Loaded episode configurations.")
