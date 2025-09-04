import os
import pandas as pd

DATA_PATH = "data"

def test_uhecr_flux_columns():
    df = pd.read_csv(os.path.join(DATA_PATH, "uhecr_flux.csv"))
    expected_cols = ["log10E", "flux", "stat_err", "sys_err"]
    for col in expected_cols:
        assert col in df.columns, f"Missing {col} in uhecr_flux.csv"

def test_gw_strain_columns():
    df = pd.read_csv(os.path.join(DATA_PATH, "gw_strain.csv"))
    expected_cols = ["frequency_hz", "strain", "strain_err"]
    for col in expected_cols:
        assert col in df.columns, f"Missing {col} in gw_strain.csv"

def test_cmb_tt_columns():
    df = pd.read_csv(os.path.join(DATA_PATH, "cmb_cl_TT.csv"))
    expected_cols = ["ell", "Cl_TT", "error"]
    for col in expected_cols:
        assert col in df.columns, f"Missing {col} in cmb_cl_TT.csv"

def test_dm_limits_columns():
    df = pd.read_csv(os.path.join(DATA_PATH, "dm_limits.csv"))
    expected_cols = ["mass_GeV", "sigma_si_cm2"]
    for col in expected_cols:
        assert col in df.columns, f"Missing {col} in dm_limits.csv"
