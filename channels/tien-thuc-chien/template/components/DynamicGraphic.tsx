import React from "react";
import { interpolate, useCurrentFrame, spring, useVideoConfig } from "remotion";
import { theme } from "../theme";
import { TreeGrowth } from "./TreeGrowth";
import { ChartMotion } from "./ChartMotion";
import { DynamicGraphicVideo2 } from "./DynamicGraphicVideo2";

interface DynamicGraphicProps {
  title?: string;
  label?: string;
  description?: string;
  component?: string;
  scene?: string;
  theme?: string;
  durationInFrames?: number;
  props?: Record<string, any>;
  narration?: string;
  [key: string]: any;
}

// Clean any developer or component prefixes from titles
export const cleanText = (t: string): string => {
  if (!t) return "";
  return t
    .replace(/^[A-Za-z0-9_]+(\s+[^\:]+)?:\s*/i, "")
    .replace(/^Tiêu đề\s*[\:\'\"]*/i, "")
    .replace(/[\'\"]$/g, "")
    .trim();
};

export const DynamicGraphic: React.FC<DynamicGraphicProps> = ({
  title = "",
  label = "",
  description = "",
  scene = "",
  component = "",
  durationInFrames = 120,
  props = {},
  narration = "",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const sc = (scene || "").toUpperCase();
  const comp = (component || "").toUpperCase();
  const rawText = cleanText(description || title || label || "");
  const cleanTitle = cleanText(title || description || "");

  // Spring animation for smooth card entrance
  const enterSpring = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.7, stiffness: 85 },
  });

  const scale = interpolate(enterSpring, [0, 1], [0.94, 1]);
  const opacity = interpolate(enterSpring, [0, 0.4], [0, 1]);
  const translateY = interpolate(enterSpring, [0, 1], [20, 0]);
  const animProgress = Math.min(1, Math.max(0, frame / (durationInFrames || 120)));

  // Delegate to DynamicGraphicVideo2 for video #2
  if (props?.videoSlug === "lam-phat-loi-song-luong-tang-tien-mat" || props?.slug === "lam-phat-loi-song-luong-tang-tien-mat") {
    return (
      <DynamicGraphicVideo2
        title={title}
        label={label}
        description={description}
        component={component}
        scene={scene}
        theme={theme}
        durationInFrames={durationInFrames}
        props={props}
        narration={narration}
      />
    );
  }


  // =========================================================================
  // --- 1. S006: ALERTBOX NGÂN HÀNG (BANNER MIỄN LÃI 45 NGÀY & ĐỒNG HỒ) ---
  // =========================================================================
  if (sc === "S006") {
    const countdown = Math.max(0, 45 - Math.floor(animProgress * 45));
    const clockRotate = (frame * 6) % 360;
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1160, border: "2px solid #38bdf8", boxShadow: "0 0 50px rgba(56, 189, 248, 0.25)" }}>
          <div style={tagStyle("#38bdf8", "#7dd3fc")}>
            <span>🏦</span> LỜI MỜI GỌI TỪ NGÂN HÀNG
          </div>
          <div style={headingStyle}>MIỄN LÃI 45 NGÀY — CHI TIÊU THẢ GA?</div>
          <div style={subheadStyle}>Cái bẫy bắt đầu bằng lời hứa miễn phí hấp dẫn, ru ngủ sự cảnh giác</div>

          {/* Visual: Bank Card with ticking clock */}
          <div style={{ display: "flex", gap: 36, alignItems: "center", marginTop: 24 }}>
            <div style={{ width: 440, height: 230, borderRadius: 20, background: "linear-gradient(135deg, #1e3a8a 0%, #0284c7 100%)", padding: 24, boxShadow: "0 15px 35px rgba(0,0,0,0.5)", border: "1px solid rgba(255,255,255,0.2)", display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ fontSize: 16, fontWeight: 800, color: "#e0f2fe", letterSpacing: "2px" }}>PLATINUM CREDIT</span>
                <span style={{ fontSize: 24 }}>💳</span>
              </div>
              <div style={{ fontSize: 28, fontWeight: 900, color: "#ffffff", letterSpacing: "1px" }}>45 NGÀY MIỄN LÃI</div>
              <div style={{ fontSize: 15, color: "#bae6fd" }}>Hạn mức: 40.000.000 VNĐ</div>
            </div>

            {/* Countdown Clock */}
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12 }}>
              <div style={{ position: "relative", width: 130, height: 130, borderRadius: "50%", border: "4px solid #38bdf8", display: "flex", alignItems: "center", justifyContent: "center", backgroundColor: "rgba(15, 23, 42, 0.8)", boxShadow: "0 0 30px rgba(56, 189, 248, 0.4)" }}>
                <svg viewBox="0 0 100 100" style={{ position: "absolute", width: "100%", height: "100%" }}>
                  <line x1="50" y1="50" x2="50" y2="20" stroke="#38bdf8" strokeWidth="4" strokeLinecap="round" transform={`rotate(${clockRotate} 50 50)`} />
                  <circle cx="50" cy="50" r="4" fill="#38bdf8" />
                </svg>
                <span style={{ fontSize: 32, fontWeight: 900, color: "#ffffff", zIndex: 2 }}>{countdown}</span>
              </div>
              <span style={{ fontSize: 16, fontWeight: 800, color: "#94a3b8", textTransform: "uppercase" }}>Ngày đếm ngược</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 2. S008: CHẠM THẺ KHÔNG CẢM GIÁC ĐAU VS RÚT TIỀN MẶT XÓT XA ---
  // =========================================================================
  if (sc === "S008") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1200 }}>
          <div style={tagStyle("#f59e0b", "#fde68a")}>
            <span>🧠</span> CẠM BẪY TÂM LÝ CHI TIÊU
          </div>
          <div style={headingStyle}>CẢM GIÁC ĐAU KHI MẤT TIỀN BỊ TRIỆT TIÊU</div>
          <div style={subheadStyle}>Não bộ không cảm nhận việc mất tài sản khi quẹt thẻ như khi rút tiền mặt</div>

          {/* Visual Dual Comparison */}
          <div style={{ display: "flex", gap: 32, width: "100%", marginTop: 28, justifyContent: "center" }}>
            {/* Left: Chạm Thẻ */}
            <div style={{ flex: 1, backgroundColor: "rgba(30, 41, 59, 0.7)", border: "2px solid #38bdf8", borderRadius: 24, padding: "28px 24px", display: "flex", flexDirection: "column", alignItems: "center" }}>
              <div style={{ fontSize: 56, marginBottom: 14 }}>💳</div>
              <div style={{ fontSize: 24, fontWeight: 900, color: "#38bdf8", marginBottom: 8 }}>CHẠM THẺ POS (1 GIÂY)</div>
              <div style={{ fontSize: 16, color: "#94a3b8", marginBottom: 18 }}>Chỉ là một tiếng "Tít" vô cảm</div>
              <div style={{ padding: "8px 18px", borderRadius: 999, backgroundColor: "rgba(56, 189, 248, 0.2)", color: "#7dd3fc", fontWeight: 800, fontSize: 15 }}>
                ❌ KHÔNG CẢM THẤY ĐAU
              </div>
            </div>

            {/* VS Badge */}
            <div style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
              <span style={{ fontSize: 22, fontWeight: 900, color: "#94a3b8", padding: "10px 16px", borderRadius: "50%", backgroundColor: "rgba(255,255,255,0.08)", border: "1px solid rgba(255,255,255,0.2)" }}>VS</span>
            </div>

            {/* Right: Tiền Mặt */}
            <div style={{ flex: 1, backgroundColor: "rgba(30, 41, 59, 0.7)", border: "2px solid #ef4444", borderRadius: 24, padding: "28px 24px", display: "flex", flexDirection: "column", alignItems: "center" }}>
              <div style={{ fontSize: 56, marginBottom: 14 }}>💵</div>
              <div style={{ fontSize: 24, fontWeight: 900, color: "#f87171", marginBottom: 8 }}>RÚT TỪNG TỜ TIỀN MẶT</div>
              <div style={{ fontSize: 16, color: "#94a3b8", marginBottom: 18 }}>Nhìn thấy bóp tiền xẹp dần</div>
              <div style={{ padding: "8px 18px", borderRadius: 999, backgroundColor: "rgba(239, 68, 68, 0.2)", color: "#fca5a5", fontWeight: 800, fontSize: 15 }}>
                ⚠️ NÃO BỘ XÓT XA THỰC SỰ
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 3. S010: HẠN MỨC THẺ TÍN DỤNG != TÀI SẢN THỰC CỦA BẠN ---
  // =========================================================================
  if (sc === "S010") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1180, border: "2px solid #ef4444", boxShadow: "0 0 50px rgba(239, 68, 68, 0.25)" }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>⚠️</span> ĐỊNH LÝ TÀI CHÍNH CỐT LÕI
          </div>
          <div style={headingStyle}>HẠN MỨC THẺ TÍN DỤNG ≠ TÀI SẢN CỦA BẠN</div>
          <div style={subheadStyle}>Ngộ nhận tiền đi vay của ngân hàng là tiền trong túi mình</div>

          {/* Visual Equation */}
          <div style={{ display: "flex", gap: 28, alignItems: "center", justifyContent: "center", marginTop: 32, width: "100%" }}>
            <div style={{ flex: 1, padding: "26px 20px", borderRadius: 20, backgroundColor: "rgba(239, 68, 68, 0.15)", border: "2px solid #ef4444", textAlign: "center" }}>
              <div style={{ fontSize: 44, marginBottom: 10 }}>💳</div>
              <div style={{ fontSize: 24, fontWeight: 900, color: "#ffffff" }}>HẠN MỨC 40.000.000đ</div>
              <div style={{ fontSize: 15, fontWeight: 800, color: "#fca5a5", marginTop: 6 }}>TIỀN ĐI VAY CỦA NGÂN HÀNG</div>
            </div>

            <div style={{ fontSize: 54, fontWeight: 900, color: "#ef4444", textShadow: "0 0 20px #ef4444" }}>
              ≠
            </div>

            <div style={{ flex: 1, padding: "26px 20px", borderRadius: 20, backgroundColor: "rgba(16, 185, 129, 0.15)", border: "2px solid #10b981", textAlign: "center" }}>
              <div style={{ fontSize: 44, marginBottom: 10 }}>🏦</div>
              <div style={{ fontSize: 24, fontWeight: 900, color: "#ffffff" }}>TÀI SẢN THỰC CỦA BẠN</div>
              <div style={{ fontSize: 15, fontWeight: 800, color: "#6ee7b7", marginTop: 6 }}>TIỀN LÀM RA & TÍCH LŨY</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 4. S013: NÚT BẤM MÀU XANH PHÁT SÁNG 'THANH TOÁN TỐI THIỂU 5%' ---
  // =========================================================================
  if (sc === "S013") {
    const pulseGlow = Math.sin(frame * 0.15) * 15 + 25;
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1100 }}>
          <div style={tagStyle("#38bdf8", "#7dd3fc")}>
            <span>📲</span> GIAO DIỆN SAO KÊ NGÂN HÀNG
          </div>
          <div style={headingStyle}>CẠM BẪY MÀU XANH: THANH TOÁN TỐI THIỂU</div>
          <div style={subheadStyle}>Ngân hàng thiết kế nút bấm phát sáng như một chiếc phao cứu sinh tâm lý</div>

          {/* Bank App UI Preview */}
          <div style={{ width: 560, backgroundColor: "#0f172a", borderRadius: 24, padding: "28px 36px", border: "1px solid rgba(255,255,255,0.15)", marginTop: 20, boxShadow: "0 20px 50px rgba(0,0,0,0.6)" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
              <span style={{ fontSize: 16, color: "#94a3b8" }}>Tổng dư nợ kỳ này:</span>
              <span style={{ fontSize: 18, fontWeight: 800, color: "#ffffff" }}>15.000.000 VNĐ</span>
            </div>
            {/* Glowing button */}
            <div style={{ padding: "18px 24px", borderRadius: 16, backgroundColor: "#0284c7", color: "#ffffff", textAlign: "center", fontSize: 22, fontWeight: 900, boxShadow: `0 0 ${pulseGlow}px rgba(2, 132, 199, 0.9)`, border: "2px solid #38bdf8", cursor: "pointer" }}>
              ✨ Thanh Toán Tối Thiểu 5%: 1.000.000đ
            </div>
            <div style={{ textAlign: "center", fontSize: 14, color: "#64748b", marginTop: 12 }}>
              (Chỉ trả 1 triệu để không bị báo cáo nợ xấu tháng này)
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 5. S014: NHẢY SỐ ĐÃ TRẢ 1TR VS DƯ NỢ CÒN LẠI 14TR ---
  // =========================================================================
  if (sc === "S014") {
    const paidVal = Math.round(interpolate(frame, [5, 45], [0, 1000000], { extrapolateRight: "clamp" }));
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140 }}>
          <div style={tagStyle("#f59e0b", "#fde68a")}>
            <span>📊</span> THỰC TRẠNG SAU KHI TRẢ TỐI THIỂU
          </div>
          <div style={headingStyle}>ẢO TƯỞNG HOÀN THÀNH NGHĨA VỤ</div>
          <div style={subheadStyle}>Chỉ 1 triệu được trả, 14 triệu còn lại tiếp tục sinh lãi kép mỗi ngày</div>

          <div style={{ display: "flex", gap: 36, width: "100%", marginTop: 24, justifyContent: "center" }}>
            <div style={{ flex: 1, padding: "26px 20px", borderRadius: 20, backgroundColor: "rgba(16, 185, 129, 0.15)", border: "2px solid #10b981", textAlign: "center" }}>
              <div style={{ fontSize: 16, fontWeight: 800, color: "#6ee7b7", marginBottom: 8 }}>SỐ TIỀN ĐÃ TRẢ THÁNG NÀY</div>
              <div style={{ fontSize: 44, fontWeight: 900, color: "#10b981" }}>{paidVal.toLocaleString("vi-VN")} đ</div>
              <div style={{ fontSize: 14, color: "#94a3b8", marginTop: 6 }}>Chỉ bằng 6.6% tổng nợ</div>
            </div>

            <div style={{ flex: 1, padding: "26px 20px", borderRadius: 20, backgroundColor: "rgba(239, 68, 68, 0.15)", border: "2px solid #ef4444", textAlign: "center" }}>
              <div style={{ fontSize: 16, fontWeight: 800, color: "#fca5a5", marginBottom: 8 }}>DƯ NỢ CÒN LẠI ĐANG CHỊU LÃI</div>
              <div style={{ fontSize: 44, fontWeight: 900, color: "#ef4444" }}>14.000.000 đ</div>
              <div style={{ fontSize: 14, color: "#fca5a5", marginTop: 6 }}>Lãi suất 35%/năm tính trên con số này!</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 6. S017: VÒNG TRÒN LUẨN QUẨN 4 BƯỚC (QUẸT -> TRẢ -> THIẾU -> QUẸT) ---
  // =========================================================================
  if (sc === "S017") {
    const cycleRotate = (frame * 1.5) % 360;
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1180, border: "2px solid #f59e0b" }}>
          <div style={tagStyle("#f59e0b", "#fde68a")}>
            <span>🔄</span> VÒNG XOÁY BẪY NỢ BẤT TẬN
          </div>
          <div style={headingStyle}>VÒNG LẶP NỢ NẦN: QUẸT THẺ → TRẢ TỐI THIỂU → THIẾU TIỀN</div>
          <div style={subheadStyle}>Chi tiêu trước, trả nợ sau cuốn phăng mọi kế hoạch tiết kiệm của bạn</div>

          {/* 4-node Circular SVG Diagram */}
          <div style={{ width: "100%", height: 320, position: "relative", display: "flex", justifyContent: "center", alignItems: "center" }}>
            <svg viewBox="0 0 600 320" style={{ width: "100%", height: "100%", overflow: "visible" }}>
              {/* Rotating Dashed Circle */}
              <circle cx="300" cy="160" r="110" fill="none" stroke="#f59e0b" strokeWidth="3" strokeDasharray="12 8" transform={`rotate(${cycleRotate} 300 160)`} />

              {/* Center Warning */}
              <circle cx="300" cy="160" r="45" fill="rgba(239, 68, 68, 0.2)" stroke="#ef4444" strokeWidth="2" />
              <text x="300" y="155" fill="#fca5a5" fontSize="13" fontWeight="900" textAnchor="middle">VÒNG LẶP</text>
              <text x="300" y="172" fill="#ffffff" fontSize="15" fontWeight="900" textAnchor="middle">BẾ TẮC</text>

              {/* Node 1: Top */}
              <rect x="220" y="15" width="160" height="42" rx="10" fill="#1e293b" stroke="#38bdf8" strokeWidth="2" />
              <text x="300" y="41" fill="#38bdf8" fontSize="15" fontWeight="900" textAnchor="middle">1. Quẹt Thẻ Chi Tiêu</text>

              {/* Node 2: Right */}
              <rect x="420" y="139" width="165" height="42" rx="10" fill="#1e293b" stroke="#f59e0b" strokeWidth="2" />
              <text x="502" y="165" fill="#fcd34d" fontSize="14" fontWeight="900" textAnchor="middle">2. Trả Tối Thiểu 5%</text>

              {/* Node 3: Bottom */}
              <rect x="220" y="260" width="160" height="42" rx="10" fill="#1e293b" stroke="#ef4444" strokeWidth="2" />
              <text x="300" y="286" fill="#f87171" fontSize="14" fontWeight="900" textAnchor="middle">3. Thiếu Tiền Sống</text>

              {/* Node 4: Left */}
              <rect x="15" y="139" width="165" height="42" rx="10" fill="#1e293b" stroke="#a855f7" strokeWidth="2" />
              <text x="97" y="165" fill="#d8b4fe" fontSize="14" fontWeight="900" textAnchor="middle">4. Lại Quẹt Thẻ Tiếp</text>
            </svg>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 7. S018: ĐỒ THỊ ĐƯỜNG DỐC ĐỨNG NỢ TĂNG VỌT 15TR LÊN 40TR ---
  // =========================================================================
  if (sc === "S018") {
    const spikeProgress = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: "clamp" });
    const currentDebt = Math.round(15 + spikeProgress * 25);
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1180, border: "2px solid #ef4444" }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>📈</span> ĐƯỜNG CONG NỢ NẦN BÙNG NỔ
          </div>
          <div style={headingStyle}>DƯ NỢ TĂNG VỌT TỪ 15 TRIỆU LÊN 40 TRIỆU</div>
          <div style={subheadStyle}>Chỉ sau 12 tháng trả tối thiểu, dư nợ âm thầm bùng nổ gần gấp 3 lần</div>

          {/* Steep Rising Line Chart */}
          <div style={{ width: "100%", height: 320, position: "relative", display: "flex", justifyContent: "center" }}>
            <svg viewBox="0 0 800 300" style={{ width: "100%", height: "100%", overflow: "visible" }}>
              {/* Axes */}
              <line x1="100" y1="250" x2="720" y2="250" stroke="#475569" strokeWidth="2" />
              <line x1="100" y1="250" x2="100" y2="40" stroke="#475569" strokeWidth="2" />

              <text x="90" y="255" fill="#94a3b8" fontSize="14" textAnchor="end">15 Tr</text>
              <text x="90" y="75" fill="#ef4444" fontSize="16" fontWeight="900" textAnchor="end">40 Tr</text>
              <text x="120" y="275" fill="#94a3b8" fontSize="14">Tháng 01</text>
              <text x="680" y="275" fill="#ef4444" fontSize="14" fontWeight="800">Tháng 12</text>

              {/* Rising Line */}
              <path
                d={`M 120 230 Q 350 200, ${120 + spikeProgress * 560} ${230 - spikeProgress * 160}`}
                fill="none"
                stroke="#ef4444"
                strokeWidth="6"
                strokeLinecap="round"
              />

              {/* Glowing Indicator Point */}
              <circle
                cx={120 + spikeProgress * 560}
                cy={230 - spikeProgress * 160}
                r="10"
                fill="#ef4444"
                style={{ filter: "drop-shadow(0 0 12px #ef4444)" }}
              />

              {/* Floating Badge */}
              <g transform={`translate(${120 + spikeProgress * 560 - 80}, ${230 - spikeProgress * 160 - 55})`}>
                <rect width="160" height="42" rx="10" fill="#0f172a" stroke="#ef4444" strokeWidth="2" />
                <text x="80" y="26" fill="#ffffff" fontSize="18" fontWeight="900" textAnchor="middle">{currentDebt}.000.000 đ</text>
              </g>
            </svg>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 8. S023: CÂY LÃI SUẤT 35% PHÂN NHÁNH NUỐT CHỒI TIỀN LƯƠNG ---
  // =========================================================================
  if (sc === "S023" || comp.includes("TREEGROWTH")) {
    return <TreeGrowth durationInFrames={durationInFrames} />;
  }

  // =========================================================================
  // --- 9. S025: BẢNG GIẢI PHẪU TOÁN HỌC KHOẢN NỢ 40 TRIỆU ---
  // =========================================================================
  if (sc === "S025") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140, border: "2px solid #38bdf8" }}>
          <div style={tagStyle("#38bdf8", "#7dd3fc")}>
            <span>🔬</span> PHÂN TÍCH CHUYÊN SÂU
          </div>
          <div style={headingStyle}>GIẢI PHẪU TOÁN HỌC KHOẢN NỢ 40 TRIỆU</div>
          <div style={subheadStyle}>Cùng đặt bút tính toán chính xác cái giá bạn phải trả cho ngân hàng</div>

          <div style={{ display: "flex", gap: 24, width: "100%", marginTop: 28 }}>
            <div style={{ flex: 1, padding: 24, borderRadius: 18, backgroundColor: "rgba(30, 41, 59, 0.7)", border: "1px solid rgba(255,255,255,0.1)", textAlign: "center" }}>
              <div style={{ fontSize: 16, color: "#94a3b8", marginBottom: 6 }}>Nợ Gốc Ban Đầu</div>
              <div style={{ fontSize: 32, fontWeight: 900, color: "#38bdf8" }}>40.000.000 đ</div>
            </div>
            <div style={{ flex: 1, padding: 24, borderRadius: 18, backgroundColor: "rgba(239, 68, 68, 0.15)", border: "1px solid #ef4444", textAlign: "center" }}>
              <div style={{ fontSize: 16, color: "#fca5a5", marginBottom: 6 }}>Lãi Suất Thẻ</div>
              <div style={{ fontSize: 32, fontWeight: 900, color: "#ef4444" }}>35% / Năm</div>
            </div>
            <div style={{ flex: 1, padding: 24, borderRadius: 18, backgroundColor: "rgba(245, 158, 11, 0.15)", border: "1px solid #f59e0b", textAlign: "center" }}>
              <div style={{ fontSize: 16, color: "#fde68a", marginBottom: 6 }}>Tiền Lãi Mỗi Tháng</div>
              <div style={{ fontSize: 32, fontWeight: 900, color: "#f59e0b" }}>~ 1.160.000 đ</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 10. S026: CON SỐ 35%/NĂM NHẢY SỐ ĐỎ NEON KÈM TIA CHỚP CẢNH BÁO ---
  // =========================================================================
  if (sc === "S026") {
    const rateVal = Math.round(interpolate(frame, [0, 45], [0, 35], { extrapolateRight: "clamp" }));
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1100, border: "2px solid #ef4444", boxShadow: "0 0 70px rgba(239, 68, 68, 0.4)" }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>⚡</span> CẢNH BÁO LÃI SUẤT KỶ LỤC
          </div>
          <div style={headingStyle}>LÃI SUẤT THẺ TÍN DỤNG: 35% / NĂM</div>
          <div style={subheadStyle}>Mức lãi suất thuộc hàng cao nhất trong toàn bộ hệ thống tài chính</div>

          <div style={{ fontSize: 110, fontWeight: 900, color: "#ef4444", textShadow: "0 0 40px #ef4444, 0 0 80px rgba(239,68,68,0.5)", margin: "20px 0" }}>
            {rateVal}% <span style={{ fontSize: 50, color: "#ffffff" }}>/ Năm</span>
          </div>
          <div style={{ padding: "10px 24px", borderRadius: 999, backgroundColor: "rgba(239, 68, 68, 0.2)", color: "#fca5a5", fontSize: 20, fontWeight: 800 }}>
            ⚡ Cao gấp 6 lần lãi suất vay thông thường!
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 11. S027: BARCHART SO SÁNH 6% VAY MUA NHÀ VS 35% THẺ TÍN DỤNG ---
  // =========================================================================
  if (sc === "S027") {
    return (
      <ChartMotion
        durationInFrames={durationInFrames}
        title="LÃI SUẤT THẺ CAO GẤP 6 LẦN VAY THƯỜNG!"
        subtitle="Lãi suất thẻ tín dụng 35%/năm vượt xa mức vay ngân hàng thông thường 6%/năm"
        bars={[
          { label: "Vay Mua Nhà", value: 6, color: "#38bdf8", formattedValue: "6% / Năm" },
          { label: "Thẻ Tín Dụng", value: 35, color: "#ef4444", formattedValue: "35% / Năm!" },
        ]}
      />
    );
  }

  // =========================================================================
  // --- 12. S028: ĐỒNG HỒ ĐẾM TIỀN LÃI 1.160.000Đ BỐC HƠI MỖI THÁNG ---
  // =========================================================================
  if (sc === "S028") {
    const interest = Math.round(interpolate(frame, [0, 50], [0, 1160000], { extrapolateRight: "clamp" }));
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1120 }}>
          <div style={tagStyle("#f59e0b", "#fde68a")}>
            <span>💸</span> TIỀN LÃI BỐC HƠI
          </div>
          <div style={headingStyle}>TIỀN LÃI PHÁT SINH HƠN 1 TRIỆU MỖI THÁNG</div>
          <div style={subheadStyle}>Số tiền này bốc hơi vào túi ngân hàng mà không làm giảm một đồng nợ gốc</div>

          <div style={{ fontSize: 78, fontWeight: 900, color: "#ef4444", textShadow: "0 0 35px rgba(239,68,68,0.5)", margin: "24px 0" }}>
            {interest.toLocaleString("vi-VN")} đ <span style={{ fontSize: 32, color: "#94a3b8" }}>/ tháng</span>
          </div>
          <div style={{ fontSize: 20, color: "#cbd5e1" }}>
            Mỗi năm mất trắng gần <b>14.000.000 VNĐ</b> chỉ để trả tiền lãi!
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 13. S029: PIECHART MIẾNG BÁNH TRẢ TỐI THIỂU: LÃI 95% VS GỐC 5% ---
  // =========================================================================
  if (sc === "S029") {
    const pieProgress = interpolate(frame, [0, 45], [0, 1], { extrapolateRight: "clamp" });
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1160 }}>
          <div style={tagStyle("#f59e0b", "#fde68a")}>
            <span>🥧</span> GIẢI MÃ KHOẢN TRẢ TỐI THIỂU 1.200.000đ
          </div>
          <div style={headingStyle}>95% KHOẢN TRẢ TỐI THIỂU CHỈ LÀ TIỀN LÃI!</div>
          <div style={subheadStyle}>Chỉ có đúng 40.000đ (5%) được trừ vào nợ gốc thực tế</div>

          {/* Donut Chart Comparison */}
          <div style={{ display: "flex", gap: 60, alignItems: "center", justifyContent: "center", marginTop: 24 }}>
            <svg viewBox="0 0 200 200" style={{ width: 220, height: 220, transform: "rotate(-90deg)" }}>
              {/* 5% Green Arc */}
              <circle cx="100" cy="100" r="70" fill="none" stroke="#10b981" strokeWidth="32" strokeDasharray="440" strokeDashoffset="0" />
              {/* 95% Red Arc */}
              <circle cx="100" cy="100" r="70" fill="none" stroke="#ef4444" strokeWidth="32" strokeDasharray="440" strokeDashoffset={440 - pieProgress * 418} />
            </svg>

            <div style={{ display: "flex", flexDirection: "column", gap: 18, textAlign: "left" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
                <span style={{ width: 24, height: 24, borderRadius: 6, backgroundColor: "#ef4444", boxShadow: "0 0 10px #ef4444" }} />
                <div>
                  <div style={{ fontSize: 26, fontWeight: 900, color: "#ffffff" }}>95% — Tiền Lãi Ngân Hàng</div>
                  <div style={{ fontSize: 18, color: "#fca5a5" }}>1.160.000 VNĐ (Mất trắng)</div>
                </div>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
                <span style={{ width: 24, height: 24, borderRadius: 6, backgroundColor: "#10b981", boxShadow: "0 0 10px #10b981" }} />
                <div>
                  <div style={{ fontSize: 26, fontWeight: 900, color: "#ffffff" }}>5% — Giảm Nợ Gốc</div>
                  <div style={{ fontSize: 18, color: "#6ee7b7" }}>40.000 VNĐ (Chỉ bằng một ly trà sữa!)</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 14. S030: ĐƯỜNG DƯ NỢ GỐC 40 TRIỆU NẰM NGANG BẤT ĐỘNG QUA 12 THÁNG ---
  // =========================================================================
  if (sc === "S030") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1180, border: "2px solid #ef4444" }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>📊</span> NỢ GỐC BẤT ĐỘNG
          </div>
          <div style={headingStyle}>DƯ NỢ GỐC 40 TRIỆU ĐỨNG YÊN SUỐT 12 THÁNG</div>
          <div style={subheadStyle}>Bạn đã trả hơn 14 triệu cả năm, nhưng số nợ gốc gần như không hề suy giảm!</div>

          {/* Horizontal Plateau Line Chart */}
          <div style={{ width: "100%", height: 320, position: "relative", display: "flex", justifyContent: "center" }}>
            <svg viewBox="0 0 800 300" style={{ width: "100%", height: "100%", overflow: "visible" }}>
              <line x1="100" y1="240" x2="720" y2="240" stroke="#475569" strokeWidth="2" />
              <line x1="100" y1="240" x2="100" y2="40" stroke="#475569" strokeWidth="2" />

              <text x="90" y="245" fill="#94a3b8" fontSize="14" textAnchor="end">0 đ</text>
              <text x="90" y="115" fill="#ef4444" fontSize="16" fontWeight="900" textAnchor="end">40 Tr</text>
              <text x="120" y="265" fill="#94a3b8" fontSize="14">Tháng 01</text>
              <text x="300" y="265" fill="#94a3b8" fontSize="14">Tháng 04</text>
              <text x="500" y="265" fill="#94a3b8" fontSize="14">Tháng 08</text>
              <text x="680" y="265" fill="#94a3b8" fontSize="14">Tháng 12</text>

              {/* Perfectly Horizontal Red Line */}
              <line x1="120" y1="110" x2="700" y2="110" stroke="#ef4444" strokeWidth="6" strokeDasharray="10 6" />

              {/* Pulsing Warning Label */}
              <g transform="translate(300, 45)">
                <rect width="260" height="44" rx="10" fill="#0f172a" stroke="#ef4444" strokeWidth="2" />
                <text x="130" y="28" fill="#fca5a5" fontSize="16" fontWeight="900" textAnchor="middle">⚠️ DƯ NỢ GỐC KHÔNG GIẢM!</text>
              </g>
            </svg>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 15. S031: THANH THỜI GIAN KÉO DÀI 10 NĂM (2026 - 2036) ---
  // =========================================================================
  if (sc === "S031") {
    const sliderPos = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: "clamp" });
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140 }}>
          <div style={tagStyle("#f59e0b", "#fde68a")}>
            <span>⏳</span> BẢN ÁN THỜI GIAN
          </div>
          <div style={headingStyle}>10 NĂM TRẢ NỢ ĐẰNG ĐẴNG VÌ TRẢ TỐI THIỂU</div>
          <div style={subheadStyle}>Mất 120 tháng chỉ để tất toán một khoản nợ thẻ tín dụng ban đầu</div>

          <div style={{ width: "90%", marginTop: 40 }}>
            {/* Timeline Bar */}
            <div style={{ position: "relative", width: "100%", height: 16, borderRadius: 8, backgroundColor: "#1e293b" }}>
              <div style={{ width: `${sliderPos * 100}%`, height: "100%", borderRadius: 8, background: "linear-gradient(90deg, #38bdf8, #ef4444)" }} />
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: 16 }}>
              <div style={{ textAlign: "left" }}>
                <div style={{ fontSize: 24, fontWeight: 900, color: "#38bdf8" }}>NĂM 2026</div>
                <div style={{ fontSize: 16, color: "#94a3b8" }}>Bắt đầu gánh nợ 40 triệu</div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: 24, fontWeight: 900, color: "#ef4444" }}>NĂM 2036</div>
                <div style={{ fontSize: 16, color: "#fca5a5" }}>10 năm sau mới trả hết!</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 16. S032: NỢ GỐC 40TR VS TỔNG TRẢ 84TR (GẤP ĐÔI) ---
  // =========================================================================
  if (sc === "S032") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140 }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>💰</span> TỔNG SỐ TIỀN MẤT TRẮNG
          </div>
          <div style={headingStyle}>TỔNG TIỀN PHẢI TRẢ LÊN TỚI 84 TRIỆU ĐỒNG</div>
          <div style={subheadStyle}>Vay 40 triệu nhưng phải trả gấp 2.1 lần số tiền ban đầu</div>

          <div style={{ display: "flex", gap: 36, marginTop: 32, width: "100%", justifyContent: "center" }}>
            <div style={{ flex: 1, padding: 30, borderRadius: 20, backgroundColor: "rgba(56, 189, 248, 0.15)", border: "2px solid #38bdf8", textAlign: "center" }}>
              <div style={{ fontSize: 18, color: "#7dd3fc", marginBottom: 8 }}>NỢ GỐC BAN ĐẦU</div>
              <div style={{ fontSize: 44, fontWeight: 900, color: "#ffffff" }}>40.000.000 đ</div>
            </div>
            <div style={{ flex: 1, padding: 30, borderRadius: 20, backgroundColor: "rgba(239, 68, 68, 0.2)", border: "2px solid #ef4444", textAlign: "center" }}>
              <div style={{ fontSize: 18, color: "#fca5a5", marginBottom: 8 }}>TỔNG TIỀN PHẢI TRẢ</div>
              <div style={{ fontSize: 48, fontWeight: 900, color: "#ef4444" }}>84.000.000 đ</div>
              <div style={{ fontSize: 16, fontWeight: 800, color: "#fca5a5", marginTop: 8 }}>GẤP ĐÔI SỐ NỢ GỐC!</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 17. S033 / S022: KỲ QUAN THỨ TÁM ĐẢO NGƯỢC (LÃI KÉP ÂM) ---
  // =========================================================================
  if (sc === "S033" || sc === "S022" || rawText.toLowerCase().includes("kỳ quan thứ tám")) {
    const vortexSpin = (frame * 2.5) % 360;
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1180, border: "2px solid #ef4444", boxShadow: "0 0 60px rgba(239, 68, 68, 0.35)" }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>🌀</span> CẠM BẪY TOÁN HỌC TÀI CHÍNH
          </div>
          <div style={headingStyle}>KỲ QUAN THỨ TÁM ĐẢO NGƯỢC: LÃI KÉP ÂM</div>
          <div style={subheadStyle}>Lãi kép giúp đầu tư nhân tài sản, nhưng khi vay nợ thẻ nó trở thành hố đen nuốt chửng thu nhập</div>

          {/* Clean Neon Infinity Path */}
          <div style={{ width: "100%", height: 300, position: "relative", display: "flex", justifyContent: "center", alignItems: "center" }}>
            <svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%", overflow: "visible" }}>
              <defs>
                <linearGradient id="vortexNeon" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor="#ef4444" />
                  <stop offset="50%" stopColor="#f59e0b" />
                  <stop offset="100%" stopColor="#ef4444" />
                </linearGradient>
              </defs>
              <path
                d="M 200 120 C 130 50, 60 50, 60 120 C 60 190, 130 190, 200 120 C 270 50, 340 50, 340 120 C 340 190, 270 190, 200 120 Z"
                transform="translate(100, 0)"
                fill="none"
                stroke="url(#vortexNeon)"
                strokeWidth="14"
                strokeLinecap="round"
                style={{ filter: "drop-shadow(0 0 16px rgba(239, 68, 68, 0.8))" }}
              />
            </svg>
          </div>
          <div style={{ padding: "10px 26px", borderRadius: 999, backgroundColor: "rgba(239, 68, 68, 0.2)", border: "1px solid #ef4444", color: "#fca5a5", fontWeight: 800, fontSize: 18 }}>
            ⚡ LÃI MẸ ĐẺ LÃI CON — HỐ ĐEN DƯ NỢ SINH SÔI MỖI NGÀY
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 18. S034: ĐỒ THỊ XANH ĐẦU TƯ VS ĐỒ THỊ ĐỎ VAY NỢ ---
  // =========================================================================
  if (sc === "S034") {
    const drawProgress = interpolate(frame, [0, 50], [0, 1], { extrapolateRight: "clamp" });
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1200 }}>
          <div style={tagStyle("#38bdf8", "#7dd3fc")}>
            <span>⚖️</span> HAI MẶT CỦA LÃI KÉP
          </div>
          <div style={headingStyle}>LÃI KÉP ĐẦU TƯ VS LÃI KÉP VAY NỢ</div>
          <div style={subheadStyle}>Cùng một công thức toán học, nhưng tạo ra hai số phận tài chính trái ngược</div>

          {/* Dual Curves Side-by-Side */}
          <div style={{ display: "flex", gap: 36, width: "100%", marginTop: 24 }}>
            {/* Left: Green Investment Curve */}
            <div style={{ flex: 1, backgroundColor: "rgba(15, 23, 42, 0.7)", border: "2px solid #10b981", borderRadius: 20, padding: 24, textAlign: "center" }}>
              <div style={{ fontSize: 20, fontWeight: 900, color: "#10b981", marginBottom: 6 }}>📈 LÃI KÉP ĐẦU TƯ (BẠN ĐỒNG HÀNH)</div>
              <div style={{ fontSize: 14, color: "#94a3b8", marginBottom: 12 }}>Tài sản tăng trưởng cấp số nhân</div>
              <svg viewBox="0 0 300 160" style={{ width: "100%", height: 140 }}>
                <path d={`M 30 130 Q 150 120, ${30 + drawProgress * 240} ${130 - drawProgress * 100}`} fill="none" stroke="#10b981" strokeWidth="5" strokeLinecap="round" />
                <circle cx={30 + drawProgress * 240} cy={130 - drawProgress * 100} r="6" fill="#10b981" />
              </svg>
            </div>

            {/* Right: Red Debt Curve */}
            <div style={{ flex: 1, backgroundColor: "rgba(15, 23, 42, 0.7)", border: "2px solid #ef4444", borderRadius: 20, padding: 24, textAlign: "center" }}>
              <div style={{ fontSize: 20, fontWeight: 900, color: "#ef4444", marginBottom: 6 }}>📉 LÃI KÉP NỢ THẺ (KẺ HỦY DIỆT)</div>
              <div style={{ fontSize: 14, color: "#fca5a5", marginBottom: 12 }}>Hố đen nuốt chửng toàn bộ thu nhập</div>
              <svg viewBox="0 0 300 160" style={{ width: "100%", height: 140 }}>
                <path d={`M 30 30 Q 150 40, ${30 + drawProgress * 240} ${30 + drawProgress * 100}`} fill="none" stroke="#ef4444" strokeWidth="5" strokeLinecap="round" />
                <circle cx={30 + drawProgress * 240} cy={30 + drawProgress * 100} r="6" fill="#ef4444" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 19. S035: CƠ CHẾ TÍNH LÃI LÙI NGƯỢC TỪ NGÀY 45 VỀ NGÀY 01 ---
  // =========================================================================
  if (sc === "S035") {
    const rewindProgress = interpolate(frame, [10, 50], [0, 1], { extrapolateRight: "clamp" });
    const arrowX = 650 - rewindProgress * 450;
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1180, border: "2px solid #ef4444" }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>⏪</span> ĐIỀU KHOẢN TÍNH LÃI TRUY THU
          </div>
          <div style={headingStyle}>CƠ CHẾ TÍNH LÃI LÙI NGƯỢC 45 NGÀY</div>
          <div style={subheadStyle}>Chỉ cần thiếu 1.000đ ở ngày 45, ngân hàng sẽ hủy bỏ toàn bộ quyền miễn lãi và tính lãi từ ngày quẹt đầu tiên!</div>

          {/* Decoupled Timeline Bar */}
          <div style={{ width: "100%", height: 260, position: "relative", marginTop: 20 }}>
            {/* Top Labels - Well Above The Bar */}
            <div style={{ display: "flex", justifyContent: "space-between", padding: "0 40px", marginBottom: 24 }}>
              <div style={{ textAlign: "left" }}>
                <span style={{ padding: "6px 14px", borderRadius: 8, backgroundColor: "#0284c7", color: "#ffffff", fontWeight: 900, fontSize: 16 }}>NGÀY 01</span>
                <div style={{ fontSize: 18, fontWeight: 800, color: "#38bdf8", marginTop: 8 }}>Quẹt Thẻ 40 Triệu</div>
              </div>
              <div style={{ textAlign: "right" }}>
                <span style={{ padding: "6px 14px", borderRadius: 8, backgroundColor: "#b91c1c", color: "#ffffff", fontWeight: 900, fontSize: 16 }}>NGÀY 45</span>
                <div style={{ fontSize: 18, fontWeight: 800, color: "#fca5a5", marginTop: 8 }}>Thiếu Đúng 1.000đ!</div>
              </div>
            </div>

            {/* Timeline Track */}
            <div style={{ position: "relative", height: 16, backgroundColor: "#334155", borderRadius: 8, margin: "0 40px" }}>
              <div style={{ width: "100%", height: "100%", background: "linear-gradient(90deg, #38bdf8, #ef4444)", borderRadius: 8 }} />
            </div>

            {/* Rewind Arrow Label - Well Below The Bar */}
            <div style={{ position: "absolute", left: arrowX, top: 120, transition: "left 0.1s linear" }}>
              <div style={{ padding: "10px 22px", borderRadius: 12, backgroundColor: "#ef4444", color: "#ffffff", fontWeight: 900, fontSize: 16, whiteSpace: "nowrap", boxShadow: "0 0 25px rgba(239, 68, 68, 0.7)" }}>
                ⏪ TRUY THU TOÀN BỘ LÃI 35% LÙI VỀ NGÀY 01
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 20. S036: ALERTBOX THIẾU 1.000Đ -> TÍNH LÃI TOÀN BỘ 40.000.000Đ ---
  // =========================================================================
  if (sc === "S036") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1120, border: "2px solid #ef4444", boxShadow: "0 0 50px rgba(239, 68, 68, 0.3)" }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>🚨</span> BẪY TOÁN HỌC 1.000 ĐỒNG
          </div>
          <div style={headingStyle}>THIẾU 1.000đ → BỊ TÍNH LÃI TOÀN BỘ 40 TRIỆU!</div>
          <div style={subheadStyle}>Ngân hàng không tính lãi trên 1.000đ còn thiếu, mà tính trên 100% số tiền 40 triệu ban đầu</div>

          <div style={{ display: "flex", gap: 32, alignItems: "center", marginTop: 28 }}>
            <div style={{ padding: "20px 28px", borderRadius: 18, backgroundColor: "rgba(239, 68, 68, 0.2)", border: "1px solid #ef4444", textAlign: "center" }}>
              <div style={{ fontSize: 16, color: "#fca5a5" }}>Bạn chỉ thiếu</div>
              <div style={{ fontSize: 38, fontWeight: 900, color: "#ffffff" }}>1.000 VNĐ</div>
            </div>
            <div style={{ fontSize: 36, color: "#ef4444", fontWeight: 900 }}>➔</div>
            <div style={{ padding: "20px 28px", borderRadius: 18, backgroundColor: "rgba(239, 68, 68, 0.3)", border: "2px solid #ef4444", textAlign: "center" }}>
              <div style={{ fontSize: 16, color: "#fca5a5" }}>Bị áp lãi 35% trên</div>
              <div style={{ fontSize: 38, fontWeight: 900, color: "#ef4444" }}>40.000.000 VNĐ!</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 21. S037: CÁC LỚP PHÍ PHẠT CHỒNG CHẤT LÊN NHAU ---
  // =========================================================================
  if (sc === "S037") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140 }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>📚</span> PHÍ PHẠT CHỒNG CHẤT
          </div>
          <div style={headingStyle}>CÁC LỚP PHÍ BÀO MÒN TÀI SẢN</div>
          <div style={subheadStyle}>Lãi suất, phí phạt chậm trả và phí thường niên liên tục cộng dồn</div>

          <div style={{ display: "flex", flexDirection: "column", gap: 14, width: "100%", maxWidth: 650, marginTop: 24 }}>
            <div style={{ padding: "16px 24px", borderRadius: 14, backgroundColor: "rgba(239, 68, 68, 0.25)", border: "1px solid #ef4444", display: "flex", justifyContent: "space-between" }}>
              <span style={{ fontSize: 20, fontWeight: 900, color: "#ffffff" }}>1. Lãi Suất Thẻ Tín Dụng</span>
              <span style={{ fontSize: 20, fontWeight: 900, color: "#fca5a5" }}>35% / Năm</span>
            </div>
            <div style={{ padding: "16px 24px", borderRadius: 14, backgroundColor: "rgba(245, 158, 11, 0.25)", border: "1px solid #f59e0b", display: "flex", justifyContent: "space-between" }}>
              <span style={{ fontSize: 20, fontWeight: 900, color: "#ffffff" }}>2. Phạt Chậm Trả</span>
              <span style={{ fontSize: 20, fontWeight: 900, color: "#fde68a" }}>4% - 6% (Tối thiểu 200k)</span>
            </div>
            <div style={{ padding: "16px 24px", borderRadius: 14, backgroundColor: "rgba(148, 163, 184, 0.25)", border: "1px solid #94a3b8", display: "flex", justifyContent: "space-between" }}>
              <span style={{ fontSize: 20, fontWeight: 900, color: "#ffffff" }}>3. Phí Thường Niên</span>
              <span style={{ fontSize: 20, fontWeight: 900, color: "#cbd5e1" }}>1.200.000 đ / Năm</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 22. S045: ĐỒNG HỒ ĐIỂM TÍN DỤNG CIC TRƯỢT XANH XUỐNG ĐỎ ---
  // =========================================================================
  
  // =========================================================================
  // --- 22. S038: BỂ CHỨA LƯƠNG BỊ CÁC VAN PHÍ PHẠT HÚT CẠN ---
  // =========================================================================
  if (sc === "S038") {
    const drainLevel = interpolate(frame, [0, 50], [170, 40], { extrapolateRight: "clamp" });
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140, border: "2px solid #ef4444" }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>💧</span> BÀO MÒN THẶNG DƯ
          </div>
          <div style={headingStyle}>BỂ CHỨA TIỀN LƯƠNG BỊ CÁC VAN PHÍ HÚT CẠN</div>
          <div style={subheadStyle}>Lãi suất 35%, phí chậm trả và phí thường niên liên tục rò rỉ rút sạch tiền lương</div>

          <div style={{ width: "100%", height: 260, position: "relative", display: "flex", justifyContent: "center", alignItems: "center" }}>
            <svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
              <rect x="150" y="20" width="300" height="190" rx="16" fill="rgba(15, 23, 42, 0.7)" stroke="#38bdf8" strokeWidth="4" />
              <rect x="154" y={206 - drainLevel} width="292" height={drainLevel} rx="12" fill="rgba(56, 189, 248, 0.4)" />
              <text x="300" y="110" fill="#ffffff" fontSize="22" fontWeight="900" textAnchor="middle">LƯƠNG 12 TRIỆU</text>

              <line x1="450" y1="70" x2="520" y2="70" stroke="#ef4444" strokeWidth="6" strokeLinecap="round" />
              <text x="530" y="75" fill="#fca5a5" fontSize="13" fontWeight="900">Lãi 35%</text>

              <line x1="450" y1="130" x2="520" y2="130" stroke="#f59e0b" strokeWidth="6" strokeLinecap="round" />
              <text x="530" y="135" fill="#fde68a" fontSize="13" fontWeight="900">Phạt trễ 200k</text>

              <line x1="450" y1="180" x2="520" y2="180" stroke="#ef4444" strokeWidth="6" strokeLinecap="round" />
              <text x="530" y="185" fill="#fca5a5" fontSize="13" fontWeight="900">Phí 1.2tr</text>
            </svg>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 23. S042: CASHBACK 100K VS PHÍ THƯỜNG NIÊN 1.2TR ---
  // =========================================================================
  if (sc === "S042") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1160 }}>
          <div style={tagStyle("#f59e0b", "#fde68a")}>
            <span>⚖️</span> CẠM BẪY CASHBACK 1%
          </div>
          <div style={headingStyle}>CHI TIÊU 10 TRIỆU ĐỂ NHẬN VỀ 100.000đ?</div>
          <div style={subheadStyle}>Cái bẫy hoàn tiền lẻ trong khi phí thường niên lên tới hơn một triệu đồng</div>

          <div style={{ display: "flex", gap: 36, width: "100%", marginTop: 24, justifyContent: "center" }}>
            <div style={{ flex: 1, padding: 24, borderRadius: 20, backgroundColor: "rgba(56, 189, 248, 0.15)", border: "2px solid #38bdf8", textAlign: "center" }}>
              <div style={{ fontSize: 44, marginBottom: 8 }}>🪙</div>
              <div style={{ fontSize: 16, color: "#7dd3fc" }}>HOÀN TIỀN (1%)</div>
              <div style={{ fontSize: 34, fontWeight: 900, color: "#38bdf8", margin: "8px 0" }}>+100.000 đ</div>
              <div style={{ fontSize: 13, color: "#94a3b8" }}>Phải quẹt tới 10.000.000đ</div>
            </div>

            <div style={{ flex: 1, padding: 24, borderRadius: 20, backgroundColor: "rgba(239, 68, 68, 0.2)", border: "2px solid #ef4444", textAlign: "center" }}>
              <div style={{ fontSize: 44, marginBottom: 8 }}>💳</div>
              <div style={{ fontSize: 16, color: "#fca5a5" }}>PHÍ THƯỜNG NIÊN</div>
              <div style={{ fontSize: 38, fontWeight: 900, color: "#ef4444", margin: "8px 0" }}>-1.200.000 đ</div>
              <div style={{ fontSize: 13, fontWeight: 800, color: "#fca5a5" }}>Gấp 12 lần tiền hoàn!</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 24. S044: 3 TỜ LỊCH THÁNG 1, 2, 3 BỊ DÁN NHÃN LÀM VIỆC 0 ĐỒNG ---
  // =========================================================================
  if (sc === "S044") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1160, border: "2px solid #ef4444" }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>📅</span> NÔ LỆ CÔNG SỞ VÌ NỢ
          </div>
          <div style={headingStyle}>HƠN 3 THÁNG LÀM VIỆC KHÔNG CÔNG CHO NGÂN HÀNG</div>
          <div style={subheadStyle}>Với lương 12 triệu, bạn mất trọn hơn 3 tháng đi làm chỉ để trả đứt 40 triệu tiền nợ thẻ</div>

          <div style={{ display: "flex", gap: 24, width: "100%", marginTop: 24, justifyContent: "center" }}>
            {["THÁNG 01", "THÁNG 02", "THÁNG 03"].map((m, idx) => (
              <div key={idx} style={{ position: "relative", width: 220, height: 160, borderRadius: 16, backgroundColor: "#1e293b", border: "2px solid #ef4444", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
                <div style={{ fontSize: 22, fontWeight: 900, color: "#94a3b8", marginBottom: 6 }}>{m}</div>
                <div style={{ fontSize: 16, color: "#cbd5e1" }}>Lương: 12.000.000đ</div>
                <div style={{ position: "absolute", transform: "rotate(-18deg)", padding: "6px 14px", backgroundColor: "#b91c1c", color: "#ffffff", fontWeight: 900, fontSize: 15, borderRadius: 6, boxShadow: "0 0 15px rgba(239, 68, 68, 0.7)" }}>
                  LÀM VIỆC 0 ĐỒNG
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }
if (sc === "S045") {
    const needleDeg = interpolate(frame, [0, 50], [-60, 60], { extrapolateRight: "clamp" });
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140, border: "2px solid #ef4444" }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>📉</span> HỆ THỐNG ĐIỂM TÍN DỤNG
          </div>
          <div style={headingStyle}>ĐIỂM TÍN DỤNG CIC LAO DỐC SANG NỢ XẤU</div>
          <div style={subheadStyle}>Nguy cơ bị khóa toàn bộ cơ hội vay mua nhà, mua xe trong 5 năm tới</div>

          {/* Speedometer Gauge */}
          <div style={{ position: "relative", width: 320, height: 170, marginTop: 24 }}>
            <svg viewBox="0 0 200 110" style={{ width: "100%", height: "100%" }}>
              <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#334155" strokeWidth="18" strokeLinecap="round" />
              {/* Green Zone */}
              <path d="M 20 100 A 80 80 0 0 1 80 35" fill="none" stroke="#10b981" strokeWidth="18" />
              {/* Yellow Zone */}
              <path d="M 80 35 A 80 80 0 0 1 120 35" fill="none" stroke="#f59e0b" strokeWidth="18" />
              {/* Red Zone */}
              <path d="M 120 35 A 80 80 0 0 1 180 100" fill="none" stroke="#ef4444" strokeWidth="18" />

              {/* Needle */}
              <line x1="100" y1="100" x2="100" y2="35" stroke="#ffffff" strokeWidth="4" strokeLinecap="round" transform={`rotate(${needleDeg} 100 100)`} />
              <circle cx="100" cy="100" r="8" fill="#ffffff" />
            </svg>
          </div>
          <div style={{ padding: "8px 22px", borderRadius: 999, backgroundColor: "rgba(239, 68, 68, 0.25)", color: "#fca5a5", fontWeight: 900, fontSize: 18, marginTop: 10 }}>
            NHÓM 3: NỢ DƯỚI TIÊU CHUẨN (NỢ XẤU)
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 23. S048: HUY HIỆU VÀNG LỢI NHUẬN 35% TUYỆT ĐỐI ---
  // =========================================================================
  if (sc === "S048") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140, border: "2px solid #f59e0b", boxShadow: "0 0 60px rgba(245, 158, 11, 0.3)" }}>
          <div style={tagStyle("#f59e0b", "#fde68a")}>
            <span>🏆</span> KHOẢN ĐẦU TƯ TỐT NHẤT THẾ GIỚI
          </div>
          <div style={headingStyle}>LỢI NHUẬN 35% ĐẢM BẢO 100% KHI TRẢ HẾT NỢ THẺ</div>
          <div style={subheadStyle}>Không có kênh đầu tư an toàn nào trên thị trường đem lại mức sinh lời 35%/năm</div>

          <div style={{ fontSize: 90, margin: "20px 0" }}>🥇</div>
          <div style={{ fontSize: 48, fontWeight: 900, color: "#f59e0b", textShadow: "0 0 25px #f59e0b" }}>
            +35% LỢI NHUẬN TỨC THÌ
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 24. S062: SƠ ĐỒ 4 BƯỚC THỰC CHIẾN DIỆT NỢ THẺ ---
  // =========================================================================
  
  // =========================================================================
  // --- 27. S049: BẢNG SO SÁNH GỬI TIẾT KIỆM 6%, QUỸ 12% VS TRẢ NỢ THẺ 35% ---
  // =========================================================================
  if (sc === "S049") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1180 }}>
          <div style={tagStyle("#f59e0b", "#fde68a")}>
            <span>📊</span> SO SÁNH TỶ SUẤT SINH LỜI
          </div>
          <div style={headingStyle}>KHÔNG KÊNH ĐẦU TƯ NÀO ĐẠT ĐƯỢC 35% / NĂM</div>
          <div style={subheadStyle}>Trả hết nợ thẻ là kênh đầu tư có lợi nhuận cao nhất và an toàn nhất hiện tại</div>

          <div style={{ display: "flex", gap: 24, width: "100%", marginTop: 24 }}>
            <div style={{ flex: 1, padding: 22, borderRadius: 18, backgroundColor: "rgba(30, 41, 59, 0.7)", border: "1px solid #64748b", textAlign: "center" }}>
              <div style={{ fontSize: 16, color: "#94a3b8", marginBottom: 6 }}>Tiết Kiệm Ngân Hàng</div>
              <div style={{ fontSize: 34, fontWeight: 900, color: "#38bdf8" }}>+6% <span style={{ fontSize: 16 }}>/ năm</span></div>
              <div style={{ fontSize: 13, color: "#64748b", marginTop: 6 }}>An toàn, sinh lời thấp</div>
            </div>
            <div style={{ flex: 1, padding: 22, borderRadius: 18, backgroundColor: "rgba(30, 41, 59, 0.7)", border: "1px solid #64748b", textAlign: "center" }}>
              <div style={{ fontSize: 16, color: "#94a3b8", marginBottom: 6 }}>Quỹ Cổ Phiếu</div>
              <div style={{ fontSize: 34, fontWeight: 900, color: "#f59e0b" }}>+12% <span style={{ fontSize: 16 }}>/ năm</span></div>
              <div style={{ fontSize: 13, color: "#64748b", marginTop: 6 }}>Biến động thị trường</div>
            </div>
            <div style={{ flex: 1.2, padding: 22, borderRadius: 18, backgroundColor: "rgba(16, 185, 129, 0.2)", border: "2px solid #10b981", textAlign: "center", boxShadow: "0 0 30px rgba(16, 185, 129, 0.25)" }}>
              <div style={{ fontSize: 16, color: "#6ee7b7", fontWeight: 800, marginBottom: 6 }}>TRẢ HẾT NỢ THẺ</div>
              <div style={{ fontSize: 40, fontWeight: 900, color: "#10b981" }}>+35% <span style={{ fontSize: 18 }}>/ năm</span></div>
              <div style={{ fontSize: 13, fontWeight: 800, color: "#6ee7b7", marginTop: 6 }}>ĐẢM BẢO 100% LỢI NHUẬN!</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 28. S050: CHIA ĐÔI MÀN HÌNH NGƯỜI A (TRÁI) VS NGƯỜI B (PHẢI) ---
  // =========================================================================
  if (sc === "S050") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1180 }}>
          <div style={tagStyle("#38bdf8", "#7dd3fc")}>
            <span>👥</span> HAI CON ĐƯỜNG — HAI SỐ PHẬN
          </div>
          <div style={headingStyle}>CÙNG MỨC LƯƠNG 12 TRIỆU — HAI SỰ LỰA CHỌN TRÁI NGƯỢC</div>
          <div style={subheadStyle}>Cùng vạch xuất phát, thói quen chi tiêu quyết định tương lai tài chính</div>

          <div style={{ display: "flex", gap: 32, width: "100%", marginTop: 24 }}>
            <div style={{ flex: 1, padding: 24, borderRadius: 20, backgroundColor: "rgba(239, 68, 68, 0.15)", border: "2px solid #ef4444", textAlign: "center" }}>
              <div style={{ fontSize: 40, marginBottom: 8 }}>🙍‍♂️</div>
              <div style={{ fontSize: 22, fontWeight: 900, color: "#fca5a5" }}>NGƯỜI A: BỐC ĐỒNG</div>
              <div style={{ fontSize: 15, color: "#cbd5e1", margin: "10px 0" }}>Quẹt thẻ xả láng, chỉ trả tối thiểu 5%</div>
              <div style={{ padding: "6px 14px", borderRadius: 8, backgroundColor: "rgba(239, 68, 68, 0.3)", color: "#fca5a5", fontWeight: 800, fontSize: 14 }}>
                NỢ TĂNG LÊN 60 TRIỆU
              </div>
            </div>

            <div style={{ flex: 1, padding: 24, borderRadius: 20, backgroundColor: "rgba(16, 185, 129, 0.15)", border: "2px solid #10b981", textAlign: "center" }}>
              <div style={{ fontSize: 40, marginBottom: 8 }}>🙎‍♀️</div>
              <div style={{ fontSize: 22, fontWeight: 900, color: "#6ee7b7" }}>NGƯỜI B: KỶ LUẬT</div>
              <div style={{ fontSize: 15, color: "#cbd5e1", margin: "10px 0" }}>Trích 4tr diệt nợ, sống 8tr phong bì</div>
              <div style={{ padding: "6px 14px", borderRadius: 8, backgroundColor: "rgba(16, 185, 129, 0.3)", color: "#6ee7b7", fontWeight: 800, fontSize: 14 }}>
                SẠCH NỢ SAU 10 THÁNG
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 29. S053: DƯ NỢ NGƯỜI A NHẢY SỐ MÀU ĐỎ TỪ 40TR VỌT LÊN 60TR ---
  // =========================================================================
  if (sc === "S053") {
    const debtA = Math.round(interpolate(frame, [0, 50], [40, 60], { extrapolateRight: "clamp" }));
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1120, border: "2px solid #ef4444", boxShadow: "0 0 60px rgba(239, 68, 68, 0.35)" }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>⚠️</span> DƯ NỢ NGƯỜI A PHÌNH TO
          </div>
          <div style={headingStyle}>KHOẢN NỢ PHÌNH TO TỪ 40 TRIỆU LÊN 60 TRIỆU</div>
          <div style={subheadStyle}>Sau một năm quẹt tiếp và trả tối thiểu, nợ tăng thêm 50% cùng nỗi căng thẳng tột cùng</div>

          <div style={{ fontSize: 90, fontWeight: 900, color: "#ef4444", textShadow: "0 0 35px #ef4444", margin: "20px 0" }}>
            {debtA}.000.000 đ
          </div>
          <div style={{ padding: "8px 20px", borderRadius: 999, backgroundColor: "rgba(239, 68, 68, 0.25)", color: "#fca5a5", fontWeight: 800, fontSize: 18 }}>
            TĂNG THÊM +20.000.000 VNĐ TIỀN LÃI & PHẠT!
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 30. S057: THANH TIẾN ĐỘ TRẢ NỢ GIẢM DẦN MỖI THÁNG 4 TRIỆU ---
  // =========================================================================
  if (sc === "S057") {
    const payProgress = interpolate(frame, [0, 60], [40, 0], { extrapolateRight: "clamp" });
    const barWidth = interpolate(frame, [0, 60], [100, 0], { extrapolateRight: "clamp" });
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1160 }}>
          <div style={tagStyle("#10b981", "#6ee7b7")}>
            <span>📉</span> TIẾN TRÌNH DIỆT NỢ NGƯỜI B
          </div>
          <div style={headingStyle}>MỖI THÁNG TRÍCH 4 TRIỆU — NỢ GỐC GIẢM ĐỀU ĐẶN</div>
          <div style={subheadStyle}>Dồn toàn lực thanh toán nợ gốc giúp khoản nợ giảm liên tục về 0 đồng</div>

          <div style={{ width: "90%", marginTop: 32 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 12 }}>
              <span style={{ fontSize: 18, color: "#94a3b8" }}>Dư nợ còn lại:</span>
              <span style={{ fontSize: 28, fontWeight: 900, color: "#10b981" }}>{Math.round(payProgress)}.000.000 VNĐ</span>
            </div>
            <div style={{ position: "relative", width: "100%", height: 22, borderRadius: 12, backgroundColor: "#1e293b", overflow: "hidden" }}>
              <div style={{ width: `${barWidth}%`, height: "100%", borderRadius: 12, background: "linear-gradient(90deg, #10b981, #38bdf8)" }} />
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: 14 }}>
              <span style={{ fontSize: 15, color: "#94a3b8" }}>Tháng 01: 40 Tr</span>
              <span style={{ fontSize: 15, color: "#94a3b8" }}>Tháng 05: 20 Tr</span>
              <span style={{ fontSize: 15, fontWeight: 900, color: "#10b981" }}>Tháng 10: 0 Tr (Sạch nợ!)</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 31. S059: CÚP MỞ KHÓA TỰ DO TÀI CHÍNH: DƯ NỢ = 0 ĐỒNG ---
  // =========================================================================
  if (sc === "S059") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140, border: "2px solid #10b981", boxShadow: "0 0 70px rgba(16, 185, 129, 0.4)" }}>
          <div style={{ fontSize: 90, margin: "14px 0" }}>🏆</div>
          <div style={headingStyle}>MỤC TIÊU HOÀN THÀNH: DƯ NỢ = 0 ĐỒNG!</div>
          <div style={subheadStyle}>Bước sang tháng thứ 11, bạn hoàn toàn sạch nợ, sở hữu quỹ dự phòng và bắt đầu tích sản</div>

          <div style={{ padding: "12px 30px", borderRadius: 999, backgroundColor: "rgba(16, 185, 129, 0.25)", border: "1px solid #10b981", color: "#6ee7b7", fontSize: 22, fontWeight: 900, marginTop: 12 }}>
            ✨ CHÀO MỪNG BẠN ĐẾN VỚI TỰ DO TÀI CHÍNH!
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 32. S060: BỨC TRANH TỔNG KẾT: NGƯỜI A KIỆT QUỆ VS NGƯỜI B THẢNH THƠI ---
  // =========================================================================
  if (sc === "S060") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1180 }}>
          <div style={tagStyle("#38bdf8", "#7dd3fc")}>
            <span>⚖️</span> TỔNG KẾT SAU 1 NĂM
          </div>
          <div style={headingStyle}>LỰA CHỌN TƯ DUY — ĐỔI THAY VẬN MỆNH</div>
          <div style={subheadStyle}>Cùng một thu nhập 12 triệu, kỷ luật tài chính tạo ra khoảng cách hàng trăm triệu đồng</div>

          <div style={{ display: "flex", gap: 32, width: "100%", marginTop: 24 }}>
            <div style={{ flex: 1, padding: 24, borderRadius: 20, backgroundColor: "rgba(239, 68, 68, 0.15)", border: "2px solid #ef4444", textAlign: "center" }}>
              <div style={{ fontSize: 20, fontWeight: 900, color: "#fca5a5", marginBottom: 8 }}>NGƯỜI A (KIỆT QUỆ)</div>
              <div style={{ fontSize: 32, fontWeight: 900, color: "#ef4444" }}>NỢ 60 TRIỆU</div>
              <div style={{ fontSize: 14, color: "#94a3b8", marginTop: 8 }}>Mất ngủ, lo âu, điểm tín dụng xấu</div>
            </div>

            <div style={{ flex: 1, padding: 24, borderRadius: 20, backgroundColor: "rgba(16, 185, 129, 0.15)", border: "2px solid #10b981", textAlign: "center" }}>
              <div style={{ fontSize: 20, fontWeight: 900, color: "#6ee7b7", marginBottom: 8 }}>NGƯỜI B (THẢNH THƠI)</div>
              <div style={{ fontSize: 32, fontWeight: 900, color: "#10b981" }}>SẠCH NỢ 0 ĐỒNG</div>
              <div style={{ fontSize: 14, color: "#94a3b8", marginTop: 8 }}>Có quỹ dự phòng, bắt đầu tích sản</div>
            </div>
          </div>
        </div>
      </div>
    );
  }
