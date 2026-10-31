#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/generate_audio_and_timing.py — Automated TTS generation & Whisper Timing Pipeline
Generates S001_narration.wav ... S157_narration.wav and S001_timing.json ... S157_timing.json
Also stitches narration_master.wav and outputs actual timing metadata.
"""

import os
import sys
import re
import json
import wave
import time
from pathlib import Path

# Fix Windows console UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
SLUG = "lam-phat-loi-song-luong-tang-tien-mat"
CHANNEL = "tien-thuc-chien"
VIDEO_DIR = ROOT_DIR / "channels" / CHANNEL / "videos" / SLUG
AUDIO_DIR = VIDEO_DIR / "audio"
SCRIPT_FILE = VIDEO_DIR / "script.md"
FPS = 30
SAMPLE_RATE = 48000


def parse_script():
    content = SCRIPT_FILE.read_text(encoding="utf-8")
    blocks = re.split(r"##\s*Scene\s*(\d+)", content)
    scenes = []
    for i in range(1, len(blocks), 2):
        s_num = int(blocks[i])
        s_body = blocks[i+1]
        beat_m = re.search(r"-\s*Beat:\s*(.+)", s_body)
        type_m = re.search(r"-\s*Loại dự kiến:\s*(.+)", s_body)
        concept_m = re.search(r"-\s*Visual concept:\s*(.+)", s_body)
        dur_m = re.search(r"-\s*Duration ước tính:\s*(\d+)s", s_body)
        nar_m = re.search(r'-\s*Narration:\s*"([^"]+)"', s_body)

        scenes.append({
            "scene_id": f"S{s_num:03d}",
            "number": s_num,
            "beat": beat_m.group(1).strip() if beat_m else "",
            "type": type_m.group(1).strip() if type_m else "GFX",
            "concept": concept_m.group(1).strip() if concept_m else "",
            "est_duration": int(dur_m.group(1)) if dur_m else 6,
            "narration": nar_m.group(1).strip() if nar_m else ""
        })
    return scenes


def get_audio_duration_ms(wav_path: Path) -> int:
    try:
        with wave.open(str(wav_path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return int(frames / rate * 1000)
    except Exception:
        return 0


def generate_audio_and_timing():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    scenes = parse_script()
    total = len(scenes)
    print(f"🎬 Bắt đầu pipeline Audio & Timing cho {total} phân cảnh...")

    from vieneu import Vieneu
    from faster_whisper import WhisperModel

    print("🎙️ Đang khởi tạo Vieneu TTS engine (voice: Hải Đăng)...")
    vieneu = Vieneu()

    print("🔍 Đang khởi tạo Faster-Whisper model (base, int8)...")
    whisper_model = WhisperModel("base", device="cpu", compute_type="int8")

    start_all = time.time()
    for idx, s in enumerate(scenes, 1):
        sid = s["scene_id"]
        narration = s["narration"]
        wav_file = AUDIO_DIR / f"{sid}_narration.wav"
        timing_file = AUDIO_DIR / f"{sid}_timing.json"

        # 1. TTS Generation
        if not wav_file.exists() or wav_file.stat().st_size < 1000:
            t0 = time.time()
            audio = vieneu.infer(narration, voice="Hải Đăng")
            vieneu.save(audio, str(wav_file))
            t_tts = time.time() - t0
        else:
            t_tts = 0.0

        dur_ms = get_audio_duration_ms(wav_file)

        # 2. Whisper Timing
        if not timing_file.exists() or timing_file.stat().st_size < 100:
            t0 = time.time()
            segments, info = whisper_model.transcribe(str(wav_file), word_timestamps=True, language="vi")
            words = []
            for seg in segments:
                for w in seg.words:
                    words.append({
                        "word": w.word.strip(),
                        "start_ms": int(w.start * 1000),
                        "end_ms": int(w.end * 1000)
                    })
            timing_data = {
                "audio_file": wav_file.name,
                "duration_ms": dur_ms,
                "word_count": len(words),
                "model": "base",
                "engine": "faster-whisper",
                "words": words
            }
            timing_file.write_text(json.dumps(timing_data, ensure_ascii=False, indent=2), encoding="utf-8")
            t_wh = time.time() - t0
        else:
            t_wh = 0.0

        frames = int(round(dur_ms / 1000.0 * FPS))
        dur_sec = dur_ms / 1000.0
        print(f"[{idx:03d}/{total}] {sid}: {dur_sec:.2f}s ({frames}f, {dur_ms}ms) | TTS: {t_tts:.1f}s | WH: {t_wh:.1f}s")

    elapsed = time.time() - start_all
    print(f"\n🎉 Hoàn thành Audio & Timing cho {total} scenes trong {elapsed:.1f}s ({elapsed/60:.2f} phút)!")

    # 3. Create narration_master.wav
    create_master_narration(scenes)


def create_master_narration(scenes):
    master_path = AUDIO_DIR / "narration_master.wav"
    print("\n🎧 Đang ghép nối narration_master.wav chuẩn xác từng frame...")

    total_frames = 0
    scene_durations = []

    for s in scenes:
        sid = s["scene_id"]
        wav_file = AUDIO_DIR / f"{sid}_narration.wav"
        dur_ms = get_audio_duration_ms(wav_file)
        # Pad duration to whole frames (at least duration of wav + 2 frames cushion)
        frames = max(int(round(dur_ms / 1000.0 * FPS)), 1)
        # For AIV scenes, duration is fixed to est_duration * FPS
        if s["type"] == "AIV":
            frames = s["est_duration"] * FPS
        scene_durations.append((s, frames, dur_ms))
        total_frames += frames

    samples_per_frame = SAMPLE_RATE // FPS
    total_samples = total_frames * samples_per_frame
    total_bytes = total_samples * 2  # 16-bit mono = 2 bytes per sample
    master_buffer = bytearray(total_bytes)

    current_frame = 0
    for s, frames, dur_ms in scene_durations:
        sid = s["scene_id"]
        wav_file = AUDIO_DIR / f"{sid}_narration.wav"
        start_sample = current_frame * samples_per_frame
        start_byte = start_sample * 2

        if wav_file.exists():
            with wave.open(str(wav_file), "rb") as wf:
                data = wf.readframes(wf.getnframes())
                end_byte = min(start_byte + len(data), total_bytes)
                master_buffer[start_byte:end_byte] = data[:end_byte - start_byte]

        current_frame += frames

    with wave.open(str(master_path), "wb") as out_wf:
        out_wf.setnchannels(1)
        out_wf.setsampwidth(2)
        out_wf.setframerate(SAMPLE_RATE)
        out_wf.writeframes(master_buffer)

    master_dur_sec = total_frames / FPS
    print(f"✅ narration_master.wav hoàn tất: {master_dur_sec:.2f}s ({total_frames} frames, {master_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    generate_audio_and_timing()
