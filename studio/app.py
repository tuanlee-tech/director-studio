"""
AI Audio Studio - Unified Management Dashboard
Runs natively (Python + Flask) or in Docker.
"""

import os
import sys
import json
import time
import threading
import platform
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static", template_folder="templates")

# --- Paths ---
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# --- Service Registry ---
SERVICES = {
    "vieneu-tts": {
        "name": "VieNeu TTS",
        "description": "Vietnamese Text-to-Speech — 48kHz, voice cloning, bilingual",
        "icon": "🎙️",
        "category": "tts",
        "url": os.environ.get("VIENEU_TTS_URL", "http://localhost:7860"),
        "health_endpoint": "/",
        "port": 7860,
        "version": "v3.8.3",
        "features": [
            "48kHz output",
            "ONNX CPU / PyTorch GPU",
            "Voice cloning",
            "Emotion tags",
            "6 preset voices",
            "Vietnamese & English",
        ],
        "models": [
            {
                "id": "pnnbao-ump/VieNeu-TTS-v3-Turbo",
                "name": "v3 Turbo (fp32)",
                "precision": "fp32",
                "description": "Default — best quality, 48kHz",
                "default": True,
            },
            {
                "id": "pnnbao-ump/VieNeu-TTS-v3-Turbo",
                "name": "v3 Turbo (int8)",
                "precision": "int8",
                "description": "Faster on AVX-512/VNNI CPUs",
                "default": False,
            },
            {
                "id": "pnnbao-ump/VieNeu-TTS-v3-Nano",
                "name": "v3 Nano (preview)",
                "precision": "fp32",
                "description": "24kHz, ultra-fast, weak CPUs / edge",
                "default": False,
            },
        ],
    },
    # --- Add future services here ---
    # "whisper-stt": { ... },
}

# --- Health Check ---
_status_cache = {}
_status_lock = threading.Lock()


def check_service_health(service_id: str) -> dict:
    """Check if a service is reachable."""
    import requests as req

    svc = SERVICES.get(service_id)
    if not svc:
        return {"status": "unknown", "message": "Service not registered"}

    try:
        url = svc["url"] + svc["health_endpoint"]
        r = req.get(url, timeout=5)
        if r.status_code == 200:
            return {
                "status": "healthy",
                "message": "Running",
                "response_time_ms": int(r.elapsed.total_seconds() * 1000),
                "checked_at": datetime.now().isoformat(),
            }
        return {
            "status": "unhealthy",
            "message": f"HTTP {r.status_code}",
            "checked_at": datetime.now().isoformat(),
        }
    except req.exceptions.ConnectionError:
        return {
            "status": "stopped",
            "message": "Not running — start with launcher",
            "checked_at": datetime.now().isoformat(),
        }
    except req.exceptions.Timeout:
        return {
            "status": "starting",
            "message": "Timeout — may be loading model",
            "checked_at": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "checked_at": datetime.now().isoformat(),
        }


def _detect_gpu() -> dict:
    """Detect GPU info from host."""
    gpu = {"name": "None", "vram_mb": 0, "driver": "", "has_gpu": False}
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
            text=True, timeout=5, stderr=subprocess.DEVNULL,
        ).strip()
        if out:
            parts = [p.strip() for p in out.split(",")]
            gpu["name"] = parts[0]
            gpu["has_gpu"] = True
            if len(parts) > 1 and "MiB" in parts[1]:
                gpu["vram_mb"] = int(parts[1].replace("MiB", "").strip())
            if len(parts) > 2:
                gpu["driver"] = parts[2]
    except Exception:
        pass
    return gpu


def _detect_backend() -> str:
    """Detect what TTS backend is being used."""
    venv_python = ROOT_DIR / "VieNeu-TTS" / ".venv" / ("Scripts" if sys.platform == "win32" else "bin") / ("python.exe" if sys.platform == "win32" else "python")
    if not venv_python.exists():
        return "unknown"
    try:
        out = subprocess.check_output(
            [str(venv_python), "-c", "import torch; print('pytorch-cuda' if torch.cuda.is_available() else 'pytorch-cpu')"],
            text=True, timeout=10, stderr=subprocess.DEVNULL,
        ).strip()
        return out
    except Exception:
        pass
    try:
        out = subprocess.check_output(
            [str(venv_python), "-c", "import onnxruntime as ort; eps=ort.get_available_providers(); print('onnx-cuda' if 'CUDAExecutionProvider' in eps else 'onnx-cpu')"],
            text=True, timeout=10, stderr=subprocess.DEVNULL,
        ).strip()
        return out
    except Exception:
        return "onnx-cpu"


