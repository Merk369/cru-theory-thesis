#!/usr/bin/env python3
"""
Offline Planck data validator for CRU.

This script checks local CSVs in ./data:
  - cmb_cl_TT.csv  (columns: ell, Cl)
  - cmb_cl_EE.csv  (columns: ell, Cl)

Outputs:
  - ./badges/planck_summary.json
  - ./badges/planck_summary.log

Exit code is 0 on success; nonzero on validation failure.
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

REQUIRED = {
    "cmb_cl_TT.csv": {"ell", "Cl"},
    "cmb_cl_EE.csv": {"ell", "Cl"},
}

def load_csv(path: Path, required_cols: set[str]) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    df = pd.read_csv(path)
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        raise ValueError(f"{path.name} missing columns: {sorted(missing)}")
    # type and finiteness checks
    for col in required_cols:
        if not np.isfinite(df[col].values).all():
            raise ValueError(f"{path.name} contains non-finite values in '{col}'")
    return df

def sanity_checks(df: pd.DataFrame, name: str) -> dict:
    ell = df["ell"].to_numpy()
    Cl  = df["Cl"].to_numpy()

    if (ell < 2).any():
        raise ValueError(f"{name}: ell must start at >=2 (got min {ell.min()})")

    # coverage
    span = (int(ell.min()), int(ell.max()))
    count = len(ell)

    # simple ordering/duplicates check
    if not np.all(np.diff(ell) > 0):
        raise ValueError(f"{name}: ell must be strictly increasing")

    # basic smoothness: finite differences should not be wildly oscillatory
    d = np.diff(Cl)
    # Robust scale with MAD
    mad = np.median(np.abs(d - np.median(d))) + 1e-32
    outlier_frac = np.mean(np.abs(d - np.median(d)) > 20 * mad)

    # no negative power (Planck Cls can be tiny but not negative)
    neg_frac = np.mean(Cl < 0)

    return {
        "name": name,
        "ell_span": span,
        "n_rows": count,
        "outlier_frac": float(outlier_frac),
        "neg_frac": float(neg_frac),
        "median_Cl": float(np.median(Cl)),
    }

def main() -> int:
    timestamp = dt.datetime.utcnow().isoformat() + "Z"
    summary = {"timestamp_utc": timestamp, "files": [], "passed": True, "notes": []}
    log_lines = [f"[{timestamp}] Planck (offline) validation:"]

    try:
        for fname, cols in REQUIRED.items():
            path = DATA / fname
            df = load_csv(path, cols)
            info = sanity_checks(df, fname)
            summary["files"].append(info)
            # accept extremely small negative fractions due to numerical noise if present
            ok = (info["outlier_frac"] < 0.20) and (info["neg_frac"] <= 0.0 + 1e-15)
            summary["passed"] &= ok
            status = "OK" if ok else "FLAG"
            log_lines.append(
                f"  - {fname}: {status} | ell {info['ell_span'][0]}–{info['ell_span'][1]}, "
                f"rows={info['n_rows']}, outlier_frac={info['outlier_frac']:.3f}, "
                f"neg_frac={info['neg_frac']:.3g}"
            )
    except Exception as e:
        summary["passed"] = False
        summary["notes"].append(str(e))
        log_lines.append(f"  ! ERROR: {e}")

    # Write artifacts
    (BADGES / "planck_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (BADGES / "planck_summary.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    # Console echo
    print("\n".join(log_lines))
    print(f"\nSummary JSON: {BADGES/'planck_summary.json'}")
    print(f"Summary LOG : {BADGES/'planck_summary.log'}")

    return 0 if summary["passed"] else 2

if __name__ == "__main__":
    sys.exit(main())
