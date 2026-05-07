"""Durable Snake app entry point.

Copyright (c) 2026 Alexandre Roman. All rights reserved.
"""

import sys

APP_DIR = "/app"

if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from badge_app import run_app
from engine import main, cleanup

run_app("Durable Snake", main, cleanup)
