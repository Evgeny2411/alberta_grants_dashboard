"""
Streamlit Community Cloud entry point.

This file acts as the main entry point for Streamlit Community Cloud deployment.
It simply imports and runs the main app from src/app.py.
"""

# Import the main app
from src.app import *  # noqa: F401, F403

# The app will run automatically when this file is executed by streamlit
