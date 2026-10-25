import React from "react";
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

interface BarData {
  label: string;
  value: number;
  color: string;
}

interface ChartMotionProps {
  title?: string;
  data?: BarData[];
}

export const ChartMotion: React.FC<ChartMotionProps> = ({
  title = "So sánh Chi phí Cơ hội",
  data = [
    { label: "Tiêu xài thẻ tín dụng", value: 300, color: "#FF4D4D" },
    { label: "Tích sản quỹ mở 10 năm", value: 850, color: "#00B050" },
  ],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const maxValue = Math.max(...data.map((d) => d.value));

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: "#0F172A",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: 60,
      }}
    >
      <h2 style={{ color: "#F8FAFC", fontSize: 48, marginBottom: 50 }}>
        {title}
      </h2>
      <div
        style={{
          display: "flex",
          gap: 60,
          alignItems: "flex-end",
          height: 400,
          width: 800,
          borderBottom: "4px solid #475569",
          paddingBottom: 10,
        }}
      >
        {data.map((item, index) => {
          const delay = index * 8;
          const grow = spring({
            frame: Math.max(0, frame - delay),
            fps,
            config: { damping: 14, mass: 0.6, stiffness: 90 },
          });

          const heightPercent = (item.value / maxValue) * 100 * grow;

          return (
            <div
              key={index}
              style={{
                flex: 1,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                height: "100%",
                justifyContent: "flex-end",
              }}
            >
              <div
                style={{
                  color: item.color,
                  fontSize: 32,
                  fontWeight: "bold",
                  marginBottom: 10,
                }}
              >
                {Math.round(item.value * grow)} Tr
              </div>
              <div
                style={{
                  width: "100%",
                  height: `${heightPercent}%`,
                  backgroundColor: item.color,
                  borderRadius: "8px 8px 0 0",
                  boxShadow: `0 0 20px ${item.color}88`,
                }}
              />
              <div
                style={{
                  color: "#CBD5E1",
                  fontSize: 22,
                  marginTop: 15,
                  textAlign: "center",
                }}
              >
                {item.label}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
