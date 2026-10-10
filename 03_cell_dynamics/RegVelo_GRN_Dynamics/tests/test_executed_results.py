"""Numerical integration checks against an explicitly supplied actual run."""
import json
import os
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import pytest
from scipy import sparse

pytestmark = pytest.mark.skipif(not os.environ.get("REGVELO_EXECUTED_OUTPUT"),
                                reason="Requires real saved official run; no synthetic substitute")


@pytest.fixture(scope="module")
def output():
    return Path(os.environ["REGVELO_EXECUTED_OUTPUT"])


def test_actual_training_metrics_and_dimensions(output):
    velocity = ad.read_h5ad(output / "velocity.h5ad")
    assert velocity.shape == (697, 1007)
    assert np.isfinite(velocity.layers["velocity"]).all()
    assert np.isfinite(velocity.layers["velocity_std"]).all()
    assert velocity.obs.latent_time.between(0, 1).all()
    for path in (output / "tables").glob("training_*.csv"):
        if path.name != "training_history.csv":
            assert np.isfinite(pd.read_csv(path, index_col=0).to_numpy(dtype=float)).all()


def test_transition_conservation_and_fate_probabilities(output):
    for path in (output / "tables").glob("*_transition_matrix.npz"):
        matrix = sparse.load_npz(path)
        assert matrix.shape == (697, 697)
        assert np.isfinite(matrix.data).all() and matrix.data.min() >= 0
        np.testing.assert_allclose(np.asarray(matrix.sum(axis=1)).ravel(), 1, atol=1e-12, rtol=0)
    for path in (output / "tables").glob("*_fate_probabilities.csv"):
        if "FAILED" in path.name:  # Historical failed solver output is retained as evidence.
            continue
        values = pd.read_csv(path, index_col=0).to_numpy()
        assert values.shape == (697, 4)
        assert np.isfinite(values).all() and values.min() >= -1e-10 and values.max() <= 1+1e-10
        np.testing.assert_allclose(values.sum(axis=1), 1, atol=1e-10, rtol=0)


def test_actual_noop_and_no_edge_controls(output):
    baseline = ad.read_h5ad(output / "baseline_posterior.h5ad")
    for filename in ("perturb_null.h5ad", "perturb_no_edges.h5ad"):
        control = ad.read_h5ad(output / filename)
        assert control.obs_names.equals(baseline.obs_names) and control.var_names.equals(baseline.var_names)
        np.testing.assert_array_equal(control.layers["velocity"], baseline.layers["velocity"])
        np.testing.assert_allclose(control.obsm["lineages_fwd"], baseline.obsm["lineages_fwd"], atol=1e-12, rtol=0)


@pytest.mark.parametrize("tf", ["elf1", "nr2f5"])
def test_knockout_has_aligned_saved_fate_deltas_and_blocked_edges(output, tf):
    baseline = ad.read_h5ad(output / "baseline_posterior.h5ad")
    knockout = ad.read_h5ad(output / f"perturb_{tf}.h5ad")
    assert knockout.obs_names.equals(baseline.obs_names) and knockout.var_names.equals(baseline.var_names)
    names = list(json.loads((output / "terminal_cell_sets.json").read_text()))
    saved = pd.read_csv(output / "tables" / f"{tf}_fate_difference.csv", index_col=0)
    assert saved.columns.tolist() == names and saved.index.tolist() == baseline.obs_names.tolist()
    delta = np.asarray(knockout.obsm["lineages_fwd"]) - np.asarray(baseline.obsm["lineages_fwd"])
    np.testing.assert_allclose(saved.values, delta, atol=1e-14, rtol=0)
    np.testing.assert_allclose(delta.sum(axis=1), 0, atol=1e-10, rtol=0)
    edges = pd.read_csv(output / "tables" / f"{tf}_blocked_edges.csv")
    assert len(edges) > 0 and edges.regulator.eq(tf).all() and edges.weight_after.eq(0).all()
    assert (edges.weight_before.abs() > .001).all()
    assert np.isfinite(knockout.layers["velocity"]).all()
    expected_l2 = np.linalg.norm(knockout.layers["velocity"] - baseline.layers["velocity"], axis=1)
    np.testing.assert_allclose(knockout.obs.perturbation_velocity_l2, expected_l2, atol=1e-8, rtol=1e-6)
