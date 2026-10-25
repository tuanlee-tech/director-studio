#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
motion-stack.py — Video Director 20/20 Code-Driven Motion & Video Rendering Stack Info
In ra danh sách chi tiết 20/20 công nghệ và vai trò của từng công cụ.
"""

import sys

# Windows UTF-8 console output fix
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

STACK_DATA = [
    {
        "group": "I. 3 SKILL DẠY AI CÁCH DỰNG VIDEO",
        "items": [
            ("1. Remotion Skill", "React", "Dựng video bằng code ReactJS, điều khiển frame-by-frame, spring physics"),
            ("2. Motion AI Kit", "React/JS", "Micro-animations, layout transitions, variants khai báo declarative"),
            ("3. GSAP Skill", "JS/TS", "Timeline animation đa tầng, staggered text và micro-timing mili-giây")
        ]
    },
    {
        "group": "II. THIẾT KẾ VỚI SVG & JSX",
        "items": [
            ("4. SVGO", "Node/CLI", "Tối ưu, dọn dẹp và nén vector path cho các biểu tượng tài chính"),
            ("5. Satori", "Vercel", "Biến HTML/JSX TailwindCSS thành vector SVG sắc nét ở mọi độ phân giải")
        ]
    },
    {
        "group": "III. 5 THƯ VIỆN HOẠT ẢNH CHUYÊN BIỆT",
        "items": [
            ("6. GSAP", "Animation", "Timeline animation mạnh mẽ, chuỗi chuyển động phức tạp mượt mà"),
            ("7. Anime.js", "Animation", "Animation JS nhẹ, cực mạnh về stroke drawing & morphing SVG"),
            ("8. Motion", "Animation", "Animation cho ReactJS & JS, xử lý state transitions và gesture"),
            ("9. Rive", "Interactive", "Hoạt hình tương tác có State Machine (đổi biểu cảm nhân vật theo beat)"),
            ("10. Lottie", "Player", "Phát animation JSON xuất từ Adobe After Effects (confetti, sticker)")
        ]
    },
    {
        "group": "IV. DỰNG 2D (CODE SANG KHUNG HÌNH)",
        "items": [
            ("11. Remotion", "Framework", "Khung sườn chính biến code ReactJS thành từng khung hình, xuất MP4"),
            ("12. Motion Canvas", "Procedural", "Lập trình animation bằng TypeScript, chuyên trị video giải thích/toán học")
        ]
    },
    {
        "group": "V. DỰNG 3D (KHỐI, ÁNH SÁNG, VẬT LÝ, HIỆU ỨNG)",
        "items": [
            ("13. Three.js", "WebGL", "Đồ họa 3D không gian, vật thể và ánh sáng ngay trên nền web"),
            ("14. React Three Fiber", "React/3D", "Viết Three.js theo cú pháp component React khai báo"),
            ("15. Drei", "R3F Helper", "Bộ helper dựng sẵn: Text3D, Environment lighting, Float controls"),
            ("16. Rapier", "Physics 3D", "Vật lý thời gian thực: tiền rơi, va chạm nảy tưng bừng, thẻ vỡ vụn"),
            ("17. Postprocessing", "Cinematic", "Hiệu ứng Bloom neon phát sáng, Depth of Field xóa phông điện ảnh")
        ]
    },
    {
        "group": "VI. ÂM THANH VÀ XUẤT VIDEO HOÀN CHỈNH",
        "items": [
            ("18. Howler.js", "Audio Engine", "Điều khiển BGM ducking (hạ nhạc nền khi đọc) và SFX đồng bộ frame"),
            ("19. Mediabunny", "Encoder", "Encode video siêu tốc chạy trên WebCodecs/WASM"),
            ("20. FFmpeg", "Final Muxer", "Ghép nối video, audio VieNeu-TTS, subtitle karaoke và xuất final MP4")
        ]
    }
]

def main():
    print("=" * 78)
    print("🎬 HỆ THỐNG 20/20 CODE-DRIVEN MOTION & VIDEO RENDERING STACK")
    print("   Quy trình Audio-First + Remotion + Motion Graphics (0 AI Credit)")
    print("=" * 78)
    
    total_count = 0
    for group in STACK_DATA:
        print(f"\n📂 {group['group']}")
        print("-" * 78)
        for name, tech_type, desc in group["items"]:
            total_count += 1
            print(f"  {name:<24} [{tech_type:<10}] : {desc}")
    
    print("\n" + "=" * 78)
    print(f"✅ ĐÃ TÍCH HỢP ĐỦ {total_count}/20 CÔNG CỤ HOẠT ẢNH & VIDEO RENDERING")
    print("=" * 78)

if __name__ == "__main__":
    main()
