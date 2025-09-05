"""
Generate figures/dm_limits.pdf from data/dm_limits.csv

Expected CSV headers:
  - mass_GeV
  - sigma_cm2
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA = Path("data/dm_limits.csv")
OUT = Path("figures/dm_limits.pdf")

def main():
    df = pd.read_csv(DATA)
    for col in ["mass_GeV", "sigma_cm2"]:
        if col not in df.columns:
            raise ValueError(f"Missing column '{col}' in {DATA}")

    m = df["mass_GeV"].values
    s = df["sigma_cm2"].values

    plt.figure(figsize=(7,4.2))
    plt.loglog(m, s)
    plt.xlabel("DM mass (GeV)")
    plt.ylabel(r"Cross section (cm$^2$)")
    plt.title("Dark Matter Direct-Detection Limits")
    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT, bbox_inches="tight")
    plt.close()
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
