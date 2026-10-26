import React from "react";
import { Audio, Img, Loop, Video, Sequence, staticFile } from "remotion";
import { DynamicGraphic } from "./components/DynamicGraphic";
import { KaraokeSubtitle } from "./components/KaraokeSubtitle";
import { KenBurnsImage } from "./components/KenBurnsImage";
import { theme } from "./theme";

export interface SequenceItem {
  id: string;
  scene: string;
  beat: string;
  type: "AIV" | "IMG" | "GFX";
  duration_seconds: number;
  duration_frames: number;
  start_frame: number;
  asset_path?: string;
  motion_effect?: "ken_burns_zoom_in" | "ken_burns_zoom_out" | "ken_burns_pan_left" | "ken_burns_pan_right" | "static";
  gfx_component?: string;
  gfx_props?: Record<string, any>;
  narration_text?: string;
  narration_audio_url?: string;
  words?: any[];
}

export interface VideoCompositionProps {
  title: string;
  slug: string;
  channel: string;
  fps: number;
  width: number;
  height: number;
  total_duration_seconds: number;
  total_frames: number;
  bgm_url?: string;
  bgm_volume?: number;
  bgm_duration_frames?: number;
  master_audio_url?: string;
  sequences: SequenceItem[];
}

export const VideoComposition: React.FC<VideoCompositionProps> = ({
  sequences = [],
  bgm_url,
  bgm_volume = 0.15,
  bgm_duration_frames,
  master_audio_url,
}) => {
  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: theme.colors.background,
        position: "relative",
        overflow: "hidden",
        fontFamily: theme.typography.fontFamily,
      }}
    >
      {/* Background Music (BGM) with Loop */}
      {bgm_url && (
        bgm_duration_frames && bgm_duration_frames > 0 ? (
          <Loop durationInFrames={bgm_duration_frames}>
            <Audio
              src={bgm_url.startsWith("http") ? bgm_url : staticFile(bgm_url)}
              volume={bgm_volume}
            />
          </Loop>
        ) : (
          <Audio
            src={bgm_url.startsWith("http") ? bgm_url : staticFile(bgm_url)}
            volume={bgm_volume}
            loop
          />
        )
      )}

      {/* Master Narration Audio Track */}
      {master_audio_url && (
        <Audio
          src={master_audio_url.startsWith("http") ? master_audio_url : staticFile(master_audio_url)}
          volume={1.0}
        />
      )}

      {/* Visual & Audio Sequences */}
      {sequences.map((seq, index) => {
        return (
          <Sequence
            key={`${seq.id}-${index}`}
            from={seq.start_frame}
            durationInFrames={seq.duration_frames}
          >
            {/* Visual Layer */}
            <div style={{ width: "100%", height: "100%", position: "absolute" }}>
              {seq.type === "GFX" ? (
                <DynamicGraphic
                  title={seq.gfx_props?.title || seq.beat}
                  label={seq.gfx_props?.label}
                  description={seq.beat}
                  component={seq.gfx_component || (seq as any).component}
                  scene={seq.scene}
                  theme={seq.gfx_props?.theme}
                  durationInFrames={seq.duration_frames}
                  props={seq.gfx_props}
                  narration={seq.narration_text}
                />
              ) : seq.type === "AIV" && seq.asset_path && seq.asset_path.endsWith(".mp4") ? (
                <>
                  <Video
                    src={seq.asset_path.startsWith("http") ? seq.asset_path : staticFile(seq.asset_path)}
                    style={{ width: "100%", height: "100%", objectFit: "cover" }}
                  />
                  {/* Badge pill watermark cover for AIV video */}
                  <Img
                    src={staticFile("images/badge_pill.png")}
                    style={{
                      position: "absolute",
                      bottom: 130,
                      right: 28,
                      width: 410,
                      height: "auto",
                      zIndex: 10,
                      filter: "drop-shadow(0 2px 8px rgba(0,0,0,0.4))",
                    }}
                  />
                </>
              ) : (
                <KenBurnsImage
                  src={
                    seq.asset_path
                      ? seq.asset_path.startsWith("http")
                        ? seq.asset_path
                        : staticFile(seq.asset_path)
                      : "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=1920&q=80"
                  }
                  durationInFrames={seq.duration_frames}
                  effect={seq.motion_effect || "ken_burns_zoom_in"}
                />
              )}
            </div>

            {/* Narration Audio Fallback (if master_audio_url missing) */}
            {!master_audio_url && seq.narration_audio_url && (
              <Audio
                src={seq.narration_audio_url.startsWith("http") ? seq.narration_audio_url : staticFile(seq.narration_audio_url)}
                volume={1.0}
              />
            )}

            {/* Karaoke Subtitle Overlay (No Background) */}
            <KaraokeSubtitle words={seq.words} fullText={seq.narration_text} />
          </Sequence>
        );
      })}
    </div>
  );
};
