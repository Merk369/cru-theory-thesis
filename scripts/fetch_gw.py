#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_gw.py

Purpose
-------
Populate data/gw_strain.csv with an offline, representative stochastic GW
background strain spectrum h(f) suitable for plots and pass/fail checks in
the CRU technical thesis. No network access is used.

Behavior
--------
- If data/gw_strain.csv does NOT exist, it is created with a smooth set of
  (f, h, sigma_h) points across PTA→LISA bands.
- If it exists, the script exits unless --force is given.

CSV schema
----------
f_Hz,h_strain,sigma_h,source

Usage
-----
python scripts/fetch_gw.py           # create if missing
python scripts/fetch_gw.py --force   # overwrite
"""

import os
import csv
import math
import argparse
from typing import List, Dict

ROOT     = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, "data")
OUT_CSV  = os.path.join(DATA_DIR, "gw_strain.csv")


def generate_strain_rows() -> List[Dict[str, str]]:
    """
    Create an illustrative h(f) ~ h0 * (f / f0)^alpha curve with gentle roll-off,
    spanning ~nHz (PTA) to ~tens of mHz (LISA). Values are representative ONLY
    and intended for deterministic builds and checks.
    """
    # Reference point (illustrative)
    f0    = 1.0e-3       # 1 mHz
    h0    = 1.0e-22      # baseline strain at f0
    alpha = 2.0          # spectral slope in h ∝ f^alpha (illustrative)
    # Frequency grid: PTA (~nHz) → LISA (~10 mHz)
    f_grid = [
        1.0e-9, 2.0e-9, 5.0e-9,
        1.0e-8, 2.0e-8, 5.0e-8,
        1.0e-7, 2.0e-7, 5.0e-7,
        1.0e-6, 2.0e-6, 5.0e-6,
        1.0e-5, 2.0e-5, 5.0e-5,
        7.5e-5, 1.0e-4, 2.0e-4, 5.0e-4,
        7.5e-4, 1.0e-3, 2.0e-3, 5.0e-3, 1.0e-2
    ]

    rows: List[Dict[str, str]] = []
    for f in f_grid:
        # Simple power law with soft high-frequency taper to avoid huge values
        # h(f) = h0 * (f/f0)^alpha / (1 + (f/0.02)^2)  (0.02 Hz taper scale)
        taper = 1.0 + (f / 2.0e-2) ** 2
        h = h0 * (f / f0) ** alpha / taper

        # Assign a small fractional uncertainty for plotting/checks (10%)
        sigma = 0.1 * h

        rows.append({
            "f_Hz": f"{f:.6e}",
            "h_strain": f"{h:.6e}",
            "sigma_h": f"{sigma:.6e}",
            "source": "offline_representative"
        })
    return rows


def write_csv(path: str, rows: List[Dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["f_Hz", "h_strain", "sigma_h", "source"]
        )
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description="Create/overwrite data/gw_strain.csv with an offline representative h(f) spectrum.")
    ap.add_argument("--force", action="store_true", help="Overwrite existing CSV.")
    args = ap.parse_args()

    if os.path.exists(OUT_CSV) and not args.force:
        print(f"[gw_strain] Found existing file: {OUT_CSV} (use --force to overwrite).")
        return

    rows = generate_strain_rows()
    write_csv(OUT_CSV, rows)
    print(f"[gw_strain] Wrote {OUT_CSV} with {len(rows)} rows.")


if __name__ == "__main__":
    main()
