#!/usr/bin/env python3
"""
Step 5: Google Colab GPU Cloud Remotion Renderer for The Karmic Genie Show episodes:
- Snapshots pre-existing Colab sessions (never touches them).
- Provisions a fresh GPU session (`l4` -> `t4 --high-mem` fallback).
- Installs Chromium runtime libraries & Latin/Noto fonts in dedicated apt-get calls.
- Transfers a lean bundle (<= 35 MB chunked if needed) containing src/, package*.json,
  tsconfig.json, public/assets/<asset_subdir>/, public/audio/<ep_slug>.mp3,
  episodes/ep01_ai_brain_trap/pilot_manifest.json, and episodes/karmic_genie/<ep_slug>/manifest.json.
- Renders proof stills first for Visual QA (`--action setup_and_proof`), launches detached
  nohup 1080p30 render (`--action start_render`), checks/downloads (`--action check_or_download`),
  or runs full streaming render (`--action render_and_download`), with immediate `colab stop`.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

COLAB_BIN = "/home/shishyan/GuruKulaDesam_Local/.venv/bin/colab"
STUDIO_ROOT = Path("/home/shishyan/GitHub/Influenzian/Utility_Explainer_Studio")

ERROR_MARKERS = (
    "Traceback (most recent call last)",
    "CalledProcessError",
    "AssertionError",
    "FATAL:",
    "RuntimeError:",
)


def run_local(cmd: str, check: bool = True, retries: int = 3, timeout_s: int = 240) -> subprocess.CompletedProcess:
    actual = f"timeout -k 5 {timeout_s} bash -c {shlex.quote(cmd)}"
    print(f"[Local] {cmd}", flush=True)
    for attempt in range(1, retries + 1):
        proc = subprocess.Popen(
            actual,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            start_new_session=True,
        )
        captured = []
        lost_conn = False
        for ln in iter(proc.stdout.readline, ""):
            sys.stdout.write(ln)
            sys.stdout.flush()
            captured.append(ln)
            if "RuntimeError: Connection was lost." in ln:
                lost_conn = True
                try:
                    import signal
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except Exception:
                    proc.kill()
                break
        proc.wait()
        out = "".join(captured)
        if not lost_conn and proc.returncode == 0:
            if check and " exec " in cmd and any(m in out for m in ERROR_MARKERS):
                raise RuntimeError(f"Remote Colab step reported error: {cmd}")
            return subprocess.CompletedProcess(actual, proc.returncode, out, "")
        if attempt < retries:
            print(f"[Retry {attempt}/{retries}] rc={proc.returncode} lost_conn={lost_conn}, sleeping 5s...", flush=True)
            time.sleep(5)
        elif check:
            raise RuntimeError(f"Command failed rc={proc.returncode}: {cmd}")
        else:
            return subprocess.CompletedProcess(actual, proc.returncode, out, "")
    raise RuntimeError("Unreachable")


def list_active_sessions() -> set[str]:
    out = subprocess.check_output(f"{COLAB_BIN} sessions", shell=True, text=True)
    ids: set[str] = set()
    for line in out.splitlines():
        m = re.match(r"^\s*\[([A-Za-z0-9_-]+)\]", line)
        if m:
            ids.add(m.group(1))
        else:
            parts = line.strip().split()
            if parts and len(parts[0]) >= 5 and parts[0].replace("-", "").replace("_", "").isalnum():
                if parts[0].lower() not in ("session", "sessions", "active", "none"):
                    ids.add(parts[0])
    return ids


def provision_safe_session(session_name: str, state_dir: Path, protected_file: Path, session_file: Path) -> str:
    existing = list_active_sessions()
    state_dir.mkdir(parents=True, exist_ok=True)
    protected_file.write_text(json.dumps(sorted(existing), indent=2), encoding="utf-8")
    print(f"[Colab] Pre-existing sessions (DO NOT TOUCH): {sorted(existing) or '<none>'}", flush=True)

    env = os.environ.copy()
    env["COLAB_CLI_ASSIGN_RETRIES"] = "1"
    env["COLAB_CLI_RETRY_BACKOFF"] = "5"

    candidates = (
        f"{COLAB_BIN} new -s {session_name} --gpu l4",
        f"{COLAB_BIN} new -s {session_name} --gpu t4 --high-mem",
        f"{COLAB_BIN} new -s {session_name} --gpu t4",
        f"{COLAB_BIN} new -s {session_name} --gpu a100",
    )
    ping_py = Path(f"/tmp/{session_name}_ping.py")
    ping_py.write_text('print("PING_OK", flush=True)\n', encoding="utf-8")

    for gpu_cmd in candidates:
        print(f"[Colab] Provisioning: {gpu_cmd}", flush=True)
        res = subprocess.run(f"timeout -k 5 240 {gpu_cmd}", shell=True, capture_output=True, text=True, env=env)
        combined = (res.stdout or "") + "\n" + (res.stderr or "")
        if combined.strip():
            print(combined.strip(), flush=True)
        if res.returncode == 0 and session_name not in existing:
            diff = {session_name}
        else:
            diff = set()
        for sid in sorted(diff):
            assert sid not in existing
            ping = subprocess.run(
                f"timeout -k 5 75 {COLAB_BIN} exec -s {sid} -f '{ping_py}' --timeout 60",
                shell=True,
                capture_output=True,
                text=True,
            )
            if ping.returncode == 0 and "PING_OK" in ((ping.stdout or "") + (ping.stderr or "")):
                print(f"[Colab] Session {sid} healthy (PING_OK)!", flush=True)
                session_file.write_text(sid, encoding="utf-8")
                return sid
            subprocess.run(f"timeout -k 5 60 {COLAB_BIN} stop -s {sid}", shell=True, check=False)
    raise RuntimeError("COLAB_PROVISION_FAILED: Unable to allocate L4/T4/A100 GPU session.")


def assert_safe_stop(sid: str, protected_file: Path, session_file: Path) -> None:
    protected = set(json.loads(protected_file.read_text(encoding="utf-8"))) if protected_file.exists() else set()
    if sid in protected:
        raise RuntimeError(f"SAFETY ABORT: {sid} is protected!")
    run_local(f"{COLAB_BIN} stop -s {sid}", check=False, retries=2, timeout_s=90)
    if session_file.exists():
        session_file.unlink()


def build_lean_bundle(ep_slug: str, asset_subdir: str, ep_rel: Path, ep_dir: Path) -> Path:
    stage = Path(f"/tmp/{ep_slug}_studio_stage")
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    for rel in ("package.json", "package-lock.json", "tsconfig.json"):
        shutil.copy2(STUDIO_ROOT / rel, stage / rel)
    shutil.copytree(STUDIO_ROOT / "src", stage / "src")
    (stage / "public" / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copytree(STUDIO_ROOT / "public" / "assets" / asset_subdir, stage / "public" / "assets" / asset_subdir)
    (stage / "public" / "audio").mkdir(parents=True, exist_ok=True)
    shutil.copy2(STUDIO_ROOT / "public" / "audio" / f"{ep_slug}.mp3", stage / "public" / "audio" / f"{ep_slug}.mp3")

    ep_stage = stage / ep_rel
    ep_stage.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ep_dir / "manifest.json", ep_stage / "manifest.json")

    ep01_rel = Path("episodes/ep01_ai_brain_trap/pilot_manifest.json")
    (stage / ep01_rel.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(STUDIO_ROOT / ep01_rel, stage / ep01_rel)

    mf = json.loads((ep_dir / "manifest.json").read_text(encoding="utf-8"))
    if mf.get("needsWhisperFallback"):
        shutil.copytree(ep_dir / "beat_audio", ep_stage / "beat_audio")

    tar_path = Path(f"/tmp/{ep_slug}_bundle.tar.gz")
    run_local(f"tar -C '{stage}' -czf '{tar_path}' .", timeout_s=180)
    print(f"[Bundle] {tar_path} ({tar_path.stat().st_size / (1024*1024):.2f} MB)", flush=True)
    return tar_path


def upload_chunked(sid: str, local_file: Path, remote_file: str, chunk_mb: int = 35) -> None:
    sz_mb = local_file.stat().st_size / (1024 * 1024)
    if sz_mb <= chunk_mb:
        run_local(f"{COLAB_BIN} upload -s {sid} '{local_file}' '{remote_file}'", retries=3, timeout_s=180)
        time.sleep(3)
        return
    prefix = "/tmp/kg_up_"
    for old in glob.glob(prefix + "*"):
        os.remove(old)
    run_local(f"split -b {chunk_mb}m -d -a 3 '{local_file}' {prefix}", timeout_s=60)
    parts = sorted(glob.glob(prefix + "*"))
    remote_parts = []
    for i, part in enumerate(parts):
        rp = f"/content/kg_up_{i:03d}"
        run_local(f"{COLAB_BIN} upload -s {sid} '{part}' '{rp}'", retries=3, timeout_s=180)
        remote_parts.append(rp)
    time.sleep(3)
    join_py = Path("/tmp/kg_join.py")
    join_py.write_text(
        f"""
