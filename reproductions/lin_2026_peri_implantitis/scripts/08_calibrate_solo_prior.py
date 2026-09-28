"""Correct SOLO probabilities from the simulated training prior to the expected real prior."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PROJECT_ROOT / "results" / "phase4a"


def main() -> int:
    with (PROJECT_ROOT / "config" / "analysis.toml").open("rb") as handle:
        doublets = tomllib.load(handle)["phase4a"]["doublets"]
    target_prior = float(doublets["expected_rate"])
    simulated_ratio = float(doublets["simulated_doublet_ratio"])
    training_prior = simulated_ratio / (1.0 + simulated_ratio)

    predictions = pd.read_csv(OUTPUT_ROOT / "solo_predictions.tsv.gz", sep="\t", index_col=0)
    raw_probability = predictions["doublet"].clip(1e-8, 1 - 1e-8)
    likelihood_ratio = (raw_probability / (1 - raw_probability)) / (
        training_prior / (1 - training_prior)
    )
    target_odds = likelihood_ratio * (target_prior / (1 - target_prior))
    predictions["doublet_probability_prior_corrected"] = target_odds / (1 + target_odds)
    predictions["prior_corrected_prediction"] = np.where(
        predictions["doublet_probability_prior_corrected"] > 0.5,
        "doublet",
        "singlet",
    )
    predictions.to_csv(
        OUTPUT_ROOT / "solo_predictions_prior_corrected.tsv.gz", sep="\t", compression="gzip"
    )

    adata = sc.read_h5ad(OUTPUT_ROOT / "phase4a_pre_doublet.h5ad")
    predictions = predictions.loc[adata.obs_names]
    adata.obs["solo_raw_doublet_probability"] = predictions["doublet"].to_numpy()
    adata.obs["solo_raw_prediction"] = predictions["prediction"].to_numpy()
    adata.obs["solo_doublet_probability"] = predictions[
        "doublet_probability_prior_corrected"
    ].to_numpy()
    adata.obs["solo_prediction"] = predictions["prior_corrected_prediction"].to_numpy()
    keep = adata.obs["solo_prediction"] == "singlet"
    filtered = adata[keep].copy()
    filtered.uns["reconstruction"]["doublet_removal"] = (
        "MODERNIZED IMPLEMENTATION: per-capture scvi-tools SOLO with prior correction"
    )
    filtered.write_h5ad(OUTPUT_ROOT / "phase4a_post_doublet.h5ad", compression="gzip")

    by_sample = (
        adata.obs.groupby(["condition", "sample_id"], observed=True)["solo_prediction"]
        .value_counts()
        .unstack(fill_value=0)
        .reset_index()
    )
    by_sample.to_csv(OUTPUT_ROOT / "solo_counts_by_sample.tsv", sep="\t", index=False)
    condition_counts = {
        str(key): int(value) for key, value in filtered.obs["condition"].value_counts().items()
    }
    summary = {
        "classification": "MODERNIZED IMPLEMENTATION",
        "method": "per-capture scvi-tools SOLO with Bayesian prior correction",
        "training_doublet_prior": training_prior,
        "target_doublet_prior": target_prior,
        "decision_threshold_after_prior_correction": 0.5,
        "cells_before": int(adata.n_obs),
        "raw_hard_doublets": int((adata.obs["solo_raw_prediction"] == "doublet").sum()),
        "prior_corrected_doublets": int((~keep).sum()),
        "cells_after": int(filtered.n_obs),
        "condition_counts_after": condition_counts,
        "paper_reported_final_cells": 90551,
        "difference_from_paper_total": int(filtered.n_obs - 90551),
    }
    (OUTPUT_ROOT / "solo_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
