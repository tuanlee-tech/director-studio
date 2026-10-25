import React from "react";
import { interpolate, useCurrentFrame, spring, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/BeVietnamPro";

const { fontFamily } = loadFont("normal", {
  weights: ["600", "700", "900"],
  subsets: ["vietnamese", "latin"],
  ignoreTooManyRequestsWarning: true,
});

interface CounterNumberProps {
  from?: number;
  to?: number;
  label?: string;
  prefix?: string;
  suffix?: string;
  durationInFrames?: number;
}

export const CounterNumber: React.FC<CounterNumberProps> = ({
  from = 0,
  to = 50000000,
  label = "Dư nợ tín dụng thực tế",
  prefix = "",
  suffix = " VNĐ",
  durationInFrames = 90,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: {
      damping: 14,
      mass: 0.6,
      stiffness: 80,
    },
  });

  const rawValue = interpolate(progress, [0, 1], [from, to]);
  const currentValue = progress >= 0.98 ? to : Math.round(rawValue);
  const formattedNumber = new Intl.NumberFormat("vi-VN").format(currentValue);

  const displayLabel = label.replace(/^CounterNumber:\s*/i, "").trim();

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
        background: "radial-gradient(ellipse at center, #1a2236 0%, #080c16 80%)",
        color: "#ffffff",
        fontFamily,
      }}
    >
      <div
        style={{
          fontSize: 32,
          fontWeight: 700,
          color: "#94a3b8",
          textTransform: "uppercase",
          letterSpacing: "0.15em",
          marginBottom: 16,
          fontFamily,
        }}
      >
        {displayLabel}
      </div>
      <div
        style={{
          fontSize: 88,
          fontWeight: 900,
          color: "#ef4444",
          textShadow: "0 0 35px rgba(239, 68, 68, 0.45)",
          letterSpacing: "-0.03em",
        }}
      >
        {prefix}
        {formattedNumber}
        {suffix}
      </div>
    </div>
  );
};
