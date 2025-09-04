# Data Schema for CRU Theory Thesis

This document defines the column layout, units, and conventions of all datasets in `./data/`.  
Every dataset is structured as a **comma-separated values (CSV)** file with UTF-8 encoding and headers on the first row.

---

## 1. `data/cmb_cl_TT.csv`

**Purpose:** CMB temperature anisotropy angular power spectrum (TT).  

**Columns:**
- `l` — Multipole moment (dimensionless, integer)  
- `Cl` — Power spectrum value \( C_l \) (units: μK² sr⁻¹)  
- `sigma_Cl` — 1σ uncertainty on \( C_l \) (same units as `Cl`)  

---

## 2. `data/cmb_cl_EE.csv`

**Purpose:** CMB E-mode polarization angular power spectrum (EE).  

**Columns:**
- `l` — Multipole moment (dimensionless, integer)  
- `Cl` — Power spectrum value \( C_l \) (units: μK² sr⁻¹)  
- `sigma_Cl` — 1σ uncertainty on \( C_l \)  

---

## 3. `data/uhecr_flux.csv`

**Purpose:** Ultra-high-energy cosmic ray (UHECR) flux spectrum.  

**Columns:**
- `log10E` — log10 of energy (units: eV)  
- `J(E)` — Differential flux \( J(E) \) (units: eV⁻¹ m⁻² s⁻¹ sr⁻¹)  
- `sigma_stat` — Statistical error (same units as `J(E)`)  
- `sigma_sys` — Systematic error (same units as `J(E)`)  

---

## 4. `data/gw_strain.csv`

**Purpose:** Gravitational wave strain spectrum.  

**Columns:**
- `f` — Frequency (units: Hz, log-spaced)  
- `h` — Strain amplitude (dimensionless)  
- `sigma_h` — 1σ uncertainty on strain amplitude  

---

## 5. `data/dm_limits.csv`

**Purpose:** Direct detection limits on dark matter scattering cross-section.  

**Columns:**
- `m_chi` — Dark matter mass (units: GeV)  
- `sigma_SI` — Spin-independent scattering cross-section (units: cm²)  
- `experiment` — String identifier for dataset (e.g., `XENONnT2023`, `LZ2023`, `PandaX4T2023`, `DARWIN_proj`)  

---

## Notes and Conventions

- All uncertainties (`sigma_*`) are 1σ standard deviations unless otherwise stated.  
- Logarithmic values (e.g., `log10E`) are explicitly stated in the header.  
- All CSV files are plain-text and version-controlled; regenerated automatically by `scripts/fetch_*.py`.  
- Figures in `./figures/` are built from these datasets by `scripts/build_figures.py`.  

---

_Last updated: 2025-09-04_
