import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

interface CounterNumberProps {
  startValue?: number;
  endValue: number;
  prefix?: string;
  suffix?: string;
  durationFrames?: number;
  color?: string;
  label?: string;
}

export const CounterNumber: React.FC<CounterNumberProps> = ({
  startValue = 0,
  endValue,
  prefix = "",
  suffix = " VNĐ",
  durationFrames = 90,
  color = "#FF0000",
  label = "Tổng số tiền thất thoát",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: { damping: 15, mass: 0.8, stiffness: 80 },
  });

  const currentValue = Math.round(
    interpolate(progress, [0, 1], [startValue, endValue])
  );

  const formattedNumber = currentValue.toLocaleString("vi-VN");

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: "#0B132B",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div style={{ fontSize: 42, color: "#A0AEC0", marginBottom: 20 }}>
        {label}
      </div>
      <div
        style={{
          fontSize: 84,
          fontWeight: "bold",
          color,
          letterSpacing: 2,
        }}
      >
        {prefix}
        {formattedNumber}
        {suffix}
      </div>
    </div>
  );
};
