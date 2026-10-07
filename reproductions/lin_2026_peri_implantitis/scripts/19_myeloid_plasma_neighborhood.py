"""Local PCA/neighborhood audit; never writes to the Phase 4A source object."""
from __future__ import annotations

import json
from pathlib import Path

import anndata as ad
import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
from scipy.sparse.csgraph import connected_components


ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "results/phase4a/phase4a_preliminary_integrated.h5ad"
CURATED = ROOT / "results/phase4b/cell2location_input/scrna_reference_counts_curated_v1.h5ad"
OUT = ROOT / "results/phase4a/myeloid_plasma_audit"
FIG = ROOT / "figures/phase4a/myeloid_plasma_audit"
TYPES = ["Macrophages", "Monocytes", "Dendritic cells", "Plasma cells", "B cells"]
MARKERS = ["C1QA", "C1QB", "C1QC", "CD68", "CD14", "FCN1", "LST1", "TYROBP", "FCER1G", "CTSS",
           "MS4A7", "CCL18", "APOE", "FCER1A", "CLEC10A", "MZB1", "JCHAIN", "IGKC", "CD79A",
           "MS4A1", "COL1A1", "DCN", "DCT", "PMEL", "CTSK", "ACP5", "KRT14", "EPCAM"]
SEED = 20260928

mpl.rcParams.update({"font.family": "sans-serif", "font.size": 7, "pdf.fonttype": 42,
                     "svg.fonttype": "none", "axes.spines.top": False, "axes.spines.right": False})


