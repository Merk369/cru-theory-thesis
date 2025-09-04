#!/usr/bin/env python3
"""
Offline Auger UHECR data validator for CRU.

Checks local CSV in ./data:
  - uhecr_flux.csv (columns: log10E, J, stat, sys)

Outputs:
  - ./badges/auger_summary.json
  - ./badges/auger_summary.log

Exit code: 0 on success, nonzero if validation fails.
"""

from __future__ import annotations
from pathlib import Path
import sys
import json
import datetime as dt
import pandas as pd
import numpy as np

DATA = Path("data")
BADGES = Path("badges")
BADGES.mkdir(parents=True, exist_ok=True)

FILENAME = "uhecr_flux.csv"
REQUIRED_COLS = {"log10E", "J", "stat", "sys"}

def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    df = pd.read_csv(path)
    if not REQUIRED_COLS.issubset(df.columns):
        missing = REQUIRED_COLS - set(df.columns)
        raise ValueError(f"{path.name} missing columns: {sorted(missing)}")
    for col in REQUIRED_COLS:
        if not np.isfinite(df[col].values).all():
            raise ValueError(f"{path.name} has non-finite values in '{col}'")
    return df

def sanity_checks(df: pd.DataFrame) -> dict:
    E = df["log10E"].to_numpy()
    J = df["J"].to_numpy()
    stat = df["stat"].to_numpy()
    sys = df["sys"].to_numpy()

    # energy coverage
    span = (float(E.min()), float(E.max()))

    # monotonic falloff expectation
    monotonic = np.all(np.diff(J) <= 0)

    # error bars non-negative
    if (stat < 0).any() or (sys < 0).any():
        raise ValueError("Negative error bars detected")

    return {
        "E_span": span,
        "n_rows": len(df),
        "monotonic": bool(monotonic),
        "median_flux": float(np.median(J)),
    }

def main() -> int:
    timestamp = dt.datetime.utcnow().isoformat() + "Z"
    summary = {"timestamp_utc": timestamp, "passed": True, "files": [], "notes": []}
    log_lines = [f"[{timestamp}] Auger UHECR (offline) validation:"]

    try:
        path = DATA / FILENAME
        df = load_csv(path)
        info = sanity_checks(df)
        summary["files"].append(info)
        summary["passed"] &= info["monotonic"]
        status = "OK" if summary["passed"] else "FLAG"
        log_lines.append(
            f"  - {FILENAME}: {status} | E range {info['E_span'][0]:.1f}–{info['E_span'][1]:.1f}, "
            f"rows={info['n_rows']}, median_flux={info['median_flux']:.3g}"
        )
    except Exception as e:
        summary["passed"] = False
        summary["notes"].append(str(e))
        log_lines.append(f"  ! ERROR: {e}")

    # write artifacts
    (BADGES / "auger_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (BADGES / "auger_summary.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    # console echo
    print("\n".join(log_lines))
    print(f"\nSummary JSON: {BADGES/'auger_summary.json'}")
    print(f"Summary LOG : {BADGES/'auger_summary.log'}")

    return 0 if summary["passed"] else 2

if __name__ == "__main__":
    sys.exit(main())
