#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Headless Google Colab NVIDIA L4 GPU Orchestrator (`google-colab-cli`)
for The Karmic Genie Show — Episode 1 (`S01E01`): "1. Respect Your DUTY First."

Implements the exact fast zero-`apt-get-update` Colab L4 workflow:
  1. Checks CCU balance before (`colab usage`) & verifies authentication (`--auth=adc` or `--auth=oauth2`
     persisted across VMs in `~/.gemini/colab_cli_token.json` / `~/.gemini/colab_cli_adc.json`).
  2. Allocates an NVIDIA L4 GPU VM (`colab new -s kg_l4 --gpu L4`, fallback `T4`).
  3. Streams episode workspace assets + Google Flow clip bundle directly onto `/content` (no slow `apt-get update`),
     installs `gTTS` + `pillow` via `colab install`, and runs the 6-worker `h264_nvenc -preset p5 -cq 18` render
     via `colab exec -s kg_l4 --timeout 900`.
  4. Pulls the rendered 1080p, 720p, and 360p MP4s back locally via `colab download`, uploads the 1080p Master
     to Google Drive (`1Mf-4vffVo6RRBhNFqTjzW3RAcC2bpbCy`) via `gdrive mutate upload`, and cleanly terminates
     the VM (`colab stop -s kg_l4`), reporting exact CCU burn (`0` active assignments).

Usage:
  # Local workstation (where ~/.config/colab-cli/adc.json or keyring already exists):
  python3 pipeline/run_on_colab_l4.py

  # Remote Antigravity VM one-time OAuth activation (saves permanently to /shared/user/.gemini/):
  python3 pipeline/run_on_colab_l4.py --auth-url
  python3 pipeline/run_on_colab_l4.py --complete-auth "<ONE_TIME_GOOGLE_AUTH_CODE>"
"""

import argparse
import json
import os
import subprocess
import sys
import tarfile
import time
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
COLAB_BIN = Path.home() / ".local" / "bin" / "colab"
COLAB_PY = Path.home() / ".local" / "share" / "uv" / "tools" / "google-colab-cli" / "bin" / "python"

PERSIST_DIR = Path.home() / ".gemini"  # Symlinked to /shared/user/.gemini across remote VMs
PENDING_OAUTH = PERSIST_DIR / "colab_cli_pending_oauth.json"
PERSIST_OAUTH_TOKEN = PERSIST_DIR / "colab_cli_token.json"
PERSIST_ADC_JSON = PERSIST_DIR / "colab_cli_adc.json"
LOCAL_ADC_PATHS = [
    Path.home() / ".config" / "colab-cli" / "adc.json",
    Path.home() / ".config" / "gcloud" / "application_default_credentials.json",
    PERSIST_ADC_JSON,
]

DRIVE_FOLDER_S01E01 = "1Mf-4vffVo6RRBhNFqTjzW3RAcC2bpbCy"
DRIVE_FLOW_BUNDLE_ID = "1jS-WnEMfHltOHQLEU-91aRkqil4mPXtJ"
DRIVE_PILOT_SRC_ID = "1WwEcJnNcrhvVEs4z46PrOGboJJHXkWRA"


def ensure_colab_cli():
    if not COLAB_BIN.exists() or not COLAB_PY.exists():
        subprocess.run(["uv", "tool", "install", "--with", "keyrings.alt", "google-colab-cli"], check=True)


def detect_auth_args() -> tuple[list[str], dict[str, str]]:
    """Auto-detect ADC (`adc.json`) vs persisted OAuth2 keyring token across local & remote VMs."""
    ensure_colab_cli()
    env = os.environ.copy()

    # 1. Check ADC files first (local ~/.config/colab-cli/adc.json or persisted ~/.gemini/colab_cli_adc.json)
    for adc_p in LOCAL_ADC_PATHS:
        if adc_p.exists() and adc_p.stat().st_size > 50:
            env["GOOGLE_APPLICATION_CREDENTIALS"] = str(adc_p)
            return ["--auth=adc"], env

    # 2. Restore persisted OAuth2 token into colab-cli keyring if present in /shared/user/.gemini
    if PERSIST_OAUTH_TOKEN.exists():
        restore_code = (
            "from pathlib import Path\n"
            "import colab_cli.auth as ca\n"
            f"tok = Path({str(PERSIST_OAUTH_TOKEN)!r}).read_text()\n"
            "if not ca._get_token_from_keyring():\n"
            "    ca._save_token_to_keyring(tok)\n"
        )
        subprocess.run([str(COLAB_PY), "-c", restore_code], check=True)
        return ["--auth=oauth2"], env

    return ["--auth=oauth2"], env


def generate_auth_url():
    ensure_colab_cli()
    code = f"""
