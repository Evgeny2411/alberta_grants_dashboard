"""Tiny smoke test to verify environment and imports."""

import importlib

packages = ["streamlit", "pandas", "plotly", "dotenv"]

missing = []
for p in packages:
    try:
        importlib.import_module(p)
    except Exception as e:
        missing.append((p, str(e)))

if missing:
    raise SystemExit(f"Missing or failing imports: {missing}")

print("OK: imports work")
