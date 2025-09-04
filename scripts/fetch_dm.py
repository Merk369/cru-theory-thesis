#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_dm.py

Purpose
-------
Populate data/dm_limits.csv with a compact, offline, representative set of
spin-independent WIMP–nucleon limits suitable for figures and checks in the
CRU technical thesis. This avoids network access and produces stable builds.

Behavior
--------
- If data/dm_limits.csv does NOT exist, it is created with curated rows.
- If it exists, the script exits without modifying it, unless --force is given.

CSV schema
----------
m_GeV,sigma_SI_cm2,experiment,year,source

Usage
-----
python scripts/fetch_dm.py           # create if missing
python scripts/fetch_dm.py --force   # overwrite
"""

import os
import csv
import argparse
from typing import List, Dict

ROOT     = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, "data")
OUT_CSV  = os.path.join(DATA_DIR, "dm_limits.csv")


def representative_rows() -> List[Dict[str, str]]:
    """
    Returns a compact, monotone set of (mass, sigma) points in the ballpark of
    recent SI limits (illustrative, offline). Values chosen to be plausible for
    plotting and pass/fail checks without claiming exact experimental numbers.

    If you later want to replace these with real datasets, keep the same schema.
    """
    rows = [
        # m_GeV,   sigma_SI_cm2,    experiment,  year, source
        {"m_GeV": "6",    "sigma_SI_cm2": "5.0e-42", "experiment": "SuperCDMS-like", "year": "2020", "source": "offline_representative"},
        {"m_GeV": "10",   "sigma_SI_cm2": "8.0e-44", "experiment": "CRESST-like",    "year": "2021", "source": "offline_representative"},
        {"m_GeV": "30",   "sigma_SI_cm2": "2.0e-46", "experiment": "XENONnT-like",   "year": "2022", "source": "offline_representative"},
        {"m_GeV": "50",   "sigma_SI_cm2": "1.2e-46", "experiment": "LZ-like",        "year": "2022", "source": "offline_representative"},
        {"m_GeV": "100",  "sigma_SI_cm2": "8.0e-47", "experiment": "LZ-like",        "year": "2023", "source": "offline_representative"},
        {"m_GeV": "200",  "sigma_SI_cm2": "1.5e-46", "experiment": "PandaX-like",    "year": "2021", "source": "offline_representative"},
        {"m_GeV": "500",  "sigma_SI_cm2": "3.0e-46", "experiment": "XENONnT-like",   "year": "2022", "source": "offline_representative"},
        {"m_GeV": "1000", "sigma_SI_cm2": "6.0e-46", "experiment": "LZ-like",        "year": "2023", "source": "offline_representative"},
    ]
    return rows


def write_csv(path: str, rows: List[Dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["m_GeV", "sigma_SI_cm2", "experiment", "year", "source"]
        )
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description="Create/overwrite data/dm_limits.csv with offline representative SI limits.")
    ap.add_argument("--force", action="store_true", help="Overwrite existing CSV.")
    args = ap.parse_args()

    if os.path.exists(OUT_CSV) and not args.force:
        print(f"[dm_limits] Found existing file: {OUT_CSV} (use --force to overwrite).")
        return

    rows = representative_rows()
    write_csv(OUT_CSV, rows)
    print(f"[dm_limits] Wrote {OUT_CSV} with {len(rows)} rows.")


if __name__ == "__main__":
    main()
