#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/build_dynamic_graphic_v2.py
Generates channels/tien-thuc-chien/template/components/DynamicGraphicVideo2.tsx
with full dedicated vector graphics for all 81 GFX scenes in Video #2.
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

output_file = Path("channels/tien-thuc-chien/template/components/DynamicGraphicVideo2.tsx")

code_parts = []

code_parts.append('''import React from "react";
import { interpolate, useCurrentFrame, spring, useVideoConfig } from "remotion";
import { theme } from "../theme";

interface DynamicGraphicVideo2Props {
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

export const cleanText = (t: string): string => {
  if (!t) return "";
  return t
    .replace(/^[A-Za-z0-9_]+(\\s+[^\\:]+)?:\\s*/i, "")
    .replace(/^Tiêu đề\\s*[\\:\\'\\"]*/i, "")
    .replace(/[\\'\\"]$/g, "")
    .trim();
};

export const DynamicGraphicVideo2: React.FC<DynamicGraphicVideo2Props> = ({
  title = "",
  label = "",
  description = "",
  scene = "",
  durationInFrames = 120,
  props = {},
  narration = "",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const sc = (scene || "").toUpperCase();
  const cleanTitle = cleanText(title || description || "");

  // Spring entrance
  const enterSpring = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.7, stiffness: 85 },
  });

  const scale = interpolate(enterSpring, [0, 1], [0.94, 1]);
  const opacity = interpolate(enterSpring, [0, 0.4], [0, 1]);
  const translateY = interpolate(enterSpring, [0, 1], [20, 0]);
  const animProgress = Math.min(1, Math.max(0, frame / (durationInFrames || 120)));
''')

def add_scene(sid, tag_icon, tag_text, tag_color, tag_bg, title, subhead, svg_jsx):
    code_parts.append(f'''
  // =========================================================================
  // --- {sid}: {title} ---
  // =========================================================================
  if (sc === "{sid}") {{
    return (
      <div style={{containerStyle}}>
        <div style={{{{ ...cardStyle, transform: `scale(${{scale}}) translateY(${{translateY}}px)`, opacity, maxWidth: 1140, border: "2px solid {tag_color}", boxShadow: "0 0 45px {tag_color}33" }}}}>
          <div style={{tagStyle("{tag_color}", "{tag_bg}")}}>
            <span>{tag_icon}</span> {tag_text}
          </div>
          <div style={{headingStyle}}>{title}</div>
          <div style={{subheadStyle}}>{subhead}</div>

          <div style={{{{ width: "100%", height: 280, position: "relative", display: "flex", justifyContent: "center", alignItems: "center" }}}}>
            {svg_jsx}
          </div>
        </div>
      </div>
    );
  }}''')

# ==================== BEAT 1: HOOK ====================
add_scene(
    "S006", "📈", "NGHỊCH LÝ DÒNG TIỀN", "#ef4444", "#fca5a5",
    "ĐƯỜNG LƯƠNG TĂNG SONG SONG VỚI ĐƯỜNG CHI TIÊU",
    "Khi thu nhập tăng 100%, mức sống và chi tiêu cũng lập tức tăng tương ứng",
    '''<svg viewBox="0 0 700 240" style={{ width: "100%", height: "100%" }}>
      <line x1="100" y1="200" x2="600" y2="200" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
      <line x1="100" y1="40" x2="100" y2="200" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
      {/* Green Income Line */}
      <path d={`M 100 180 Q 350 ${180 - animProgress * 120} 600 ${180 - animProgress * 140}`} fill="none" stroke="#10b981" strokeWidth="6" strokeLinecap="round" />
      <circle cx={100 + animProgress * 500} cy={180 - animProgress * 140} r="8" fill="#10b981" />
      <text x="610" y="45" fill="#10b981" fontSize="18" fontWeight="bold">LƯƠNG: +100%</text>
      {/* Red Expense Line */}
      <path d={`M 100 190 Q 350 ${190 - animProgress * 120} 600 ${190 - animProgress * 140}`} fill="none" stroke="#ef4444" strokeWidth="6" strokeLinecap="round" strokeDasharray="8 8" />
      <circle cx={100 + animProgress * 500} cy={190 - animProgress * 140} r="8" fill="#ef4444" />
      <text x="610" y="75" fill="#ef4444" fontSize="18" fontWeight="bold">CHI TIÊU: +100%</text>
      <text x="350" y="230" fill="#94a3b8" fontSize="16" textAnchor="middle">KHOẢNG CÁCH TÍCH LŨY = 0 ĐỒNG</text>
    </svg>'''
)

add_scene(
    "S007", "⚠️", "CẠM BẪY VÔ HÌNH", "#f59e0b", "#fde68a",
    "CHIẾC BẪY LẠM PHÁT LỐI SỐNG",
    "Thứ âm thầm nuốt chửng mọi thành quả làm việc chăm chỉ của bạn",
    '''<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="150" y="40" width="300" height="150" rx="20" fill="rgba(245, 158, 11, 0.1)" stroke="#f59e0b" strokeWidth="4" />
      <circle cx="300" cy="115" r={50 + Math.sin(frame * 0.1) * 8} fill="rgba(245, 158, 11, 0.2)" stroke="#f59e0b" strokeWidth="3" />
      <text x="300" y="105" fill="#fde68a" fontSize="32" textAnchor="middle" fontWeight="bold">🧀</text>
      <text x="300" y="140" fill="#ffffff" fontSize="20" textAnchor="middle" fontWeight="bold">MỨC SỐNG CAO HƠN</text>
      <path d={`M 200 60 L ${200 + animProgress * 200} 170`} stroke="#ef4444" strokeWidth="5" strokeLinecap="round" />
      <text x="300" y="225" fill="#ef4444" fontSize="16" textAnchor="middle" fontWeight="bold">BẪY CHUỘT BẰNG VÀNG ĐANG SẬP XUỐNG</text>
    </svg>'''
)

# ==================== BEAT 2: BÓC THỰC TRẠNG ====================
add_scene(
    "S010", "🏠", "ĐIỂM XUẤT PHÁT", "#38bdf8", "#bae6fd",
    "BẢNG KÊ CHI PHÍ NHÀ Ở THỜI LƯƠNG 10 TRIỆU",
    "Thuê phòng nhỏ 2.5 triệu, điện nước 500 nghìn, tổng 3 triệu mỗi tháng",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="30" width="490" height="180" rx="16" fill="rgba(30, 41, 59, 0.7)" stroke="#38bdf8" strokeWidth="2" />
      <text x="120" y="75" fill="#cbd5e1" fontSize="18">Tiền thuê phòng trọ:</text>
      <text x="480" y="75" fill="#38bdf8" fontSize="20" fontWeight="bold">2.500.000 đ</text>
      <text x="120" y="120" fill="#cbd5e1" fontSize="18">Điện, nước, internet:</text>
      <text x="480" y="120" fill="#38bdf8" fontSize="20" fontWeight="bold">500.000 đ</text>
      <line x1="120" y1="145" x2="530" y2="145" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
      <text x="120" y="185" fill="#ffffff" fontSize="20" fontWeight="bold">TỔNG CHI PHÍ NHÀ Ở:</text>
      <text x="480" y="185" fill="#10b981" fontSize="22" fontWeight="900">3.000.000 đ (30%)</text>
    </svg>'''
)

add_scene(
    "S012", "🏢", "NÂNG CẤP VỘI VÃ", "#ef4444", "#fca5a5",
    "HỢP ĐỒNG THUÊ CĂN HỘ MỚI KHI LƯƠNG 20 TRIỆU",
    "Tiền nhà 6 triệu, phí dịch vụ 1 triệu, điện nước 2 triệu, tổng 9 triệu",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="20" width="490" height="200" rx="16" fill="rgba(30, 41, 59, 0.85)" stroke="#ef4444" strokeWidth="3" />
      <text x="120" y="65" fill="#cbd5e1" fontSize="18">Tiền thuê căn hộ dịch vụ:</text>
      <text x="480" y="65" fill="#fca5a5" fontSize="20" fontWeight="bold">6.000.000 đ</text>
      <text x="120" y="105" fill="#cbd5e1" fontSize="18">Phí quản lý & gửi xe:</text>
      <text x="480" y="105" fill="#fca5a5" fontSize="20" fontWeight="bold">1.000.000 đ</text>
      <text x="120" y="145" fill="#cbd5e1" fontSize="18">Điện nước giá thương mại:</text>
      <text x="480" y="145" fill="#fca5a5" fontSize="20" fontWeight="bold">2.000.000 đ</text>
      <line x1="120" y1="165" x2="530" y2="165" stroke="#ef4444" strokeWidth="2" />
      <text x="120" y="200" fill="#ffffff" fontSize="20" fontWeight="bold">TỔNG CHI PHÍ MỚI:</text>
      <text x="480" y="200" fill="#ef4444" fontSize="24" fontWeight="900">9.000.000 đ (45%)</text>
    </svg>'''
)

add_scene(
    "S013", "⚖️", "CÁN CÂN CHI PHÍ", "#f59e0b", "#fde68a",
    "CHI PHÍ NHÀ Ở TĂNG GẤP 3 LẦN",
    "Từ 3 triệu vọt lên 9 triệu đồng mỗi tháng, nuốt trọn phần lớn tiền tăng thêm",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      {/* Old column */}
      <rect x="150" y={190 - animProgress * 50} width="120" height={animProgress * 50} rx="10" fill="#10b981" />
      <text x="210" y="130" fill="#10b981" fontSize="20" fontWeight="bold" textAnchor="middle">3 TRIỆU</text>
      <text x="210" y="220" fill="#cbd5e1" fontSize="16" textAnchor="middle">Phòng trọ cũ</text>
      {/* New column */}
      <rect x="380" y={190 - animProgress * 150} width="120" height={animProgress * 150} rx="10" fill="#ef4444" />
      <text x="440" y={180 - animProgress * 150} fill="#ef4444" fontSize="24" fontWeight="900" textAnchor="middle">9 TRIỆU</text>
      <text x="440" y="220" fill="#cbd5e1" fontSize="16" textAnchor="middle">Chung cư mới</text>
      <text x="325" y="50" fill="#f59e0b" fontSize="20" fontWeight="bold" textAnchor="middle">TĂNG VỌT +300%!</text>
    </svg>'''
)

add_scene(
    "S015", "⏱️", "TỔNG THẤT THOÁT", "#ef4444", "#fca5a5",
    "10 THÁNG THUÊ NHÀ = GẦN MỘT NĂM LƯƠNG CŨ",
    "Mỗi năm việc đổi chỗ ở đã nuốt chửng 60 triệu đồng tiền chênh lệch của bạn",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="100" y="40" width="450" height="150" rx="16" fill="rgba(239, 68, 68, 0.15)" stroke="#ef4444" strokeWidth="3" />
      <text x="325" y="85" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">CHÊNH LỆCH: 6.000.000 đ / THÁNG</text>
      <text x="325" y="125" fill="#fca5a5" fontSize="18" textAnchor="middle">x 10 THÁNG = 60.000.000 đ BỐC HƠI</text>
      <path d={`M 150 160 L ${150 + animProgress * 350} 160`} stroke="#ef4444" strokeWidth="12" strokeLinecap="round" />
      <text x="325" y="220" fill="#cbd5e1" fontSize="16" textAnchor="middle">Tương đương 6 tháng lương cũ đã bị tiêu biến hoàn toàn</text>
    </svg>'''
)

add_scene(
    "S016", "🚨", "NGƯỠNG BÁO ĐỘNG", "#ef4444", "#fca5a5",
    "TỶ TRỌNG TIỀN NHÀ VƯỢT NGƯỠNG AN TOÀN",
    "Chiếm 45% tổng thu nhập hàng tháng trong khi trần tối đa chỉ là 30%",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      {/* Gauge bar */}
      <rect x="100" y="80" width="450" height="40" rx="20" fill="rgba(255,255,255,0.1)" />
      <rect x="100" y="80" width={450 * 0.3} height="40" rx="20" fill="#10b981" />
      <rect x={100 + 450 * 0.3} y="80" width={animProgress * (450 * 0.15)} height="40" fill="#ef4444" />
      <line x1={100 + 450 * 0.3} y1="65" x2={100 + 450 * 0.3} y2="135" stroke="#ffffff" strokeWidth="4" />
      <text x={100 + 450 * 0.3} y="55" fill="#10b981" fontSize="16" fontWeight="bold" textAnchor="middle">CHUẨN: 30%</text>
      <text x="440" y="155" fill="#ef4444" fontSize="22" fontWeight="900" textAnchor="middle">THỰC TẾ: 45% (BÁO ĐỘNG ĐỎ!)</text>
      <text x="325" y="210" fill="#cbd5e1" fontSize="16" textAnchor="middle">Vượt quá 15% trần chịu tải tài chính cá nhân</text>
    </svg>'''
)

add_scene(
    "S019", "☕", "RÒ RỈ VI MÔ", "#f59e0b", "#fde68a",
    "PHÉP TÍNH CHÊNH LỆCH CÀ PHÊ HÀNG NGÀY",
    "Chênh lệch 50 nghìn mỗi ngày lấy đi thêm 1.5 triệu đồng mỗi tháng",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="100" y="30" width="450" height="170" rx="16" fill="rgba(30, 41, 59, 0.7)" stroke="#f59e0b" strokeWidth="2" />
      <text x="140" y="75" fill="#cbd5e1" fontSize="18">Cà phê vỉa hè cũ:</text>
      <text x="450" y="75" fill="#10b981" fontSize="20" fontWeight="bold">15.000 đ / ngày</text>
      <text x="140" y="115" fill="#cbd5e1" fontSize="18">Cà phê thương hiệu mới:</text>
      <text x="450" y="115" fill="#ef4444" fontSize="20" fontWeight="bold">65.000 đ / ngày</text>
      <line x1="140" y1="135" x2="510" y2="135" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
      <text x="140" y="175" fill="#ffffff" fontSize="18">Chênh lệch: +50k x 30 ngày =</text>
      <text x="420" y="175" fill="#f59e0b" fontSize="22" fontWeight="900">+1.500.000 đ</text>
      <text x="325" y="225" fill="#cbd5e1" fontSize="15" textAnchor="middle">Khoản tiền đủ mua một chứng chỉ quỹ tích sản mỗi tháng</text>
    </svg>'''
)

