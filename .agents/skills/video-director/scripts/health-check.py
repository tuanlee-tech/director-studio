#!/usr/bin/env python3
"""
health-check.py — Kiểm tra trạng thái tất cả services của Video Director.
Sử dụng từ cheatcode @health.

Usage:
    python health-check.py [--api-url http://localhost:8000] [--studio-url http://localhost:3000] [--json]
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
import platform
from pathlib import Path

# Fix Windows console cp1252 encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def check_http(url: str, timeout: int = 5) -> tuple[bool, str]:
    """Kiểm tra HTTP endpoint. Trả về (ok, message)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "health-check/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return True, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, str(e.reason)
    except Exception as e:
        return False, str(e)


def check_whisper() -> tuple[bool, str]:
    """Kiểm tra Whisper đã cài chưa."""
    try:
        import whisper  # type: ignore
        return True, "openai-whisper (sẵn sàng)"
    except ImportError:
        pass
    try:
        from faster_whisper import WhisperModel  # type: ignore
        return True, "faster-whisper (sẵn sàng)"
    except ImportError:
        return False, "Chưa cài — pip install openai-whisper hoặc faster-whisper"


def check_model_cache() -> tuple[bool, str]:
    """Kiểm tra HuggingFace model cache."""
    hf_cache = Path.home() / ".cache" / "huggingface" / "hub"
    if not hf_cache.exists():
        return False, "Thư mục cache chưa tạo"
    models = list(hf_cache.glob("models--pnnbao-ump--VieNeu*"))
    if models:
        return True, f"Tìm thấy: {models[0].name}"
    return False, "VieNeu-TTS model chưa tải vào cache"


def print_status(label: str, ok: bool, msg: str):
    icon = "✅" if ok else "❌"
    color_ok = "\033[32m" if ok else "\033[31m"
    reset = "\033[0m"
    if sys.stdout.isatty():
        print(f"  {icon} {color_ok}{label:<30}{reset} {msg}")
    else:
        print(f"  {icon} {label:<30} {msg}")


def main():
    parser = argparse.ArgumentParser(description="Kiểm tra trạng thái Video Director services")
    parser.add_argument("--api-url", default="http://localhost:8000")
    parser.add_argument("--studio-url", default="http://localhost:3000")
    parser.add_argument("--tts-ui-url", default="http://localhost:7860")
    parser.add_argument("--json", action="store_true", help="Output dạng JSON")
    args = parser.parse_args()

    results = {}

    if not args.json:
        print(f"\n🏥 Video Director — Health Check")
        print(f"   Hệ điều hành: {platform.system()} {platform.machine()}")
        print(f"   Python: {platform.python_version()}\n")

    # 1. VieNeu-TTS API
    ok, msg = check_http(f"{args.api_url}/health")
    results["vieneu_api"] = {"ok": ok, "url": args.api_url, "msg": msg}
    if not args.json:
        print_status(f"VieNeu-TTS API ({args.api_url})", ok, msg)

    # 2. VieNeu-TTS Web UI
    ok, msg = check_http(args.tts_ui_url)
    results["vieneu_ui"] = {"ok": ok, "url": args.tts_ui_url, "msg": msg}
    if not args.json:
        print_status(f"VieNeu-TTS UI ({args.tts_ui_url})", ok, msg)

    # 3. Studio Dashboard
    ok, msg = check_http(f"{args.studio_url}/api/health")
    results["studio"] = {"ok": ok, "url": args.studio_url, "msg": msg}
    if not args.json:
        print_status(f"Studio Dashboard ({args.studio_url})", ok, msg)

    # 4. Whisper STT
    ok, msg = check_whisper()
    results["whisper"] = {"ok": ok, "msg": msg}
    if not args.json:
        print_status("Whisper (timing analysis)", ok, msg)

    # 5. VieNeu Model Cache
    ok, msg = check_model_cache()
    results["model_cache"] = {"ok": ok, "msg": msg}
    if not args.json:
        print_status("VieNeu-TTS Model Cache", ok, msg)

    all_critical_ok = results["vieneu_api"]["ok"] and results["whisper"]["ok"]

    if args.json:
        results["all_critical_ok"] = all_critical_ok
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print()
        if all_critical_ok:
            print("🚀 Hệ thống hoàn toàn sẵn sàng để tạo video Audio-First!")
        else:
            print("💡 Hướng dẫn chuẩn bị:")
            if not results["vieneu_api"]["ok"]:
                print("   → Chạy '@start-tts' hoặc '.\\launcher.ps1 start' để bật VieNeu-TTS.")
            if not results["whisper"]["ok"]:
                print("   → Cài Whisper: pip install openai-whisper (hoặc pip install faster-whisper).")
        print()

    sys.exit(0 if all_critical_ok else 1)


if __name__ == "__main__":
    main()
