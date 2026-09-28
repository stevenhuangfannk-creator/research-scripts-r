"""Create a preliminary scVI/UMAP reconstruction and evidence-based major labels."""

from __future__ import annotations

import json
import os
import tomllib
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
import scvi
import torch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PROJECT_ROOT / "results" / "phase4a"
FIGURE_ROOT = PROJECT_ROOT / "figures" / "phase4a"
MODEL_ROOT = OUTPUT_ROOT / "models" / "solo_scvi"

MARKERS = {
    "B cells": ["MS4A1", "CD79A", "CD79B", "CD19"],
    "Dendritic cells": ["IRF7", "FCER1A", "CD1C", "CLEC10A"],
    "T cells": ["CD3D", "CD3E", "TRAC", "IL7R"],
    "NK cells": ["NKG7", "GNLY", "KLRD1", "NCR1"],
    "Neutrophils": ["CSF3R", "FCGR3B", "FPR1", "S100A8", "S100A9"],
    "Monocytes": ["LST1", "FCN1", "CTSS", "LYZ"],
    "Macrophages": ["C1QA", "C1QB", "C1QC", "APOE"],
    "Plasma cells": ["MZB1", "JCHAIN", "SDC1", "CD79A"],
    "Epithelial cells": ["KRT14", "KRT5", "KRT19", "EPCAM"],
    "Fibroblasts": ["COL1A1", "COL1A2", "DCN", "LUM"],
    "Vascular endothelium": ["PECAM1", "VWF", "EMCN", "KDR"],
    "Lymphatic endothelium": ["PROX1", "PDPN", "LYVE1", "FLT4"],
    "Smooth muscle/pericytes": ["ACTA2", "TAGLN", "MYL9", "RGS5"],
    "Mast cells": ["TPSAB1", "TPSB2", "CPA3", "MS4A2"],
}


def main() -> int:
    with (PROJECT_ROOT / "config" / "analysis.toml").open("rb") as handle:
        config = tomllib.load(handle)
    seed = int(config["project"]["random_seed"])
    n_hvg = int(config["phase4a"]["features"]["n_highly_variable_genes"])
    n_neighbors = int(config["phase4a"]["neighbors"]["n_neighbors"])
    resolution = float(config["phase4a"]["clustering"]["leiden_resolution"])
    scvi.settings.seed = seed
    torch.set_num_threads(min(8, os.cpu_count() or 1))

    pre = sc.read_h5ad(OUTPUT_ROOT / "phase4a_pre_doublet.h5ad")
    training = pre.copy()
    sc.pp.highly_variable_genes(
        training,
        n_top_genes=n_hvg,
        flavor="seurat_v3",
        layer="counts",
        batch_key="sample_id",
        subset=True,
    )
    model = scvi.model.SCVI.load(MODEL_ROOT, adata=training)
    latent = pd.DataFrame(model.get_latent_representation(), index=training.obs_names)
    del training, pre

    adata = sc.read_h5ad(OUTPUT_ROOT / "phase4a_post_doublet.h5ad")
    adata.obsm["X_scVI"] = latent.loc[adata.obs_names].to_numpy()
    sc.pp.neighbors(adata, n_neighbors=n_neighbors, use_rep="X_scVI", random_state=seed)
    sc.tl.umap(adata, random_state=seed)
    sc.tl.leiden(
        adata,
        resolution=resolution,
        random_state=seed,
        flavor="igraph",
        n_iterations=2,
        directed=False,
        key_added="leiden_scvi",
    )

    adata.X = adata.layers["counts"].copy()
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)

    clusters = adata.obs["leiden_scvi"].cat.categories
    marker_genes = sorted({gene for genes in MARKERS.values() for gene in genes if gene in adata.var_names})
    cluster_means = pd.DataFrame(index=clusters, columns=marker_genes, dtype=float)
    for cluster in clusters:
        subset = adata[adata.obs["leiden_scvi"] == cluster, marker_genes]
        cluster_means.loc[cluster] = np.asarray(subset.X.mean(axis=0)).ravel()
    gene_std = cluster_means.std(axis=0).replace(0, np.nan)
    zscores = (cluster_means - cluster_means.mean(axis=0)) / gene_std
    signature_scores = pd.DataFrame(index=clusters)
    for label, genes in MARKERS.items():
        present = [gene for gene in genes if gene in zscores.columns]
        signature_scores[label] = zscores[present].mean(axis=1)

    top_label = signature_scores.idxmax(axis=1)
    ordered = np.sort(signature_scores.to_numpy(), axis=1)
    margin = ordered[:, -1] - ordered[:, -2]
    annotations = pd.DataFrame(
        {
            "leiden_scvi": clusters,
            "major_cell_type": top_label.to_numpy(),
            "top_vs_second_score_margin": margin,
            "annotation_confidence": np.where(margin >= 0.25, "provisional", "low"),
            "cells": [int((adata.obs["leiden_scvi"] == cluster).sum()) for cluster in clusters],
        }
    ).set_index("leiden_scvi")
    adata.obs["major_cell_type"] = adata.obs["leiden_scvi"].map(annotations["major_cell_type"]).astype("category")
    adata.obs["annotation_confidence"] = adata.obs["leiden_scvi"].map(
        annotations["annotation_confidence"]
    ).astype("category")
    adata.uns["reconstruction"]["integration_embedding"] = (
        "PRELIMINARY MODERNIZED IMPLEMENTATION: pre-doublet scVI base model, singlets projected"
    )
    adata.uns["reconstruction"]["major_cell_annotation"] = (
        "METHOD-BASED RECONSTRUCTION: paper markers plus expanded canonical marker sets"
    )

    signature_scores.to_csv(OUTPUT_ROOT / "cluster_signature_scores.tsv", sep="\t")
    cluster_means.to_csv(OUTPUT_ROOT / "cluster_marker_means.tsv", sep="\t")
    annotations.to_csv(OUTPUT_ROOT / "cluster_annotations.tsv", sep="\t")
    cell_counts = (
        adata.obs.groupby(["condition", "major_cell_type"], observed=True)
        .size()
        .rename("cells")
        .reset_index()
    )
    cell_counts.to_csv(OUTPUT_ROOT / "major_cell_counts_by_condition.tsv", sep="\t", index=False)
    adata.write_h5ad(OUTPUT_ROOT / "phase4a_preliminary_integrated.h5ad", compression="gzip")

    FIGURE_ROOT.mkdir(parents=True, exist_ok=True)
    figure = sc.pl.umap(
        adata,
        color=["condition", "major_cell_type", "annotation_confidence"],
        ncols=3,
        frameon=False,
        wspace=0.35,
        show=False,
        return_fig=True,
    )
    figure.suptitle("Lin 2026 Figure 1a method-based reconstruction (preliminary)", y=1.02)
    figure.savefig(FIGURE_ROOT / "figure1a_preliminary_umap.png", dpi=300, bbox_inches="tight")
    figure.savefig(FIGURE_ROOT / "figure1a_preliminary_umap.pdf", bbox_inches="tight")
    plt.close(figure)

    summary = {
        "classification": "METHOD-BASED RECONSTRUCTION / PRELIMINARY",
        "cells": int(adata.n_obs),
        "genes": int(adata.n_vars),
        "clusters": int(len(clusters)),
        "major_labels": int(adata.obs["major_cell_type"].nunique()),
        "low_confidence_cells": int((adata.obs["annotation_confidence"] == "low").sum()),
        "embedding_model": "pre-doublet scVI base; retraining decision pending validation",
    }
    (OUTPUT_ROOT / "preliminary_integration_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(annotations.to_string())
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
