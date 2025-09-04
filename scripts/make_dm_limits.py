import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Paths
DATA_PATH = "./data/dm_limits.csv"
OUTPUT_PATH = "./figures/dm_limits.pdf"

# Load dark matter direct detection limits (mass [GeV], cross-section [cm^2])
data = pd.read_csv(DATA_PATH)
mass = data["mass_GeV"].values
sigma = data["sigma_cm2"].values
label = data.get("experiment", ["Exp"] * len(mass))

# Plot
plt.figure(figsize=(7,5))
for exp in set(label):
    idx = [i for i, l in enumerate(label) if l == exp]
    plt.loglog(mass[idx], sigma[idx], marker="o", linestyle="-", label=exp)

plt.xlabel("Dark Matter Mass [GeV]")
plt.ylabel(r"SI Cross-section [$cm^2$]")
plt.title("Dark Matter Direct Detection Limits")
plt.legend()
plt.grid(True, which="both", ls="--", lw=0.5, alpha=0.6)
plt.tight_layout()

# Ensure output folder exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH)
print(f"Saved figure to {OUTPUT_PATH}")
