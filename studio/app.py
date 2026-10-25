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

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

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


def ensure_master_narration(video_dir: Path, sequences: list, fps: int = 30):
    """Ghép nối chính xác tất cả audio segments thành một file narration_master.wav duy nhất.
    Khắc phục triệt để lỗi Windows CreateProcess command-line length limit khi Remotion gọi FFmpeg với hàng chục audio inputs."""
    audio_dir = video_dir / "audio"
    if not audio_dir.exists():
        return None
    master_path = audio_dir / "narration_master.wav"

    total_frames = sum(s.get("duration_frames", 0) for s in sequences)
    if total_frames <= 0:
        return None

    sample_rate = 48000
    samples_per_frame = sample_rate // fps
    total_samples = total_frames * samples_per_frame
    total_bytes = total_samples * 2

    # Kiểm tra xem có file narration nào không
    has_wavs = any((audio_dir / f"{s.get('scene_id') or s.get('scene')}_narration.wav").exists() for s in sequences)
    if not has_wavs:
        return None

    # Nếu master file đã có và kích thước khớp, dùng luôn
    if master_path.exists() and abs(master_path.stat().st_size - (total_bytes + 44)) < 4000:
        return master_path

    try:
        import wave
        master_buffer = bytearray(total_bytes)
        for seq in sequences:
            scene = seq.get("scene_id") or seq.get("scene")
            start_frame = seq.get("from_frame", seq.get("start_frame", 0))
            start_sample = start_frame * samples_per_frame
            start_byte = start_sample * 2

            wav_path = audio_dir / f"{scene}_narration.wav"
            if wav_path.exists():
                with wave.open(str(wav_path), "rb") as w:
                    n_frames = w.getnframes()
                    frames_data = w.readframes(n_frames)
                    end_byte = min(start_byte + len(frames_data), total_bytes)
                    master_buffer[start_byte:end_byte] = frames_data[:end_byte - start_byte]

        with wave.open(str(master_path), "wb") as out_w:
            out_w.setnchannels(1)
            out_w.setsampwidth(2)
            out_w.setframerate(sample_rate)
            out_w.writeframes(master_buffer)
        return master_path
    except Exception as e:
        print(f"[MasterNarration] Lỗi tạo file master narration: {e}")
        return None


def resolve_bgm_for_channel_slug(channel: str, slug: str, base_url: str = "") -> dict:
    """Tự động resolve nhạc nền BGM (nhạc nhẹ, không lời) mặc định cho channel hoặc video."""
    prefix = base_url.rstrip("/") if base_url else ""
    channel_dir = ROOT_DIR / "channels" / channel
    ch_config_file = channel_dir / "config.json"
    ch_config = {}
    if ch_config_file.exists():
        try:
            ch_config = json.loads(ch_config_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    default_track = (
        ch_config.get("default_bgm")
        or ch_config.get("bgm", {}).get("default_track")
        or "bgm_calm_lofi.mp3"
    )
    default_vol = float(
        ch_config.get("default_bgm_volume")
        or ch_config.get("bgm", {}).get("default_volume", 0.10)
    )

    track_path = channel_dir / "bgm" / default_track
    if not track_path.exists():
        track_path = ROOT_DIR / "channels" / "_common" / "bgm" / default_track
    if not track_path.exists():
        track_path = ROOT_DIR / "studio" / "remotion" / "public" / "bgm" / default_track

    if not track_path.exists():
        bgm_folder = channel_dir / "bgm"
        if bgm_folder.exists():
            mp3s = list(bgm_folder.glob("*.mp3"))
            if mp3s:
                track_path = mp3s[0]
                default_track = track_path.name

    if track_path.exists():
        dur_s = 168.0
        try:
            out = subprocess.check_output(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(track_path)],
                text=True, timeout=5
            ).strip()
            dur_s = float(out)
        except Exception:
            pass

        return {
            "bgm_url": f"{prefix}/api/media/{channel}/bgm/{default_track}",
            "bgm_volume": default_vol,
            "bgm_duration_seconds": dur_s,
            "bgm_duration_frames": int(dur_s * 30),
        }
    return {}


