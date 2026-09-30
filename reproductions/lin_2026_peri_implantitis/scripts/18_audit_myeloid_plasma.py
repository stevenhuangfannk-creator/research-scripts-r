"""Targeted, non-destructive audit of preliminary myeloid and B/plasma labels."""
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
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results/phase4b/cell2location_input/scrna_reference_counts_curated_v1.h5ad"
FULL = ROOT / "results/phase4a/phase4a_preliminary_integrated.h5ad"
OUT = ROOT / "results/phase4a/myeloid_plasma_audit"
FIG = ROOT / "figures/phase4a/myeloid_plasma_audit"
TYPES = ["Macrophages", "Monocytes", "Dendritic cells", "Plasma cells", "B cells"]
MYELOID = ["C1QA", "C1QB", "C1QC", "CD68", "CD14", "FCGR3A", "LST1", "TYROBP", "CTSS", "FCER1G", "AIF1", "LGALS3", "MS4A7", "CTSD", "CTSB"]
B_PLASMA = ["CD79A", "CD79B", "MS4A1", "CD37", "CD74", "HLA-DRA", "CD19", "CD27", "CD38", "MZB1", "JCHAIN", "SDC1", "XBP1", "PRDM1", "IGHG1", "IGHG2", "IGHG3", "IGHG4", "IGKC", "IGLC1", "IGLC2"]
FOCUS = ["7", "12", "22", "35", "36", "44", "54", "25", "27", "26", "17", "18", "23"]

mpl.rcParams.update({"font.family": "sans-serif", "font.size": 7, "pdf.fonttype": 42,
                     "svg.fonttype": "none", "axes.spines.top": False, "axes.spines.right": False})


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIG / f"{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)


def fractions(counts, genes: pd.Index, prefix: tuple[str, ...]) -> np.ndarray:
    indices = np.flatnonzero(genes.str.startswith(prefix))
    total = np.asarray(counts.sum(axis=1)).ravel()
    selected = np.asarray(counts[:, indices].sum(axis=1)).ravel()
    return np.divide(selected, total, out=np.zeros_like(total, dtype=float), where=total > 0)


def table(obs: pd.DataFrame, name: str, rows: str, columns: str) -> None:
    pd.crosstab(obs[rows], obs[columns]).to_csv(OUT / f"{name}.tsv", sep="\t")


