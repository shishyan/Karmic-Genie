#!/usr/bin/env bash
set -euo pipefail

# End-to-End Google Flow MCP 48-Shot Film Generator + Master Assembler for:
#   The Karmic Genie Show — S01E01: "The Way Forward (2026–2050)"
#
# Automatically launches local Chrome on CDP port 9225 if on a desktop workstation,
# or attaches to an existing `--remote-debugging-port=9225` session logged into https://flow.google.com/u/0/

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

echo "1/3 Exporting & verifying 48-shot Google Flow ledger..."
python3 pipeline/generate_s01e01_way_forward_flow_clips.py --export-ledger

echo "2/3 Rendering 12 RGBA glass cinema badges..."
python3 pipeline/render_s01e01_way_forward_overlays.py

echo "3/3 Running Google Flow MCP v3.0 Full-Film Engine (48 widescreen 16:9 clips + 1080p -14 LUFS Master Assembly)..."
if [ "$#" -gt 0 ]; then
    python3 pipeline/google_flow_mcp_s01e01_storyboard.py --run-batch "$1"
    python3 pipeline/google_flow_mcp_s01e01_storyboard.py --assemble
else
    python3 pipeline/google_flow_mcp_s01e01_storyboard.py --full-film
fi

echo "✅ S01E01 'The Way Forward' Master Google Flow Film pipeline finished!"