add_scene(
    "S021", "🍱", "ĂN TRƯA CÔNG SỞ", "#ef4444", "#fca5a5",
    "CHI PHÍ ĂN TRƯA TĂNG GẦN GẤP 3",
    "Từ cơm bình dân 900 nghìn vọt lên 2.5 triệu đồng mỗi tháng",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="140" y={190 - animProgress * 60} width="140" height={animProgress * 60} rx="12" fill="#10b981" />
      <text x="210" y="120" fill="#10b981" fontSize="20" fontWeight="bold" textAnchor="middle">900.000 đ</text>
      <text x="210" y="215" fill="#cbd5e1" fontSize="16" textAnchor="middle">Cơm bình dân (35k)</text>
      <rect x="370" y={190 - animProgress * 150} width="140" height={animProgress * 150} rx="12" fill="#ef4444" />
      <text x="440" y={180 - animProgress * 150} fill="#ef4444" fontSize="22" fontWeight="900" textAnchor="middle">2.500.000 đ</text>
      <text x="440" y="215" fill="#cbd5e1" fontSize="16" textAnchor="middle">Nhà hàng (100k)</text>
      <text x="325" y="40" fill="#f59e0b" fontSize="18" fontWeight="bold" textAnchor="middle">THẤT THOÁT THÊM 1.600.000 đ / THÁNG</text>
    </svg>'''
)

add_scene(
    "S023", "💸", "TỔNG RÒ RỈ ĂN UỐNG", "#ef4444", "#fca5a5",
    "CHI PHÍ ĂN UỐNG & GIẢI TRÍ TĂNG TỪ 3TR LÊN 7.5TR",
    "Mỗi tháng cuốn bay thêm hơn 4 triệu đồng mà không hề để ý",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="100" y="40" width="450" height="150" rx="16" fill="rgba(30, 41, 59, 0.8)" stroke="#ef4444" strokeWidth="2" />
      <text x="140" y="80" fill="#cbd5e1" fontSize="18">Thời điểm lương 10 triệu:</text>
      <text x="460" y="80" fill="#10b981" fontSize="20" fontWeight="bold">3.000.000 đ</text>
      <text x="140" y="125" fill="#cbd5e1" fontSize="18">Thời điểm lương 20 triệu:</text>
      <text x="460" y="125" fill="#ef4444" fontSize="24" fontWeight="900">7.500.000 đ</text>
      <line x1="140" y1="145" x2="510" y2="145" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
      <text x="325" y="175" fill="#f59e0b" fontSize="18" fontWeight="bold" textAnchor="middle">BỐC HƠI THÊM: 4.500.000 đ MỖI THÁNG</text>
    </svg>'''
)

add_scene(
    "S024", "🔪", "CẢNH BÁO TÀI CHÍNH", "#ef4444", "#fca5a5",
    "RÒ RỈ VI MÔ LÀ CON DAO CẮT ĐỨT DÒNG TIỀN",
    "Những khoản tiền nhỏ không gây sốc nhưng âm thầm rút cạn tương lai",
    '''<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="300" cy="90" r="50" fill="rgba(239, 68, 68, 0.2)" stroke="#ef4444" strokeWidth="3" />
      <text x="300" y="105" fill="#ffffff" fontSize="40" textAnchor="middle">💧</text>
      <text x="300" y="170" fill="#ef4444" fontSize="22" fontWeight="900" textAnchor="middle">NƯỚC CHẢY QUA KẼ TAY</text>
      <text x="300" y="205" fill="#cbd5e1" fontSize="16" textAnchor="middle">100k/ngày = 36 triệu/năm tích sản bị triệt tiêu</text>
    </svg>'''
)

add_scene(
    "S027", "🛵", "TRẢ GÓP XE MỚI", "#38bdf8", "#bae6fd",
    "HỢP ĐỒNG TRẢ GÓP XE TAY GA ĐẮT TIỀN",
    "Trả góp 2.5 triệu mỗi tháng trong vòng 2 năm vì nghĩ mình thừa sức",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="30" width="490" height="170" rx="16" fill="rgba(15, 23, 42, 0.85)" stroke="#38bdf8" strokeWidth="2" />
      <text x="120" y="75" fill="#cbd5e1" fontSize="18">Giá trị xe tay ga mới:</text>
      <text x="480" y="75" fill="#38bdf8" fontSize="20" fontWeight="bold">80.000.000 đ</text>
      <text x="120" y="115" fill="#cbd5e1" fontSize="18">Trả góp hàng tháng:</text>
      <text x="480" y="115" fill="#ef4444" fontSize="22" fontWeight="bold">2.500.000 đ / tháng</text>
      <text x="120" y="155" fill="#cbd5e1" fontSize="18">Thời hạn cam kết nợ:</text>
      <text x="480" y="155" fill="#f59e0b" fontSize="20" fontWeight="bold">24 Tháng liên tục</text>
      <text x="325" y="225" fill="#cbd5e1" fontSize="15" textAnchor="middle">Một khoản nợ cố định 60 triệu đè nặng lên thu nhập</text>
    </svg>'''
)

add_scene(
    "S029", "🚗", "ĐẶT XE CÔNG NGHỆ", "#f59e0b", "#fde68a",
    "LỊCH SỬ CHUYẾN ĐI ĐẶT XE Ô TÔ",
    "Mỗi tuần 4 cuốc xe ô tô, một tháng tiêu tốn thêm 1.2 triệu đồng",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="100" y="35" width="450" height="160" rx="16" fill="rgba(30, 41, 59, 0.8)" stroke="#f59e0b" strokeWidth="2" />
      <text x="140" y="80" fill="#cbd5e1" fontSize="18">Tần suất đặt xe ô tô:</text>
      <text x="450" y="80" fill="#fde68a" fontSize="20" fontWeight="bold">4 Chuyến / tuần</text>
      <text x="140" y="120" fill="#cbd5e1" fontSize="18">Giá cước trung bình:</text>
      <text x="450" y="120" fill="#fde68a" fontSize="20" fontWeight="bold">75.000 đ / chuyến</text>
      <line x1="140" y1="140" x2="510" y2="140" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
      <text x="140" y="175" fill="#ffffff" fontSize="18">Tổng phát sinh mỗi tháng:</text>
      <text x="430" y="175" fill="#ef4444" fontSize="22" fontWeight="900">1.200.000 đ</text>
    </svg>'''
)

add_scene(
    "S030", "⚙️", "HỆ SINH THÁI XE CỘ", "#ef4444", "#fca5a5",
    "CHI PHÍ PHƯƠNG TIỆN TĂNG GẤP 8 LẦN",
    "Xăng xe, bảo dưỡng, gửi xe và trả góp vọt lên 4 triệu đồng mỗi tháng",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="150" y={190 - animProgress * 30} width="120" height={animProgress * 30} rx="10" fill="#10b981" />
      <text x="210" y="150" fill="#10b981" fontSize="18" fontWeight="bold" textAnchor="middle">500.000 đ</text>
      <text x="210" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Xe máy cũ</text>
      <rect x="380" y={190 - animProgress * 150} width="120" height={animProgress * 150} rx="10" fill="#ef4444" />
      <text x="440" y={180 - animProgress * 150} fill="#ef4444" fontSize="22" fontWeight="900" textAnchor="middle">4.000.000 đ</text>
      <text x="440" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Xe mới + Trả góp</text>
      <text x="325" y="45" fill="#f59e0b" fontSize="18" fontWeight="bold" textAnchor="middle">GẤP 8 LẦN CHI PHÍ CŨ!</text>
    </svg>'''
)

add_scene(
    "S032", "🕸️", "BẪY BẢO TRÌ", "#ef4444", "#fca5a5",
    "MUA TÀI SẢN GIÁ CAO KÉO THEO CHI PHÍ VẬN HÀNH CAO",
    "Bạn không chỉ mua đồ vật, bạn đang cam kết trả một chuỗi chi phí dài hạn",
    '''<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="300" cy="110" r="45" fill="#38bdf8" />
      <text x="300" y="115" fill="#ffffff" fontSize="15" fontWeight="bold" textAnchor="middle">MUA ĐỒ</text>
      {/* Surrounding circles */}
      <circle cx="160" cy="70" r="32" fill="rgba(239, 68, 68, 0.3)" stroke="#ef4444" strokeWidth="2" />
      <text x="160" y="75" fill="#fca5a5" fontSize="12" textAnchor="middle">Bảo dưỡng</text>
      <circle cx="440" cy="70" r="32" fill="rgba(239, 68, 68, 0.3)" stroke="#ef4444" strokeWidth="2" />
      <text x="440" y="75" fill="#fca5a5" fontSize="12" textAnchor="middle">Gửi xe đắt</text>
      <circle cx="160" cy="160" r="32" fill="rgba(239, 68, 68, 0.3)" stroke="#ef4444" strokeWidth="2" />
      <text x="160" y="165" fill="#fca5a5" fontSize="12" textAnchor="middle">Bảo hiểm</text>
      <circle cx="440" cy="160" r="32" fill="rgba(239, 68, 68, 0.3)" stroke="#ef4444" strokeWidth="2" />
      <text x="440" y="165" fill="#fca5a5" fontSize="12" textAnchor="middle">Phụ tùng</text>
      <line x1="200" y1="80" x2="260" y2="100" stroke="#ef4444" strokeWidth="2" />
      <line x1="400" y1="80" x2="340" y2="100" stroke="#ef4444" strokeWidth="2" />
      <line x1="200" y1="150" x2="260" y2="120" stroke="#ef4444" strokeWidth="2" />
      <line x1="400" y1="150" x2="340" y2="120" stroke="#ef4444" strokeWidth="2" />
      <text x="300" y="225" fill="#cbd5e1" fontSize="15" textAnchor="middle">Chuỗi chi phí phái sinh bám theo tài sản</text>
    </svg>'''
)

add_scene(
    "S035", "💳", "TRẢ GÓP 0%", "#f59e0b", "#fde68a",
    "ẢO TƯỞNG TRẢ GÓP LÃI SUẤT 0%",
    "35 triệu mua sắm chia 12 tháng lấy đi 3 triệu mỗi tháng",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="30" width="490" height="170" rx="16" fill="rgba(30, 41, 59, 0.85)" stroke="#f59e0b" strokeWidth="2" />
      <text x="120" y="75" fill="#cbd5e1" fontSize="18">Tổng giá trị đơn hàng công nghệ:</text>
      <text x="480" y="75" fill="#ffffff" fontSize="22" fontWeight="bold">35.000.000 đ</text>
      <text x="120" y="115" fill="#cbd5e1" fontSize="18">Chia đều cho 12 tháng:</text>
      <text x="480" y="115" fill="#f59e0b" fontSize="22" fontWeight="bold">3.000.000 đ / tháng</text>
      <text x="120" y="155" fill="#cbd5e1" fontSize="18">Ảo tưởng tâm lý:</text>
      <text x="480" y="155" fill="#ef4444" fontSize="18" fontWeight="bold">Mỗi tháng chỉ có vài triệu!</text>
      <text x="325" y="225" fill="#cbd5e1" fontSize="15" textAnchor="middle">Nuốt trọn 30% phần tiền lương tăng thêm suốt 1 năm</text>
    </svg>'''
)

add_scene(
    "S038", "🛍️", "MUA SẮM CÁ NHÂN", "#ef4444", "#fca5a5",
    "CHI PHÍ MUA SẮM NGẪU HỨNG",
    "Đồ công nghệ và quần áo lấy đi thêm 3.5 triệu đồng mỗi tháng",
    '''<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="100" y="40" width="400" height="150" rx="16" fill="rgba(239, 68, 68, 0.15)" stroke="#ef4444" strokeWidth="3" />
      <text x="300" y="85" fill="#ffffff" fontSize="20" fontWeight="bold" textAnchor="middle">MUA SẮM ONLINE & ĐỒ CÔNG NGHỆ</text>
      <text x="300" y="130" fill="#ef4444" fontSize="32" fontWeight="900" textAnchor="middle">+3.500.000 đ / THÁNG</text>
      <text x="300" y="170" fill="#cbd5e1" fontSize="16" textAnchor="middle">Tương đương 42 triệu đồng mỗi năm tiêu biến</text>
    </svg>'''
)