def _check_model_cached() -> dict:
    """Check if the TTS model is downloaded."""
    venv_python = ROOT_DIR / "VieNeu-TTS" / ".venv" / ("Scripts" if sys.platform == "win32" else "bin") / ("python.exe" if sys.platform == "win32" else "python")
    if not venv_python.exists():
        return {"cached": False, "size_mb": 0}
    try:
        out = subprocess.check_output(
            [str(venv_python), "-c", """
from huggingface_hub import scan_cache_dir
for r in scan_cache_dir().repos:
    if 'VieNeu-TTS-v3-Turbo' in r.repo_id:
        print(f"yes:{r.size_on_disk // (1024*1024)}")
        break
else:
    print("no:0")
"""],
            text=True, timeout=10, stderr=subprocess.DEVNULL,
        ).strip()
        parts = out.split(":")
        return {"cached": parts[0] == "yes", "size_mb": int(parts[1]) if len(parts) > 1 else 0}
    except Exception:
        return {"cached": False, "size_mb": 0}


def background_health_checker():
    """Periodically check all services."""
    while True:
        for sid in SERVICES:
            result = check_service_health(sid)
            with _status_lock:
                _status_cache[sid] = result
        time.sleep(15)


# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html", services=SERVICES)


@app.route("/api/health")
def api_health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


@app.route("/api/services")
def api_services():
    result = {}
    for sid, svc in SERVICES.items():
        with _status_lock:
            status = _status_cache.get(sid, {"status": "unknown", "message": "Checking..."})
        result[sid] = {
            **svc,
            "health": status,
            "external_url": f"http://localhost:{svc['port']}",
        }
    return jsonify(result)


@app.route("/api/services/<service_id>/health")
def api_service_health(service_id):
    result = check_service_health(service_id)
    with _status_lock:
        _status_cache[service_id] = result
    return jsonify(result)