if (sc === "S062") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1200 }}>
          <div style={tagStyle("#10b981", "#6ee7b7")}>
            <span>🗺️</span> CHIẾN LƯỢC HÀNH ĐỘNG
          </div>
          <div style={headingStyle}>LỘ TRÌNH 4 BƯỚC DIỆT SẠCH NỢ THẺ</div>
          <div style={subheadStyle}>Quy trình thực chiến giúp bạn giải phóng 40 triệu nợ trong 10 tháng</div>

          {/* 4 Steps Row */}
          <div style={{ display: "flex", gap: 18, width: "100%", marginTop: 28 }}>
            {[
              { num: "01", title: "Cắt Thẻ", desc: "Phong tỏa tâm lý", color: "#ef4444" },
              { num: "02", title: "Bản Đồ Nợ", desc: "Snowball chiến lược", color: "#f59e0b" },
              { num: "03", title: "Ngân Sách 12Tr", desc: "Kỷ luật 3 phong bì", color: "#38bdf8" },
              { num: "04", title: "Quỹ Mini 2Tr", desc: "Lá chắn tài chính", color: "#10b981" },
            ].map((step, idx) => (
              <div key={idx} style={{ flex: 1, padding: 20, borderRadius: 18, backgroundColor: "rgba(30, 41, 59, 0.7)", border: `2px solid ${step.color}`, textAlign: "center" }}>
                <div style={{ fontSize: 24, fontWeight: 900, color: step.color, marginBottom: 8 }}>{step.num}</div>
                <div style={{ fontSize: 18, fontWeight: 800, color: "#ffffff", marginBottom: 4 }}>{step.title}</div>
                <div style={{ fontSize: 13, color: "#94a3b8" }}>{step.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 25. S071: BIỂU ĐỒ CHIA LƯƠNG: 4TR (33%) TRẢ NỢ VS 8TR (67%) SINH HOẠT ---
  // =========================================================================
  
  // =========================================================================
  // --- 34. S063: BƯỚC 1 — PHONG TỎA THẺ & CẮT MỎ NEO TÂM LÝ ---
  // =========================================================================
  if (sc === "S063") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140, border: "2px solid #ef4444" }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>🔒</span> BƯỚC 1 TRONG LỘ TRÌNH
          </div>
          <div style={headingStyle}>BƯỚC 1: PHONG TỎA THẺ & CẮT MỎ NEO TÂM LÝ</div>
          <div style={subheadStyle}>Chặn đứng ngay lập tức nguồn cơn rò rỉ tài chính trước khi thực hiện bất kỳ kế hoạch nào</div>

          <div style={{ display: "flex", gap: 28, marginTop: 24 }}>
            <div style={{ padding: "20px 28px", borderRadius: 16, backgroundColor: "rgba(239, 68, 68, 0.2)", border: "1px solid #ef4444", textAlign: "center" }}>
              <div style={{ fontSize: 44, marginBottom: 8 }}>✂️ 💳</div>
              <div style={{ fontSize: 18, fontWeight: 900, color: "#ffffff" }}>Cắt đôi thẻ vật lý</div>
            </div>
            <div style={{ padding: "20px 28px", borderRadius: 16, backgroundColor: "rgba(239, 68, 68, 0.2)", border: "1px solid #ef4444", textAlign: "center" }}>
              <div style={{ fontSize: 44, marginBottom: 8 }}>🔒 📱</div>
              <div style={{ fontSize: 18, fontWeight: 900, color: "#ffffff" }}>Khóa thẻ trên Banking App</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 35. S065: MÀN HÌNH ĐIỆN THOẠI XÓA LIÊN KẾT KHỎI CÁC SÀN THƯƠNG MẠI ---
  // =========================================================================
  if (sc === "S065") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1160 }}>
          <div style={tagStyle("#38bdf8", "#7dd3fc")}>
            <span>📲</span> XÓA CÁM DỖ 1-CHẠM
          </div>
          <div style={headingStyle}>HỦY MỌI LIÊN KẾT THẺ TRÊN CÁC SÀN MUA SẮM</div>
          <div style={subheadStyle}>Cắt đứt hoàn toàn thói quen quẹt thẻ mua sắm bốc đồng giữa đêm</div>

          <div style={{ display: "flex", gap: 24, width: "100%", marginTop: 24, justifyContent: "center" }}>
            {[
              { app: "Shopee", icon: "🛒" },
              { app: "Lazada", icon: "📦" },
              { app: "TikTok Shop", icon: "📱" },
            ].map((item, idx) => (
              <div key={idx} style={{ flex: 1, padding: 22, borderRadius: 18, backgroundColor: "rgba(30, 41, 59, 0.7)", border: "1px solid #10b981", textAlign: "center" }}>
                <div style={{ fontSize: 36, marginBottom: 8 }}>{item.icon}</div>
                <div style={{ fontSize: 18, fontWeight: 900, color: "#ffffff", marginBottom: 10 }}>{item.app}</div>
                <div style={{ padding: "6px 12px", borderRadius: 8, backgroundColor: "rgba(16, 185, 129, 0.25)", color: "#6ee7b7", fontWeight: 800, fontSize: 13 }}>
                  ✓ ĐÃ XÓA LIÊN KẾT
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 36. S066: BƯỚC 2 — LẬP BẢN ĐỒ NỢ & CHIẾN LƯỢC SNOWBALL ---
  // =========================================================================
  if (sc === "S066") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140, border: "2px solid #f59e0b" }}>
          <div style={tagStyle("#f59e0b", "#fde68a")}>
            <span>❄️</span> BƯỚC 2 TRONG LỘ TRÌNH
          </div>
          <div style={headingStyle}>BƯỚC 2: LẬP BẢN ĐỒ NỢ & CHIẾN LƯỢC HÒN TUYẾT LĂN</div>
          <div style={subheadStyle}>Liệt kê chi tiết từng chiếc thẻ: Dư nợ, Lãi suất, và Ngày sao kê để lên kế hoạch đánh chiếm</div>

          <div style={{ display: "flex", gap: 24, marginTop: 24 }}>
            <div style={{ padding: "18px 26px", borderRadius: 16, backgroundColor: "rgba(245, 158, 11, 0.2)", border: "1px solid #f59e0b", textAlign: "center" }}>
              <div style={{ fontSize: 36, marginBottom: 6 }}>📜</div>
              <div style={{ fontSize: 18, fontWeight: 900, color: "#ffffff" }}>Bản Đồ Nợ Minh Bạch</div>
            </div>
            <div style={{ padding: "18px 26px", borderRadius: 16, backgroundColor: "rgba(56, 189, 248, 0.2)", border: "1px solid #38bdf8", textAlign: "center" }}>
              <div style={{ fontSize: 36, marginBottom: 6 }}>🏔️</div>
              <div style={{ fontSize: 18, fontWeight: 900, color: "#ffffff" }}>Chiến Lược Snowball</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 37. S068: HỒNG TÂM NHẮM TRÚNG THẺ LÃI SUẤT CAO NHẤT ---
  // =========================================================================
  if (sc === "S068") {
    const pulseRing = Math.sin(frame * 0.2) * 8 + 65;
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140, border: "2px solid #ef4444" }}>
          <div style={tagStyle("#ef4444", "#fca5a5")}>
            <span>🎯</span> MỤC TIÊU BẮN TỈA
          </div>
          <div style={headingStyle}>TẬP TRUNG TIÊU DIỆT CHIẾC THẺ CÓ LÃI SUẤT CAO NHẤT</div>
          <div style={subheadStyle}>Dồn toàn lực dập tắt ngọn lửa lãi suất 35% trước để chặn lãi mẹ đẻ lãi con</div>

          <div style={{ position: "relative", width: 340, height: 180, marginTop: 20, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <div style={{ width: 280, height: 140, borderRadius: 16, backgroundColor: "#1e293b", border: "2px solid #ef4444", padding: 18, textAlign: "center", display: "flex", flexDirection: "column", justifyContent: "center" }}>
              <div style={{ fontSize: 18, fontWeight: 900, color: "#ffffff" }}>THẺ LÃI SUẤT 35%</div>
              <div style={{ fontSize: 14, color: "#fca5a5" }}>Dư nợ: 40.000.000 VNĐ</div>
            </div>
            <div style={{ position: "absolute", width: pulseRing * 2, height: pulseRing * 2, borderRadius: "50%", border: "3px solid #ef4444", pointerEvents: "none", boxShadow: "0 0 20px #ef4444" }} />
          </div>
          <div style={{ padding: "6px 18px", borderRadius: 8, backgroundColor: "rgba(239, 68, 68, 0.3)", color: "#fca5a5", fontWeight: 900, fontSize: 15, marginTop: 14 }}>
            🎯 MỤC TIÊU TIÊU DIỆT HÀNG ĐẦU
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 38. S069: CON DẤU 'ĐÃ THANH TOÁN XONG' ĐÓNG DẤU ĐỎ LÊN THẺ ---
  // =========================================================================
  if (sc === "S069") {
    const stampScale = spring({ frame, fps, config: { damping: 10, mass: 0.5, stiffness: 180 } });
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140 }}>
          <div style={tagStyle("#10b981", "#6ee7b7")}>
            <span>🎉</span> CHIẾN THẮNG TÂM LÝ
          </div>
          <div style={headingStyle}>XÓA SỔ HOÀN TOÀN MỘT CHIẾC THẺ TÍN DỤNG</div>
          <div style={subheadStyle}>Cảm giác chiến thắng chiếc thẻ đầu tiên tiếp thêm động lực mạnh mẽ cho cả chặng đường</div>

          <div style={{ position: "relative", width: 440, height: 200, borderRadius: 18, backgroundColor: "#1e293b", border: "1px solid rgba(255,255,255,0.15)", marginTop: 24, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <div style={{ fontSize: 24, fontWeight: 900, color: "#64748b" }}>PLATINUM CARD 40TR</div>
            <div style={{ position: "absolute", transform: `scale(${stampScale}) rotate(-14deg)`, padding: "12px 28px", border: "4px solid #ef4444", color: "#ef4444", fontWeight: 900, fontSize: 32, letterSpacing: "2px", borderRadius: 12, backgroundColor: "rgba(15, 23, 42, 0.85)", boxShadow: "0 0 35px rgba(239, 68, 68, 0.6)" }}>
              ĐÃ TẤT TOÁN 100%
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 39. S070: BƯỚC 3 — TÁI CẤU TRÚC NGÂN SÁCH TRÊN LƯƠNG 12 TRIỆU ---
  // =========================================================================
  if (sc === "S070") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140, border: "2px solid #38bdf8" }}>
          <div style={tagStyle("#38bdf8", "#7dd3fc")}>
            <span>📐</span> BƯỚC 3 TRONG LỘ TRÌNH
          </div>
          <div style={headingStyle}>BƯỚC 3: TÁI CẤU TRÚC NGÂN SÁCH TRÊN LƯƠNG 12 TRIỆU</div>
          <div style={subheadStyle}>Thiết lập kỷ luật tài chính thép để không còn một đồng nào bị rò rỉ vô ích</div>

          <div style={{ display: "flex", gap: 24, marginTop: 24 }}>
            <div style={{ padding: "18px 28px", borderRadius: 16, backgroundColor: "rgba(56, 189, 248, 0.2)", border: "1px solid #38bdf8", textAlign: "center" }}>
              <div style={{ fontSize: 36, marginBottom: 6 }}>💰</div>
              <div style={{ fontSize: 18, fontWeight: 900, color: "#ffffff" }}>Lương Về: 12.000.000đ</div>
            </div>
            <div style={{ padding: "18px 28px", borderRadius: 16, backgroundColor: "rgba(16, 185, 129, 0.2)", border: "1px solid #10b981", textAlign: "center" }}>
              <div style={{ fontSize: 36, marginBottom: 6 }}>⚖️</div>
              <div style={{ fontSize: 18, fontWeight: 900, color: "#ffffff" }}>Tỷ Lệ 33% / 67%</div>
            </div>
          </div>
        </div>
      </div>
    );
  }