add_scene(
    "S040", "🧠", "HƯNG PHẤN NGẮN HẠN", "#ef4444", "#fca5a5",
    "CHỈ SỐ THỎA MÃN CHỚP NHOÁNG VS NỢ DÀI HẠN",
    "Niềm vui mở hộp đồ mới chỉ kéo dài vài ngày nhưng nợ thẻ kéo dài nhiều tháng",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      {/* Joy curve - drops fast */}
      <path d={`M 100 180 Q 180 50 300 180`} fill="none" stroke="#10b981" strokeWidth="5" />
      <text x="200" y="50" fill="#10b981" fontSize="16" fontWeight="bold">Niềm vui: 3 ngày</text>
      {/* Debt line - long flat */}
      <line x1="100" y1="120" x2="550" y2="120" stroke="#ef4444" strokeWidth="5" strokeDasharray="6 6" />
      <text x="450" y="105" fill="#ef4444" fontSize="18" fontWeight="bold">Nợ thẻ: 12 tháng!</text>
      <text x="325" y="220" fill="#cbd5e1" fontSize="16" textAnchor="middle">Chúng ta chi tiền thật để mua những cảm xúc thoáng qua</text>
    </svg>'''
)

add_scene(
    "S043", "🥂", "TIỆC TÙNG XÃ GIAO", "#f59e0b", "#fde68a",
    "HÓA ĐƠN TIỆC TÙNG VÀ NGOẠI GIAO",
    "Mỗi buổi gặp gỡ chia hóa đơn không dưới 500 nghìn đến 1 triệu đồng",
    '''<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="100" y="30" width="400" height="170" rx="16" fill="rgba(30, 41, 59, 0.85)" stroke="#f59e0b" strokeWidth="2" />
      <text x="140" y="75" fill="#cbd5e1" fontSize="18">2 Buổi tiệc cuối tuần:</text>
      <text x="420" y="75" fill="#f59e0b" fontSize="20" fontWeight="bold">2.000.000 đ</text>
      <text x="140" y="115" fill="#cbd5e1" fontSize="18">Tiền phong bì cưới hỏi:</text>
      <text x="420" y="115" fill="#f59e0b" fontSize="20" fontWeight="bold">1.500.000 đ</text>
      <line x1="140" y1="135" x2="460" y2="135" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
      <text x="140" y="175" fill="#ffffff" fontSize="18">Tổng chi phí xã giao:</text>
      <text x="400" y="175" fill="#ef4444" fontSize="22" fontWeight="900">3.500.000 đ</text>
    </svg>'''
)

add_scene(
    "S045", "🤝", "CHI PHÍ HÌNH ẢNH", "#ef4444", "#fca5a5",
    "CHI PHÍ DUY TRÌ HÌNH ẢNH TĂNG GẤP 3.5 LẦN",
    "Tăng từ 1 triệu lên 3.5 triệu mỗi tháng để giữ gìn quan hệ và vỏ bọc",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="150" y={190 - animProgress * 40} width="120" height={animProgress * 40} rx="10" fill="#10b981" />
      <text x="210" y="140" fill="#10b981" fontSize="18" fontWeight="bold" textAnchor="middle">1.000.000 đ</text>
      <text x="210" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Trước đây</text>
      <rect x="380" y={190 - animProgress * 140} width="120" height={animProgress * 140} rx="10" fill="#ef4444" />
      <text x="440" y={180 - animProgress * 140} fill="#ef4444" fontSize="22" fontWeight="900" textAnchor="middle">3.500.000 đ</text>
      <text x="440" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Hiện tại</text>
      <text x="325" y="45" fill="#f59e0b" fontSize="18" fontWeight="bold" textAnchor="middle">THẤT THOÁT THÊM 2.5 TRIỆU / THÁNG</text>
    </svg>'''
)

add_scene(
    "S047", "📊", "TỔNG KẾT 5 HẠNG MỤC", "#ef4444", "#fca5a5",
    "BẢNG CÂN ĐỐI 5 KHOẢN TỰ ĐỘNG NÂNG CẤP",
    "Nhà ở +6tr, Ăn uống +4tr, Xe +3.5tr, Mua sắm +3.5tr, Xã giao +2.5tr",
    '''<svg viewBox="0 0 700 240" style={{ width: "100%", height: "100%" }}>
      <rect x="50" y="20" width="600" height="200" rx="16" fill="rgba(30, 41, 59, 0.9)" stroke="#ef4444" strokeWidth="2" />
      <text x="80" y="55" fill="#cbd5e1" fontSize="16">1. Nhà ở & Tiện ích: +6.000.000 đ</text>
      <text x="80" y="85" fill="#cbd5e1" fontSize="16">2. Ăn uống & Cà phê: +4.000.000 đ</text>
      <text x="80" y="115" fill="#cbd5e1" fontSize="16">3. Xe cộ & Di chuyển: +3.500.000 đ</text>
      <text x="80" y="145" fill="#cbd5e1" fontSize="16">4. Mua sắm & Công nghệ: +3.500.000 đ</text>
      <text x="80" y="175" fill="#cbd5e1" fontSize="16">5. Xã giao & Hình ảnh: +2.500.000 đ</text>
      <line x1="420" y1="35" x2="420" y2="195" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
      <text x="535" y="80" fill="#ffffff" fontSize="18" textAnchor="middle">LƯƠNG TĂNG:</text>
      <text x="535" y="110" fill="#10b981" fontSize="22" fontWeight="bold" textAnchor="middle">+10 TRIỆU</text>
      <text x="535" y="150" fill="#ffffff" fontSize="18" textAnchor="middle">CHI PHÍ TĂNG:</text>
      <text x="535" y="180" fill="#ef4444" fontSize="24" fontWeight="900" textAnchor="middle">+19.5 TRIỆU!</text>
    </svg>'''
)

add_scene(
    "S048", "🔴", "SỰ THẬT TÀN NHẪN", "#ef4444", "#fca5a5",
    "THU NHẬP 20 TRIỆU — SỐ DƯ CUỐI THÁNG BẰNG 0",
    "Lương tăng gấp đôi nhưng ví tiền vẫn rỗng không vào cuối tháng",
    '''<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="490" height="150" rx="20" fill="rgba(239, 68, 68, 0.2)" stroke="#ef4444" strokeWidth="4" />
      <text x="325" y="90" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">THU NHẬP: 20 TRIỆU = TỔNG CHI: 20 TRIỆU</text>
      <text x="325" y="150" fill="#ef4444" fontSize="48" fontWeight="900" textAnchor="middle">SỐ DƯ: 0 ĐỒNG</text>
      <text x="325" y="220" fill="#cbd5e1" fontSize="16" textAnchor="middle">Vòng lặp bất an tài chính vẫn lặp lại y hệt</text>
    </svg>'''
)

print(f"Generated up to Beat 2. Total parts: {len(code_parts)}")

# ==================== BEAT 3: SỐ LIỆU & GIẢI PHẪU 3 BẪY TÂM LÝ ====================
add_scene(
    "S050", "🎡", "BẪY TÂM LÝ SỐ 1", "#818cf8", "#c7d2fe",
    "CỖ MÁY THÍCH NGHI KHOÁI LẠC",
    "Não bộ thích nghi cực nhanh với mọi sự sung túc và tiện nghi mới",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="325" cy="110" r="70" fill="none" stroke="#818cf8" strokeWidth="6" strokeDasharray="12 12" />
      <circle cx="325" cy="110" r="45" fill="rgba(129, 140, 248, 0.2)" />
      <text x="325" y="115" fill="#ffffff" fontSize="16" fontWeight="bold" textAnchor="middle">MÁY CHẠY BỘ</text>
      <text x="325" y="215" fill="#c7d2fe" fontSize="16" textAnchor="middle">Chân chạy càng nhanh nhưng vị trí vẫn dậm chân tại chỗ</text>
    </svg>"""
)

add_scene(
    "S051", "📉", "SÓNG CẢM XÚC", "#f59e0b", "#fde68a",
    "HẠNH PHÚC TĂNG VỌT RỒI TỤT DỐC SAU 30 NGÀY",
    "Chỉ sau một tháng, căn hộ mới trở thành tiêu chuẩn bình thường mới",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <line x1="80" y1="180" x2="580" y2="180" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
      <line x1="80" y1="40" x2="80" y2="180" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
      {/* Curve peaking then falling to baseline */}
      <path d={`M 80 180 Q 200 30 350 175 T 580 180`} fill="none" stroke="#f59e0b" strokeWidth="6" strokeLinecap="round" />
      <circle cx="210" cy="50" r="8" fill="#10b981" />
      <text x="210" y="35" fill="#10b981" fontSize="16" fontWeight="bold" textAnchor="middle">Hưng phấn: Tuần 1</text>
      <circle cx="450" cy="178" r="8" fill="#ef4444" />
      <text x="450" y="160" fill="#ef4444" fontSize="16" fontWeight="bold" textAnchor="middle">Bình thường mới: Ngày 30</text>
    </svg>"""
)

add_scene(
    "S054", "🪜", "BẬC THANG THÍCH NGHI", "#ef4444", "#fca5a5",
    "TIÊU CHUẨN SỐNG TĂNG LÊN VĨNH VIỄN",
    "Sự thỏa mãn biến mất nhưng bạn không thể quay về phòng trọ cũ được nữa",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <path d="M 120 190 L 260 190 L 260 130 L 400 130 L 400 70 L 540 70" fill="none" stroke="#ef4444" strokeWidth="6" />
      <text x="190" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Trọ 2.5tr</text>
      <text x="330" y="155" fill="#cbd5e1" fontSize="15" textAnchor="middle">Chung cư 6tr</text>
      <text x="470" y="95" fill="#fca5a5" fontSize="15" textAnchor="middle">Cao cấp 10tr?</text>
      <text x="325" y="35" fill="#f59e0b" fontSize="18" fontWeight="bold" textAnchor="middle">VAN MỘT CHIỀU: DỄ LÊN, KHÔNG THỂ XUỐNG</text>
    </svg>"""
)

add_scene(
    "S056", "🔄", "VÒNG LẶP LUẨN QUẨN", "#f59e0b", "#fde68a",
    "CHU KỲ BẪY THU NHẬP VÀ CHI TIÊU",
    "Kiếm nhiều hơn -> Tiêu nhiều hơn -> Cần cày cuốc nhiều hơn để nuôi mức sống",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="80" width="140" height="60" rx="12" fill="rgba(16, 185, 129, 0.2)" stroke="#10b981" strokeWidth="2" />
      <text x="150" y="115" fill="#10b981" fontSize="15" fontWeight="bold" textAnchor="middle">Kiếm nhiều tiền</text>
      <path d="M 230 110 L 270 110" stroke="#ffffff" strokeWidth="3" markerEnd="url(#arrow)" />
      <rect x="280" y="80" width="140" height="60" rx="12" fill="rgba(239, 68, 68, 0.2)" stroke="#ef4444" strokeWidth="2" />
      <text x="350" y="115" fill="#ef4444" fontSize="15" fontWeight="bold" textAnchor="middle">Tiêu nhiều hơn</text>
      <path d="M 430 110 L 470 110" stroke="#ffffff" strokeWidth="3" />
      <rect x="480" y="80" width="140" height="60" rx="12" fill="rgba(245, 158, 11, 0.2)" stroke="#f59e0b" strokeWidth="2" />
      <text x="550" y="115" fill="#fde68a" fontSize="15" fontWeight="bold" textAnchor="middle">Áp lực cày cuốc</text>
      <path d="M 550 150 Q 350 210 150 150" fill="none" stroke="#f59e0b" strokeWidth="3" strokeDasharray="6 6" />
      <text x="350" y="225" fill="#cbd5e1" fontSize="14" textAnchor="middle">Bị mắc kẹt trong vòng xoáy chuột chạy</text>
    </svg>"""
)

add_scene(
    "S058", "📉", "TÍNH BẤT ĐỐI XỨNG", "#ef4444", "#fca5a5",
    "CHI PHÍ VĨNH VIỄN — NIỀM VUI TẠM THỜI",
    "Chúng ta liên tục chi tiêu thật cho những cảm giác thỏa mãn ngắn hạn",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="120" y="40" width="410" height="70" rx="14" fill="rgba(239, 68, 68, 0.2)" stroke="#ef4444" strokeWidth="2" />
      <text x="325" y="70" fill="#ffffff" fontSize="16">Cam kết chi phí cố định:</text>
      <text x="325" y="95" fill="#ef4444" fontSize="20" fontWeight="bold">DÀI HẠN & VĨNH VIỄN</text>
      <rect x="120" y="130" width="410" height="70" rx="14" fill="rgba(16, 185, 129, 0.2)" stroke="#10b981" strokeWidth="2" />
      <text x="325" y="160" fill="#ffffff" fontSize="16">Cảm giác hưng phấn hạnh phúc:</text>
      <text x="325" y="185" fill="#10b981" fontSize="20" fontWeight="bold">CHỈ VÀI NGÀY ĐẦU</text>
    </svg>"""
)

add_scene(
    "S060", "🚪", "QUY LUẬT VAN MỘT CHIỀU", "#ef4444", "#fca5a5",
    "NÂNG MỨC SỐNG MẤT 1 NGÀY — HẠ XUỐNG MẤT CẢ NĂM",
    "Những thói quen xa xỉ rất dễ hình thành nhưng cực kỳ khó từ bỏ",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="300" cy="100" r="50" fill="rgba(239, 68, 68, 0.2)" stroke="#ef4444" strokeWidth="4" />
      <text x="300" y="110" fill="#ef4444" fontSize="36" textAnchor="middle">🔒</text>
      <text x="300" y="175" fill="#ffffff" fontSize="20" fontWeight="bold" textAnchor="middle">VAN MỘT CHIỀU CỦA NÃO BỘ</text>
      <text x="300" y="210" fill="#cbd5e1" fontSize="16" textAnchor="middle">Đòi hỏi ý chí phi thường mới có thể thắt lưng buộc bụng</text>
    </svg>"""
)

