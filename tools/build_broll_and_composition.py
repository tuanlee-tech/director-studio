#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/build_broll_and_composition.py
Builds broll-plan.json, broll-plan.md, remotion-composition.json,
studio/remotion/current_props.json, and assets/prompts.md
using exact durations from Whisper timings.
"""
import sys
import os
import json
import re
import wave
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
CHANNEL = "tien-thuc-chien"
SLUG = "lam-phat-loi-song-luong-tang-tien-mat"
VIDEO_DIR = ROOT_DIR / "channels" / CHANNEL / "videos" / SLUG
AUDIO_DIR = VIDEO_DIR / "audio"
ASSETS_DIR = VIDEO_DIR / "assets"
SCRIPT_FILE = VIDEO_DIR / "script.md"
PROPS_FILE = ROOT_DIR / "studio" / "remotion" / "current_props.json"
BROLL_JSON = VIDEO_DIR / "broll-plan.json"
BROLL_MD = VIDEO_DIR / "broll-plan.md"
COMP_FILE = ASSETS_DIR / "remotion-composition.json"
PROMPTS_FILE = ASSETS_DIR / "prompts.md"
FPS = 30

def get_audio_duration_ms(wav_path: Path) -> int:
    try:
        with wave.open(str(wav_path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return int(frames / rate * 1000)
    except Exception:
        return 0

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

def build():
    scenes = parse_script()
    print(f"🎬 Đang đồng bộ broll, composition và props cho {len(scenes)} scenes...")

    broll_scenes = []
    visual_sequences = []
    props_sequences = []

    current_frame = 0

    for s in scenes:
        sid = s["scene_id"]
        stype = s["type"]
        concept = s["concept"]
        narration = s["narration"]

        wav_file = AUDIO_DIR / f"{sid}_narration.wav"
        timing_file = AUDIO_DIR / f"{sid}_timing.json"

        audio_ms = get_audio_duration_ms(wav_file)
        audio_dur_s = audio_ms / 1000.0

        if stype == "AIV":
            dur_s = 6.0
            dur_frames = 6 * FPS
            asset_filename = f"{sid}-A_6s_AIV.mp4"
        else:
            # Calculate frames needed for audio + 2 frames cushion
            calc_frames = int(round(audio_dur_s * FPS)) + 2
            # At least the estimated duration
            dur_frames = max(calc_frames, s["est_duration"] * FPS)
            dur_s = dur_frames / float(FPS)
            asset_filename = f"{sid}-A_{int(dur_s)}s_{stype}.png" if stype == "IMG" else None

        # Clean title for viewer
        clean_title = concept
        clean_title = re.sub(r"^[A-Za-z0-9_]+(\s+[^:]+)?:?\s*", "", clean_title)

        words = []
        if timing_file.exists():
            try:
                tdata = json.loads(timing_file.read_text(encoding="utf-8"))
                words = tdata.get("words", [])
            except Exception:
                words = []

        motion_effects = ["ken_burns_zoom_in", "ken_burns_pan_left", "ken_burns_zoom_out", "ken_burns_pan_right"]
        motion_effect = motion_effects[len(broll_scenes) % len(motion_effects)]

        # Broll entry
        broll_scenes.append({
            "scene_id": sid,
            "beat": s["beat"],
            "type": stype,
            "duration": dur_s,
            "duration_frames": dur_frames,
            "concept": concept,
            "narration": narration,
            "asset_file": asset_filename
        })

        # Visual sequence for tracks.visual_sequences
        seq_entry = {
            "scene_id": sid,
            "type": stype,
            "from_frame": current_frame,
            "duration_frames": dur_frames,
            "description": clean_title,
            "props": {
                "title": clean_title,
                "videoSlug": SLUG,
                "slug": SLUG,
                "channel": CHANNEL,
                "topic": SLUG,
                "narration": narration
            }
        }
        if stype in ("AIV", "IMG") and asset_filename:
            seq_entry["props"]["src"] = f"assets/{asset_filename}"
            seq_entry["props"]["asset_type"] = "video" if stype == "AIV" else "image"

        visual_sequences.append(seq_entry)

        # Full sequence entry (universal compatibility for VideoComposition & Root)
        full_seq = {
            "id": f"{sid}-A",
            "scene": sid,
            "beat": s["beat"],
            "narration_text": narration,
            "narration": narration,
            "type": stype,
            "start_frame": current_frame,
            "from": current_frame,
            "from_frame": current_frame,
            "duration_frames": dur_frames,
            "durationInFrames": dur_frames,
            "duration_seconds": round(dur_s, 2),
            "component": "Video" if stype == "AIV" else ("KenBurnsImage" if stype == "IMG" else "DynamicGraphic"),
            "gfx_component": "DynamicGraphicVideo2" if stype == "GFX" else None,
            "gfx_props": {
                "title": clean_title,
                "videoSlug": SLUG,
                "slug": SLUG,
                "channel": CHANNEL,
                "topic": SLUG,
                "narration": narration,
                "theme": "finance-clean-vyond"
            },
            "asset_path": f"assets/{asset_filename}" if asset_filename else None,
            "src": f"assets/{asset_filename}" if asset_filename else None,
            "narration_audio_url": f"audio/{sid}_narration.wav",
            "words": words,
            "motion_effect": motion_effect
        }

        props_sequences.append(full_seq)

        current_frame += dur_frames

    total_frames = current_frame
    total_seconds = total_frames / FPS

    # 1. Write broll-plan.json
    broll_data = {
        "channel": CHANNEL,
        "video_slug": SLUG,
        "total_scenes": len(scenes),
        "total_duration_seconds": round(total_seconds, 2),
        "total_frames": total_frames,
        "fps": FPS,
        "scenes": broll_scenes
    }
    BROLL_JSON.write_text(json.dumps(broll_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 2. Write broll-plan.md
    md_lines = [
        f"# B-Roll Plan — {SLUG}",
        f"**Kênh**: {CHANNEL} | **Tổng phân cảnh**: {len(scenes)} | **Thời lượng**: {total_seconds/60:.2f} phút ({total_seconds:.1f}s, {total_frames} frames)",
        "",
        "| Scene | Type | Duration | Beat | Visual Concept | Asset File |",
        "| :--- | :---: | :---: | :--- | :--- | :--- |"
    ]
    for b in broll_scenes:
        md_lines.append(f"| `{b['scene_id']}` | **{b['type']}** | {b['duration']:.1f}s ({b['duration_frames']}f) | {b['beat']} | {b['concept']} | `{b['asset_file'] or 'DynamicGraphic'}` |")
    BROLL_MD.write_text("\n".join(md_lines), encoding="utf-8")

    # 3. Write remotion-composition.json
    comp_data = {
        "schema_version": "1.0",
        "fps": FPS,
        "width": 1920,
        "height": 1080,
        "channel": CHANNEL,
        "video_slug": SLUG,
        "title": "Tại Sao Lương Tăng Gấp Đôi Nhưng Ví Tiền Vẫn Về 0 Cuối Tháng?",
        "audio_track": "audio/narration_master.wav",
        "master_audio_url": "audio/narration_master.wav",
        "audioSrc": "audio/narration_master.wav",
        "bgm_url": "bgm/bgm_enlivening.mp3",
        "bgmSrc": "bgm/bgm_enlivening.mp3",
        "bgm_volume": 0.15,
        "bgmVolume": 0.15,
        "bgm_duration_seconds": 152.82,
        "bgm_duration_frames": 4584,
        "total_frames": total_frames,
        "total_duration_seconds": round(total_seconds, 2),
        "durationInFrames": total_frames,
        "composition": {
            "id": "VideoComposition",
            "fps": FPS,
            "width": 1920,
            "height": 1080,
            "duration_frames": total_frames,
            "duration_seconds": round(total_seconds, 2)
        },
        "tracks": {
            "audio_master": {
                "src": "audio/narration_master.wav",
                "volume": 1.0
            },
            "bgm": {
                "src": "bgm/bgm_enlivening.mp3",
                "volume": 0.15
            },
            "visual_sequences": visual_sequences
        },
        "sequences": props_sequences
    }
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    COMP_FILE.write_text(json.dumps(comp_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 4. Write studio/remotion/current_props.json
    current_props = {
        "channel": CHANNEL,
        "videoSlug": SLUG,
        "slug": SLUG,
        "topic": SLUG,
        "fps": FPS,
        "width": 1920,
        "height": 1080,
        "total_frames": total_frames,
        "total_duration_seconds": round(total_seconds, 2),
        "durationInFrames": total_frames,
        "audioSrc": "audio/narration_master.wav",
        "master_audio_url": "audio/narration_master.wav",
        "bgmSrc": "bgm/bgm_enlivening.mp3",
        "bgm_url": "bgm/bgm_enlivening.mp3",
        "bgmVolume": 0.15,
        "bgm_volume": 0.15,
        "bgm_duration_frames": 4584,
        "sequences": props_sequences
    }
    PROPS_FILE.write_text(json.dumps(current_props, ensure_ascii=False, indent=2), encoding="utf-8")

    # 5. Write assets/prompts.md
    write_prompts_file(scenes)

    print(f"✅ Đã tạo hoàn tất:")
    print(f"  - broll-plan.json & broll-plan.md: {total_seconds/60:.2f} phút ({total_frames} frames)")
    print(f"  - remotion-composition.json ({len(visual_sequences)} visual sequences)")
    print(f"  - studio/remotion/current_props.json")
    print(f"  - assets/prompts.md")


def write_prompts_file(scenes):
    lines = [
        f"# Media Prompts — {SLUG}",
        f"Kênh: {CHANNEL} | Phong cách: 2D flat vector cartoon illustration, Vyond animation style | Tuân thủ nghiêm ngặt Rule 9 (No AIV speech/music)",
        "",
        "## 1. Danh sách Prompts AIV (7 Scenes) & IMG (69 Scenes)",
        "",
        "| ID | Type | Duration | Concept | Prompt Sinh Media |",
        "| :--- | :---: | :---: | :--- | :--- |"
    ]

    for s in scenes:
        sid = s["scene_id"]
        stype = s["type"]
        concept = s["concept"]
        dur = s["est_duration"]
        if stype not in ("AIV", "IMG"):
            continue

        if stype == "AIV":
            # Rule 9 compliance: Audio clause mandatory
            audio_clause = "Audio: No character speech, no dialogue, no talking voices, no background music. Only subtle natural ambient environmental sounds and foley sound effects."
            prompt = (
                f"Full-frame 6-second continuous motion: {concept}. "
                f"2D flat vector cartoon illustration, Vyond animation style, thick black outlines, vibrant solid colors, flat shading, clean background. "
                f"Expressive character with fluid comic-style motion. "
                f"{audio_clause} "
                f"Avoid text, typography, watermarks, distorted faces."
            )
        else: # IMG
            prompt = (
                f"2D flat vector illustration: {concept}. "
                f"Vyond cartoon animation style, thick clean black outlines, bold saturated colors, minimal flat shading, solid pastel backdrop. "
                f"Character consistency: 27-year-old Vietnamese professional man, short neat black hair, modern glasses, wearing crisp white button-up collared shirt. "
                f"Avoid text, words, labels, typography, logos, watermarks, distorted limbs."
            )

        lines.append(f"| `{sid}` | **{stype}** | {dur}s | {concept} | {prompt} |")

    PROMPTS_FILE.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    build()
