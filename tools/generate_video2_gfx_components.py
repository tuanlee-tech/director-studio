#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/generate_video2_gfx_components.py
Generates the complete DynamicGraphicVideo2.tsx with bespoke SVG motion graphics
for all 81 GFX scenes in Video #2.
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

output_path = Path("channels/tien-thuc-chien/template/components/DynamicGraphicVideo2.tsx")

code = '''import React from "react";
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

'''

# We will append handlers for each scene
# Let's write the generator with detailed templates for all 81 scenes