add_scene(
    "S062", "🔑", "THÔNG ĐIỆP CỐT LÕI", "#10b981", "#a7f3d0",
    "LÀM CHỦ CỖ MÁY THÍCH NGHI ĐỂ TỰ DO TÀI CHÍNH",
    "Nhận diện được cái bẫy này là bước ngoặt đầu tiên để giữ lại tiền",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="440" height="150" rx="18" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" strokeWidth="3" />
      <text x="300" y="90" fill="#10b981" fontSize="36" textAnchor="middle">🗝️</text>
      <text x="300" y="135" fill="#ffffff" fontSize="20" fontWeight="bold" textAnchor="middle">TỈNH THỨC TRƯỚC SỰ TIỆN NGHI</text>
      <text x="300" y="170" fill="#a7f3d0" fontSize="16" textAnchor="middle">Không để mức sống vượt qua năng lực tích sản</text>
    </svg>"""
)

add_scene(
    "S064", "🧥", "BẪY TÂM LÝ SỐ 2", "#f59e0b", "#fde68a",
    "HIỆU ỨNG ĐI-ĐƠ-RÔ — PHẢN ỨNG MUA SẮM DÂY CHUYỀN",
    "Một món đồ nhỏ nâng cấp kích hoạt cả một chuỗi chi tiêu thảm họa",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="160" cy="110" r="50" fill="rgba(239, 68, 68, 0.3)" stroke="#ef4444" strokeWidth="3" />
      <text x="160" y="105" fill="#ffffff" fontSize="24" textAnchor="middle">🧥</text>
      <text x="160" y="130" fill="#fca5a5" fontSize="13" textAnchor="middle">Áo choàng đỏ</text>
      <path d="M 220 110 L 270 110" stroke="#f59e0b" strokeWidth="4" />
      <circle cx="325" cy="110" r="45" fill="rgba(245, 158, 11, 0.3)" stroke="#f59e0b" strokeWidth="3" />
      <text x="325" y="105" fill="#ffffff" fontSize="24" textAnchor="middle">🪑</text>
      <text x="325" y="130" fill="#fde68a" fontSize="13" textAnchor="middle">Bàn ghế mới</text>
      <path d="M 380 110 L 430 110" stroke="#f59e0b" strokeWidth="4" />
      <circle cx="490" cy="110" r="45" fill="rgba(239, 68, 68, 0.3)" stroke="#ef4444" strokeWidth="3" />
      <text x="490" y="105" fill="#ffffff" fontSize="24" textAnchor="middle">🏺</text>
      <text x="490" y="130" fill="#fca5a5" fontSize="13" textAnchor="middle">Thảm & Tượng</text>
      <text x="325" y="210" fill="#cbd5e1" fontSize="15" textAnchor="middle">Món đồ đầu tiên kéo theo toàn bộ tài sản bốc hơi</text>
    </svg>"""
)

add_scene(
    "S067", "💥", "CHUỖI PHẢN ỨNG", "#ef4444", "#fca5a5",
    "SƠ ĐỒ DOMINO CHI TIÊU KHÔNG ĐÁY",
    "Để xứng với chiếc áo, triết gia mua bàn mới, thảm mới và tượng đồng",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="60" width="100" height="100" rx="12" fill="#ef4444" />
      <text x="130" y="105" fill="#ffffff" fontSize="18" fontWeight="bold" textAnchor="middle">ÁO</text>
      <text x="130" y="135" fill="#ffffff" fontSize="12" textAnchor="middle">Choàng</text>
      <text x="205" y="115" fill="#ffffff" fontSize="24">➔</text>
      <rect x="230" y="60" width="100" height="100" rx="12" fill="#f59e0b" />
      <text x="280" y="105" fill="#ffffff" fontSize="18" fontWeight="bold" textAnchor="middle">BÀN</text>
      <text x="280" y="135" fill="#ffffff" fontSize="12" textAnchor="middle">Gỗ mới</text>
      <text x="355" y="115" fill="#ffffff" fontSize="24">➔</text>
      <rect x="380" y="60" width="100" height="100" rx="12" fill="#38bdf8" />
      <text x="430" y="105" fill="#ffffff" fontSize="18" fontWeight="bold" textAnchor="middle">THẢM</text>
      <text x="430" y="135" fill="#ffffff" fontSize="12" textAnchor="middle">Lụa quý</text>
      <text x="505" y="115" fill="#ffffff" fontSize="24">➔</text>
      <rect x="530" y="60" width="90" height="100" rx="12" fill="#ef4444" />
      <text x="575" y="105" fill="#ffffff" fontSize="16" fontWeight="bold" textAnchor="middle">NỢ</text>
      <text x="575" y="135" fill="#ffffff" fontSize="12" textAnchor="middle">Cạn tiền</text>
      <text x="325" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Sự thỏa hiệp ban đầu dẫn tới khủng hoảng tài chính</text>
    </svg>"""
)

add_scene(
    "S069", "📱", "HIỆN THỰC HIỆN ĐẠI", "#38bdf8", "#bae6fd",
    "NÂNG CẤP ĐỒNG BỘ HỆ SINH THÁI",
    "Mua điện thoại mới kéo theo mua ốp lưng, tai nghe và củ sạc đắt tiền",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="490" height="150" rx="16" fill="rgba(15, 23, 42, 0.85)" stroke="#38bdf8" strokeWidth="2" />
      <text x="325" y="80" fill="#38bdf8" fontSize="22" fontWeight="bold" textAnchor="middle">ĐIỆN THOẠI 30 TRIỆU ĐỒNG</text>
      <text x="325" y="120" fill="#cbd5e1" fontSize="16" textAnchor="middle">Kéo theo: Ốp lưng 500k + Sạc 1tr + Tai nghe 3tr</text>
      <text x="325" y="160" fill="#ef4444" fontSize="20" fontWeight="bold" textAnchor="middle">+4.500.000 đ CHI PHÍ BẮT BUỘC ĐỒNG BỘ</text>
      <text x="325" y="225" fill="#cbd5e1" fontSize="15" textAnchor="middle">Hiệu ứng Đi-đơ-rô diễn ra hàng ngày trong vô thức</text>
    </svg>"""
)

add_scene(
    "S071", "📋", "DANH SÁCH CHI PHÍ PHÁI SINH", "#ef4444", "#fca5a5",
    "BẢNG KÊ CÁC KHOẢN TIỀN KÉO THEO",
    "Ốp lưng 500k, sạc nhanh 1tr, tai nghe 3tr và gói bảo hiểm rơi vỡ",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="60" y="20" width="480" height="180" rx="16" fill="rgba(30, 41, 59, 0.9)" stroke="#ef4444" strokeWidth="2" />
      <text x="90" y="60" fill="#cbd5e1" fontSize="16">1. Ốp lưng chính hãng:</text>
      <text x="440" y="60" fill="#ffffff" fontSize="18" fontWeight="bold">500.000 đ</text>
      <text x="90" y="95" fill="#cbd5e1" fontSize="16">2. Củ sạc nhanh công suất lớn:</text>
      <text x="440" y="95" fill="#ffffff" fontSize="18" fontWeight="bold">1.000.000 đ</text>
      <text x="90" y="130" fill="#cbd5e1" fontSize="16">3. Tai nghe không dây cao cấp:</text>
      <text x="440" y="130" fill="#ffffff" fontSize="18" fontWeight="bold">3.000.000 đ</text>
      <text x="90" y="165" fill="#cbd5e1" fontSize="16">4. Gói bảo hiểm rơi vỡ màn hình:</text>
      <text x="440" y="165" fill="#ef4444" fontSize="18" fontWeight="bold">2.500.000 đ</text>
    </svg>"""
)

add_scene(
    "S073", "🧨", "NGÒI NỔ TÀI CHÍNH", "#ef4444", "#fca5a5",
    "MÓN ĐỒ 20TR KÉO THEO 15TR CHI PHÍ PHÁI SINH",
    "Món đồ ban đầu chỉ là ngòi nổ, chuỗi chi tiêu phía sau mới tàn phá túi tiền",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="120" y={190 - animProgress * 80} width="160" height={animProgress * 80} rx="12" fill="#38bdf8" />
      <text x="200" y="95" fill="#38bdf8" fontSize="20" fontWeight="bold" textAnchor="middle">20 TRIỆU</text>
      <text x="200" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Món đồ ban đầu</text>
      <rect x="370" y={190 - animProgress * 140} width="160" height={animProgress * 140} rx="12" fill="#ef4444" />
      <text x="450" y="180 - animProgress * 140} fill="#ef4444" fontSize="22" fontWeight="900" textAnchor="middle">+15 TRIỆU</text>
      <text x="450" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Chuỗi chi tiêu phái sinh</text>
      <text x="325" y="40" fill="#f59e0b" fontSize="18" fontWeight="bold" textAnchor="middle">TỔNG THIỆT HẠI: 35 TRIỆU ĐỒNG!</text>
    </svg>"""
)

add_scene(
    "S075", "🛡️", "DẬP TẮT NGÒI NỔ", "#10b981", "#a7f3d0",
    "DẬP TẮT CHUỖI MUA SẮM TỪ MẮT XÍCH ĐẦU TIÊN",
    "Muốn giữ được tiền, phải chặn đứng ý muốn mua sắm ngay từ món đồ đầu tiên",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="300" cy="100" r="50" fill="rgba(16, 185, 129, 0.2)" stroke="#10b981" strokeWidth="4" />
      <text x="300" y="110" fill="#10b981" fontSize="40" textAnchor="middle">🛑</text>
      <text x="300" y="175" fill="#ffffff" fontSize="20" fontWeight="bold" textAnchor="middle">CHẶN NGAY TỪ ĐẦU</text>
      <text x="300" y="210" fill="#a7f3d0" fontSize="16" textAnchor="middle">Không bắt đầu mắt xích thứ nhất = Bảo vệ an toàn 35 triệu</text>
    </svg>"""
)

add_scene(
    "S078", "⏳", "BẪY TÂM LÝ SỐ 3", "#f59e0b", "#fde68a",
    "THIÊN KIẾN HIỆN TẠI VÀ ẢO TƯỞNG THÁNG SAU TIẾT KIỆM",
    "Bộ não luôn đánh giá phần thưởng hôm nay cao hơn nhiều so với tương lai",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="120" y="50" width="180" height="120" rx="16" fill="rgba(16, 185, 129, 0.2)" stroke="#10b981" strokeWidth="3" />
      <text x="210" y="95" fill="#10b981" fontSize="24" fontWeight="bold" textAnchor="middle">HIỆN TẠI</text>
      <text x="210" y="135" fill="#ffffff" fontSize="16" textAnchor="middle">Sự thỏa mãn ngay</text>
      <text x="325" y="115" fill="#ffffff" fontSize="28" fontWeight="bold" textAnchor="middle">&gt;&gt;&gt;</text>
      <rect x="350" y="50" width="180" height="120" rx="16" fill="rgba(255, 255, 255, 0.05)" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
      <text x="440" y="95" fill="#94a3b8" fontSize="24" fontWeight="bold" textAnchor="middle">TƯƠNG LAI</text>
      <text x="440" y="135" fill="#64748b" fontSize="16" textAnchor="middle">Coi như người xa lạ</text>
      <text x="325" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Cơ chế tiến hóa thúc đẩy tiêu xài ngay lập tức</text>
    </svg>"""
)

