#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# AI Audio Platform - Smart Launcher (Linux/macOS)
# Native-first: runs with Python/uv; Docker optional
# ============================================================

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TTS_DIR="$ROOT_DIR/VieNeu-TTS"
STUDIO_DIR="$ROOT_DIR/studio"
ACTION="${1:-start}"
PIDFILE_TTS="$ROOT_DIR/.tts.pid"
PIDFILE_STUDIO="$ROOT_DIR/.studio.pid"

G='\033[0;32m'; Y='\033[1;33m'; R='\033[0;31m'; C='\033[0;36m'; X='\033[0m'

ok()   { echo -e "${G}[OK]${X} $1"; }
warn() { echo -e "${Y}[WARN]${X} $1"; }
err()  { echo -e "${R}[ERROR]${X} $1"; }
info() { echo -e "${C}[INFO]${X} $1"; }

echo ""
echo -e "${C}========================================${X}"
echo -e "${C}  AI Audio Platform - Smart Launcher${X}"
echo -e "${C}========================================${X}"
echo ""

# --- Detect Environment ---
detect_gpu() {
    HAS_GPU=false
    GPU_NAME="None"
    VRAM_MB=0
    if command -v nvidia-smi &>/dev/null; then
        GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -n1 || echo "")
        if [[ -n "$GPU_NAME" ]]; then
            HAS_GPU=true
            VRAM_MB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -n1 || echo "0")
        fi
    fi
}

