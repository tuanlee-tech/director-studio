import React from "react";
import { AbsoluteFill } from "remotion";
import { theme } from "../theme";

export const Thumbnail: React.FC = () => {
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
      {/* Background Ambience & Lighting Flares */}
      <div
        style={{
          position: "absolute",
          top: "-15%",
          left: "-10%",
          width: "55%",
          height: "80%",
          background: "radial-gradient(circle, rgba(239, 68, 68, 0.28) 0%, rgba(5, 8, 20, 0) 70%)",
          filter: "blur(70px)",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: "-20%",
          right: "5%",
          width: "60%",
          height: "85%",
          background: "radial-gradient(circle, rgba(16, 185, 129, 0.25) 0%, rgba(5, 8, 20, 0) 70%)",
          filter: "blur(80px)",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: "10%",
          right: "30%",
          width: "40%",
          height: "60%",
          background: "radial-gradient(circle, rgba(250, 204, 21, 0.18) 0%, rgba(5, 8, 20, 0) 70%)",
          filter: "blur(60px)",
          pointerEvents: "none",
        }}
      />

      {/* Subtle Financial Background Grid Pattern */}
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
          <pattern id="thumb-grid" width="60" height="60" patternUnits="userSpaceOnUse">
            <path d="M 60 0 L 0 0 0 60" fill="none" stroke="#ffffff" strokeWidth="1" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#thumb-grid)" />
      </svg>

      {/* Main Content Container - 2 Columns (Text & Visual) */}
      <div
        style={{
          display: "flex",
          width: "100%",
          height: "100%",
          zIndex: 10,
          padding: "70px 80px",
          boxSizing: "border-box",
        }}
      >
        {/* LEFT COLUMN: Ultra High-Impact Headline & Badges (62% Width) */}
        <div
          style={{
            flex: "0 0 62%",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "flex-start",
            paddingRight: 40,
          }}
        >
          {/* Top Pill: Channel Tag & Authority */}
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 12,
              padding: "10px 24px",
              borderRadius: 40,
              backgroundColor: "rgba(250, 204, 21, 0.15)",
              border: "2px solid rgba(250, 204, 21, 0.6)",
              boxShadow: "0 0 25px rgba(250, 204, 21, 0.35)",
              marginBottom: 28,
            }}
          >
            <span style={{ fontSize: 28 }}>🔥</span>
            <span
              style={{
                color: "#fde047",
                fontSize: 24,
                fontWeight: 900,
                letterSpacing: "0.08em",
                textTransform: "uppercase",
              }}
            >
              TIỀN THỰC CHIẾN • QUY TRÌNH 4 BƯỚC
            </span>
          </div>

          {/* MAIN MASSIVE HEADLINE (3 Lines with extreme contrast) */}
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              lineHeight: 1.05,
              marginBottom: 32,
            }}
          >
            {/* Line 1: THOÁT BẪY NỢ */}
            <span
              style={{
                fontSize: 104,
                fontWeight: 900,
                color: "#FFE600",
                letterSpacing: "-0.03em",
                textTransform: "uppercase",
                textShadow: `
                  -4px -4px 0 #000, 4px -4px 0 #000, -4px 4px 0 #000, 4px 4px 0 #000,
                  0 0 35px rgba(255, 230, 0, 0.75), 0 12px 28px rgba(0,0,0,0.95)
                `,
              }}
            >
              THOÁT BẪY NỢ
            </span>

            {/* Line 2: THẺ TÍN DỤNG */}
            <span
              style={{
                fontSize: 92,
                fontWeight: 900,
                color: "#FFFFFF",
                letterSpacing: "-0.02em",
                textTransform: "uppercase",
                marginTop: 4,
                textShadow: `
                  -4px -4px 0 #000, 4px -4px 0 #000, -4px 4px 0 #000, 4px 4px 0 #000,
                  0 10px 25px rgba(0,0,0,0.9)
                `,
              }}
            >
              THẺ TÍN DỤNG
            </span>
          </div>

          {/* DUAL CONTRAST PILL: 40 TRIỆU -> 0 ĐỒNG */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 16,
              marginBottom: 32,
            }}
          >
            {/* Red Box: Nợ 40 Triệu */}
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                padding: "14px 28px",
                borderRadius: 18,
                backgroundColor: "rgba(239, 68, 68, 0.2)",
                border: "3px solid #ef4444",
                boxShadow: "0 0 30px rgba(239, 68, 68, 0.45)",
              }}
            >
              <span style={{ fontSize: 18, fontWeight: 800, color: "#fca5a5", letterSpacing: "0.05em" }}>
                DƯ NỢ GỐC
              </span>
              <span
                style={{
                  fontSize: 42,
                  fontWeight: 900,
                  color: "#ff4d4f",
                  letterSpacing: "-0.02em",
                  textShadow: "-2px -2px 0 #000, 2px 2px 0 #000",
                }}
              >
                40 TRIỆU
              </span>
            </div>

            {/* Glowing Arrow Transition */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                width: 58,
                height: 58,
                borderRadius: "50%",
                backgroundColor: "#1e293b",
                border: "2px solid #64748b",
                boxShadow: "0 4px 16px rgba(0,0,0,0.6)",
              }}
            >
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#fde047" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 12h14" />
                <path d="M12 5l7 7-7 7" />
              </svg>
            </div>

            {/* Green Box: Về 0 Đồng */}
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                padding: "14px 28px",
                borderRadius: 18,
                backgroundColor: "rgba(16, 185, 129, 0.2)",
                border: "3px solid #10b981",
                boxShadow: "0 0 35px rgba(16, 185, 129, 0.55)",
              }}
            >
              <span style={{ fontSize: 18, fontWeight: 800, color: "#6ee7b7", letterSpacing: "0.05em" }}>
                SAU 10 THÁNG
              </span>
              <span
                style={{
                  fontSize: 42,
                  fontWeight: 900,
                  color: "#10b981",
                  letterSpacing: "-0.02em",
                  textShadow: "-2px -2px 0 #000, 2px 2px 0 #000",
                }}
              >
                0 ĐỒNG!
              </span>
            </div>
          </div>

          {/* Social Proof Subtitle */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              padding: "10px 22px",
              borderRadius: 30,
              backgroundColor: "rgba(255, 255, 255, 0.08)",
              border: "1px solid rgba(255, 255, 255, 0.15)",
              backdropFilter: "blur(10px)",
            }}
          >
            <span style={{ color: "#10b981", fontSize: 24, fontWeight: 900 }}>✓</span>
            <span style={{ color: "#e2e8f0", fontSize: 22, fontWeight: 700 }}>
              Áp dụng thực tế cho người có thu nhập 10 - 12 triệu/tháng
            </span>
          </div>
        </div>

        {/* RIGHT COLUMN: Dramatic Graphic Centerpiece (38% Width) */}
        <div
          style={{
            flex: "0 0 38%",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            position: "relative",
          }}
        >
          {/* Main Visual: Big Vector SVG with Cut Credit Card & Scissors */}
          <div
            style={{
              position: "relative",
              width: "100%",
              maxWidth: 580,
              height: 520,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {/* Background Halo Glow */}
            <div
              style={{
                position: "absolute",
                width: 440,
                height: 440,
                borderRadius: "50%",
                background: "radial-gradient(circle, rgba(239, 68, 68, 0.4) 0%, rgba(245, 158, 11, 0.2) 50%, rgba(5,8,20,0) 80%)",
                filter: "blur(30px)",
              }}
            />

            <svg width="520" height="460" viewBox="0 0 520 460" fill="none">
              <defs>
                {/* Credit Card Left Gradient */}
                <linearGradient id="cardLeft" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#1e293b" />
                  <stop offset="100%" stopColor="#0f172a" />
                </linearGradient>
                {/* Credit Card Right Gradient */}
                <linearGradient id="cardRight" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#dc2626" />
                  <stop offset="100%" stopColor="#991b1b" />
                </linearGradient>
                {/* Gold Chip */}
                <linearGradient id="goldChip" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#fef08a" />
                  <stop offset="100%" stopColor="#ca8a04" />
                </linearGradient>
                {/* Neon Red Shadow */}
                <filter id="neonRedGlow" x="-20%" y="-20%" width="140%" height="140%">
                  <feDropShadow dx="0" dy="0" stdDeviation="14" floodColor="#ef4444" floodOpacity="0.8" />
                </filter>
                {/* Gold Glow */}
                <filter id="goldGlow" x="-20%" y="-20%" width="140%" height="140%">
                  <feDropShadow dx="0" dy="0" stdDeviation="16" floodColor="#facc15" floodOpacity="0.75" />
                </filter>
              </defs>

              {/* Stack of Gold Coins in background */}
              <g transform="translate(60, 240)">
                <ellipse cx="60" cy="110" rx="45" ry="18" fill="#ca8a04" />
                <rect x="15" y="95" width="90" height="15" fill="#eab308" />
                <ellipse cx="60" cy="95" rx="45" ry="18" fill="#fef08a" />
                
                <ellipse cx="60" cy="85" rx="45" ry="18" fill="#ca8a04" />
                <rect x="15" y="70" width="90" height="15" fill="#eab308" />
                <ellipse cx="60" cy="70" rx="45" ry="18" fill="#fef08a" />
                
                <ellipse cx="60" cy="60" rx="45" ry="18" fill="#ca8a04" />
                <rect x="15" y="45" width="90" height="15" fill="#eab308" />
                <ellipse cx="60" cy="45" rx="45" ry="18" fill="#fef08a" />
              </g>

              {/* Left Half of Cut Credit Card (Tilted left) */}
              <g transform="translate(40, 70) rotate(-14 170 120)">
                <rect
                  x="30"
                  y="40"
                  width="180"
                  height="220"
                  rx="18"
                  fill="url(#cardLeft)"
                  stroke="#475569"
                  strokeWidth="4"
                  filter="drop-shadow(0 15px 25px rgba(0,0,0,0.8))"
                />
                {/* Chip */}
                <rect x="65" y="80" width="48" height="38" rx="6" fill="url(#goldChip)" stroke="#a16207" strokeWidth="2" />
                <line x1="65" y1="99" x2="113" y2="99" stroke="#78350f" strokeWidth="1.5" />
                <line x1="89" y1="80" x2="89" y2="118" stroke="#78350f" strokeWidth="1.5" />
                
                {/* Card Number dots */}
                <circle cx="65" cy="160" r="5" fill="#94a3b8" />
                <circle cx="85" cy="160" r="5" fill="#94a3b8" />
                <circle cx="105" cy="160" r="5" fill="#94a3b8" />
                <circle cx="125" cy="160" r="5" fill="#94a3b8" />
                
                <rect x="65" y="195" width="80" height="10" rx="4" fill="#64748b" opacity="0.6" />
                
                {/* Jagged cut edge on right */}
                <path d="M 210 40 L 195 90 L 215 140 L 190 190 L 210 260" stroke="#ff4d4f" strokeWidth="5" fill="none" />
              </g>

              {/* Right Half of Cut Credit Card (Tilted right & falling) */}
              <g transform="translate(190, 95) rotate(18 200 130)">
                <rect
                  x="120"
                  y="40"
                  width="180"
                  height="220"
                  rx="18"
                  fill="url(#cardRight)"
                  stroke="#ef4444"
                  strokeWidth="4"
                  filter="url(#neonRedGlow)"
                />
                
                {/* Big 35% Stamp on Card */}
                <g transform="translate(145, 90)">
                  <rect x="0" y="0" width="130" height="48" rx="8" fill="#7f1d1d" stroke="#fca5a5" strokeWidth="2" />
                  <text x="65" y="33" fill="#ffffff" fontSize="24" fontWeight="900" textAnchor="middle" fontFamily="sans-serif">
                    LÃI 35%!
                  </text>
                </g>

                {/* Jagged cut edge on left */}
                <path d="M 120 40 L 105 90 L 125 140 L 100 190 L 120 260" stroke="#ff4d4f" strokeWidth="5" fill="none" />
              </g>

              {/* Cutting Sparks & Electric Bolts */}
              <g stroke="#fde047" strokeWidth="4" strokeLinecap="round">
                <line x1="220" y1="130" x2="205" y2="105" />
                <line x1="245" y1="170" x2="275" y2="155" />
                <line x1="210" y1="210" x2="185" y2="230" />
                <line x1="230" y1="250" x2="255" y2="275" />
              </g>
              <g fill="#ffe600">
                <circle cx="225" cy="150" r="7" filter="url(#goldGlow)" />
                <circle cx="215" cy="220" r="5" filter="url(#goldGlow)" />
                <circle cx="250" cy="190" r="6" filter="url(#goldGlow)" />
              </g>

              {/* Giant Stainless Steel Scissors Cutting Through */}
              <g transform="translate(140, 20) rotate(12 160 160)">
                {/* Scissor Upper Blade */}
                <path
                  d="M 140 180 L 290 85 C 300 78 310 92 300 102 L 175 195 Z"
                  fill="#f1f5f9"
                  stroke="#334155"
                  strokeWidth="3"
                  filter="drop-shadow(0 8px 16px rgba(0,0,0,0.7))"
                />
                {/* Scissor Lower Blade */}
                <path
                  d="M 140 195 L 290 285 C 300 292 310 278 300 268 L 175 180 Z"
                  fill="#cbd5e1"
                  stroke="#334155"
                  strokeWidth="3"
                  filter="drop-shadow(0 8px 16px rgba(0,0,0,0.7))"
                />
                {/* Golden Pivot Screw */}
                <circle cx="160" cy="188" r="14" fill="#facc15" stroke="#a16207" strokeWidth="3" />
                <circle cx="160" cy="188" r="6" fill="#78350f" />
                
                {/* Scissor Red Handles */}
                <ellipse cx="330" cy="70" rx="36" ry="24" fill="none" stroke="#ef4444" strokeWidth="16" />
                <ellipse cx="330" cy="295" rx="36" ry="24" fill="none" stroke="#ef4444" strokeWidth="16" />
              </g>

              {/* Emerald Green Financial Shield at bottom right */}
              <g transform="translate(300, 260)">
                <path
                  d="M 60 10 L 115 35 C 115 90 60 125 60 125 C 60 125 5 90 5 35 Z"
                  fill="#059669"
                  stroke="#34d399"
                  strokeWidth="5"
                  filter="drop-shadow(0 0 25px rgba(16, 185, 129, 0.8))"
                />
                {/* Checkmark in shield */}
                <path d="M 38 65 L 53 80 L 85 45" fill="none" stroke="#ffffff" strokeWidth="8" strokeLinecap="round" strokeLinejoin="round" />
              </g>
            </svg>
          </div>

          {/* Attention-Grabbing Badge at bottom of Graphic */}
          <div
            style={{
              marginTop: 10,
              padding: "12px 30px",
              borderRadius: 20,
              backgroundColor: "rgba(220, 38, 38, 0.95)",
              border: "3px solid #fecaca",
              boxShadow: "0 0 35px rgba(220, 38, 38, 0.7)",
              display: "flex",
              alignItems: "center",
              gap: 12,
            }}
          >
            <span style={{ fontSize: 26 }}>⚠️</span>
            <span
              style={{
                fontSize: 26,
                fontWeight: 900,
                color: "#ffffff",
                letterSpacing: "0.04em",
                textTransform: "uppercase",
                textShadow: "0 2px 8px rgba(0,0,0,0.8)",
              }}
            >
              CẢNH BÁO BẪY TỐI THIỂU
            </span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
