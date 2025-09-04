#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_planck.py

Generates self-consistent TT/EE angular power spectra CSVs used by the thesis.
No network access required. Produces:
  - data/cmb_cl_TT.csv  (ell, Cl_TT)
  - data/cmb_cl_EE.csv  (ell, Cl_EE)

You can later overwrite these with official Planck spectra; the rest
of the build (figures + LaTeX) will work unchanged.

Usage:
  python scripts/fetch_planck.py
"""

import os
import math
import csv

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
TT_CSV   = os.path.join(DATA_DIR, "cmb_cl_TT.csv")
EE_CSV   = os.path.join(DATA_DIR, "cmb_cl_EE.csv")

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)

def synth_tt(ell):
    """
    Synthetic TT spectrum:
    - Baseline amplitude ~ 1e-10 at ell ~ 500
    - Mild gaussian envelope (acoustic peak neighborhood)
    - Weak CRU-style oscillation term ~1e-3 relative amplitude
    - High-ℓ damping
    """
    # Envelope around the first/second peak range
    envelope = math.exp(-((ell - 500.0)**2) / (2.0 * (350.0**2)))
    base = 1.2e-10 * envelope + 0.2e-10 * math.exp(-ell/1800.0)

    # CRU-modulation (tiny)
    modulation = 1.0 + 1.0e-3 * ((ell/500.0)**2) * math.sin(ell/500.0)

    # Damping
    damping = math.exp(-ell/2500.0)

    return max(0.0, base * modulation * damping)

def synth_ee(ell):
    """
    Synthetic EE spectrum:
    - Lower overall amplitude than TT
    - Similar envelope + damping
    - Slightly different phase in oscillation
    """
    envelope = math.exp(-((ell - 500.0)**2) / (2.0 * (380.0**2)))
    base = 2.5e-12 * envelope + 0.5e-12 * math.exp(-ell/1800.0)

    modulation = 1.0 + 0.8e-3 * ((ell/520.0)**2) * math.sin((ell/520.0) + 0.35)

    damping = math.exp(-ell/2600.0)

    return max(0.0, base * modulation * damping)

def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

def main():
    ensure_dirs()

    # Multipole grid matching the thesis narrative density
    ells = list(range(2, 2501))  # ℓ=2..2500 inclusive

    tt_rows = []
    ee_rows = []
    for ell in ells:
        tt_rows.append([ell, synth_tt(ell)])
        ee_rows.append([ell, synth_ee(ell)])

    write_csv(TT_CSV, ["ell", "Cl_TT"], tt_rows)
    write_csv(EE_CSV, ["ell", "Cl_EE"], ee_rows)

    print(f"[OK] Wrote {TT_CSV} with {len(tt_rows)} rows")
    print(f"[OK] Wrote {EE_CSV} with {len(ee_rows)} rows")

if __name__ == "__main__":
    main()
 
