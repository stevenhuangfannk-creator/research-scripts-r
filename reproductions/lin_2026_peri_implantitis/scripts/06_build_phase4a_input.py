"""Build the PI + healthy gingiva pre-doublet AnnData input."""

from __future__ import annotations

import gzip
import json
import tomllib
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import scanpy as sc
from scipy.io import mmread


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PI_ROOT = PROJECT_ROOT / "data" / "raw" / "pi_scrna"
HG_ROOT = PROJECT_ROOT / "data" / "raw" / "gse164241_healthy_gingiva"
OUTPUT_ROOT = PROJECT_ROOT / "results" / "phase4a"


def load_config() -> dict:
    with (PROJECT_ROOT / "config" / "analysis.toml").open("rb") as handle:
        return tomllib.load(handle)


def add_qc(adata: ad.AnnData) -> None:
    adata.var["mt"] = adata.var_names.str.upper().str.startswith("MT-")
    sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], percent_top=None, log1p=False, inplace=True)


def attach_metadata(adata: ad.AnnData, *, sample_id: str, donor_id: str, condition: str, source: str) -> None:
    adata.obs_names = pd.Index([f"{sample_id}:{barcode}" for barcode in adata.obs_names])
    adata.obs["sample_id"] = sample_id
    adata.obs["donor_id"] = donor_id
    adata.obs["condition"] = condition
    adata.obs["source_dataset"] = source


def read_healthy(directory: Path) -> ad.AnnData:
    matrix_path = next(directory.glob("*_matrix.mtx.gz"))
    barcode_path = next(directory.glob("*_barcodes.tsv.gz"))
    feature_paths = list(directory.glob("*_features.tsv.gz")) + list(directory.glob("*_genes.tsv.gz"))
    if len(feature_paths) != 1:
        raise ValueError(f"expected one feature table in {directory}")
    features = pd.read_csv(feature_paths[0], sep="\t", header=None, compression="gzip")
    with gzip.open(barcode_path, "rt", encoding="utf-8") as handle:
        barcodes = [line.rstrip("\n") for line in handle]
    matrix = mmread(matrix_path).tocsr().transpose().tocsr()
    var = pd.DataFrame(index=pd.Index(features.iloc[:, 1].astype(str), name="gene_symbol"))
    var["gene_id"] = features.iloc[:, 0].astype(str).to_numpy()
    adata = ad.AnnData(X=matrix, obs=pd.DataFrame(index=barcodes), var=var)
    adata.var_names_make_unique()
    return adata


def main() -> int:
    config = load_config()["phase4a"]
    pi_qc = config["qc"]
    hg_qc = config["healthy_qc"]
    pi_samples = pd.read_csv(PROJECT_ROOT / "config" / "pi_samples.tsv", sep="\t")
    hg_samples = pd.read_csv(PROJECT_ROOT / "config" / "healthy_samples.tsv", sep="\t")
    objects: list[ad.AnnData] = []
    counts: list[dict[str, object]] = []

    for sample in pi_samples.itertuples(index=False):
        matches = [
            path
            for path in PI_ROOT.rglob(f"{sample.sample_id}_filtered_feature_bc_matrix.h5")
            if "__MACOSX" not in path.parts
        ]
        if len(matches) != 1:
            raise ValueError(f"expected one H5 for {sample.sample_id}")
        adata = sc.read_10x_h5(matches[0], gex_only=True)
        adata.var_names_make_unique()
        add_qc(adata)
        keep = (
            (adata.obs["pct_counts_mt"] <= float(pi_qc["max_pct_mito"]))
            & (adata.obs["n_genes_by_counts"] >= int(pi_qc["min_genes"]))
            & (adata.obs["n_genes_by_counts"] <= int(pi_qc["max_genes"]))
        )
        counts.append({"sample_id": sample.sample_id, "condition": "PI", "raw": adata.n_obs, "retained": int(keep.sum())})
        adata = adata[keep].copy()
        attach_metadata(adata, sample_id=sample.sample_id, donor_id=sample.donor_id, condition="PI", source="Zenodo:19697597")
        objects.append(adata)

    for sample in hg_samples.itertuples(index=False):
        adata = read_healthy(HG_ROOT / sample.sample_id)
        add_qc(adata)
        keep = (
            (adata.obs["pct_counts_mt"] < float(hg_qc["max_pct_mito"]))
            & (adata.obs["n_genes_by_counts"] > int(hg_qc["min_genes_exclusive"]))
            & (adata.obs["n_genes_by_counts"] < int(hg_qc["max_genes_exclusive"]))
        )
        counts.append({"sample_id": sample.sample_id, "condition": "HG", "raw": adata.n_obs, "retained": int(keep.sum())})
        adata = adata[keep].copy()
        attach_metadata(adata, sample_id=sample.sample_id, donor_id=sample.donor_id, condition="HG", source="GSE164241")
        objects.append(adata)

    combined = ad.concat(objects, join="inner", merge="same", index_unique=None)
    combined.obs["sample_id"] = combined.obs["sample_id"].astype("category")
    combined.obs["donor_id"] = combined.obs["donor_id"].astype("category")
    combined.obs["condition"] = combined.obs["condition"].astype("category")
    combined.obs["source_dataset"] = combined.obs["source_dataset"].astype("category")
    combined.layers["counts"] = combined.X.copy()
    combined.uns["reconstruction"] = {
        "pi_qc": "USER/CODEX ANALYTICAL CHOICE",
        "healthy_qc": "METHOD-BASED RECONSTRUCTION",
        "doublet_removal": "NOT YET APPLIED",
    }

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_ROOT / "phase4a_pre_doublet.h5ad"
    combined.write_h5ad(output, compression="gzip")
    count_table = pd.DataFrame(counts)
    count_table.to_csv(OUTPUT_ROOT / "phase4a_pre_doublet_counts.tsv", sep="\t", index=False)
    summary = {
        "cells": int(combined.n_obs),
        "genes_intersection": int(combined.n_vars),
        "samples": int(combined.obs["sample_id"].nunique()),
        "donors": int(combined.obs["donor_id"].nunique()),
        "condition_counts": {key: int(value) for key, value in combined.obs["condition"].value_counts().items()},
        "paper_reported_final_cells": 90551,
        "difference_before_doublet_removal": int(combined.n_obs - 90551),
        "output": str(output.relative_to(PROJECT_ROOT)),
    }
    (OUTPUT_ROOT / "phase4a_pre_doublet_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
