#!/usr/bin/env bash
# tts-generate.sh — Tạo TTS audio qua VieNeu-TTS API (Linux/Mac)
# Usage: ./tts-generate.sh -t "Nội dung" -voice "Hải Đăng" -scene 1 -video-dir "channels/ch/videos/vid"
# Sử dụng từ cheatcode @gen-audio

set -euo pipefail

# --- Defaults ---
TEXT=""
VOICE="Hải Đăng"
OUTPUT=""
API_URL="http://localhost:8000"
SCENE=0
VIDEO_DIR=""

# --- Parse args ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        -t|--text)        TEXT="$2";      shift 2 ;;
        -voice|--voice)   VOICE="$2";     shift 2 ;;
        -o|--output)      OUTPUT="$2";    shift 2 ;;
        -api|--api-url)   API_URL="$2";   shift 2 ;;
        -scene|--scene)   SCENE="$2";     shift 2 ;;
        -video-dir)       VIDEO_DIR="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; exit 1 ;;
    esac
done

if [[ -z "$TEXT" ]]; then
    echo "❌ Thiếu -t <text>"
    exit 1
fi

# --- Resolve output path ---
if [[ -z "$OUTPUT" ]]; then
    if [[ "$SCENE" -gt 0 && -n "$VIDEO_DIR" ]]; then
        SCENE_STR=$(printf "%03d" "$SCENE")
        AUDIO_DIR="${VIDEO_DIR}/audio"
        mkdir -p "$AUDIO_DIR"
        OUTPUT="${AUDIO_DIR}/S${SCENE_STR}_narration.wav"
    else
        echo "❌ Cần -o <output> hoặc cả -scene và -video-dir"
        exit 1
    fi
fi

# --- Health check ---
echo "🔍 Kiểm tra VieNeu-TTS tại $API_URL ..."
if ! curl -sf "$API_URL/health" > /dev/null 2>&1; then
    echo "❌ VieNeu-TTS không chạy tại $API_URL"
    echo "   → Hãy chạy: ./launcher.sh start"
    exit 1
fi
echo "✅ VieNeu-TTS đang online."

# --- Gọi TTS API ---
echo "🎙️  Đang tạo audio | Voice: $VOICE | Chars: ${#TEXT}"
HTTP_CODE=$(curl -s -o "$OUTPUT" -w "%{http_code}" \
    -X POST "$API_URL/v1/audio/speech" \
    -H "Content-Type: application/json; charset=utf-8" \
    -d "{\"model\":\"vieneu-tts-v3-turbo\",\"input\":$(printf '%s' "$TEXT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),\"voice\":\"$VOICE\",\"response_format\":\"wav\"}")

if [[ "$HTTP_CODE" == "200" ]]; then
    SIZE=$(du -k "$OUTPUT" | cut -f1)
    echo "✅ Audio saved: $OUTPUT (${SIZE} KB)"
else
    echo "❌ API trả về HTTP $HTTP_CODE"
    rm -f "$OUTPUT"
    exit 1
fi