def build_composition_for_channel_slug(channel, slug, base_url="http://127.0.0.1:3000"):
    """Tạo cấu trúc VideoCompositionProps hoàn chỉnh cho Remotion Player hoặc Render CLI."""
    video_dir = ROOT_DIR / "channels" / channel / "videos" / slug
    if not video_dir.exists():
        return None

    prefix = base_url.rstrip("/") if base_url else ""
    comp_file = video_dir / "assets" / "remotion-composition.json"
    if comp_file.exists():
        try:
            data = json.loads(comp_file.read_text(encoding="utf-8"))
            # Lấy lời thoại chuẩn từ broll-plan nếu có
            scene_narrations = {}
            broll_file = video_dir / "broll-plan.json"
            if broll_file.exists():
                try:
                    b_data = json.loads(broll_file.read_text(encoding="utf-8"))
                    b_scenes = b_data.get("scenes", []) if isinstance(b_data, dict) else b_data
                    for sc in b_scenes:
                        sid = sc.get("scene_id") or sc.get("scene")
                        if sid and sc.get("narration"):
                            scene_narrations[sid] = sc.get("narration")
                except Exception:
                    pass

            # Tự động map từ visual_sequences nếu thiếu sequences phẳng
            if "sequences" not in data and "tracks" in data and "visual_sequences" in data["tracks"]:
                sequences = []
                fps = data.get("fps", 30)
                for item in data["tracks"]["visual_sequences"]:
                    scene = item.get("scene_id") or item.get("scene", "")
                    seq_id = item.get("id", "")
                    seq_type = item.get("type", "IMG")
                    start_f = item.get("from_frame", 0)
                    dur_f = item.get("duration_frames", 0)
                    dur_s = item.get("duration_seconds", dur_f / fps if fps else 0)
                    desc = item.get("description", "")
                    props = item.get("props", {}) or {}
                    src = props.get("src")

                    # Thiết lập thông tin props phong phú cho GFX
                    if seq_type == "GFX":
                        if not props.get("title"):
                            props["title"] = desc
                        comp_name = item.get("component")
                        if comp_name == "CounterNumber" and "to" not in props:
                            if "35%" in desc:
                                props["label"] = "Lãi Suất Thẻ Tín Dụng"
                                props["to"] = 35
                                props["suffix"] = "% / Năm"
                            elif "1.160.000" in desc:
                                props["label"] = "Tiền Lãi Bốc Hơi Mỗi Tháng"
                                props["to"] = 1160000
                                props["suffix"] = " VNĐ"
                            elif "60 triệu" in desc:
                                props["label"] = "Dư Nợ Tăng Vọt (Người A)"
                                props["to"] = 60000000
                                props["suffix"] = " VNĐ"
                            elif "14.000.000" in desc or "1.000.000" in desc:
                                props["label"] = "Thanh Toán Tối Thiểu"
                                props["to"] = 1000000
                                props["suffix"] = " VNĐ"

                    seq = {
                        "id": seq_id,
                        "scene": scene,
                        "beat": desc,
                        "narration_text": scene_narrations.get(scene, desc),
                        "type": seq_type,
                        "start_frame": start_f,
                        "duration_frames": dur_f,
                        "duration_seconds": dur_s,
                        "component": item.get("component"),
                        "gfx_component": item.get("component") if seq_type == "GFX" else None,
                        "gfx_props": props,
                    }
                    if src:
                        seq["asset_path"] = f"{prefix}/api/media/{channel}/{slug}/{src.lstrip('/')}"
                    sequences.append(seq)
                data["sequences"] = sequences

            # Chuẩn hóa URLs để phục vụ qua static API hoặc Remotion Headless Chromium
            for seq in data.get("sequences", []):
                scene = seq.get("scene", "")
                seq_id = seq.get("id", "")
                # Narration audio
                audio_file = video_dir / "audio" / f"{scene}_narration.wav"
                if audio_file.exists():
                    seq["narration_audio_url"] = f"{prefix}/api/media/{channel}/{slug}/audio/{scene}_narration.wav"

                # Word timings chuẩn xác từ timing JSON
                timing_file = video_dir / "audio" / f"{scene}_timing.json"
                if timing_file.exists():
                    try:
                        t_data = json.loads(timing_file.read_text(encoding="utf-8"))
                        seq["words"] = t_data.get("words", [])
                    except Exception:
                        pass
                if scene in scene_narrations:
                    seq["narration_text"] = scene_narrations[scene]

                # Asset path fallback nếu chưa có
                if not seq.get("asset_path"):
                    assets_dir = video_dir / "assets"
                    matched_asset = None
                    for ext in [".mp4", ".png", ".jpg", ".webp"]:
                        candidate = assets_dir / f"{seq_id}{ext}"
                        if candidate.exists():
                            matched_asset = f"{prefix}/api/media/{channel}/{slug}/assets/{seq_id}{ext}"
                            break
                        candidate_scene = assets_dir / f"{scene}_{seq.get('type', 'IMG')}{ext}"
                        if candidate_scene.exists():
                            matched_asset = f"{prefix}/api/media/{channel}/{slug}/assets/{candidate_scene.name}"
                            break
                    if matched_asset:
                        seq["asset_path"] = matched_asset

            # Đảm bảo tổng số frames và duration chính xác
            total_f = sum(s.get("duration_frames", 0) for s in data.get("sequences", []))
            data["total_frames"] = total_f
            data["total_duration_seconds"] = total_f / data.get("fps", 30) if data.get("fps", 30) else 0

            # Master audio track ghép chính xác timing các cảnh (tránh lỗi Windows CLI limit khi FFmpeg mux 81 wavs)
            master_file = ensure_master_narration(video_dir, data.get("sequences", []), data.get("fps", 30))
            if master_file and master_file.exists():
                data["master_audio_url"] = f"{prefix}/api/media/{channel}/{slug}/audio/narration_master.wav"

            # Tự động gán BGM mặc định cho channel nếu video chưa có cấu hình riêng
            if not data.get("bgm_url"):
                bgm_info = resolve_bgm_for_channel_slug(channel, slug, base_url=base_url)
                if bgm_info:
                    data.update(bgm_info)

            return data
        except Exception as e:
            print(f"Error parsing remotion-composition.json: {e}")
            return None

    # Fallback nếu chưa có file remotion-composition.json nhưng có broll-plan
    broll_file = video_dir / "broll-plan.json"
    if broll_file.exists():
        try:
            broll_data = json.loads(broll_file.read_text(encoding="utf-8"))
            scenes = broll_data.get("scenes", []) if isinstance(broll_data, dict) else broll_data
            sequences = []
            fps = 30
            current_frame = 0
            for item in scenes:
                dur_s = item.get("duration_seconds", 4)
                dur_f = int(dur_s * fps)
                scene = item.get("scene_id") or item.get("scene", "S001")
                brolls = item.get("brolls", [])
                if brolls:
                    for b in brolls:
                        b_dur_s = b.get("duration_s", 4)
                        b_dur_f = int(b_dur_s * fps)
                        seq_id = b.get("broll_id", f"{scene}-A")
                        seq_type = b.get("type", "IMG")
                        seq = {
                            "id": seq_id,
                            "scene": scene,
                            "beat": b.get("description", "Scene Beat"),
                            "type": seq_type,
                            "duration_seconds": b_dur_s,
                            "duration_frames": b_dur_f,
                            "start_frame": current_frame,
                            "motion_effect": "ken_burns_zoom_in" if seq_type == "IMG" else "static",
                            "narration_text": item.get("narration", ""),
                        }
                        audio_file = video_dir / "audio" / f"{scene}_narration.wav"
                        if audio_file.exists():
                            seq["narration_audio_url"] = f"{prefix}/api/media/{channel}/{slug}/audio/{scene}_narration.wav"
                        timing_file = video_dir / "audio" / f"{scene}_timing.json"
                        if timing_file.exists():
                            try:
                                t_data = json.loads(timing_file.read_text(encoding="utf-8"))
                                seq["words"] = t_data.get("words", [])
                            except Exception:
                                pass
                        sequences.append(seq)
                        current_frame += b_dur_f
                else:
                    seq = {
                        "id": f"{scene}-A",
                        "scene": scene,
                        "beat": item.get("description", "Scene Beat"),
                        "type": "IMG",
                        "duration_seconds": dur_s,
                        "duration_frames": dur_f,
                        "start_frame": current_frame,
                        "motion_effect": "ken_burns_zoom_in",
                        "narration_text": item.get("narration", ""),
                    }
                    sequences.append(seq)
                    current_frame += dur_f

            total_s = current_frame / fps
            master_file = ensure_master_narration(video_dir, sequences, fps)
            master_audio_url = f"{prefix}/api/media/{channel}/{slug}/audio/narration_master.wav" if master_file and master_file.exists() else None
            bgm_info = resolve_bgm_for_channel_slug(channel, slug, base_url=base_url)
            ret = {
                "title": slug,
                "slug": slug,
                "channel": channel,
                "fps": fps,
                "width": 1920,
                "height": 1080,
                "total_duration_seconds": total_s,
                "total_frames": current_frame,
                "master_audio_url": master_audio_url,
                "sequences": sequences,
            }
            if bgm_info:
                ret.update(bgm_info)
            return ret
        except Exception as e:
            print(f"Error parsing broll plan: {e}")
            return None
    return None