if (sc === "S071") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1160 }}>
          <div style={tagStyle("#10b981", "#6ee7b7")}>
            <span>📊</span> CƠ CẤU LƯƠNG 12 TRIỆU
          </div>
          <div style={headingStyle}>TRÍCH TỰ ĐỘNG 4 TRIỆU (33%) TRẢ NỢ GỐC</div>
          <div style={subheadStyle}>Ngay khi lương về tài khoản, chuyển thẳng 4 triệu diệt nợ trước khi chi tiêu</div>

          <div style={{ display: "flex", gap: 32, width: "100%", marginTop: 28, justifyContent: "center" }}>
            <div style={{ flex: 1, padding: 26, borderRadius: 20, backgroundColor: "rgba(16, 185, 129, 0.15)", border: "2px solid #10b981", textAlign: "center" }}>
              <div style={{ fontSize: 16, color: "#6ee7b7", marginBottom: 6 }}>33% LƯƠNG — DIỆT NỢ</div>
              <div style={{ fontSize: 40, fontWeight: 900, color: "#10b981" }}>4.000.000 đ</div>
              <div style={{ fontSize: 14, color: "#cbd5e1", marginTop: 8 }}>Chuyển tự động ngày nhận lương</div>
            </div>
            <div style={{ flex: 1.5, padding: 26, borderRadius: 20, backgroundColor: "rgba(56, 189, 248, 0.15)", border: "2px solid #38bdf8", textAlign: "center" }}>
              <div style={{ fontSize: 16, color: "#7dd3fc", marginBottom: 6 }}>67% LƯƠNG — CHI TIÊU THIẾT YẾU</div>
              <div style={{ fontSize: 40, fontWeight: 900, color: "#38bdf8" }}>8.000.000 đ</div>
              <div style={{ fontSize: 14, color: "#cbd5e1", marginTop: 8 }}>Chia vào 3 phong bì tiền mặt</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 26. S072: 3 PHONG BÌ TIỀN MẶT (NHÀ 3.5TR, ĂN 3.5TR, XĂNG XE 1TR) ---
  // =========================================================================
  if (sc === "S072") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1180 }}>
          <div style={tagStyle("#38bdf8", "#7dd3fc")}>
            <span>✉️</span> KỶ LUẬT 3 PHONG BÌ
          </div>
          <div style={headingStyle}>PHÂN BỔ 8 TRIỆU VÀO 3 PHONG BÌ TIỀN MẶT</div>
          <div style={subheadStyle}>Dùng tiền mặt giới hạn chi tiêu, tuyệt đối không quẹt thẻ</div>

          <div style={{ display: "flex", gap: 24, width: "100%", marginTop: 28 }}>
            <div style={{ flex: 1, padding: 24, borderRadius: 18, backgroundColor: "rgba(30, 41, 59, 0.7)", border: "1px solid #38bdf8", textAlign: "center" }}>
              <div style={{ fontSize: 44, marginBottom: 10 }}>🏠</div>
              <div style={{ fontSize: 20, fontWeight: 900, color: "#ffffff" }}>TIỀN NHÀ & ĐIỆN</div>
              <div style={{ fontSize: 28, fontWeight: 900, color: "#38bdf8", marginTop: 8 }}>3.500.000 đ</div>
            </div>
            <div style={{ flex: 1, padding: 24, borderRadius: 18, backgroundColor: "rgba(30, 41, 59, 0.7)", border: "1px solid #f59e0b", textAlign: "center" }}>
              <div style={{ fontSize: 44, marginBottom: 10 }}>🍚</div>
              <div style={{ fontSize: 20, fontWeight: 900, color: "#ffffff" }}>ĂN UỐNG NẤU TẠI NHÀ</div>
              <div style={{ fontSize: 28, fontWeight: 900, color: "#f59e0b", marginTop: 8 }}>3.500.000 đ</div>
            </div>
            <div style={{ flex: 1, padding: 24, borderRadius: 18, backgroundColor: "rgba(30, 41, 59, 0.7)", border: "1px solid #10b981", textAlign: "center" }}>
              <div style={{ fontSize: 44, marginBottom: 10 }}>🛵</div>
              <div style={{ fontSize: 20, fontWeight: 900, color: "#ffffff" }}>XĂNG XE & PHÁT SINH</div>
              <div style={{ fontSize: 28, fontWeight: 900, color: "#10b981", marginTop: 8 }}>1.000.000 đ</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 27. S080: CÂY TÍCH SẢN TÀI CHÍNH NỞ HOA ---
  // =========================================================================
  
  // =========================================================================
  // --- 42. S074: BƯỚC 4 — THIẾT LẬP LÁ CHẮN QUỸ KHẨN CẤP MINI 2 TRIỆU ---
  // =========================================================================
  if (sc === "S074") {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140, border: "2px solid #10b981", boxShadow: "0 0 60px rgba(16, 185, 129, 0.3)" }}>
          <div style={tagStyle("#10b981", "#6ee7b7")}>
            <span>🛡️</span> BƯỚC 4 TRONG LỘ TRÌNH
          </div>
          <div style={headingStyle}>BƯỚC 4: THIẾT LẬP LÁ CHẮN QUỸ KHẨN CẤP MINI 2 TRIỆU</div>
          <div style={subheadStyle}>Lá chắn tài chính giúp bạn không bao giờ phải quẹt thẻ lại khi gặp sự cố bất ngờ</div>

          <div style={{ display: "flex", gap: 32, alignItems: "center", marginTop: 24 }}>
            <div style={{ fontSize: 72 }}>🛡️</div>
            <div style={{ textAlign: "left" }}>
              <div style={{ fontSize: 36, fontWeight: 900, color: "#10b981" }}>QUỸ KHẨN CẤP: 2.000.000 VNĐ</div>
              <div style={{ fontSize: 16, color: "#94a3b8", marginTop: 6 }}>Dành riêng cho xe hỏng, đau ốm nhẹ — Tuyệt đối không quẹt thẻ!</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 43. S076: ĐỒNG HỒ ĐẾM NGƯỢC 10 THÁNG VỀ MỐC 0 ĐỒNG TRÒN TRĨNH ---
  // =========================================================================
  if (sc === "S076") {
    const monthsLeft = Math.max(0, 10 - Math.floor(animProgress * 10));
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140 }}>
          <div style={tagStyle("#10b981", "#6ee7b7")}>
            <span>⏱️</span> ĐẾM NGƯỢC TỰ DO
          </div>
          <div style={headingStyle}>10 THÁNG NỮA: BẠN SẼ CHÍNH THỨC SẠCH NỢ HOÀN TOÀN!</div>
          <div style={subheadStyle}>Với kỷ luật 4 triệu mỗi tháng, ngày giải phóng tài chính đang đến rất gần</div>

          <div style={{ display: "flex", gap: 40, alignItems: "center", marginTop: 24, justifyContent: "center" }}>
            <div style={{ width: 140, height: 140, borderRadius: "50%", border: "4px solid #10b981", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", backgroundColor: "rgba(16, 185, 129, 0.15)", boxShadow: "0 0 35px rgba(16, 185, 129, 0.4)" }}>
              <span style={{ fontSize: 44, fontWeight: 900, color: "#10b981" }}>{monthsLeft}</span>
              <span style={{ fontSize: 13, color: "#6ee7b7", fontWeight: 800 }}>THÁNG NỮA</span>
            </div>
            <div style={{ fontSize: 36, color: "#10b981", fontWeight: 900 }}>➔</div>
            <div style={{ padding: "20px 28px", borderRadius: 20, backgroundColor: "rgba(16, 185, 129, 0.2)", border: "2px solid #10b981", textAlign: "center" }}>
              <div style={{ fontSize: 16, color: "#6ee7b7" }}>DƯ NỢ THẺ TÍN DỤNG</div>
              <div style={{ fontSize: 40, fontWeight: 900, color: "#ffffff", marginTop: 4 }}>0 ĐỒNG TRÒN TRĨNH</div>
            </div>
          </div>
        </div>
      </div>
    );
  }