add_scene(
    "S080", "👤", "THẦN KINH HỌC", "#818cf8", "#c7d2fe",
    "BẢN THÂN TRONG TƯƠNG LAI BỊ XEM NHƯ NGƯỜI LẠ",
    "Khi nghĩ về mình sau 10 năm, não bộ xử lý thông tin hệt như nghĩ về người dưng",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="200" cy="100" r="45" fill="rgba(16, 185, 129, 0.3)" stroke="#10b981" strokeWidth="3" />
      <text x="200" y="105" fill="#ffffff" fontSize="16" fontWeight="bold" textAnchor="middle">Tôi hôm nay</text>
      <circle cx="400" cy="100" r="45" fill="rgba(100, 116, 139, 0.3)" stroke="#64748b" strokeWidth="3" strokeDasharray="6 6" />
      <text x="400" y="105" fill="#cbd5e1" fontSize="15" textAnchor="middle">Tôi 10 năm sau</text>
      <text x="300" y="105" fill="#ef4444" fontSize="28" textAnchor="middle">≠</text>
      <text x="300" y="180" fill="#ef4444" fontSize="18" fontWeight="bold" textAnchor="middle">SẴN SÀNG TRỪNG PHẠT BẢN THÂN TƯƠNG LAI</text>
      <text x="300" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Để thỏa mãn cảm giác sung sướng chốc lát ở hiện tại</text>
    </svg>"""
)

add_scene(
    "S082", "⚠️", "LỜI NÓI DỐI TAI HẠI", "#ef4444", "#fca5a5",
    "THÁNG SAU TIẾT KIỆM LÀ LỜI HỨA SUÔNG NGUY HIỂM",
    "Nếu hôm nay có thêm tiền không giữ được, tháng sau chắc chắn cũng không",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="490" height="140" rx="16" fill="rgba(239, 68, 68, 0.15)" stroke="#ef4444" strokeWidth="3" />
      <text x="325" y="85" fill="#fca5a5" fontSize="22" fontWeight="bold" textAnchor="middle">"THÁNG SAU MÌNH SẼ BẮT ĐẦU TIẾT KIỆM"</text>
      <text x="325" y="125" fill="#ffffff" fontSize="18" textAnchor="middle">Khi tháng sau đến, nó lại biến thành hiện tại</text>
      <text x="325" y="160" fill="#ef4444" fontSize="20" fontWeight="900" textAnchor="middle">VÀ BẠN SẼ TIẾP TỤC TIÊU SẠCH SỐ TIỀN ĐÓ</text>
    </svg>"""
)

add_scene(
    "S084", "⚙️", "NGUYÊN TẮC THÉP", "#10b981", "#a7f3d0",
    "LOẠI BỎ Ý CHÍ KHỎI QUY TRÌNH GIỮ TIỀN",
    "Cách duy nhất để thắng thiên kiến là tự động hóa trích tiền ngay khi lương về",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="100" y="40" width="400" height="150" rx="16" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" strokeWidth="3" />
      <text x="300" y="85" fill="#10b981" fontSize="36" textAnchor="middle">🤖</text>
      <text x="300" y="130" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">TỰ ĐỘNG HÓA 100%</text>
      <text x="300" y="165" fill="#a7f3d0" fontSize="16" textAnchor="middle">Không dựa vào sự kiên nhẫn hay ý chí cảm tính</text>
    </svg>"""
)

add_scene(
    "S086", "⚖️", "BÀI TOÁN CHI PHÍ CƠ HỘI", "#38bdf8", "#bae6fd",
    "HAI KỊCH BẢN ĐỐI LẬP CHO 10 TRIỆU LƯƠNG TĂNG",
    "Kịch bản A tiêu hết vào mức sống vs Kịch bản B tích sản 50%",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="50" y="40" width="250" height="150" rx="16" fill="rgba(239, 68, 68, 0.15)" stroke="#ef4444" strokeWidth="2" />
      <text x="175" y="80" fill="#ef4444" fontSize="20" fontWeight="bold" textAnchor="middle">KỊCH BẢN A</text>
      <text x="175" y="120" fill="#ffffff" fontSize="16" textAnchor="middle">Tiêu hết 10 triệu</text>
      <text x="175" y="155" fill="#fca5a5" fontSize="18" fontWeight="bold" textAnchor="middle">Tích sản: 0 ĐỒNG</text>
      <rect x="350" y="40" width="250" height="150" rx="16" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" strokeWidth="2" />
      <text x="475" y="80" fill="#10b981" fontSize="20" fontWeight="bold" textAnchor="middle">KỊCH BẢN B</text>
      <text x="475" y="120" fill="#ffffff" fontSize="16" textAnchor="middle">Trích 50% tích sản</text>
      <text x="475" y="155" fill="#10b981" fontSize="18" fontWeight="bold" textAnchor="middle">Tích sản: 5 TR/THÁNG</text>
    </svg>"""
)

add_scene(
    "S087", "📈", "SỨC MẠNH LÃI KÉP", "#10b981", "#a7f3d0",
    "5 TRIỆU/THÁNG — LỢI NHUẬN KỲ VỌNG 10%/NĂM",
    "Đều đặn tích sản vào chứng chỉ quỹ tăng trưởng dài hạn",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="440" height="150" rx="16" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" strokeWidth="2" />
      <text x="300" y="80" fill="#ffffff" fontSize="20" textAnchor="middle">Vốn tích lũy: 5.000.000 đ / tháng</text>
      <text x="300" y="120" fill="#10b981" fontSize="28" fontWeight="bold" textAnchor="middle">LÃI SUẤT 10% / NĂM</text>
      <text x="300" y="160" fill="#a7f3d0" fontSize="18" textAnchor="middle">Kỳ quan thứ tám của thế giới tài chính</text>
    </svg>"""
)

add_scene(
    "S088", "1️⃣", "CỘT MỐC 1 NĂM", "#10b981", "#a7f3d0",
    "SAU 1 NĂM: KỊCH BẢN B ĐẠT 63 TRIỆU ĐỒNG",
    "Kịch bản A có 0 đồng; Kịch bản B có quỹ an toàn 63 triệu tiền mặt",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="150" y={190 - animProgress * 10} width="120" height={animProgress * 10} rx="10" fill="#ef4444" />
      <text x="210" y="170" fill="#ef4444" fontSize="18" fontWeight="bold" textAnchor="middle">0 ĐỒNG</text>
      <text x="210" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Kịch bản A</text>
      <rect x="380" y={190 - animProgress * 110} width="120" height={animProgress * 110} rx="10" fill="#10b981" />
      <text x="440" y={180 - animProgress * 110} fill="#10b981" fontSize="22" fontWeight="bold" textAnchor="middle">63 TRIỆU</text>
      <text x="440" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Kịch bản B</text>
      <text x="325" y="45" fill="#ffffff" fontSize="18" fontWeight="bold" textAnchor="middle">Đủ chi phí sinh hoạt 6 tháng nếu có biến cố!</text>
    </svg>"""
)

add_scene(
    "S090", "3️⃣", "CỘT MỐC 3 NĂM", "#10b981", "#a7f3d0",
    "SAU 3 NĂM: KỊCH BẢN B TÍCH LŨY 215 TRIỆU ĐỒNG",
    "Kịch bản A vẫn chật vật; Kịch bản B sở hữu khối tài sản vững chãi",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="150" y={190 - animProgress * 10} width="120" height={animProgress * 10} rx="10" fill="#ef4444" />
      <text x="210" y="170" fill="#ef4444" fontSize="18" fontWeight="bold" textAnchor="middle">0 ĐỒNG</text>
      <text x="210" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Kịch bản A</text>
      <rect x="380" y={190 - animProgress * 140} width="120" height={animProgress * 140} rx="10" fill="#10b981" />
      <text x="440" y={180 - animProgress * 140} fill="#10b981" fontSize="24" fontWeight="bold" textAnchor="middle">215 TRIỆU</text>
      <text x="440" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Kịch bản B</text>
      <text x="325" y="35" fill="#f59e0b" fontSize="18" fontWeight="bold" textAnchor="middle">LÃI KÉP BẮT ĐẦU PHÁT HUY SỨC MẠNH</text>
    </svg>"""
)

add_scene(
    "S091", "5️⃣", "CỘT MỐC 5 NĂM", "#10b981", "#a7f3d0",
    "SAU 5 NĂM: KỊCH BẢN B CÁN MỐC 410 TRIỆU ĐỒNG",
    "Tương đương gần nửa tỷ đồng tích lũy tự do tài chính",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="150" y={190 - animProgress * 10} width="120" height={animProgress * 10} rx="10" fill="#ef4444" />
      <text x="210" y="170" fill="#ef4444" fontSize="18" fontWeight="bold" textAnchor="middle">0 ĐỒNG</text>
      <text x="210" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Kịch bản A</text>
      <rect x="380" y={190 - animProgress * 160} width="120" height={animProgress * 160} rx="10" fill="#10b981" />
      <text x="440" y={180 - animProgress * 160} fill="#10b981" fontSize="26" fontWeight="900" textAnchor="middle">410 TRIỆU</text>
      <text x="440" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Kịch bản B</text>
      <text x="325" y="30" fill="#10b981" fontSize="20" fontWeight="bold" textAnchor="middle">GẦN NỬA TỶ ĐỒNG TÀI SẢN RÒNG!</text>
    </svg>"""
)

add_scene(
    "S093", "🔟", "CỘT MỐC 10 NĂM", "#10b981", "#a7f3d0",
    "SAU 10 NĂM: KỊCH BẢN B CHÍNH THỨC VƯỢT 1.1 TỶ ĐỒNG",
    "Sức mạnh lãi kép nhân số vốn 5 triệu/tháng thành một gia tài",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="100" y="40" width="450" height="150" rx="20" fill="rgba(16, 185, 129, 0.2)" stroke="#10b981" strokeWidth="4" />
      <text x="325" y="85" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">KẾT QUẢ SAU 10 NĂM KIÊN TRÌ</text>
      <text x="325" y="140" fill="#10b981" fontSize="44" fontWeight="900" textAnchor="middle">1.100.000.000 đ</text>
      <text x="325" y="175" fill="#a7f3d0" fontSize="16" textAnchor="middle">Chỉ từ 5 triệu đồng tiền lương tăng thêm mỗi tháng</text>
    </svg>"""
)

add_scene(
    "S094", "📊", "ĐỒ THỊ PHÂN KỲ", "#f59e0b", "#fde68a",
    "KHOẢNG CÁCH KHỔNG LỒ GIỮA 0 ĐỒNG VÀ 1.1 TỶ",
    "Cái giá của việc nâng cấp lối sống bừa bãi là cả một gia tài",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <path d={`M 100 180 Q 300 160 550 50`} fill="none" stroke="#10b981" strokeWidth="6" />
      <text x="560" y="55" fill="#10b981" fontSize="18" fontWeight="bold">1.1 TỶ</text>
      <line x1="100" y1="180" x2="550" y2="180" stroke="#ef4444" strokeWidth="4" strokeDasharray="6 6" />
      <text x="560" y="185" fill="#ef4444" fontSize="18" fontWeight="bold">0 ĐỒNG</text>
      <text x="325" y="225" fill="#cbd5e1" fontSize="15" textAnchor="middle">Cùng xuất phát điểm tăng lương, hai kết quả hoàn toàn trái ngược</text>
    </svg>"""
)

add_scene(
    "S096", "🏆", "KẾT LUẬN ĐANH THÉP", "#10b981", "#a7f3d0",
    "TĂNG LƯƠNG KHÔNG LÀM BẠN GIÀU",
    "Giữ lại được bao nhiêu tiền từ khoản tăng đó mới quyết định tương lai",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="490" height="150" rx="18" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" strokeWidth="3" />
      <text x="325" y="85" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">NĂNG LỰC TÀI CHÍNH THỰC SỰ</text>
      <text x="325" y="130" fill="#10b981" fontSize="28" fontWeight="900" textAnchor="middle">KHẢ NĂNG KIỂM SOÁT PHẦN TIỀN TĂNG THÊM</text>
      <text x="325" y="170" fill="#a7f3d0" fontSize="16" textAnchor="middle">Đó là sự khác biệt duy nhất giữa giàu lên và nghèo đi</text>
    </svg>"""
)

# ==================== BEAT 4: TƯƠNG PHẢN ====================
add_scene(
    "S100", "👥", "GÓC NHÌN BÊN NGOÀI", "#38bdf8", "#bae6fd",
    "BẢNG SO SÁNH VẺ BỀ NGOÀI SAU 3 NĂM",
    "Người A trông như doanh nhân thành đạt; Người B trông như nhân viên bình thường",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="50" y="40" width="250" height="150" rx="16" fill="rgba(30, 41, 59, 0.85)" stroke="#38bdf8" strokeWidth="2" />
      <text x="175" y="80" fill="#38bdf8" fontSize="20" fontWeight="bold" textAnchor="middle">NGƯỜI A</text>
      <text x="175" y="115" fill="#ffffff" fontSize="15" textAnchor="middle">Chung cư cao cấp, xe ga</text>
      <text x="175" y="145" fill="#cbd5e1" fontSize="14" textAnchor="middle">Đồ hiệu, ăn nhà hàng sang</text>
      <text x="175" y="175" fill="#38bdf8" fontSize="15" fontWeight="bold" textAnchor="middle">Vẻ ngoài thành đạt</text>
      <rect x="350" y="40" width="250" height="150" rx="16" fill="rgba(30, 41, 59, 0.85)" stroke="#10b981" strokeWidth="2" />
      <text x="475" y="80" fill="#10b981" fontSize="20" fontWeight="bold" textAnchor="middle">NGƯỜI B</text>
      <text x="475" y="115" fill="#ffffff" fontSize="15" textAnchor="middle">Phòng trọ cũ, xe máy số</text>
      <text x="475" y="145" fill="#cbd5e1" fontSize="14" textAnchor="middle">Sơ mi giản dị, cơm nhà</text>
      <text x="475" y="175" fill="#10b981" fontSize="15" fontWeight="bold" textAnchor="middle">Vẻ ngoài bình dị</text>
    </svg>"""
)