import os
with open("{remote_file}", "wb") as out:
    for rp in {remote_parts!r}:
        with open(rp, "rb") as f: out.write(f.read())
        os.remove(rp)
assert os.path.getsize("{remote_file}") == {local_file.stat().st_size}
print("JOIN_OK", os.path.getsize("{remote_file}"), flush=True)
""",
        encoding="utf-8",
    )
    run_local(f"{COLAB_BIN} exec -s {sid} -f '{join_py}' --timeout 240", timeout_s=260)


def download_chunked(sid: str, remote_path: str, local_path: Path, chunk_mb: int = 40) -> None:
    sp = Path("/tmp/kg_split.py")
    sp.write_text(
        f"""
import glob, hashlib, os, subprocess
src = "{remote_path}"
assert os.path.exists(src), f"Missing {{src}}"
sz = os.path.getsize(src)
h = hashlib.md5()
with open(src, "rb") as f:
    for blk in iter(lambda: f.read(1 << 20), b""): h.update(blk)
for old in glob.glob("/content/kg_dl_*"): os.remove(old)
subprocess.run(f"split -b {chunk_mb}m -d -a 3 '{{src}}' /content/kg_dl_", shell=True, check=True)
parts = sorted(glob.glob("/content/kg_dl_*"))
print(f"SPLIT_META:{{sz}}:{{h.hexdigest()}}:{{','.join(parts)}}", flush=True)
""",
        encoding="utf-8",
    )
    res = run_local(f"{COLAB_BIN} exec -s {sid} -f '{sp}' --timeout 180", retries=3, timeout_s=200)
    meta = [ln for ln in res.stdout.splitlines() if "SPLIT_META:" in ln][-1]
    _, sz_s, exp_md5, parts_csv = meta.split(":", 3)
    exp_sz = int(sz_s)
    remote_parts = [p.strip() for p in parts_csv.split(",") if p.strip()]

    tmp_dir = Path("/tmp/kg_dl_parts")
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True)
    h_loc = hashlib.md5()
    local_path.parent.mkdir(parents=True, exist_ok=True)
    with open(local_path, "wb") as out_f:
        for i, rp in enumerate(remote_parts):
            lp = tmp_dir / f"part_{i:03d}"
            run_local(f"{COLAB_BIN} download -s {sid} '{rp}' '{lp}'", retries=3, timeout_s=150)
            data = lp.read_bytes()
            h_loc.update(data)
            out_f.write(data)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    assert local_path.stat().st_size == exp_sz and h_loc.hexdigest() == exp_md5
    print(f"[Download Verified] {local_path} ({exp_sz:,} B, MD5={exp_md5})", flush=True)


def make_setup_remote_py(remote_tar: str) -> str:
    return f"""
