# Makefile for CRU thesis repo (single-file LaTeX build + data + figures)

PY := python3

.PHONY: all data figures pdf clean

all: data figures pdf

data:
	@$(PY) scripts/generate_datasets.py

figures: data
	@$(PY) scripts/plot_figures.py

pdf:
	# Build the LaTeX (pdflatex + bibtex + twice more pdflatex)
	# Works on TeXLive in GitHub Codespaces or your machine.
	pdflatex -interaction=nonstopmode CRU_thesis.tex
	bibtex CRU_thesis || true
	pdflatex -interaction=nonstopmode CRU_thesis.tex
	pdflatex -interaction=nonstopmode CRU_thesis.tex

clean:
	@rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot *.idx *.ilg *.ind