import json
from importlib import resources
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
import colab_cli.auth as ca

cfg = json.loads(resources.files("colab_cli").joinpath("oauth_config.json").read_text())
flow = InstalledAppFlow.from_client_config(cfg, ca.PUBLIC_SCOPES)
flow.redirect_uri = ca.REMOTE_REDIRECT_URI
auth_url, state = flow.authorization_url(prompt="consent", token_usage="remote", access_type="offline")

st_path = Path({str(PENDING_OAUTH)!r})
st_path.parent.mkdir(parents=True, exist_ok=True)
st_path.write_text(json.dumps({{
    "client_config": cfg,
    "scopes": ca.PUBLIC_SCOPES,
    "redirect_uri": ca.REMOTE_REDIRECT_URI,
    "code_verifier": flow.code_verifier,
    "state": state,
    "auth_url": auth_url,
}}, indent=2))
print(auth_url)
"""
    print(subprocess.check_output([str(COLAB_PY), "-c", code]).decode().strip())


def complete_auth(auth_code: str):
    ensure_colab_cli()
    if not PENDING_OAUTH.exists():
        raise FileNotFoundError(f"No pending PKCE state at {PENDING_OAUTH}. Run --auth-url first.")
    script = f"""
import json, sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
import colab_cli.auth as ca

st_path = Path({str(PENDING_OAUTH)!r})
st = json.loads(st_path.read_text())
flow = InstalledAppFlow.from_client_config(st["client_config"], st["scopes"], state=st["state"])
flow.redirect_uri = st["redirect_uri"]
flow.code_verifier = st["code_verifier"]
flow.fetch_token(code=sys.argv[1].strip())
creds_json = flow.credentials.to_json()
ca._save_token_to_keyring(creds_json)
Path({str(PERSIST_OAUTH_TOKEN)!r}).write_text(creds_json)
st_path.unlink(missing_ok=True)
print("✅ Saved Colab CLI credentials permanently to keyring + ~/.gemini/colab_cli_token.json")
"""
    subprocess.run([str(COLAB_PY), "-c", script, auth_code], check=True)
    auth_flags, env = detect_auth_args()
    subprocess.run([str(COLAB_BIN), *auth_flags, "usage"], env=env, check=True)


def build_lightweight_workspace_tar(tar_out: Path):
    """Packs only the Episode 1 ledger, overlays, storyboard plates, theme WAV, opener MP4, and builder script."""
    include_rels = [
        "pipeline/build_s01e01_duty_first_epic_preview.py",
        "episodes/S01E01_Respect_Your_Duty_First/s01e01_48_shot_flow_ledger.json",
        "episodes/S01E01_Respect_Your_Duty_First/overlays",
        "docs/assets/storyboard/s01e01_duty_first",
        "assets/theme/official_karmic_genie_7d_theme_song.wav",
        "assets/logo/official_karmic_genie_show_logo.jpg",
        "renders/Karmic_Genie_Show_Official_7D_Theme_Opener_16x9.mp4",
    ]
    with tarfile.open(tar_out, "w:gz") as tf:
        for rel in include_rels:
            p = REPO_DIR / rel
            if p.exists():
                tf.add(p, arcname=rel)


def run_colab_l4_render(session: str = "kg_l4", upload_drive: bool = True):
    auth_flags, env = detect_auth_args()

    def colab(*args, check: bool = True):
        return subprocess.run([str(COLAB_BIN), *auth_flags, *args], env=env, check=check)

    print("📊 Checking Colab Compute Unit balance before L4 allocation...", flush=True)
    colab("usage")

    print(f"🚀 Allocating Google Colab NVIDIA L4 GPU session `{session}`...", flush=True)
    res = colab("new", "-s", session, "--gpu", "L4", check=False)
    if res.returncode != 0:
        print("⚠️ L4 unavailable on current tier/pool; falling back to T4 GPU...", flush=True)
        colab("new", "-s", session, "--gpu", "T4", check=True)

    t0 = time.time()
    try:
        # 1. Stage local workspace + Google Flow clip bundle
        ws_tar = Path("/tmp/kg_s01e01_colab_ws.tar.gz")
        flow_tar = Path("/tmp/karmic_genie_7d_colab_bundle.tar.gz")
        build_lightweight_workspace_tar(ws_tar)

        if not flow_tar.exists():
            subprocess.run(
                ["gdrive", "readonly", "download", DRIVE_FLOW_BUNDLE_ID, "--out", str(flow_tar)],
                check=True,
            )

        print("📦 Streaming workspace & Google Flow clip bundle directly to /content (zero apt-get update)...", flush=True)
        colab("upload", "-s", session, str(ws_tar), "/content/kg_s01e01_colab_ws.tar.gz")
        colab("upload", "-s", session, str(flow_tar), "/content/karmic_genie_7d_colab_bundle.tar.gz")

        print("⚡ Installing gTTS & Pillow via uv on Colab L4...", flush=True)
        colab("install", "-s", session, "gTTS", "pillow")

        remote_driver = Path("/tmp/remote_kg_l4_driver.py")
        remote_driver.write_text(
            """import os, subprocess, time
