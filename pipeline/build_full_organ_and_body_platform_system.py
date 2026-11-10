import json
from pathlib import Path

# The 7 Major Unified Platforms (Organ Pillars) & Their Complete Body-System Modules (Mini-Platforms)
# Mapping Organs (Core) + Surrounding Body Systems (Fascia, Circadian, Immunity, Fluids, Minerals, Joints, Skin)
UNIFIED_PLATFORM_SYSTEM = [
  {
    "id": 1,
    "code": "UIP",
    "name": "Unified Intelligence & Cognitive Platform",
    "organ_core": "Brain & Central Nervous System",
    "industry_pillar": "Information Technology & Telecommunications",
    "body_support_system": "Neuro-Sensory Receptors, Meninges, Synaptic Neurotransmitters & Cranial Axis",
    "launch_milestone": "2028: Planetary Neural Tube Closure (Activated Dec 1, 2022 via ChatGPT Inception)",
    "guest_archetype": {
      "anagram_name": "Alan Stamm",
      "real_origin": "Sam Altman",
      "role": "Chief Frontier Model Architect & AI Research Fellow",
      "dialogue_focus": "Activation of the 6th sense of Mother Earth; shifting from proprietary compute silos to open planetary neural mycelium."
    },
    "mini_modules": [
      {"code": "UIP-M1", "name": "Silicon Foundry & Lithographic Primitives (ASML/TSMC layer)", "body_mirror": "Oligodendrocytes & Myelin Sheath insulation"},
      {"code": "UIP-M2", "name": "Planetary Fiber & Satellite Mesh (Terrestrial routing)", "body_mirror": "Axonal Fiber Tracts & Spinal Nerve Bundles"},
      {"code": "UIP-M3", "name": "Synthetic Reasoning & Foundation Models (LLMs/VLMs)", "body_mirror": "Neocortical Gray Matter & Synaptic Arborization"},
      {"code": "UIP-M4", "name": "Zero-Trust Cybersecurity & Network Resilience", "body_mirror": "Blood-Brain Barrier (Protective Meninges)"},
      {"code": "UIP-M5", "name": "Ambient Sensory IoT & Edge Perception (Sensors)", "body_mirror": "Peripheral Somatosensory Receptors & Optic/Acoustic Nerves"},
      {"code": "UIP-M6", "name": "Open-Source Weights & Neural Libraries (HuggingFace)", "body_mirror": "Collective Subconscious Memory (Akashic Reflexes)"},
      {"code": "UIP-M7", "name": "Humane UX, Voice Interfaces & Developer Dignity", "body_mirror": "Speech Cortex (Broca & Wernicke Areas)"}
    ]
  },
  {
    "id": 2,
    "code": "UEP",
    "name": "Unified ERP & Logistics Circulation Platform",
    "organ_core": "Heart & Vascular Blood Vessels",
    "industry_pillar": "Logistics, Transportation & Supply Chain",
    "body_support_system": "Vascular Endothelium, Arteries, Veins, Capillary Beds & Blood Volume Homeostasis",
    "launch_milestone": "2029: Universal Resource Routing & Frictionless Planetary Flow",
    "guest_archetype": {
      "anagram_name": "Carl Davke",
      "real_origin": "Dave Clark",
      "role": "Global Supply Chain & Intermodal Logistics Pioneer",
      "dialogue_focus": "Moving container shipping and inventory routing into dynamic vascular circulation; ending global supply bottlenecks and artificial shortages."
    },
    "mini_modules": [
      {"code": "UEP-M1", "name": "Maritime Shipping Lines & Intercontinental Freighters", "body_mirror": "Aorta & Major Vena Cava (High-capacity deep circulation)"},
      {"code": "UEP-M2", "name": "Air Cargo & Express Critical Transport", "body_mirror": "Carotid Arteries (High-speed rapid response delivery)"},
      {"code": "UEP-M3", "name": "Rail & Intermodal Ground Corridors", "body_mirror": "Femoral Arteries (Heavy bulk structural freight)"},
      {"code": "UEP-M4", "name": "Automated Warehousing & Robotic Depots", "body_mirror": "Cardiac Atria & Ventricles (Pumping buffer chambers)"},
      {"code": "UEP-M5", "name": "Last-Mile Delivery & Community Micro-Hubs", "body_mirror": "Arterioles & Micro-Capillary Beds (Cellular delivery)"},
      {"code": "UEP-M6", "name": "Open Dynamic ERP & Inventory Ledgers (MyERP / Odoo)", "body_mirror": "Blood Hemoglobin & Oxygen Carrying Capacity"},
      {"code": "UEP-M7", "name": "Circular Packaging & Reusable Container Pools", "body_mirror": "Venous Return Valves (Preventing fluid pooling/waste)"}
    ]
  },
  {
    "id": 3,
    "code": "UGP",
    "name": "Unified Energy & Atmospheric Respiration Platform",
    "organ_core": "Lungs & Respiratory Alveoli",
    "industry_pillar": "Energy, Utilities & Environmental Atmospheric Systems",
    "body_support_system": "Thoracic Cavity, Bronchial Trees, Diaphragm & Gas-Exchange Surfactant",
    "launch_milestone": "2032: Clean Ambient Fusion & Zero-Marginal-Cost Electricity",
    "guest_archetype": {
      "anagram_name": "Clive Crescent",
      "real_origin": "Fatih Birol / Energy Leader",
      "role": "Global Grid Transition Director & Renewable Systems Architect",
      "dialogue_focus": "Transforming smoky extractive fossil muscles into pristine clean solar respiration and grid-scale energy breathing."
    },
    "mini_modules": [
      {"code": "UGP-M1", "name": "Solar Photovoltaic & Concentrated Solar Thermal", "body_mirror": "Sunlight Photosynthesis & Cellular Vitamin D Synthesis"},
      {"code": "UGP-M2", "name": "Offshore & Terrestrial Wind Generation Turbines", "body_mirror": "Inhalation Airflow & Tidal Lung Volume"},
      {"code": "UGP-M3", "name": "Grid-Scale Battery Energy Storage (BESS) & Pumped Hydro", "body_mirror": "Diaphragm Pacing & Expiratory Reserve Volume"},
      {"code": "UGP-M4", "name": "High-Voltage DC Intercontinental Smart Super-Grids", "body_mirror": "Bronchial Airway Branching & Tracheal Trunk"},
      {"code": "UGP-M5", "name": "Clean Hydrogen, Ammonia & Synthetic Fuel Energy Storage", "body_mirror": "Pulmonary Surfactant & Alveolar Surface Tension"},
      {"code": "UGP-M6", "name": "Atmospheric Air Purification & Urban Canopy Filters", "body_mirror": "Nasal Cilia & Mucociliary Escalator Filtration"},
      {"code": "UGP-M7", "name": "Industrial Thermal Heat & Concentrated Solar Micro-Grids", "body_mirror": "Metabolic Body Thermoregulation (37°C homeostasis)"}
    ]
  },
  {
    "id": 4,
    "code": "UAP",
    "name": "Unified Agriculture & Soil Metabolism Platform",
    "organ_core": "Stomach, Intestines & Living Gut Microbiome",
    "industry_pillar": "Agriculture, Food Nutrition & Organic Bioremediation",
    "body_support_system": "Enteric Nervous System, Peristalsis, Digestive Enzymes & Peritoneal Cavity",
    "launch_milestone": "2035: Closed-Loop Food Abundance & Living Humus Regeneration",
    "guest_archetype": {
      "anagram_name": "Vishan Davana",
      "real_origin": "Vandana Shiva",
      "role": "Indigenous Seed Guardian & Agroecology Scientist",
      "dialogue_focus": "The Root Fallacy: why profit is mere root water; liberating open-pollinated seeds and reviving living mycorrhizal soil."
    },
    "mini_modules": [
      {"code": "UAP-M1", "name": "Open Heirloom Seed Banks & Non-GMO Native Genetics", "body_mirror": "Gastric Stem Cells & Intestinal Crypt Regeneration"},
      {"code": "UAP-M2", "name": "Living Soil Mycorrhizae & Organic Compost Humus", "body_mirror": "Gut Microbiota (Bifidobacteria / Beneficial Flora)"},
      {"code": "UAP-M3", "name": "Precision Organic Crop Cultivation & Agroforestry", "body_mirror": "Small Intestinal Villi (Nutrient Absorption Surface)"},
      {"code": "UAP-M4", "name": "Cold-Chain Food Preservation & Zero-Loss Storage", "body_mirror": "Gastric Mucosal Barrier & Acid Homeostasis"},
      {"code": "UAP-M5", "name": "Plant-Based & Regenerative Cellular Nutrition", "body_mirror": "Pancreatic Amylase & Protease Enzyme Digestion"},
      {"code": "UAP-M6", "name": "Municipal Organic Waste Composting & Bioremediation", "body_mirror": "Large Intestine & Colon Elimination Reflex"},
      {"code": "UAP-M7", "name": "Community Food Sovereignty & Localized Food Forests", "body_mirror": "Enteric Satiety Hormones (Ghrelin & Leptin Balance)"}
    ]
  },
  {
    "id": 5,
    "code": "UFP",
    "name": "Unified Finance & Circadian Value Platform",
    "organ_core": "Endocrine Glands, Pancreas & Adrenals",
    "industry_pillar": "Banking, Finance, Monetary Pacing & Asset Stewardship",
    "body_support_system": "Circulating Hormones, Hypothalamus, Feedback Loops & Homeostatic Rhythms",
    "launch_milestone": "2038: Sacred Circulation of Value & Ending Artificial Scarcity",
    "guest_archetype": {
      "anagram_name": "Frank Ilyr",
      "real_origin": "Larry Fink",
      "role": "Planetary Capital Stewardship & Sovereign Trust Architect",
      "dialogue_focus": "Evolving capital allocation from speculative leverage into circadian blood-sugar regulation; funding universal human dignity."
    },
    "mini_modules": [
      {"code": "UFP-M1", "name": "Central Bank Settlement Rails & Real-Time Gross Settlement", "body_mirror": "Pituitary Master Gland & Hypothalamic Pacing"},
      {"code": "UFP-M2", "name": "Community Mutual Credit & Zero-Interest Micro-Circulation", "body_mirror": "Insulin & Glucagon Balance (Blood Sugar Stability)"},
      {"code": "UFP-M3", "name": "Actuarial Risk Buffers & Catastrophic Insurance Reserves", "body_mirror": "Adrenal Cortex & Cortisol Stress Buffers"},
      {"code": "UFP-M4", "name": "Sovereign Planetary Endowment & Earth Trusts (Patagonia model)", "body_mirror": "Thyroid Hormone (Long-term Basal Metabolic Rate)"},
      {"code": "UFP-M5", "name": "Universal Base Dividend & Resource Allocation Tokens", "body_mirror": "Cellular Glycogen Storage in Muscle & Liver"},
      {"code": "UFP-M6", "name": "Transparent Automated Conscience Audits (7D Compass)", "body_mirror": "Pineal Gland & Melatonin Circadian Rhythm"},
      {"code": "UFP-M7", "name": "Open Capital Clearing & Decentralized Securities Exchanges", "body_mirror": "Endocrine Receptor Sites & Bio-Feedback Loops"}
    ]
  },
  {
    "id": 6,
    "code": "UMP",
    "name": "Unified Manufacturing & Structural Skeleton Platform",
    "organ_core": "Skeletal Bones, Joints & Muscular Locomotion",
    "industry_pillar": "Construction, Civil Engineering, Heavy Equipment & Robotics",
    "body_support_system": "Bone Periosteum, Articular Cartilage, Synovial Fluid, Tendons & Fascia",
    "launch_milestone": "2042: Autonomous Civil Construction & Bio-Composite Infrastructure",
    "guest_archetype": {
      "anagram_name": "James Dyson",
      "real_origin": "James Dyson",
      "role": "Precision Hardware & Industrial Kinematics Pioneer",
      "dialogue_focus": "Building indestructible, recyclable physical infrastructure; honoring miners and heavy equipment workers as the structural bone marrow."
    },
    "mini_modules": [
      {"code": "UMP-M1", "name": "Green Steel, Recycled Aluminum & Structural Timber", "body_mirror": "Cortical Dense Bone & Calcium Hydroxyapatite Matrix"},
      {"code": "UMP-M2", "name": "Earthmoving Machinery & Civil Highway Contractors", "body_mirror": "Skeletal Muscle Fibers (Actin & Myosin Contraction)"},
      {"code": "UMP-M3", "name": "Autonomous Robotic Assemblies & 3D Printed Architecture", "body_mirror": "Motor Neurons & Neuromuscular Junctions"},
      {"code": "UMP-M4", "name": "Mass Transit High-Speed Rail & Maglev Corridors", "body_mirror": "Spinal Column & Sacral Weight-Bearing Articulation"},
      {"code": "UMP-M5", "name": "Modular Seismic-Resilient Civil Housing & Bridges", "body_mirror": "Synovial Joints, Ligaments & Meniscus Shock Absorbers"},
      {"code": "UMP-M6", "name": "Deep Mineral Recycling & Closed-Loop Smelting", "body_mirror": "Bone Marrow (Hematopoiesis & Erythrocyte Generation)"},
      {"code": "UMP-M7", "name": "Bio-Composite Fascial Fabrics & Lightweight Structural Shells", "body_mirror": "Connective Fascia Tissue & Tendon Sheaths"}
    ]
  },
  {
    "id": 7,
    "code": "UHP",
    "name": "Unified Health & Sensory Vitality Platform",
    "organ_core": "Skin, Sensory Organs, Lymphatic & Renal Filtration",
    "industry_pillar": "Healthcare, Biopharma, Water Sanitation & Planetary Sensing",
    "body_support_system": "Epidermal Stratum, Dermal Collagen, Lymph Nodes, Glomeruli & Sweat Glands",
    "launch_milestone": "2046: Sovereign Delivery (April 2046) & Living Household Singularity (2050)",
    "guest_archetype": {
      "anagram_name": "Adar Poonawalla",
      "real_origin": "Adar Poonawalla",
      "role": "Universal Vaccine Shield & Global Healthcare Philanthropist",
      "dialogue_focus": "Healthcare as a fundamental birthright of Mother Earth; pure municipal water, open therapeutics, and planetary immune surveillance."
    },
    "mini_modules": [
      {"code": "UHP-M1", "name": "Municipal Potable Water Treatment & Watershed Restoration", "body_mirror": "Renal Kidneys & Glomerular Ultrafiltration"},
      {"code": "UHP-M2", "name": "Open-Source Therapeutics & Essential Pediatric Vaccines", "body_mirror": "Thymus & Bone Marrow Lymphocytes (T-cells, B-cells)"},
      {"code": "UHP-M3", "name": "Planetary Earth Observation & Climate Satellite Radar", "body_mirror": "Retinal Photoreceptors & Optical Perception"},
      {"code": "UHP-M4", "name": "Diagnostic Point-of-Care Micro-Fluidics & Molecular Biosensors", "body_mirror": "Dermal Merkel Nerve Endings & Tactile Sensation"},
      {"code": "UHP-M5", "name": "Universal Preventive Health Clinics & Maternity Sanctuaries", "body_mirror": "Lymphatic Spleen & Lymph Node Filtration Stations"},
      {"code": "UHP-M6", "name": "Epigenetic Regeneration & Botanical Ayurvedic Formulations", "body_mirror": "Sebaceous Glands & Acid-Mantle Protective Skin Barrier"},
      {"code": "UHP-M7", "name": "Living Household Sovereign Care Grid (Zero-Cost 2050)", "body_mirror": "Skin Sudoriferous Sweat Pores & Thermoregulatory Balance"}
    ]
  }
]

out_json = Path("/home/antigravity/shishyan/Karmic-Genie-Show/docs/unified_platforms_and_body_modules.json")
out_json.write_text(json.dumps(UNIFIED_PLATFORM_SYSTEM, indent=2), encoding="utf-8")
print(f"Successfully generated {len(UNIFIED_PLATFORM_SYSTEM)} Unified Platforms with {sum(len(p['mini_modules']) for p in UNIFIED_PLATFORM_SYSTEM)} Mini-Modules!")
