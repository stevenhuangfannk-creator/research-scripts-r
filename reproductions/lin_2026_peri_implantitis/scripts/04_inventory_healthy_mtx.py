"""Inventory the 13 GSE164241 healthy gingiva 10x matrices."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_ROOT = PROJECT_ROOT / "data" / "raw" / "gse164241_healthy_gingiva"
OUTPUT_ROOT = PROJECT_ROOT / "results" / "phase4a"


def count_lines(path: Path) -> int:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def matrix_shape(path: Path) -> tuple[int, int, int]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        header = next(handle).strip()
        if not header.startswith("%%MatrixMarket"):
            raise ValueError(f"invalid Matrix Market header in {path}")
        for line in handle:
            if not line.startswith("%"):
                rows, columns, nonzero = (int(value) for value in line.split())
                return rows, columns, nonzero
    raise ValueError(f"matrix dimensions not found in {path}")


def main() -> int:
    samples = pd.read_csv(PROJECT_ROOT / "config" / "healthy_samples.tsv", sep="\t")
    rows: list[dict[str, object]] = []
    for sample in samples.itertuples(index=False):
        directory = INPUT_ROOT / sample.sample_id
        barcodes = next(directory.glob("*_barcodes.tsv.gz"))
        features = list(directory.glob("*_features.tsv.gz")) + list(directory.glob("*_genes.tsv.gz"))
        matrices = list(directory.glob("*_matrix.mtx.gz"))
        if len(features) != 1 or len(matrices) != 1:
            raise ValueError(f"incomplete or ambiguous 10x files for {sample.sample_id}")
        n_barcodes = count_lines(barcodes)
        n_features = count_lines(features[0])
        matrix_rows, matrix_columns, nonzero = matrix_shape(matrices[0])
        rows.append(
            {
                "sample_id": sample.sample_id,
                "geo_accession": sample.geo_accession,
                "donor_id": sample.donor_id,
                "feature_schema": "features.tsv" if "features" in features[0].name else "genes.tsv",
                "features": n_features,
                "barcodes": n_barcodes,
                "matrix_rows": matrix_rows,
                "matrix_columns": matrix_columns,
                "nonzero_entries": nonzero,
                "dimensions_match": n_features == matrix_rows and n_barcodes == matrix_columns,
            }
        )
    inventory = pd.DataFrame(rows)
    summary = {
        "files_expected": 39,
        "samples": len(inventory),
        "donors": int(inventory["donor_id"].nunique()),
        "raw_filtered_barcodes": int(inventory["barcodes"].sum()),
        "all_dimensions_match": bool(inventory["dimensions_match"].all()),
        "legacy_gene_schema_samples": int((inventory["feature_schema"] == "genes.tsv").sum()),
    }
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    inventory.to_csv(OUTPUT_ROOT / "healthy_mtx_inventory.tsv", sep="\t", index=False)
    (OUTPUT_ROOT / "healthy_mtx_inventory.json").write_text(
        json.dumps({"summary": summary, "samples": rows}, indent=2), encoding="utf-8"
    )
    print(inventory.to_string(index=False))
    print(json.dumps(summary, indent=2))
    return 0 if summary["samples"] == 13 and summary["all_dimensions_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
