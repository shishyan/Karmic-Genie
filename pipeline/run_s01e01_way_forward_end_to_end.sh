#!/usr/bin/env bash
set -euo pipefail

# End-to-End Local Google Flow 48-Shot Film Generator + Master Assembler for:
#   The Karmic Genie Show — S01E01: "The Way Forward (2026–2050)"
#
# Prerequisite on your local workstation:
#   Google Chrome running with `--remote-debugging-port=9225` and logged into https://flow.google.com/u/0/

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

echo "1/4 Exporting & verifying 48-shot Google Flow ledger..."
python3 pipeline/generate_s01e01_way_forward_flow_clips.py --export-ledger

echo "2/4 Rendering 12 RGBA glass cinema badges..."
python3 pipeline/render_s01e01_way_forward_overlays.py

echo "3/4 Generating & downloading all 48 widescreen 16:9 spoken cinema clips in Google Flow..."
python3 pipeline/generate_s01e01_way_forward_flow_clips.py "$@"

echo "4/4 Assembling 1080p -14 LUFS Master Film & Web Portal Cut..."
python3 pipeline/build_s01e01_way_forward_master_film.py

echo "✅ S01E01 'The Way Forward' Master Google Flow Film complete!"
