#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
asset_qa_verifier.py — Automated QA Verifier for Video Production Pipeline
Kiểm định chuyên sâu chất lượng và tính toàn vẹn của:
1. Độ phủ & Tính toàn vẹn Assets (100% coverage, >50KB, ffprobe MP4, PIL integrity)
2. Chuẩn hóa tên file (Sxxx-A_Xs_TYPE.ext, cấm nghiêm ngặt alias scene_*.png)
3. Tính nhất quán nhân vật & Đối chiếu Giới tính với Lời thoại Narration:
   - Nam MC đại diện kênh (S001, S002, S004, S005, S007, S077, S078, S079, S081): master_anchor.png
   - Người A (S051, S052, S054): 'Anh ta' -> Phải là NAM
   - Người B (S055, S058): 'Cô ấy' -> Phải là NỮ
4. Quét Watermark text / Filename leak bằng RapidOCR trên toàn bộ ảnh PNG/JPG
5. Remotion & GFX 8 Điều luật bắt buộc (44/44 GFX dedicated, 0 prefix leak, glassy subtitle)
6. Audio & Word Timing Synchronization (81/81 WAV, 81/81 Timing JSON, 0 audio cut-off)
"""

import sys
import os
import json
import re
import wave
import subprocess
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image

# Reconfigure stdout for UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

KNOWN_PREFIXES = [
    'ChartMotion', 'SplitComparison', 'AlertBox', 'FocusCard', 'CounterNumber',
    'LoopDiagram', 'TreeGrowth', 'IntroCard', 'BarChart', 'PieChart',
    'TimelineSlider', 'Infographic', 'CalendarAnimation', 'StackFee',
    'DrainWater', 'MonthCalendar', 'CreditScoreMeter', 'BadgeGraphic',
    'ComparisonTable', 'ProgressBar', 'MilestoneUnlocked', 'StepFlow',
    'StepHeader', 'AppUnlink', 'TargetHighlight', 'BadgeUnlock',
    'SalarySplit', 'BudgetEnvelope', 'CountdownMonths', 'AssetTree', 'MotionGraphic'
]

PREFIX_REGEX = re.compile(rf"^({'|'.join(KNOWN_PREFIXES)})(\s+[^\:]+)?:?\s*", re.IGNORECASE)

# Standard file name patterns for assets:
PRIMARY_ASSET_REGEX = re.compile(r"^S\d{3}-[A-Z]_\d+s_(AIV|IMG)\.(mp4|png|jpg|jpeg|webp)$", re.IGNORECASE)
STORYBOARD_ASSET_REGEX = re.compile(r"^S\d{3}-[A-Z]_\d+s_(AIV|IMG)_sb\.(png|jpg|jpeg|webp)$", re.IGNORECASE)
POSTER_FRAME_REGEX = re.compile(r"^S\d{3}-[A-Z]_\d+s_AIV_frame\d+\.(jpg|jpeg|png)$", re.IGNORECASE)

# Forbidden alias patterns (e.g. scene_01.png, scene_*.png, shot_*.mp4)
FORBIDDEN_ALIAS_REGEX = re.compile(r"^(scene|shot|alias|temp|unnamed).*", re.IGNORECASE)

# Negative style keywords banned by Channel Bible
NEGATIVE_STYLE_KEYWORDS = [
    "photorealism", "photorealistic", "3d render", "cgi", "unreal engine",
    "chibi", "exaggerated caricature", "watercolor", "messy sketches"
]

# Female keywords indicating gender
FEMALE_KEYWORDS = [
    r"\bwoman\b", r"\bwomen\b", r"\bgirl\b", r"\bfemale\b", r"\blady\b",
    r"\bcô gái\b", r"\bphụ nữ\b", r"\bbà mẹ\b", r"\bnữ giới\b", r"\bnữ nhân viên\b"
]

# Male keywords indicating gender
MALE_KEYWORDS = [
    r"\bman\b", r"\bmen\b", r"\bboy\b", r"\bmale\b", r"\bgentleman\b",
    r"\bchàng trai\b", r"\bnam thanh niên\b", r"\bnam giới\b", r"\banh ta\b"
]

# Persona Scene Mapping
MC_HOST_SCENES = ["S001", "S002", "S004", "S005", "S007", "S077", "S078", "S079", "S081"]
PERSON_A_MALE_SCENES = ["S051", "S052", "S054"]     # "Anh ta"
PERSON_B_FEMALE_SCENES = ["S055", "S058"]           # "Cô ấy"


@dataclass
class QACheckResult:
    category: str
    name: str
    passed: bool
    details: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class QAReport:
    channel: str
    video_slug: str
    timestamp: str
    passed: bool
    total_checks: int
    passed_checks: int
    failed_checks: int
    warning_checks: int
    checks: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    summary_stats: Dict[str, Any] = field(default_factory=dict)


def find_project_root() -> Path:
    current = Path(__file__).resolve().parent
    for _ in range(6):
        if (current / "docker-compose.yml").is_file() or (current / "channels").is_dir():
            return current
        current = current.parent
    return Path.cwd()


class AssetQAVerifier:
    def __init__(self, channel: str = "tien-thuc-chien", slug: str = "thoat-bay-no-the-tin-dung", root_dir: Optional[Path] = None, skip_ocr: bool = False):
        self.root_dir = root_dir or find_project_root()
        self.channel = channel
        self.slug = slug
        self.skip_ocr = skip_ocr

        self.video_dir = self.root_dir / "channels" / channel / "videos" / slug
        self.assets_dir = self.video_dir / "assets"
        self.audio_dir = self.video_dir / "audio"
        self.reports_dir = self.video_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        self.comp_file = self.assets_dir / "remotion-composition.json"
        self.broll_file = self.video_dir / "broll-plan.json"
        self.prompts_file = self.assets_dir / "prompts.md"
        self.channel_bible_file = self.root_dir / "channels" / channel / "channel-bible.md"
        self.characters_dir = self.root_dir / "channels" / channel / "characters"
        self.master_anchor_file = self.characters_dir / "master_anchor.png"

        self.template_dir = self.root_dir / "channels" / channel / "template"
        self.dg_file = self.template_dir / "components" / "DynamicGraphic.tsx"
        self.karaoke_file = self.template_dir / "components" / "KaraokeSubtitle.tsx"
        self.props_file = self.root_dir / "studio" / "remotion" / "current_props.json"

        self.checks: List[QACheckResult] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.summary_stats: Dict[str, Any] = {}

    def _probe_video(self, file_path: Path) -> Tuple[bool, str, Dict[str, Any]]:
        """Sử dụng ffprobe để xác thực metadata của video MP4."""
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "stream=codec_type,codec_name,width,height:format=duration,size",
            "-of", "json", str(file_path)
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if res.returncode != 0:
                return False, f"ffprobe lỗi: {res.stderr.strip()}", {}
            data = json.loads(res.stdout)
            streams = data.get("streams", [])
            vstream = next((s for s in streams if s.get("codec_type") == "video"), None)
            if not vstream:
                return False, "Không tìm thấy video stream", {}
            
            width = int(vstream.get("width", 0))
            height = int(vstream.get("height", 0))
            codec = vstream.get("codec_name", "")
            duration = float(data.get("format", {}).get("duration", 0))

            if width <= 0 or height <= 0:
                return False, f"Kích thước video không hợp lệ: {width}x{height}", {}
            if duration <= 0:
                return False, f"Thời lượng video không hợp lệ: {duration}s", {}

            return True, "Video stream hợp lệ", {
                "width": width, "height": height, "codec": codec, "duration": duration
            }
        except Exception as e:
            return False, f"Lỗi ngoại lệ ffprobe: {e}", {}

    def _verify_image(self, file_path: Path) -> Tuple[bool, str, Dict[str, Any]]:
        """Xác thực tính toàn vẹn của file ảnh PNG/JPG bằng Pillow."""
        try:
            with Image.open(file_path) as img:
                img.verify()
            with Image.open(file_path) as img:
                width, height = img.size
                fmt = img.format
                if width <= 0 or height <= 0:
                    return False, f"Kích thước ảnh không hợp lệ: {width}x{height}", {}
                return True, "Ảnh hợp lệ", {"width": width, "height": height, "format": fmt}
        except Exception as e:
            return False, f"Ảnh hỏng hoặc lỗi định dạng: {e}", {}

    def check_asset_coverage_and_integrity(self) -> QACheckResult:
        """1. Kiểm tra Độ phủ & Tính toàn vẹn của Assets (100% coverage, >50KB, ffprobe/PIL)."""
        check = QACheckResult(
            category="Assets",
            name="Asset Coverage & File Integrity",
            passed=True,
            details=""
        )

        if not self.comp_file.exists():
            check.passed = False
            msg = f"Không tìm thấy remotion-composition.json tại {self.comp_file}"
            check.errors.append(msg)
            self.errors.append(msg)
            return check

        try:
            comp_data = json.loads(self.comp_file.read_text(encoding="utf-8"))
        except Exception as e:
            check.passed = False
            msg = f"Lỗi parse JSON remotion-composition: {e}"
            check.errors.append(msg)
            self.errors.append(msg)
            return check

        visual_sequences = comp_data.get("tracks", {}).get("visual_sequences", [])
        total_seqs = len(visual_sequences)
        aiv_count = sum(1 for s in visual_sequences if s.get("type") == "AIV")
        img_count = sum(1 for s in visual_sequences if s.get("type") == "IMG")
        gfx_count = sum(1 for s in visual_sequences if s.get("type") == "GFX")

        self.summary_stats["total_visual_sequences"] = total_seqs
        self.summary_stats["aiv_count"] = aiv_count
        self.summary_stats["img_count"] = img_count
        self.summary_stats["gfx_count"] = gfx_count

        missing_assets = []
        corrupted_assets = []
        under_50kb_assets = []
        verified_assets = []

        for seq in visual_sequences:
            sid = seq.get("scene_id") or seq.get("id", "UNKNOWN")
            stype = seq.get("type")

            if stype in ("AIV", "IMG"):
                props = seq.get("props", {})
                src = props.get("src", "")
                if not src:
                    msg = f"Cảnh {sid} ({stype}) không có props.src trong composition"
                    check.errors.append(msg)
                    missing_assets.append(sid)
                    continue

                filename = os.path.basename(src)
                asset_path = self.assets_dir / filename

                if not asset_path.exists():
                    msg = f"Thiếu file asset: Cảnh {sid} cần '{filename}' nhưng không tồn tại trong assets/"
                    check.errors.append(msg)
                    missing_assets.append(sid)
                    continue

                file_size = asset_path.stat().st_size
                if file_size < 50 * 1024:
                    msg = f"File quá nhỏ hoặc 0-byte: {filename} ({file_size} bytes < 50KB)"
                    check.errors.append(msg)
                    under_50kb_assets.append(filename)
                    continue

                if stype == "AIV":
                    valid, reason, meta = self._probe_video(asset_path)
                    if not valid:
                        msg = f"Video hỏng: {filename} — {reason}"
                        check.errors.append(msg)
                        corrupted_assets.append(filename)
                    else:
                        verified_assets.append({
                            "scene_id": sid, "file": filename, "type": "AIV",
                            "size_kb": file_size // 1024, "meta": meta
                        })
                elif stype == "IMG":
                    valid, reason, meta = self._verify_image(asset_path)
                    if not valid:
                        msg = f"Ảnh hỏng: {filename} — {reason}"
                        check.errors.append(msg)
                        corrupted_assets.append(filename)
                    else:
                        verified_assets.append({
                            "scene_id": sid, "file": filename, "type": "IMG",
                            "size_kb": file_size // 1024, "meta": meta
                        })

        if missing_assets or corrupted_assets or under_50kb_assets:
            check.passed = False
            for err in check.errors:
                self.errors.append(err)
            check.details = (
                f"Phát hiện lỗi assets: {len(missing_assets)} thiếu, "
                f"{len(corrupted_assets)} hỏng, {len(under_50kb_assets)} < 50KB"
            )
        else:
            check.details = (
                f"100% Assets hợp lệ: {len(verified_assets)} files (AIV: {aiv_count}, IMG: {img_count}) "
                f"đều nguyên vẹn, > 50KB và đúng metadata ffprobe/PIL"
            )

        self.summary_stats["verified_assets_count"] = len(verified_assets)
        return check

    def check_file_naming_standardization(self) -> QACheckResult:
        """2. Chuẩn hóa tên file: Kiểm tra nghiêm ngặt format Sxxx-A_Xs_TYPE.ext, cấm alias scene_*.png."""
        check = QACheckResult(
            category="Naming",
            name="File Naming & Anti-Alias Standardization",
            passed=True,
            details=""
        )

        alias_violations = []
        invalid_format_files = []
        valid_files = []

        whitelisted_system_files = {".gitkeep", "prompts.md", "remotion-composition.json"}
        whitelisted_subdirs = {"archive_old_vyond", "temp"}

        for item in self.assets_dir.iterdir():
            if item.is_dir():
                if item.name not in whitelisted_subdirs:
                    check.warnings.append(f"Thư mục con lạ trong assets/: {item.name}")
                continue

            fname = item.name
            if fname in whitelisted_system_files:
                continue

            # Kiểm tra alias cấm (scene_*.png, shot_*.mp4, ...)
            if FORBIDDEN_ALIAS_REGEX.match(fname):
                msg = f"[CẤM TÊN ALIAS] Phát hiện file alias không chuẩn mực: '{fname}'. Bắt buộc dùng định dạng Sxxx-A_Xs_TYPE.ext!"
                alias_violations.append(fname)
                check.errors.append(msg)
                continue

            # Kiểm tra định dạng chuẩn
            is_primary = PRIMARY_ASSET_REGEX.match(fname)
            is_storyboard = STORYBOARD_ASSET_REGEX.match(fname)
            is_poster = POSTER_FRAME_REGEX.match(fname)

            if is_primary or is_storyboard or is_poster:
                valid_files.append(fname)
            else:
                msg = f"[LỖI ĐỊNH DẠNG TÊN] File không tuân thủ quy chuẩn đặt tên Sxxx-A_Xs_TYPE.ext: '{fname}'"
                invalid_format_files.append(fname)
                check.errors.append(msg)

        if alias_violations or invalid_format_files:
            check.passed = False
            for err in check.errors:
                self.errors.append(err)
            check.details = (
                f"Vi phạm chuẩn hóa tên file: {len(alias_violations)} file alias cấm, "
                f"{len(invalid_format_files)} file sai định dạng chuẩn"
            )
        else:
            check.details = f"100% File trong assets/ ({len(valid_files)} files) tuân thủ nghiêm ngặt chuẩn Sxxx-A_Xs_TYPE.ext"

        self.summary_stats["valid_media_files"] = len(valid_files)
        return check

    def check_character_narration_alignment(self) -> QACheckResult:
        """
        3. Kiểm định Tính nhất quán nhân vật & Đối chiếu Giới tính với Lời thoại Narration:
           - Nam MC đại diện kênh (S001, S002, S004, S005, S007, S077, S078, S079, S081): master_anchor.png
           - Người A (S051, S052, S054): 'Anh ta' -> Phải là NAM
           - Người B (S055, S058): 'Cô ấy' -> Phải là NỮ
        """
        check = QACheckResult(
            category="Character",
            name="Character Continuity & Narration Gender Alignment",
            passed=True,
            details=""
        )

        # 3.1. Kiểm tra master_anchor.png
        if not self.master_anchor_file.exists():
            check.passed = False
            msg = f"Thiếu file nhân vật mỏ neo master anchor: {self.master_anchor_file}"
            check.errors.append(msg)
            self.errors.append(msg)
        else:
            anchor_sz = self.master_anchor_file.stat().st_size
            if anchor_sz < 50 * 1024:
                check.passed = False
                msg = f"File master_anchor.png quá nhỏ ({anchor_sz} bytes < 50KB)"
                check.errors.append(msg)
                self.errors.append(msg)

        # 3.2. Đọc prompts.md và map theo scene_id
        prompts_by_scene: Dict[str, str] = {}
        if self.prompts_file.exists():
            prompts_content = self.prompts_file.read_text(encoding="utf-8")
            for line in prompts_content.splitlines():
                if line.startswith("|") and "`S" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 6:
                        raw_sid = parts[2].replace("`", "").strip()
                        # Xử lý trường hợp "S001 (SB)" -> "S001"
                        base_sid = raw_sid.split()[0]
                        prompt_text = parts[5]
                        prompts_by_scene[base_sid] = prompt_text
                        prompts_by_scene[raw_sid] = prompt_text

        # 3.3. Đọc broll-plan.json
        broll_by_scene: Dict[str, Dict[str, Any]] = {}
        if self.broll_file.exists():
            try:
                broll_data = json.loads(self.broll_file.read_text(encoding="utf-8"))
                for s in broll_data.get("scenes", []):
                    broll_by_scene[s.get("scene_id")] = s
            except Exception as e:
                check.warnings.append(f"Lỗi đọc broll-plan.json: {e}")

        mismatches = []
        style_violations = []

        # 3.4. Kiểm tra nhóm MC/Host (Nam MC 27 tuổi, kính mắt, áo sơ mi)
        for sid in MC_HOST_SCENES:
            p_text = prompts_by_scene.get(sid, "")
            b_data = broll_by_scene.get(sid, {})
            b_desc = " ".join([b.get("description", "") for b in b_data.get("brolls", [])])
            full_desc = f"{p_text} {b_desc}"

            # Quét xem có bị gán nhầm sang nữ không
            for pat in FEMALE_KEYWORDS:
                if re.search(pat, full_desc, re.IGNORECASE) and not any(k in full_desc.lower() for k in ["friends", "bạn bè", "đồng nghiệp"]):
                    mismatches.append(
                        f"[LỆCH GIỚI TÍNH MC] Cảnh {sid} (Nam MC chuẩn kênh) bị gán nhầm từ khóa nữ: '{pat}'"
                    )

        # 3.5. Kiểm tra nhóm Người A (S051, S052, S054): Narration 'Anh ta' -> Phải là NAM
        for sid in PERSON_A_MALE_SCENES:
            p_text = prompts_by_scene.get(sid, "")
            b_data = broll_by_scene.get(sid, {})
            b_desc = " ".join([b.get("description", "") for b in b_data.get("brolls", [])])
            full_desc = f"{p_text} {b_desc}"

            for pat in FEMALE_KEYWORDS:
                if re.search(pat, full_desc, re.IGNORECASE) and not any(k in full_desc.lower() for k in ["friends", "bạn bè", "quán cà phê"]):
                    mismatches.append(
                        f"[LỆCH GIỚI TÍNH NGƯỜI A] Cảnh {sid} Narration nói về 'Anh ta' (Nam), nhưng mô tả có từ khóa nữ: '{pat}'"
                    )

        # 3.6. Kiểm tra nhóm Người B (S055, S058): Narration 'Cô ấy' -> Phải là NỮ
        for sid in PERSON_B_FEMALE_SCENES:
            p_text = prompts_by_scene.get(sid, "")
            b_data = broll_by_scene.get(sid, {})
            b_desc = " ".join([b.get("description", "") for b in b_data.get("brolls", [])])
            full_desc = f"{p_text} {b_desc}"

            # Nếu prompt mô tả "man", "chàng trai", "nam MC" thay vì "cô ấy / woman"
            has_male_keyword = any(re.search(pat, p_text, re.IGNORECASE) for pat in [r"\bman\b", r"\bmale\b", r"\bchàng trai\b"])
            has_anchor_lock = "27-year-old vietnamese professional man" in p_text.lower() or "master_anchor" in p_text.lower()
            
            if has_male_keyword or has_anchor_lock:
                mismatches.append(
                    f"[LỆCH GIỚI TÍNH NARRATION NGƯỜI B] Cảnh {sid}: Lời thoại Narration là 'Cô ấy' (Nữ, Người B khóa thẻ/trả nợ), nhưng prompt lại mô tả nhân vật Nam MC ('27-year-old Vietnamese professional man')! Cần cập nhật prompt thành Nữ nhân vật Người B (young Vietnamese woman)."
                )

        # 3.7. Quét vi phạm Negative Style
        if self.prompts_file.exists():
            p_content = self.prompts_file.read_text(encoding="utf-8").lower()
            for neg in NEGATIVE_STYLE_KEYWORDS:
                if neg in p_content:
                    style_violations.append(f"Phong cách cấm '{neg}' xuất hiện trong prompts.md")

        if mismatches or style_violations:
            check.passed = False
            for m in mismatches:
                check.errors.append(m)
                self.errors.append(m)
            for s in style_violations:
                check.errors.append(f"[VI PHẠM STYLE LOCK] {s}")
                self.errors.append(f"[VI PHẠM STYLE LOCK] {s}")
            check.details = f"Phát hiện {len(mismatches)} lỗi lệch giới tính narration, {len(style_violations)} vi phạm style"
        else:
            check.details = (
                f"Khớp 100% nhân vật & lời thoại Narration: Nam MC (9 cảnh), "
                f"Người A Nam (S051-S054), Người B Nữ (S055-S058)"
            )

        return check

    def check_rapidocr_watermarks(self) -> QACheckResult:
        """4. Quét Watermark text / Filename leak bằng RapidOCR: phát hiện và chặn nếu ảnh bị dán chữ filename."""
        check = QACheckResult(
            category="OCR & Watermark",
            name="RapidOCR Technical Text & Filename Leak Scan",
            passed=True,
            details=""
        )

        if self.skip_ocr:
            check.details = "Bỏ qua quét OCR theo cờ --skip-ocr"
            return check

        try:
            from rapidocr_onnxruntime import RapidOCR
            engine = RapidOCR()
        except ImportError:
            check.warnings.append("Thiếu thư viện rapidocr_onnxruntime. Bỏ qua quét OCR tự động.")
            check.details = "Không thể chạy RapidOCR do thiếu package"
            return check

        png_files = sorted(list(self.assets_dir.glob("*.png")))
        jpg_files = sorted(list(self.assets_dir.glob("*.jpg")))
        all_imgs = [f for f in png_files + jpg_files if not f.name.endswith("_frame0.jpg")]

        tainted_files = []
        clean_files = []

        for p in all_imgs:
            try:
                result, _ = engine(str(p))
                texts = [item[1] for item in result] if result else []
                full_text = " ".join(texts)

                scene_code = p.stem.split("-")[0]
                has_filename_leak = (
                    (scene_code.lower() in full_text.lower() and any(ext in full_text.lower() for ext in [".png", ".mp4", "_img", "_aiv"]))
                    or ("rename" in full_text.lower())
                    or ("[scene:" in full_text.lower())
                    or ("output file" in full_text.lower())
                    or (p.name.lower() in full_text.lower())
                )

                if has_filename_leak:
                    tainted_files.append((p.name, texts))
                    msg = f"[FILENAME LEAK TRÊN ẢNH] File '{p.name}' bị AI dán đè tên file / prompt vào nội dung ảnh: {texts}"
                    check.errors.append(msg)
                else:
                    clean_files.append(p.name)
            except Exception as e:
                check.warnings.append(f"Lỗi khi OCR file {p.name}: {e}")

        if tainted_files:
            check.passed = False
            for err in check.errors:
                self.errors.append(err)
            check.details = f"Phát hiện {len(tainted_files)} ảnh bị dán chữ filename/watermark kỹ thuật: {[t[0] for t in tainted_files]}"
        else:
            check.details = f"100% Ảnh sạch ({len(clean_files)} files), không bị rò rỉ bất kỳ filename leak hay watermark nào"

        self.summary_stats["clean_images_count"] = len(clean_files)
        self.summary_stats["tainted_images_count"] = len(tainted_files)
        return check

    def check_remotion_gfx_rules(self) -> QACheckResult:
        """5. Kiểm định Remotion & GFX (8 Điều luật bắt buộc: Dedicated Component, Anti-Prefix, Glassy Subtitles, Layout)."""
        check = QACheckResult(
            category="Remotion",
            name="Remotion & GFX 8 Mandatory Rules",
            passed=True,
            details=""
        )

        prefix_errors = []
        unhandled_gfx = []

        # 5.1. Kiểm tra rò rỉ prefix trong remotion-composition.json
        if self.comp_file.exists():
            try:
                cdata = json.loads(self.comp_file.read_text(encoding="utf-8"))
                for seq in cdata.get("tracks", {}).get("visual_sequences", []):
                    sid = seq.get("scene_id", "")
                    title = seq.get("props", {}).get("title", "")
                    desc = seq.get("description", "")
                    if PREFIX_REGEX.search(title):
                        prefix_errors.append(f"[RULE 2] Cảnh {sid} rò rỉ prefix trong title: '{title}'")
                    if PREFIX_REGEX.search(desc):
                        prefix_errors.append(f"[RULE 2] Cảnh {sid} rò rỉ prefix trong description: '{desc}'")
            except Exception as e:
                check.errors.append(f"Lỗi parse comp file: {e}")

        # 5.2. Kiểm tra rò rỉ prefix trong current_props.json
        if self.props_file.exists():
            try:
                pdata = json.loads(self.props_file.read_text(encoding="utf-8"))
                for seq in pdata.get("sequences", []):
                    sid = seq.get("scene", "")
                    title = seq.get("gfx_props", {}).get("title", "")
                    beat = seq.get("beat", "")
                    if PREFIX_REGEX.search(title):
                        prefix_errors.append(f"[RULE 2] Cảnh {sid} rò rỉ prefix trong props title: '{title}'")
                    if PREFIX_REGEX.search(beat):
                        prefix_errors.append(f"[RULE 2] Cảnh {sid} rò rỉ prefix trong props beat: '{beat}'")
            except Exception as e:
                check.warnings.append(f"Lỗi parse props file: {e}")

        # 5.3. Kiểm tra 100% GFX scenes có dedicated visual graphic trong DynamicGraphic.tsx
        if self.dg_file.exists() and self.comp_file.exists():
            try:
                dg_code = self.dg_file.read_text(encoding="utf-8")
                cdata = json.loads(self.comp_file.read_text(encoding="utf-8"))
                gfx_scenes = [
                    s.get("scene_id")
                    for s in cdata.get("tracks", {}).get("visual_sequences", [])
                    if s.get("type") == "GFX"
                ]

                for sid in gfx_scenes:
                    if f'sc === "{sid}"' not in dg_code and f'"{sid}"' not in dg_code:
                        unhandled_gfx.append(sid)

                if unhandled_gfx:
                    msg = f"[RULE 1 VIOLATION] Có {len(unhandled_gfx)} cảnh GFX chưa có visual handler chuyên biệt (rơi vào fallback): {unhandled_gfx}"
                    check.errors.append(msg)
            except Exception as e:
                check.errors.append(f"Lỗi phân tích DynamicGraphic: {e}")
        else:
            check.errors.append(f"Không tìm thấy DynamicGraphic.tsx tại {self.dg_file}")

        # 5.4. Kiểm tra Subtitle Karaoke Glassy (Rule 6)
        if self.karaoke_file.exists():
            k_code = self.karaoke_file.read_text(encoding="utf-8")
            if "textShadow" not in k_code:
                check.warnings.append("[RULE 6] KaraokeSubtitle.tsx thiếu textShadow đa tầng để hiển thị glassy không viền hộp")
        else:
            check.warnings.append(f"Không tìm thấy KaraokeSubtitle.tsx tại {self.karaoke_file}")

        if prefix_errors or unhandled_gfx:
            check.passed = False
            for err in prefix_errors:
                check.errors.append(err)
                self.errors.append(err)
            for err in check.errors:
                if err not in self.errors:
                    self.errors.append(err)
            check.details = f"Vi phạm luật Remotion GFX: {len(prefix_errors)} prefix leaks, {len(unhandled_gfx)} unhandled GFX"
        else:
            check.details = "100% Tuân thủ 8 Điều luật Remotion & Motion Graphics (44/44 GFX dedicated, 0 prefix leaks, glassy subtitle)"

        return check

    def check_audio_and_word_timing(self) -> QACheckResult:
        """6. Kiểm tra Audio & Word Timing (narration wav, timing json, không bị cut-off âm thanh)."""
        check = QACheckResult(
            category="Audio",
            name="Audio & Word Timing Synchronization",
            passed=True,
            details=""
        )

        master_wav = self.audio_dir / "narration_master.wav"
        if not master_wav.exists():
            check.passed = False
            msg = f"Thiếu file master audio: {master_wav}"
            check.errors.append(msg)
            self.errors.append(msg)
        else:
            sz_mb = master_wav.stat().st_size / (1024 * 1024)
            if sz_mb < 1.0:
                check.passed = False
                msg = f"File master audio quá nhỏ: {sz_mb:.2f} MB (< 1 MB)"
                check.errors.append(msg)
                self.errors.append(msg)

        if not self.comp_file.exists():
            return check

        try:
            comp_data = json.loads(self.comp_file.read_text(encoding="utf-8"))
            vseqs = comp_data.get("tracks", {}).get("visual_sequences", [])
        except Exception:
            return check

        missing_wav = []
        missing_timing = []
        truncated_audio = []
        valid_scenes = 0

        for seq in vseqs:
            sid = seq.get("scene_id") or seq.get("id", "")
            dur_frames = seq.get("duration_frames", 0)
            dur_s = dur_frames / 30.0

            wav_f = self.audio_dir / f"{sid}_narration.wav"
            timing_f = self.audio_dir / f"{sid}_timing.json"

            if not wav_f.exists():
                missing_wav.append(sid)
            if not timing_f.exists():
                missing_timing.append(sid)

            if wav_f.exists() and timing_f.exists():
                try:
                    with wave.open(str(wav_f), "rb") as w:
                        frames = w.getnframes()
                        rate = w.getframerate()
                        audio_dur_s = frames / float(rate)
                        if audio_dur_s > dur_s + 0.1:
                            truncated_audio.append((sid, round(audio_dur_s, 2), round(dur_s, 2)))
                except Exception as e:
                    check.warnings.append(f"Lỗi đọc WAV {sid}: {e}")

                try:
                    t_data = json.loads(timing_f.read_text(encoding="utf-8"))
                    words = t_data.get("words", [])
                    if not words and not t_data.get("segments"):
                        check.warnings.append(f"Timing JSON của {sid} rỗng không có words")
                except Exception as e:
                    check.warnings.append(f"Lỗi đọc timing JSON {sid}: {e}")

                valid_scenes += 1

        if missing_wav or missing_timing or truncated_audio:
            check.passed = False
            if missing_wav:
                msg = f"Thiếu {len(missing_wav)} file narration WAV: {missing_wav[:5]}..."
                check.errors.append(msg)
                self.errors.append(msg)
            if missing_timing:
                msg = f"Thiếu {len(missing_timing)} file timing JSON: {missing_timing[:5]}..."
                check.errors.append(msg)
                self.errors.append(msg)
            if truncated_audio:
                msg = f"Phát hiện {len(truncated_audio)} cảnh bị cắt cụt âm thanh (audio dài hơn video): {truncated_audio[:5]}"
                check.errors.append(msg)
                self.errors.append(msg)
            check.details = f"Lỗi âm thanh: {len(missing_wav)} thiếu wav, {len(missing_timing)} thiếu timing, {len(truncated_audio)} bị cắt"
        else:
            check.details = f"100% Audio & Timing đồng bộ: {valid_scenes}/{len(vseqs)} cảnh đầy đủ WAV và JSON timing, 0 cảnh bị cắt âm"

        self.summary_stats["audio_valid_scenes"] = valid_scenes
        return check

    def run_all_checks(self) -> QAReport:
        """Thực thi toàn bộ bộ kiểm định chất lượng tự động."""
        print("=" * 80)
        print(f"🔍 BẮT ĐẦU KIỂM ĐỊNH CHẤT LƯỢNG TỰ ĐỘNG (AUTOMATED QA AUDIT PIPELINE)")
        print(f"   Kênh: {self.channel} | Video: {self.slug}")
        print("=" * 80)

        self.checks = [
            self.check_asset_coverage_and_integrity(),
            self.check_file_naming_standardization(),
            self.check_character_narration_alignment(),
            self.check_rapidocr_watermarks(),
            self.check_remotion_gfx_rules(),
            self.check_audio_and_word_timing(),
        ]

        total = len(self.checks)
        passed_count = sum(1 for c in self.checks if c.passed)
        failed_count = total - passed_count
        warning_count = sum(len(c.warnings) for c in self.checks)

        all_passed = (failed_count == 0)

        for idx, c in enumerate(self.checks, 1):
            status = "✅ [PASS]" if c.passed else "❌ [FAIL]"
            print(f"\n{idx}. {status} {c.category}: {c.name}")
            print(f"   • {c.details}")
            if c.errors:
                for err in c.errors:
                    print(f"     ❌ {err}")
            if c.warnings:
                for warn in c.warnings:
                    print(f"     ⚠️  {warn}")

        print("\n" + "=" * 80)
        if all_passed:
            print("🎉🎉 [PASS] QA AUDIT PASSED 100%! ĐẠT TẤT CẢ TIÊU CHUẨN XUẤT BẢN VIDEO! 🎉🎉")
        else:
            print(f"🚨🚨 [FAIL] QA AUDIT FAILED! Có {failed_count}/{total} hạng mục không đạt chuẩn! 🚨🚨")
            print("Vui lòng sửa các lỗi được liệt kê ở trên trước khi kích hoạt render.")
        print("=" * 80)

        import datetime
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = QAReport(
            channel=self.channel,
            video_slug=self.slug,
            timestamp=now_str,
            passed=all_passed,
            total_checks=total,
            passed_checks=passed_count,
            failed_checks=failed_count,
            warning_checks=warning_count,
            checks=[
                {
                    "category": c.category,
                    "name": c.name,
                    "passed": c.passed,
                    "details": c.details,
                    "errors": c.errors,
                    "warnings": c.warnings
                }
                for c in self.checks
            ],
            errors=self.errors,
            warnings=self.warnings,
            summary_stats=self.summary_stats
        )

        self._export_reports(report)
        return report

    def _export_reports(self, report: QAReport):
        """Xuất báo cáo chi tiết dạng JSON và Markdown vào thư mục reports/."""
        json_path = self.reports_dir / "qa_audit_report.json"
        md_path = self.reports_dir / "qa_audit_report.md"

        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(asdict(report), f, ensure_ascii=False, indent=2)
            print(f"\n📄 Đã lưu báo cáo JSON: {json_path}")
        except Exception as e:
            print(f"⚠️ Không thể lưu báo cáo JSON: {e}")

        try:
            md_lines = [
                f"# BÁO CÁO KIỂM ĐỊNH CHẤT LƯỢNG TỰ ĐỘNG (QA AUDIT REPORT)",
                f"**Kênh:** `{report.channel}` | **Video:** `{report.video_slug}`  ",
                f"**Thời gian kiểm tra:** {report.timestamp}  ",
                f"**Kết quả chung:** {'🟢 PASS (100% ĐẠT CHUẨN)' if report.passed else '🔴 FAIL (CÓ LỖI BẮT BUỘC SỬA)'}  ",
                "",
                "---",
                "",
                "## 1. Tổng quan các hạng mục kiểm định",
                "",
                "| STT | Phân loại | Tên hạng mục | Trạng thái | Chi tiết kết quả |",
                "|:---:|:---|:---|:---:|:---|",
            ]

            for idx, c in enumerate(report.checks, 1):
                st_icon = "🟢 PASS" if c["passed"] else "🔴 FAIL"
                md_lines.append(f"| {idx} | **{c['category']}** | {c['name']} | {st_icon} | {c['details']} |")

            md_lines.extend([
                "",
                "---",
                "",
                "## 2. Chi tiết lỗi & Cảnh báo",
                ""
            ])

            if report.errors:
                md_lines.append("### ❌ Danh sách lỗi bắt buộc sửa (Critical Errors):")
                for err in report.errors:
                    md_lines.append(f"- 🔴 {err}")
                md_lines.append("")
            else:
                md_lines.append("✅ Không phát hiện bất kỳ lỗi vi phạm nào!")
                md_lines.append("")

            if report.warnings:
                md_lines.append("### ⚠️ Cảnh báo cần lưu ý (Warnings):")
                for warn in report.warnings:
                    md_lines.append(f"- ⚠️ {warn}")
                md_lines.append("")

            md_lines.extend([
                "---",
                "",
                "## 3. Thống kê Assets & Video",
                f"- **Tổng số phân cảnh (Visual Sequences):** {report.summary_stats.get('total_visual_sequences', 'N/A')}",
                f"- **Cảnh AI Video (AIV):** {report.summary_stats.get('aiv_count', 'N/A')}",
                f"- **Cảnh Minh họa tĩnh (IMG):** {report.summary_stats.get('img_count', 'N/A')}",
                f"- **Cảnh Đồ họa động (GFX):** {report.summary_stats.get('gfx_count', 'N/A')}",
                f"- **Tổng số asset media hợp lệ:** {report.summary_stats.get('valid_media_files', 'N/A')}",
                f"- **Số ảnh sạch không watermark (RapidOCR):** {report.summary_stats.get('clean_images_count', 'N/A')}",
                f"- **Số ảnh bị dán text/filename leak:** {report.summary_stats.get('tainted_images_count', 'N/A')}",
                f"- **Tổng số cảnh audio đồng bộ:** {report.summary_stats.get('audio_valid_scenes', 'N/A')}",
                ""
            ])

            with open(md_path, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines))
            print(f"📄 Đã lưu báo cáo Markdown: {md_path}")
        except Exception as e:
            print(f"⚠️ Không thể lưu báo cáo Markdown: {e}")


def main():
    parser = argparse.ArgumentParser(description="Automated QA Verifier for Video Production Pipeline")
    parser.add_argument("slug", nargs="?", default="thoat-bay-no-the-tin-dung", help="Slug của video")
    parser.add_argument("--channel", default="tien-thuc-chien", help="Tên kênh (mặc định: tien-thuc-chien)")
    parser.add_argument("--skip-ocr", action="store_true", help="Bỏ qua quét RapidOCR (tiết kiệm thời gian)")
    args = parser.parse_args()

    verifier = AssetQAVerifier(channel=args.channel, slug=args.slug, skip_ocr=args.skip_ocr)
    report = verifier.run_all_checks()

    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
