"""Prepare exact-symbol cell2location inputs after Phase 4B spatial QC."""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import scanpy as sc
from scipy.io import mmread


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "phase4b" / "cell2location_input"
SCRNA = ROOT / "results" / "phase4a" / "phase4a_preliminary_integrated.h5ad"
HEALTHY_ROOT = ROOT / "data" / "raw" / "gse206621_healthy_spatial"
PI_ROOT = ROOT / "data" / "raw" / "pi_spatial" / "space ranger output"
HEALTHY = ["GSM6258251_A1", "GSM6258252_B1", "GSM6258253_C1", "GSM6258254_D1",
           "GSM6258255_A2", "GSM6258256_B2", "GSM6258257_C2", "GSM6258258_D2"]


def exact_unique_genes(values: pd.Series | pd.Index) -> tuple[pd.Index, pd.Index]:
    series = pd.Series(values.astype(str))
    duplicate = pd.Index(series[series.duplicated(keep=False)].unique())
    unique = pd.Index(series[~series.duplicated(keep=False)])
    return unique, duplicate


def healthy_features(sample: str) -> pd.DataFrame:
    return pd.read_csv(HEALTHY_ROOT / f"{sample}_features.tsv.gz", sep="\t", header=None,
                       names=["gene_id", "gene_symbol", "feature_type"], compression="gzip")


def healthy_positions(sample: str) -> pd.DataFrame:
    frame = pd.read_csv(HEALTHY_ROOT / f"{sample}_tissue_positions_list.csv.gz", header=None,
                        names=["barcode", "in_tissue", "array_row", "array_col", "pxl_row", "pxl_col"],
                        compression="gzip")
    return frame.set_index("barcode")


def build_healthy(sample: str, common: pd.Index) -> ad.AnnData:
    features = healthy_features(sample)
    matrix = mmread(HEALTHY_ROOT / f"{sample}_matrix.mtx.gz").tocsr().T
    with gzip.open(HEALTHY_ROOT / f"{sample}_barcodes.tsv.gz", "rt", encoding="utf-8") as handle:
        barcodes = [line.strip() for line in handle if line.strip()]
    unique_mask = ~features["gene_symbol"].duplicated(keep=False)
    lookup = pd.Series(np.flatnonzero(unique_mask), index=features.loc[unique_mask, "gene_symbol"])
    gene_index = lookup.loc[common].to_numpy()
    pos = healthy_positions(sample).loc[barcodes]
    tissue = pos["in_tissue"].astype(int).eq(1).to_numpy()
    obs = pos.iloc[tissue].copy()
    obs["sample_id"] = sample
    obs["condition"] = "HG"
    var = pd.DataFrame(index=common)
    var["gene_symbol"] = common
    var["gene_id"] = features.loc[gene_index, "gene_id"].to_numpy()
    result = ad.AnnData(matrix[tissue][:, gene_index], obs=obs, var=var)
    result.layers["counts"] = result.X.copy()
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    reference = ad.read_h5ad(SCRNA)
    scrna_genes, scrna_duplicates = exact_unique_genes(reference.var_names)

    pi = sc.read_10x_h5(PI_ROOT / "filtered_feature_bc_matrix.h5")
    pi_genes, pi_duplicates = exact_unique_genes(pi.var_names)
    healthy_sets, healthy_duplicates = {}, {}
    for sample in HEALTHY:
        features = healthy_features(sample)
        unique, duplicate = exact_unique_genes(features["gene_symbol"])
        healthy_sets[sample] = set(unique)
        healthy_duplicates[sample] = duplicate

    common = set(scrna_genes) & set(pi_genes)
    for genes in healthy_sets.values():
        common &= genes
    common = pd.Index(sorted(common))

    universe = sorted(set(scrna_genes) | set(pi_genes) | set().union(*healthy_sets.values()))
    intersection = pd.DataFrame({"gene_symbol": universe})
    intersection["in_scrna"] = intersection["gene_symbol"].isin(scrna_genes)
    intersection["in_pi_spatial"] = intersection["gene_symbol"].isin(pi_genes)
    for sample in HEALTHY:
        intersection[f"in_{sample}"] = intersection["gene_symbol"].isin(healthy_sets[sample])
    intersection["in_all_inputs"] = intersection["gene_symbol"].isin(common)
    intersection.to_csv(OUT / "gene_intersection.tsv", sep="\t", index=False)

    reference = reference[:, common].copy()
    if "counts" in reference.layers:
        reference.X = reference.layers["counts"].copy()
    reference.var["gene_symbol"] = reference.var_names.astype(str)
    reference.write_h5ad(OUT / "scrna_reference_counts.h5ad", compression="gzip")

    pi_lookup = pd.Series(np.arange(pi.n_vars), index=pi.var_names)
    pi = pi[:, pi_lookup.loc[common].to_numpy()].copy()
    pi.var_names = common
    pi.var["gene_symbol"] = common
    pi.obs["sample_id"] = "PI_spatial"
    pi.obs["condition"] = "PI"
    pi.layers["counts"] = pi.X.copy()
    pi.write_h5ad(OUT / "PI_spatial.h5ad", compression="gzip")

    spot_counts = [{"sample": "PI_spatial", "condition": "PI", "spots": pi.n_obs}]
    for sample in HEALTHY:
        spatial = build_healthy(sample, common)
        spatial.write_h5ad(OUT / f"{sample}.h5ad", compression="gzip")
        spot_counts.append({"sample": sample, "condition": "HG", "spots": spatial.n_obs})

    cell_counts = reference.obs.groupby(["major_cell_type", "annotation_confidence"], observed=True).size()
    cell_counts.rename("cells").reset_index().to_csv(OUT / "cells_per_cell_type.tsv", sep="\t", index=False)
    pd.DataFrame(spot_counts).to_csv(OUT / "spots_per_sample.tsv", sep="\t", index=False)
    duplicate_summary = {
        "scrna_duplicate_symbols": scrna_duplicates.tolist(),
        "pi_spatial_duplicate_symbols": pi_duplicates.tolist(),
        "healthy_duplicate_symbol_counts": {k: len(v) for k, v in healthy_duplicates.items()},
    }
    (OUT / "duplicate_gene_summary.json").write_text(json.dumps(duplicate_summary, indent=2), encoding="utf-8")
    summary = {
        "scrna_cells": int(reference.n_obs),
        "scrna_genes": int(len(scrna_genes)),
        "pi_spatial_genes": int(len(pi_genes)),
        "healthy_spatial_genes": {k: len(v) for k, v in healthy_sets.items()},
        "intersected_genes": int(len(common)),
        "cell_types": int(reference.obs["major_cell_type"].nunique()),
        "low_confidence_cells": int(reference.obs["annotation_confidence"].eq("low").sum()),
        "gene_matching": "exact unique gene symbols only; no fuzzy mapping",
        "spatial_spots": {row["sample"]: row["spots"] for row in spot_counts},
    }
    (OUT / "cell2location_input_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
