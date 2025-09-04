import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_CSV = "./data/uhecr_flux.csv"
OUT_PDF  = "./figures/uhecr_spectrum.pdf"

def main():
    # Load dataset
    df = pd.read_csv(DATA_CSV)

    required_cols = {"log10E_eV", "flux", "sigma_stat", "sigma_sys"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"uhecr_flux.csv must have columns: {required_cols}")

    E = df["log10E_eV"].to_numpy()
    J = df["flux"].to_numpy()
    stat = df["sigma_stat"].to_numpy()
    sys = df["sigma_sys"].to_numpy()

    # Plot
    plt.figure(figsize=(7,5))
    plt.errorbar(E, J, yerr=stat, fmt="o", color="navy", label="UHECR flux (CRU data)")

    # Optional shaded systematics
    plt.fill_between(E, J - sys, J + sys, alpha=0.2, color="red", label="±sys")

    plt.yscale("log")
    plt.xlabel(r"$\log_{10}(E/\mathrm{eV})$")
    plt.ylabel(r"$J(E)$ [eV$^{-1}$ m$^{-2}$ s$^{-1}$ sr$^{-1}$]")
    plt.title("CRU Predicted UHECR Spectrum")
    plt.grid(True, which="both", ls="--", lw=0.5, alpha=0.6)
    plt.legend()
    plt.tight_layout()

    os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
    plt.savefig(OUT_PDF)
    print(f"Saved {OUT_PDF}")

if __name__ == "__main__":
    main()
