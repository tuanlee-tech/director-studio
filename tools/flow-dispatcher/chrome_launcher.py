#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chrome_launcher.py — Google Flow Multi-Account Chrome Launcher (Wrapper)
Chuyển tiếp tới browser_pool.py để đồng nhất quản lý Chrome CDP.
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from browser_pool import (
    find_chrome_executable,
    resolve_profile_path,
    load_accounts_config,
    save_accounts_config,
    check_cdp_status,
    get_active_tabs,
    launch_account,
    close_account,
    launch_all,
    close_all,
    get_accounts,
    main
)

action_start_all = launch_all
action_status = lambda: main()

if __name__ == "__main__":
    main()
