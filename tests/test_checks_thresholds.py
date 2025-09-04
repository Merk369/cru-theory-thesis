import pytest
import json
import os

# Load CRU prediction thresholds (could be JSON or YAML)
with open("config/cru.yml", "r") as f:
    config = f.read()

def test_thresholds_exist():
    """Ensure all critical prediction thresholds are defined."""
    for key in ["cmb", "gw", "uhecr", "dm"]:
        assert key in config, f"Missing threshold for {key}"

def test_cmb_thresholds():
    """CMB chi2 thresholds must be finite and positive."""
    assert "cmb" in config
    assert "chi2_limit" in config["cmb"]
    assert config["cmb"]["chi2_limit"] > 0

def test_gw_thresholds():
    """GW strain thresholds must be finite and positive."""
    assert "gw" in config
    assert "strain_limit" in config["gw"]
    assert config["gw"]["strain_limit"] > 0

def test_uhecr_thresholds():
    """UHECR sigma thresholds must be finite and positive."""
    assert "uhecr" in config
    assert "sigma_limit" in config["uhecr"]
    assert config["uhecr"]["sigma_limit"] > 0

def test_dm_thresholds():
    """DM cross-section thresholds must be finite and positive."""
    assert "dm" in config
    assert "sigma_si_limit" in config["dm"]
    assert config["dm"]["sigma_si_limit"] > 0
