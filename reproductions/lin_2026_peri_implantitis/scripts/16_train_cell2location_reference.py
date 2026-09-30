"""Train the formal cell2location reference signature model."""
from __future__ import annotations

import argparse
import json
import platform
import time
from importlib.metadata import version
from pathlib import Path

import anndata as ad
import matplotlib as mpl
mpl.use("Agg")
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

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 8,
        "axes.spines.right": False,
        "axes.spines.top": False,
    }
)


def save_figure(fig: plt.Figure, name: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    path = FIG / name
    fig.savefig(path.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=250)
    parser.add_argument("--batch-size", type=int, default=2500)
    parser.add_argument("--accelerator", choices=("auto", "cpu", "gpu"), default="auto")
    parser.add_argument("--posterior-only", action="store_true")
    parser.add_argument("--finalize-existing-posterior", action="store_true")
    parser.add_argument("--training-elapsed-seconds", type=float)
    parser.add_argument("--curated-v1", action="store_true", help="Use the documented Leiden 47 correction")
    args = parser.parse_args()

    global INPUT, OUT, MODEL, FIG
    if args.curated_v1:
        INPUT = INPUT.with_name("scrna_reference_counts_curated_v1.h5ad")
        OUT = OUT / "curated_v1"
        MODEL = MODEL / "curated_v1"
        FIG = FIG / "curated_v1"

    accelerator = args.accelerator
    if accelerator == "auto":
        accelerator = "gpu" if torch.cuda.is_available() else "cpu"
    if accelerator == "gpu" and not torch.cuda.is_available():
        raise RuntimeError("GPU training requested but torch.cuda.is_available() is False")

    OUT.mkdir(parents=True, exist_ok=True)
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    scvi.settings.seed = SEED
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)
    torch.set_num_threads(min(8, torch.get_num_threads()))

    adata = ad.read_h5ad(INPUT)
    RegressionModel.setup_anndata(adata, batch_key="sample_id", labels_key="major_cell_type")
    if args.posterior_only:
        model = RegressionModel.load(MODEL, adata=adata, accelerator=accelerator)
        elapsed = args.training_elapsed_seconds
        history = pd.read_csv(OUT / "training_history.tsv", sep="\t", index_col=0)
    else:
        model = RegressionModel(adata)
        started = time.time()
        model.train(
            max_epochs=args.epochs,
            batch_size=args.batch_size,
            train_size=1,
            lr=0.002,
            accelerator=accelerator,
            enable_checkpointing=False,
        )
        elapsed = time.time() - started
        model.save(MODEL, overwrite=True)
        history = pd.DataFrame(
            {key: np.asarray(value).ravel() for key, value in model.history.items()}
        )
        history.to_csv(OUT / "training_history.tsv", sep="\t")
    history.to_csv(OUT / "training_history.tsv", sep="\t")
    if args.finalize_existing_posterior:
        adata = ad.read_h5ad(OUT / "reference_posterior.h5ad")
        signatures = pd.read_csv(
            OUT / "reference_signatures.tsv.gz", sep="\t", index_col=0
        )
    else:
        adata = model.export_posterior(
            adata,
            sample_kwargs={
                "num_samples": 1000,
                "batch_size": args.batch_size,
                "accelerator": accelerator,
                "device": "auto",
            },
        )
        signatures = adata.varm["means_per_cluster_mu_fg"].copy()
        if not isinstance(signatures, pd.DataFrame):
            signatures = pd.DataFrame(
                signatures,
                index=adata.var_names,
                columns=adata.uns["mod"]["factor_names"],
            )
        signatures.to_csv(OUT / "reference_signatures.tsv.gz", sep="\t", compression="gzip")
        # anndata 0.13 serialises DataFrame columns as HDF5 keys; the valid label
        # "Smooth muscle/pericytes" contains a slash, so preserve factor_names in
        # uns and store posterior varm entries as numeric matrices.
        for key in list(adata.varm.keys()):
            if isinstance(adata.varm[key], pd.DataFrame):
                adata.varm[key] = adata.varm[key].to_numpy()
        adata.write_h5ad(OUT / "reference_posterior.h5ad", compression="gzip")

    prefix = "means_per_cluster_mu_fg_"
    signatures.columns = [
        column.removeprefix(prefix) for column in signatures.columns
    ]
    signatures.to_csv(OUT / "reference_signatures.tsv.gz", sep="\t", compression="gzip")

    loss_key = next(key for key in history if "elbo" in key.lower())
    loss = history[loss_key].dropna().to_numpy(float)
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    ax.plot(np.arange(1, len(loss) + 1), loss, color="#486f91", linewidth=1.2)
    ax.set(xlabel="Epoch", ylabel=loss_key, title="Reference model convergence")
    ax.grid(alpha=0.2)
    save_figure(fig, "reference_training_loss")

    counts = adata.layers["counts"] if "counts" in adata.layers else adata.X
    label_values = adata.obs["major_cell_type"].astype(str).to_numpy()
    naive = pd.DataFrame(
        {
            cell_type: np.asarray(counts[label_values == cell_type].mean(axis=0)).ravel()
            for cell_type in signatures.columns
        },
        index=adata.var_names,
    )
    correlations = {
        cell_type: float(np.corrcoef(signatures[cell_type], naive[cell_type])[0, 1])
        for cell_type in signatures.columns.intersection(naive.columns)
    }
    ordered = pd.Series(correlations, name="pearson_r").sort_values()
    ordered.to_csv(OUT / "signature_naive_correlations.tsv", sep="\t", header=True)
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.bar(ordered.index, ordered.values, color="#6b88a7")
    ax.axhline(0.8, color="#b0403a", linestyle="--", linewidth=0.8)
    ax.set(ylabel="Pearson r", title="Posterior signatures vs. cluster means")
    ax.tick_params(axis="x", rotation=45)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")
        label.set_rotation_mode("anchor")
    save_figure(fig, "reference_signature_correlations")

    tail = loss[-min(25, len(loss)) :]
    tail_slope = float(np.polyfit(np.arange(len(tail)), tail, 1)[0]) if len(tail) > 1 else np.nan
    summary = {
        "python": platform.python_version(),
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "scvi_tools": version("scvi-tools"),
        "cell2location": version("cell2location"),
        "cuda_available": torch.cuda.is_available(),
        "gpu_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "accelerator": accelerator,
        "seed": SEED,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "learning_rate": 0.002,
        "elapsed_seconds": elapsed,
        "cells": adata.n_obs,
        "genes": adata.n_vars,
        "cell_types": adata.obs["major_cell_type"].nunique(),
        "loss_key": loss_key,
        "initial_loss": float(loss[0]),
        "final_loss": float(loss[-1]),
        "tail_25_epoch_slope": tail_slope,
        "minimum_signature_correlation": min(correlations.values()),
        "maximum_gpu_memory_mb": (
            float(torch.cuda.max_memory_allocated() / 2**20)
            if torch.cuda.is_available() and not args.posterior_only else None
        ),
        "postprocessing_from_saved_model": bool(args.posterior_only and args.finalize_existing_posterior),
    }
    (OUT / "reference_model_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
