import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { WordTiming } from "../types";

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
          textAlign: "center",
          padding: "0 60px",
          pointerEvents: "none",
        }}
      >
        <span
          style={{
            fontFamily: "Inter, 'SF Pro Display', sans-serif",
            fontSize: 48,
            fontWeight: 800,
            color: "#ffffff",
            textShadow: "0 4px 16px rgba(0,0,0,0.85), 0 2px 4px rgba(0,0,0,0.9)",
            backgroundColor: "rgba(15, 23, 42, 0.75)",
            padding: "8px 24px",
            borderRadius: 12,
            letterSpacing: "-0.02em",
          }}
        >
          {fullText}
        </span>
      </div>
    );
  }

  // Lọc lấy các từ trong khoảng hiển thị hiện tại (cụm từ gần currentMs trong vòng 3.5s)
  const activeWordIndex = words.findIndex(
    (w) => currentMs >= w.start_ms && currentMs <= w.end_ms
  );

  // Chọn cửa sổ 6 từ xung quanh từ đang đọc
  let startIndex = 0;
  if (activeWordIndex !== -1) {
    startIndex = Math.max(0, Math.floor(activeWordIndex / 6) * 6);
  } else {
    // Nếu nằm giữa 2 từ
    const nextIdx = words.findIndex((w) => currentMs < w.start_ms);
    startIndex = nextIdx !== -1 ? Math.max(0, Math.floor(nextIdx / 6) * 6) : Math.max(0, words.length - 6);
  }
  const currentChunk = words.slice(startIndex, startIndex + 6);

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
          gap: "12px",
          backgroundColor: "rgba(10, 15, 29, 0.78)",
          padding: "12px 28px",
          borderRadius: 18,
          backdropFilter: "blur(8px)",
          border: "1px solid rgba(255, 255, 255, 0.12)",
          boxShadow: "0 8px 32px rgba(0, 0, 0, 0.6)",
        }}
      >
        {currentChunk.map((w, idx) => {
          const isSpoken = currentMs >= w.start_ms;
          const isCurrent = currentMs >= w.start_ms && currentMs <= w.end_ms;

          let color = "#94a3b8"; // Chưa đọc: xám
          let scale = 1.0;
          let shadow = "none";

          if (isCurrent) {
            color = "#facc15"; // Đang đọc: vàng rực
            scale = 1.12;
            shadow = "0 0 20px rgba(250, 204, 21, 0.8), 0 2px 4px rgba(0,0,0,0.9)";
          } else if (isSpoken) {
            color = "#ffffff"; // Đã đọc: trắng
            scale = 1.0;
          }

          return (
            <span
              key={`${w.word}-${idx}`}
              style={{
                fontFamily: "Inter, 'Segoe UI', sans-serif",
                fontSize: 46,
                fontWeight: 900,
                color,
                transform: `scale(${scale})`,
                transition: "all 0.08s ease-out",
                textShadow: shadow,
                display: "inline-block",
                letterSpacing: "-0.01em",
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
