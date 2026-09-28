"""Inventory released PI 10x HDF5 matrices and compare reported cell counts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import h5py


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_ROOT = PROJECT_ROOT / "data" / "raw" / "pi_scrna"
OUTPUT_ROOT = PROJECT_ROOT / "results" / "phase4a"
EXPECTED_CELLS = {
    "IGT1": 1050,
    "IGT2": 363,
    "IGT3": 9429,
    "IGT4": 7709,
    "IGT5": 8604,
    "IGT6": 2126,
    "IGT7": 3834,
    "IGT8": 6278,
}


def sample_from_name(path: Path) -> str:
    upper = path.name.upper()
    matches = [sample for sample in EXPECTED_CELLS if sample in upper]
    if len(matches) != 1:
        raise ValueError(f"cannot resolve one sample ID from {path.name!r}")
    return matches[0]


def inspect(path: Path) -> dict[str, object]:
    with h5py.File(path, "r") as handle:
        if "matrix" not in handle:
            raise ValueError(f"missing /matrix group in {path}")
        matrix = handle["matrix"]
        shape = tuple(int(value) for value in matrix["shape"][:])
        barcodes = int(matrix["barcodes"].shape[0])
        genes = int(matrix["features"]["name"].shape[0])
    sample = sample_from_name(path)
    expected = EXPECTED_CELLS[sample]
    return {
        "sample_id": sample,
        "file": str(path.relative_to(PROJECT_ROOT)),
        "genes": genes,
        "barcodes": barcodes,
        "matrix_rows": shape[0],
        "matrix_columns": shape[1],
        "expected_cells": expected,
        "cell_count_match": barcodes == expected,
    }


def main() -> int:
    files = sorted(INPUT_ROOT.rglob("*.h5"))
    if not files:
        raise FileNotFoundError(f"no .h5 files found under {INPUT_ROOT}")

    rows = sorted((inspect(path) for path in files), key=lambda row: row["sample_id"])
    duplicates = len({row["sample_id"] for row in rows}) != len(rows)
    total_observed = sum(int(row["barcodes"]) for row in rows)
    total_expected = sum(EXPECTED_CELLS.values())
    summary = {
        "files": len(rows),
        "samples": [row["sample_id"] for row in rows],
        "duplicate_sample_ids": duplicates,
        "total_observed_cells": total_observed,
        "total_expected_cells": total_expected,
        "total_match": total_observed == total_expected,
        "all_sample_counts_match": all(bool(row["cell_count_match"]) for row in rows),
    }

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    columns = list(rows[0])
    with (OUTPUT_ROOT / "pi_h5_inventory.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    (OUTPUT_ROOT / "pi_h5_inventory.json").write_text(
        json.dumps({"summary": summary, "samples": rows}, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_sample_counts_match"] and summary["total_match"] and not duplicates else 1


if __name__ == "__main__":
    raise SystemExit(main())
