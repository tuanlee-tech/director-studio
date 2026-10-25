import React from "react";
import { useCurrentFrame, useVideoConfig, spring } from "remotion";
import { theme } from "../theme";

interface ChartBar {
  label: string;
  value: number;
  color?: string;
  formattedValue?: string;
}

interface ChartMotionProps {
  type?: "bar" | "pie";
  title?: string;
  subtitle?: string;
  bars?: ChartBar[];
  durationInFrames: number;
}

export const ChartMotion: React.FC<ChartMotionProps> = ({
  type = "bar",
  title = "So Sánh Lãi Suất",
  subtitle,
  bars = [
    { label: "Vay Mua Nhà", value: 6, color: "#38bdf8", formattedValue: "6% / Năm" },
    { label: "Thẻ Tín Dụng", value: 35, color: "#ef4444", formattedValue: "35% / Năm!" },
  ],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const animProgress = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.8, stiffness: 120 },
  });

  const maxValue = Math.max(...bars.map((b) => b.value), 40);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: theme.colors.background,
        padding: 40,
        fontFamily: theme.typography.fontFamily,
      }}
    >
      <div
        style={{
          width: 1180,
          backgroundColor: theme.colors.cardBg,
          border: `2px solid ${theme.colors.cardBorder}`,
          borderRadius: 28,
          boxShadow: theme.shadows.subtle,
          padding: "44px 56px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        {/* Tag */}
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 8,
            padding: "8px 20px",
            borderRadius: 9999,
            backgroundColor: "rgba(56, 189, 248, 0.12)",
            border: "1px solid rgba(56, 189, 248, 0.3)",
            color: "#38bdf8",
            fontSize: 15,
            fontWeight: 800,
            letterSpacing: "0.1em",
            textTransform: "uppercase",
            marginBottom: 20,
          }}
        >
          <span>📊</span> BẢN ĐỒ LÃI SUẤT TÀI CHÍNH
        </div>

        {/* Title - Fixed margin prevents any collision */}
        <div
          style={{
            fontSize: 42,
            fontWeight: 900,
            color: "#ffffff",
            textAlign: "center",
            lineHeight: 1.25,
            marginBottom: 10,
          }}
        >
          {title}
        </div>

        {subtitle && (
          <div
            style={{
              fontSize: 20,
              color: theme.colors.textSecondary,
              textAlign: "center",
              marginBottom: 36,
            }}
          >
            {subtitle}
          </div>
        )}

        {/* Chart Area with generous height (340px) */}
        <div
          style={{
            display: "flex",
            alignItems: "flex-end",
            justifyContent: "center",
            gap: 80,
            height: 320,
            width: "80%",
            marginTop: 20,
            paddingBottom: 16,
            borderBottom: "2px solid #334155",
          }}
        >
          {bars.map((bar, idx) => {
            const barHeight = Math.max(20, (bar.value / maxValue) * 220 * animProgress);
            const isHighlight = bar.value >= 30;

            return (
              <div
                key={idx}
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  flex: 1,
                  maxWidth: 220,
                }}
              >
                {/* Metric value with ample buffer space above bar */}
                <div
                  style={{
                    fontSize: isHighlight ? 36 : 28,
                    fontWeight: 900,
                    color: bar.color || "#ffffff",
                    marginBottom: 12,
                    textShadow: isHighlight ? "0 0 20px rgba(239, 68, 68, 0.8)" : "none",
                  }}
                >
                  {bar.formattedValue || `${bar.value}% / Năm`}
                </div>

                {/* Animated Bar */}
                <div
                  style={{
                    width: isHighlight ? 170 : 150,
                    height: barHeight,
                    backgroundColor: bar.color || "#38bdf8",
                    background: isHighlight
                      ? "linear-gradient(180deg, #ef4444 0%, #991b1b 100%)"
                      : "linear-gradient(180deg, #38bdf8 0%, #0284c7 100%)",
                    borderRadius: "14px 14px 0 0",
                    boxShadow: isHighlight
                      ? "0 0 35px rgba(239, 68, 68, 0.6)"
                      : "0 0 20px rgba(56, 189, 248, 0.4)",
                    transition: "height 0.05s ease-out",
                  }}
                />

                {/* Bar Label */}
                <div
                  style={{
                    fontSize: isHighlight ? 24 : 20,
                    fontWeight: isHighlight ? 900 : 700,
                    color: isHighlight ? "#f87171" : "#94a3b8",
                    marginTop: 16,
                    textAlign: "center",
                  }}
                >
                  {bar.label}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