add_scene(
    "S102", "📋", "SỰ THẬT TÀI CHÍNH", "#ef4444", "#fca5a5",
    "BẢNG SỐ DƯ THỰC TẾ CỦA NGƯỜI A",
    "Tài khoản còn 6 triệu, nợ thẻ 20 triệu, chậm lương 10 ngày là khủng hoảng",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="30" width="490" height="175" rx="16" fill="rgba(30, 41, 59, 0.9)" stroke="#ef4444" strokeWidth="3" />
      <text x="120" y="70" fill="#cbd5e1" fontSize="18">Số dư khả dụng tài khoản:</text>
      <text x="480" y="70" fill="#ffffff" fontSize="20" fontWeight="bold">6.000.000 đ</text>
      <text x="120" y="110" fill="#cbd5e1" fontSize="18">Dư nợ thẻ tín dụng đến hạn:</text>
      <text x="480" y="110" fill="#ef4444" fontSize="22" fontWeight="bold">-20.000.000 đ</text>
      <text x="120" y="150" fill="#cbd5e1" fontSize="18">Chi phí sinh hoạt cố định:</text>
      <text x="480" y="150" fill="#f59e0b" fontSize="20" fontWeight="bold">19.000.000 đ / tháng</text>
      <text x="325" y="195" fill="#ef4444" fontSize="16" fontWeight="bold" textAnchor="middle">CHẬM LƯƠNG 10 NGÀY = VỠ TRẬN TÀI CHÍNH</text>
    </svg>"""
)

add_scene(
    "S104", "⚖️", "CÁN CÂN TỰ DO", "#10b981", "#a7f3d0",
    "SỐ NGÀY SỐNG SÓT NẾU MẤT VIỆC",
    "Người A có 0 ngày sống sót vs Người B có 24 tháng thảnh thơi tự chủ",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="140" y={190 - animProgress * 15} width="140" height={animProgress * 15} rx="10" fill="#ef4444" />
      <text x="210" y="165" fill="#ef4444" fontSize="18" fontWeight="bold" textAnchor="middle">0 NGÀY</text>
      <text x="210" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Người A</text>
      <rect x="370" y={190 - animProgress * 150} width="140" height={animProgress * 150} rx="10" fill="#10b981" />
      <text x="440" y={180 - animProgress * 150} fill="#10b981" fontSize="24" fontWeight="bold" textAnchor="middle">24 THÁNG</text>
      <text x="440" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Người B (2 năm)</text>
      <text x="325" y="35" fill="#f59e0b" fontSize="18" fontWeight="bold" textAnchor="middle">ĐỆM AN TOÀN QUYẾT ĐỊNH SỰ TỰ DO</text>
    </svg>"""
)

add_scene(
    "S107", "💎", "BẢN CHẤT CỐT LÕI", "#10b981", "#a7f3d0",
    "ẢO GIÁC GIÀU CÓ VS TỰ DO THỰC SỰ",
    "Người A chọn vẻ ngoài giả tạo; người B chọn sự thịnh vượng bền vững",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="220" height="150" rx="16" fill="rgba(239, 68, 68, 0.15)" stroke="#ef4444" strokeWidth="2" />
      <text x="190" y="85" fill="#ef4444" fontSize="18" fontWeight="bold" textAnchor="middle">NGƯỜI A</text>
      <text x="190" y="125" fill="#ffffff" fontSize="15" textAnchor="middle">Nô lệ cho mức sống</text>
      <text x="190" y="160" fill="#fca5a5" fontSize="15" textAnchor="middle">Bất an thường trực</text>
      <rect x="350" y="40" width="220" height="150" rx="16" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" strokeWidth="2" />
      <text x="460" y="85" fill="#10b981" fontSize="18" fontWeight="bold" textAnchor="middle">NGƯỜI B</text>
      <text x="460" y="125" fill="#ffffff" fontSize="15" textAnchor="middle">Làm chủ tài chính</text>
      <text x="460" y="160" fill="#a7f3d0" fontSize="15" textAnchor="middle">Tự do trong tâm trí</text>
    </svg>"""
)

add_scene(
    "S109", "👁️", "NGHỊCH LÝ XÃ HỘI", "#818cf8", "#c7d2fe",
    "NGƯỜI TA KHÔNG NGƯỠNG MỘ CHIẾC XE CỦA BẠN",
    "Họ chỉ đang tưởng tượng bản thân họ ngồi trong chiếc xe đó mà thôi",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="300" cy="100" r="50" fill="rgba(129, 140, 248, 0.2)" stroke="#818cf8" strokeWidth="4" />
      <text x="300" y="115" fill="#ffffff" fontSize="40" textAnchor="middle">🏎️</text>
      <text x="300" y="175" fill="#ffffff" fontSize="18" fontWeight="bold" textAnchor="middle">TÂM LÝ HỌC VỀ TIỀN</text>
      <text x="300" y="210" fill="#c7d2fe" fontSize="15" textAnchor="middle">Không ai ấn tượng với món đồ của bạn nhiều bằng chính bạn</text>
    </svg>"""
)

add_scene(
    "S111", "💰", "ĐỊNH NGHĨA SỰ GIÀU CÓ", "#10b981", "#a7f3d0",
    "GIÀU CÓ LÀ NHỮNG GÌ BẠN GIỮ LẠI ĐƯỢC",
    "Chiếc xe bạn không mua, căn hộ bạn không nâng cấp quá đà chính là tài sản",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="440" height="150" rx="18" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" strokeWidth="3" />
      <text x="300" y="85" fill="#10b981" fontSize="36" textAnchor="middle">💎</text>
      <text x="300" y="130" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">TÀI SẢN THỰC SỰ LÀ TÀI SẢN VÔ HÌNH</text>
      <text x="300" y="165" fill="#a7f3d0" fontSize="16" textAnchor="middle">Nó bảo vệ bạn trước mọi cơn bão của cuộc đời</text>
    </svg>"""
)

add_scene(
    "S113", "📜", "TỔNG KẾT TƯƠNG PHẢN", "#38bdf8", "#bae6fd",
    "BẢNG TÓM TẮT HAI CON ĐƯỜNG",
    "Lối sống hào nhoáng dẫn tới kiệt quệ vs Kỷ luật dẫn tới bình an",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="60" y="30" width="530" height="170" rx="16" fill="rgba(30, 41, 59, 0.9)" stroke="#38bdf8" strokeWidth="2" />
      <text x="180" y="70" fill="#ef4444" fontSize="18" fontWeight="bold" textAnchor="middle">HÀO NHOÁNG</text>
      <text x="470" y="70" fill="#10b981" fontSize="18" fontWeight="bold" textAnchor="middle">KỶ LUẬT THỰC CHIẾN</text>
      <line x1="325" y1="45" x2="325" y2="185" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
      <text x="180" y="110" fill="#cbd5e1" fontSize="15" textAnchor="middle">Nợ thẻ, cạn tiền cuối tháng</text>
      <text x="470" y="110" fill="#cbd5e1" fontSize="15" textAnchor="middle">Dòng tiền tích sản đều đặn</text>
      <text x="180" y="150" fill="#cbd5e1" fontSize="15" textAnchor="middle">Áp lực không dám nghỉ việc</text>
      <text x="470" y="150" fill="#cbd5e1" fontSize="15" textAnchor="middle">Tự chủ, thảnh thơi lựa chọn</text>
    </svg>"""
)

add_scene(
    "S115", "🎯", "CHUYỂN DỊCH CHIẾN LƯỢC", "#10b981", "#a7f3d0",
    "HỆ THỐNG PHÒNG THỦ BA TẦNG THỰC CHIẾN",
    "Từ cạm bẫy tâm lý chuyển dịch sang giải pháp bảo vệ tự động",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="70" width="140" height="80" rx="14" fill="#ef4444" />
      <text x="150" y="115" fill="#ffffff" fontSize="16" fontWeight="bold" textAnchor="middle">BẪY TÂM LÝ</text>
      <path d="M 240 110 L 390 110" stroke="#10b981" strokeWidth="6" strokeDasharray="8 8" />
      <text x="315" y="95" fill="#10b981" fontSize="20" fontWeight="bold" textAnchor="middle">CHUYỂN DỊCH</text>
      <rect x="410" y="70" width="160" height="80" rx="14" fill="#10b981" />
      <text x="490" y="115" fill="#ffffff" fontSize="16" fontWeight="bold" textAnchor="middle">3 TẦNG BẢO VỆ</text>
      <text x="325" y="210" fill="#cbd5e1" fontSize="15" textAnchor="middle">Không sống kham khổ cực đoan, mà quản trị bằng hệ thống</text>
    </svg>"""
)

# ==================== BEAT 5: LỘ TRÌNH 3 TẦNG PHÒNG THỦ THỰC CHIẾN ====================
add_scene(
    "S117", "1️⃣", "TẦNG PHÒNG THỦ SỐ 1", "#38bdf8", "#bae6fd",
    "QUY TẮC ĐÓNG BĂNG LỐI SỐNG SÁU THÁNG",
    "Lệnh giới nghiêm chi tiêu trong đúng 180 ngày kể từ khi có quyết định tăng lương",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="300" cy="95" r="50" fill="rgba(56, 189, 248, 0.2)" stroke="#38bdf8" strokeWidth="4" />
      <text x="300" y="110" fill="#38bdf8" fontSize="40" textAnchor="middle">🧊</text>
      <text x="300" y="175" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">ĐÓNG BĂNG 180 NGÀY</text>
      <text x="300" y="210" fill="#bae6fd" fontSize="16" textAnchor="middle">Giữ nguyên mức sống cũ để cơ thể làm quen với khoản dư</text>
    </svg>"""
)

add_scene(
    "S119", "🚫", "3 ĐIỀU CẤM KỶ LUẬT", "#ef4444", "#fca5a5",
    "BIỂN BÁO BA ĐIỀU CẤM TRONG 6 THÁNG ĐẦU",
    "1. Cấm chuyển nhà | 2. Cấm đổi xe | 3. Cấm mua đồ công nghệ xa xỉ",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="25" width="490" height="185" rx="16" fill="rgba(239, 68, 68, 0.15)" stroke="#ef4444" strokeWidth="3" />
      <text x="120" y="70" fill="#ffffff" fontSize="18" fontWeight="bold">❌ ĐIỀU 1: CẤM CHUYỂN CHỖ Ở</text>
      <text x="120" y="115" fill="#ffffff" fontSize="18" fontWeight="bold">❌ ĐIỀU 2: CẤM ĐỔI XE MỚI</text>
      <text x="120" y="160" fill="#ffffff" fontSize="18" fontWeight="bold">❌ ĐIỀU 3: CẤM MUA ĐỒ CÔNG NGHỆ ĐẮT TIỀN</text>
      <text x="325" y="225" fill="#cbd5e1" fontSize="15" textAnchor="middle">Tránh những quyết định tài chính bốc đồng không thể đảo ngược</text>
    </svg>"""
)

add_scene(
    "S121", "🧠", "LỢI ÍCH TÂM LÝ HỌC", "#818cf8", "#c7d2fe",
    "LÀM NGUỘI CƠN HƯNG PHẤN TĂNG LƯƠNG",
    "6 tháng giúp bộ não lấy lại sự tỉnh táo trước khi ra quyết định chi tiêu lớn",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="100" y="40" width="400" height="150" rx="16" fill="rgba(129, 140, 248, 0.15)" stroke="#818cf8" strokeWidth="3" />
      <text x="300" y="85" fill="#818cf8" fontSize="36" textAnchor="middle">🌡️</text>
      <text x="300" y="130" fill="#ffffff" fontSize="20" fontWeight="bold" textAnchor="middle">HẠ NHIỆT CẢM XÚC BỐC ĐỒNG</text>
      <text x="300" y="165" fill="#c7d2fe" fontSize="16" textAnchor="middle">Để lý trí làm việc thay cho cảm xúc nhất thời</text>
    </svg>"""
)

add_scene(
    "S122", "💰", "KẾT QUẢ ĐÓNG BĂNG", "#10b981", "#a7f3d0",
    "GOM ĐƯỢC 60 TRIỆU ĐỒNG VỐN AN TOÀN",
    "6 tháng nhân 10 triệu lương tăng bằng 60 triệu quỹ dự phòng nguyên vẹn",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="440" height="150" rx="20" fill="rgba(16, 185, 129, 0.2)" stroke="#10b981" strokeWidth="4" />
      <text x="300" y="85" fill="#ffffff" fontSize="20" fontWeight="bold" textAnchor="middle">6 THÁNG x 10.000.000 đ =</text>
      <text x="300" y="140" fill="#10b981" fontSize="46" fontWeight="900" textAnchor="middle">60.000.000 đ</text>
      <text x="300" y="175" fill="#a7f3d0" fontSize="16" textAnchor="middle">Quỹ an toàn được tích lũy nhẹ nhàng mà không cần gồng gánh</text>
    </svg>"""
)

add_scene(
    "S124", "🚀", "BƯỚC CHẠY ĐÀ", "#38bdf8", "#bae6fd",
    "ĐÓNG BĂNG LỐI SỐNG LÀ TẠO KHOẢNG ĐỆM BỨT PHÁ",
    "Không phải kìm hãm cuộc sống, mà là thiết lập thế chủ động trước đồng tiền",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <path d={`M 100 170 Q 300 170 500 50`} fill="none" stroke="#38bdf8" strokeWidth="6" strokeLinecap="round" />
      <circle cx="500" cy="50" r="10" fill="#38bdf8" />
      <text x="300" y="130" fill="#ffffff" fontSize="20" fontWeight="bold" textAnchor="middle">KHOẢNG ĐỆM 6 THÁNG</text>
      <text x="300" y="215" fill="#cbd5e1" fontSize="16" textAnchor="middle">Lấy đà vững chắc trước khi bước sang giai đoạn phân bổ</text>
    </svg>"""
)

