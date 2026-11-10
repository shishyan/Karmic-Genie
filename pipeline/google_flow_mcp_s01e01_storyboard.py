#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Flow MCP Server & Full-Film Autonomous Engine (v3.0)
The Karmic Genie Show — Season 1, Episode 1 (~08:05 Epic Theatrical Film):
  "THE WAY FORWARD: AS IN THE MACROCOSM, SO IN THE MICROCOSM (Pindam in Andam)"
Account: nagaraj957@gmail.com (Google Flow Ultra Plan — Omni 1.1 Flash / Veo 3.1)

Exposes 6 MCP Tools over JSON-RPC 2.0 stdio:
  1. `check_google_flow_connection`
     Inspects live Chrome CDP (`9225`, `9222`), ComfyUI Flow Bridge (`8190`), and clip download
     progress (`X / 48` spoken 16:9 clips) across `episodes/S01E01_The_Way_Forward_Master/flow_16x9_clips/`.
  2. `get_s01e01_storyboard_scenes`
     Returns the 12-scene S01E01 Epic Movie Storyboard (`GOOGLE_FLOW_STORYBOARD_PACKAGE_S01E01.json`).
  3. `get_s01e01_48_shot_ledger`
     Exports & returns the canonical 48-shot (`WF01..WF48`), 10-batch shooting ledger aligned to the
     14-page screenplay (`Narrator Me + 1 Child ONLY` in movie scenes, White-Wall Zoom-In/Zoom-Out
     portals, Two-Birds active mirroring + 3D Bullet-Time Time-Pauses, zero real brand/person names).
  4. `generate_google_flow_batch`
     Executes a specific batch (`batch_01`..`batch_10`) or `"all"` in Google Flow (`flow.google.com`)
     using `FlowFilmRunner`: opens fresh Flow project, sets `Never` + `16:9` + `x1`, uploads the 16:9
     storyboard reference plate, attaches the official `Me` Avatar chip (`Avatars -> Me -> Add to prompt`
     with ZERO literal `@` in ProseMirror), handles confirmation prompts, and downloads `.mp4` clips.
  5. `assemble_s01e01_master_film`
     Runs `build_s01e01_way_forward_master_film.py` (`faster-whisper` speech-to-slot alignment,
     `rubberband` `0.87x`/`0.84x` cinema pacing, 12 RGBA glass badges, borderless ASS subtitles,
     Official 7D Cold Open + `-14 LUFS` Logo Finale) to render the final 1080p MP4 film.
  6. `build_s01e01_full_epic_film_in_flow`
     End-to-end master tool: generates all 48 Google Flow 16:9 clips across batches 1..10 AND
     immediately assembles `renders/Karmic_Genie_Show_S01E01_The_Way_Forward_Master_16x9.mp4` +
     `docs/assets/videos/Karmic_Genie_Show_S01E01_The_Way_Forward_Master_16x9.mp4`.

Direct CLI Modes:
  python3 pipeline/google_flow_mcp_s01e01_storyboard.py --status
  python3 pipeline/google_flow_mcp_s01e01_storyboard.py --launch-chrome
  python3 pipeline/google_flow_mcp_s01e01_storyboard.py --run-batch batch_01
  python3 pipeline/google_flow_mcp_s01e01_storyboard.py --full-film
