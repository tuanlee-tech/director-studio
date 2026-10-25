#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cdp_client.py — Chrome DevTools Protocol Client for Google Flow Automation
Kết nối trực tiếp tới Google Chrome qua WebSocket CDP để:
1. Định vị tab Google Flow
2. Điền prompt vào ô chatbox
3. Bấm gửi và theo dõi trạng thái hoàn tất
4. Trích xuất URL asset (ảnh hoặc video) và tải về thư mục local
"""

import sys
import os
import json
import time
import urllib.request
import requests
from pathlib import Path

# Fix UTF-8 for Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    import websocket
except ImportError:
    websocket = None


class FlowCDPClient:
    def __init__(self, port=9222, timeout=120):
        self.port = port
        self.timeout = timeout
        self.ws_url = None
        self.target_id = None
        self.ws = None
        self._msg_id = 0

    def connect(self):
        """Tìm tab Google Flow và mở kết nối WebSocket."""
        if not websocket:
            raise RuntimeError("Thiếu thư viện 'websocket'. Vui lòng chạy: pip install websocket-client")

        list_url = f"http://127.0.0.1:{self.port}/json/list"
        try:
            req = urllib.request.Request(list_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                tabs = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            raise ConnectionError(f"Không thể kết nối tới Chrome trên port {self.port}. Hãy đảm bảo Chrome đang chạy với '--remote-debugging-port={self.port}'. Lỗi: {e}")

        # Tìm tab có URL chứa flow.google.com hoặc tab type == 'page'
        target_tab = None
        for tab in tabs:
            url = tab.get("url", "")
            if "flow.google.com" in url:
                target_tab = tab
                break

        if not target_tab:
            # Nếu chưa có tab flow.google.com, lấy page đầu tiên hoặc mở tab mới
            pages = [t for t in tabs if t.get("type") == "page"]
            target_tab = pages[0] if pages else None

        if not target_tab:
            raise RuntimeError(f"Không tìm thấy tab trình duyệt nào khả dụng trên port {self.port}")

        self.target_id = target_tab.get("id")
        self.ws_url = target_tab.get("webSocketDebuggerUrl")

        if not self.ws_url:
            raise RuntimeError(f"Tab không cung cấp webSocketDebuggerUrl (tab ID: {self.target_id})")

        self.ws = websocket.create_connection(self.ws_url, timeout=10)
        return True

    def close(self):
        if self.ws:
            try:
                self.ws.close()
            except Exception:
                pass
            self.ws = None

    def send_cdp_command(self, method, params=None):
        """Gửi lệnh CDP qua WebSocket và nhận kết quả."""
        if not self.ws:
            self.connect()

        self._msg_id += 1
        payload = {
            "id": self._msg_id,
            "method": method,
            "params": params or {}
        }

        self.ws.send(json.dumps(payload))
        
        start_time = time.time()
        while time.time() - start_time < 15:
            resp_str = self.ws.recv()
            if not resp_str:
                continue
            data = json.loads(resp_str)
            if data.get("id") == self._msg_id:
                return data.get("result", {})

        return {}

    def evaluate_js(self, expression):
        """Thực thi mã JavaScript trên trang và nhận kết quả trả về."""
        res = self.send_cdp_command("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True
        })
        val = res.get("result", {})
        return val.get("value")

    def check_page_loaded(self):
        """Kiểm tra xem trang Google Flow đã load xong chưa."""
        js = """
        (() => {
            return {
                url: window.location.href,
                title: document.title,
                has_input: document.querySelector('textarea, [contenteditable="true"], input[type="text"]') !== null,
                is_flow: window.location.href.includes('flow.google.com')
            };
        })()
        """
        return self.evaluate_js(js)

    def inject_and_send_prompt(self, prompt_text):
        """Điền prompt vào ô chatbox của Google Flow và bấm gửi."""
        # Escape các ký tự đặc biệt trong prompt_text cho JavaScript string
        safe_prompt = json.dumps(prompt_text)

        js = f"""
        (() => {{
            const textToEnter = {safe_prompt};
            
            // Tìm ô input prompt của Google Flow
            const selectors = [
                'textarea[placeholder*="Describe"]',
                'textarea[placeholder*="prompt"]',
                'textarea',
                '[contenteditable="true"]',
                'input[type="text"]'
            ];
            
            let inputEl = null;
            for (const sel of selectors) {{
                const el = document.querySelector(sel);
                if (el && el.offsetParent !== null) {{ // Phần tử đang hiển thị
                    inputEl = el;
                    break;
                }}
            }}

            if (!inputEl) {{
                return {{ success: false, error: 'Không tìm thấy ô nhập prompt trên giao diện' }};
            }}

            // Focus và nhập nội dung
            inputEl.focus();
            if (inputEl.tagName.toLowerCase() === 'textarea' || inputEl.tagName.toLowerCase() === 'input') {{
                inputEl.value = textToEnter;
                inputEl.dispatchEvent(new Event('input', {{ bubbles: true }}));
                inputEl.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }} else {{
                inputEl.innerText = textToEnter;
                inputEl.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}

            // Tìm nút Send hoặc gửi phím Enter
            setTimeout(() => {{
                const sendButtons = Array.from(document.querySelectorAll('button')).filter(btn => {{
                    const label = (btn.getAttribute('aria-label') || btn.innerText || '').toLowerCase();
                    return label.includes('send') || label.includes('generate') || label.includes('submit') || btn.querySelector('svg');
                }});
                
                if (sendButtons.length > 0) {{
                    sendButtons[sendButtons.length - 1].click();
                }} else {{
                    inputEl.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                }}
            }}, 300);

            return {{ success: true, message: 'Đã gửi prompt thành công' }};
        }})()
        """
        return self.evaluate_js(js)

    def extract_recent_media_urls(self):
        """Trích xuất danh sách link ảnh hoặc video vừa sinh."""
        js = """
        (() => {
            const results = [];
            // Tìm các thẻ video và hình ảnh kết quả
            const videos = Array.from(document.querySelectorAll('video source, video[src]')).map(v => v.src || v.currentSrc).filter(Boolean);
            const images = Array.from(document.querySelectorAll('img')).map(img => img.src).filter(src => src && (src.includes('blob:') || src.includes('googleusercontent') || src.includes('data:image') || src.includes('generativelanguage')));

            return {
                videos: Array.from(new Set(videos)),
                images: Array.from(new Set(images))
            };
        })()
        """
        return self.evaluate_js(js)

    def download_asset_file(self, url, dest_path):
        """Tải asset từ url về file local."""
        dest_path = Path(dest_path)
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            resp = requests.get(url, stream=True, timeout=30)
            if resp.status_code == 200:
                with open(dest_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True, dest_path
            return False, f"HTTP {resp.status_code}"
        except Exception as e:
            return False, str(e)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Test Google Flow CDP Client.")
    parser.add_argument("--port", type=int, default=9222, help="Debug port (mặc định 9222)")
    parser.add_argument("--check", action="store_true", help="Kiểm tra kết nối và trang hiện tại")

    args = parser.parse_args()
    client = FlowCDPClient(port=args.port)

    print(f"🔌 Đang kết nối tới Chrome trên port {args.port}...")
    try:
        client.connect()
        print("✅ Kết nối WebSocket CDP thành công!")
        info = client.check_page_loaded()
        print(f"📄 Thông tin tab hiện tại: {json.dumps(info, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"❌ Kết nối thất bại: {e}")
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    main()
