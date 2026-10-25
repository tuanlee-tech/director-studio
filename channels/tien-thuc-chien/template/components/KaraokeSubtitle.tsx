import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

export interface WordTiming {
  word: string;
  start_ms: number;
  end_ms: number;
}

interface KaraokeSubtitleProps {
  words?: WordTiming[];
  fullText?: string;
}

export const KaraokeSubtitle: React.FC<KaraokeSubtitleProps> = ({ words, fullText }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentMs = (frame / fps) * 1000;

  if (!words || words.length === 0) {
    if (!fullText) return null;
    return (
      <div
        style={{
          position: "absolute",
          bottom: 110,
          width: "100%",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          padding: "0 60px",
          pointerEvents: "none",
        }}
      >
        <span
          style={{
            fontFamily: theme.typography.fontFamily,
            fontSize: 46,
            fontWeight: 800,
            color: "#ffffff",
            textShadow:
              "0 2px 6px rgba(0,0,0,0.95), 0 0 14px rgba(0,0,0,0.85), -2px -2px 0 rgba(0,0,0,0.9), 2px -2px 0 rgba(0,0,0,0.9), -2px 2px 0 rgba(0,0,0,0.9), 2px 2px 0 rgba(0,0,0,0.9)",
            letterSpacing: "0.01em",
            textAlign: "center",
          }}
        >
          {fullText}
        </span>
      </div>
    );
  }

  // Active word detection
  const activeWordIndex = words.findIndex(
    (w) => currentMs >= w.start_ms && currentMs <= w.end_ms
  );

  let startIndex = 0;
  if (activeWordIndex !== -1) {
    startIndex = Math.max(0, Math.floor(activeWordIndex / 5) * 5);
  } else {
    const nextIdx = words.findIndex((w) => currentMs < w.start_ms);
    startIndex = nextIdx !== -1 ? Math.max(0, Math.floor(nextIdx / 5) * 5) : Math.max(0, words.length - 5);
  }
  const currentChunk = words.slice(startIndex, startIndex + 5);

  return (
    <div
      style={{
        position: "absolute",
        bottom: 110,
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "0 80px",
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          alignItems: "center",
          gap: "6px 13px",
          backgroundColor: "transparent",
        }}
      >
        {currentChunk.map((w, idx) => {
          const isSpoken = currentMs >= w.start_ms;
          const isCurrent = currentMs >= w.start_ms && currentMs <= w.end_ms;

          let color = "#e2e8f0";
          let scale = 1.0;
          let shadow =
            "0 2px 6px rgba(0,0,0,0.95), 0 0 12px rgba(0,0,0,0.9), -2px -2px 0 rgba(0,0,0,0.9), 2px -2px 0 rgba(0,0,0,0.9), -2px 2px 0 rgba(0,0,0,0.9), 2px 2px 0 rgba(0,0,0,0.9)";

          if (isCurrent) {
            color = "#facc15";
            scale = 1.1;
            shadow =
              "0 0 24px rgba(250, 204, 21, 0.95), 0 2px 6px rgba(0,0,0,0.95), -2px -2px 0 rgba(0,0,0,0.95), 2px -2px 0 rgba(0,0,0,0.95), -2px 2px 0 rgba(0,0,0,0.95), 2px 2px 0 rgba(0,0,0,0.95)";
          } else if (isSpoken) {
            color = "#ffffff";
            scale = 1.0;
          }

          return (
            <span
              key={`${w.word}-${idx}`}
              style={{
                fontFamily: theme.typography.fontFamily,
                fontSize: 46,
                fontWeight: 900,
                color,
                transform: `scale(${scale})`,
                transition: "all 0.08s ease-out",
                textShadow: shadow,
                display: "inline-block",
                padding: "0 2px",
                letterSpacing: "0.01em",
              }}
            >
              {w.word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
