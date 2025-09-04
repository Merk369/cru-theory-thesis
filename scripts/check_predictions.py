#!/usr/bin/env python3
"""
Run technical CRU checks against local datasets and emit a PASS/FAIL badge.

Inputs (CSV files expected in ./data):
  - gw_strain.csv         columns: f_Hz, h_strain
  - cmb_cl_TT.csv         columns: ell, Cl
  - uhecr_flux.csv        columns: log10E_eV, flux
  - dm_limits.csv         (optional) columns: mass_GeV, sigma_SI_cm2, limit_SI_cm2

Outputs (in ./badges):
  - checks.json           machine-readable summary
  - checks.log            human-readable log
  - cru_checks.svg        badge (green=PASS / red=FAIL)
"""

from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
import pandas as pd
import math
import datetime as dt

DATA = Path("data")
BADGES = Path("badges")
BADGES.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Utility: badge SVG generator
# ----------------------------
def write_badge(svg_path: Path, label: str, status: str, ok: bool) -> None:
    """
    Minimal self-contained SVG badge (no deps).
    """
    label_text = label
    status_text = status
    # Widths approximated for monospace; tweak if desired
    label_w = 6 * len(label_text) + 20
    status_w = 6 * len(status_text) + 20
    total_w = label_w + status_w
    height = 20

    color = "#4c1" if ok else "#e05d44"  # green / red
    label_bg = "#555"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{height}" role="img" aria-label="{label_text}: {status_text}">
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="m">
    <rect width="{total_w}" height="{height}" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#m)">
    <rect width="{label_w}" height="{height}" fill="{label_bg}"/>
    <rect x="{label_w}" width="{status_w}" height="{height}" fill="{color}"/>
    <rect width="{total_w}" height="{height}" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle"
     font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="{label_w/2}" y="14">{label_text}</text>
    <text x="{label_w + status_w/2}" y="14">{status_text}</text>
  </g>
