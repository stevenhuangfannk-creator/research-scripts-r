"""Run batch-aware scVI/SOLO doublet reconstruction on the 21-sample input."""

from __future__ import annotations

import json
import os
import tomllib
from pathlib import Path

import pandas as pd
import scanpy as sc
import scvi
import torch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PROJECT_ROOT / "results" / "phase4a"
MODEL_ROOT = OUTPUT_ROOT / "models"


def main() -> int:
    with (PROJECT_ROOT / "config" / "analysis.toml").open("rb") as handle:
        config = tomllib.load(handle)
    seed = int(config["project"]["random_seed"])
    doublets = config["phase4a"]["doublets"]
    n_hvg = int(config["phase4a"]["features"]["n_highly_variable_genes"])

    scvi.settings.seed = seed
    torch.set_num_threads(min(8, os.cpu_count() or 1))
    adata = sc.read_h5ad(OUTPUT_ROOT / "phase4a_pre_doublet.h5ad")
    training = adata.copy()
    sc.pp.highly_variable_genes(
        training,
        n_top_genes=n_hvg,
        flavor="seurat_v3",
        layer="counts",
        batch_key="sample_id",
        subset=True,
    )

    MODEL_ROOT.mkdir(parents=True, exist_ok=True)
    base_model_path = MODEL_ROOT / "solo_scvi"
    if (base_model_path / "model.pt").exists():
        model = scvi.model.SCVI.load(base_model_path, adata=training)
        scvi_epochs_completed = int(doublets["scvi_max_epochs"])
        print(f"loaded completed scVI base model: {base_model_path}")
    else:
        scvi.model.SCVI.setup_anndata(training, layer="counts", batch_key="sample_id")
        model = scvi.model.SCVI(training, n_latent=30, gene_likelihood="nb")
        model.train(
            max_epochs=int(doublets["scvi_max_epochs"]),
            accelerator="cpu",
            devices=1,
            batch_size=int(doublets["batch_size"]),
            early_stopping=True,
            enable_progress_bar=True,
        )
        model.save(base_model_path, overwrite=True)
        scvi_epochs_completed = int(model.history["elbo_train"].shape[0])

    prediction_tables: list[pd.DataFrame] = []
    solo_epoch_counts: dict[str, int] = {}
    for sample_id in training.obs["sample_id"].cat.categories:
        print(f"training SOLO for capture: {sample_id}")
        solo = scvi.external.SOLO.from_scvi_model(model, restrict_to_batch=str(sample_id))
        solo.train(
            max_epochs=int(doublets["solo_max_epochs"]),
            accelerator="cpu",
            devices=1,
            batch_size=int(doublets["batch_size"]),
            early_stopping=True,
            enable_progress_bar=False,
        )
        solo.save(MODEL_ROOT / "solo_by_sample" / str(sample_id), overwrite=True)
        soft = solo.predict(soft=True)
        hard = solo.predict(soft=False)
        if isinstance(hard, pd.DataFrame):
            hard = hard.iloc[:, 0]
        sample_predictions = soft.copy()
        sample_predictions["prediction"] = hard.astype(str)
        prediction_tables.append(sample_predictions)
        solo_epoch_counts[str(sample_id)] = int(solo.history["validation_loss"].shape[0])

    predictions = pd.concat(prediction_tables).loc[adata.obs_names]
    predictions["sample_id"] = adata.obs.loc[predictions.index, "sample_id"].astype(str)
    predictions["condition"] = adata.obs.loc[predictions.index, "condition"].astype(str)
    predictions.to_csv(OUTPUT_ROOT / "solo_predictions.tsv.gz", sep="\t", compression="gzip")

    adata.obs["solo_doublet_probability"] = predictions["doublet"].to_numpy()
    adata.obs["solo_singlet_probability"] = predictions["singlet"].to_numpy()
    adata.obs["solo_prediction"] = predictions["prediction"].to_numpy()
    keep = adata.obs["solo_prediction"] == "singlet"
    filtered = adata[keep].copy()
    filtered.uns["reconstruction"]["doublet_removal"] = "MODERNIZED IMPLEMENTATION: scvi-tools SOLO"
    filtered.write_h5ad(OUTPUT_ROOT / "phase4a_post_doublet_uncalibrated.h5ad", compression="gzip")

    by_sample = (
        adata.obs.groupby(["condition", "sample_id"], observed=True)["solo_prediction"]
        .value_counts()
        .unstack(fill_value=0)
        .reset_index()
    )
    by_sample.to_csv(OUTPUT_ROOT / "solo_uncalibrated_counts_by_sample.tsv", sep="\t", index=False)
    summary = {
        "classification": "MODERNIZED IMPLEMENTATION",
        "method": "scvi-tools SOLO",
        "seed": seed,
        "hvg": n_hvg,
        "scvi_epochs_completed": scvi_epochs_completed,
        "solo_epochs_by_sample": solo_epoch_counts,
        "cells_before": int(adata.n_obs),
        "predicted_doublets": int((~keep).sum()),
        "cells_after": int(filtered.n_obs),
        "paper_reported_final_cells": 90551,
        "difference_from_paper_total": int(filtered.n_obs - 90551),
        "cuda_available": bool(torch.cuda.is_available()),
    }
    (OUTPUT_ROOT / "solo_uncalibrated_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