if (sc === "S080" || rawText.toLowerCase().includes("cây tích sản")) {
    return (
      <div style={containerStyle}>
        <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1140, border: "2px solid #10b981", boxShadow: "0 0 60px rgba(16, 185, 129, 0.3)" }}>
          <div style={{ fontSize: 80, marginBottom: 16 }}>🌳</div>
          <div style={headingStyle}>CÂY TÍCH SẢN TÀI CHÍNH NỞ HOA</div>
          <div style={subheadStyle}>Tiền lương của bạn từ nay không còn nuôi ngân hàng, mà tạo ra tài sản thực thụ!</div>

          <div style={{ display: "flex", gap: 24, marginTop: 24 }}>
            <div style={{ padding: "14px 28px", borderRadius: 16, backgroundColor: "rgba(16, 185, 129, 0.2)", border: "1px solid #10b981", color: "#6ee7b7", fontSize: 22, fontWeight: 900 }}>
              📈 Chứng Chỉ Quỹ
            </div>
            <div style={{ padding: "14px 28px", borderRadius: 16, backgroundColor: "rgba(245, 158, 11, 0.2)", border: "1px solid #f59e0b", color: "#fcd34d", fontSize: 22, fontWeight: 900 }}>
              🪙 Vàng Tích Lũy
            </div>
          </div>
        </div>
      </div>
    );
  }

  // =========================================================================
  // --- 28. FALLBACK CHUẨN: KHÔNG CÓ ALT TEXT — VẼ GRAPHIC VECTOR CAO CẤP ---
  // =========================================================================
  return (
    <div style={containerStyle}>
      <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 1120 }}>
        <div style={tagStyle("#38bdf8", "#7dd3fc")}>
          <span>💡</span> CHIẾN LƯỢC TÀI CHÍNH THỰC CHIẾN
        </div>

        <h2 style={{ fontSize: 42, fontWeight: 900, color: "#ffffff", lineHeight: 1.35, marginBottom: 16, fontFamily: theme.typography.fontFamily }}>
          {cleanTitle}
        </h2>

        {narration && (
          <p style={{ fontSize: 20, color: "#94a3b8", maxWidth: 900, lineHeight: 1.4, marginBottom: 28, fontFamily: theme.typography.fontFamily }}>
            {narration}
          </p>
        )}

        <div style={{ display: "flex", gap: 10, marginTop: 8 }}>
          <span style={{ width: 12, height: 12, borderRadius: "50%", backgroundColor: "#38bdf8" }} />
          <span style={{ width: 12, height: 12, borderRadius: "50%", backgroundColor: "#818cf8" }} />
          <span style={{ width: 12, height: 12, borderRadius: "50%", backgroundColor: "#c084fc" }} />
        </div>
      </div>
    </div>
  );
};

