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
