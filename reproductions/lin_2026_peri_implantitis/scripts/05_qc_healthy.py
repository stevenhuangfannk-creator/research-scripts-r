"""Apply the source-paper QC rules to the 13 healthy gingiva matrices."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import mmread


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_ROOT = PROJECT_ROOT / "data" / "raw" / "gse164241_healthy_gingiva"
OUTPUT_ROOT = PROJECT_ROOT / "results" / "phase4a"
MIN_GENES_EXCLUSIVE = 200
MAX_GENES_EXCLUSIVE = 5000
MAX_PCT_MITO_EXCLUSIVE = 15.0
PAPER_TOTAL_CELLS = 90551
PI_REPORTED_CELLS = 39393
DERIVED_HEALTHY_FINAL_CELLS = PAPER_TOTAL_CELLS - PI_REPORTED_CELLS


def main() -> int:
    samples = pd.read_csv(PROJECT_ROOT / "config" / "healthy_samples.tsv", sep="\t")
    rows: list[dict[str, object]] = []
    for sample in samples.itertuples(index=False):
        directory = INPUT_ROOT / sample.sample_id
        matrix_path = next(directory.glob("*_matrix.mtx.gz"))
        feature_paths = list(directory.glob("*_features.tsv.gz")) + list(directory.glob("*_genes.tsv.gz"))
        if len(feature_paths) != 1:
            raise ValueError(f"expected one feature table for {sample.sample_id}")
        features = pd.read_csv(feature_paths[0], sep="\t", header=None, compression="gzip")
        matrix = mmread(matrix_path).tocsr()
        if matrix.shape[0] != len(features):
            raise ValueError(f"feature dimension mismatch for {sample.sample_id}")

        gene_symbols = features.iloc[:, 1].astype(str)
        mitochondrial = gene_symbols.str.upper().str.startswith("MT-").to_numpy()
        total_counts = np.asarray(matrix.sum(axis=0)).ravel()
        detected_genes = matrix.getnnz(axis=0)
        mito_counts = np.asarray(matrix[mitochondrial, :].sum(axis=0)).ravel()
        pct_mito = np.divide(
            mito_counts * 100.0,
            total_counts,
            out=np.zeros_like(mito_counts, dtype=float),
            where=total_counts > 0,
        )
        keep = (
            (detected_genes > MIN_GENES_EXCLUSIVE)
            & (detected_genes < MAX_GENES_EXCLUSIVE)
            & (pct_mito < MAX_PCT_MITO_EXCLUSIVE)
        )
        retained = int(keep.sum())
        rows.append(
            {
                "sample_id": sample.sample_id,
                "donor_id": sample.donor_id,
                "raw_filtered_barcodes": int(matrix.shape[1]),
                "retained_source_paper_qc": retained,
                "removed_source_paper_qc": int(matrix.shape[1]) - retained,
                "retained_fraction": retained / int(matrix.shape[1]),
            }
        )
        print(f"{sample.sample_id}: raw={matrix.shape[1]}, retained={retained}")

    table = pd.DataFrame(rows)
    retained_total = int(table["retained_source_paper_qc"].sum())
    summary = {
        "classification": "METHOD-BASED RECONSTRUCTION",
        "provenance": "Williams 2021 public workflow for GSE164241 healthy gingiva",
        "thresholds": {
            "min_genes_exclusive": MIN_GENES_EXCLUSIVE,
            "max_genes_exclusive": MAX_GENES_EXCLUSIVE,
            "max_pct_mito_exclusive": MAX_PCT_MITO_EXCLUSIVE,
        },
        "raw_filtered_barcodes": int(table["raw_filtered_barcodes"].sum()),
        "retained_source_paper_qc": retained_total,
        "healthy_cells_implied_by_current_paper": DERIVED_HEALTHY_FINAL_CELLS,
        "gap_before_later_cluster_exclusions": retained_total - DERIVED_HEALTHY_FINAL_CELLS,
    }
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUTPUT_ROOT / "healthy_qc_counts.tsv", sep="\t", index=False)
    (OUTPUT_ROOT / "healthy_qc_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
