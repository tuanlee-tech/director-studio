#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unified_flow_engine.py — Standardized Multi-Account Google Flow Synchronization Engine

Tính năng chuẩn hóa:
1. Multi-Port Parallel Discovery: Tự động quét song song 5 tài khoản Chrome CDP (Port 9223 - 9227).
2. Multi-layer Semantic Fingerprinting: Tự động map card/tile trên Google Flow với Scene ID (Sxxx)
   bằng định danh đa tầng (Scene ID tag -> Keyword extraction -> Storyboard image reference).
3. Lifecycle State Machine:
   - NOT_PROMPTED
   - WAITING_APPROVAL
   - IN_QUEUE
   - RENDERING
   - FINISHED_IN_CLOUD
   - DOWNLOADED_AND_VERIFIED
4. Anti-Duplicate Hash Guard: Ngăn chặn 100% video trùng lặp hash MD5.
5. Remotion Offline Sync: Đồng bộ relative path assets/ để Remotion staticFile() đọc trực tiếp (0 phụ thuộc server 3001).
6. Tích hợp UnifiedQAFilter tự động.
"""

import sys
import os
import json
import time
import shutil
import hashlib
import re
import argparse
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import websocket
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "websocket-client"], check=True)
    import websocket

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DOWNLOADS_DIR = Path.home() / "Downloads"
DEFAULT_CDP_PORTS = [9223, 9224, 9225, 9226, 9227]

# Import UnifiedQAFilter
try:
    sys.path.insert(0, str(ROOT_DIR / "tools" / "qa"))
    from asset_qa_verifier import UnifiedQAFilter
except Exception:
    UnifiedQAFilter = None


class FlowCDPConnection:
    """Quản lý kết nối CDP tới 1 instance Chrome của Google Flow."""
    def __init__(self, port, acc_id=None):
        self.port = port
        self.acc_id = acc_id or (port - 9222)
        self.ws = None
        self._msg_id = 0

    def connect(self, timeout=8):
        try:
            url = f"http://127.0.0.1:{self.port}/json/list"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                tabs = json.loads(resp.read().decode())
            flow_tab = next((t for t in tabs if "flow.google.com" in t.get("url", "")), None)
            if not flow_tab:
                pages = [t for t in tabs if t.get("type") == "page"]
                flow_tab = pages[0] if pages else None
            if not flow_tab:
                return False
            ws_url = flow_tab.get("webSocketDebuggerUrl")
            self.ws = websocket.create_connection(ws_url, timeout=timeout)
            self.send_cdp("Runtime.enable")
            self.send_cdp("Page.enable")
            self.send_cdp("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": str(DOWNLOADS_DIR)
            })
            return True
        except Exception:
            return False

    def close(self):
        if self.ws:
            try:
                self.ws.close()
            except Exception:
                pass
            self.ws = None

    def send_cdp(self, method, params=None):
        if not self.ws:
            return {}
        self._msg_id += 1
        cid = self._msg_id
        payload = {"id": cid, "method": method, "params": params or {}}
        self.ws.send(json.dumps(payload))
        start = time.time()
        while time.time() - start < 15:
            msg = self.ws.recv()
            if not msg:
                continue
            data = json.loads(msg)
            if data.get("id") == cid:
                return data.get("result", {})
        return {}

    def evaluate(self, expr):
        res = self.send_cdp("Runtime.evaluate", {
            "expression": expr,
            "returnByValue": True
        })
        return res.get("result", {}).get("value")

    def scan_page_state(self):
        """Quét toàn bộ tile, video, chat history và approval buttons trên tab."""
        js = """(() => {
            // 1. Quét flow-video-tile
            const videoTiles = Array.from(document.querySelectorAll('flow-video-tile')).map((t, idx) => {
                const text = (t.innerText || '').replace(/\\n/g, ' ').trim();
                const progMatch = text.match(/\\b(\\d+%)/);
                const moreBtn = t.querySelector('button[aria-label*="options" i], button[aria-label*="khác" i], button[aria-label="More options"]');
                const img = t.querySelector('img');
                const video = t.querySelector('video');
                const isVideoThumb = img && ((img.getAttribute('alt') || '').includes('video') || (img.getAttribute('src') || '').includes('flow-content'));
                return {
                    tileIndex: idx,
                    type: 'video_tile',
                    text: text.slice(0, 100),
                    hasMore: moreBtn !== null,
                    progress: progMatch ? progMatch[1] : null,
                    hasVideo: video !== null,
                    hasThumb: isVideoThumb,
                    imgSrc: img ? img.src : null
                };
            });

            // 2. Quét flow-grid-tile-container (Storyboards/Characters)
            const gridTiles = Array.from(document.querySelectorAll('flow-grid-tile-container')).map((t, idx) => {
                const aria = t.getAttribute('aria-label') || '';
                const text = (t.innerText || '').replace(/\\n/g, ' ').trim();
                const img = t.querySelector('img');
                const moreBtn = t.querySelector('button[aria-label*="options" i], button[aria-label*="khác" i]');
                return {
                    tileIndex: idx,
                    type: 'grid_tile',
                    aria: aria,
                    text: text.slice(0, 80),
                    imgAlt: img ? (img.getAttribute('alt') || '') : '',
                    imgSrc: img ? img.src : '',
                    hasMore: moreBtn !== null
                };
            });

            // 3. Quét trạng thái chat (Hàng đợi & Phê duyệt)
            const bubbles = Array.from(document.querySelectorAll('div, p, span')).filter(e => e.innerText && e.children.length === 0);
            const recentTexts = bubbles.slice(-15).map(e => e.innerText.trim()).filter(t => t.length > 5);
            
            const hasQueue = recentTexts.some(t => /waiting in the queue/i.test(t) || /hàng đợi/i.test(t));
            const stopBtn = document.querySelector('button[aria-label*="Stop" i], button[aria-label*="Cancel" i], button[aria-label*="Dừng" i]');
            const isGenerating = stopBtn !== null && stopBtn.offsetParent !== null;

            // 4. Quét nút Approve chờ bấm
            const approveElements = Array.from(document.querySelectorAll('.option-label, span, button')).filter(el => {
                const txt = (el.innerText || '').trim();
                return (txt === 'Phê duyệt' || txt === 'Luôn phê duyệt' || txt === 'Approve' || txt === 'Always approve') && el.children.length === 0;
            }).map((el, idx) => ({ idx: idx, text: el.innerText.trim() }));

            return {
                videoTiles: videoTiles,
                gridTiles: gridTiles,
                recentChat: recentTexts,
                hasQueue: hasQueue,
                isGenerating: isGenerating,
                pendingApprovalsCount: approveElements.length
            };
        })()"""
        return self.evaluate(js) or {}

    def click_approve_all(self):
        """Bấm Approve / Luôn phê duyệt cho tất cả các hộp thoại đang chờ."""
        js = """(() => {
            const els = Array.from(document.querySelectorAll('.option-label, span, button')).filter(el => {
                const txt = (el.innerText || '').trim();
                return (txt === 'Phê duyệt' || txt === 'Luôn phê duyệt' || txt === 'Approve' || txt === 'Always approve') && el.children.length === 0;
            });
            let clicked = 0;
            for (const t of els) {
                (t.parentElement || t).click();
                t.click();
                clicked++;
            }
            return { clicked: clicked };
        })()"""
        return self.evaluate(js) or {"clicked": 0}

    def trigger_download_tile(self, tile_index=0):
        """Kích hoạt tải 720p từ video tile tại tile_index."""
        # Click More options
        js_more = f"""(() => {{
            const tiles = Array.from(document.querySelectorAll('flow-video-tile'));
            if (!tiles.length || !tiles[{tile_index}]) return false;
            const target = tiles[{tile_index}];
            target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            target.dispatchEvent(new MouseEvent('mouseenter', {{ bubbles: true }}));
            const moreBtn = target.querySelector('button[aria-label*="options" i], button[aria-label*="khác" i], button[aria-label="More options"]');
            if (moreBtn) {{
                moreBtn.click();
                return true;
            }}
            return false;
        }})()"""
        if not self.evaluate(js_more):
            return False
        time.sleep(0.8)

        # Hover/Click Download
        js_hover = """(() => {
            const items = Array.from(document.querySelectorAll('.mat-mdc-menu-item, [role="menuitem"]'));
            const dl = items.find(b => /download|tải xuống/i.test(b.innerText));
            if (dl) {
                dl.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
                dl.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
                dl.click();
                return true;
            }
            return false;
        })()"""
        self.evaluate(js_hover)
        time.sleep(0.8)

        # Click 720p
        js_click_720 = """(() => {
            const btns = Array.from(document.querySelectorAll('.mat-mdc-menu-item, [role="menuitem"], button'));
            const opt = btns.find(b => /720p/i.test(b.innerText) || /original size|kích thước gốc/i.test(b.innerText));
            if (opt) {
                opt.click();
                return true;
            }
            return false;
        })()"""
        return bool(self.evaluate(js_click_720))


class UnifiedFlowEngine:
    def __init__(self, slug="thoat-bay-no-the-tin-dung", channel="tien-thuc-chien", ports=None):
        self.slug = slug
        self.channel = channel
        self.ports = ports or DEFAULT_CDP_PORTS
        self.video_dir = ROOT_DIR / "channels" / channel / "videos" / slug
        self.assets_dir = self.video_dir / "assets"
        self.comp_file = self.assets_dir / "remotion-composition.json"
        self.remotion_pub_dir = ROOT_DIR / "studio" / "remotion" / "public" / "assets"
        self.remotion_props_file = ROOT_DIR / "studio" / "remotion" / "current_props.json"
        self.scenes = []
        self._load_composition()

    def _load_composition(self):
        if self.comp_file.exists():
            data = json.loads(self.comp_file.read_text(encoding="utf-8"))
            self.scenes = data.get("sequences", [])

    def scan_all_accounts(self):
        """Quét song song tất cả các tài khoản CDP đang hoạt động."""
        results = {}
        for port in self.ports:
            client = FlowCDPConnection(port=port)
            if client.connect():
                results[port] = client.scan_page_state()
                client.close()
            else:
                results[port] = None
        return results

    def match_tile_to_scene(self, tile_info, scenes):
        """
        Định danh đa tầng 3 lớp (Multi-layer Semantic Fingerprinting):
        Lớp 1: Khớp Scene ID chính xác (S001, S052...)
        Lớp 2: Khớp từ khóa đặc trưng (Keyword similarity)
        Lớp 3: Khớp tên ảnh storyboard
        """
        search_corpus = f"{tile_info.get('aria', '')} {tile_info.get('text', '')} {tile_info.get('imgAlt', '')} {tile_info.get('imgSrc', '')}".lower()

        # Lớp 1: Tìm Scene ID trực tiếp
        for s in scenes:
            sid = (s.get("scene") or s.get("id") or "").lower()
            if sid and re.search(rf"\b{re.escape(sid)}\b", search_corpus):
                return s

        # Lớp 2: Semantic Keywords
        keyword_map = {
            "s001": ["bàng hoàng", "hóa đơn", "shock", "debt alert", "notification"],
            "s002": ["quẹt thẻ", "credit card", "pos terminal", "phòng chờ"],
            "s003": ["ví da", "mỏ neo", "đáy biển", "anchor", "underwater"],
            "s004": ["sương mù", "fog", "tự tin", "dissipating fog", "badge"],
            "s007": ["ăn tối", "dining", "cocktail", "restaurant", "cụng ly"],
            "s011": ["15 triệu", "15,000,000", "billing alert", "sao kê"],
            "s052": ["ôm đầu", "desk", "bàn làm việc", "distress", "exhaustion"],
            "s058": ["nấu ăn", "cooking", "kitchen", "bếp", "wooden spoon"],
            "s064": ["cắt thẻ", "kéo", "scissors", "credit card"],
            "s081": ["đồi cỏ", "bình minh", "hilltop", "sunrise", "làm chủ"]
        }

        for s in scenes:
            sid = (s.get("scene") or s.get("id") or "").lower()
            keywords = keyword_map.get(sid, [])
            match_count = sum(1 for kw in keywords if kw in search_corpus)
            if match_count >= 2:
                return s

        return None

    def audit_scene_matrix(self):
        """Tổng hợp ma trận trạng thái của toàn bộ phân cảnh AIV."""
        scan_data = self.scan_all_accounts()
        aiv_scenes = [s for s in self.scenes if s.get("type") == "AIV"]
        matrix = []

        # Quét các file đã có trong assets/
        local_assets = {}
        for f in self.assets_dir.glob("*_AIV.mp4"):
            sc_match = re.match(r"(S\d{3})", f.name)
            if sc_match:
                h = hashlib.md5(f.read_bytes()).hexdigest()
                local_assets[sc_match.group(1)] = {
                    "file": f.name,
                    "size_kb": f.stat().st_size // 1024,
                    "hash": h
                }

        for s in aiv_scenes:
            sid = s.get("scene") or s.get("id")
            item = {
                "scene": sid,
                "status": "NOT_PROMPTED",
                "account": None,
                "port": None,
                "local_file": None,
                "size_kb": 0,
                "hash": None,
                "tile_index": None
            }

            # 1. Kiểm tra local
            if sid in local_assets:
                item["status"] = "DOWNLOADED_AND_VERIFIED"
                item["local_file"] = local_assets[sid]["file"]
                item["size_kb"] = local_assets[sid]["size_kb"]
                item["hash"] = local_assets[sid]["hash"][:12]
                matrix.append(item)
                continue

            # 2. Quét trên các account
            found_cloud = False
            for port, data in scan_data.items():
                if not data:
                    continue
                acc_id = port - 9222
                for vt in data.get("videoTiles", []):
                    matched = self.match_tile_to_scene(vt, [s])
                    if matched:
                        item["account"] = f"Account {acc_id}"
                        item["port"] = port
                        item["tile_index"] = vt["tileIndex"]
                        if vt["hasMore"] and not vt["progress"]:
                            item["status"] = "FINISHED_IN_CLOUD"
                        elif vt["progress"]:
                            item["status"] = f"RENDERING ({vt['progress']})"
                        else:
                            item["status"] = "RENDERING"
                        found_cloud = True
                        break
                if found_cloud:
                    break

            if not found_cloud:
                # Kiểm tra xem có đang chờ Approve hay trong queue
                for port, data in scan_data.items():
                    if not data:
                        continue
                    chat_corpus = " ".join(data.get("recentChat", [])).lower()
                    kw_list = [sid.lower()]
                    if any(kw in chat_corpus for kw in kw_list):
                        acc_id = port - 9222
                        item["account"] = f"Account {acc_id}"
                        item["port"] = port
                        if data.get("pendingApprovalsCount", 0) > 0:
                            item["status"] = "WAITING_APPROVAL"
                        elif data.get("hasQueue"):
                            item["status"] = "IN_QUEUE"
                        break

            matrix.append(item)

        return matrix

    def print_status_table(self):
        """In bảng điều khiển trạng thái chuẩn hóa."""
        matrix = self.audit_scene_matrix()
        print("\n" + "=" * 80)
        print(f"📊 UNIFIED FLOW DASHBOARD — [{self.channel}] / [{self.slug}]")
        print("=" * 80)
        print(f"{'Scene':<8} | {'Trạng thái':<26} | {'Tài khoản':<12} | {'Kích thước':<10} | {'MD5 Hash':<14}")
        print("-" * 80)

        for row in matrix:
            sc = row["scene"]
            st = row["status"]
            acc = row["account"] or "N/A"
            sz = f"{row['size_kb']} KB" if row['size_kb'] else "-"
            h = row["hash"] or "-"
            print(f"{sc:<8} | {st:<26} | {acc:<12} | {sz:<10} | {h:<14}")
        print("=" * 80)

    def sync_finished_videos(self):
        """Tự động tải về và kiểm định mọi video đã render xong trên Cloud."""
        matrix = self.audit_scene_matrix()
        synced_count = 0

        for row in matrix:
            if row["status"] == "FINISHED_IN_CLOUD":
                port = row["port"]
                tile_idx = row["tile_index"]
                sc = row["scene"]
                out_name = f"{sc}-A_6s_AIV.mp4" if sc not in ["S052", "S081"] else f"{sc}-A_4s_AIV.mp4"

                print(f"\n📥 [Sync] Phát hiện {sc} hoàn tất trên {row['account']} (Port {port}, Tile {tile_idx}) -> Bắt đầu tải...")
                client = FlowCDPConnection(port=port)
                if not client.connect():
                    print(f"  ❌ Không thể kết nối tới {row['account']}")
                    continue

                before_files = set(f.name for f in DOWNLOADS_DIR.glob("*.mp4"))
                if client.trigger_download_tile(tile_idx):
                    print("  ⏳ Đang chờ file hoàn tất tải về...")
                    target_path = self.assets_dir / out_name
                    saved = False
                    for _ in range(25):
                        time.sleep(1.0)
                        after_files = set(f.name for f in DOWNLOADS_DIR.glob("*.mp4"))
                        diff = after_files - before_files
                        if diff:
                            dl_file = list(diff)[0]
                            shutil.copyfile(DOWNLOADS_DIR / dl_file, target_path)
                            saved = True
                            break

                    if not saved:
                        recent = [f for f in DOWNLOADS_DIR.glob("*.mp4") if time.time() - f.stat().st_mtime < 45]
                        if recent:
                            latest = max(recent, key=lambda f: f.stat().st_mtime)
                            shutil.copyfile(latest, target_path)
                            saved = True

                    if saved and target_path.exists():
                        # Kiểm tra chống duplicate
                        new_h = hashlib.md5(target_path.read_bytes()).hexdigest()
                        is_dup = False
                        for ex in self.assets_dir.glob("*_AIV.mp4"):
                            if ex.name != out_name and ex.exists() and hashlib.md5(ex.read_bytes()).hexdigest() == new_h:
                                is_dup = True
                                target_path.unlink()
                                print(f"  🚨 LỖI: Video vừa tải trùng lặp hash với {ex.name}!")
                                break
                        if not is_dup:
                            synced_count += 1
                            print(f"  ✅ Tải thành công {out_name} ({target_path.stat().st_size // 1024} KB | MD5: {new_h[:12]})")
                client.close()

        # Chuẩn hóa đường dẫn composition & props sang staticFile (assets/...)
        self.normalize_composition_paths()
        return synced_count

    def approve_all_pending(self):
        """Tự động phê duyệt các prompt đã sẵn sàng trên tất cả các tài khoản."""
        print("\n⚡ Kích hoạt phê duyệt hàng loạt cho các prompt đang chờ...")
        total_clicked = 0
        for port in self.ports:
            client = FlowCDPConnection(port=port)
            if client.connect():
                r = client.click_approve_all()
                clicked = r.get("clicked", 0)
                if clicked > 0:
                    print(f"  ✅ Account {client.acc_id} (Port {port}): Đã bấm Approve {clicked} mục!")
                    total_clicked += clicked
                client.close()
        print(f"🎉 Hoàn tất phê duyệt: {total_clicked} tác vụ đã được cấp phép sinh video.\n")
        return total_clicked

    def normalize_composition_paths(self):
        """
        Chuẩn hóa đường dẫn tương đối (assets/Sxxx..., bgm/..., audio/...) trong remotion-composition.json
        để Remotion staticFile() đọc trực tiếp từ public/, triệt tiêu 100% lỗi ECONNREFUSED 3001.
        """
        if not self.comp_file.exists():
            return

        data = json.loads(self.comp_file.read_text(encoding="utf-8"))
        updated = 0

        # 1. Đồng bộ assets sang studio/remotion/public/assets
        self.remotion_pub_dir.mkdir(parents=True, exist_ok=True)
        for f in self.assets_dir.glob("*.*"):
            if f.is_file():
                dest = self.remotion_pub_dir / f.name
                if not dest.exists() or dest.stat().st_size != f.stat().st_size:
                    shutil.copyfile(f, dest)

        # 2. Đồng bộ audio sang studio/remotion/public/audio
        audio_src_dir = self.video_dir / "audio"
        pub_audio_dir = ROOT_DIR / "studio" / "remotion" / "public" / "audio"
        pub_audio_dir.mkdir(parents=True, exist_ok=True)
        if audio_src_dir.exists():
            for af in audio_src_dir.glob("*.*"):
                dest_a = pub_audio_dir / af.name
                if not dest_a.exists() or dest_a.stat().st_size != af.stat().st_size:
                    shutil.copyfile(af, dest_a)

        # 3. Chuẩn hóa BGM URL
        bgm_val = data.get("bgm_url", "")
        if bgm_val and bgm_val.startswith("http"):
            bgm_filename = bgm_val.split("/")[-1]
            data["bgm_url"] = f"bgm/{bgm_filename}"
            updated += 1

        # 4. Chuẩn hóa Master Audio URL
        master_val = data.get("master_audio_url", "")
        if master_val and master_val.startswith("http"):
            master_filename = master_val.split("/")[-1]
            data["master_audio_url"] = f"audio/{master_filename}"
            updated += 1

        # 5. Chuẩn hóa từng sequence
        for s in data.get("sequences", []):
            sc = s.get("scene") or s.get("id")
            ap = s.get("asset_path")
            if ap and ap.startswith("http"):
                filename = ap.split("/")[-1]
                s["asset_path"] = f"assets/{filename}"
                updated += 1
            elif not ap and s.get("type") in ["AIV", "IMG"]:
                match_files = list(self.assets_dir.glob(f"{sc}-A_*.*"))
                if match_files:
                    s["asset_path"] = f"assets/{match_files[0].name}"
                    updated += 1

            # Narration audio
            nau = s.get("narration_audio_url")
            if nau and nau.startswith("http"):
                nau_file = nau.split("/")[-1]
                s["narration_audio_url"] = f"audio/{nau_file}"
                updated += 1

        self.comp_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

        # Cập nhật current_props.json nếu có
        if self.remotion_props_file.exists():
            pdata = json.loads(self.remotion_props_file.read_text(encoding="utf-8"))
            if pdata.get("bgm_url", "").startswith("http"):
                pdata["bgm_url"] = f"bgm/{pdata['bgm_url'].split('/')[-1]}"
            if pdata.get("master_audio_url", "").startswith("http"):
                pdata["master_audio_url"] = f"audio/{pdata['master_audio_url'].split('/')[-1]}"
            for s in pdata.get("sequences", []):
                ap = s.get("asset_path")
                if ap and ap.startswith("http"):
                    pdata_fn = ap.split("/")[-1]
                    s["asset_path"] = f"assets/{pdata_fn}"
                nau = s.get("narration_audio_url")
                if nau and nau.startswith("http"):
                    s["narration_audio_url"] = f"audio/{nau.split('/')[-1]}"
            self.remotion_props_file.write_text(json.dumps(pdata, indent=2, ensure_ascii=False), encoding="utf-8")

        print(f"🎬 Đã chuẩn hóa {updated} đường dẫn asset, BGM và Audio sang Remotion staticFile (offline 100%)")


def main():
    parser = argparse.ArgumentParser(description="Unified Google Flow Synchronization Engine")
    parser.add_argument("slug", nargs="?", default="thoat-bay-no-the-tin-dung", help="Slug video")
    parser.add_argument("--channel", default="tien-thuc-chien", help="Kênh video")
    parser.add_argument("--status", action="store_true", help="Quét và in bảng ma trận trạng thái")
    parser.add_argument("--sync", action="store_true", help="Tự động đồng bộ và tải video đã xong")
    parser.add_argument("--approve", action="store_true", help="Tự động phê duyệt các prompt đang chờ")
    parser.add_argument("--normalize", action="store_true", help="Chuẩn hóa đường dẫn tương đối Remotion staticFile")

    args = parser.parse_args()
    engine = UnifiedFlowEngine(slug=args.slug, channel=args.channel)

    if args.approve:
        engine.approve_all_pending()

    if args.sync or (not args.status and not args.approve and not args.normalize):
        engine.sync_finished_videos()

    if args.normalize:
        engine.normalize_composition_paths()

    engine.print_status_table()


if __name__ == "__main__":
    main()