@app.route("/api/media/<channel>/bgm/<path:filepath>")
def api_channel_bgm(channel, filepath):
    """Phục vụ file nhạc nền BGM của channel hoặc fallback chung."""
    bgm_path = ROOT_DIR / "channels" / channel / "bgm" / filepath
    if bgm_path.exists():
        return send_from_directory(str(bgm_path.parent), bgm_path.name)
    common_path = ROOT_DIR / "channels" / "_common" / "bgm" / filepath
    if common_path.exists():
        return send_from_directory(str(common_path.parent), common_path.name)
    remotion_public = ROOT_DIR / "studio" / "remotion" / "public" / "bgm" / filepath
    if remotion_public.exists():
        return send_from_directory(str(remotion_public.parent), remotion_public.name)
    return jsonify({"status": "error", "message": "BGM file not found"}), 404


@app.route("/api/video-data/<channel>/<slug>")
def api_video_data(channel, slug):
    """Lấy dữ liệu composition và sequences cho Remotion Player."""
    data = build_composition_for_channel_slug(channel, slug, base_url="")
    if data:
        return jsonify({"status": "ok", "composition": data})
    return jsonify({"status": "error", "message": "Composition not found"}), 404


@app.route("/api/media/<channel>/<slug>/<path:filepath>")
def api_media(channel, slug, filepath):
    """Phục vụ an toàn các file media từ thư mục video."""
    video_dir = ROOT_DIR / "channels" / channel / "videos" / slug
    full_path = video_dir / filepath
    if not full_path.exists():
        return jsonify({"status": "error", "message": "File not found"}), 404
    return send_from_directory(str(full_path.parent), full_path.name)


