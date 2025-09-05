"""
Generate figures/cmb_power_spectrum.pdf from data/cmb_cl_TT.csv and data/cmb_cl_EE.csv

Expected CSV headers:
  - ell, Cl_TT   (for TT)
  - ell, Cl_EE   (for EE)

Both files must share the same 'ell' grid.
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_TT = Path("data/cmb_cl_TT.csv")
DATA_EE = Path("data/cmb_cl_EE.csv")
OUT = Path("figures/cmb_power_spectrum.pdf")

def main():
    tt = pd.read_csv(DATA_TT)
    ee = pd.read_csv(DATA_EE)

    for f, cols in [(tt, {"ell", "Cl_TT"}), (ee, {"ell", "Cl_EE"})]:
        missing = cols - set(f.columns)
        if missing:
            raise ValueError(f"Missing columns {missing} in file")

    if not (tt["ell"].equals(ee["ell"])):
        raise ValueError("ell grids differ between TT and EE files")

    ell = tt["ell"].values
    cl_tt = tt["Cl_TT"].values
    cl_ee = ee["Cl_EE"].values

    # Plot
    plt.figure(figsize=(7,4.2))
    plt.loglog(ell, cl_tt, label="TT")
    plt.loglog(ell, cl_ee, label="EE")
    plt.xlabel(r"Multipole $\ell$")
    plt.ylabel(r"$C_\ell$")
    plt.title("CMB Power Spectrum (TT, EE)")
    plt.legend()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(OUT, bbox_inches="tight")
    plt.close()
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