import os, select, subprocess, sys, time

def srun(cmd, label):
    print(f"--> {{label}}", flush=True)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    t0 = time.time()
    while True:
        ready, _, _ = select.select([proc.stdout], [], [], 8.0)
        if ready:
            ln = proc.stdout.readline()
            if ln:
                print(ln, end="", flush=True)
            elif proc.poll() is not None:
                break
        else:
            if proc.poll() is not None:
                break
            print(f"[setup heartbeat {{int(time.time() - t0)}}s] {{label}}...", flush=True)
    rc = proc.wait()
    if rc != 0:
        print(f"FATAL: {{label}} rc={{rc}}", flush=True)
        sys.exit(rc)

subprocess.run("killall -9 apt-get apt dpkg 2>/dev/null || true; dpkg --configure -a 2>/dev/null || true", shell=True)
srun("apt-get -o Acquire::ForceIPv4=true -o Acquire::http::Timeout=15 update -qq || true", "apt-get update")
srun("DEBIAN_FRONTEND=noninteractive apt-get -o Acquire::ForceIPv4=true install -y -qq --no-install-recommends fonts-noto-core fonts-dejavu-core fonts-liberation fontconfig", "install fonts")
srun("fc-cache -f", "fc-cache")
srun("DEBIAN_FRONTEND=noninteractive apt-get -o Acquire::ForceIPv4=true install -y -qq --no-install-recommends libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpangocairo-1.0-0 libxshmfence1 libasound2t64 ffmpeg", "install chromium libs + ffmpeg")

