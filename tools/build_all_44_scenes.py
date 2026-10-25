# Python script to generate DynamicGraphic.tsx with all 44 scenes
import os, sys

target_path = 'channels/tien-thuc-chien/template/components/DynamicGraphic.tsx'

# Let's read the current file up to line 770
with open(target_path, 'r', encoding='utf-8') as f:
    text = f.read()

# We know lines up to S037 are already solid.
# Let's inspect where S037 ends and where S045 starts:
idx_s037_end = text.find('if (sc === "S045")')
if idx_s037_end == -1:
    print("Could not find S045 anchor")
    sys.exit(1)

part1 = text[:idx_s037_end]

# S038, S042, S044
between_s037_and_s045 = """
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
"""

# Let's inspect where S048 ends and where S062 starts:
idx_s048_start = text.find('if (sc === "S048")')
idx_s062_start = text.find('if (sc === "S062")')

part_s045_to_s048 = text[idx_s037_end:idx_s062_start]

# S049, S050, S053, S057, S059, S060
between_s048_and_s062 = """
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
"""

# Let's inspect where S062 ends and where S071 starts:
idx_s071_start = text.find('if (sc === "S071")')
part_s062 = text[idx_s062_start:idx_s071_start]

# S063, S065, S066, S068, S069, S070
between_s062_and_s071 = """
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
"""

# Let's inspect where S072 ends and where S080 starts:
idx_s080_start = text.find('if (sc === "S080"')
part_s071_s072 = text[idx_s071_start:idx_s080_start]

# S074, S076
between_s072_and_s080 = """
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
"""

part_s080_to_end = text[idx_s080_start:]

full_new_code = (
    part1 +
    between_s037_and_s045 +
    part_s045_to_s048 +
    between_s048_and_s062 +
    part_s062 +
    between_s062_and_s071 +
    part_s071_s072 +
    between_s072_and_s080 +
    part_s080_to_end
)

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(full_new_code)

print(f"Successfully wrote full code with ALL 44 scenes! Length: {len(full_new_code)}")
