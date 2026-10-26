import React from "react";
import { Sequence, Audio, Video, Img, staticFile } from "remotion";
import { VideoCompositionProps, SequenceItem } from "./types";
import { KenBurnsImage } from "./components/KenBurnsImage";
import { KaraokeSubtitle } from "./components/KaraokeSubtitle";
import { CounterNumber } from "./components/motion/CounterNumber";
import { ChartMotion } from "./components/motion/ChartMotion";

export const VideoComposition: React.FC<VideoCompositionProps> = ({
  sequences = [],
  bgm_url,
  bgm_volume = 0.12,
}) => {
  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#05070f",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Background Music (BGM) */}
      {bgm_url && (
        <Audio
          src={bgm_url.startsWith("http") ? bgm_url : staticFile(bgm_url)}
          volume={bgm_volume}
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
                seq.gfx_component === "CounterNumber" ? (
                  <CounterNumber {...seq.gfx_props} durationInFrames={seq.duration_frames} />
                ) : seq.gfx_component === "ChartMotion" ? (
                  <ChartMotion {...seq.gfx_props} durationInFrames={seq.duration_frames} />
                ) : (
                  <CounterNumber {...seq.gfx_props} durationInFrames={seq.duration_frames} />
                )
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
                      bottom: 137,
                      right: 28,
                      width: 410,
                      height: "auto",
                      zIndex: 10,
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

            {/* Narration Audio Track */}
            {seq.narration_audio_url && (
              <Audio
                src={
                  seq.narration_audio_url.startsWith("http")
                    ? seq.narration_audio_url
                    : staticFile(seq.narration_audio_url)
                }
                volume={1.0}
              />
            )}

            {/* Karaoke Subtitle Overlay */}
            <KaraokeSubtitle words={seq.words} fullText={seq.narration_text} />
          </Sequence>
        );
      })}
    </div>
  );
};