</svg>
"""
    svg_path.write_text(svg, encoding="utf-8")

# ----------------------------
# Check result container
# ----------------------------
@dataclass
class CheckResult:
    name: str
    passed: bool
    details: str

# ----------------------------
# Individual checks
# ----------------------------
def check_gw_strain(path: Path) -> CheckResult:
    """
    Sanity check: CRU predicts ~1e-22 at ~1e-3 Hz order-of-magnitude.
    We verify that at 1 mHz, h is within [3e-23, 3e-22].
    """
    try:
        df = pd.read_csv(path)
        # find nearest to 1e-3 Hz
        target = 1e-3
        idx = (df["f_Hz"] - target).abs().idxmin()
        f = float(df.iloc[idx]["f_Hz"])
        h = float(df.iloc[idx]["h_strain"])
        lo, hi = 3e-23, 3e-22
        ok = (h >= lo) and (h <= hi)
        return CheckResult(
            name="GW@1mHz",
            passed=ok,
            details=f"Nearest f={f:.3e} Hz, h={h:.3e}; expected in [{lo:.1e},{hi:.1e}]"
        )
    except Exception as e:
        return CheckResult("GW@1mHz", False, f"Error: {e}")

def check_cmb_feature(path: Path) -> CheckResult:
    """
    Check for a small oscillatory feature around ell~500 at ~1e-3 relative level.
    We compute local slope changes across a window and ensure modulation depth
    is ~ O(1e-3) compared to the baseline in that region.
    """
    try:
        df = pd.read_csv(path)
        ell = df["ell"].values
        Cl = df["Cl"].values

        # focus window near l~500
        w = (ell >= 450) & (ell <= 550)
        if w.sum() < 10:
            return CheckResult("CMB_l~500", False, "Insufficient samples near ell~500")

        base = np.median(Cl[w])
        # rough modulation depth: max deviation in window relative to local median
        dev = np.max(np.abs(Cl[w] - base)) / max(base, 1e-20)
        # Expect around 1e-3; accept [3e-4, 5e-3] to allow dataset noise
        ok = (dev >= 3e-4) and (dev <= 5e-3)
        return CheckResult(
            name="CMB_l~500",
            passed=ok,
            details=f"Median Cl~{base:.3e}, relative modulation depth~{dev:.2e} (target ~1e-3)"
        )
    except Exception as e:
        return CheckResult("CMB_l~500", False, f"Error: {e}")

def check_uhecr_cutoff(path: Path) -> CheckResult:
    """
    Verify the UHECR flux shows a suppression above ~5e19 eV (~log10E=19.7).
    We compare median flux below vs. above 19.7 and require a drop >= factor 5.
    """
    try:
        df = pd.read_csv(path)
        E = df["log10E_eV"].values
        J = df["flux"].values

        below = (E >= 19.0) & (E < 19.7)
        above = (E >= 19.7) & (E <= 20.3)

        if below.sum() < 3 or above.sum() < 2:
            return CheckResult("UHECR_cutoff", False, "Insufficient bins around cutoff")

        med_below = float(np.median(J[below]))
        med_above = float(np.median(J[above]))
        # Expect clear suppression
        ratio = med_below / max(med_above, 1e-99)
        ok = ratio >= 5.0
        return CheckResult(
            name="UHECR_cutoff",
            passed=ok,
            details=f"Median below={med_below:.3e}, above={med_above:.3e}, ratio={ratio:.2f} (>=5 passes)"
        )
    except Exception as e:
        return CheckResult("UHECR_cutoff", False, f"Error: {e}")

def check_dm_limits(path: Path) -> CheckResult:
    """
    Optional: ensure predicted cross-sections (sigma_SI_cm2) sit below the provided
    experimental limits (limit_SI_cm2) across the mass range.

    If file is missing, we mark as 'skipped' but do NOT fail global status.
    """
    if not path.exists():
        return CheckResult("DM_limits", True, "Skipped (dm_limits.csv not present)")
    try:
        df = pd.read_csv(path)
        if not {"mass_GeV", "sigma_SI_cm2", "limit_SI_cm2"} <= set(df.columns):
            return CheckResult("DM_limits", False, "Missing required columns")
        ok = bool(np.all(df["sigma_SI_cm2"].values <= df["limit_SI_cm2"].values))
        viol = int(np.sum(df["sigma_SI_cm2"].values > df["limit_SI_cm2"].values))
        return CheckResult(
            name="DM_limits",
            passed=ok,
            details="All masses under limits" if ok else f"{viol} mass points exceed limits"
        )
    except Exception as e:
        return CheckResult("DM_limits", False, f"Error: {e}")

# ----------------------------
# Main
# ----------------------------
def main():
    results = []
    results.append(check_gw_strain(DATA / "gw_strain.csv"))
    results.append(check_cmb_feature(DATA / "cmb_cl_TT.csv"))
    results.append(check_uhecr_cutoff(DATA / "uhecr_flux.csv"))
    results.append(check_dm_limits(DATA / "dm_limits.csv"))

    passed_all = all(r.passed for r in results)

    # Write logs
    timestamp = dt.datetime.utcnow().isoformat() + "Z"
    log_lines = [f"[{timestamp}] CRU checks:"]
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        log_lines.append(f"  - {r.name}: {status} — {r.details}")
    (BADGES / "checks.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    # Write JSON
    payload = {
        "timestamp_utc": timestamp,
        "passed_all": passed_all,
        "results": [asdict(r) for r in results],
    }
    (BADGES / "checks.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # Write badge
    write_badge(BADGES / "cru_checks.svg", label="CRU", status=("PASS" if passed_all else "FAIL"), ok=passed_all)

    print("\n".join(log_lines))
    print(f"\nBadge written to {BADGES/'cru_checks.svg'}")
    print(f"JSON  written to {BADGES/'checks.json'}")
    print(f"Log   written to {BADGES/'checks.log'}")

if __name__ == "__main__":
    main()