@app.route("/api/services/<service_id>/test-tts", methods=["POST"])
def api_test_tts(service_id):
    """Quick TTS test via OpenAI-compatible API."""
    import requests as req

    data = request.get_json() or {}
    text = data.get("text", "Xin chào, đây là bài test giọng nói.")
    voice = data.get("voice", "ngoc-anh")

    api_url = os.environ.get("VIENEU_API_URL", "http://localhost:8000")
    try:
        r = req.post(
            f"{api_url}/v1/audio/speech",
            json={"model": "vieneu-tts-v3-turbo", "input": text, "voice": voice, "response_format": "wav"},
            timeout=60,
        )
        if r.status_code == 200:
            ts = int(time.time())
            fname = f"test_{ts}.wav"
            (DATA_DIR / fname).write_bytes(r.content)
            return jsonify({"status": "ok", "audio_url": f"/api/audio/{fname}", "duration_ms": int(r.elapsed.total_seconds() * 1000)})
        return jsonify({"status": "error", "message": f"API {r.status_code}: {r.text[:200]}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/audio/<filename>")
def api_audio(filename):
    return send_from_directory(str(DATA_DIR), filename)


# --- Video Rendering & Studio Timeline ---
_render_tasks = {}
_render_lock = threading.Lock()


@app.route("/api/channels-videos")
def api_channels_videos():
    """Liệt kê danh sách channels và video slugs trong monorepo."""
    channels_dir = ROOT_DIR / "channels"
    result = []
    if not channels_dir.exists():
        return jsonify({"channels": []})

    for ch_path in channels_dir.iterdir():
        if not ch_path.is_dir() or ch_path.name.startswith("."):
            continue

        ch_name = ch_path.name
        ch_title = ch_name
        config_file = ch_path / "config.json"
        if config_file.exists():
            try:
                cfg = json.loads(config_file.read_text(encoding="utf-8"))
                ch_title = cfg.get("channel_name", ch_name)
            except Exception:
                pass

        videos_dir = ch_path / "videos"
        videos = []
        if videos_dir.exists():
            for v_path in videos_dir.iterdir():
                if not v_path.is_dir() or v_path.name.startswith("."):
                    continue

                slug = v_path.name
                has_comp = (v_path / "assets" / "remotion-composition.json").exists()
                has_broll = (v_path / "broll-plan.json").exists()
                has_subs = (v_path / "subtitles" / "karaoke.srt").exists() or (v_path / "subtitles" / "karaoke.ass").exists()
                audio_dir = v_path / "audio"
                audio_count = len(list(audio_dir.glob("*.wav"))) if audio_dir.exists() else 0
                final_video_path = v_path / "final_video.mp4"

                videos.append({
                    "slug": slug,
                    "has_composition": has_comp,
                    "has_broll": has_broll,
                    "has_subs": has_subs,
                    "audio_count": audio_count,
                    "final_video_exists": final_video_path.exists(),
                    "final_video_url": f"/api/media/{ch_name}/{slug}/final_video.mp4" if final_video_path.exists() else None,
                })

        result.append({
            "name": ch_name,
            "title": ch_title,
            "videos": videos,
        })

    return jsonify({"channels": result})


@app.route("/api/video-data/<channel>/<slug>")
def api_video_data(channel, slug):
    """Lấy dữ liệu composition và sequences cho Remotion Player."""
    video_dir = ROOT_DIR / "channels" / channel / "videos" / slug
    if not video_dir.exists():
        return jsonify({"status": "error", "message": "Video directory not found"}), 404

    comp_file = video_dir / "assets" / "remotion-composition.json"
    if comp_file.exists():
        try:
            data = json.loads(comp_file.read_text(encoding="utf-8"))
            # Chuẩn hóa URLs để phục vụ qua static API
            for seq in data.get("sequences", []):
                scene = seq.get("scene", "")
                seq_id = seq.get("id", "")
                # Narration audio
                audio_file = video_dir / "audio" / f"{scene}_narration.wav"
                if audio_file.exists():
                    seq["narration_audio_url"] = f"/api/media/{channel}/{slug}/audio/{scene}_narration.wav"

                # Word timings từ Whisper
                timing_file = video_dir / "audio" / f"{scene}_timing.json"
                if timing_file.exists() and "words" not in seq:
                    try:
                        t_data = json.loads(timing_file.read_text(encoding="utf-8"))
                        seq["words"] = t_data.get("words", [])
                    except Exception:
                        pass

                # Asset path
                assets_dir = video_dir / "assets"
                matched_asset = None
                for ext in [".mp4", ".png", ".jpg", ".webp"]:
                    candidate = assets_dir / f"{seq_id}{ext}"
                    if candidate.exists():
                        matched_asset = f"/api/media/{channel}/{slug}/assets/{seq_id}{ext}"
                        break
                    candidate_scene = assets_dir / f"{scene}_{seq.get('type', 'IMG')}{ext}"
                    if candidate_scene.exists():
                        matched_asset = f"/api/media/{channel}/{slug}/assets/{candidate_scene.name}"
                        break
                if matched_asset:
                    seq["asset_path"] = matched_asset

            return jsonify({"status": "ok", "composition": data})
        except Exception as e:
            return jsonify({"status": "error", "message": f"Error parsing composition: {e}"}), 500

    # Fallback nếu chưa có file remotion-composition.json nhưng có broll-plan
    broll_file = video_dir / "broll-plan.json"
    if broll_file.exists():
        try:
            broll_data = json.loads(broll_file.read_text(encoding="utf-8"))
            sequences = []
            fps = 30
            current_frame = 0
            for item in broll_data:
                dur_s = item.get("duration_seconds", 4)
                dur_f = int(dur_s * fps)
                scene = item.get("scene", "S001")
                seq_id = item.get("broll_id", f"{scene}-A")
                seq_type = item.get("type", "AIV")

                seq = {
                    "id": seq_id,
                    "scene": scene,
                    "beat": item.get("visual_beat", "Scene Beat"),
                    "type": seq_type,
                    "duration_seconds": dur_s,
                    "duration_frames": dur_f,
                    "start_frame": current_frame,
                    "motion_effect": "ken_burns_zoom_in" if seq_type == "IMG" else "static",
                    "narration_text": item.get("visual_beat", ""),
                }

                audio_file = video_dir / "audio" / f"{scene}_narration.wav"
                if audio_file.exists():
                    seq["narration_audio_url"] = f"/api/media/{channel}/{slug}/audio/{scene}_narration.wav"

                timing_file = video_dir / "audio" / f"{scene}_timing.json"
                if timing_file.exists():
                    try:
                        t_data = json.loads(timing_file.read_text(encoding="utf-8"))
                        seq["words"] = t_data.get("words", [])
                    except Exception:
                        pass

                sequences.append(seq)
                current_frame += dur_f

            total_s = current_frame / fps
            return jsonify({
                "status": "ok",
                "composition": {
                    "title": slug,
                    "slug": slug,
                    "channel": channel,
                    "fps": fps,
                    "width": 1920,
                    "height": 1080,
                    "total_duration_seconds": total_s,
                    "total_frames": current_frame,
                    "sequences": sequences,
                }
            })
        except Exception as e:
            return jsonify({"status": "error", "message": f"Error parsing broll plan: {e}"}), 500

    return jsonify({"status": "error", "message": "No composition or broll plan found"}), 404


@app.route("/api/media/<channel>/<slug>/<path:filepath>")
def api_media(channel, slug, filepath):
    """Phục vụ an toàn các file media từ thư mục video."""
    video_dir = ROOT_DIR / "channels" / channel / "videos" / slug
    full_path = video_dir / filepath
    if not full_path.exists():
        return jsonify({"status": "error", "message": "File not found"}), 404
    return send_from_directory(str(full_path.parent), full_path.name)


def _execute_render_task(task_id, channel, slug, fps=30):
    """Worker chạy tiến trình render Remotion ngầm."""
    import re
    import uuid

    video_dir = ROOT_DIR / "channels" / channel / "videos" / slug
    remotion_dir = ROOT_DIR / "studio" / "remotion"
    output_file = video_dir / "final_video.mp4"

    try:
        # Lấy composition data
        comp_file = video_dir / "assets" / "remotion-composition.json"
        if not comp_file.exists():
            raise FileNotFoundError(f"Không tìm thấy remotion-composition.json tại {comp_file}")

        comp_data = json.loads(comp_file.read_text(encoding="utf-8"))
        
        # Tạo file props tạm thời
        temp_props_file = remotion_dir / f"temp_props_{task_id}.json"
        temp_props_file.write_text(json.dumps(comp_data, ensure_ascii=False), encoding="utf-8")

        cmd = [
            "npx", "remotion", "render",
            "src/index.ts", "MainVideo",
            str(output_file),
            f"--props={temp_props_file.name}",
            "--overwrite"
        ]

        # Windows execution wrapper
        shell_needed = sys.platform == "win32"
        proc = subprocess.Popen(
            cmd,
            cwd=str(remotion_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=shell_needed,
            encoding="utf-8",
            errors="replace"
        )

        with _render_lock:
            _render_tasks[task_id]["pid"] = proc.pid
            _render_tasks[task_id]["status"] = "rendering"

        # Đọc tiến độ
        progress_pattern = re.compile(r"Rendered\s+(\d+)/(\d+)")
        percent_pattern = re.compile(r"(\d+)%")

        for line in iter(proc.stdout.readline, ""):
            line_str = line.strip()
            if not line_str:
                continue

            prog_match = progress_pattern.search(line_str)
            if prog_match:
                curr, total = int(prog_match.group(1)), int(prog_match.group(2))
                if total > 0:
                    pct = min(100, int((curr / total) * 100))
                    with _render_lock:
                        _render_tasks[task_id]["progress"] = pct
                        _render_tasks[task_id]["log_line"] = line_str

            pct_match = percent_pattern.search(line_str)
            if pct_match and not prog_match:
                with _render_lock:
                    _render_tasks[task_id]["progress"] = int(pct_match.group(1))
                    _render_tasks[task_id]["log_line"] = line_str

        proc.wait()

        # Dọn dẹp file tạm
        if temp_props_file.exists():
            try:
                temp_props_file.unlink()
            except Exception:
                pass

        if proc.returncode == 0 and output_file.exists():
            with _render_lock:
                _render_tasks[task_id]["status"] = "done"
                _render_tasks[task_id]["progress"] = 100
                _render_tasks[task_id]["video_url"] = f"/api/media/{channel}/{slug}/final_video.mp4"
                _render_tasks[task_id]["finished_at"] = datetime.now().isoformat()
        else:
            with _render_lock:
                _render_tasks[task_id]["status"] = "error"
                _render_tasks[task_id]["error"] = f"Remotion render failed with exit code {proc.returncode}"
    except Exception as e:
        with _render_lock:
            _render_tasks[task_id]["status"] = "error"
            _render_tasks[task_id]["error"] = str(e)


@app.route("/api/render-video", methods=["POST"])
def api_render_video():
    """Kích hoạt tiến trình render Remotion ra file MP4."""
    import uuid

    data = request.json or {}
    channel = data.get("channel")
    slug = data.get("slug")
    fps = int(data.get("fps", 30))

    if not channel or not slug:
        return jsonify({"status": "error", "message": "channel and slug are required"}), 400

    task_id = str(uuid.uuid4())[:8]
    with _render_lock:
        _render_tasks[task_id] = {
            "task_id": task_id,
            "channel": channel,
            "slug": slug,
            "status": "queued",
            "progress": 0,
            "started_at": datetime.now().isoformat(),
            "video_url": None,
            "error": None,
        }

    thread = threading.Thread(target=_execute_render_task, args=(task_id, channel, slug, fps), daemon=True)
    thread.start()

    return jsonify({"status": "ok", "task_id": task_id, "message": "Render task queued"})


@app.route("/api/render-status/<task_id>")
def api_render_status(task_id):
    """Kiểm tra tiến độ render."""
    with _render_lock:
        task = _render_tasks.get(task_id)
    if not task:
        return jsonify({"status": "error", "message": "Task not found"}), 404
    return jsonify(task)


# --- Google Flow Multi-Account Dispatcher Integration ---
_flow_dispatch_tasks = {}
_flow_lock = threading.Lock()

# Add tools/flow-dispatcher to sys.path
FLOW_DIR = ROOT_DIR / "tools" / "flow-dispatcher"
if str(FLOW_DIR) not in sys.path:
    sys.path.insert(0, str(FLOW_DIR))


@app.route("/api/flow/accounts")
def api_flow_accounts():
    """Lấy danh sách 5 tài khoản Google Flow và trạng thái CDP realtime."""
    try:
        from chrome_launcher import load_accounts_config, check_cdp_status, get_active_tabs
        cfg = load_accounts_config()
        accounts_data = []

        for acc in cfg.get("accounts", []):
            port = acc["port"]
            is_online, browser_name = check_cdp_status(port)
            tabs = get_active_tabs(port) if is_online else []
            flow_tab = next((t for t in tabs if "flow.google.com" in t.get("url", "")), None)
            active_tab_title = flow_tab.get("title", "Google Flow") if flow_tab else (tabs[0].get("title", "Chrome") if tabs else "None")

            accounts_data.append({
                "id": acc["id"],
                "name": acc["name"],
                "port": port,
                "is_online": is_online,
                "browser_name": browser_name,
                "active_tab_title": active_tab_title,
                "daily_credit_limit": acc.get("daily_credit_limit", 50),
                "credit_used_today": acc.get("credit_used_today", 0),
            })

        return jsonify({
            "status": "ok",
            "accounts": accounts_data,
            "default_url": cfg.get("default_flow_url", "https://flow.google.com")
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/flow/launch", methods=["POST"])
def api_flow_launch():
    """Mở cửa sổ Chrome độc lập cho 1 tài khoản."""
    data = request.json or {}
    acc_id = int(data.get("acc_id", 1))
    try:
        from chrome_launcher import launch_account
        res = launch_account(acc_id)
        return jsonify({"status": "ok", "message": f"Chrome account {acc_id} launched", "exit_code": res})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/flow/launch-all", methods=["POST"])
def api_flow_launch_all():
    """Mở đồng loạt cả 5 cửa sổ Chrome."""
    try:
        from chrome_launcher import action_start_all
        threading.Thread(target=action_start_all, daemon=True).start()
        return jsonify({"status": "ok", "message": "Launching all accounts in background"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def _execute_flow_dispatch_task(task_id, channel, slug, dry_run=False):
    """Worker chạy tiến trình dispatch Google Flow song song."""
    try:
        cmd = [sys.executable, str(FLOW_DIR / "flow_dispatcher.py"), slug, f"--channel={channel}"]
        if dry_run:
            cmd.append("--dry-run")

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        with _flow_lock:
            _flow_dispatch_tasks[task_id]["status"] = "running"
            _flow_dispatch_tasks[task_id]["pid"] = proc.pid

        for line in iter(proc.stdout.readline, ""):
            line_str = line.strip()
            if not line_str:
                continue
            with _flow_lock:
                _flow_dispatch_tasks[task_id]["logs"].append(line_str)
                _flow_dispatch_tasks[task_id]["last_log"] = line_str

        proc.wait()

        with _flow_lock:
            if proc.returncode == 0:
                _flow_dispatch_tasks[task_id]["status"] = "done"
            else:
                _flow_dispatch_tasks[task_id]["status"] = "error"
                _flow_dispatch_tasks[task_id]["error"] = f"Dispatcher exited with code {proc.returncode}"
    except Exception as e:
        with _flow_lock:
            _flow_dispatch_tasks[task_id]["status"] = "error"
            _flow_dispatch_tasks[task_id]["error"] = str(e)


@app.route("/api/flow/dispatch", methods=["POST"])
def api_flow_dispatch():
    """Kích hoạt tiến trình phân bổ prompt và cào asset từ 5 tài khoản."""
    import uuid
    data = request.json or {}
    channel = data.get("channel", "tien-thuc-chien")
    slug = data.get("slug", "thoat-bay-no-the-tin-dung")
    dry_run = bool(data.get("dry_run", False))

    task_id = str(uuid.uuid4())[:8]
    with _flow_lock:
        _flow_dispatch_tasks[task_id] = {
            "task_id": task_id,
            "channel": channel,
            "slug": slug,
            "status": "queued",
            "logs": [],
            "last_log": "Starting dispatcher...",
            "started_at": datetime.now().isoformat(),
            "error": None
        }

    thread = threading.Thread(target=_execute_flow_dispatch_task, args=(task_id, channel, slug, dry_run), daemon=True)
    thread.start()

    return jsonify({"status": "ok", "task_id": task_id, "message": "Dispatch task queued"})


@app.route("/api/flow/dispatch-status/<task_id>")
def api_flow_dispatch_status(task_id):
    """Kiểm tra tiến độ dispatch."""
    with _flow_lock:
        task = _flow_dispatch_tasks.get(task_id)
    if not task:
        return jsonify({"status": "error", "message": "Task not found"}), 404
    return jsonify(task)


@app.route("/api/system")
def api_system():
    """System & GPU info."""
    gpu = _detect_gpu()
    backend = _detect_backend()
    model = _check_model_cached()

    disk_path = "/" if sys.platform != "win32" else "C:\\"
    disk = shutil.disk_usage(disk_path)

    return jsonify({
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "gpu": gpu,
        "backend": backend,
        "model_cached": model,
        "disk": {
            "total_gb": round(disk.total / (1024**3), 1),
            "used_gb": round(disk.used / (1024**3), 1),
            "free_gb": round(disk.free / (1024**3), 1),
        },
        "docker_available": shutil.which("docker") is not None,
    })


if __name__ == "__main__":
    # Fix Windows console encoding
    if sys.platform == "win32":
        import io
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

    checker = threading.Thread(target=background_health_checker, daemon=True)
    checker.start()

    port = int(os.environ.get("PORT", 3000))
    print(f"[Studio] AI Audio Studio starting on http://0.0.0.0:{port}")
    print(f"[Studio] Platform: {platform.system()} {platform.machine()}")
    print(f"[Studio] Root: {ROOT_DIR}")
    app.run(host="0.0.0.0", port=port, debug=False)