os.makedirs("/content/Utility_Explainer_Studio", exist_ok=True)
srun("tar -xzf {remote_tar} -C /content/Utility_Explainer_Studio", "extract bundle")
srun("cd /content/Utility_Explainer_Studio && npm ci --prefer-offline --no-audit --no-fund || npm install --no-audit --no-fund", "npm install")
print("REMOTE_ENV_READY", flush=True)
"""


def select_proof_frames(beats: list[dict]) -> list[tuple[str, int]]:
    def mid_frame(b: dict) -> int:
        return int(round((b["startSec"] + min(2.2, b["durationSec"] * 0.45)) * 30))

    with_widgets = [b for b in beats if b.get("overlayWidget") and b.get("overlayWidget") != "OUTRO_CARD"]
    outro = next((b for b in beats if b.get("overlayWidget") == "OUTRO_CARD"), beats[-1])
    picks: list[tuple[str, int]] = []
    if len(with_widgets) >= 2:
        picks.append((f"proof_{with_widgets[0]['id'].lower()}", mid_frame(with_widgets[0])))
        mid_w = with_widgets[len(with_widgets) // 2]
        picks.append((f"proof_{mid_w['id'].lower()}", mid_frame(mid_w)))
    else:
        picks.append(("proof_open", mid_frame(beats[0])))
        picks.append(("proof_mid", mid_frame(beats[len(beats) // 2])))
    picks.append(("proof_outro", int(round((outro["startSec"] + min(2.0, outro["durationSec"] * 0.5)) * 30))))
    return picks


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep-slug", default="KG_Ep03_Infinite_Distractions")
    ap.add_argument("--asset-subdir", default="kg_ep03_distractions")
    ap.add_argument("--session-name", default="kgep03")
    ap.add_argument("--session", default="")
    ap.add_argument("--remote-mp4", default="")
    ap.add_argument("--local-mp4", default="")
    ap.add_argument("--keep-alive", action="store_true", help="Keep warm Colab GPU session alive for next episode")
    ap.add_argument(
        "--action",
        choices=["setup_and_proof", "start_render", "check_or_download", "render_and_download", "push_assets_and_render", "download_only", "stop"],
        required=True,
    )
    args = ap.parse_args()

    ep_slug = args.ep_slug
    asset_subdir = args.asset_subdir
    ep_rel = Path(f"episodes/karmic_genie/{ep_slug}")
    ep_dir = STUDIO_ROOT / ep_rel
    state_dir = ep_dir / "_colab_state"
    session_file = state_dir / "active_session.txt"
    protected_file = state_dir / "protected_sessions.json"

    remote_tar = f"/content/{ep_slug}_bundle.tar.gz"
    remote_mp4 = args.remote_mp4 or f"/content/{ep_slug}_1080p.mp4"
    local_mp4 = Path(args.local_mp4) if args.local_mp4 else (ep_dir / f"{ep_slug}_1080p.mp4")

    if args.action == "download_only":
        sid = args.session or session_file.read_text(encoding="utf-8").strip()
        download_chunked(sid, remote_mp4, local_mp4)
        return

    if args.action == "stop":
        sid = args.session or session_file.read_text(encoding="utf-8").strip()
        assert_safe_stop(sid, protected_file, session_file)
        return

    if args.action == "setup_and_proof":
        sid = args.session or provision_safe_session(args.session_name, state_dir, protected_file, session_file)
        if not args.session:
            bundle = build_lean_bundle(ep_slug, asset_subdir, ep_rel, ep_dir)
            upload_chunked(sid, bundle, remote_tar)
            time.sleep(3)

        setup_py = Path(f"/tmp/{ep_slug}_setup.py")
        setup_py.write_text(make_setup_remote_py(remote_tar), encoding="utf-8")
        run_local(f"{COLAB_BIN} exec -s {sid} -f '{setup_py}' --timeout 900", timeout_s=920)

        mf = json.loads((ep_dir / "manifest.json").read_text(encoding="utf-8"))
        proof_frames = select_proof_frames(mf["beats"])
        proof_py = Path(f"/tmp/{ep_slug}_proof.py")
        proof_py.write_text(
            f"""
