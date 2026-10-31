import React from "react";
import { Composition, Still } from "remotion";
import { VideoComposition as DefaultComposition } from "./VideoComposition";
import { VideoComposition as TienThucChienComposition } from "../../../channels/tien-thuc-chien/template";
import { VideoComposition as StarterComposition } from "../../../channels/_template_starter";
import { Thumbnail } from "../../../channels/tien-thuc-chien/template/components/Thumbnail";
import { ThumbnailMaster } from "../../../channels/tien-thuc-chien/template/components/ThumbnailMaster";
import { VideoCompositionProps } from "./types";
import { loadFont } from "@remotion/google-fonts/BeVietnamPro";

loadFont("normal", {
  weights: ["400", "600", "700", "800", "900"],
  subsets: ["vietnamese", "latin"],
  ignoreTooManyRequestsWarning: true,
});

const ChannelVideoRouter: React.FC<any> = (props) => {
  const ch = (props?.channel || "tien-thuc-chien").toLowerCase();
  if (ch === "tien-thuc-chien") {
    return <TienThucChienComposition {...props} />;
  }
  return <StarterComposition {...props} />;
};

const defaultProps: VideoCompositionProps = {
  title: "Video Director Composition",
  slug: "demo-video",
  channel: "demo-channel",
  fps: 30,
  width: 1920,
  height: 1080,
  total_duration_seconds: 14,
  total_frames: 420,
  bgm_url: "bgm/bgm_calm_lofi.mp3",
  bgm_volume: 0.1,
  bgm_duration_frames: 5040,
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

let initialProps = defaultProps;
try {
  const current = require("../current_props.json");
  if (current && current.sequences && current.sequences.length > 0) {
    initialProps = current;
  }
} catch (e) {
  // fallback to defaultProps
}

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MainVideo"
        component={ChannelVideoRouter as any}
        durationInFrames={12270}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={initialProps as any}
        calculateMetadata={({ props }: any) => {
          const totalFrames =
            Number(props?.total_frames) ||
            Number(props?.durationInFrames) ||
            Number(props?.composition?.duration_frames) ||
            (props?.sequences && props.sequences.length > 0
              ? props.sequences.reduce((sum: number, s: any) => sum + (Number(s.duration_frames) || Number(s.durationInFrames) || 0), 0)
              : 12270);
          return {
            durationInFrames: Number.isFinite(totalFrames) && totalFrames > 0 ? totalFrames : 12270,
            fps: props?.fps || 30,
            width: props?.width || 1920,
            height: props?.height || 1080,
          };
        }}
      />
      <Composition
        id="tien-thuc-chien"
        component={TienThucChienComposition as any}
        durationInFrames={12270}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={initialProps as any}
      />
      <Composition
        id="demo-channel"
        component={StarterComposition as any}
        durationInFrames={12270}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={initialProps as any}
      />
      <Still
        id="Thumbnail"
        component={Thumbnail}
        width={1920}
        height={1080}
      />
      <Still
        id="Thumbnail-720p"
        component={Thumbnail}
        width={1280}
        height={720}
      />
      <Still
        id="ThumbnailMaster"
        component={ThumbnailMaster as any}
        width={1920}
        height={1080}
      />
    </>
  );
};
