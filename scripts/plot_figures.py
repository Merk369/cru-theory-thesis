#!/usr/bin/env python3
"""
plot_figures.py
Reads datasets from ./data and writes publication figures into ./figures.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

FIG = Path("figures")
FIG.mkdir(parents=True, exist_ok=True)

# 1) GW strain
gw = pd.read_csv("data/gw_strain.csv")
plt.figure()
plt.loglog(gw["frequency_hz"], gw["strain"])
plt.xlabel("Frequency (Hz)")
plt.ylabel("Strain")
plt.title("CRU GW Prediction")
plt.grid(True, which="both", ls=":")
plt.tight_layout()
plt.savefig(FIG / "gw_prediction.pdf")
plt.close()

# 2) UHECR flux
uhe = pd.read_csv("data/uhecr_flux.csv")
E = 10**uhe["log10_E_eV"].values
plt.figure()
plt.loglog(E, uhe["J_eV_m2_s_sr_inv"])
plt.xlabel("Energy (eV)")
plt.ylabel(r"$J(E)$ (eV$^{-1}$ m$^{-2}$ s$^{-1}$ sr$^{-1}$)")
plt.title("UHECR Flux (CRU fit)")
plt.grid(True, which="both", ls=":")
plt.tight_layout()
plt.savefig(FIG / "uhecr_flux.pdf")
plt.close()

# 3) CMB C_ell
cmb = pd.read_csv("data/cmb_cl_l500_2500.csv")
plt.figure()
plt.semilogy(cmb["ell"], cmb["C_ell_sr_inv"])
plt.xlabel(r"Multipole $\ell$")
plt.ylabel(r"$C_\ell$ (sr$^{-1}$)")
plt.title("CMB Power Spectrum (CRU imprint)")
plt.grid(True, ls=":")
plt.tight_layout()
plt.savefig(FIG / "cmb_power_spectrum.pdf")
plt.close()

print("Figures written to ./figures")
