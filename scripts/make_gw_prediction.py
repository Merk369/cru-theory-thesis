import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_CSV = "./data/gw_strain.csv"
OUT_PDF  = "./figures/gw_prediction.pdf"

def main():
    # Load data: expect columns frequency_Hz,strain[,sigma]
    df = pd.read_csv(DATA_CSV)

    if "frequency_Hz" not in df.columns or "strain" not in df.columns:
        raise ValueError("gw_strain.csv must have columns: frequency_Hz,strain[,sigma]")

    f = df["frequency_Hz"].to_numpy(dtype=float)
    h = df["strain"].to_numpy(dtype=float)
    sigma = df["sigma"].to_numpy(dtype=float) if "sigma" in df.columns else None

    plt.figure(figsize=(7,5))
    plt.loglog(f, h, label="GW strain (CRU prediction)")

    # Optional error band if sigma is present
    if sigma is not None:
        h_lo = np.clip(h - sigma, a_min=1e-99, a_max=None)
        h_hi = h + sigma
        plt.fill_between(f, h_lo, h_hi, alpha=0.2, label="±1σ")

    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Strain")
    plt.title("CRU Predicted Stochastic GW Background")
    plt.grid(True, which="both", ls="--", lw=0.5, alpha=0.6)
    plt.legend()
    plt.tight_layout()

    os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
    plt.savefig(OUT_PDF)
    print(f"Saved {OUT_PDF}")

if __name__ == "__main__":
    main()
