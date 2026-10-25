import React from "react";
import { Composition } from "remotion";
import { VideoComposition } from "./VideoComposition";
import { VideoCompositionProps } from "./types";

const defaultProps: VideoCompositionProps = {
  title: "Video Director Composition",
  slug: "demo-video",
  channel: "demo-channel",
  fps: 30,
  width: 1920,
  height: 1080,
  total_duration_seconds: 14,
  total_frames: 420,
  bgm_volume: 0.1,
  sequences: [
    {
      id: "S001-A",
      scene: "S001",
      beat: "Hook",
      type: "IMG",
      duration_seconds: 6,
      duration_frames: 180,
      start_frame: 0,
      motion_effect: "ken_burns_zoom_in",
      narration_text: "Bạn nghĩ thẻ tín dụng là công cụ tài chính thông minh?",
      words: [
        { word: "Bạn", start_ms: 100, end_ms: 400 },
        { word: "nghĩ", start_ms: 450, end_ms: 750 },
        { word: "thẻ", start_ms: 800, end_ms: 1100 },
        { word: "tín", start_ms: 1150, end_ms: 1450 },
        { word: "dụng", start_ms: 1500, end_ms: 1900 },
        { word: "là", start_ms: 2000, end_ms: 2300 },
        { word: "công", start_ms: 2350, end_ms: 2650 },
        { word: "cụ", start_ms: 2700, end_ms: 3000 },
        { word: "tài", start_ms: 3050, end_ms: 3350 },
        { word: "chính", start_ms: 3400, end_ms: 3800 },
        { word: "thông", start_ms: 3900, end_ms: 4300 },
        { word: "minh?", start_ms: 4350, end_ms: 4900 },
      ],
    },
    {
      id: "S002-A",
      scene: "S002",
      beat: "Problem",
      type: "GFX",
      gfx_component: "ChartMotion",
      duration_seconds: 8,
      duration_frames: 240,
      start_frame: 180,
      narration_text: "Thực tế, lãi suất và phí phạt có thể lên tới 45% mỗi năm.",
      words: [
        { word: "Thực", start_ms: 6100, end_ms: 6400 },
        { word: "tế,", start_ms: 6450, end_ms: 6800 },
        { word: "lãi", start_ms: 6900, end_ms: 7200 },
        { word: "suất", start_ms: 7250, end_ms: 7600 },
        { word: "và", start_ms: 7650, end_ms: 7900 },
        { word: "phí", start_ms: 7950, end_ms: 8250 },
        { word: "phạt", start_ms: 8300, end_ms: 8650 },
        { word: "có", start_ms: 8700, end_ms: 8950 },
        { word: "thể", start_ms: 9000, end_ms: 9250 },
        { word: "lên", start_ms: 9300, end_ms: 9600 },
        { word: "tới", start_ms: 9650, end_ms: 9900 },
        { word: "45%", start_ms: 10000, end_ms: 10600 },
        { word: "mỗi", start_ms: 10700, end_ms: 11000 },
        { word: "năm.", start_ms: 11050, end_ms: 11600 },
      ],
      gfx_props: {
        title: "Bẫy Lãi Suất Thẻ Tín Dụng",
        bars: [
          { label: "Vay thường", value: 10, color: "#3b82f6" },
          { label: "Thẻ tín dụng", value: 36, color: "#f59e0b" },
          { label: "Phạt quá hạn", value: 45, color: "#ef4444" },
        ],
      },
    },
  ],
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MainVideo"
        component={VideoComposition as any}
        durationInFrames={420}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={defaultProps as any}
        calculateMetadata={({ props }: any) => {
          const totalFrames =
            props?.total_frames ||
            (props?.sequences && props.sequences.length > 0
              ? props.sequences.reduce((sum: number, s: any) => sum + s.duration_frames, 0)
              : 420);
          return {
            durationInFrames: Math.max(totalFrames, 30),
            fps: props?.fps || 30,
            width: props?.width || 1920,
            height: props?.height || 1080,
          };
        }}
      />
    </>
  );
};