// Common decoupled styles ensuring ample spacing
const tagStyle = (borderColor: string, textColor: string): React.CSSProperties => ({
  display: "inline-flex",
  alignItems: "center",
  gap: 10,
  padding: "8px 22px",
  borderRadius: 999,
  backgroundColor: "rgba(15, 23, 42, 0.6)",
  border: `1px solid ${borderColor}`,
  color: textColor,
  fontSize: 16,
  fontWeight: 800,
  letterSpacing: "0.15em",
  textTransform: "uppercase",
  marginBottom: 20,
  fontFamily: theme.typography.fontFamily,
});

const headingStyle: React.CSSProperties = {
  fontSize: 40,
  fontWeight: 900,
  color: "#ffffff",
  lineHeight: 1.3,
  letterSpacing: "-0.01em",
  marginBottom: 12,
  textAlign: "center",
  fontFamily: theme.typography.fontFamily,
};

const subheadStyle: React.CSSProperties = {
  fontSize: 20,
  color: "#cbd5e1",
  lineHeight: 1.4,
  maxWidth: 950,
  textAlign: "center",
  marginBottom: 20,
  fontFamily: theme.typography.fontFamily,
};

const containerStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  justifyContent: "center",
  width: "100%",
  height: "100%",
  backgroundColor: theme.colors.background,
  background: "radial-gradient(ellipse at center, #0e1726 0%, #05070f 85%)",
  color: "#ffffff",
  fontFamily: theme.typography.fontFamily,
  padding: "40px 60px",
  position: "relative",
  overflow: "hidden",
};

const cardStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  textAlign: "center",
  padding: "44px 56px",
  borderRadius: 32,
  backgroundColor: "rgba(15, 23, 42, 0.85)",
  border: "1px solid rgba(255, 255, 255, 0.15)",
  boxShadow: "0 25px 60px rgba(0, 0, 0, 0.6)",
  backdropFilter: "blur(20px)",
  width: "100%",
};