def marker_matrix(counts, var_names: pd.Index, labels: np.ndarray, genes: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    present = [g for g in genes if g in var_names]
    values = counts[:, var_names.get_indexer(present)].toarray()
    means = pd.DataFrame(values).groupby(labels).mean()
    detected = pd.DataFrame(values > 0).groupby(labels).mean()
    means.columns = detected.columns = present
    return means, detected


def dotplot(means: pd.DataFrame, detected: pd.DataFrame, genes: list[str], name: str) -> None:
    genes = [g for g in genes if g in means.columns]
    groups = [g for g in FOCUS if g in means.index]
    matrix = np.log1p(means.loc[groups, genes])
    matrix = matrix.div(matrix.max(axis=0).replace(0, 1), axis=1)
    fig, ax = plt.subplots(figsize=(max(8.0, len(genes) * 0.38), 4.2))
    for yi, group in enumerate(groups):
        for xi, gene in enumerate(genes):
            ax.scatter(xi, yi, s=12 + 140 * detected.loc[group, gene],
                       c=matrix.loc[group, gene], vmin=0, vmax=1, cmap="viridis", edgecolors="none")
    ax.set_xticks(range(len(genes)), genes, rotation=60, ha="right")
    ax.set_yticks(range(len(groups)), groups)
    ax.invert_yaxis()
    ax.set(xlim=(-0.6, len(genes) - 0.4), ylim=(len(groups) - 0.4, -0.6),
           title=f"{name}: color = relative mean, size = detected fraction", ylabel="Leiden cluster")
    fig.tight_layout()
    save(fig, f"dotplot_{name.lower()}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    backed = ad.read_h5ad(SOURCE, backed="r")
    full = ad.read_h5ad(FULL, backed="r")
    assert backed.obs_names.equals(full.obs_names)
    all_obs = backed.obs.copy()
    all_obs["leiden_scvi"] = all_obs["leiden_scvi"].astype(str)
    all_obs["major_cell_type"] = all_obs["major_cell_type"].astype(str)
    all_obs["sample_group"] = np.where(all_obs["sample_id"].astype(str).str.startswith("IGT"), "IGT", "HG")
    all_obs["igt_group"] = np.where(all_obs["sample_group"].eq("IGT"), all_obs["sample_id"].astype(str), "HG")
    macrophage = all_obs.loc[all_obs["major_cell_type"].eq("Macrophages")].copy()
    for name, col in [("macrophage_by_leiden", "leiden_scvi"), ("macrophage_by_sample", "sample_id"),
                      ("macrophage_by_igt_group", "igt_group"), ("macrophage_by_confidence", "annotation_confidence")]:
        macrophage[col].value_counts(dropna=False).rename("cells").to_csv(OUT / f"{name}.tsv", sep="\t", header=True)
    table(macrophage, "macrophage_leiden_by_sample", "leiden_scvi", "sample_id")
    table(all_obs, "all_cell_types_by_sample", "major_cell_type", "sample_id")

    selected = all_obs["major_cell_type"].isin(TYPES).to_numpy()
    x = full[selected].to_memory()
    x.obs = all_obs.loc[x.obs_names].copy()
    counts = x.layers["counts"] if "counts" in x.layers else x.X
    genes = pd.Index(x.var_names.astype(str))
    x.obs["ig_fraction_all_genes"] = fractions(counts, genes, ("IGH", "IGK", "IGL"))
    x.obs["ribo_fraction_all_genes"] = fractions(counts, genes, ("RPL", "RPS"))
    x.obs["mt_fraction_all_genes"] = fractions(counts, genes, ("MT-",))
    x.obs["all_gene_counts"] = np.asarray(counts.sum(axis=1)).ravel()
    x.obs.to_csv(OUT / "target_cells_metrics.tsv.gz", sep="\t", compression="gzip")
    x.obs.loc[x.obs["major_cell_type"].eq("Macrophages")].to_csv(
        OUT / "macrophage_cells.tsv.gz", sep="\t", compression="gzip")

    keys = ["total_counts", "n_genes_by_counts", "pct_counts_mt", "solo_doublet_probability",
            "ig_fraction_all_genes", "ribo_fraction_all_genes", "mt_fraction_all_genes"]
    x.obs.groupby(["major_cell_type", "sample_group"], observed=True)[keys].median().to_csv(
        OUT / "cell_type_group_medians.tsv", sep="\t")
    cluster_qc = x.obs.groupby(["leiden_scvi", "sample_group"], observed=True)[keys].agg(["count", "median"])
    cluster_qc.columns = [f"{metric}_{stat}" for metric, stat in cluster_qc.columns]
    cluster_qc.to_csv(OUT / "cluster_group_qc.tsv", sep="\t")
    igt3_qc = x.obs.loc[x.obs["major_cell_type"].eq("Macrophages")].groupby(
        x.obs["sample_id"].astype(str).eq("IGT3"), observed=True
    )[keys].agg(["count", "median", "mean"])
    igt3_qc.columns = [f"{metric}_{stat}" for metric, stat in igt3_qc.columns]
    igt3_qc.index = igt3_qc.index.map({False: "non_IGT3", True: "IGT3"})
    igt3_qc.to_csv(OUT / "macrophage_igt3_comparison.tsv", sep="\t")

    present = [g for g in MYELOID + B_PLASMA if g in genes]
    missing = [g for g in MYELOID + B_PLASMA if g not in genes]
    means, detected = marker_matrix(counts, genes, x.obs["leiden_scvi"].astype(str).to_numpy(), present)
    means.to_csv(OUT / "cluster_marker_mean_counts.tsv", sep="\t")
    detected.to_csv(OUT / "cluster_marker_detected_fraction.tsv", sep="\t")
    check_genes = ["PTPRC", "C1QA", "TYROBP", "COL1A1", "DCN", "MZB1", "JCHAIN", "IGKC"]
    check = pd.DataFrame(counts[:, genes.get_indexer(check_genes)].toarray() > 0,
                         columns=check_genes, index=x.obs_names)
    check["MZB1_and_COL1A1"] = check["MZB1"] & check["COL1A1"]
    check["MZB1_and_PTPRC"] = check["MZB1"] & check["PTPRC"]
    check["C1QA_and_MZB1"] = check["C1QA"] & check["MZB1"]
    check["COL1A1_and_PTPRC"] = check["COL1A1"] & check["PTPRC"]
    check["ig_fraction_gt_0_20"] = x.obs["ig_fraction_all_genes"].gt(0.20)
    check["solo_probability_gt_0_20"] = x.obs["solo_doublet_probability"].gt(0.20)
    check["leiden_scvi"] = x.obs["leiden_scvi"].astype(str)
    coexpression = check.loc[x.obs["major_cell_type"].eq("Macrophages")].groupby("leiden_scvi").agg(
        ["size", "mean"]
    )
    coexpression.columns = [f"{marker}_{stat}" for marker, stat in coexpression.columns]
    coexpression.to_csv(OUT / "macrophage_lineage_coexpression.tsv", sep="\t")
    labels = x.obs["leiden_scvi"].astype(str).to_numpy()
    library = np.asarray(counts.sum(axis=1)).ravel()
    scaled = counts.multiply(np.divide(1e4, library, out=np.zeros_like(library, dtype=float), where=library > 0)[:, None]).tocsr()
    total_scaled = np.asarray(scaled.sum(axis=0)).ravel()
    top_rows = []
    for group in FOCUS:
        mask = labels == group
        if not mask.any():
            continue
        inside = np.asarray(scaled[mask].sum(axis=0)).ravel()
        mean_in = inside / mask.sum()
        mean_out = (total_scaled - inside) / (~mask).sum()
        detected_in = np.asarray((counts[mask] > 0).mean(axis=0)).ravel()
        score = np.log2((mean_in + 0.1) / (mean_out + 0.1))
        score[(mean_in < 1) | (detected_in < 0.1)] = -np.inf
        for rank, idx in enumerate(np.argsort(score)[-30:][::-1], start=1):
            top_rows.append({"leiden_scvi": group, "cells": int(mask.sum()), "rank": rank,
                             "gene": genes[idx], "log2_mean_ratio": float(score[idx]),
                             "mean_counts_per_10k": float(mean_in[idx]),
                             "detected_fraction": float(detected_in[idx])})
    pd.DataFrame(top_rows).to_csv(OUT / "cluster_top_markers.tsv", sep="\t", index=False)
    dotplot(means, detected, MYELOID, "Myeloid")
    dotplot(means, detected, B_PLASMA, "B_plasma")

    groups = [g for g in FOCUS if g in means.index]
    z = np.log1p(means.loc[groups, present])
    z = z.sub(z.mean(axis=0), axis=1).div(z.std(axis=0).replace(0, 1), axis=1)
    fig, ax = plt.subplots(figsize=(11.0, 4.8))
    sns.heatmap(z, ax=ax, cmap="RdBu_r", center=0, vmin=-2, vmax=2, cbar_kws={"label": "Gene z score"})
    ax.set(xlabel="Marker gene", ylabel="Leiden cluster", title="Cluster-average lineage markers")
    ax.tick_params(axis="x", rotation=65, labelsize=6)
    fig.tight_layout()
    save(fig, "cluster_marker_heatmap")

    focus_obs = x.obs.loc[x.obs["leiden_scvi"].isin(groups)].copy()
    fig, axes = plt.subplots(1, 3, figsize=(11.0, 4.0))
    for ax, (key, ylabel) in zip(axes, [("ig_fraction_all_genes", "Ig count fraction"),
                                        ("n_genes_by_counts", "Detected genes"),
                                        ("solo_doublet_probability", "SOLO doublet probability")]):
        sns.violinplot(data=focus_obs, x="leiden_scvi", y=key, order=groups, inner=None,
                       color="#8ca9bf", cut=0, ax=ax)
        ax.set(xlabel="Leiden cluster", ylabel=ylabel)
        ax.tick_params(axis="x", rotation=60)
    fig.tight_layout()
    save(fig, "cluster_violin_qc")
    violin_markers = [gene for gene in ["C1QA", "CD68", "LST1", "MZB1", "JCHAIN", "IGKC"] if gene in genes]
    marker_values = np.log1p(scaled[:, genes.get_indexer(violin_markers)].toarray())
    marker_obs = pd.DataFrame(marker_values, columns=violin_markers)
    marker_obs["leiden_scvi"] = labels
    marker_obs = marker_obs.loc[marker_obs["leiden_scvi"].isin(groups)]
    fig, axes = plt.subplots(2, 3, figsize=(12.0, 6.5))
    for ax, gene in zip(axes.flat, violin_markers):
        sns.violinplot(data=marker_obs, x="leiden_scvi", y=gene, order=groups,
                       inner="quart", color="#8ca9bf", cut=0, ax=ax)
        ax.set(xlabel="Leiden cluster", ylabel="log1p(counts per 10k)", title=gene)
        ax.tick_params(axis="x", rotation=60)
    fig.tight_layout()
    save(fig, "cluster_violin_markers")
    summary = {"label_source": str(SOURCE.relative_to(ROOT)), "count_source": str(FULL.relative_to(ROOT)),
               "cells_total": int(backed.n_obs),
               "cells_audited": int(x.n_obs), "macrophage_cells": int(len(macrophage)),
               "genes_in_full_phase4a_object": int(x.n_vars), "marker_genes_missing": missing,
               "fraction_denominator": "raw counts across all 21,934 Phase 4A genes",
               "source_objects_modified": False}
    (OUT / "audit_inventory.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
