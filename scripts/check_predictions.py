#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_predictions.py

Runs offline pass/fail checks against the data/ CSVs to validate headline
predictions of the CRU (technical) thesis. Outputs:

  - badges/cru_checks.svg     (overall PASS/FAIL badge)
  - logs/checks_report.md     (detailed report)
  - process exit code: 0 if pass (or all checks skipped), 1 on any failure

Checks (performed only if the corresponding CSV exists):
  1) UHECR suppression (GZK): J(10^20 eV) is sufficiently below J(10^19.6 eV)
  2) GW level near 1 mHz (10^-3 Hz) is within an expected envelope
  3) CMB angular power spectrum (TT) is well-formed: positive and broadly decreasing over ℓ≈500–2500

Usage:
  python scripts/check_predictions.py
"""

import os
import sys
import csv
import math
from typing import List, Tuple, Dict

# Paths
ROOT      = os.path.dirname(os.path.dirname(__file__))
DATA_DIR  = os.path.join(ROOT, "data")
BADGE_DIR = os.path.join(ROOT, "badges")
LOGS_DIR  = os.path.join(ROOT, "logs")

UHECR_CSV = os.path.join(DATA_DIR, "uhecr_flux.csv")
GW_CSV    = os.path.join(DATA_DIR, "gw_strain.csv")
CMB_TT    = os.path.join(DATA_DIR, "cmb_cl_TT.csv")

BADGE_OUT = os.path.join(BADGE_DIR, "cru_checks.svg")
REPORT_MD = os.path.join(LOGS_DIR, "checks_report.md")


# ----------------------------
# Utilities
# ----------------------------

def ensure_dirs():
    os.makedirs(BADGE_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)


def read_csv_columns(path: str, required_cols: List[str]) -> List[Dict[str, str]]:
    with open(path, "r", newline="") as f:
        r = csv.DictReader(f)
        for col in required_cols:
            if col not in r.fieldnames:
                raise ValueError(f"File {path} missing required column '{col}'. Found: {r.fieldnames}")
        return list(r)


def nearest_index(values: List[float], target: float) -> int:
    return min(range(len(values)), key=lambda i: abs(values[i] - target))


def write_badge(passing: bool, label: str = "CRU checks") -> None:
    # Minimal inline SVG badge (shields-like style)
    color = "#4c1" if passing else "#e05d44"
    text  = "passing" if passing else "failing"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="110" height="20" role="img" aria-label="{label}: {text}">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="110" height="20" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <rect width="70" height="20" fill="#555"/>
    <rect x="70" width="40" height="20" fill="{color}"/>
    <rect width="110" height="20" fill="url(#b)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="35" y="15">{label}</text>
    <text x="90" y="15">{text}</text>
  </g>
</svg>
"""
    with open(BADGE_OUT, "w", encoding="utf-8") as f:
        f.write(svg)


def write_report(md: str) -> None:
    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write(md)


# ----------------------------
# Checks
# ----------------------------

def check_uhecr_suppression() -> Tuple[str, bool, str]:
    """
    Expectation: UHECR flux is suppressed above the GZK scale.
    Conservative rule of thumb:

      Let E1 = 10^19.6 eV, E2 = 10^20.0 eV.
      Require J(E2) <= 0.3 * J(E1)

    Uses columns: log10E, J, sigma_stat, sigma_sys (last two only read, not used).
    """
    if not os.path.exists(UHECR_CSV):
        return ("UHECR suppression", True, "SKIPPED (data/uhecr_flux.csv not found)")

    rows = read_csv_columns(UHECR_CSV, ["log10E", "J"])
    log10E = [float(r["log10E"]) for r in rows]
    J = [float(r["J"]) for r in rows]

    # Find nearest to 19.6 and 20.0
    i1 = nearest_index(log10E, 19.6)
    i2 = nearest_index(log10E, 20.0)

    J1 = J[i1]
    J2 = J[i2]

    if J1 <= 0 or J2 <= 0:
        return ("UHECR suppression", False, f"FAIL: non-positive flux values (J1={J1}, J2={J2}).")

    ratio = J2 / J1
    passed = ratio <= 0.30  # conservative suppression requirement

    detail = (
        f"E1≈10^19.6 eV: J1={J1:.3e}\n"
        f"E2≈10^20.0 eV: J2={J2:.3e}\n"
        f"ratio J(E2)/J(E1)={ratio:.3f} (threshold ≤ 0.30) → {'PASS' if passed else 'FAIL'}"
    )
    return ("UHECR suppression", passed, detail)


