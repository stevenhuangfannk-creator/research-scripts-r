"""Quantitative QC for the formal cell2location reference signatures."""
from __future__ import annotations

import json
import argparse
from pathlib import Path

import anndata as ad
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "phase4b" / "cell2location_input" / "scrna_reference_counts.h5ad"
OUT = ROOT / "results" / "phase4b" / "cell2location_reference"
FIG = ROOT / "figures" / "phase4b" / "cell2location_reference"

MARKERS = {
    "B cells": ["CD79A", "MS4A1", "CD37", "CD74", "HLA-DRA"],
    "Dendritic cells": ["IRF7", "FCER1A", "CD1C", "CLEC10A", "HLA-DRA", "CST3"],
    "Epithelial cells": ["EPCAM", "KRT8", "KRT18", "KRT19", "KRT14", "KRT13", "KRT5", "TACSTD2"],
    "Fibroblasts": ["COL1A1", "COL1A2", "DCN", "LUM", "COL3A1"],
    "Lymphatic endothelium": ["PDPN", "LYVE1", "FLT4", "CCL21", "PROX1"],
    "Macrophages": ["C1QA", "C1QB", "C1QC", "APOE", "CD68", "LST1", "TYROBP", "FCER1G", "CTSS", "MS4A7"],
    "Mast cells": ["TPSAB1", "TPSB2", "KIT", "CPA3", "MS4A2"],
    "Monocytes": ["LST1", "LILRB1", "CTSS", "FCN1", "S100A8", "CTSD"],
    "NK cells": ["NKG7", "GNLY", "KLRD1", "PRF1", "GZMB"],
    "Neutrophils": ["FCGR3B", "CSF3R", "S100A8", "S100A9", "FPR1"],
    "Plasma cells": ["MZB1", "JCHAIN", "SDC1", "IGKC", "DERL3"],
    "Smooth muscle/pericytes": ["RGS5", "CSPG4", "MCAM", "ACTA2", "TAGLN"],
    "T cells": ["CD3D", "CD3E", "TRBC1", "TRBC2", "IL7R"],
    "Vascular endothelium": ["PECAM1", "VWF", "EMCN", "KDR", "ENG"],
}
NEUTROPHIL_DIAGNOSTIC_GENES = [
    "FDCSP", "TACSTD2", "SPRR2A", "FCGR3B", "CSF3R", "S100A8", "S100A9", "FPR1", "PTPRC"
]

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 7,
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


def mean_vector(matrix, mask: np.ndarray) -> np.ndarray:
    return np.asarray(matrix[mask].mean(axis=0)).ravel()


