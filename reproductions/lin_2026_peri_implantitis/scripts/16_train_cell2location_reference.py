"""Train and audit the cell2location reference signature model."""
from __future__ import annotations

import argparse
import json
import platform
from importlib.metadata import version
from pathlib import Path

import anndata as ad
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scvi
import torch
from cell2location.models import RegressionModel


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "phase4b" / "cell2location_input" / "scrna_reference_counts.h5ad"
OUT = ROOT / "results" / "phase4b" / "cell2location_reference"
MODEL = ROOT / "models" / "phase4b" / "cell2location_reference"
FIG = ROOT / "figures" / "phase4b" / "cell2location_reference"
SEED = 20260928

mpl.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
                     "svg.fonttype": "none", "pdf.fonttype": 42, "font.size": 8,
                     "axes.spines.right": False, "axes.spines.top": False})


def save_figure(fig, name: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    path = FIG / name
    fig.savefig(path.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=2500)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    scvi.settings.seed = SEED
    torch.manual_seed(SEED)
    torch.set_num_threads(min(8, torch.get_num_threads()))

    adata = ad.read_h5ad(INPUT)
    RegressionModel.setup_anndata(adata, batch_key="sample_id", labels_key="major_cell_type")
    model = RegressionModel(adata)
    model.train(max_epochs=args.epochs, batch_size=args.batch_size, train_size=1, lr=0.002,
                accelerator="cpu")
    model.save(MODEL, overwrite=True)

    history = pd.concat({key: value for key, value in model.history.items()}, axis=1)
    history.to_csv(OUT / "training_history.tsv", sep="\t")
    adata = model.export_posterior(
        adata,
        sample_kwargs={"num_samples": 1000, "batch_size": args.batch_size, "use_gpu": False},
    )
    adata.write_h5ad(OUT / "reference_posterior.h5ad", compression="gzip")
    signatures = adata.varm["means_per_cluster_mu_fg"].copy()
    if not isinstance(signatures, pd.DataFrame):
        signatures = pd.DataFrame(signatures, index=adata.var_names,
                                  columns=adata.uns["mod"]["factor_names"])
    signatures.to_csv(OUT / "reference_signatures.tsv.gz", sep="\t", compression="gzip")

    loss_key = next(key for key in model.history if "elbo" in key.lower())
    loss = np.asarray(model.history[loss_key]).ravel()
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    ax.plot(np.arange(1, len(loss) + 1), loss, color="#486f91", linewidth=1.2)
    ax.set(xlabel="Epoch", ylabel=loss_key, title="Cell2location reference training")
    ax.grid(alpha=0.2)
    save_figure(fig, "reference_training_loss")

    naive = model._compute_cluster_averages(key="_scvi_labels")
    correlations = {}
    for cell_type in signatures.columns.intersection(naive.columns):
        correlations[cell_type] = float(np.corrcoef(signatures[cell_type], naive[cell_type])[0, 1])
    pd.Series(correlations, name="pearson_r").sort_values().to_csv(
        OUT / "signature_naive_correlations.tsv", sep="\t", header=True
    )
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ordered = pd.Series(correlations).sort_values()
    ax.bar(ordered.index, ordered.values, color="#6b88a7")
    ax.axhline(0.8, color="#b0403a", linestyle="--", linewidth=0.8)
    ax.set(ylabel="Pearson r", title="Posterior signatures vs. cluster-average expression")
    ax.tick_params(axis="x", rotation=45)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right"); label.set_rotation_mode("anchor")
    save_figure(fig, "reference_signature_correlations")

    environment = {
        "python": platform.python_version(),
        "torch": torch.__version__,
        "scvi_tools": version("scvi-tools"),
        "cell2location": version("cell2location"),
        "cuda_available": torch.cuda.is_available(),
        "accelerator": "cpu",
        "seed": SEED,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "cells": adata.n_obs,
        "genes": adata.n_vars,
        "cell_types": adata.obs["major_cell_type"].nunique(),
        "final_loss": float(loss[-1]),
        "minimum_signature_correlation": min(correlations.values()),
    }
    (OUT / "reference_model_summary.json").write_text(json.dumps(environment, indent=2), encoding="utf-8")
    print(json.dumps(environment, indent=2))


if __name__ == "__main__":
    main()
