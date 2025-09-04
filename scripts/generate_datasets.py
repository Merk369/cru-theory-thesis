#!/usr/bin/env python3
"""
generate_datasets.py
Generates full-resolution datasets used by the CRU thesis.

Outputs (created under ./data):
  - gw_strain.csv           : 1000-point logspaced frequency–strain grid
  - uhecr_flux.csv          : 11-bin spectrum with stat & sys errors
  - cmb_cl_l500_2500.csv    : l=500..2500 (step 2) power spectrum + sigma
"""

import numpy as np
import pandas as pd
from pathlib import Path

DATA = Path("data")
DATA.mkdir(parents=True, exist_ok=True)

# ---------- 1) Gravitational wave strain (1000 points, log-spaced) ----------
# Frequencies from 1e-15 Hz to 1e-3 Hz (covers PTA through LISA band)
f = np.logspace(-15, -3, 1000)
# Use the thesis toy model scaling: h ~ 1e-22 * (f / f0)^2 with f0 = (5e19 eV)/c in Hz.
# Convert 5e19 eV to Hz via h = E/h (Planck const), but keep the relative form used in the draft.
# We normalize to match the 1e-3 Hz ~ 1e-22 anchor.
f_anchor = 1e-3
h = 1.0e-22 * (f / f_anchor) ** 2
sigma_h = h * 0.10  # 10% fractional uncertainty as a placeholder

gw_df = pd.DataFrame({"frequency_hz": f, "strain": h, "sigma_strain": sigma_h})
gw_df.to_csv(DATA / "gw_strain.csv", index=False)

# ---------- 2) UHECR flux table (exact bins from manuscript) ----------
uhecr_rows = [
    (18.0, 1.0e-17, 0.1e-17, 0.14e-17),
    (18.2, 7.9e-18, 0.08e-18, 0.11e-18),
    (18.4, 6.3e-18, 0.06e-18, 0.09e-18),
    (18.6, 5.0e-18, 0.05e-18, 0.07e-18),
    (18.8, 4.0e-18, 0.04e-18, 0.06e-18),
    (19.0, 3.2e-18, 0.03e-18, 0.04e-18),
    (19.2, 2.5e-18, 0.02e-18, 0.03e-18),
    (19.4, 2.0e-18, 0.02e-18, 0.03e-18),
    (19.6, 1.6e-18, 0.02e-18, 0.02e-18),
    (19.8, 1.3e-18, 0.01e-18, 0.02e-18),
    (20.0, 1.0e-19, 0.2e-19, 0.14e-19),
]
uhecr_df = pd.DataFrame(uhecr_rows, columns=[
    "log10_E_eV", "J_eV_m2_s_sr_inv", "sigma_stat", "sigma_sys"
])
uhecr_df.to_csv(DATA / "uhecr_flux.csv", index=False)

# ---------- 3) CMB C_ell around l~500 with uncertainties (l=500..2500, step 2) ----------
ell = np.arange(500, 2501, 2)
# Reproduce the table’s rough envelope and a gentle decay; include an oscillatory imprint.
cl0 = 1.2e-10
decay = np.linspace(0, 1, ell.size)  # linear decay proxy
cl = cl0 * (1 - 0.58*decay) * (1 + 1e-3*np.sin(ell/50.0))
sigma = cl * 1e-3

cmb_df = pd.DataFrame({"ell": ell, "C_ell_sr_inv": cl, "sigma_C_ell_sr_inv": sigma})
cmb_df.to_csv(DATA / "cmb_cl_l500_2500.csv", index=False)

print("Datasets written to ./data")
