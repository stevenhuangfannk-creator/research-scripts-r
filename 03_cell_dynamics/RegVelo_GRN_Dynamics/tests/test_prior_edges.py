"""Meaningful adapters for signed, directed TF Atlas priors."""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from regvelo_workflow.core import read_prior, validate_grn


def test_named_edge_direction_and_unmatched_species(tmp_path):
    path = tmp_path / "edges.csv"
    pd.DataFrame({"source": ["JUND", "JUND", "Mitfa"], "target": ["IL6", "FOS", "pigment"], "weight": [1, -1, 1]}).to_csv(path, index=False)
    config = {"grn": str(path), "grn_format": "edge_list", "grn_orientation": "regulator_by_target"}
    matrix = read_prior(config, ["JUND", "IL6", "FOS"])
    aligned = validate_grn(matrix, ["FOS", "JUND", "IL6"], config["grn_orientation"])
    assert aligned.loc["IL6", "JUND"] == 1
    assert aligned.loc["FOS", "JUND"] == -1
    assert "Mitfa" not in aligned.columns


def test_conflicting_evidence_is_not_silently_aggregated(tmp_path):
    path = tmp_path / "edges.csv"
    pd.DataFrame({"source": ["JUND", "JUND"], "target": ["IL6", "IL6"], "weight": [1, -1]}).to_csv(path, index=False)
    config = {"grn": str(path), "grn_format": "edge_list", "grn_orientation": "target_by_regulator"}
    with pytest.raises(ValueError, match="Duplicate"):
        read_prior(config, ["JUND", "IL6"])
