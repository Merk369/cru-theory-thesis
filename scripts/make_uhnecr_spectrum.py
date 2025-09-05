"""
Generate figures/unhecr_spectrum.pdf from data/unhecr_flux.csv

Expected CSV headers:
  - energy_eV
  - flux
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA = Path("data/unhecr_flux.csv")
OUT = Path("figures/unhecr_spectrum.pdf")

def main():
    df = pd.read_csv(DATA)
    for col in ["energy_eV", "flux"]:
        if col not in df.columns:
            raise ValueError(f"Missing column '{col}' in {DATA}")

    E = df["energy_eV"].values
    F = df["flux"].values

    plt.figure(figsize=(7,4.2))
    plt.loglog(E, F)
    plt.xlabel("Energy (eV)")
    plt.ylabel("Flux (arb. units)")
    plt.title("Ultra-High-Energy Cosmic Ray Spectrum")
    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT, bbox_inches="tight")
    plt.close()
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