"""

import io
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from contextlib import redirect_stdout
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parent
REPO_DIR = PIPELINE_DIR.parent
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from generate_s01e01_way_forward_flow_clips import (  # noqa: E402
    BATCH_SPECS,
    CDP_PORTS,
    EP_CLIPS_DIR,
    FlowFilmRunner,
    build_batch_prompt,
    export_ledger_json,
    flatten_shot_ledger,
    resolve_repo_image,
)

PACKAGE_JSON = REPO_DIR / "GOOGLE_FLOW_STORYBOARD_PACKAGE_S01E01.json"
DOCS_PACKAGE_JSON = REPO_DIR / "docs" / "GOOGLE_FLOW_STORYBOARD_PACKAGE_S01E01.json"
MASTER_ASSEMBLER_PY = PIPELINE_DIR / "build_s01e01_way_forward_master_film.py"
OUT_MASTER_MP4 = REPO_DIR / "renders" / "Karmic_Genie_Show_S01E01_The_Way_Forward_Master_16x9.mp4"
OUT_WEB_MP4 = REPO_DIR / "docs" / "assets" / "videos" / "Karmic_Genie_Show_S01E01_The_Way_Forward_Master_16x9.mp4"
COMFYUI_URL = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8190")
GOOGLE_ACCOUNT = os.environ.get("GOOGLE_ACCOUNT", "nagaraj957@gmail.com")


def sanitize_flow_prompt(prompt: str) -> str:
    """Guarantee zero literal '@' symbols exist in ProseMirror text (uses attached Me Avatar chip instead)."""
    cleaned = prompt.replace("@Me", "Me").replace("@me", "Me").replace("@", "")
    return cleaned.strip()


def load_storyboard_package() -> dict:
    if PACKAGE_JSON.exists():
        return json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    raise FileNotFoundError(f"Missing storyboard package: {PACKAGE_JSON}")


def find_active_cdp_tab() -> tuple[int | None, dict | None, list[dict]]:
    """Inspect local CDP ports (9225, 9222) for an open Google Flow page tab."""
    all_tabs: list[dict] = []
    for port in CDP_PORTS:
        try:
            raw = urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=2).read()
            tabs = json.loads(raw.decode("utf-8"))
            all_tabs.extend(tabs)
            flow_tabs = [
                t for t in tabs
                if t.get("type") == "page" and ("flow.google" in t.get("url", "") or "labs.google" in t.get("url", ""))
            ]
            if flow_tabs:
                return port, flow_tabs[0], tabs
        except Exception:
            continue
    return None, None, all_tabs


def try_auto_launch_local_chrome(port: int = 9225) -> dict:
    """
    If running on a workstation with an existing signed-in Chrome profile and DISPLAY/Wayland,
    launch Chrome on `--remote-debugging-port=9225` pointing to `https://flow.google.com/u/0/`.
    Never launches an unauthenticated empty headless session in cloud VMs without a profile.
    """
    display = os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
    candidate_profiles = [
        Path(os.environ.get("FLOW_CHROME_PROFILE", "")) if os.environ.get("FLOW_CHROME_PROFILE") else None,
        Path.home() / ".config" / "google-chrome-flow-9225",
        Path.home() / ".config" / "google-chrome",
        Path("/home/shishyan/.config/google-chrome"),
    ]
    valid_profile = next(
        (p for p in candidate_profiles if p is not None and p.exists() and (p / "Default" / "Cookies").exists()),
        None,
    )
    chrome_bin = shutil.which("google-chrome") or shutil.which("google-chrome-stable") or shutil.which("chromium")
    if not chrome_bin:
        return {"launched": False, "reason": "No google-chrome/chromium binary found on PATH."}
    if not display and valid_profile is None:
        return {
            "launched": False,
            "reason": (
                "Running in headless cloud VM without a signed-in local Chrome user-data-dir for "
                f"{GOOGLE_ACCOUNT} (OAuth/session cookies stay on the local workstation by security policy)."
            ),
        }

    cmd = [
        chrome_bin,
        f"--remote-debugging-port={port}",
        "--no-first-run",
        "--no-default-browser-check",
    ]
    if valid_profile is not None:
        cmd.append(f"--user-data-dir={valid_profile}")
    if not display:
        cmd.append("--headless=new")
    cmd.append("https://flow.google.com/u/0/")

    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    for _ in range(12):
        time.sleep(1.0)
        found_port, tab, _ = find_active_cdp_tab()
        if found_port and tab:
            return {"launched": True, "cdp_port": found_port, "url": tab.get("url")}
    return {"launched": False, "reason": f"Spawned {chrome_bin}, but no authenticated flow.google.com tab appeared on port {port}."}


def count_clip_progress() -> dict:
    """Count downloaded MP4 clips per batch and sub-batch against the 48-shot ledger."""
    flat = flatten_shot_ledger()
    groups: dict[tuple[str, str], int] = {}
    for sh in flat:
        key = (sh["batch_id"], sh["file_prefix"])
        groups[key] = groups.get(key, 0) + 1

    ready_total = 0
    expected_total = 0
    per_batch = []
    for (bid, prefix), exp in groups.items():
        expected_total += exp
        bdir = EP_CLIPS_DIR / bid
        found = sorted([p.name for p in bdir.glob(f"{prefix}_*.mp4") if p.stat().st_size > 200_000]) if bdir.exists() else []
        ready = min(len(found), exp)
        ready_total += ready
        per_batch.append({
            "batch_id": bid,
            "file_prefix": prefix,
            "ready_clips": ready,
            "expected_clips": exp,
            "complete": ready >= exp,
            "files": found,
        })
    return {
        "ready_clips": ready_total,
        "expected_clips": expected_total,
        "all_48_clips_ready": ready_total >= expected_total,
        "master_mp4_exists": OUT_MASTER_MP4.exists(),
        "web_mp4_exists": OUT_WEB_MP4.exists(),
        "batches": per_batch,
    }


def get_connection_status() -> dict:
    port, tab, _ = find_active_cdp_tab()
    comfy_ok = False
    try:
        urllib.request.urlopen(f"{COMFYUI_URL}/system_stats", timeout=1.5).read()
        comfy_ok = True
    except Exception:
        comfy_ok = False

    progress = count_clip_progress()
    return {
        "mcp_server": "karmic-genie-google-flow-mcp",
        "version": "3.0.0",
        "account": GOOGLE_ACCOUNT,
        "environment_host": os.uname().nodename,
        "home_dir": str(Path.home()),
        "cdp_connected": bool(port and tab),
        "cdp_port": port,
        "active_flow_tab_url": tab.get("url") if tab else None,
        "comfyui_bridge_connected": comfy_ok,
        "clip_progress": progress,
        "workstation_chrome_command": (
            "google-chrome --remote-debugging-port=9225 "
            "--user-data-dir=\"$HOME/.config/google-chrome-flow-9225\" https://flow.google.com/u/0/"
        ),
    }


def execute_flow_batches(batch_filter: str = "all", auto_launch_chrome: bool = True) -> dict:
    """
    Run one or all 10 Episode 1 batches in Google Flow via `FlowFilmRunner`.
    Captures `FlowFilmRunner` stdout cleanly so MCP JSON-RPC stdout is never corrupted!
    """
    export_ledger_json()
    port, tab, _ = find_active_cdp_tab()
    launch_info = None
    if not (port and tab) and auto_launch_chrome:
        launch_info = try_auto_launch_local_chrome(port=CDP_PORTS[0])
        port, tab, _ = find_active_cdp_tab()

    if not (port and tab):
        status = get_connection_status()
        return {
            "ok": False,
            "status": "blocked_no_authenticated_flow_browser_session",
            "message": (
                f"No authenticated Google Flow (`flow.google.com`) Chrome CDP session detected on ports {CDP_PORTS} "
                f"for `{GOOGLE_ACCOUNT}`."
            ),
            "auto_launch_attempt": launch_info,
            "connection": status,
            "how_to_run_immediately": [
                "1. On your signed-in workstation, start Chrome with remote debugging enabled on port 9225:",
                f"   {status['workstation_chrome_command']}",
                "2. Invoke MCP tool `build_s01e01_full_epic_film_in_flow` from your local IDE MCP (`google-flow`) OR run:",
                "   python3 pipeline/google_flow_mcp_s01e01_storyboard.py --full-film",
            ],
        }

    selected = [
        b for b in BATCH_SPECS
        if batch_filter in ("all", "", "*") or batch_filter in b["id"]
    ]
    if not selected:
        return {
            "ok": False,
            "error": f"No batch matched '{batch_filter}'. Valid IDs: {[b['id'] for b in BATCH_SPECS]}",
        }

    log_buf = io.StringIO()
    generated_summary = []
    with redirect_stdout(log_buf):
        runner = FlowFilmRunner()
        try:
            for b in selected:
                bid = b["id"]
                bdir = EP_CLIPS_DIR / bid
                if "mixed_sub_batches" in b:
                    for sub in b["mixed_sub_batches"]:
                        ref_img = resolve_repo_image(sub["ref_rel"])
                        prompt_txt = sanitize_flow_prompt(
                            build_batch_prompt(sub["shots"], sub["include_me"], sub.get("extra_header", ""))
                        )
                        saved = runner.run_sub_batch(
                            bdir, sub["sub_prefix"], ref_img, sub["include_me"], prompt_txt, len(sub["shots"])
                        )
                        generated_summary.append({"batch_id": bid, "prefix": sub["sub_prefix"], "saved": saved})
                else:
                    ref_img = resolve_repo_image(b["ref_rel"])
                    prompt_txt = sanitize_flow_prompt(build_batch_prompt(b["shots"], b["include_me"]))
                    saved = runner.run_sub_batch(
                        bdir, bid, ref_img, b["include_me"], prompt_txt, len(b["shots"])
                    )
                    generated_summary.append({"batch_id": bid, "prefix": bid, "saved": saved})
        finally:
            runner.close()

    return {
        "ok": True,
        "status": "completed_google_flow_generation",
        "cdp_port": port,
        "batches_executed": [b["id"] for b in selected],
        "generated_summary": generated_summary,
        "clip_progress": count_clip_progress(),
        "runner_log": log_buf.getvalue()[-4000:],
    }


def run_master_assembler(check_only: bool = False) -> dict:
    """Invoke `build_s01e01_way_forward_master_film.py` and return structured JSON output."""
    cmd = [sys.executable, str(MASTER_ASSEMBLER_PY)]
    if check_only:
        cmd.append("--check")
    proc = subprocess.run(cmd, cwd=str(REPO_DIR), capture_output=True, text=True)
    return {
        "ok": proc.returncode == 0,
        "exit_code": proc.returncode,
        "check_only": check_only,
        "master_mp4": str(OUT_MASTER_MP4) if OUT_MASTER_MP4.exists() else None,
        "master_size_mb": round(OUT_MASTER_MP4.stat().st_size / 1e6, 2) if OUT_MASTER_MP4.exists() else None,
        "web_mp4": str(OUT_WEB_MP4) if OUT_WEB_MP4.exists() else None,
        "web_size_mb": round(OUT_WEB_MP4.stat().st_size / 1e6, 2) if OUT_WEB_MP4.exists() else None,
        "stdout": proc.stdout[-4000:],
        "stderr": proc.stderr[-2000:],
    }


MCP_TOOLS = [
    {
        "name": "check_google_flow_connection",
        "description": (
            "Check live Google Flow Chrome CDP connection (ports 9225/9222 for nagaraj957@gmail.com), "
            "ComfyUI bridge status, and 48-shot S01E01 clip download progress."
        ),
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_s01e01_storyboard_scenes",
        "description": (
            "Retrieve all 12 Episode 1 (S01E01: The Way Forward — Epic Movie Edition) storyboard scenes, "
            "Two-Birds active narrator blocking, 3D Bullet-Time Time-Pause notes, and visual asset paths."
        ),
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_s01e01_48_shot_ledger",
        "description": (
            "Export and return the canonical 48-shot (WF01..WF48), 10-batch Google Flow shooting ledger "
            "for S01E01 aligned to the 14-page Epic Movie screenplay (Narrator Me + 1 Child rule, "
            "White-Wall portals, Two-Birds active mirroring, Me Avatar attachment, 15-18 spoken words/shot)."
        ),
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "generate_google_flow_batch",
        "description": (
            "Generate widescreen 16:9 spoken cinema video clips in Google Flow (flow.google.com, Omni 1.1 Flash / "
            "Veo 3.1) for a specific S01E01 batch ('batch_01'..'batch_10') or 'all', automatically attaching "
            "the 16:9 storyboard reference image and the official Me Avatar chip."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "batch_id": {
                    "type": "string",
                    "description": "Batch identifier ('batch_01'..'batch_10') or 'all' for all 48 shots.",
                    "default": "all",
                }
            },
        },
    },
    {
        "name": "assemble_s01e01_master_film",
        "description": (
            "Assemble the 48 downloaded Google Flow 16:9 clips into the finished ~8-minute 1080p -14 LUFS "
            "theatrical film (Karmic_Genie_Show_S01E01_The_Way_Forward_Master_16x9.mp4) using faster-whisper "
            "alignment, rubberband cinema pacing, 12 RGBA glass badges, and ASS subtitles."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "check_only": {
                    "type": "boolean",
                    "description": "If true, runs pre-flight verification (--check) without encoding.",
                    "default": False,
                }
            },
        },
    },
    {
        "name": "build_s01e01_full_epic_film_in_flow",
        "description": (
            "End-to-end Episode 1 Film Builder via Google Flow MCP: executes all 10 batches (48 spoken 16:9 "
            "clips with Me Avatar + storyboard plates) in Google Flow and assembles the final 1080p master MP4."
        ),
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def call_mcp_tool(name: str, args: dict) -> dict:
    if name == "check_google_flow_connection":
        return get_connection_status()
    if name == "get_s01e01_storyboard_scenes":
        return load_storyboard_package()
    if name == "get_s01e01_48_shot_ledger":
        ledger_path = export_ledger_json()
        return json.loads(ledger_path.read_text(encoding="utf-8"))
    if name == "generate_google_flow_batch":
        batch_id = str(args.get("batch_id", "all"))
        return execute_flow_batches(batch_filter=batch_id)
    if name == "assemble_s01e01_master_film":
        return run_master_assembler(check_only=bool(args.get("check_only", False)))
    if name == "build_s01e01_full_epic_film_in_flow":
        gen_res = execute_flow_batches(batch_filter="all")
        if not gen_res.get("ok"):
            return gen_res
        progress = gen_res.get("clip_progress", {})
        if not progress.get("all_48_clips_ready"):
            return {
                "ok": False,
                "status": "partial_clips_generated",
                "generation": gen_res,
                "message": (
                    f"Generated {progress.get('ready_clips')}/{progress.get('expected_clips')} clips so far; "
                    "re-invoke `build_s01e01_full_epic_film_in_flow` to resume remaining clips before final assembly."
                ),
            }
        asm_res = run_master_assembler(check_only=False)
        return {
            "ok": asm_res.get("ok", False),
            "status": "epic_film_assembled" if asm_res.get("ok") else "assembly_failed",
            "generation": gen_res,
            "assembly": asm_res,
        }
    return {"error": f"Unknown tool: {name}"}


def send_rpc_message(payload: dict, framed: bool = False):
    body = json.dumps(payload, ensure_ascii=False)
    if framed:
        raw = body.encode("utf-8")
        sys.stdout.buffer.write(f"Content-Length: {len(raw)}\r\n\r\n".encode("ascii") + raw)
        sys.stdout.buffer.flush()
    else:
        sys.stdout.write(body + "\n")
        sys.stdout.flush()


def handle_rpc_object(req: dict, framed: bool = False):
    method = req.get("method")
    msg_id = req.get("id")

    if method == "initialize":
        send_rpc_message({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "karmic-genie-google-flow-mcp",
                    "version": "3.0.0",
                },
            },
        }, framed=framed)
    elif method in ("notifications/initialized", "initialized"):
        return
    elif method == "ping":
        send_rpc_message({"jsonrpc": "2.0", "id": msg_id, "result": {}}, framed=framed)
    elif method == "tools/list":
        send_rpc_message({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": MCP_TOOLS}}, framed=framed)
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name", "")
        args = params.get("arguments", {}) or {}
        try:
            res_obj = call_mcp_tool(name, args)
            is_err = bool(res_obj.get("error") or res_obj.get("ok") is False)
            content = [{"type": "text", "text": json.dumps(res_obj, indent=2, ensure_ascii=False)}]
            send_rpc_message(
                {"jsonrpc": "2.0", "id": msg_id, "result": {"content": content, "isError": is_err}},
                framed=framed,
            )
        except Exception as exc:
            send_rpc_message(
                {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps({"ok": False, "exception": str(exc)})}],
                        "isError": True,
                    },
                },
                framed=framed,
            )
    elif msg_id is not None:
        send_rpc_message(
            {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}},
            framed=framed,
        )


def serve_mcp_stdio():
    """Supports both newline-delimited JSON-RPC (MCP 2024-11-05) and Content-Length LSP framing."""
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            break
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.lower().startswith(b"content-length:"):
            length = int(stripped.split(b":", 1)[1].strip())
            while True:
                hdr = sys.stdin.buffer.readline()
                if not hdr or hdr in (b"\r\n", b"\n"):
                    break
            body = sys.stdin.buffer.read(length)
            if not body:
                break
            handle_rpc_object(json.loads(body.decode("utf-8")), framed=True)
        else:
            try:
                req = json.loads(stripped.decode("utf-8"))
            except Exception:
                continue
            handle_rpc_object(req, framed=False)


def main():
    if "--status" in sys.argv:
        print(json.dumps(get_connection_status(), indent=2, ensure_ascii=False))
        return
    if "--launch-chrome" in sys.argv:
        print(json.dumps(try_auto_launch_local_chrome(port=CDP_PORTS[0]), indent=2, ensure_ascii=False))
        return
    if "--run-batch" in sys.argv:
        idx = sys.argv.index("--run-batch")
        bid = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else "all"
        print(json.dumps(execute_flow_batches(batch_filter=bid), indent=2, ensure_ascii=False))
        return
    if "--assemble" in sys.argv:
        print(json.dumps(run_master_assembler(check_only=("--check" in sys.argv)), indent=2, ensure_ascii=False))
        return
    if "--full-film" in sys.argv:
        print(json.dumps(call_mcp_tool("build_s01e01_full_epic_film_in_flow", {}), indent=2, ensure_ascii=False))
        return
    if "--build-all" in sys.argv:
        pkg = load_storyboard_package()
        if DOCS_PACKAGE_JSON.parent.exists():
            shutil.copy2(PACKAGE_JSON, DOCS_PACKAGE_JSON)
        export_ledger_json()
        print(f"✅ Synced 12-scene storyboard + 48-shot Flow ledger for {pkg.get('account', GOOGLE_ACCOUNT)}.")
        return

    serve_mcp_stdio()


if __name__ == "__main__":
    main()
