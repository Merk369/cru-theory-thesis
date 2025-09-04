# Data Provenance for CRU Theory Thesis

This document provides full provenance of all datasets used in the **Causal Resonance Unification (CRU) Theory Thesis**.  
Every dataset is either sourced from public archives, official collaborations, or internally generated simulations, with references included.

---

## Cosmic Microwave Background (CMB)

**Files:**  
- `data/cmb_cl_TT.csv`  
- `data/cmb_cl_EE.csv`  

**Source:**  
Planck 2018 Legacy Archive (ESA / Planck Collaboration).  
- DOI: [10.1051/0004-6361/201833910](https://doi.org/10.1051/0004-6361/201833910)  
- Archive: [https://pla.esac.esa.int](https://pla.esac.esa.int)  

**Notes:**  
Downloaded via official Planck Python API, post-processed into CSV format for LaTeX table and figure integration.  

---

## Ultra-High-Energy Cosmic Rays (UHECR)

**Files:**  
- `data/uhecr_flux.csv`  
- `tables/uhecr_table.tex`  

**Source:**  
Pierre Auger Observatory – 2025 Spectrum Release.  
- DOI: [10.48550/arXiv.2504.10333](https://doi.org/10.48550/arXiv.2504.10333)  

**Notes:**  
Converted from ROOT files provided by Auger into CSV tables.  
Statistical and systematic uncertainties retained explicitly.  

---

## Gravitational Waves (GW)

**Files:**  
- `data/gw_strain.csv`  
- `figures/gw_prediction.pdf`  

**Source:**  
- LIGO/Virgo O3/O4 public releases.  
- NANOGrav 15-year data set.  
  - DOI: [10.3847/2041-8213/acdac6](https://doi.org/10.3847/2041-8213/acdac6)  

**Notes:**  
Strain spectral density extracted from published PSD curves and interpolated to uniform log-spaced bins.  

---

## Dark Matter (DM)

**Files:**  
- `data/dm_limits.csv`  
- `figures/dm_limits.pdf`  

**Source:**  
- XENONnT 2023, LZ 2023, PandaX-4T 2023 published results.  
- DARWIN projected limits (white paper).  

**Notes:**  
Cross-sections converted to cm², energies normalized to GeV, compiled into CSV format for reproducible figure generation.  

---

## Simulation Outputs

**Scripts:**  
- `scripts/build_figures.py`  
- `scripts/check_predictions.py`  

**Figures:**  
- `figures/cmb_power_spectrum.pdf`  
- `figures/uhecr_spectrum.pdf`  
- `figures/gw_prediction.pdf`  
- `figures/dm_limits.pdf`  

**Source:**  
Generated using CRPropa (UHECR), custom Python scripts (GW, CMB, DM).  
All parameters and seeds documented in the corresponding script headers.  

---

## License and Reproducibility

All processed datasets (CSV, TEX, PDF) included in this repository are redistributed under the **CC-BY-4.0 license**, with attribution to the original collaborations.  
Raw data should always be accessed from the official archives for definitive results.  

---

_Last updated: 2025-09-04_