add_scene(
    "S126", "🌉", "CẦU NỐI CHUYỂN TIẾP", "#f59e0b", "#fde68a",
    "TỪ ĐÓNG BĂNG BƯỚC SANG CÔNG THỨC 50/50",
    "Hết 6 tháng, bạn hoàn toàn được nâng cấp mức sống theo tỷ lệ vàng",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="70" width="180" height="80" rx="14" fill="#38bdf8" />
      <text x="170" y="115" fill="#ffffff" fontSize="16" fontWeight="bold" textAnchor="middle">6 THÁNG ĐÓNG BĂNG</text>
      <text x="300" y="120" fill="#ffffff" fontSize="28">➔</text>
      <rect x="340" y="70" width="180" height="80" rx="14" fill="#10b981" />
      <text x="430" y="115" fill="#ffffff" fontSize="16" fontWeight="bold" textAnchor="middle">TỶ LỆ VÀNG 50/50</text>
      <text x="300" y="210" fill="#cbd5e1" fontSize="15" textAnchor="middle">Nâng cấp mức sống có kế hoạch và bền vững</text>
    </svg>"""
)

add_scene(
    "S127", "2️⃣", "TẦNG PHÒNG THỦ SỐ 2", "#10b981", "#a7f3d0",
    "QUY TẮC CHIA ĐÔI PHẦN LƯƠNG TĂNG 50/50",
    "Bắt buộc chia đôi 10 triệu lương tăng thành hai phần hoàn toàn bằng nhau",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="100" y="40" width="450" height="150" rx="18" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" strokeWidth="3" />
      <text x="325" y="85" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">10 TRIỆU LƯƠNG TĂNG THÊM</text>
      <text x="210" y="145" fill="#10b981" fontSize="24" fontWeight="bold" textAnchor="middle">50% TÍCH SẢN</text>
      <line x1="325" y1="105" x2="325" y2="175" stroke="#ffffff" strokeWidth="2" />
      <text x="440" y="145" fill="#38bdf8" fontSize="24" fontWeight="bold" textAnchor="middle">50% NÂNG CẤP</text>
    </svg>"""
)

add_scene(
    "S128", "🔀", "SƠ ĐỒ PHÂN LUỒNG", "#38bdf8", "#bae6fd",
    "PHÂN LUỒNG 10 TRIỆU LƯƠNG TĂNG THÊM",
    "5 triệu (50%) vào Quỹ tích sản — 5 triệu (50%) nâng cấp có chủ đích",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="325" cy="50" r="35" fill="#ffffff" />
      <text x="325" y="55" fill="#0f172a" fontSize="14" fontWeight="bold" textAnchor="middle">+10 TR</text>
      <path d="M 300 80 L 180 140" stroke="#10b981" strokeWidth="4" />
      <rect x="90" y="140" width="180" height="70" rx="12" fill="#10b981" />
      <text x="180" y="170" fill="#ffffff" fontSize="16" fontWeight="bold" textAnchor="middle">5 TRIỆU (50%)</text>
      <text x="180" y="195" fill="#ffffff" fontSize="13" textAnchor="middle">Quỹ tích sản</text>
      <path d="M 350 80 L 470 140" stroke="#38bdf8" strokeWidth="4" />
      <rect x="380" y="140" width="180" height="70" rx="12" fill="#38bdf8" />
      <text x="470" y="170" fill="#ffffff" fontSize="16" fontWeight="bold" textAnchor="middle">5 TRIỆU (50%)</text>
      <text x="470" y="195" fill="#ffffff" fontSize="13" textAnchor="middle">Nâng cấp cuộc sống</text>
    </svg>"""
)

add_scene(
    "S129", "📥", "NHÁNH SỐ 1: TỰ ĐỘNG HÓA", "#10b981", "#a7f3d0",
    "5 TRIỆU TỰ ĐỘNG CHUYỂN VÀO TÀI KHOẢN TÍCH SẢN",
    "Cài đặt lệnh trích tiền tự động lúc 8h sáng ngày nhận lương",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="440" height="150" rx="18" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" strokeWidth="3" />
      <text x="300" y="85" fill="#10b981" fontSize="36" textAnchor="middle">⏰</text>
      <text x="300" y="130" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">8:00 SÁNG NGÀY CÓ LƯƠNG</text>
      <text x="300" y="165" fill="#a7f3d0" fontSize="16" textAnchor="middle">Chuyển thẳng 5 triệu trước khi bạn kịp nhìn thấy</text>
    </svg>"""
)

add_scene(
    "S131", "🏛️", "TRẢ CHO MÌNH TRƯỚC", "#f59e0b", "#fde68a",
    "COI 5 TRIỆU TÍCH SẢN NHƯ MỘT KHOẢN THUẾ BẮT BUỘC",
    "Khoản tiền chưa từng tồn tại trong ví, phần còn lại mới dùng để sống",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="300" cy="95" r="50" fill="rgba(245, 158, 11, 0.2)" stroke="#f59e0b" strokeWidth="4" />
      <text x="300" y="110" fill="#f59e0b" fontSize="40" textAnchor="middle">🛡️</text>
      <text x="300" y="175" fill="#ffffff" fontSize="20" fontWeight="bold" textAnchor="middle">TRẢ CHO BẢN THÂN MÌNH TRƯỚC</text>
      <text x="300" y="210" fill="#fde68a" fontSize="16" textAnchor="middle">Nguyên tắc vàng bất biến của giới tài chính tinh hoa</text>
    </svg>"""
)

add_scene(
    "S132", "🎁", "NHÁNH SỐ 2: TẬN HƯỞNG", "#38bdf8", "#bae6fd",
    "5 TRIỆU CÒN LẠI DÙNG ĐỂ NÂNG CẤP CUỘC SỐNG",
    "Được phép chi tiêu thoải mái không cần áy náy hay lo âu",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="440" height="150" rx="18" fill="rgba(56, 189, 248, 0.15)" stroke="#38bdf8" strokeWidth="3" />
      <text x="300" y="85" fill="#38bdf8" fontSize="36" textAnchor="middle">✨</text>
      <text x="300" y="130" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">5.000.000 đ NÂNG CẤP THỰC SỰ</text>
      <text x="300" y="165" fill="#bae6fd" fontSize="16" textAnchor="middle">Ăn ngon hơn, học khóa mới, phụng dưỡng cha mẹ</text>
    </svg>"""
)

add_scene(
    "S134", "⚖️", "CÂN BẰNG TÂM LÝ", "#10b981", "#a7f3d0",
    "VỪA CÓ ĐỘNG LỰC — VỪA GIÀU CÓ TƯƠNG LAI",
    "Không bị ức chế tâm lý cực đoan, tài sản tương lai vẫn sinh sôi mạnh mẽ",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="440" height="150" rx="18" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" strokeWidth="3" />
      <text x="300" y="85" fill="#10b981" fontSize="36" textAnchor="middle">🎯</text>
      <text x="300" y="130" fill="#ffffff" fontSize="20" fontWeight="bold" textAnchor="middle">HẠNH PHÚC HIỆN TẠI & BỀN VỮNG TƯƠNG LAI</text>
      <text x="300" y="165" fill="#a7f3d0" fontSize="16" textAnchor="middle">Chi tiêu có chủ đích, tự hào và không bao giờ hối hận</text>
    </svg>"""
)

add_scene(
    "S136", "📈", "LŨY KẾ 3 NĂM", "#10b981", "#a7f3d0",
    "LŨY KẾ 3 NĂM ÁP DỤNG QUY TẮC 50/50",
    "Vừa sống thoải mái hơn 25%, vừa tích lũy được hơn 200 triệu đồng",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="60" y="40" width="240" height="150" rx="16" fill="rgba(56, 189, 248, 0.15)" stroke="#38bdf8" strokeWidth="2" />
      <text x="180" y="80" fill="#38bdf8" fontSize="18" fontWeight="bold" textAnchor="middle">MỨC SỐNG TĂNG</text>
      <text x="180" y="130" fill="#ffffff" fontSize="32" fontWeight="900" textAnchor="middle">+25%</text>
      <text x="180" y="165" fill="#bae6fd" fontSize="14" textAnchor="middle">Tận hưởng trọn vẹn</text>
      <rect x="350" y="40" width="240" height="150" rx="16" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" strokeWidth="2" />
      <text x="470" y="80" fill="#10b981" fontSize="18" fontWeight="bold" textAnchor="middle">TÍCH SẢN TĂNG</text>
      <text x="470" y="130" fill="#10b981" fontSize="32" fontWeight="900" textAnchor="middle">&gt;200 TR</text>
      <text x="470" y="165" fill="#a7f3d0" fontSize="14" textAnchor="middle">An tâm vững chãi</text>
    </svg>"""
)

add_scene(
    "S138", "⚡", "TỐC ĐỘ TỰ DO", "#f59e0b", "#fde68a",
    "MỖI LẦN TĂNG LƯƠNG — TĂNG GẤP ĐÔI TỐC ĐỘ TỰ DO",
    "Cứ mỗi nấc thang thu nhập mới, tốc độ tích sản sẽ tăng theo cấp số nhân",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="440" height="150" rx="18" fill="rgba(245, 158, 11, 0.15)" stroke="#f59e0b" strokeWidth="3" />
      <text x="300" y="85" fill="#f59e0b" fontSize="36" textAnchor="middle">⚡</text>
      <text x="300" y="130" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">BỨT PHÁ TÀI SẢN THEO CẤP SỐ NHÂN</text>
      <text x="300" y="165" fill="#fde68a" fontSize="16" textAnchor="middle">Thay vì để tiền tăng thêm trôi tuột vào chi phí sinh hoạt</text>
    </svg>"""
)

add_scene(
    "S139", "3️⃣", "TẦNG PHÒNG THỦ SỐ 3", "#818cf8", "#c7d2fe",
    "HỆ THỐNG 3 TÀI KHOẢN SỐ & BỘ LỌC 72 GIỜ",
    "Phân luồng dòng tiền tự động trên ứng dụng điện thoại",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="60" y="60" width="150" height="110" rx="14" fill="#38bdf8" />
      <text x="135" y="110" fill="#ffffff" fontSize="16" fontWeight="bold" textAnchor="middle">1. SỐNG</text>
      <text x="135" y="140" fill="#ffffff" fontSize="13" textAnchor="middle">Cơ bản: 10tr</text>
      <rect x="250" y="60" width="150" height="110" rx="14" fill="#10b981" />
      <text x="325" y="110" fill="#ffffff" fontSize="16" fontWeight="bold" textAnchor="middle">2. KÉT SẮT</text>
      <text x="325" y="140" fill="#ffffff" fontSize="13" textAnchor="middle">Tích sản: 5tr</text>
      <rect x="440" y="60" width="150" height="110" rx="14" fill="#f59e0b" />
      <text x="515" y="110" fill="#ffffff" fontSize="16" fontWeight="bold" textAnchor="middle">3. HƯỞNG</text>
      <text x="515" y="140" fill="#ffffff" fontSize="13" textAnchor="middle">Trải nghiệm: 5tr</text>
      <text x="325" y="215" fill="#cbd5e1" fontSize="15" textAnchor="middle">Không để chung tiền trong một tài khoản duy nhất</text>
    </svg>"""
)

