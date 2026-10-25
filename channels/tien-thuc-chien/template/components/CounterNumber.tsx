import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";

interface CounterNumberProps {
  from?: number;
  to: number;
  durationInFrames?: number;
  label?: string;
  prefix?: string;
  suffix?: string;
  decimals?: number;
  color?: string;
}

export const CounterNumber: React.FC<CounterNumberProps> = ({
  from = 0,
  to,
  durationInFrames = 90,
  label,
  prefix = "",
  suffix = "",
  decimals = 0,
  color,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.8, stiffness: 100 },
  });

  const rawCurrent = interpolate(progress, [0, 1], [from, to] as readonly number[]);
  const current = progress >= 0.98 ? to : Math.round(rawCurrent);

  const formattedNumber = current.toLocaleString("vi-VN", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });

  const isDanger = to >= 1000000 || suffix.includes("%");
  const numColor = color || (isDanger ? theme.colors.danger : theme.colors.gold);

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
          width: 1100,
          backgroundColor: theme.colors.cardBg,
          border: `2px solid ${numColor}`,
          borderRadius: 28,
          boxShadow: `0 20px 60px rgba(0, 0, 0, 0.7), 0 0 40px ${numColor}40`,
          padding: "52px 64px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
        }}
      >
        {label && (
          <div
            style={{
              fontSize: 28,
              fontWeight: 800,
              color: theme.colors.textSecondary,
              textTransform: "uppercase",
              letterSpacing: "0.15em",
              marginBottom: 24,
            }}
          >
            {label}
          </div>
        )}

        <div
          style={{
            fontSize: 76,
            fontWeight: 900,
            color: numColor,
            letterSpacing: "-0.03em",
            textShadow: `0 0 35px ${numColor}80`,
          }}
        >
          {prefix}
          {formattedNumber}
          {suffix}
        </div>
      </div>
    </div>
  );
};