def main() -> None:
    sc.settings.verbosity = 1
    source = ad.read_h5ad(FULL, backed="r")
    labels = ad.read_h5ad(CURATED, backed="r")
    assert source.obs_names.equals(labels.obs_names)
    keep = labels.obs["major_cell_type"].astype(str).isin(TYPES).to_numpy()
    x = source[keep].to_memory()
    x.obs = labels.obs.loc[x.obs_names].copy()
    x.obs["major_cell_type"] = x.obs["major_cell_type"].astype(str)
    x.obs["leiden_scvi"] = x.obs["leiden_scvi"].astype(str)
    raw = x.layers["counts"].tocsr()
    sc.pp.highly_variable_genes(x, n_top_genes=2500, flavor="seurat_v3",
                               layer="counts")
    pd.DataFrame({"gene": x.var_names, "highly_variable": x.var["highly_variable"].to_numpy()}).to_csv(
        OUT / "local_hvg_set.tsv", sep="\t", index=False)
    work = x[:, x.var["highly_variable"].to_numpy()].copy()
    work.X = work.layers["counts"].copy()
    work.uns.pop("log1p", None)
    sc.pp.normalize_total(work, target_sum=1e4)
    sc.pp.log1p(work)
    sc.tl.pca(work, n_comps=30, svd_solver="arpack", random_state=SEED)
    sc.pp.neighbors(work, n_neighbors=20, n_pcs=30, random_state=SEED)
    components, component_label = connected_components(work.obsp["connectivities"], directed=False)
    sc.tl.leiden(work, resolution=0.6, random_state=SEED, flavor="igraph",
                 n_iterations=2, directed=False, key_added="audit_leiden")
    sc.tl.umap(work, random_state=SEED)
    x.obs["audit_leiden"] = work.obs["audit_leiden"].astype(str).to_numpy()
    x.obs["neighbor_component"] = component_label
    x.obs["umap_1"] = work.obsm["X_umap"][:, 0]
    x.obs["umap_2"] = work.obsm["X_umap"][:, 1]
    x.obs["pca_1"] = work.obsm["X_pca"][:, 0]
    x.obs["pca_2"] = work.obsm["X_pca"][:, 1]
    metrics = pd.read_csv(OUT / "target_cells_metrics.tsv.gz", sep="\t", index_col=0)
    x.obs["ig_fraction_all_genes"] = metrics.loc[x.obs_names, "ig_fraction_all_genes"].to_numpy()
    x.obs.to_csv(OUT / "local_embedding.tsv.gz", sep="\t", compression="gzip")
    pd.crosstab(x.obs["audit_leiden"], x.obs["major_cell_type"]).to_csv(
        OUT / "local_leiden_by_prior_label.tsv", sep="\t")
    pd.crosstab(x.obs["audit_leiden"], x.obs["leiden_scvi"]).to_csv(
        OUT / "local_leiden_by_original_leiden.tsv", sep="\t")
    pd.crosstab(x.obs["audit_leiden"], x.obs["sample_id"]).to_csv(
        OUT / "local_leiden_by_sample.tsv", sep="\t")
    present = [gene for gene in MARKERS if gene in x.var_names]
    marker_counts = raw[:, x.var_names.get_indexer(present)].toarray()
    marker_means = pd.DataFrame(marker_counts, columns=present).groupby(x.obs["audit_leiden"].to_numpy()).mean()
    marker_means.to_csv(OUT / "local_cluster_marker_means.tsv", sep="\t")
    pd.DataFrame(marker_counts > 0, columns=present).groupby(x.obs["audit_leiden"].to_numpy()).mean().to_csv(
        OUT / "local_cluster_marker_detected.tsv", sep="\t")

    keys = ["major_cell_type", "leiden_scvi", "audit_leiden"]
    fig, axes = plt.subplots(1, 4, figsize=(15.0, 3.9))
    for ax, key in zip(axes[:3], keys):
        category = x.obs[key].astype(str)
        codes, names = pd.factorize(category, sort=True)
        ax.scatter(x.obs["umap_1"], x.obs["umap_2"], c=codes, cmap="tab20",
                   s=1.5, alpha=0.6, linewidths=0, rasterized=True)
        ax.set_title(f"Local UMAP: {key} ({len(names)} groups)")
        ax.set(xlabel="UMAP 1", ylabel="UMAP 2")
        if key == "major_cell_type":
            for index, name in enumerate(names):
                ax.scatter([], [], color=plt.get_cmap("tab20")(index / (len(names) - 1)),
                           s=15, label=name)
            ax.legend(loc="upper left", fontsize=5, markerscale=1, frameon=False)
    colors = np.clip(x.obs["ig_fraction_all_genes"].to_numpy(float), 0, 0.75)
    im = axes[3].scatter(x.obs["umap_1"], x.obs["umap_2"], c=colors,
                         cmap="magma", vmin=0, vmax=0.75, s=1.5, linewidths=0, rasterized=True)
    axes[3].set(title="Ig fraction (full counts)", xlabel="UMAP 1", ylabel="UMAP 2")
    fig.colorbar(im, ax=axes[3], label="Ig fraction", fraction=0.04)
    fig.tight_layout()
    fig.savefig(FIG / "local_umap_overview.png", dpi=300, bbox_inches="tight")
    fig.savefig(FIG / "local_umap_overview.pdf", bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.7))
    for ax, sample in zip(axes, ["IGT3", "other samples"]):
        mask = x.obs["sample_id"].astype(str).eq("IGT3").to_numpy()
        if sample == "other samples":
            mask = ~mask
        ax.scatter(x.obs.loc[~mask, "umap_1"], x.obs.loc[~mask, "umap_2"],
                   s=1, c="#cccccc", linewidths=0, rasterized=True)
        ax.scatter(x.obs.loc[mask, "umap_1"], x.obs.loc[mask, "umap_2"],
                   s=2, c="#a34b42", alpha=0.6, linewidths=0, rasterized=True)
        ax.set(title=f"{sample} (n={mask.sum():,})", xlabel="UMAP 1", ylabel="UMAP 2")
    fig.tight_layout()
    fig.savefig(FIG / "local_umap_igt3.png", dpi=300, bbox_inches="tight")
    fig.savefig(FIG / "local_umap_igt3.pdf", bbox_inches="tight")
    plt.close(fig)

    labels_local = x.obs["audit_leiden"].astype(str).to_numpy()
    library = np.asarray(raw.sum(axis=1)).ravel()
    scaled = raw.multiply(np.divide(1e4, library, out=np.zeros_like(library, dtype=float), where=library > 0)[:, None]).tocsr()
    total = np.asarray(scaled.sum(axis=0)).ravel()
    rows = []
    for cluster in np.unique(labels_local):
        mask = labels_local == cluster
        inside = np.asarray(scaled[mask].sum(axis=0)).ravel()
        mean_in = inside / mask.sum()
        mean_out = (total - inside) / (~mask).sum()
        detected = np.asarray((raw[mask] > 0).mean(axis=0)).ravel()
        score = np.log2((mean_in + 0.1) / (mean_out + 0.1))
        score[(mean_in < 1) | (detected < 0.1)] = -np.inf
        for rank, idx in enumerate(np.argsort(score)[-20:][::-1], start=1):
            rows.append({"audit_leiden": cluster, "cells": int(mask.sum()), "rank": rank,
                         "gene": x.var_names[idx], "log2_mean_ratio": float(score[idx]),
                         "mean_counts_per_10k": float(mean_in[idx]), "detected_fraction": float(detected[idx])})
    pd.DataFrame(rows).to_csv(OUT / "local_cluster_top_markers.tsv", sep="\t", index=False)
    summary = {"cells": int(x.n_obs), "genes": int(x.n_vars), "hvg": int(work.n_vars),
               "hvg_batch_key": None,
               "pca_dimensions": 30, "neighbors": 20, "leiden_resolution": 0.6,
               "seed": SEED, "local_clusters": int(x.obs["audit_leiden"].nunique()),
               "neighbor_graph_components": int(components),
               "source_objects_modified": False}
    (OUT / "local_analysis_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