def safe_corr(a: np.ndarray, b: np.ndarray) -> float:
    valid = np.isfinite(a) & np.isfinite(b)
    if valid.sum() < 3 or np.std(a[valid]) == 0 or np.std(b[valid]) == 0:
        return np.nan
    return float(np.corrcoef(a[valid], b[valid])[0, 1])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--curated-v1", action="store_true")
    parser.add_argument("--curated-v2", action="store_true")
    args = parser.parse_args()
    if args.curated_v1 and args.curated_v2:
        parser.error("Select one curated reference version")
    global INPUT, OUT, FIG
    if args.curated_v1:
        INPUT = INPUT.with_name("scrna_reference_counts_curated_v1.h5ad")
        OUT = OUT / "curated_v1"
        FIG = FIG / "curated_v1"
    if args.curated_v2:
        INPUT = INPUT.parent / "curated_v2" / "scrna_reference_counts.h5ad"
        OUT = OUT / "curated_v2"
        FIG = FIG / "curated_v2"
    summary = json.loads((OUT / "reference_model_summary.json").read_text(encoding="utf-8"))
    history = pd.read_csv(OUT / "training_history.tsv", sep="\t", index_col=0)
    signatures = pd.read_csv(OUT / "reference_signatures.tsv.gz", sep="\t", index_col=0)
    correlations = pd.read_csv(
        OUT / "signature_naive_correlations.tsv", sep="\t", index_col=0
    ).iloc[:, 0]
    adata = ad.read_h5ad(INPUT)
    counts = adata.layers["counts"] if "counts" in adata.layers else adata.X
    labels = adata.obs["major_cell_type"].astype(str).to_numpy()
    samples = adata.obs["sample_id"].astype(str).to_numpy()
    confidence = adata.obs["annotation_confidence"].astype(str).to_numpy()

    low_rows = []
    batch_rows = []
    for cell_type in signatures.columns:
        cell_mask = labels == cell_type
        high_mask = cell_mask & (confidence != "low")
        overall = mean_vector(counts, cell_mask)
        high = mean_vector(counts, high_mask)
        expressed = (overall >= 0.05) | (high >= 0.05)
        log_fc = np.abs(np.log2((overall[expressed] + 0.05) / (high[expressed] + 0.05)))
        low_rows.append(
            {
                "cell_type": cell_type,
                "cells": int(cell_mask.sum()),
                "low_confidence_cells": int((cell_mask & (confidence == "low")).sum()),
                "low_confidence_fraction": float((cell_mask & (confidence == "low")).sum() / cell_mask.sum()),
                "log1p_mean_correlation_all_vs_provisional": safe_corr(
                    np.log1p(overall), np.log1p(high)
                ),
                "median_abs_log2_fold_change": float(np.median(log_fc)) if log_fc.size else 0.0,
                "p95_abs_log2_fold_change": float(np.quantile(log_fc, 0.95)) if log_fc.size else 0.0,
            }
        )
        for sample in np.unique(samples[cell_mask]):
            sample_mask = cell_mask & (samples == sample)
            if sample_mask.sum() < 50:
                continue
            sample_mean = mean_vector(counts, sample_mask)
            batch_rows.append(
                {
                    "cell_type": cell_type,
                    "sample_id": sample,
                    "cells": int(sample_mask.sum()),
                    "log1p_mean_correlation_to_cell_type_mean": safe_corr(
                        np.log1p(sample_mean), np.log1p(overall)
                    ),
                }
            )

    low = pd.DataFrame(low_rows).set_index("cell_type")
    low.to_csv(OUT / "low_confidence_signature_impact.tsv", sep="\t")
    batch = pd.DataFrame(batch_rows)
    batch.to_csv(OUT / "batch_signature_correlations.tsv", sep="\t", index=False)
    batch_summary = batch.groupby("cell_type").agg(
        qualifying_samples=("sample_id", "nunique"),
        minimum_sample_correlation=("log1p_mean_correlation_to_cell_type_mean", "min"),
        median_sample_correlation=("log1p_mean_correlation_to_cell_type_mean", "median"),
    )
    batch_summary.to_csv(OUT / "batch_signature_summary.tsv", sep="\t")
    representation = pd.crosstab(labels, samples)
    representation_summary = pd.DataFrame(
        {
            "cells": representation.sum(axis=1),
            "represented_samples": (representation > 0).sum(axis=1),
            "largest_sample": representation.idxmax(axis=1),
            "largest_sample_fraction": representation.max(axis=1) / representation.sum(axis=1),
        }
    )
    representation_summary.to_csv(OUT / "sample_representation_summary.tsv", sep="\t")

    neutrophil = labels == "Neutrophils"
    diagnostic_rows = []
    for cluster in np.unique(adata.obs.loc[neutrophil, "leiden_scvi"].astype(str)):
        cluster_mask = adata.obs["leiden_scvi"].astype(str).to_numpy() == cluster
        row = {"leiden_scvi": cluster, "cells": int(cluster_mask.sum())}
        for gene in NEUTROPHIL_DIAGNOSTIC_GENES:
            if gene in adata.var_names:
                row[f"{gene}_mean"] = float(
                    mean_vector(counts, cluster_mask)[adata.var_names.get_loc(gene)]
                )
        diagnostic_rows.append(row)
    pd.DataFrame(diagnostic_rows).to_csv(
        OUT / "neutrophil_cluster_diagnosis.tsv", sep="\t", index=False
    )

    dominance_rows = []
    top_rows = []
    marker_rows = []
    for cell_type in signatures.columns:
        values = signatures[cell_type].clip(lower=0).sort_values(ascending=False)
        total = float(values.sum())
        dominance_rows.append(
            {
                "cell_type": cell_type,
                "top_gene": str(values.index[0]),
                "top1_fraction": float(values.iloc[0] / total),
                "top10_fraction": float(values.iloc[:10].sum() / total),
                "nonzero_genes": int((values > 0).sum()),
            }
        )
        for rank, (gene, value) in enumerate(values.iloc[:30].items(), start=1):
            top_rows.append({"cell_type": cell_type, "rank": rank, "gene": gene, "signature": value})
        ranks = values.rank(ascending=False, method="min")
        for gene in MARKERS[cell_type]:
            if gene not in signatures.index:
                marker_rows.append(
                    {"cell_type": cell_type, "gene": gene, "available": False, "rank": np.nan,
                     "in_top_500": False, "specificity_log2_vs_max_other": np.nan}
                )
                continue
            other_max = signatures.loc[gene, signatures.columns != cell_type].max()
            marker_rows.append(
                {
                    "cell_type": cell_type,
                    "gene": gene,
                    "available": True,
                    "rank": int(ranks.loc[gene]),
                    "in_top_500": bool(ranks.loc[gene] <= 500),
                    "specificity_log2_vs_max_other": float(
                        np.log2((signatures.loc[gene, cell_type] + 0.01) / (other_max + 0.01))
                    ),
                }
            )

    dominance = pd.DataFrame(dominance_rows).set_index("cell_type")
    dominance.to_csv(OUT / "signature_dominance.tsv", sep="\t")
    top_genes = pd.DataFrame(top_rows)
    top_genes.to_csv(OUT / "signature_top_genes.tsv", sep="\t", index=False)
    marker = pd.DataFrame(marker_rows)
    marker.to_csv(OUT / "canonical_marker_audit.tsv", sep="\t", index=False)
    marker_summary = marker.groupby("cell_type").agg(
        available_markers=("available", "sum"),
        markers_in_top_500=("in_top_500", "sum"),
        median_marker_rank=("rank", "median"),
        median_specificity_log2=("specificity_log2_vs_max_other", "median"),
    )
    marker_summary.to_csv(OUT / "canonical_marker_summary.tsv", sep="\t")
    ig_mask = signatures.index.str.startswith(("IGH", "IGK", "IGL"))
    ig_fraction = signatures.loc[ig_mask].sum(axis=0) / signatures.sum(axis=0)
    ig_fraction.rename("ig_signature_fraction").to_csv(OUT / "immunoglobulin_signature_fraction.tsv", sep="\t", header=True)
    macrophage_ig_top10 = int(top_genes.loc[
        top_genes["cell_type"].eq("Macrophages") & top_genes["rank"].le(10), "gene"
    ].str.startswith(("IGH", "IGK", "IGL")).sum())

    loss_col = next(c for c in history.columns if "elbo" in c.lower())
    loss = history[loss_col].dropna().to_numpy(float)
    tail = loss[-min(25, len(loss)) :]
    relative_tail_slope = float(np.polyfit(np.arange(len(tail)), tail, 1)[0] / np.median(tail))
    excessive_dominance = dominance.loc[dominance["top1_fraction"] >= 0.10]
    expected_plasma_ig = all(
        cell_type == "Plasma cells" and gene.startswith(("IGK", "IGL", "IGH"))
        for cell_type, gene in excessive_dominance["top_gene"].items()
    )
    gates = {
        "loss_finite": bool(np.isfinite(loss).all()),
        "loss_decreased": bool(loss[-1] < loss[0]),
        "tail_relative_slope_abs_lt_0_002": bool(abs(relative_tail_slope) < 0.002),
        "fourteen_finite_nonnegative_signatures": bool(
            signatures.shape[1] == 14
            and np.isfinite(signatures.to_numpy()).all()
            and (signatures.to_numpy() >= 0).all()
        ),
        "minimum_posterior_naive_correlation_ge_0_75": bool(correlations.min() >= 0.75),
        "no_unexplained_top1_signature_fraction_ge_0_10": bool(expected_plasma_ig),
        "low_confidence_logmean_correlation_ge_0_95": bool(
            low.loc[low["low_confidence_cells"] > 0, "log1p_mean_correlation_all_vs_provisional"].min()
            >= 0.95
        ),
        "median_batch_correlation_ge_0_70": bool(
            batch_summary["median_sample_correlation"].min() >= 0.70
        ),
        "at_least_one_canonical_marker_top500_each_type": bool(
            (marker_summary["markers_in_top_500"] >= 1).all()
        ),
        "macrophage_core_marker_top500": bool(
            marker.loc[
                marker["cell_type"].eq("Macrophages")
                & marker["gene"].isin(["C1QA", "C1QB", "C1QC", "CD68"]),
                "in_top_500",
            ].any()
        ),
        "macrophage_ig_fraction_lt_0_02": bool(ig_fraction["Macrophages"] < 0.02),
        "macrophage_ig_genes_in_top10_le_2": bool(macrophage_ig_top10 <= 2),
        "neutrophil_fcgr3b_or_csf3r_top500": bool(marker.loc[
            marker["cell_type"].eq("Neutrophils") & marker["gene"].isin(["FCGR3B", "CSF3R"]),
            "in_top_500",
        ].any()),
    }
    qc = {
        "relative_tail_25_epoch_slope": relative_tail_slope,
        "minimum_posterior_naive_correlation": float(correlations.min()),
        "maximum_top1_fraction": float(dominance["top1_fraction"].max()),
        "top1_fraction_exceptions": excessive_dominance[["top_gene", "top1_fraction"]].to_dict(orient="index"),
        "minimum_low_confidence_correlation": float(
            low.loc[low["low_confidence_cells"] > 0, "log1p_mean_correlation_all_vs_provisional"].min()
        ),
        "minimum_median_batch_correlation": float(batch_summary["median_sample_correlation"].min()),
        "types_over_0_75_single_sample_fraction": representation_summary.loc[
            representation_summary["largest_sample_fraction"] > 0.75,
            ["largest_sample", "largest_sample_fraction"],
        ].to_dict(orient="index"),
        "macrophage_ig_signature_fraction": float(ig_fraction["Macrophages"]),
        "macrophage_ig_genes_in_top10": macrophage_ig_top10,
        "gates": gates,
        "automatic_gate_pass": bool(all(gates.values())),
    }
    (OUT / "reference_qc_summary.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")

    fig, axes = plt.subplots(1, 3, figsize=(11.0, 5.3))
    correlations.sort_values().plot.barh(ax=axes[0], color="#5f7f9d")
    axes[0].axvline(0.75, color="#b3473f", linestyle="--", linewidth=0.8)
    axes[0].set(xlabel="Pearson r", ylabel="", title="Posterior vs. cluster mean")
    affected = low[low["low_confidence_cells"] > 0].sort_values(
        "log1p_mean_correlation_all_vs_provisional"
    )
    affected["log1p_mean_correlation_all_vs_provisional"].plot.barh(
        ax=axes[1], color="#789b78"
    )
    axes[1].axvline(0.95, color="#b3473f", linestyle="--", linewidth=0.8)
    axes[1].set(xlabel="Pearson r", ylabel="", title="Retained vs. provisional-only mean")
    batch_summary["median_sample_correlation"].sort_values().plot.barh(
        ax=axes[2], color="#aa8260"
    )
    axes[2].axvline(0.70, color="#b3473f", linestyle="--", linewidth=0.8)
    axes[2].set(xlabel="Median Pearson r", ylabel="", title="Across-sample stability")
    for ax in axes:
        ax.tick_params(axis="y", labelsize=6)
        ax.set_xlim(0.68, 1.01)
    fig.tight_layout()
    save_figure(fig, "reference_signature_qc")

    ordered_types = list(signatures.columns)
    marker_genes = list(dict.fromkeys(g for ct in ordered_types for g in MARKERS[ct] if g in signatures.index))
    matrix = np.log1p(signatures.loc[marker_genes, ordered_types])
    matrix = matrix.sub(matrix.mean(axis=1), axis=0).div(matrix.std(axis=1).replace(0, 1), axis=0)
    fig, ax = plt.subplots(figsize=(8.2, 9.0))
    image = ax.imshow(matrix, aspect="auto", cmap="RdBu_r", vmin=-2.5, vmax=2.5)
    ax.set_xticks(range(len(ordered_types)), ordered_types, rotation=55, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(len(marker_genes)), marker_genes)
    ax.set(title="Canonical marker structure in posterior signatures")
    fig.colorbar(image, ax=ax, label="Row z score", fraction=0.025, pad=0.02)
    fig.tight_layout()
    save_figure(fig, "reference_canonical_marker_heatmap")
    print(json.dumps(qc, indent=2))


if __name__ == "__main__":
    main()
