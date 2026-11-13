#!/usr/bin/env bash
# RUN ON THE CLOUD VM after uploading kgs_flow_profile.tar.gz to Drive.
#   bash import_flow_profile.sh [drive-file-id | local-tar-path]
set -euo pipefail
ARG="${1:-}"
P="$HOME/.config/kgs-flow-chrome"
T=/tmp/kgs_flow_profile.tar.gz
if [ -f "$ARG" ]; then cp "$ARG" "$T"; elif [ -n "$ARG" ]; then gdrive readonly download "$ARG" --out "$T"
else f=$(ls "$HOME"/upload/kgs_flow_profile*.tar.gz | head -1); cp "$f" "$T"; fi
for p in $(pgrep -f "user-data-dir=$P" || true); do kill "$p" 2>/dev/null || true; done
sleep 2; rm -rf "$P"; mkdir -p "$P"; tar -C "$P" -xzf "$T"; rm -f "$P"/Singleton*
nohup google-chrome --headless=new --no-sandbox --remote-debugging-port=9225 \
  --user-data-dir="$P" https://labs.google/fx/tools/flow >/tmp/kgs_chrome.log 2>&1 &
sleep 8
curl -s localhost:9225/json | grep -E '"(title|url)"' | head -4
echo "If the URL shows accounts.google.com, the session was rejected (re-login needed)."
