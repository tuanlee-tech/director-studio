#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
browser_flow.py — Google Flow CDP Automation Agent
Thực hiện 4 bước tự động hóa Google Flow qua Chrome DevTools Protocol:
1. Kết nối WebSocket tới tab Flow / Project
2. Đảm bảo đang mở đúng Project URL (trang home không có ô nhập)
3. Điền prompt qua ProseMirror và dispatch KeyEvent Enter đúng 1 lần (không click nút)
4. Poll trạng thái tile / spinner và sync media (ảnh / video) về Studio
"""

import sys
import os
import json
import time
import socket
import re
import urllib.request
import requests
from pathlib import Path
from datetime import datetime

# Fix UTF-8 console output for Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent

try:
    import websocket
except ImportError:
    websocket = None


class FlowBrowserSession:
    def __init__(self, port, project_url=None, timeout=180):
        self.port = port
        self.project_url = project_url
        self.timeout = timeout
        self.ws = None
        self._msg_id = 0
        self.tab_id = None
        self.tab_url = None

    def connect(self):
        """Bước 1 & 2: Tìm tab Flow, kết nối WebSocket và đảm bảo project_tab được mở."""
        if not websocket:
            raise RuntimeError("Cần cài đặt thư viện 'websocket-client' (pip install websocket-client)")

        list_url = f"http://127.0.0.1:{self.port}/json/list"
        try:
            req = urllib.request.Request(list_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                tabs = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            raise ConnectionError(f"Không thể kết nối tới Chrome trên port {self.port}: {e}")

        # Tìm tab Flow hiện có
        target_tab = None
        for t in tabs:
            u = t.get("url", "")
            if "flow.google.com" in u:
                target_tab = t
                break

        if not target_tab:
            pages = [t for t in tabs if t.get("type") == "page"]
            target_tab = pages[0] if pages else None

        if not target_tab:
            raise RuntimeError(f"Không tìm thấy tab nào trên Chrome port {self.port}")

        self.tab_id = target_tab.get("id")
        self.tab_url = target_tab.get("url", "")
        ws_url = target_tab.get("webSocketDebuggerUrl")
        if not ws_url:
            raise RuntimeError(f"Không lấy được webSocketDebuggerUrl từ tab {self.tab_id}")

        self.ws = websocket.create_connection(ws_url, timeout=15)

        # Kích hoạt Runtime, Page, DOM domains
        self.send_cdp("Runtime.enable")
        self.send_cdp("Page.enable")

        # Đảm bảo vào đúng Project URL
        if self.project_url:
            self.ensure_project_tab(self.project_url)

        return True

    def close(self):
        if self.ws:
            try:
                self.ws.close()
            except Exception:
                pass
            self.ws = None

    def send_cdp(self, method, params=None, wait_response=True):
        """Gửi lệnh CDP qua WebSocket và đợi phản hồi khớp ID."""
        if not self.ws:
            raise RuntimeError("WebSocket chưa kết nối")

        self._msg_id += 1
        call_id = self._msg_id
        payload = {"id": call_id, "method": method, "params": params or {}}
        self.ws.send(json.dumps(payload))

        if not wait_response:
            return {}

        start = time.time()
        while time.time() - start < 20:
            msg = self.ws.recv()
            if not msg:
                continue
            data = json.loads(msg)
            if data.get("id") == call_id:
                if "error" in data:
                    raise RuntimeError(f"CDP Error ({method}): {data['error'].get('message')}")
                return data.get("result", {})

        return {}

    def evaluate(self, expression):
        """Thực thi JavaScript trong context trang web."""
        res = self.send_cdp("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True
        })
        val = res.get("result", {})
        return val.get("value")

    def ensure_project_tab(self, project_url):
        """
        Trang home Flow không có ô nhập → điều hướng tới trang project nếu cần.
        """
        if not project_url:
            return

        curr_url = self.evaluate("window.location.href") or ""
        # Nếu đã ở trong project
        if "/project/" in curr_url and (project_url in curr_url or curr_url in project_url):
            return

        print(f"🔄 Đang chuyển hướng tab tới Google Flow Project: {project_url}...")
        self.send_cdp("Page.navigate", {"url": project_url})

        # Đợi trang tải xong và ô ProseMirror xuất hiện
        start = time.time()
        while time.time() - start < 30:
            time.sleep(1.5)
            ready = self.evaluate("""
                (() => {
                    const ready = document.readyState === 'complete';
                    const hasInput = document.querySelector('.ProseMirror, [aria-label*="What do you want to create"]') !== null;
                    return ready && hasInput;
                })()
            """)
            if ready:
                print("✅ Trang Google Flow Project đã tải xong và sẵn sàng nhập prompt!")
                return
        print("⚠️ Hết thời gian chờ trang Project tải, tiếp tục thử tương tác...")

    def inject_and_send_prompt(self, prompt_text):
        """
        Bước 3: Nhập prompt vào ô ProseMirror và bấm Enter ĐÚNG 1 LẦN.
        Tuyệt đối không click nút submit vì nút trên Flow toggle thành 'Stop generation'.
        """
        escaped_prompt = json.dumps(prompt_text)

        # 3.1 Focus, selectAll, insertText và dispatch input event
        js_inject = f"""
        (() => {{
            const el = document.querySelector('.ProseMirror') || 
                       document.querySelector('[aria-label="What do you want to create?"]') ||
                       document.querySelector('textarea');
            if (!el) return {{ success: false, error: 'Không tìm thấy ô nhập prompt (.ProseMirror)' }};

            el.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('insertText', false, {escaped_prompt});
            el.dispatchEvent(new InputEvent('input', {{ bubbles: true }}));
            return {{ success: true }};
        }})()
        """
        res = self.evaluate(js_inject)
        if not res or not res.get("success"):
            error_msg = res.get("error") if res else "Lỗi không xác định khi tìm ô nhập prompt"
            raise RuntimeError(error_msg)

        time.sleep(0.3)

        # 3.2 Dispatch key event Enter đúng 1 lần (rawKeyDown + keyUp)
        enter_raw_down = {
            "type": "rawKeyDown",
            "windowsVirtualKeyCode": 13,
            "unmodifiedText": "\r",
            "text": "\r",
            "key": "Enter",
            "code": "Enter"
        }
        enter_up = {
            "type": "keyUp",
            "windowsVirtualKeyCode": 13,
            "unmodifiedText": "\r",
            "text": "\r",
            "key": "Enter",
            "code": "Enter"
        }

        self.send_cdp("Input.dispatchKeyEvent", enter_raw_down)
        self.send_cdp("Input.dispatchKeyEvent", enter_up)
        print("🚀 Đã inject prompt và nhấn phím Enter (1 lần) thành công!")
        return True

    def poll_tiles_status(self, target_scene_labels=None):
        """
        Bước 4: Quét các tile kết quả và spinner:
        - Nút Stop generation (button[aria-label*="Stop"])
        - flow-grid-tile-container, flow-video-tile lấy .footer-title + progress-percent != 0
        """
        labels_json = json.dumps(target_scene_labels or [])

        js_poll = f"""
        (() => {{
            const targetLabels = {labels_json}.map(l => l.toLowerCase());
            
            // Dò nút Stop/Cancel (hỗ trợ đa ngôn ngữ EN / VI)
            const stopBtn = document.querySelector('button[aria-label*="Stop" i], button[aria-label*="Cancel" i], button[aria-label*="Dừng" i], button[aria-label*="Hủy" i]');
            const isAgentRunning = stopBtn !== null && stopBtn.offsetParent !== null;

            // Quét các tile
            const tiles = Array.from(document.querySelectorAll('flow-grid-tile-container, flow-video-tile, [class*="tile"]'));
            const results = [];

            for (const tile of tiles) {{
                const titleEl = tile.querySelector('.footer-title, [class*="title"], h3, span');
                const titleText = titleEl ? titleEl.innerText.trim() : '';
                
                // Trạng thái spinner / inProgress
                const progressEl = tile.querySelector('[class*="progress"], [class*="spinner"], flow-progress');
                const percentText = progressEl ? (progressEl.getAttribute('progress-percent') || progressEl.innerText || '') : '';
                const inProgress = (percentText !== '' && percentText !== '0%' && percentText !== '0') || 
                                   tile.querySelector('.spinner, [role="progressbar"]') !== null;

                // Lấy URL media src
                const imgEl = tile.querySelector('img');
                const videoEl = tile.querySelector('video source, video');
                const mediaUrl = videoEl ? (videoEl.src || videoEl.currentSrc) : (imgEl ? imgEl.src : null);

                results.push({{
                    title: titleText,
                    in_progress: inProgress,
                    media_url: mediaUrl,
                    is_video: videoEl !== null
                }});
            }}

            return {{
                is_agent_running: isAgentRunning,
                tiles: results
            }};
        }})()
        """
        return self.evaluate(js_poll) or {"is_agent_running": False, "tiles": []}

    def wait_for_completion(self, target_scene_labels, is_video=False, timeout=None):
        """
        Vòng lặp poll mỗi ~2s:
        Ảnh: đủ các tile 'Scene N' target và không còn inProgress (timeout 180s).
        Video: timeout 450s.
        """
        max_timeout = timeout or (450 if is_video else 180)
        start_time = time.time()
        print(f"⏳ Bắt đầu giám sát tiến trình Google Flow (Timeout: {max_timeout}s, Targets: {target_scene_labels})...")

        # Đợi 3s ban đầu để agent Google Flow tiếp nhận prompt
        time.sleep(3)

        while time.time() - start_time < max_timeout:
            status = self.poll_tiles_status(target_scene_labels)
            is_running = status.get("is_agent_running", False)
            tiles = status.get("tiles", [])

            # Lọc các tile khớp với targets
            matched_tiles = {}
            for target in target_scene_labels:
                target_norm = target.strip().lower()
                for tile in tiles:
                    t_title = (tile.get("title") or "").strip().lower()
                    if target_norm in t_title or t_title in target_norm:
                        matched_tiles[target] = tile
                        break

            all_matched = len(matched_tiles) >= len(target_scene_labels)
            any_in_progress = any(t.get("in_progress") for t in matched_tiles.values()) or is_running

            elapsed = int(time.time() - start_time)
            print(f"⏱️ [{elapsed}s/{max_timeout}s] Đã tìm thấy {len(matched_tiles)}/{len(target_scene_labels)} tiles (Đang xử lý: {any_in_progress})")

            # Điều kiện hoàn thành: Đã đủ các tile target, có media URL và không còn inProgress
            if all_matched and not any_in_progress:
                all_have_url = all(bool(t.get("media_url")) for t in matched_tiles.values())
                if all_have_url:
                    print("🎉 Tất cả các Scene target đã hoàn tất và sẵn sàng tải về!")
                    return True, matched_tiles

            time.sleep(2)

        # Hết timeout: trả về những gì đã thu thập được
        status = self.poll_tiles_status(target_scene_labels)
        return False, matched_tiles


def sync_flow_media_to_studio(channel, slug, scene_idx, media_url, media_id=None, is_video=False):
    """
    Tải bytes media từ URL Google Flow về thư mục assets của scene.
    Cập nhật horizontal_image_url hoặc video_url và trạng thái COMPLETED trong composition.
    """
    video_dir = ROOT_DIR / "channels" / channel / "videos" / slug
    assets_dir = video_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    ext = "mp4" if is_video else "png"
    dest_filename = f"scene_{scene_idx:02d}.{ext}"
    dest_path = assets_dir / dest_filename

    print(f"📥 Đang tải asset Scene {scene_idx} từ Google Flow ({media_url[:60]}...)...")
    try:
        resp = requests.get(media_url, stream=True, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code == 200:
            with open(dest_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=16384):
                    f.write(chunk)
            print(f"💾 Đã lưu asset thành công: {dest_path.name} ({dest_path.stat().st_size // 1024} KB)")

            # Cập nhật remotion-composition.json
            comp_path = assets_dir / "remotion-composition.json"
            if comp_path.exists():
                try:
                    data = json.loads(comp_path.read_text(encoding="utf-8"))
                    scenes = data.get("scenes", [])
                    for s in scenes:
                        if s.get("index") == scene_idx:
                            if is_video:
                                s["video_url"] = f"/api/media/{channel}/{slug}/{dest_filename}"
                            else:
                                s["image_url"] = f"/api/media/{channel}/{slug}/{dest_filename}"
                                s["horizontal_image_url"] = f"/api/media/{channel}/{slug}/{dest_filename}"
                            s["status"] = "COMPLETED"
                            if media_id:
                                s["media_id"] = media_id
                            break
                    comp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
                except Exception as e:
                    print(f"⚠️ Lỗi cập nhật remotion-composition.json: {e}")

            return True, str(dest_path)
        else:
            return False, f"HTTP Error {resp.status_code}"
    except Exception as e:
        return False, str(e)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Google Flow CDP Agent Runner.")
    parser.add_argument("--port", type=int, default=9223, help="CDP Port")
    parser.add_argument("--project-url", default=None, help="Google Flow Project URL")
    parser.add_argument("--prompt", default=None, help="Prompt cần nhập")
    parser.add_argument("--status", action="store_true", help="Kiểm tra trạng thái tiles")

    args = parser.parse_args()
    session = FlowBrowserSession(port=args.port, project_url=args.project_url)

    try:
        session.connect()
        print("✅ Kết nối CDP thành công!")

        if args.prompt:
            session.inject_and_send_prompt(args.prompt)
            print("🚀 Prompt đã gửi, đang chờ hoàn tất...")
            ok, tiles = session.wait_for_completion(["Scene 1"])
            print("Kết quả:", tiles)
        elif args.status:
            st = session.poll_tiles_status()
            print(json.dumps(st, indent=2, ensure_ascii=False))
        else:
            print("Tab URL:", session.tab_url)
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()
