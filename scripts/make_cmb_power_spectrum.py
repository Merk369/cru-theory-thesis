import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Paths
DATA_PATH = "./data/cmb_cl_TT.csv"
OUTPUT_PATH = "./figures/cmb_power_spectrum.pdf"

# Load CMB data (multipole moment l, TT spectrum, error)
data = pd.read_csv(DATA_PATH)
ell = data["ell"].values
cl = data["C_l"].values
err = data["sigma"].values

# Plot
plt.figure(figsize=(7,5))
plt.errorbar(ell, cl, yerr=err, fmt="o", markersize=2, color="blue", ecolor="lightgray", capsize=2)
plt.xscale("log")
plt.yscale("log")
plt.xlabel(r"Multipole $\ell$")
plt.ylabel(r"$C_\ell$  [$\mu K^2$]")
plt.title("CMB Power Spectrum (TT)")
plt.grid(True, which="both", ls="--", lw=0.5, alpha=0.6)
plt.tight_layout()

# Ensure output folder exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH)
print(f"Saved figure to {OUTPUT_PATH}")
