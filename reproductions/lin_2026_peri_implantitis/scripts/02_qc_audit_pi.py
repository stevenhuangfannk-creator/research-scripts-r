"""Audit paper-reported and reconstruction QC thresholds on PI matrices."""

from __future__ import annotations

import csv
import json
import tomllib
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_ROOT = PROJECT_ROOT / "data" / "raw" / "pi_scrna"
OUTPUT_ROOT = PROJECT_ROOT / "results" / "phase4a"


def read_config() -> tuple[float, int]:
    with (PROJECT_ROOT / "config" / "analysis.toml").open("rb") as handle:
        config = tomllib.load(handle)
    qc = config["phase4a"]["qc"]
    return float(qc["max_pct_mito"]), int(qc["min_genes"])


def read_samples() -> pd.DataFrame:
    return pd.read_csv(PROJECT_ROOT / "config" / "pi_samples.tsv", sep="\t").set_index("sample_id")


def h5_for_sample(sample_id: str) -> Path:
    matches = [
        path
        for path in INPUT_ROOT.rglob(f"{sample_id}_filtered_feature_bc_matrix.h5")
        if "__MACOSX" not in path.parts and not path.name.startswith("._")
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one H5 for {sample_id}, found {len(matches)}")
    return matches[0]


def quantiles(values: pd.Series, metric: str, sample_id: str) -> list[dict[str, object]]:
    return [
        {
            "sample_id": sample_id,
            "metric": metric,
            "quantile": label,
            "value": float(np.quantile(values, probability)),
        }
        for label, probability in (("min", 0), ("p01", 0.01), ("p05", 0.05), ("median", 0.5), ("p95", 0.95), ("p99", 0.99), ("max", 1))
    ]


def main() -> int:
    max_pct_mito, min_genes = read_config()
    samples = read_samples()
    count_rows: list[dict[str, object]] = []
    quantile_rows: list[dict[str, object]] = []

    for sample_id, metadata in samples.iterrows():
        path = h5_for_sample(sample_id)
        adata = sc.read_10x_h5(path, gex_only=True)
        adata.var_names_make_unique()
        adata.var["mt"] = adata.var_names.str.upper().str.startswith("MT-")
        sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], percent_top=None, log1p=False, inplace=True)

        pass_mito = adata.obs["pct_counts_mt"] <= max_pct_mito
        pass_genes = adata.obs["n_genes_by_counts"] >= min_genes
        pass_reconstruction_qc = pass_mito & pass_genes
        reported = int(metadata["reported_cells"])
        count_rows.append(
            {
                "sample_id": sample_id,
                "donor_id": metadata["donor_id"],
                "raw_filtered_barcodes": adata.n_obs,
                "pass_paper_reported_mito_only": int(pass_mito.sum()),
                "pass_reconstruction_min_genes_only": int(pass_genes.sum()),
                "pass_reconstruction_combined_qc": int(pass_reconstruction_qc.sum()),
                "reported_final_cells": reported,
                "remaining_gap_after_combined_qc": int(pass_reconstruction_qc.sum()) - reported,
            }
        )
        for metric in ("total_counts", "n_genes_by_counts", "pct_counts_mt"):
            quantile_rows.extend(quantiles(adata.obs[metric], metric, sample_id))
        print(
            f"{sample_id}: raw={adata.n_obs}, mito={pass_mito.sum()}, "
            f"combined={pass_reconstruction_qc.sum()}, reported={reported}"
        )

    counts = pd.DataFrame(count_rows)
    totals = {
        "sample_id": "TOTAL",
        "donor_id": "7 donors",
        **{column: int(counts[column].sum()) for column in counts.columns if column not in {"sample_id", "donor_id"}},
    }
    counts = pd.concat([counts, pd.DataFrame([totals])], ignore_index=True)
    quantile_table = pd.DataFrame(quantile_rows)

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    counts.to_csv(OUTPUT_ROOT / "pi_qc_counts.tsv", sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)
    quantile_table.to_csv(OUTPUT_ROOT / "pi_qc_quantiles.tsv", sep="\t", index=False)
    summary = {
        "classification": {
            "mitochondrial_threshold": "PAPER-REPORTED METHOD",
            "minimum_genes_threshold": "USER/CODEX ANALYTICAL CHOICE",
            "doublet_removal": "NOT YET APPLIED",
        },
        "thresholds": {"max_pct_mito": max_pct_mito, "min_genes": min_genes},
        "totals": totals,
    }
    (OUTPUT_ROOT / "pi_qc_audit.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
