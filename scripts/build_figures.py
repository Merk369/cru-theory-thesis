#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_figures.py

Reads CSVs in ./data and generates publication-ready figures in ./figures:
  - figures/uhecr_spectrum.pdf      (from data/uhecr_flux.csv)
  - figures/gw_prediction.pdf       (from data/gw_strain.csv)
  - figures/cmb_power_spectrum.pdf  (from data/cmb_cl_TT.csv [+ optional EE])

Usage:
  python scripts/build_figures.py
"""

import os
import sys
import csv
from typing import List, Tuple

import matplotlib
matplotlib.use("Agg")  # headless save
import matplotlib.pyplot as plt

ROOT     = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, "data")
FIG_DIR  = os.path.join(ROOT, "figures")

UHECR_CSV = os.path.join(DATA_DIR, "uhecr_flux.csv")
GW_CSV    = os.path.join(DATA_DIR, "gw_strain.csv")
CMB_TT    = os.path.join(DATA_DIR, "cmb_cl_TT.csv")
CMB_EE    = os.path.join(DATA_DIR, "cmb_cl_EE.csv")  # optional

UHECR_FIG = os.path.join(FIG_DIR, "uhecr_spectrum.pdf")
GW_FIG    = os.path.join(FIG_DIR, "gw_prediction.pdf")
CMB_FIG   = os.path.join(FIG_DIR, "cmb_power_spectrum.pdf")


def ensure_dirs():
    os.makedirs(FIG_DIR, exist_ok=True)


def read_uhecr_csv(path: str) -> Tuple[List[float], List[float], List[float], List[float]]:
    log10E, J, s_stat, s_sys = [], [], [], []
    with open(path, "r") as f:
        r = csv.DictReader(f)
        for row in r:
            log10E.append(float(row["log10E"]))
            J.append(float(row["J"]))
            s_stat.append(float(row["sigma_stat"]))
            s_sys.append(float(row["sigma_sys"]))
    return log10E, J, s_stat, s_sys


def read_gw_csv(path: str) -> Tuple[List[float], List[float], List[float]]:
    freq, h, sig = [], [], []
    with open(path, "r") as f:
        r = csv.DictReader(f)
        # Expected columns: f, h, sigma_h
        for row in r:
            freq.append(float(row["f"]))
            h.append(float(row["h"]))
            # sigma_h may be absent; handle gracefully
            if "sigma_h" in row and row["sigma_h"] not in ("", None):
                sig.append(float(row["sigma_h"]))
            else:
                sig.append(0.0)
    return freq, h, sig


def read_cmb_csv(path: str) -> Tuple[List[float], List[float]]:
    ell, cl = [], []
    with open(path, "r") as f:
        r = csv.DictReader(f)
        # Expected columns: ell, Cl
        for row in r:
            ell.append(float(row["ell"]))
            cl.append(float(row["Cl"]))
    return ell, cl


def plot_uhecr():
    if not os.path.exists(UHECR_CSV):
        print(f"[WARN] Missing {UHECR_CSV}; skipping UHECR figure.")
        return

    log10E, J, s_stat, s_sys = read_uhecr_csv(UHECR_CSV)
    # total uncertainty (quadrature)
    s_tot = [(ss**2 + sy**2) ** 0.5 for ss, sy in zip(s_stat, s_sys)]
    E = [10.0 ** x for x in log10E]

    plt.figure(figsize=(6, 4.2))
    # error bars in log-log space; matplotlib handles if values >0
    plt.errorbar(E, J, yerr=s_tot, fmt="o", capsize=3, linewidth=1, markersize=4)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel(r"Energy $E$ (eV)")
    plt.ylabel(r"Flux $J(E)$ (eV$^{-1}$ m$^{-2}$ s$^{-1}$ sr$^{-1}$)")
    plt.title("UHECR Spectrum (binned)")
    plt.grid(True, which="both", linestyle=":", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(UHECR_FIG)
    plt.close()
    print(f"[OK] Wrote {UHECR_FIG}")


def plot_gw():
    if not os.path.exists(GW_CSV):
        print(f"[WARN] Missing {GW_CSV}; skipping GW figure.")
        return

    f, h, s = read_gw_csv(GW_CSV)

    plt.figure(figsize=(6, 4.2))
    # If sigma present and nonzero, show error bars
    if any(x > 0 for x in s):
        plt.errorbar(f, h, yerr=s, fmt="-", linewidth=1)
    else:
        plt.plot(f, h, "-")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Strain")
    plt.title("Stochastic Gravitational-Wave Background (CRU)")
    plt.grid(True, which="both", linestyle=":", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(GW_FIG)
    plt.close()
    print(f"[OK] Wrote {GW_FIG}")


def plot_cmb():
    if not os.path.exists(CMB_TT):
        print(f"[WARN] Missing {CMB_TT}; skipping CMB figure.")
        return

    ell_TT, cl_TT = read_cmb_csv(CMB_TT)

    plt.figure(figsize=(6.4, 4.2))
    plt.plot(ell_TT, cl_TT, "-", label="TT")

    if os.path.exists(CMB_EE):
        ell_EE, cl_EE = read_cmb_csv(CMB_EE)
        plt.plot(ell_EE, cl_EE, "--", label="EE")

    plt.xlabel(r"Multipole $\ell$")
    plt.ylabel(r"$C_\ell$ (sr$^{-1}$)")
    plt.title("CMB Angular Power Spectrum")
    plt.yscale("log")
    plt.xlim(left=max(2, min(ell_TT)))
    plt.grid(True, which="both", linestyle=":", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(CMB_FIG)
    plt.close()
    print(f"[OK] Wrote {CMB_FIG}")


def main():
    ensure_dirs()
    plot_uhecr()
    plot_gw()
    plot_cmb()
    print("[DONE] All available figures built.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
