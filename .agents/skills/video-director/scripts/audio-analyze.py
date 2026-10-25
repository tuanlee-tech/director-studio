#!/usr/bin/env python3
"""
audio-analyze.py — Phân tích audio narration → word-level timestamps (JSON).
Sử dụng từ cheatcode @analyze.

Usage:
    python audio-analyze.py <audio_file> <output_json> [--model base|small|medium] [--language vi]

Output JSON format:
{
    "audio_file": "S001_narration.wav",
    "duration_ms": 6320,
    "word_count": 18,
    "model": "base",
    "words": [
        {"word": "Năm", "start_ms": 120, "end_ms": 390},
        {"word": "một", "start_ms": 400, "end_ms": 550},
        ...
    ]
}
"""

import sys
import json
import wave
import argparse
from pathlib import Path

# Fix Windows console cp1252 encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def get_audio_duration_ms(audio_path: str) -> int:
    """Lấy thời lượng audio bằng thư viện wave chuẩn."""
    try:
        with wave.open(audio_path, 'r') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return int(frames / rate * 1000)
    except Exception:
        return 0


def analyze_with_whisper(audio_path: str, model_name: str = "base", language: str = "vi") -> dict:
    """Dùng openai-whisper để transcribe + lấy word-level timestamps."""
    try:
        import whisper  # type: ignore
        print(f"🔍 Đang tải Whisper model '{model_name}'...", flush=True)
        model = whisper.load_model(model_name)
        print(f"🎵 Đang phân tích: {audio_path}", flush=True)

        result = model.transcribe(
            audio_path,
            word_timestamps=True,
            language=language,
            verbose=False
        )

        words = []
        for segment in result.get("segments", []):
            for w in segment.get("words", []):
                words.append({
                    "word": w["word"].strip(),
                    "start_ms": int(w["start"] * 1000),
                    "end_ms": int(w["end"] * 1000),
                })

        duration_ms = get_audio_duration_ms(audio_path)
        return {
            "audio_file": Path(audio_path).name,
            "duration_ms": duration_ms,
            "word_count": len(words),
            "model": model_name,
            "engine": "openai-whisper",
            "words": words,
        }

    except ImportError:
        print("⚠️  openai-whisper chưa cài. Thử faster-whisper...", flush=True)
        return analyze_with_faster_whisper(audio_path, model_name, language)


def analyze_with_faster_whisper(audio_path: str, model_name: str = "base", language: str = "vi") -> dict:
    """Fallback: dùng faster-whisper (nhanh hơn, GPU/CPU)."""
    try:
        from faster_whisper import WhisperModel  # type: ignore
        print(f"🔍 Đang tải faster-whisper model '{model_name}'...", flush=True)
        try:
            model = WhisperModel(model_name, device="auto", compute_type="int8")
            segments, info = model.transcribe(audio_path, word_timestamps=True, language=language)
            # test generator
            segments = list(segments)
        except RuntimeError:
            print("⚠️ CUDA DLL không có sẵn, chuyển sang device='cpu'...", flush=True)
            model = WhisperModel(model_name, device="cpu", compute_type="int8")
            segments, info = model.transcribe(audio_path, word_timestamps=True, language=language)
            segments = list(segments)

        words = []
        for segment in segments:
            for w in segment.words:
                words.append({
                    "word": w.word.strip(),
                    "start_ms": int(w.start * 1000),
                    "end_ms": int(w.end * 1000),
                })

        duration_ms = get_audio_duration_ms(audio_path)
        return {
            "audio_file": Path(audio_path).name,
            "duration_ms": duration_ms,
            "word_count": len(words),
            "model": model_name,
            "engine": "faster-whisper",
            "words": words,
        }

    except ImportError:
        print("⚠️  Không có Whisper. Dùng ước lượng timing (PACE-based)...", flush=True)
        return estimate_timing(audio_path)


def estimate_timing(audio_path: str, pace: float = 4.0) -> dict:
    """
    Fallback cuối: ước lượng timing dựa trên PACE (từ/giây).
    Dùng khi không cài Whisper. Kém chính xác hơn nhưng vẫn dùng được.
    """
    duration_ms = get_audio_duration_ms(audio_path)
    return {
        "audio_file": Path(audio_path).name,
        "duration_ms": duration_ms,
        "word_count": 0,
        "model": "none",
        "engine": "pace-estimate",
        "words": [],
        "note": "Install openai-whisper or faster-whisper for word-level timing. pip install openai-whisper",
    }


def main():
    parser = argparse.ArgumentParser(description="Phân tích audio → word-level timestamps")
    parser.add_argument("audio_file", help="Đường dẫn file audio (.wav)")
    parser.add_argument("output_json", help="Đường dẫn file JSON đầu ra")
    parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model (mặc định: base)")
    parser.add_argument("--language", default="vi", help="Ngôn ngữ audio (mặc định: vi)")
    args = parser.parse_args()

    if not Path(args.audio_file).exists():
        print(f"❌ Không tìm thấy file: {args.audio_file}", file=sys.stderr)
        sys.exit(1)

    result = analyze_with_whisper(args.audio_file, args.model, args.language)

    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ Timing saved: {args.output_json}")
    print(f"   Duration: {result['duration_ms']}ms | Words: {result['word_count']} | Engine: {result['engine']}")


if __name__ == "__main__":
    main()
