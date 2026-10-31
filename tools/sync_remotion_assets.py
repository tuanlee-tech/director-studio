#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/sync_remotion_assets.py — Sync video assets & audio to Remotion public runtime cache

Usage:
  # Sync a specific video to Remotion Studio public cache:
  python tools/sync_remotion_assets.py thoat-bay-no-the-tin-dung --channel tien-thuc-chien

  # Clean the Remotion Studio public cache:
  python tools/sync_remotion_assets.py --clean
"""

import sys
import os
import shutil
import argparse
from pathlib import Path

# Reconfigure stdout for UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
PUB_DIR = ROOT_DIR / "studio" / "remotion" / "public"
PUB_ASSETS_DIR = PUB_DIR / "assets"
PUB_AUDIO_DIR = PUB_DIR / "audio"
PUB_BGM_DIR = PUB_DIR / "bgm"


def clean_public_cache():
    """Remove runtime files in studio/remotion/public/{assets,audio} while preserving .gitkeep."""
    print("🧹 Cleaning Remotion Studio public runtime cache...")
    count = 0
    for folder in [PUB_ASSETS_DIR, PUB_AUDIO_DIR]:
        if folder.exists():
            for item in folder.iterdir():
                if item.name == ".gitkeep":
                    continue
                if item.is_file():
                    item.unlink()
                    count += 1
                elif item.is_dir():
                    shutil.rmtree(item)
                    count += 1
    print(f"✅ Cleared {count} temporary files/folders from studio/remotion/public/")


def sync_video_assets(video_slug: str, channel_id: str = "tien-thuc-chien"):
    """Sync assets and audio from channels/<channel>/videos/<slug>/ into studio/remotion/public/."""
    video_dir = ROOT_DIR / "channels" / channel_id / "videos" / video_slug
    if not video_dir.exists():
        print(f"❌ Error: Video directory not found: {video_dir}")
        sys.exit(1)

    assets_src = video_dir / "assets"
    audio_src = video_dir / "audio"

    PUB_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    PUB_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    PUB_BGM_DIR.mkdir(parents=True, exist_ok=True)

    asset_count = 0
    if assets_src.exists():
        for f in assets_src.glob("*.*"):
            if f.is_file() and f.name not in [".gitkeep", "prompts.md", "remotion-composition.json"]:
                dest = PUB_ASSETS_DIR / f.name
                if not dest.exists() or dest.stat().st_size != f.stat().st_size:
                    shutil.copyfile(f, dest)
                asset_count += 1

    audio_count = 0
    if audio_src.exists():
        for f in audio_src.glob("*.*"):
            if f.is_file() and f.name != ".gitkeep":
                dest = PUB_AUDIO_DIR / f.name
                if not dest.exists() or dest.stat().st_size != f.stat().st_size:
                    shutil.copyfile(f, dest)
                # Also copy narration_master.wav to assets/ for Remotion /assets/ access
                if f.name == "narration_master.wav":
                    dest_asset = PUB_ASSETS_DIR / f.name
                    if not dest_asset.exists() or dest_asset.stat().st_size != f.stat().st_size:
                        shutil.copyfile(f, dest_asset)
                audio_count += 1

    # Copy BGM if available
    bgm_src = ROOT_DIR / "channels" / channel_id / "bgm"
    if bgm_src.exists():
        for f in bgm_src.glob("*.mp3"):
            shutil.copyfile(f, PUB_BGM_DIR / f.name)
            shutil.copyfile(f, PUB_ASSETS_DIR / f.name)

    print(f"✅ Synced {asset_count} assets and {audio_count} audio files for '{video_slug}' ({channel_id}) into Remotion public cache.")


def main():
    parser = argparse.ArgumentParser(description="Sync or clean Remotion public runtime assets")
    parser.add_argument("video_slug", nargs="?", default="thoat-bay-no-the-tin-dung", help="Video slug")
    parser.add_argument("--channel", default="tien-thuc-chien", help="Channel ID")
    parser.add_argument("--clean", action="store_true", help="Clean public runtime cache")
    args = parser.parse_args()

    if args.clean:
        clean_public_cache()
    else:
        sync_video_assets(args.video_slug, args.channel)


if __name__ == "__main__":
    main()