add_scene(
    "S140", "📱", "MÔ HÌNH 3 TÀI KHOẢN SỐ", "#38bdf8", "#bae6fd",
    "CẤU TRÚC 3 TÀI KHOẢN NGÂN HÀNG SỐ ĐỘC LẬP",
    "Tài khoản 1 sinh hoạt | Tài khoản 2 tích sản | Tài khoản 3 trải nghiệm",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="50" y="40" width="170" height="140" rx="14" fill="rgba(56, 189, 248, 0.2)" stroke="#38bdf8" strokeWidth="2" />
      <text x="135" y="80" fill="#38bdf8" fontSize="18" fontWeight="bold" textAnchor="middle">TK SINH HOẠT</text>
      <text x="135" y="120" fill="#ffffff" fontSize="20" fontWeight="bold" textAnchor="middle">10.000.000 đ</text>
      <text x="135" y="155" fill="#cbd5e1" fontSize="13" textAnchor="middle">Nhà, ăn, hóa đơn</text>
      <rect x="240" y="40" width="170" height="140" rx="14" fill="rgba(16, 185, 129, 0.2)" stroke="#10b981" strokeWidth="2" />
      <text x="325" y="80" fill="#10b981" fontSize="18" fontWeight="bold" textAnchor="middle">KÉT TÍCH SẢN</text>
      <text x="325" y="120" fill="#ffffff" fontSize="20" fontWeight="bold" textAnchor="middle">5.000.000 đ</text>
      <text x="325" y="155" fill="#cbd5e1" fontSize="13" textAnchor="middle">Bất khả xâm phạm</text>
      <rect x="430" y="40" width="170" height="140" rx="14" fill="rgba(245, 158, 11, 0.2)" stroke="#f59e0b" strokeWidth="2" />
      <text x="515" y="80" fill="#f59e0b" fontSize="18" fontWeight="bold" textAnchor="middle">TK TRẢI NGHIỆM</text>
      <text x="515" y="120" fill="#ffffff" fontSize="20" fontWeight="bold" textAnchor="middle">5.000.000 đ</text>
      <text x="515" y="155" fill="#cbd5e1" fontSize="13" textAnchor="middle">Tiêu hết là dừng</text>
    </svg>"""
)

add_scene(
    "S141", "🏠", "TÀI KHOẢN SỐ 1", "#38bdf8", "#bae6fd",
    "TÀI KHOẢN SINH HOẠT CƠ BẢN: 10 TRIỆU",
    "Nhận lương và giữ nguyên 10 triệu cho toàn bộ chi phí thiết yếu",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="440" height="150" rx="18" fill="rgba(56, 189, 248, 0.15)" stroke="#38bdf8" strokeWidth="3" />
      <text x="300" y="85" fill="#38bdf8" fontSize="22" fontWeight="bold" textAnchor="middle">TÀI KHOẢN 1: SINH HOẠT CĂN BẢN</text>
      <text x="300" y="135" fill="#ffffff" fontSize="36" fontWeight="900" textAnchor="middle">10.000.000 đ</text>
      <text x="300" y="170" fill="#bae6fd" fontSize="16" textAnchor="middle">Tiền nhà, ăn uống, hóa đơn điện nước thiết yếu</text>
    </svg>"""
)

add_scene(
    "S142", "🔒", "TÀI KHOẢN SỐ 2", "#10b981", "#a7f3d0",
    "KÉT SẮT TÍCH SẢN: 5 TRIỆU BẤT KHẢ XÂM PHẠM",
    "Tiền chỉ có một chiều đi vào, tuyệt đối không gắn thẻ rút tiền",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="440" height="150" rx="18" fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" strokeWidth="3" />
      <text x="300" y="85" fill="#10b981" fontSize="22" fontWeight="bold" textAnchor="middle">TÀI KHOẢN 2: KÉT SẮT TÍCH SẢN</text>
      <text x="300" y="135" fill="#10b981" fontSize="36" fontWeight="900" textAnchor="middle">5.000.000 đ (MỘT CHIỀU VÀO)</text>
      <text x="300" y="170" fill="#a7f3d0" fontSize="16" textAnchor="middle">Không gắn thẻ rút tiền, không cài app chuyển tiền trên máy</text>
    </svg>"""
)

add_scene(
    "S143", "🎉", "TÀI KHOẢN SỐ 3", "#f59e0b", "#fde68a",
    "TÀI KHOẢN TRẢI NGHIỆM: 5 TRIỆU CÓ HẠN MỨC",
    "Tiêu trọn cho sở thích cá nhân, tiêu hết là dừng, cấm bù trừ",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="440" height="150" rx="18" fill="rgba(245, 158, 11, 0.15)" stroke="#f59e0b" strokeWidth="3" />
      <text x="300" y="85" fill="#f59e0b" fontSize="22" fontWeight="bold" textAnchor="middle">TÀI KHOẢN 3: TRẢI NGHIỆM TỰ DO</text>
      <text x="300" y="135" fill="#ffffff" fontSize="36" fontWeight="900" textAnchor="middle">5.000.000 đ / THÁNG</text>
      <text x="300" y="170" fill="#fde68a" fontSize="16" textAnchor="middle">Tiêu hết là dừng lại, không được phép bù trừ từ tài khoản khác</text>
    </svg>"""
)

add_scene(
    "S145", "⏳", "BỘ LỌC 72 GIỜ", "#818cf8", "#c7d2fe",
    "QUY TẮC ĐỢI ĐỦ 72 GIỜ TRƯỚC KHI MUA ĐỒ",
    "80% ham muốn mua sắm bốc đồng sẽ tự động biến mất sau 3 ngày",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="300" cy="95" r="50" fill="rgba(129, 140, 248, 0.2)" stroke="#818cf8" strokeWidth="4" />
      <text x="300" y="110" fill="#818cf8" fontSize="36" textAnchor="middle">⏰</text>
      <text x="300" y="175" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">BỘ LỌC 72 GIỜ</text>
      <text x="300" y="210" fill="#c7d2fe" fontSize="16" textAnchor="middle">80% CƠN SỐT MUA SẮM SẼ TỰ ĐỘNG HẠ NHIỆT</text>
    </svg>"""
)

add_scene(
    "S147", "⏱️", "QUY ĐỔI GIÁ TRỊ", "#f59e0b", "#fde68a",
    "QUY ĐỔI GIÁ TIỀN RA GIỜ LAO ĐỘNG",
    "Lương 100k/giờ -> Chiếc đồng hồ 6 triệu tương đương 60 giờ làm việc",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="80" y="40" width="490" height="140" rx="16" fill="rgba(30, 41, 59, 0.85)" stroke="#f59e0b" strokeWidth="2" />
      <text x="325" y="80" fill="#cbd5e1" fontSize="18" textAnchor="middle">Thu nhập: 100.000 đ / giờ làm việc</text>
      <text x="325" y="125" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">ĐỒNG HỒ 6 TRIỆU = 60 GIỜ LÀM VIỆC VẤT VẢ</text>
      <text x="325" y="160" fill="#fde68a" fontSize="18" fontWeight="bold" textAnchor="middle">LIỆU MÓN ĐỒ CÓ ĐÁNG GIÁ NỬA THÁNG LÀM VIỆC?</text>
    </svg>"""
)

add_scene(
    "S149", "🏰", "BỨC TƯỜNG THÀNH", "#10b981", "#a7f3d0",
    "BA TẦNG PHÒNG THỦ VỮNG CHẮC",
    "Bảo vệ bạn trọn đời trước mọi cám dỗ của lạm phát lối sống",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="60" y="70" width="160" height="80" rx="14" fill="#38bdf8" />
      <text x="140" y="105" fill="#ffffff" fontSize="15" fontWeight="bold" textAnchor="middle">TẦNG 1</text>
      <text x="140" y="130" fill="#ffffff" fontSize="13" textAnchor="middle">Đóng băng 6 tháng</text>
      <rect x="245" y="70" width="160" height="80" rx="14" fill="#10b981" />
      <text x="325" y="105" fill="#ffffff" fontSize="15" fontWeight="bold" textAnchor="middle">TẦNG 2</text>
      <text x="325" y="130" fill="#ffffff" fontSize="13" textAnchor="middle">Tỷ lệ vàng 50/50</text>
      <rect x="430" y="70" width="160" height="80" rx="14" fill="#818cf8" />
      <text x="510" y="105" fill="#ffffff" fontSize="15" fontWeight="bold" textAnchor="middle">TẦNG 3</text>
      <text x="510" y="130" fill="#ffffff" fontSize="13" textAnchor="middle">3 Tài khoản số</text>
      <text x="325" y="210" fill="#cbd5e1" fontSize="15" textAnchor="middle">Hệ thống bảo vệ tài chính tự động hoàn chỉnh</text>
    </svg>"""
)

# ==================== BEAT 6: KẾT BÌNH YÊN ====================
add_scene(
    "S150", "🌳", "CÂY TÀI SẢN", "#10b981", "#a7f3d0",
    "CÂY TÀI SẢN TỎA BÓNG BÌNH AN",
    "Tài chính không phải là cuộc đua tiêu xài mà là hành trình xây dựng sự bình yên",
    """<svg viewBox="0 0 600 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="300" cy="90" r="55" fill="rgba(16, 185, 129, 0.3)" stroke="#10b981" strokeWidth="4" />
      <text x="300" y="105" fill="#10b981" fontSize="45" textAnchor="middle">🌳</text>
      <text x="300" y="175" fill="#ffffff" fontSize="22" fontWeight="bold" textAnchor="middle">TÍCH SẢN CHO SỰ AN NHIÊN</text>
      <text x="300" y="210" fill="#a7f3d0" fontSize="16" textAnchor="middle">Không còn giật mình thon thót mỗi khi nhận thông báo số dư</text>
    </svg>"""
)

add_scene(
    "S152", "🕊️", "TỰ DO ĐÍCH THỰC", "#38bdf8", "#bae6fd",
    "SƠ ĐỒ TỰ DO TÀI CHÍNH BỀN VỮNG",
    "Kiếm tiền thông minh -> Giữ tiền kỷ luật -> Tự do lựa chọn cuộc sống",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="50" y="70" width="160" height="70" rx="12" fill="#38bdf8" />
      <text x="130" y="110" fill="#ffffff" fontSize="15" fontWeight="bold" textAnchor="middle">KIẾM THÔNG MINH</text>
      <text x="235" y="115" fill="#ffffff" fontSize="24">➔</text>
      <rect x="255" y="70" width="150" height="70" rx="12" fill="#10b981" />
      <text x="330" y="110" fill="#ffffff" fontSize="15" fontWeight="bold" textAnchor="middle">GIỮ KỶ LUẬT</text>
      <text x="430" y="115" fill="#ffffff" fontSize="24">➔</text>
      <rect x="450" y="70" width="150" height="70" rx="12" fill="#f59e0b" />
      <text x="525" y="110" fill="#ffffff" fontSize="15" fontWeight="bold" textAnchor="middle">TỰ DO TỰ CHỦ</text>
      <text x="325" y="200" fill="#cbd5e1" fontSize="16" textAnchor="middle">Quyền được nói không với những điều mình không muốn</text>
    </svg>"""
)

add_scene(
    "S153", "✨", "CHÂM NGÔN KHẮC GHI", "#f59e0b", "#fde68a",
    "TÀI SẢN LỚN NHẤT LÀ SỰ TỰ DO TRONG TÂM TRÍ",
    "Hãy để mỗi đồng tiền tăng thêm trở thành viên gạch xây dựng tự do",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <rect x="70" y="35" width="510" height="150" rx="20" fill="rgba(245, 158, 11, 0.15)" stroke="#f59e0b" strokeWidth="3" />
      <text x="325" y="80" fill="#fde68a" fontSize="20" fontWeight="bold" textAnchor="middle">"TÀI SẢN LỚN NHẤT CỦA MỘT CON NGƯỜI"</text>
      <text x="325" y="125" fill="#ffffff" fontSize="26" fontWeight="900" textAnchor="middle">KHÔNG PHẢI LÀ ĐỒ HIỆU XA XỈ</text>
      <text x="325" y="160" fill="#10b981" fontSize="22" fontWeight="bold" textAnchor="middle">MÀ LÀ SỰ TỰ DO VÀ BÌNH AN TRONG TÂM TRÍ</text>
    </svg>"""
)

add_scene(
    "S156", "🛡️", "KÊNH TIỀN THỰC CHIẾN", "#10b981", "#a7f3d0",
    "ĐỒNG HÀNH CÙNG TIỀN THỰC CHIẾN",
    "Kiến thức thực chiến — Hành động mỗi ngày — Bình an tài chính",
    """<svg viewBox="0 0 650 240" style={{ width: "100%", height: "100%" }}>
      <circle cx="325" cy="80" r="45" fill="rgba(16, 185, 129, 0.2)" stroke="#10b981" strokeWidth="4" />
      <text x="325" y="90" fill="#10b981" fontSize="32" fontWeight="900" textAnchor="middle">TTC</text>
      <text x="325" y="155" fill="#ffffff" fontSize="24" fontWeight="900" textAnchor="middle">KÊNH TIỀN THỰC CHIẾN</text>
      <text x="325" y="195" fill="#a7f3d0" fontSize="16" textAnchor="middle">Kiến thức thực chiến • Hành động mỗi ngày • Bình an tài chính</text>
    </svg>"""
)

code_parts.append("""
  // Default fallback if unknown scene
  return (
    <div style={containerStyle}>
      <div style={{ ...cardStyle, transform: `scale(${scale}) translateY(${translateY}px)`, opacity, maxWidth: 900 }}>
        <div style={tagStyle("#38bdf8", "#bae6fd")}>TIỀN THỰC CHIẾN</div>
        <div style={headingStyle}>{cleanTitle}</div>
      </div>
    </div>
  );
};

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
  fontSize: 38,
  fontWeight: 900,
  color: "#ffffff",
  lineHeight: 1.3,
  letterSpacing: "-0.01em",
  marginBottom: 12,
  textAlign: "center",
  fontFamily: theme.typography.fontFamily,
};

const subheadStyle: React.CSSProperties = {
  fontSize: 19,
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
  padding: "40px 50px",
  borderRadius: 32,
  backgroundColor: "rgba(15, 23, 42, 0.85)",
  border: "1px solid rgba(255, 255, 255, 0.15)",
  boxShadow: "0 25px 60px rgba(0, 0, 0, 0.6)",
  backdropFilter: "blur(20px)",
  width: "100%",
};

""")

output_file.write_text("".join(code_parts), encoding="utf-8")
print(f"Generated {output_file} successfully!")
