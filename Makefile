# CRU Thesis build: figures → PDF → checks
SHELL := /bin/bash

PDF := CRU_thesis.pdf
TEX := CRU_thesis.tex

# Default: build figures and the thesis PDF
all: figures $(PDF)

# Generate figures from data (writes PDFs into ./figures as per repo spec)
figures:
	python3 scripts/build_figures.py

# Compile thesis (latexmk handles multiple passes + bibtex)
$(PDF): $(TEX) refs.bib
	latexmk -pdf -interaction=nonstopmode -halt-on-error $(TEX)

# Run prediction checks and produce a status badge
check:
	python3 scripts/check_predictions.py

# Clean build artifacts
clean:
	latexmk -C
	rm -f figures/*.pdf figures/*.png
	rm -f badges/*.svg
	rm -f tables/*.tex

# Convenience target: everything
ci: clean all check

.PHONY: all figures check clean ci
