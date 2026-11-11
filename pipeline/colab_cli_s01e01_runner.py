#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Colab CLI (`googlecolab/google-colab-cli`) OAuth Completion & Remote GPU Film Runner
for The Karmic Genie Show — Episode 1 (`S01E01`): "1. Respect Your DUTY First."

Modes:
  1. Generate OAuth authorization URL (persists PKCE code_verifier in ~/.gemini/colab_cli_pending_oauth.json):
       python3 pipeline/colab_cli_s01e01_runner.py --auth-url
  2. Complete OAuth authorization with the one-time code from Google's browser consent screen:
       python3 pipeline/colab_cli_s01e01_runner.py --complete-auth "<AUTH_CODE>"
  3. Check Colab CLI session & GPU quota status:
       python3 pipeline/colab_cli_s01e01_runner.py --status
  4. Provision an L4/T4 Colab GPU session and run the Episode 1 GPU video render remotely:
       python3 pipeline/colab_cli_s01e01_runner.py --render-gpu
"""

import argparse
import json
import os
import subprocess
import sys
from importlib import resources
from pathlib import Path

COLAB_PYTHON = Path.home() / ".local" / "share" / "uv" / "tools" / "google-colab-cli" / "bin" / "python"
COLAB_BIN = Path.home() / ".local" / "bin" / "colab"
STATE_FILE = Path.home() / ".gemini" / "colab_cli_pending_oauth.json"
REPO_DIR = Path(__file__).resolve().parent.parent


def ensure_colab_cli():
    if not COLAB_BIN.exists() or not COLAB_PYTHON.exists():
        subprocess.run(["uv", "tool", "install", "--with", "keyrings.alt", "google-colab-cli"], check=True)


def generate_auth_url():
    ensure_colab_cli()
    code = """
import json
from importlib import resources
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
import colab_cli.auth as ca

cfg = json.loads(resources.files("colab_cli").joinpath("oauth_config.json").read_text())
flow = InstalledAppFlow.from_client_config(cfg, ca.PUBLIC_SCOPES)
flow.redirect_uri = ca.REMOTE_REDIRECT_URI
auth_url, state = flow.authorization_url(prompt="consent", token_usage="remote", access_type="offline")

state_file = Path.home() / ".gemini" / "colab_cli_pending_oauth.json"
state_file.parent.mkdir(parents=True, exist_ok=True)
state_file.write_text(json.dumps({
    "client_config": cfg,
    "scopes": ca.PUBLIC_SCOPES,
    "redirect_uri": ca.REMOTE_REDIRECT_URI,
    "code_verifier": flow.code_verifier,
    "state": state,
    "auth_url": auth_url,
}, indent=2))
print(auth_url)
"""
    out = subprocess.check_output([str(COLAB_PYTHON), "-c", code]).decode().strip()
    print(out)


def complete_auth(auth_code: str):
    ensure_colab_cli()
    if not STATE_FILE.exists():
        raise FileNotFoundError(f"Missing PKCE state file {STATE_FILE}. Run `--auth-url` first.")
    script = """
import json, sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
import colab_cli.auth as ca

state_file = Path.home() / ".gemini" / "colab_cli_pending_oauth.json"
st = json.loads(state_file.read_text())
flow = InstalledAppFlow.from_client_config(st["client_config"], st["scopes"], state=st["state"])
flow.redirect_uri = st["redirect_uri"]
flow.code_verifier = st["code_verifier"]
flow.fetch_token(code=sys.argv[1].strip())
creds_json = flow.credentials.to_json()
ca._save_token_to_keyring(creds_json)
# Also mirror to persistent ~/.gemini/colab_cli_token.json across ephemeral VMs
(Path.home() / ".gemini" / "colab_cli_token.json").write_text(creds_json)
state_file.unlink(missing_ok=True)
print("OAuth token saved to colab-cli keyring and ~/.gemini/colab_cli_token.json!")
"""
    subprocess.run([str(COLAB_PYTHON), "-c", script, auth_code], check=True)
    subprocess.run([str(COLAB_BIN), "sessions"], check=True)


def restore_persisted_token_if_needed():
    ensure_colab_cli()
    persisted = Path.home() / ".gemini" / "colab_cli_token.json"
    if persisted.exists():
        script = """
from pathlib import Path
import colab_cli.auth as ca
tok = (Path.home() / ".gemini" / "colab_cli_token.json").read_text()
if not ca._get_token_from_keyring():
    ca._save_token_to_keyring(tok)
"""
        subprocess.run([str(COLAB_PYTHON), "-c", script], check=True)


def check_status():
    restore_persisted_token_if_needed()
    subprocess.run([str(COLAB_BIN), "sessions"], check=False)
    subprocess.run([str(COLAB_BIN), "usage"], check=False)


def run_remote_gpu_render(session_name: str = "karmic-genie-s01e01"):
    restore_persisted_token_if_needed()
    # Try L4 first, fallback to T4
    res = subprocess.run([str(COLAB_BIN), "new", "-s", session_name, "--gpu", "L4"])
    if res.returncode != 0:
        print("L4 unavailable, falling back to T4 GPU...", flush=True)
        subprocess.run([str(COLAB_BIN), "new", "-s", session_name, "--gpu", "T4"], check=True)
    try:
        subprocess.run(
            [str(COLAB_BIN), "ssh", "-s", session_name, "--", "nvidia-smi | head -n 15"],
            check=False,
        )
        remote_script = REPO_DIR / "pipeline" / "build_s01e01_duty_first_epic_preview.py"
        if remote_script.exists():
            subprocess.run([str(COLAB_BIN), "exec", "-s", session_name, "-f", str(remote_script)], check=True)
    finally:
        subprocess.run([str(COLAB_BIN), "stop", "-s", session_name], check=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auth-url", action="store_true")
    ap.add_argument("--complete-auth", type=str, default=None)
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--render-gpu", action="store_true")
    args = ap.parse_args()

    if args.auth_url:
        generate_auth_url()
    elif args.complete_auth:
        complete_auth(args.complete_auth)
    elif args.status:
        check_status()
    elif args.render_gpu:
        run_remote_gpu_render()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
