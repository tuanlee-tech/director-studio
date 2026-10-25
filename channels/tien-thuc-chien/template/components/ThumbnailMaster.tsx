import React from "react";
import { AbsoluteFill, staticFile } from "remotion";
import { theme } from "../theme";

export interface ThumbnailProps {
  title_line1?: string;
  title_line2?: string;
  character_pose?: string; // e.g. "cutting", "shock", "confident", or direct URL
  debt_start?: string;
  debt_target?: string;
  time_frame?: string;
  badge_text?: string;
  proof_text?: string;
  channel_name?: string;
  character_position?: "left" | "right";
}

export const ThumbnailMaster: React.FC<ThumbnailProps> = ({
  title_line1 = "THOÁT BẪY NỢ",
  title_line2 = "THẺ TÍN DỤNG",
  character_pose = "cutting",
  debt_start = "40 TRIỆU",
  debt_target = "0 ĐỒNG!",
  time_frame = "SAU 10 THÁNG",
  badge_text = "TIỀN THỰC CHIẾN • QUY TRÌNH 4 BƯỚC",
  proof_text = "Áp dụng cho thu nhập 10 - 12 triệu/tháng",
  channel_name = "tien-thuc-chien",
  character_position = "left",
}) => {
  // Resolve character image path
  const characterSrc =
    character_pose.startsWith("http") ||
    character_pose.startsWith("/") ||
    character_pose.startsWith("data:")
      ? character_pose
      : staticFile(`channels/${channel_name}/characters/${character_pose}.png`);

  const isLeft = character_position === "left";

  const CharacterBlock = (
    <div
      key="character-block"
      style={{
        flex: "0 0 44%",
        display: "flex",
        alignItems: "flex-end",
        justifyContent: "center",
        position: "relative",
        height: "100%",
        paddingBottom: 20,
      }}
    >
      {/* Background Aura behind character */}
      <div
        style={{
          position: "absolute",
          bottom: "10%",
          width: 500,
          height: 500,
          borderRadius: "50%",
          background: isLeft
            ? "radial-gradient(circle, rgba(56, 189, 248, 0.22) 0%, rgba(5,8,20,0) 70%)"
            : "radial-gradient(circle, rgba(239, 68, 68, 0.22) 0%, rgba(5,8,20,0) 70%)",
          filter: "blur(50px)",
          pointerEvents: "none",
        }}
      />

      {/* Character Image with Vox-style thick white sticker outline & shadow */}
      {characterSrc && (
        <img
          src={characterSrc}
          alt="Character Cutout"
          style={{
            maxHeight: "98%",
            maxWidth: "100%",
            objectFit: "contain",
            // Vox-style sticker effect: crisp multi-layer white outline + heavy shadow
            filter: `
              drop-shadow(-5px -5px 0 #ffffff)
              drop-shadow(5px -5px 0 #ffffff)
              drop-shadow(-5px 5px 0 #ffffff)
              drop-shadow(5px 5px 0 #ffffff)
              drop-shadow(0 25px 40px rgba(0,0,0,0.95))
            `,
          }}
          onError={(e) => {
            (e.currentTarget as HTMLElement).style.display = "none";
          }}
        />
      )}
    </div>
  );

  const TextBlock = (
    <div
      key="text-block"
      style={{
        flex: "0 0 56%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "flex-start",
        paddingLeft: isLeft ? 20 : 0,
        paddingRight: isLeft ? 20 : 20,
      }}
    >
      {/* Authority Tag Pill */}
      <div
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 12,
          padding: "10px 24px",
          borderRadius: 40,
          backgroundColor: "rgba(250, 204, 21, 0.15)",
          border: "2.5px solid rgba(250, 204, 21, 0.75)",
          boxShadow: "0 0 25px rgba(250, 204, 21, 0.35)",
          marginBottom: 24,
        }}
      >
        <span style={{ fontSize: 26 }}>🔥</span>
        <span
          style={{
            color: "#fde047",
            fontSize: 22,
            fontWeight: 900,
            letterSpacing: "0.08em",
            textTransform: "uppercase",
          }}
        >
          {badge_text}
        </span>
      </div>

      {/* Massive 3D Headline */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          lineHeight: 1.04,
          marginBottom: 28,
        }}
      >
        <span
          style={{
            fontSize: 106,
            fontWeight: 900,
            color: "#FFE600",
            letterSpacing: "-0.03em",
            textTransform: "uppercase",
            textShadow: `
              -4px -4px 0 #000, 4px -4px 0 #000, -4px 4px 0 #000, 4px 4px 0 #000,
              0 0 35px rgba(255, 230, 0, 0.8), 0 12px 28px rgba(0,0,0,0.95)
            `,
          }}
        >
          {title_line1}
        </span>
        <span
          style={{
            fontSize: 92,
            fontWeight: 900,
            color: "#FFFFFF",
            letterSpacing: "-0.02em",
            textTransform: "uppercase",
            marginTop: 6,
            textShadow: `
              -4px -4px 0 #000, 4px -4px 0 #000, -4px 4px 0 #000, 4px 4px 0 #000,
              0 10px 25px rgba(0,0,0,0.9)
            `,
          }}
        >
          {title_line2}
        </span>
      </div>

      {/* Milestone Comparison Badges */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 16,
          marginBottom: 28,
        }}
      >
        {/* Start Debt Badge */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            padding: "12px 26px",
            borderRadius: 16,
            backgroundColor: "rgba(239, 68, 68, 0.22)",
            border: "3px solid #ef4444",
            boxShadow: "0 0 30px rgba(239, 68, 68, 0.45)",
          }}
        >
          <span style={{ fontSize: 16, fontWeight: 800, color: "#fca5a5", letterSpacing: "0.05em" }}>
            DƯ NỢ GỐC
          </span>
          <span
            style={{
              fontSize: 40,
              fontWeight: 900,
              color: "#ff4d4f",
              letterSpacing: "-0.02em",
              textShadow: "-2px -2px 0 #000, 2px 2px 0 #000",
            }}
          >
            {debt_start}
          </span>
        </div>

        {/* Glowing Arrow */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: 52,
            height: 52,
            borderRadius: "50%",
            backgroundColor: "#1e293b",
            border: "2px solid #64748b",
            boxShadow: "0 4px 16px rgba(0,0,0,0.6)",
          }}
        >
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fde047" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
            <path d="M5 12h14" />
            <path d="M12 5l7 7-7 7" />
          </svg>
        </div>

        {/* Target Freedom Badge */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            padding: "12px 26px",
            borderRadius: 16,
            backgroundColor: "rgba(16, 185, 129, 0.22)",
            border: "3px solid #10b981",
            boxShadow: "0 0 35px rgba(16, 185, 129, 0.55)",
          }}
        >
          <span style={{ fontSize: 16, fontWeight: 800, color: "#6ee7b7", letterSpacing: "0.05em" }}>
            {time_frame}
          </span>
          <span
            style={{
              fontSize: 40,
              fontWeight: 900,
              color: "#10b981",
              letterSpacing: "-0.02em",
              textShadow: "-2px -2px 0 #000, 2px 2px 0 #000",
            }}
          >
            {debt_target}
          </span>
        </div>
      </div>

      {/* Social Proof Pill */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          padding: "10px 22px",
          borderRadius: 30,
          backgroundColor: "rgba(255, 255, 255, 0.08)",
          border: "1px solid rgba(255, 255, 255, 0.16)",
          backdropFilter: "blur(10px)",
        }}
      >
        <span style={{ color: "#10b981", fontSize: 24, fontWeight: 900 }}>✓</span>
        <span style={{ color: "#e2e8f0", fontSize: 20, fontWeight: 700 }}>
          {proof_text}
        </span>
      </div>
    </div>
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#050814",
        fontFamily: theme.typography.fontFamily,
        color: "#ffffff",
        overflow: "hidden",
        position: "relative",
        display: "flex",
        flexDirection: "row",
      }}
    >
      {/* Dynamic Lighting Flares */}
      <div
        style={{
          position: "absolute",
          top: "-15%",
          left: isLeft ? "-5%" : "45%",
          width: "55%",
          height: "80%",
          background: isLeft
            ? "radial-gradient(circle, rgba(56, 189, 248, 0.28) 0%, rgba(5, 8, 20, 0) 70%)"
            : "radial-gradient(circle, rgba(239, 68, 68, 0.32) 0%, rgba(5, 8, 20, 0) 70%)",
          filter: "blur(70px)",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: "10%",
          right: isLeft ? "10%" : "30%",
          width: "50%",
          height: "75%",
          background: "radial-gradient(circle, rgba(250, 204, 21, 0.22) 0%, rgba(5, 8, 20, 0) 70%)",
          filter: "blur(60px)",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: "-20%",
          right: isLeft ? "5%" : "-10%",
          width: "55%",
          height: "80%",
          background: "radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, rgba(5, 8, 20, 0) 70%)",
          filter: "blur(80px)",
          pointerEvents: "none",
        }}
      />

      {/* Financial Geometric Grid */}
      <svg
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          opacity: 0.08,
          pointerEvents: "none",
        }}
      >
        <defs>
          <pattern id="thumb-master-grid" width="60" height="60" patternUnits="userSpaceOnUse">
            <path d="M 60 0 L 0 0 0 60" fill="none" stroke="#ffffff" strokeWidth="1" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#thumb-master-grid)" />
      </svg>

      {/* Main Split-Screen Container */}
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          width: "100%",
          height: "100%",
          zIndex: 10,
          padding: "50px 60px",
          boxSizing: "border-box",
        }}
      >
        {isLeft ? [CharacterBlock, TextBlock] : [TextBlock, CharacterBlock]}
      </div>
    </AbsoluteFill>
  );
};
