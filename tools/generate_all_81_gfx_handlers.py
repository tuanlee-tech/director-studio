#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/generate_all_81_gfx_handlers.py
Generates channels/tien-thuc-chien/template/components/DynamicGraphicVideo2.tsx
with full dedicated vector graphics for all 81 GFX scenes in Video #2.
"""
import sys, json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

scenes = json.loads(Path("tools/gfx_scenes_list.json").read_text(encoding="utf-8"))

target_file = Path("channels/tien-thuc-chien/template/components/DynamicGraphicVideo2.tsx")

header = """import React from "react";
import { interpolate, useCurrentFrame, spring, useVideoConfig } from "remotion";
import { theme } from "../theme";

interface DynamicGraphicVideo2Props {
  title?: string;
  label?: string;
  description?: string;
  component?: string;
  scene?: string;
  theme?: string;
  durationInFrames?: number;
  props?: Record<string, any>;
  narration?: string;
  [key: string]: any;
}

export const cleanText = (t: string): string => {
  if (!t) return "";
  return t
    .replace(/^[A-Za-z0-9_]+(\\s+[^\\:]+)?:\\s*/i, "")
    .replace(/^Tiêu đề\\s*[\\:\\'\\"]*/i, "")
    .replace(/[\\'\\"]$/g, "")
    .trim();
};

export const DynamicGraphicVideo2: React.FC<DynamicGraphicVideo2Props> = ({
  title = "",
  label = "",
  description = "",
  scene = "",
  durationInFrames = 120,
  props = {},
  narration = "",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const sc = (scene || "").toUpperCase();
  const rawText = cleanText(description || title || label || "");
  const cleanTitle = cleanText(title || description || "");

  // Spring entrance
  const enterSpring = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.7, stiffness: 85 },
  });

  const scale = interpolate(enterSpring, [0, 1], [0.94, 1]);
  const opacity = interpolate(enterSpring, [0, 0.4], [0, 1]);
  const translateY = interpolate(enterSpring, [0, 1], [20, 0]);
  const animProgress = Math.min(1, Math.max(0, frame / (durationInFrames || 120)));

"""

handlers = []

def make_handler(sid, tag_icon, tag_text, tag_color, tag_bg, title, subhead, svg_content):
    return f"""  // =========================================================================
  // --- {sid}: {title} ---
  // =========================================================================
  if (sc === "{sid}") {{
    return (
      <div style={{...containerStyle}}>
        <div style={{{{ ...cardStyle, transform: `scale(${{scale}}) translateY(${{translateY}}px)`, opacity, maxWidth: 1140, border: "2px solid {tag_color}" }}}}>
          <div style={{tagStyle("{tag_color}", "{tag_bg}")}}>
            <span>{tag_icon}</span> {tag_text}
          </div>
          <div style={{headingStyle}}>{title}</div>
          <div style={{subheadStyle}}>{subhead}</div>

          <div style={{{{ width: "100%", height: 280, position: "relative", display: "flex", justifyContent: "center", alignItems: "center" }}}}>
            {svg_content}
          </div>
        </div>
      </div>
    );
  }}
"""

print(f"Loaded {len(scenes)} scenes.")