def _execute_render_task(task_id, channel, slug, fps=30):
    """Worker chạy tiến trình render Remotion ngầm không bị kẹt tiến trình."""
    import re
    import uuid

    video_dir = ROOT_DIR / "channels" / channel / "videos" / slug
    remotion_dir = ROOT_DIR / "studio" / "remotion"
    output_file = video_dir / "final_video.mp4"

    try:
        # Lấy composition data đầy đủ với full HTTP URLs cho Remotion Headless Chromium
        comp_data = build_composition_for_channel_slug(channel, slug, base_url="http://127.0.0.1:3000")
        if not comp_data:
            raise FileNotFoundError(f"Không thể khởi tạo composition data cho {channel}/{slug}")

        # Tạo file props tạm thời
        temp_props_file = remotion_dir / f"temp_props_{task_id}.json"
        temp_props_file.write_text(json.dumps(comp_data, ensure_ascii=False), encoding="utf-8")

        temp_out_name = f"render_out_{task_id}.mp4"
        temp_out_file = remotion_dir / temp_out_name

        cmd = [
            "npx", "remotion", "render",
            "src/index.ts", "MainVideo",
            temp_out_name,
            f"--props={temp_props_file.name}",
            "--overwrite",
            "--gl=angle",
            "--concurrency=4"
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
            _render_tasks[task_id]["progress"] = 1
            _render_tasks[task_id]["log_line"] = "Bắt đầu bundling và render video qua Remotion..."

        # Đọc tiến độ với stream chunking (tách cả \r và \n) để không bị treo ở Bundling %
        progress_pattern = re.compile(r"Rendered\s+(\d+)/(\d+)")
        encoded_pattern = re.compile(r"Encoded\s+(\d+)/(\d+)")
        percent_pattern = re.compile(r"(\d+)%")

        buf = ""
        recent_logs = []
        while True:
            chunk = proc.stdout.read(64)
            if not chunk:
                break
            buf += chunk
            while "\r" in buf or "\n" in buf:
                idx_r = buf.find("\r")
                idx_n = buf.find("\n")
                if idx_r != -1 and idx_n != -1:
                    idx = min(idx_r, idx_n)
                elif idx_r != -1:
                    idx = idx_r
                else:
                    idx = idx_n
                line_str = buf[:idx].strip()
                buf = buf[idx + 1:]
                if not line_str:
                    continue

                recent_logs.append(line_str)
                if len(recent_logs) > 20:
                    recent_logs.pop(0)

                prog_match = progress_pattern.search(line_str)
                if prog_match:
                    curr, total = int(prog_match.group(1)), int(prog_match.group(2))
                    if total > 0:
                        pct = min(100, int((curr / total) * 100))
                        with _render_lock:
                            _render_tasks[task_id]["progress"] = pct
                            _render_tasks[task_id]["log_line"] = f"Rendered {curr}/{total} frames ({pct}%)"
                    continue

                enc_match = encoded_pattern.search(line_str)
                if enc_match:
                    curr, total = int(enc_match.group(1)), int(enc_match.group(2))
                    with _render_lock:
                        _render_tasks[task_id]["progress"] = 99
                        _render_tasks[task_id]["log_line"] = f"Đang encode MP4: {curr}/{total} frames"
                    continue

                pct_match = percent_pattern.search(line_str)
                if pct_match:
                    p_val = int(pct_match.group(1))
                    with _render_lock:
                        if "bundl" in line_str.lower():
                            _render_tasks[task_id]["progress"] = min(15, max(1, int(p_val * 0.15)))
                            _render_tasks[task_id]["log_line"] = f"Bundling Remotion ({p_val}%)..."
                        else:
                            _render_tasks[task_id]["log_line"] = line_str

        proc.wait()

        # Dọn dẹp file tạm
        if temp_props_file.exists():
            try:
                temp_props_file.unlink()
            except Exception:
                pass

        if proc.returncode == 0 and temp_out_file.exists():
            shutil.copy2(temp_out_file, output_file)
            try:
                temp_out_file.unlink()
            except Exception:
                pass
            with _render_lock:
                _render_tasks[task_id]["status"] = "done"
                _render_tasks[task_id]["progress"] = 100
                _render_tasks[task_id]["video_url"] = f"/api/media/{channel}/{slug}/final_video.mp4"
                _render_tasks[task_id]["finished_at"] = datetime.now().isoformat()
        else:
            err_details = " | ".join(recent_logs[-5:]) if recent_logs else "No log output"
            with _render_lock:
                _render_tasks[task_id]["status"] = "error"
                _render_tasks[task_id]["error"] = f"Remotion render failed with exit code {proc.returncode}. {err_details}"
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


@app.route("/api/sync-remotion-props", methods=["POST"])
def api_sync_remotion_props():
    """Đồng bộ props của video hiện tại sang studio/remotion/current_props.json cho Remotion Studio Timeline."""
    data = request.json or {}
    channel = data.get("channel")
    slug = data.get("slug")
    if not channel or not slug:
        return jsonify({"status": "error", "message": "Missing channel or slug"}), 400

    comp_data = build_composition_for_channel_slug(channel, slug, base_url="http://127.0.0.1:3000")
    if not comp_data:
        return jsonify({"status": "error", "message": "Composition not found"}), 404

    remotion_dir = ROOT_DIR / "studio" / "remotion"
    (remotion_dir / "current_props.json").write_text(json.dumps(comp_data, ensure_ascii=False), encoding="utf-8")
    return jsonify({"status": "ok", "message": "Props synced for Remotion Studio Timeline", "sequences_count": len(comp_data.get("sequences", []))})


# --- Google Flow Multi-Account Browser Pool & Dispatcher Integration ---
_flow_dispatch_tasks = {}
_flow_lock = threading.Lock()

# Add tools/flow-dispatcher to sys.path
FLOW_DIR = ROOT_DIR / "tools" / "flow-dispatcher"
if str(FLOW_DIR) not in sys.path:
    sys.path.insert(0, str(FLOW_DIR))


@app.route("/api/browser/accounts", methods=["GET"])
@app.route("/api/flow/accounts", methods=["GET"])
def api_browser_accounts():
    """Lấy danh sách 5 tài khoản Google Flow và trạng thái CDP realtime."""
    try:
        from browser_pool import get_accounts, load_accounts_config
        cfg = load_accounts_config()
        accounts_data = get_accounts()
        return jsonify({
            "status": "ok",
            "accounts": accounts_data,
            "default_url": cfg.get("default_flow_url", "https://flow.google.com"),
            "default_project_url": cfg.get("default_project_url", "")
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/browser/accounts/launch", methods=["POST"])
@app.route("/api/flow/launch", methods=["POST"])
def api_browser_launch():
    """Mở cửa sổ Chrome độc lập cho 1 tài khoản (hoặc mở tất cả nếu không truyền acc_id)."""
    data = request.json or {}
    acc_id = data.get("account_id") or data.get("acc_id")
    project_url = data.get("project_url")

    try:
        from browser_pool import launch_account, launch_all
        if acc_id is not None and str(acc_id).strip() != "":
            ok, msg = launch_account(int(acc_id), project_url=project_url)
            return jsonify({"status": "ok" if ok else "error", "message": msg, "account_id": int(acc_id)})
        else:
            res = launch_all(project_url=project_url)
            return jsonify({"status": "ok", "message": "All accounts launched", "results": res})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/browser/accounts/close", methods=["POST"])
@app.route("/api/flow/close", methods=["POST"])
def api_browser_close():
    """Đóng Chrome an toàn qua CDP Browser.close (không kill port cứng, chống popup Restore)."""
    data = request.json or {}
    acc_id = data.get("account_id") or data.get("acc_id")

    try:
        from browser_pool import close_account, close_all
        if acc_id is not None and str(acc_id).strip() != "":
            ok, msg = close_account(int(acc_id))
            return jsonify({"status": "ok" if ok else "error", "message": msg, "account_id": int(acc_id)})
        else:
            res = close_all()
            return jsonify({"status": "ok", "message": "All accounts closed safely", "results": res})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/browser/accounts/update-project", methods=["POST"])
def api_browser_update_project():
    """Cập nhật Google Flow Project URL cho tài khoản hoặc mặc định."""
    data = request.json or {}
    acc_id = data.get("account_id") or data.get("acc_id")
    project_url = (data.get("project_url") or "").strip()

    try:
        from browser_pool import load_accounts_config, save_accounts_config
        cfg = load_accounts_config()
        if acc_id is not None and str(acc_id).strip() != "":
            acc = next((a for a in cfg["accounts"] if a["id"] == int(acc_id)), None)
            if acc:
                acc["project_url"] = project_url
        else:
            cfg["default_project_url"] = project_url
            for a in cfg["accounts"]:
                if not a.get("project_url"):
                    a["project_url"] = project_url

        save_accounts_config(cfg)
        return jsonify({"status": "ok", "message": "Project URL updated successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/flow/launch-all", methods=["POST"])
def api_flow_launch_all():
    """Alias mở đồng loạt 5 cửa sổ Chrome."""
    try:
        from browser_pool import launch_all
        threading.Thread(target=launch_all, daemon=True).start()
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
