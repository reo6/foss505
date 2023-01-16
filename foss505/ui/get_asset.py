"""
Simple utility to get the path of the asset file requested.
"""
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent / "assets"

def asset(path: str):
    return str(ASSETS_DIR / path)
