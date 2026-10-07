"""Evaluate plausible gene-count thresholds without treating fit as provenance."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import scanpy as sc


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_ROOT = PROJECT_ROOT / "data" / "raw" / "pi_scrna"
OUTPUT_ROOT = PROJECT_ROOT / "results" / "phase4a"
MAX_PCT_MITO = 25.0  # PAPER-REPORTED METHOD
MIN_GENES = (200, 500, 750, 1000, 1250, 1500, 2000)
MAX_GENES = (4000, 6000, 8000, None)


def main() -> int:
    metadata = pd.read_csv(PROJECT_ROOT / "config" / "pi_samples.tsv", sep="\t")
    rows: list[dict[str, object]] = []
    for sample in metadata.itertuples(index=False):
        matches = [
            path
            for path in INPUT_ROOT.rglob(f"{sample.sample_id}_filtered_feature_bc_matrix.h5")
            if "__MACOSX" not in path.parts
        ]
        if len(matches) != 1:
            raise ValueError(f"expected one H5 for {sample.sample_id}, found {len(matches)}")
        adata = sc.read_10x_h5(matches[0], gex_only=True)
        adata.var_names_make_unique()
        adata.var["mt"] = adata.var_names.str.upper().str.startswith("MT-")
        sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], percent_top=None, log1p=False, inplace=True)
        for min_genes in MIN_GENES:
            for max_genes in MAX_GENES:
                keep = (adata.obs["pct_counts_mt"] <= MAX_PCT_MITO) & (
                    adata.obs["n_genes_by_counts"] >= min_genes
                )
                if max_genes is not None:
                    keep &= adata.obs["n_genes_by_counts"] <= max_genes
                retained = int(keep.sum())
                rows.append(
                    {
                        "sample_id": sample.sample_id,
                        "min_genes": min_genes,
                        "max_genes": "none" if max_genes is None else max_genes,
                        "retained_before_doublet_removal": retained,
                        "reported_final_cells": int(sample.reported_cells),
                        "gap": retained - int(sample.reported_cells),
                    }
                )

    sensitivity = pd.DataFrame(rows)
    ranking = (
        sensitivity.groupby(["min_genes", "max_genes"], as_index=False)
        .agg(
            retained_before_doublet_removal=("retained_before_doublet_removal", "sum"),
            reported_final_cells=("reported_final_cells", "sum"),
            sample_absolute_error=("gap", lambda values: int(values.abs().sum())),
            maximum_sample_absolute_error=("gap", lambda values: int(values.abs().max())),
        )
        .assign(total_gap=lambda table: table.retained_before_doublet_removal - table.reported_final_cells)
        .sort_values(["sample_absolute_error", "maximum_sample_absolute_error"])
    )
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    sensitivity.to_csv(OUTPUT_ROOT / "pi_qc_sensitivity.tsv", sep="\t", index=False)
    ranking.to_csv(OUTPUT_ROOT / "pi_qc_sensitivity_ranking.tsv", sep="\t", index=False)
    print(ranking.head(12).to_string(index=False))
    print(
        "\nInterpretation: these are reconstruction sensitivity results, not evidence "
        "of the authors' unreported thresholds. Doublet removal has not been applied."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
