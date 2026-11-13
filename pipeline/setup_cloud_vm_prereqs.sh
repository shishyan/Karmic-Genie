#!/usr/bin/env bash
# One-time cloud-VM prerequisites for Karmic Genie Show + Spotify episode builds.
# User-space only (no sudo). Idempotent: safe to re-run.
#   usage: bash pipeline/setup_cloud_vm_prereqs.sh [start-chrome]
set -euo pipefail
VENV="$HOME/.venvs/kgs"
PROFILE="$HOME/.config/kgs-flow-chrome"
CDP_PORT=9225

echo "== 1. System tools check =="
for t in ffmpeg ffprobe python3 uv node; do
  command -v "$t" >/dev/null || { echo "MISSING: $t"; exit 1; }
done
CHROME="$(command -v google-chrome || command -v chromium || true)"
[ -n "$CHROME" ] || { echo "MISSING: chrome/chromium"; exit 1; }
ENCS="$(ffmpeg -hide_banner -encoders 2>/dev/null || true)"
case "$ENCS" in *libx264*) ;; *) echo "ffmpeg lacks libx264"; exit 1;; esac

echo "== 2. Python venv + libs =="
[ -d "$VENV" ] || uv venv "$VENV"
uv pip install --python "$VENV/bin/python" -q \
  faster-whisper numpy pillow websockets requests playwright \
  google-api-python-client google-auth-oauthlib

echo "== 3. Whisper tiny.en model cache =="
"$VENV/bin/python" - <<'PY'
from faster_whisper import WhisperModel
WhisperModel("tiny.en", device="cpu", compute_type="int8"); print("tiny.en ready")
PY

echo "== 4. Drive-skills sync =="
[ -x "$HOME/scripts/install_drive_skills.sh" ] && "$HOME/scripts/install_drive_skills.sh" || true

echo "== 5. Chrome profile for Google Flow (CDP $CDP_PORT) =="
mkdir -p "$PROFILE"
if [ "${1:-}" = "start-chrome" ]; then
  nohup "$CHROME" --headless=new --no-sandbox --remote-debugging-port=$CDP_PORT \
    --user-data-dir="$PROFILE" --window-size=1920,1080 about:blank \
    >/tmp/kgs_chrome.log 2>&1 &
  sleep 3; curl -s "http://localhost:$CDP_PORT/json/version" | head -3
fi

cat <<EOF

DONE. Remaining ONE-TIME HUMAN steps (cannot be automated):
  * Sign in to Google Flow ULTRA inside the Chrome profile $PROFILE
    (Google login/2FA must be completed by you in a visible browser).
  * Colab L4 has no CLI on this VM; GPU render is optional (CPU libx264 fallback is used).
Python: $VENV/bin/python   Chrome: $CHROME
EOF
