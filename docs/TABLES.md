# 📑 Master Table Index — CRU Thesis

This file lists all data tables used in the CRU thesis, their purpose, and where they are included.

---

### **Table 1 — Resonant Frequency Anchors**
**File:** `tables/resonant_anchors.tex`  
- Lists Standard Model particles (electron, muon, tau, proton, W/Z bosons, Higgs).  
- Includes mass values, Compton frequencies, and resonance roles.  
- Basis for resonance spectrum figures.  

---

### **Table 2 — Verification Table**
**File:** `tables/verification_table.tex`  
- Uses electron as anchor (\(\zeta = 1\)).  
- Cross-checks muon and Higgs masses.  
- Confirms CRU equation reproduces measured values with minimal tuning.  

---

### **Table 3 — Cosmology Constraints**
**File:** `tables/cosmo_constraints.tex`  
- Summarizes observational limits:  
  - BBN: \(|\kappa_G| \lesssim 10^{-2}\).  
  - CMB: \(\Delta N_\text{eff} < 0.3\).  
  - Fifth-force: \(|\xi| \lesssim 10^{-3}\).  
  - Structure formation: \(m_\text{dark} \gtrsim 1\ \text{GeV}\).  
- Defines viable CRU parameter window.  

---

### **Table 4 — Experimental Benchmark Protocols**
**File:** `tables/experimental_protocols.tex`  
- Defines scanning offsets and pass/fail criteria for falsification.  
- Electron anchor: ±10⁻⁶ resonance precision.  
- Muon and Higgs as cross-checks.  

---

### **Table 5 — Data Provenance & Constants**
**File:** `DATA_PROVENANCE.md`  
- CODATA 2022 constants.  
- Planck 2018 + SPTpol cosmological parameters.  
- Traceable reference for all numbers used in thesis.  

---

✅ All tables are fully included in the build via `CRU_thesis.tex` and cross-referenced in the Master Index.