detect_backend() {
    local venv_python="$TTS_DIR/.venv/bin/python"
    BACKEND="unknown"
    if [[ -f "$venv_python" ]]; then
        BACKEND=$($venv_python -c "
try:
    import torch
    print('pytorch-cuda' if torch.cuda.is_available() else 'pytorch-cpu')
except ImportError:
    import onnxruntime as ort
    eps = ort.get_available_providers()
    print('onnx-cuda' if 'CUDAExecutionProvider' in eps else 'onnx-cpu')
" 2>/dev/null || echo "onnx-cpu")
    fi
}

# --- Install ---
do_install() {
    info "Setting up AI Audio Platform..."

    # Python check
    if ! command -v python3 &>/dev/null; then
        err "Python 3 not found. Install:"
        echo "  Ubuntu: sudo apt install python3 python3-venv python3-pip"
        exit 1
    fi

    # uv check/install
    if ! command -v uv &>/dev/null; then
        warn "uv not found. Installing..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
    fi

    # VieNeu-TTS
    info "Setting up VieNeu-TTS..."
    cd "$TTS_DIR"
    uv sync
    ok "VieNeu-TTS dependencies installed"

    # Studio
    info "Setting up Studio UI..."
    if [[ ! -d "$STUDIO_DIR/venv" ]]; then
        python3 -m venv "$STUDIO_DIR/venv"
    fi
    "$STUDIO_DIR/venv/bin/pip" install -q flask requests
    ok "Studio UI dependencies installed"

    # .env
    if [[ ! -f "$ROOT_DIR/.env" ]] && [[ -f "$ROOT_DIR/.env.example" ]]; then
        cp "$ROOT_DIR/.env.example" "$ROOT_DIR/.env"
        info "Created .env from .env.example"
    fi

    ok "Installation complete!"
}

# --- Start ---
do_start() {
    detect_gpu
    detect_backend

    echo -e "${C}Environment:${X}"
    echo "  GPU:       $(if $HAS_GPU; then echo "$GPU_NAME (${VRAM_MB}MB)"; else echo "None"; fi)"
    echo "  Backend:   $BACKEND"
    echo ""

    # Start TTS
    if curl -s --max-time 3 http://127.0.0.1:7860/ &>/dev/null; then
        ok "VieNeu TTS already running at http://localhost:7860"
    else
        local venv_python="$TTS_DIR/.venv/bin/python"
        if [[ ! -f "$venv_python" ]]; then
            err "VieNeu-TTS venv not found. Run: ./launcher.sh install"
            exit 1
        fi

        info "Starting VieNeu TTS on http://localhost:7860 ..."
        cd "$TTS_DIR"
        nohup "$venv_python" apps/gradio_main.py > vieneu-web.stdout.log 2> vieneu-web.stderr.log &
        echo $! > "$PIDFILE_TTS"
        info "TTS started (PID: $(cat "$PIDFILE_TTS")), waiting..."

        for i in $(seq 1 60); do
            if curl -s --max-time 3 http://127.0.0.1:7860/ &>/dev/null; then
                ok "VieNeu TTS ready at http://localhost:7860"
                break
            fi
            sleep 2
            printf "\r  Waiting %ds..." $((i*2))
        done
        echo ""
    fi

    # Start Studio
    if curl -s --max-time 3 http://127.0.0.1:3000/api/health &>/dev/null; then
        ok "Studio already running at http://localhost:3000"
    else
        local studio_python="$STUDIO_DIR/venv/bin/python"
        if [[ ! -f "$studio_python" ]]; then
            warn "Studio venv not found. Installing..."
            python3 -m venv "$STUDIO_DIR/venv"
            "$STUDIO_DIR/venv/bin/pip" install -q flask requests
        fi

        info "Starting Studio UI on http://localhost:3000 ..."
        cd "$STUDIO_DIR"
        VIENEU_TTS_URL=http://localhost:7860 PORT=3000 \
            nohup "$studio_python" app.py > studio.log 2> studio.err.log &
        echo $! > "$PIDFILE_STUDIO"
        sleep 3

        if curl -s --max-time 3 http://127.0.0.1:3000/api/health &>/dev/null; then
            ok "Studio ready at http://localhost:3000"
        else
            warn "Studio starting... check $STUDIO_DIR/studio.err.log"
        fi
    fi

    echo ""
    echo -e "${G}========================================${X}"
    echo -e "${G}  Services:${X}"
    echo -e "    TTS UI:     http://localhost:7860"
    echo -e "    Studio:     http://localhost:3000"
    echo -e "${G}========================================${X}"
    echo ""
    echo "Stop with: ./launcher.sh stop"
}

# --- Stop ---
do_stop() {
    info "Stopping services..."

    for pidfile in "$PIDFILE_TTS" "$PIDFILE_STUDIO"; do
        if [[ -f "$pidfile" ]]; then
            pid=$(cat "$pidfile")
            if kill -0 "$pid" 2>/dev/null; then
                kill "$pid"
                ok "Stopped PID $pid"
            else
                warn "Process $pid already gone"
            fi
            rm -f "$pidfile"
        fi
    done

    # Kill anything on our ports
    for port in 7860 3000; do
        if command -v fuser &>/dev/null; then
            fuser -k "${port}/tcp" &>/dev/null || true
            ok "Freed port $port"
        elif command -v lsof &>/dev/null; then
            pids=$(lsof -ti :$port 2>/dev/null || true)
            if [[ -n "$pids" ]]; then
                echo "$pids" | xargs kill -9 2>/dev/null || true
                ok "Freed port $port"
            fi
        fi
    done

    ok "All services stopped"
}

# --- Status ---
do_status() {
    echo -e "${C}Service Status:${X}"
    echo ""

    if curl -s --max-time 3 http://127.0.0.1:7860/ &>/dev/null; then
        echo -e "  VieNeu TTS (7860): ${G}Running${X}"
    else
        echo -e "  VieNeu TTS (7860): ${R}Stopped${X}"
    fi

    if curl -s --max-time 3 http://127.0.0.1:3000/api/health &>/dev/null; then
        echo -e "  Studio UI  (3000): ${G}Running${X}"
    else
        echo -e "  Studio UI  (3000): ${R}Stopped${X}"
    fi
    echo ""
}

# --- Main ---
case "$ACTION" in
    start)   do_start ;;
    stop)    do_stop ;;
    status)  do_status ;;
    install) do_install ;;
    restart) do_stop; sleep 2; do_start ;;
    *)
        echo "Usage: $0 {start|stop|status|restart|install}"
        exit 1
        ;;
esac
