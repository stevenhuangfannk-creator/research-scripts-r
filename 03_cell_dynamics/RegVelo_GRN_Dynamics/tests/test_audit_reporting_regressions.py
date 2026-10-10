"""Actual CLI regressions; tiny software fixtures are not biological evidence."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import anndata as ad
import numpy as np
import pandas as pd
import pytest

MODULE = Path(__file__).resolve().parents[1]


def invoke(stage, config):
    env = os.environ.copy()
    env.update(OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", NUMBA_NUM_THREADS="4")
    return subprocess.run([sys.executable, str(MODULE / "scripts/regvelo.py"), stage, "--config", str(config)],
                          capture_output=True, text=True, encoding="utf-8", env=env, timeout=60)


@pytest.mark.parametrize("duplicate_prior", [False, True])
def test_missing_splice_layers_still_records_prior_evidence(tmp_path, duplicate_prior):
    source = tmp_path / "expression_only.h5ad"
    data = ad.AnnData(np.array([[2, 0, 3], [0, 4, 1]], dtype=float),
                      obs=pd.DataFrame({"cell_type": ["fixture_a", "fixture_b"]}, index=["cell_1", "cell_2"]),
                      var=pd.DataFrame(index=["TF1", "target1", "target2"]))
    data.layers["counts"] = data.X.copy()
    data.write_h5ad(source)
    prior = tmp_path / "prior.csv"
    pd.DataFrame({"source": ["TF1", "TF1"],
                  "target": ["target1", "target1" if duplicate_prior else "target2"],
                  "weight": [1, -1]}).to_csv(prior, index=False)
    hashes = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in (source, prior)}
    config = tmp_path / "job.json"
    config.write_text(json.dumps({"input": source.name, "grn": prior.name, "output": "derived",
                                  "grn_format": "edge_list", "grn_orientation": "regulator_by_target",
                                  "group_key": "cell_type", "time_key": None}), encoding="utf-8")
    process = invoke("audit", config)
    assert process.returncode == 1, process.stdout + process.stderr
    output = tmp_path / "derived"
    audit = json.loads((output / "INPUT_AUDIT.json").read_text(encoding="utf-8"))
    assert audit["status"] == "FAIL"
    assert audit["readiness"] == "NOT_READY"
    assert audit["required_layers_missing"] == ["spliced", "unspliced"]
    assert audit["layers_present"] == ["counts"]
    assert any("Missing required RNA layers" in issue for issue in audit["issues"])
    if duplicate_prior:
        assert audit["grn"]["status"] == "FAIL"
        assert "Duplicate TF-target" in audit["grn"]["error"]
        assert any(issue.startswith("GRN:") for issue in audit["issues"])
    else:
        assert audit["grn"]["edges"] == 2
        assert audit["grn"]["active_regulators"] == 1
        assert audit["grn"]["active_targets"] == 2
    evidence = pd.read_csv(output / "tables/input_cell_qc.csv", index_col=0)
    assert evidence.index.tolist() == data.obs_names.tolist()
    assert evidence.cell_type.tolist() == data.obs.cell_type.tolist()
    assert not any(column.startswith(("spliced_", "unspliced_")) for column in evidence)
    assert {Path(record["path"]): record["sha256"] for record in audit["sources"]} == hashes
    assert all(hashlib.sha256(path.read_bytes()).hexdigest() == digest for path, digest in hashes.items())
    state = json.loads((output / "run_state.json").read_text(encoding="utf-8"))
    assert state["stages"]["audit"]["status"] == "FAIL"
    assert Path(state["stages"]["audit"]["error_log"]).is_file()


def test_completed_report_has_final_pass_and_explicit_not_run_stages(tmp_path):
    config = tmp_path / "job.json"
    config.write_text(json.dumps({"input": "not_run.h5ad", "grn": "not_run.csv", "output": "derived"}), encoding="utf-8")
    process = invoke("report", config)
    assert process.returncode == 0, process.stdout + process.stderr
    output = tmp_path / "derived"
    state = json.loads((output / "run_state.json").read_text(encoding="utf-8"))
    assert set(state["stages"]) == {"report"}
    assert state["stages"]["report"]["status"] == "PASS"
    report = (output / "ANALYSIS_REPORT.md").read_text(encoding="utf-8")
    assert "| report | PASS |" in report
    assert "RUNNING" not in report
    for stage in ("audit", "prepare", "fit", "velocity", "fate", "grn", "perturb", "visualize"):
        assert f"| {stage} | NOT_RUN |" in report
    assert not (output / "model").exists()
    assert not (output / "velocity.h5ad").exists()
