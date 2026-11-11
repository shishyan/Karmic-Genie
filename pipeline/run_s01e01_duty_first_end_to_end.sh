#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# THE KARMIC GENIE SHOW — EPISODE 1 (`S01E01`): "1. RESPECT YOUR DUTY FIRST."
# End-to-End Google Flow MCP + 48-Shot Widescreen (16:9, -14 LUFS) Film Runner
# ==============================================================================

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

echo "=========================================================================="
echo "🎬 KARMIC GENIE SHOW — S01E01: '1. RESPECT YOUR DUTY FIRST.' (EPIC FILM)"
echo "=========================================================================="

echo "1️⃣ Exporting 12-Scene @Me Storyboard Package & 48-Shot Flow Ledger (DF01..DF48)..."
python3 pipeline/generate_s01e01_duty_first_flow_clips.py --export-ledger

echo "2️⃣ Rendering 12 RGBA Cinema Glass Badges..."
python3 pipeline/render_s01e01_duty_first_overlays.py

echo "3️⃣ Checking Google Flow MCP Connection (Ports 9225 / 9222)..."
python3 pipeline/google_flow_mcp_s01e01_storyboard.py --status

echo "4️⃣ Running End-to-End Google Flow MCP Full-Film Engine..."
python3 pipeline/google_flow_mcp_s01e01_storyboard.py --full-film
