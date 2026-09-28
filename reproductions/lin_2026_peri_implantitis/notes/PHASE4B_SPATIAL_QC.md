# Phase 4B-1 Spatial QC and Mapping

Date: 2026-09-28

## Scope and classification

This stage validates the released expression matrices, barcodes, tissue positions,
scale factors and tissue images. No spot filtering was applied.

- Released-file integrity and coordinate correspondence: **EXACTLY REPRODUCED STEP**.
- Cross-sample QC summary and anomaly assessment: **USER/CODEX ANALYTICAL CHOICE**.
- Paper-specific filtering thresholds: **UNRESOLVED / UNAVAILABLE INFORMATION**.

## Results

| Sample | Condition | Matrix spots | Tissue spots | Median UMI in tissue | Median genes in tissue | Coordinate/image match |
|---|---|---:|---:|---:|---:|---|
| PI_spatial | PI | 4,992 | 640 | 34,769 | 5,682 | pass |
| GSM6258251_A1 | HG | 4,992 | 231 | 236 | 175 | pass |
| GSM6258252_B1 | HG | 4,992 | 284 | 286 | 212 | pass |
| GSM6258253_C1 | HG | 4,992 | 295 | 636 | 402 | pass |
| GSM6258254_D1 | HG | 4,992 | 319 | 300 | 220 | pass |
| GSM6258255_A2 | HG | 4,992 | 1,088 | 4,539 | 2,309.5 | pass |
| GSM6258256_B2 | HG | 4,992 | 415 | 23,197 | 4,968 | pass |
| GSM6258257_C2 | HG | 4,992 | 160 | 35,348 | 5,774 | pass |
| GSM6258258_D2 | HG | 4,992 | 501 | 5,038 | 2,154 | pass |

All nine datasets have complete matrix-to-position barcode correspondence and all
scaled full-resolution coordinates lie within the corresponding high-resolution
image. PI filtered barcodes overlap the tissue-position table 640/640.

## Anomaly assessment

The healthy A1-D1 group has substantially lower median UMI and detected genes than
PI and most A2-D2 samples. This is a real input-depth/batch difference and must be
preserved in downstream metadata. A1 also contains 220 zero-count non-tissue matrix
barcodes; B1-D1 contain 26-72. No zero-count tissue spot was used to define a filter.

No sample is removed. Suggested future filtering thresholds should be chosen only
after inspecting per-sample tissue-spot distributions and the source-study method;
a single global threshold would disproportionately remove A1-D1.

## Outputs

- `results/phase4b/qc/spatial_qc_summary.tsv`
- `results/phase4b/qc/spatial_spot_qc.tsv.gz`
- `results/phase4b/qc/spatial_qc_audit.json`
- `figures/phase4b/qc/spatial_qc_distributions.{png,pdf}`
- `figures/phase4b/qc/*_tissue_coverage.{png,pdf}`

## Gate decision

**PASS with batch-depth warning.** Input geometry is valid and no file is incomplete.
Phase 4B-2 may proceed, but cell2location inputs must retain sample identity and must
not pool the eight healthy samples into one pseudo-sample.