from pathlib import Path

print("=== Colab GPU Hardware Check ===", flush=True)
subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"], check=False)
print("vCPUs:", os.cpu_count(), flush=True)

Path("/content/Karmic-Genie-Show").mkdir(parents=True, exist_ok=True)
Path("/tmp/flow_bundle").mkdir(parents=True, exist_ok=True)
subprocess.run(["tar", "-xzf", "/content/kg_s01e01_colab_ws.tar.gz", "-C", "/content/Karmic-Genie-Show"], check=True)
subprocess.run(["tar", "-xzf", "/content/karmic_genie_7d_colab_bundle.tar.gz", "-C", "/tmp/flow_bundle"], check=True)

t_start = time.time()
subprocess.run(
    ["python3", "/content/Karmic-Genie-Show/pipeline/build_s01e01_duty_first_epic_preview.py"],
    cwd="/content/Karmic-Genie-Show",
    check=True,
)
print(f"=== L4 NVENC Render Completed in {time.time() - t_start:.1f}s ===", flush=True)
""",
            encoding="utf-8",
        )

        print("🎬 Launching 6-worker `h264_nvenc -preset p5 -cq 18` render on Colab L4 (`--timeout 900`)...", flush=True)
        colab("exec", "-s", session, "--timeout", "900", "-f", str(remote_driver))

        # Pull back rendered outputs locally
        out_1080 = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_Master_16x9.mp4"
        out_720 = REPO_DIR / "docs" / "assets" / "videos" / "Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_Master_16x9.mp4"
        out_360 = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E01_Respect_Your_Duty_First_360p.mp4"
        out_1080.parent.mkdir(parents=True, exist_ok=True)
        out_720.parent.mkdir(parents=True, exist_ok=True)

        print("⬇️ Pulling rendered 1080p, 720p & 360p MP4s back from Colab L4...", flush=True)
        colab("download", "-s", session, f"/content/Karmic-Genie-Show/renders/{out_1080.name}", str(out_1080))
        colab("download", "-s", session, f"/content/Karmic-Genie-Show/docs/assets/videos/{out_720.name}", str(out_720))
        colab("download", "-s", session, f"/content/Karmic-Genie-Show/renders/{out_360.name}", str(out_360))

        if upload_drive:
            print(f"☁️ Uploading {out_1080.name} to Google Drive ({DRIVE_FOLDER_S01E01})...", flush=True)
            subprocess.run(
                ["gdrive", "mutate", "upload", str(out_1080), "--parent", DRIVE_FOLDER_S01E01],
                check=True,
            )
    finally:
        print(f"🛑 Stopping Colab GPU session `{session}` cleanly...", flush=True)
        colab("stop", "-s", session, check=False)
        colab("sessions", check=False)
        colab("usage", check=False)
        print(f"⏱️ Total End-to-End Colab L4 Wall Time: {time.time() - t0:.1f}s", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auth-url", action="store_true", help="Print one-time PKCE auth URL for remote VM setup")
    ap.add_argument("--complete-auth", type=str, default=None, help="Exchange one-time auth code & persist token")
    ap.add_argument("--session", type=str, default="kg_l4", help="Colab CLI session name")
    ap.add_argument("--no-drive-upload", action="store_true", help="Skip Google Drive upload after pulling MP4")
    args = ap.parse_args()

    if args.auth_url:
        generate_auth_url()
    elif args.complete_auth:
        complete_auth(args.complete_auth)
    else:
        run_colab_l4_render(session=args.session, upload_drive=not args.no_drive_upload)


if __name__ == "__main__":
    main()
