"""
Simple utility to get the path of the asset file requested.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

def asset(path: str):
    return str(ASSETS_DIR / path)
