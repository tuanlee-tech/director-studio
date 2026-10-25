import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { theme } from "../theme";

interface TreeGrowthProps {
  title?: string;
  themeName?: string;
  durationInFrames: number;
}

export const TreeGrowth: React.FC<TreeGrowthProps> = ({ durationInFrames }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Spring animation for trunk and branches
  const trunkProgress = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.8, stiffness: 100 },
  });

  const branchLeftProgress = spring({
    frame: Math.max(0, frame - 15),
    fps,
    config: { damping: 12, mass: 0.6, stiffness: 120 },
  });

  const branchRightProgress = spring({
    frame: Math.max(0, frame - 28),
    fps,
    config: { damping: 12, mass: 0.6, stiffness: 120 },
  });

  const branchCenterProgress = spring({
    frame: Math.max(0, frame - 40),
    fps,
    config: { damping: 12, mass: 0.6, stiffness: 120 },
  });

  // Pulse effect for red warning glow
  const pulse = Math.sin(frame * 0.15) * 0.08 + 1.0;

  // Shrinking of salary sprouts as debt branches engulf them
  const sproutScale = interpolate(frame, [25, 75], [1.0, 0.45], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const sproutOpacity = interpolate(frame, [30, 80], [1.0, 0.35], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

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
          width: 1240,
          backgroundColor: theme.colors.cardBg,
          border: `2px solid ${theme.colors.danger}`,
          borderRadius: 28,
          boxShadow: `0 20px 60px rgba(0, 0, 0, 0.7), ${theme.shadows.neonRed}`,
          padding: "36px 48px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          position: "relative",
          overflow: "hidden",
        }}
      >
        {/* Header Tag */}
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 10,
            padding: "8px 20px",
            borderRadius: 9999,
            backgroundColor: "rgba(239, 68, 68, 0.15)",
            border: "1px solid rgba(239, 68, 68, 0.4)",
            color: "#fca5a5",
            fontSize: 15,
            fontWeight: 800,
            letterSpacing: "0.1em",
            textTransform: "uppercase",
            marginBottom: 16,
          }}
        >
          <span>🌱 ➔ 🥀</span> BẪY LÃI MẸ ĐẺ LÃI CON
        </div>

        {/* Main Title - Decoupled with generous margins */}
        <div
          style={{
            fontSize: 40,
            fontWeight: 900,
            color: "#ffffff",
            textAlign: "center",
            lineHeight: 1.25,
            marginBottom: 8,
          }}
        >
          CÂY LÃI SUẤT 35%/NĂM NUỐT CHỬNG TIỀN LƯƠNG
        </div>
        <div
          style={{
            fontSize: 20,
            color: theme.colors.textSecondary,
            textAlign: "center",
            marginBottom: 28,
          }}
        >
          Lãi mẹ sinh lãi con theo cấp số nhân, rút cạn từng đồng thu nhập của bạn
        </div>

        {/* Visual Animated SVG Tree Canvas */}
        <div
          style={{
            width: "100%",
            height: 400,
            position: "relative",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <svg
            viewBox="0 0 1000 420"
            style={{ width: "100%", height: "100%", overflow: "visible" }}
          >
            <defs>
              <linearGradient id="trunkGrad" x1="0" y1="1" x2="0" y2="0">
                <stop offset="0%" stopColor="#1e293b" />
                <stop offset="100%" stopColor="#7f1d1d" />
              </linearGradient>
              <linearGradient id="branchRed" x1="0" y1="1" x2="1" y2="0">
                <stop offset="0%" stopColor="#ef4444" />
                <stop offset="100%" stopColor="#dc2626" />
              </linearGradient>
              <filter id="neonRedGlow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="8" result="blur" />
                <feMerge>
                  <feMergeNode in="blur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>

            {/* Tree Base / Soil */}
            <ellipse cx="500" cy="390" rx="220" ry="24" fill="#0f172a" stroke="#334155" strokeWidth="3" />

            {/* Main Trunk (Gốc Nợ) */}
            <path
              d="M 470 380 Q 485 280 490 220 L 510 220 Q 515 280 530 380 Z"
              fill="url(#trunkGrad)"
              stroke="#ef4444"
              strokeWidth="3"
              style={{
                transformOrigin: "500px 380px",
                transform: `scaleY(${trunkProgress})`,
              }}
            />

            {/* Left Branch: Lãi Suất 35% */}
            <path
              d="M 490 230 Q 380 180 280 120 Q 240 100 200 110"
              fill="none"
              stroke="url(#branchRed)"
              strokeWidth="14"
              strokeLinecap="round"
              filter="url(#neonRedGlow)"
              strokeDasharray="400"
              strokeDashoffset={400 * (1 - branchLeftProgress)}
            />
            {/* Thorny thorns on left branch */}
            {branchLeftProgress > 0.6 && (
              <>
                <path d="M 390 188 L 395 155 L 380 183 Z" fill="#ef4444" />
                <path d="M 310 140 L 305 110 L 298 136 Z" fill="#ef4444" />
              </>
            )}

            {/* Right Branch: Phí Thường Niên */}
            <path
              d="M 510 230 Q 620 180 720 120 Q 760 100 800 110"
              fill="none"
              stroke="url(#branchRed)"
              strokeWidth="14"
              strokeLinecap="round"
              filter="url(#neonRedGlow)"
              strokeDasharray="400"
              strokeDashoffset={400 * (1 - branchRightProgress)}
            />
            {/* Thorny thorns on right branch */}
            {branchRightProgress > 0.6 && (
              <>
                <path d="M 610 188 L 605 155 L 620 183 Z" fill="#ef4444" />
                <path d="M 690 140 L 695 110 L 702 136 Z" fill="#ef4444" />
              </>
            )}

            {/* Center Branch: Phạt Trễ Hạn */}
            <path
              d="M 500 220 Q 500 150 500 80"
              fill="none"
              stroke="url(#branchRed)"
              strokeWidth="12"
              strokeLinecap="round"
              filter="url(#neonRedGlow)"
              strokeDasharray="200"
              strokeDashoffset={200 * (1 - branchCenterProgress)}
            />
          </svg>

          {/* Root Badge: Gốc nợ 40 Triệu */}
          <div
            style={{
              position: "absolute",
              bottom: 12,
              backgroundColor: "rgba(15, 23, 42, 0.95)",
              border: "2px solid #ef4444",
              borderRadius: 14,
              padding: "8px 24px",
              color: "#f87171",
              fontWeight: 900,
              fontSize: 22,
              boxShadow: "0 0 25px rgba(239, 68, 68, 0.5)",
            }}
          >
            💳 GỐC NỢ: 40.000.000 VNĐ
          </div>

          {/* Engulfed Salary Sprouts (Left) */}
          <div
            style={{
              position: "absolute",
              left: 100,
              top: 50,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              transform: `scale(${sproutScale})`,
              opacity: sproutOpacity,
              transition: "all 0.1s ease",
            }}
          >
            <div style={{ fontSize: 44 }}>🌱 💵</div>
            <div
              style={{
                backgroundColor: "rgba(16, 185, 129, 0.2)",
                border: "1px solid #10b981",
                borderRadius: 8,
                padding: "4px 10px",
                color: "#34d399",
                fontWeight: 800,
                fontSize: 16,
                marginTop: 4,
              }}
            >
              Tiền Lương Tháng
            </div>
            {branchLeftProgress > 0.8 && (
              <div
                style={{
                  color: "#ef4444",
                  fontSize: 13,
                  fontWeight: 900,
                  marginTop: 2,
                  textTransform: "uppercase",
                }}
              >
                [ Bị Nuốt Chửng ]
              </div>
            )}
          </div>

          {/* Engulfed Living Cost Sprouts (Right) */}
          <div
            style={{
              position: "absolute",
              right: 100,
              top: 50,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              transform: `scale(${sproutScale})`,
              opacity: sproutOpacity,
              transition: "all 0.1s ease",
            }}
          >
            <div style={{ fontSize: 44 }}>🌱 🪙</div>
            <div
              style={{
                backgroundColor: "rgba(16, 185, 129, 0.2)",
                border: "1px solid #10b981",
                borderRadius: 8,
                padding: "4px 10px",
                color: "#34d399",
                fontWeight: 800,
                fontSize: 16,
                marginTop: 4,
              }}
            >
              Tiền Tích Lũy
            </div>
            {branchRightProgress > 0.8 && (
              <div
                style={{
                  color: "#ef4444",
                  fontSize: 13,
                  fontWeight: 900,
                  marginTop: 2,
                  textTransform: "uppercase",
                }}
              >
                [ Bốc Hơi Hết ]
              </div>
            )}
          </div>

          {/* Floating Metric Badges on Branches */}
          {branchLeftProgress > 0.4 && (
            <div
              style={{
                position: "absolute",
                left: 230,
                top: 140,
                backgroundColor: "rgba(220, 38, 38, 0.95)",
                border: "2px solid #ffffff",
                borderRadius: 12,
                padding: "6px 16px",
                color: "#ffffff",
                fontWeight: 900,
                fontSize: 18,
                transform: `scale(${pulse})`,
                boxShadow: "0 0 20px #ef4444",
              }}
            >
              🔥 LÃI SUẤT 35%/NĂM
            </div>
          )}

          {branchCenterProgress > 0.4 && (
            <div
              style={{
                position: "absolute",
                top: 40,
                backgroundColor: "rgba(220, 38, 38, 0.95)",
                border: "2px solid #ffffff",
                borderRadius: 12,
                padding: "6px 16px",
                color: "#ffffff",
                fontWeight: 900,
                fontSize: 18,
                transform: `scale(${pulse})`,
                boxShadow: "0 0 20px #ef4444",
              }}
            >
              ⚠️ PHẠT QUÁ HẠN 45%
            </div>
          )}

          {branchRightProgress > 0.4 && (
            <div
              style={{
                position: "absolute",
                right: 230,
                top: 140,
                backgroundColor: "rgba(220, 38, 38, 0.95)",
                border: "2px solid #ffffff",
                borderRadius: 12,
                padding: "6px 16px",
                color: "#ffffff",
                fontWeight: 900,
                fontSize: 18,
                transform: `scale(${pulse})`,
                boxShadow: "0 0 20px #ef4444",
              }}
            >
              💸 LÃI MẸ ĐẺ LÃI CON
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
