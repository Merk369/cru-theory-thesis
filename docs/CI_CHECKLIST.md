# ✅ CRU Thesis CI Checklist

This checklist ensures the CRU Thesis PDF compiles **reproducibly** in GitHub Actions and locally.

---

## 1. Core Build Requirements
- `CRU_thesis.tex` exists in repo root.
- `ref.bib` is present for bibliography.
- All required tables exist in `/tables/`:
  - `resonant_anchors.tex`
  - `verification_table.tex`
  - `cosmo_constraints.tex`
  - `experimental_protocols.tex`
  - `unhecr_table.tex`
- All required figures exist in `/figures/` (see [INDEX.md](INDEX.md)).

---

## 2. GitHub Actions
- `.github/workflows/latex.yml` runs `latexmk -pdf CRU_thesis.tex`.
- Workflow **uploads `CRU_thesis.pdf`** as an artifact.
- `.github/workflows/python.yml` runs pytest for:
  - `tests/test_data_scheme.py`
  - `tests/test_checks_thresholds.py`
  - `tests/test_figures_exist.py`

---

## 3. LaTeX Environment
- `.latexmkrc` specifies `pdflatex` and `bibtex` (switch to `biber` if needed).
- `texlive.packages.txt` includes:
  - `texlive-base`, `texlive-latex-recommended`, `texlive-latex-extra`
  - `texlive-fonts-recommended`, `texlive-fonts-extra`
  - `texlive-bibtex-extra`, `texlive-science`, `texlive-pictures`
  - `texlive-publishers`, `pgfplots`
- Builds cleanly on `ubuntu-latest` in GitHub CI.

---

## 4. Local Build Steps
1. Install TeX Live (full recommended).
2. Clone the repo:
   ```bash
   git clone https://github.com/<YOUR-USERNAME>/<YOUR-REPO>.git
   cd <YOUR-REPO>