import json, subprocess
from pathlib import Path
root = Path("/content/Utility_Explainer_Studio")
mf_path = root / "{ep_rel}" / "manifest.json"
mf = json.loads(mf_path.read_text(encoding="utf-8"))
props_path = Path("/content/{ep_slug}_props.json")
props_path.write_text(json.dumps({{"data": mf}}), encoding="utf-8")
for tag, fnum in {proof_frames!r}:
    out_png = f"/content/{{tag}}.png"
    subprocess.run(
        [
            "./node_modules/.bin/remotion", "still", "src/index.tsx",
            "KarmicGenie-ColorfulCreator-16x9", out_png,
            f"--props={{props_path}}", f"--frame={{fnum}}", "--gl=angle",
        ],
        cwd=str(root), check=True,
    )
    print("PROOF_OK:", out_png, flush=True)
""",
            encoding="utf-8",
        )
        run_local(f"{COLAB_BIN} exec -s {sid} -f '{proof_py}' --timeout 420", timeout_s=440)
        proofs_dir = ep_dir / "proofs"
        proofs_dir.mkdir(parents=True, exist_ok=True)
        for tag, _ in proof_frames:
            run_local(f"{COLAB_BIN} download -s {sid} '/content/{tag}.png' '{proofs_dir / f'{tag}.png'}'", timeout_s=120)
        print(f"[DONE setup_and_proof] Session={sid} | Proofs saved in {proofs_dir}", flush=True)

    elif args.action == "start_render":
        sid = args.session or session_file.read_text(encoding="utf-8").strip()
        run_local(
            f"{COLAB_BIN} upload -s {sid} '{ep_dir / 'manifest.json'}' '/content/{ep_slug}_manifest.json'",
            retries=3,
            timeout_s=90,
        )
        run_local(
            f"{COLAB_BIN} upload -s {sid} '{STUDIO_ROOT / 'src' / 'KarmicGenieCreatorStage.tsx'}' '/content/KarmicGenieCreatorStage.tsx'",
            retries=3,
            timeout_s=90,
        )
        time.sleep(3)

        launch_py = Path(f"/tmp/{ep_slug}_launch.py")
        launch_py.write_text(
            f"""
import json, os, shutil, subprocess
from pathlib import Path