def check_gw_level() -> Tuple[str, bool, str]:
    """
    Expectation: Around f ≈ 1e-3 Hz, SGWB strain amplitude h is ~1e-22 ± order-of-mag.
    Conservative envelope: 5e-24 ≤ h(f≈1e-3 Hz) ≤ 5e-21 (lenient 1/20x – 50x).

    Uses columns: f, h, (optional) sigma_h
    """
    if not os.path.exists(GW_CSV):
        return ("GW level", True, "SKIPPED (data/gw_strain.csv not found)")

    rows = read_csv_columns(GW_CSV, ["f", "h"])
    f = [float(r["f"]) for r in rows]
    h = [float(r["h"]) for r in rows]

    idx = nearest_index(f, 1.0e-3)
    f0, h0 = f[idx], h[idx]

    lower, upper = 5e-24, 5e-21
    passed = (lower <= h0 <= upper)

    detail = (
        f"Nearest to 1e-3 Hz → f={f0:.3e} Hz, h={h0:.3e}\n"
        f"Allowed envelope: [{lower:.1e}, {upper:.1e}] → {'PASS' if passed else 'FAIL'}"
    )
    return ("GW level", passed, detail)


def check_cmb_well_formed() -> Tuple[str, bool, str]:
    """
    Expectation: TT spectrum C_ell (ℓ ~ 500–2500) should be positive and broadly decreasing.
    We implement two basic sanity checks:

      1) All Cℓ > 0 for ℓ ∈ [500, 2500]
      2) Median of Cℓ(ℓ>1000) < Median of Cℓ(ℓ∈[500,800])

    Uses columns: ell, Cl
    """
    if not os.path.exists(CMB_TT):
        return ("CMB TT well-formed", True, "SKIPPED (data/cmb_cl_TT.csv not found)")

    rows = read_csv_columns(CMB_TT, ["ell", "Cl"])
    ell = [float(r["ell"]) for r in rows]
    Cl  = [float(r["Cl"]) for r in rows]

    # Focus window
    window = [(L, C) for L, C in zip(ell, Cl) if 500 <= L <= 2500]
    if len(window) < 20:
        return ("CMB TT well-formed", False, "FAIL: insufficient samples in 500≤ℓ≤2500.")

    Lw, Cw = zip(*window)

    # Check positivity
    if any(c <= 0 for c in Cw):
        return ("CMB TT well-formed", False, "FAIL: non-positive Cℓ values in 500≤ℓ≤2500.")

    # Compare medians between two sub-bands
    band_lo = [c for L, c in window if 500 <= L <= 800]
    band_hi = [c for L, c in window if 1000 <= L <= 2500]

    if len(band_lo) == 0 or len(band_hi) == 0:
        return ("CMB TT well-formed", False, "FAIL: not enough points in comparison bands.")

    def median(xs: List[float]) -> float:
        s = sorted(xs)
        n = len(s)
        if n % 2 == 1:
            return s[n // 2]
        return 0.5 * (s[n // 2 - 1] + s[n // 2])

    m_lo = median(band_lo)
    m_hi = median(band_hi)

    passed = m_hi < m_lo  # broadly decreasing

    detail = (
        f"Median Cℓ[500–800]={m_lo:.3e}, Median Cℓ[1000–2500]={m_hi:.3e}\n"
        f"Require high-ℓ median < low-ℓ median → {'PASS' if passed else 'FAIL'}"
    )
    return ("CMB TT well-formed", passed, detail)


# ----------------------------
# Main
# ----------------------------

def main():
    ensure_dirs()

    checks = [
        check_uhecr_suppression(),
        check_gw_level(),
        check_cmb_well_formed(),
    ]

    # Compose report
    lines = ["# CRU Technical Thesis — Automated Checks\n"]
    passed_all = True
    any_executed = False

    for name, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        if "SKIPPED" in detail:
            status = "SKIP"
        else:
            any_executed = True
        lines.append(f"## {name}: **{status}**\n")
        lines.append("```\n" + detail + "\n```\n")
        if not ok and "SKIPPED" not in detail:
            passed_all = False

    if not any_executed:
        # If nothing ran (all skipped), treat as pass but make it clear.
        lines.append("> All checks skipped (no datasets found). Treating as PASS for CI.\n")
        passed_all = True

    write_report("\n".join(lines))
    write_badge(passed_all)

    print(f"[REPORT] {REPORT_MD}")
    print(f"[BADGE ] {BADGE_OUT}")
    print(f"[RESULT] {'PASS' if passed_all else 'FAIL'}")

    sys.exit(0 if passed_all else 1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Robust error: still try to emit a FAIL badge + report
        ensure_dirs()
        write_badge(False)
        write_report(f"# CRU Technical Thesis — Automated Checks\n\n**ERROR:** {e}\n")
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
