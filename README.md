# Causal Resonance Unification (CRU) Thesis

This repository contains the full **technical version** of the Causal Resonance Unification (CRU) theory thesis.  
It is structured for reproducibility, peer review, and automated compilation into a final **LaTeX PDF** with supporting datasets, figures, and validation scripts.

---

## 📂 Repository Structure
CRU-thesis/
├── CRU_thesis.tex            # Full LaTeX thesis
├── refs.bib                  # Bibliography
├── Makefile                  # Build pipeline (data → figures → PDF)
├── figures/                  # Generated plots and figures
├── data/                     # Raw & processed datasets
├── scripts/                  # Python scripts for data/figures
├── tables/                   # Auto-generated LaTeX tables
├── tests/                    # Automated checks
├── config/                   # Configurations
├── badges/                   # Build & validation badges
├── .github/workflows/        # GitHub Actions (CI/CD)
├── .gitignore                # Ignore build artifacts
├── README.md                 # Project overview (this file)
├── CITATION.cff              # Citation metadata
└── DATA_PROVENANCE.md        # Data provenance & licensing
---

## ⚙️ Dependencies

To build and validate the project, install:

- **LaTeX distribution** (e.g. TeX Live, MikTeX)
- **Python 3.10+**
- Python packages:  
  ```bash
  pip install -r requirements.txt
  make all
  make clean
  pytest tests/
  @misc{cleary2025cru,
  author       = {Shaun Cleary},
  title        = {Causal Resonance Unification (CRU) Thesis},
  year         = {2025},
  publisher    = {GitHub},
  url          = {https://github.com/<your-username>/CRU-thesis}
}

  
  
