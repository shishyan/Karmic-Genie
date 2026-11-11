#!/usr/bin/env bash
set -euo pipefail
# Redirected to current Episode 1 ("1. Respect Your DUTY First.") end-to-end Google Flow MCP pipeline:
exec bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_s01e01_duty_first_end_to_end.sh" "$@"
