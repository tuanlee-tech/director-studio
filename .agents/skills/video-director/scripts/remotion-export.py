#!/usr/bin/env python3
"""
remotion-export.py — Xuất composition schema chuẩn cho Remotion / Hyperframe từ broll-plan.json.
Sử dụng từ cheatcode @gen-remotion.

Usage:
    python remotion-export.py <broll_plan_json> <output_composition_json> [--fps 30]
"""

import sys
import json
import argparse
from pathlib import Path

# Fix Windows console cp1252 encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def broll_plan_to_remotion(broll_plan_path: str, output_path: str, fps: int = 30):
    with open(broll_plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    composition = {
        "schema_version": "1.0",
        "fps": fps,
        "width": 1920,
        "height": 1080,
        "channel": plan.get("channel", ""),
        "video_slug": plan.get("video_slug", ""),
        "audio_track": f"audio/narration_master.wav",
        "tracks": {
            "visual_sequences": [],
            "subtitles": f"subtitles/karaoke.srt"
        }
    }

    current_frame = 0
    scenes = plan.get("scenes", [])

    for scene in scenes:
        scene_id = scene.get("scene_id", "")
        brolls = scene.get("brolls", [])

        for broll in brolls:
            broll_id = broll.get("broll_id", "")
            broll_type = broll.get("type", "IMG")
            duration_s = broll.get("duration_s", 4)
            duration_frames = int(duration_s * fps)
            desc = broll.get("description", "")

            seq_item = {
                "id": broll_id,
                "scene_id": scene_id,
                "type": broll_type,
                "from_frame": current_frame,
                "duration_frames": duration_frames,
                "duration_seconds": duration_s,
                "description": desc
            }

            if broll_type == "AIV":
                seq_item["component"] = "VideoClip"
                seq_item["props"] = {
                    "src": f"assets/{broll_id}_{duration_s}s_AIV.mp4",
                    "playbackRate": 1.0
                }
            elif broll_type == "GFX":
                seq_item["component"] = broll.get("component", "MotionGraphic")
                seq_item["props"] = broll.get("props", {
                    "title": desc,
                    "theme": "finance-dark",
                    "animationType": "slide-up"
                })
            else:  # IMG
                seq_item["component"] = "KenBurnsImage"
                seq_item["props"] = {
                    "src": f"assets/{broll_id}_IMG.png",
                    "animation": broll.get("camera", "zoom-in"),
                    "scaleRange": [1.0, 1.15]
                }

            composition["tracks"]["visual_sequences"].append(seq_item)
            current_frame += duration_frames

    composition["total_frames"] = current_frame
    composition["total_duration_seconds"] = round(current_frame / fps, 2)

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(composition, f, ensure_ascii=False, indent=2)

    print(f"✅ Remotion Composition saved: {output_path}")
    print(f"   Sequences: {len(composition['tracks']['visual_sequences'])} | Total frames: {current_frame} ({composition['total_duration_seconds']}s @ {fps}fps)")


def main():
    parser = argparse.ArgumentParser(description="Chuyển broll-plan.json sang Remotion composition schema")
    parser.add_argument("broll_plan", help="Đường dẫn file broll-plan.json")
    parser.add_argument("output_json", help="Đường dẫn file composition JSON đầu ra")
    parser.add_argument("--fps", type=int, default=30, help="Số frame mỗi giây (mặc định: 30)")
    args = parser.parse_args()

    broll_plan_to_remotion(args.broll_plan, args.output_json, args.fps)


if __name__ == "__main__":
    main()
