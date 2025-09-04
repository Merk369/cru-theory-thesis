#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_figures.py

Purpose
-------
End-to-end offline pipeline:
1) Generate/refresh datasets in ./data via fetch_* scripts.
2) Build all figures in ./figures via build_figures.py.

Usage
-----
python scripts/fetch_figures.py
python scripts/fetch_figures.py --force   # overwrite data & figures

Notes
-----
- Assumes this file lives in CRU-thesis/scripts/.
- All called scripts are local and offline-safe.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Project roots/paths
SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT_DIR    = SCRIPTS_DIR.parent
DATA_DIR    = ROOT_DIR / "data"
FIG_DIR     = ROOT_DIR / "figures"

# Script paths
FETCH_PLANCK = SCRIPTS_DIR / "fetch_planck.py"
FETCH_AUGER  = SCRIPTS_DIR / "fetch_auger.py"
FETCH_GW     = SCRIPTS_DIR / "fetch_gw.py"
FETCH_DM     = SCRIPTS_DIR / "fetch_dm.py"
BUILD_FIGS   = SCRIPTS_DIR / "build_figures.py"


def check_exists(path: Path, desc: str) -> None:
    if not path.exists():
        print(f"[setup] Creating {desc}: {path}")
        path.mkdir(parents=True, exist_ok=True)


def run_script(script: Path, force: bool = False) -> None:
    if not script.exists():
        print(f"[error] Required script not found: {script}")
        sys.exit(1)
    cmd = [sys.executable, str(script)]
    if force:
        cmd.append("--force")
    print(f"[run] {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[error] Script failed: {script.name} (exit code {e.returncode})")
        sys.exit(e.returncode)


def main():
    ap = argparse.ArgumentParser(
        description="Prepare datasets and build all figures (offline)."
    )
    ap.add_argument(
        "--force", action="store_true",
        help="Overwrite existing CSVs and figures."
    )
    args = ap.parse_args()

    # Ensure directories exist
    check_exists(DATA_DIR, "data directory")
    check_exists(FIG_DIR, "figures directory")

    # 1) Fetch/generate datasets
    run_script(FETCH_PLANCK, force=args.force)
    run_script(FETCH_AUGER,  force=args.force)
    run_script(FETCH_GW,     force=args.force)
    run_script(FETCH_DM,     force=args.force)

    # 2) Build figures
    run_script(BUILD_FIGS,   force=args.force)

    print("[ok] Data prepared and figures built successfully.")


if __name__ == "__main__":
    main()
