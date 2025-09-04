#!/usr/bin/env python3
"""
Build CRU figures from datasets in ./data/.
Outputs plots in ./figures/ for LaTeX \includegraphics.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Directories
DATA = Path("data")
FIGS = Path("figures")
TABLES = Path("tables")

FIGS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

# === 1. Gravitational Wave Prediction ===
def plot_gw_prediction():
    df = pd.read_csv(DATA / "gw_strain.csv")
    f = df["f_Hz"].values
    h = df["h_strain"].values

    plt.figure()
    plt.loglog(f, h, label="CRU prediction")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Strain $h$")
    plt.title("CRU Gravitational Wave Prediction")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.savefig(FIGS / "gw_prediction.pdf")
    plt.close()

# === 2. CMB Power Spectrum (TT only for now) ===
def plot_cmb_power():
    df_tt = pd.read_csv(DATA / "cmb_cl_TT.csv")
    ell = df_tt["ell"].values
    Cl = df_tt["Cl"].values

    plt.figure()
    plt.semilogy(ell, Cl, label="CRU prediction TT")
    plt.xlabel("Multipole $\\ell$")
    plt.ylabel("$C_\\ell$ [$\\mu K^2$]")
    plt.title("CRU CMB Power Spectrum (TT)")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.savefig(FIGS / "cmb_power_spectrum.pdf")
    plt.close()

# === 3. UHECR Spectrum ===
def plot_uhecr():
    df = pd.read_csv(DATA / "uhecr_flux.csv")
    E = df["log10E_eV"].values
    J = df["flux"].values

    plt.figure()
    plt.semilogy(E, J, "o-", label="Auger+CRU fit")
    plt.xlabel("log10(E/eV)")
    plt.ylabel("Flux [eV$^{-1}$ m$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    plt.title("UHECR Spectrum")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.savefig(FIGS / "uhecr_spectrum.pdf")
    plt.close()

# === Build all ===
def main():
    plot_gw_prediction()
    plot_cmb_power()
    plot_uhecr()

if __name__ == "__main__":
    main()
