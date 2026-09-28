# Phase 4B Healthy Spatial Validation

Date: 2026-09-28

## Acquisition

The official GEO `GSE206621_RAW.tar` archive was downloaded with resumable HTTP Range requests from the NCBI FTP supplement and passed the published archive-size check.

- expected and observed bytes: `133,652,480`
- observed MD5: `7286ddc0f66589f6eb5879a531fa0a12`
- extraction root: `data/raw/gse206621_healthy_spatial/`
- source file list: official GEO `filelist.txt`

GEO did not provide an MD5 in the file list used here, so the observed MD5 is provenance metadata rather than an independent published checksum.

## Sample-level validation

All 8 samples have 9/9 expected assets and no missing local files. Matrix/coordinate validation passed for every sample:

| Samples | Barcodes | Features | Matrix dimensions | Position rows | Checks |
|---|---:|---:|---|---:|---|
| A1, B1, C1, D1 | 4,992 each | 36,601 each | 36,601 × 4,992 | 4,992 each | dimensions and barcode/position correspondence pass |
| A2, B2, C2, D2 | 4,992 each | 36,945 each | 36,945 × 4,992 | 4,992 each | dimensions and barcode/position correspondence pass |

Machine-readable outputs:

- `results/phase4b/spatial_asset_manifest.json`
- `results/phase4b/spatial_validation.json`

## Classification and next gate

Archive retrieval and file-structure validation are **EXACTLY REPRODUCED STEPS** for the public files. No biological labels or spatial mapping conclusions have been inferred. Both PI and healthy spatial inputs are now available for spatial QC, coordinate/image checks and later cell2location/NMF reconstruction.