root = Path("/content/Utility_Explainer_Studio")
shutil.copy2("/content/{ep_slug}_manifest.json", root / "{ep_rel}" / "manifest.json")
shutil.copy2("/content/KarmicGenieCreatorStage.tsx", root / "src" / "KarmicGenieCreatorStage.tsx")
mf = json.loads((root / "{ep_rel}" / "manifest.json").read_text(encoding="utf-8"))
props_path = Path("/content/{ep_slug}_props.json")
props_path.write_text(json.dumps({{"data": mf}}), encoding="utf-8")
cores = min(10, max(6, os.cpu_count() or 8))
runner_sh = Path("/content/run_{ep_slug}.sh")
runner_sh.write_text(
    "#!/usr/bin/env bash\\n"
    "set -euo pipefail\\n"
    "cd /content/Utility_Explainer_Studio\\n"
    f"./node_modules/.bin/remotion render src/index.tsx KarmicGenie-ColorfulCreator-16x9 '{remote_mp4}' "
    f"--props='{{props_path}}' --gl=angle --concurrency={{cores}} --codec=h264 --crf=18 --audio-bitrate=256k\\n"
    f"ffprobe -v error -show_entries format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate -of json '{remote_mp4}' > /content/{ep_slug}_probe.json\\n"
    "echo RENDER_COMPLETE_SENTINEL\\n",
    encoding="utf-8",
)
os.chmod(runner_sh, 0o755)
pid = subprocess.check_output(
    f"nohup /content/run_{ep_slug}.sh < /dev/null > /content/{ep_slug}_render.log 2>&1 & echo $!",
    shell=True,
    text=True,
).strip()
print(f"RENDER_LAUNCHED pid={{pid}} cores={{cores}} dur={{mf['totalDurationSec']}}s", flush=True)
""",
            encoding="utf-8",
        )
        run_local(f"{COLAB_BIN} exec -s {sid} -f '{launch_py}' --timeout 60", timeout_s=80)

    elif args.action == "check_or_download":
        sid = args.session or session_file.read_text(encoding="utf-8").strip()
        chk_py = Path(f"/tmp/{ep_slug}_chk.py")
        chk_py.write_text(
            f"""
import os
from pathlib import Path
log_p = Path("/content/{ep_slug}_render.log")
txt = log_p.read_text(encoding="utf-8", errors="replace") if log_p.exists() else ""
lines = [ln for ln in txt.splitlines() if ln.strip()]
for bad in ("status: 404", "HTTP 404", "Failed to fetch", "Error:"):
    if bad in txt:
        print("RENDER_ERROR_FOUND:", bad, flush=True)
        print("\\n".join(lines[-25:]), flush=True)
        raise SystemExit(1)
if "RENDER_COMPLETE_SENTINEL" in txt and os.path.exists("{remote_mp4}"):
    print("STATUS:COMPLETE", os.path.getsize("{remote_mp4}"), flush=True)
else:
    prog = [ln for ln in lines if "Rendered " in ln or "Encoded " in ln or "Stitching" in ln]
    print("STATUS:RUNNING", prog[-1] if prog else (lines[-1] if lines else "initializing"), flush=True)
""",
            encoding="utf-8",
        )
        res = run_local(f"{COLAB_BIN} exec -s {sid} -f '{chk_py}' --timeout 60", timeout_s=80)
        if "STATUS:COMPLETE" in res.stdout:
            download_chunked(sid, remote_mp4, local_mp4)
            assert_safe_stop(sid, protected_file, session_file)
            print(f"[ALL RENDERED & CLEANED] {local_mp4}", flush=True)

    elif args.action == "render_and_download":
        sid = args.session or session_file.read_text(encoding="utf-8").strip()
        run_local(
            f"{COLAB_BIN} upload -s {sid} '{ep_dir / 'manifest.json'}' '/content/{ep_slug}_manifest.json'",
            retries=3,
            timeout_s=90,
        )
        run_local(
            f"{COLAB_BIN} upload -s {sid} '{STUDIO_ROOT / 'src' / 'KarmicGenieCreatorStage.tsx'}' '/content/KarmicGenieCreatorStage.tsx'",
            retries=3,
            timeout_s=90,
        )
        time.sleep(3)

        render_py = Path(f"/tmp/{ep_slug}_render.py")
        render_py.write_text(
            f"""
