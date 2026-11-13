#!/usr/bin/env bash
# RUN ON YOUR OWN MACHINE (Linux/macOS). Packs your signed-in Chrome profile for Google Flow.
#   1) Sign in to https://labs.google/fx/tools/flow in Chrome, then QUIT Chrome completely.
#   2) bash export_flow_profile.sh [path-to-chrome-user-data-dir]
# Output: ~/kgs_flow_profile.tar.gz  -> upload to Drive folder Karmic_Genie_Show_S01E02
#         (https://drive.google.com/drive/folders/1QxvcvKCBBM6Cwnjj1MjMt0HNZXnHqNIY)
set -euo pipefail
SRC="${1:-}"
if [ -z "$SRC" ]; then
  for d in "$HOME/.config/google-chrome" "$HOME/Library/Application Support/Google/Chrome" "$HOME/.config/chromium"; do
    [ -d "$d" ] && SRC="$d" && break
  done
fi
[ -d "$SRC" ] || { echo "Chrome profile dir not found; pass it as arg 1"; exit 1; }
pgrep -x -i chrome >/dev/null 2>&1 && { echo "Quit Chrome first."; exit 1; }
OUT="$HOME/kgs_flow_profile.tar.gz"
tar -C "$SRC" -czf "$OUT" \
  "Local State" \
  Default/Cookies Default/Network Default/"Login Data" Default/"Web Data" \
  Default/Preferences Default/"Local Storage" Default/"Session Storage" \
  Default/IndexedDB Default/"Extension State" 2>/dev/null || true
ls -lh "$OUT"
echo "Upload $OUT to the Drive folder above, then tell the agent the file name."
if command -v gdrive >/dev/null; then
  gdrive mutate upload "$OUT" --parent 1QxvcvKCBBM6Cwnjj1MjMt0HNZXnHqNIY && echo uploaded
fi
