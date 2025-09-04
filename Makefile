# ===========================
# CRU-thesis Makefile (locked)
# ===========================

# -------- Config --------
PY        := python3
LATEXMK   := latexmk
TEXFLAGS  := -pdf -interaction=nonstopmode -halt-on-error -file-line-error
MANUSCRIPT:= CRU_thesis.tex
PDF       := CRU_thesis.pdf

# Directories
DATA_DIR   := data
FIG_DIR    := figures
TAB_DIR    := tables
BADGE_DIR  := badges
SCR_DIR    := scripts

# Data files (produced by fetch_* scripts)
UHECR_CSV  := $(DATA_DIR)/uhecr_flux.csv
GW_CSV     := $(DATA_DIR)/gw_strain.csv
CMB_TT_CSV := $(DATA_DIR)/cmb_cl_TT.csv
CMB_EE_CSV := $(DATA_DIR)/cmb_cl_EE.csv
DM_CSV     := $(DATA_DIR)/dm_limits.csv

# Figures (produced by build_figures.py)
FIG_GW     := $(FIG_DIR)/gw_prediction.pdf
FIG_CMB    := $(FIG_DIR)/cmb_power_spectrum.pdf
FIG_UHECR  := $(FIG_DIR)/uhecr_spectrum.pdf
FIG_DM     := $(FIG_DIR)/dm_limits.pdf

# Tables (may be auto-generated)
TAB_UHECR  := $(TAB_DIR)/uhecr_table.tex

# Badges / checks
CRU_BADGE  := $(BADGE_DIR)/cru_checks.svg

# Phony targets
.PHONY: all data figures tables check pdf clean distclean ci

# Default: everything
all: data figures tables check pdf

# -------- Data pipeline --------
data: $(UHECR_CSV) $(GW_CSV) $(CMB_TT_CSV) $(CMB_EE_CSV) $(DM_CSV)

$(UHECR_CSV): $(SCR_DIR)/fetch_auger.py | $(DATA_DIR)
	$(PY) $(SCR_DIR)/fetch_auger.py --out $@

$(GW_CSV): $(SCR_DIR)/fetch_gw.py | $(DATA_DIR)
	$(PY) $(SCR_DIR)/fetch_gw.py --out $@

$(CMB_TT_CSV): $(SCR_DIR)/fetch_planck.py | $(DATA_DIR)
	$(PY) $(SCR_DIR)/fetch_planck.py --spectrum TT --out $@

$(CMB_EE_CSV): $(SCR_DIR)/fetch_planck.py | $(DATA_DIR)
	$(PY) $(SCR_DIR)/fetch_planck.py --spectrum EE --out $@

$(DM_CSV): $(SCR_DIR)/fetch_dm.py | $(DATA_DIR)
	$(PY) $(SCR_DIR)/fetch_dm.py --out $@

$(DATA_DIR):
	mkdir -p $(DATA_DIR)

# -------- Build figures/tables --------
figures: $(FIG_GW) $(FIG_CMB) $(FIG_UHECR) $(FIG_DM)

$(FIG_GW) $(FIG_CMB) $(FIG_UHECR) $(FIG_DM): $(SCR_DIR)/build_figures.py data | $(FIG_DIR)
	$(PY) $(SCR_DIR)/build_figures.py --data $(DATA_DIR) --out $(FIG_DIR)

$(FIG_DIR):
	mkdir -p $(FIG_DIR)

tables: $(TAB_UHECR)

$(TAB_UHECR): $(SCR_DIR)/build_figures.py data | $(TAB_DIR)
	$(PY) $(SCR_DIR)/build_figures.py --data $(DATA_DIR) --tables $(TAB_DIR)

$(TAB_DIR):
	mkdir -p $(TAB_DIR)

# -------- Checks / badges --------
check: $(CRU_BADGE)

$(CRU_BADGE): $(SCR_DIR)/check_predictions.py figures data | $(BADGE_DIR)
	$(PY) $(SCR_DIR)/check_predictions.py --data $(DATA_DIR) --figures $(FIG_DIR) --out $@

$(BADGE_DIR):
	mkdir -p $(BADGE_DIR)

# -------- LaTeX compile --------
pdf: $(PDF)

$(PDF): $(MANUSCRIPT) refs.bib figures tables
	$(LATEXMK) $(TEXFLAGS) $(MANUSCRIPT)

# -------- Cleanup --------
clean:
	$(LATEXMK) -c
	rm -f *.bbl *.run.xml *.bcf
	rm -f $(CRU_BADGE)

distclean: clean
	rm -f $(PDF)
	rm -rf $(FIG_DIR) $(TAB_DIR) $(BADGE_DIR)
# (intentionally keep data/ so fetch is not required every time)

# -------- CI convenience --------
ci: all
	@echo "CI build complete."
