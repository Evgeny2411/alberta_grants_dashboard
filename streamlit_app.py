"""
Streamlit Community Cloud entry point.

This file acts as the main entry point for Streamlit Community Cloud deployment.
It imports the main app module and ensures it executes on every rerun.
"""

from __future__ import annotations

import importlib
import sys

MODULE_NAME = "src.app"


def _load_app() -> None:
    """Import or reload the app module so Streamlit renders reliably."""

    if MODULE_NAME in sys.modules:
        # Drop cached module so Streamlit runs fresh import on rerun.
        del sys.modules[MODULE_NAME]
        importlib.invalidate_caches()

    importlib.import_module(MODULE_NAME)


_load_app()