import json, os, select, shutil, subprocess, sys, time
from pathlib import Path

root = Path("/content/Utility_Explainer_Studio")
shutil.copy2("/content/{ep_slug}_manifest.json", root / "{ep_rel}" / "manifest.json")
shutil.copy2("/content/KarmicGenieCreatorStage.tsx", root / "src" / "KarmicGenieCreatorStage.tsx")
mf = json.loads((root / "{ep_rel}" / "manifest.json").read_text(encoding="utf-8"))
props_path = Path("/content/{ep_slug}_props.json")
props_path.write_text(json.dumps({{"data": mf}}), encoding="utf-8")
out_mp4 = "{remote_mp4}"
cores = min(10, max(6, os.cpu_count() or 8))
log_path = "/content/{ep_slug}_render.log"
cmd = (
    f"cd /content/Utility_Explainer_Studio && "
    f"./node_modules/.bin/remotion render src/index.tsx KarmicGenie-ColorfulCreator-16x9 {{out_mp4}} "
    f"--props={{props_path}} --gl=angle --concurrency={{cores}} --codec=h264 --crf=18 --audio-bitrate=256k"
)
print(f"[Render Start] cores={{cores}} dur={{mf['totalDurationSec']}}s", flush=True)
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
t0 = time.time()
tail = []
with open(log_path, "w", encoding="utf-8") as lf:
    while True:
        ready, _, _ = select.select([proc.stdout], [], [], 9.0)
        if ready:
            ln = proc.stdout.readline()
            if ln:
                lf.write(ln)
                lf.flush()
                tail.append(ln.rstrip())
                if len(tail) > 30: tail.pop(0)
                if "Rendered " in ln or "Encoded " in ln or "Error" in ln or "Failed" in ln:
                    print(ln, end="", flush=True)
            elif proc.poll() is not None:
                break
        else:
            if proc.poll() is not None:
                break
            print(f"[render heartbeat {{int(time.time() - t0)}}s]", flush=True)
rc = proc.wait()
if rc != 0:
    print("FATAL: Render failed rc=", rc, flush=True)
    print("\\n".join(tail[-20:]), flush=True)
    sys.exit(rc)

probe = subprocess.check_output(
    f"ffprobe -v error -show_entries format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate -of json {{out_mp4}}",
    shell=True, text=True,
)
print("FFPROBE_OK:", probe, flush=True)
print("RENDER_COMPLETE", flush=True)
""",
            encoding="utf-8",
        )
        run_local(f"{COLAB_BIN} exec -s {sid} -f '{render_py}' --timeout 0", retries=3, timeout_s=7200)
        download_chunked(sid, remote_mp4, local_mp4)
        if not args.keep_alive:
            assert_safe_stop(sid, protected_file, session_file)
            print(f"[ALL RENDERED & CLEANED] {local_mp4}", flush=True)
        else:
            print(f"[RENDERED — WARM SESSION {sid} KEPT ALIVE] {local_mp4}", flush=True)

    elif args.action == "push_assets_and_render":
        sid = args.session
        assert sid, "--session is required for push_assets_and_render"
        delta_stage = Path(f"/tmp/{ep_slug}_delta_stage")
        if delta_stage.exists():
            shutil.rmtree(delta_stage)
        (delta_stage / "public" / "assets").mkdir(parents=True, exist_ok=True)
        shutil.copytree(STUDIO_ROOT / "public" / "assets" / asset_subdir, delta_stage / "public" / "assets" / asset_subdir)
        (delta_stage / "public" / "audio").mkdir(parents=True, exist_ok=True)
        shutil.copy2(STUDIO_ROOT / "public" / "audio" / f"{ep_slug}.mp3", delta_stage / "public" / "audio" / f"{ep_slug}.mp3")
        (delta_stage / ep_rel).mkdir(parents=True, exist_ok=True)
        shutil.copy2(ep_dir / "manifest.json", delta_stage / ep_rel / "manifest.json")
        shutil.copytree(STUDIO_ROOT / "src", delta_stage / "src")
        delta_tar = Path(f"/tmp/{ep_slug}_delta.tar.gz")
        run_local(f"tar -C '{delta_stage}' -czf '{delta_tar}' .", timeout_s=90)
        upload_chunked(sid, delta_tar, f"/content/{ep_slug}_delta.tar.gz")
        time.sleep(4)

        mf = json.loads((ep_dir / "manifest.json").read_text(encoding="utf-8"))
        pf_frame = select_proof_frames(mf["beats"])[0][1]
        proof_dir = ep_dir / "proofs"
        proof_dir.mkdir(parents=True, exist_ok=True)

        push_py = Path(f"/tmp/{ep_slug}_push_render.py")
        push_py.write_text(
            f"""
