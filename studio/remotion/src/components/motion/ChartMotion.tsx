import React from "react";
import { interpolate, useCurrentFrame, spring, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/BeVietnamPro";

const { fontFamily } = loadFont("normal", {
  weights: ["600", "700", "800"],
  subsets: ["vietnamese", "latin"],
  ignoreTooManyRequestsWarning: true,
});

interface ChartBar {
  label: string;
  value: number;
  color: string;
}

interface ChartMotionProps {
  title?: string;
  bars?: ChartBar[];
  durationInFrames?: number;
}

export const ChartMotion: React.FC<ChartMotionProps> = ({
  title = "So sánh Lãi suất Thực tế",
  bars = [
    { label: "Vay thường", value: 10, color: "#3b82f6" },
    { label: "Thẻ tín dụng", value: 36, color: "#ef4444" },
    { label: "Phạt quá hạn", value: 45, color: "#dc2626" },
  ],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: {
      damping: 12,
      stiffness: 90,
    },
  });

  const maxValue = Math.max(...bars.map((b) => b.value), 50);

  const displayTitle = title.replace(/^ChartMotion:\s*/i, "").trim();

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        width: "100%",
        height: "100%",
        backgroundColor: "#080c16",
        background: "radial-gradient(ellipse at center, #111a2e 0%, #080c16 85%)",
        color: "#ffffff",
        fontFamily,
        padding: "40px 80px",
      }}
    >
      <h2
        style={{
          fontSize: 44,
          fontWeight: 800,
          color: "#f8fafc",
          marginBottom: 48,
          letterSpacing: "-0.02em",
          fontFamily,
          textShadow: "0 4px 20px rgba(0,0,0,0.6)",
        }}
      >
        {displayTitle}
      </h2>

      <div
        style={{
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "center",
          gap: 60,
          height: 380,
          width: "80%",
          borderBottom: "3px solid #334155",
          paddingBottom: 20,
        }}
      >
        {bars.map((bar, idx) => {
          const barHeight = interpolate(progress, [0, 1], [0, (bar.value / maxValue) * 320]);

          return (
            <div
              key={idx}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                width: 140,
              }}
            >
              <span
                style={{
                  fontSize: 28,
                  fontWeight: 800,
                  color: bar.color,
                  marginBottom: 10,
                }}
              >
                {Math.round(interpolate(progress, [0, 1], [0, bar.value]))}%
              </span>

              <div
                style={{
                  width: "100%",
                  height: `${barHeight}px`,
                  backgroundColor: bar.color,
                  borderRadius: "10px 10px 0 0",
                  boxShadow: `0 0 25px ${bar.color}40`,
                }}
              />

              <span
                style={{
                  marginTop: 16,
                  fontSize: 22,
                  fontWeight: 600,
                  color: "#94a3b8",
                  textAlign: "center",
                }}
              >
                {bar.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