import json, os, select, subprocess, sys, time
from pathlib import Path

subprocess.run("tar -xzf /content/{ep_slug}_delta.tar.gz -C /content/Utility_Explainer_Studio", shell=True, check=True)
root = Path("/content/Utility_Explainer_Studio")
mf = json.loads((root / "{ep_rel}" / "manifest.json").read_text(encoding="utf-8"))
props_path = Path("/content/{ep_slug}_props.json")
props_path.write_text(json.dumps({{"data": mf}}), encoding="utf-8")

# Quick 1-frame proof check before full render
subprocess.run(
    f"cd /content/Utility_Explainer_Studio && ./node_modules/.bin/remotion still src/index.tsx KarmicGenie-ColorfulCreator-16x9 /content/{ep_slug}_proof.png --frame={pf_frame} --props={{props_path}} --gl=angle",
    shell=True, check=True
)
print("PROOF_OK", flush=True)

out_mp4 = "{remote_mp4}"
cores = min(10, max(6, os.cpu_count() or 8))
cmd = (
    f"cd /content/Utility_Explainer_Studio && "
    f"./node_modules/.bin/remotion render src/index.tsx KarmicGenie-ColorfulCreator-16x9 {{out_mp4}} "
    f"--props={{props_path}} --gl=angle --concurrency={{cores}} --codec=h264 --crf=18 --audio-bitrate=256k"
)
print(f"[Render Start {ep_slug}] cores={{cores}} dur={{mf['totalDurationSec']}}s", flush=True)
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
t0 = time.time()
tail = []
while True:
    ready, _, _ = select.select([proc.stdout], [], [], 9.0)
    if ready:
        ln = proc.stdout.readline()
        if ln:
            tail.append(ln.rstrip())
            if len(tail) > 30: tail.pop(0)
            if "Rendered " in ln or "Encoded " in ln or "Error" in ln or "Failed" in ln:
                print(ln, end="", flush=True)
        elif proc.poll() is not None:
            break
    else:
        if proc.poll() is not None:
            break
        print(f"[render heartbeat {{int(time.time() - t0)}}s]", flush=True)
rc = proc.wait()
if rc != 0:
    print("FATAL: Render failed rc=", rc, flush=True)
    print("\\n".join(tail[-20:]), flush=True)
    sys.exit(rc)
print("RENDER_COMPLETE", flush=True)
""",
            encoding="utf-8",
        )
        run_local(f"{COLAB_BIN} exec -s {sid} -f '{push_py}' --timeout 0", retries=3, timeout_s=7200)
        run_local(f"{COLAB_BIN} download -s {sid} '/content/{ep_slug}_proof.png' '{proof_dir / 'proof_mid.png'}'", retries=2, timeout_s=90)
        download_chunked(sid, remote_mp4, local_mp4)
        if not args.keep_alive:
            assert_safe_stop(sid, protected_file, session_file)
            print(f"[ALL RENDERED & CLEANED] {local_mp4}", flush=True)
        else:
            print(f"[RENDERED — WARM SESSION {sid} KEPT ALIVE] {local_mp4}", flush=True)


if __name__ == "__main__":
    main()
