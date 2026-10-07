# Phase 4B PI Spatial Validation

Date: 2026-09-28

## Acquisition

The PI spatial archive was retrieved from the official Zenodo API file endpoint using resumable HTTP Range requests. The final archive is `data/downloads/space ranger output.zip`.

- record ID: `19697597`
- file: `space ranger output.zip`
- bytes: `169,698,220`
- MD5: `503e0e75aeff315b3f1a14f3cd8d3243`
- extraction root: `data/raw/pi_spatial/space ranger output/`

This is an **EXACTLY REPRODUCED STEP** for public archive acquisition and checksum validation. The HTTP 403 observed in earlier attempts was intermittent; the current record, API and file endpoints returned HTTP 200 before download.

## Space Ranger inventory

| Asset | Observed result | Classification |
|---|---:|---|
| Filtered HDF5 | 640 barcodes × 17,943 features | EXACTLY REPRODUCED STEP for released output |
| Raw HDF5 | 4,992 barcodes × 36,945 features | EXACTLY REPRODUCED STEP for released output |
| Tissue positions | 4,992 rows; 6-column headerless format | EXACTLY REPRODUCED STEP for released output |
| Barcode/position correspondence | 4,992 / 4,992 exact overlap | EXACTLY REPRODUCED STEP |
| Spatial images and metadata | all 7 required assets present | EXACTLY REPRODUCED STEP |

The detailed machine-readable inventory is `results/phase4b/pi_spatial_inventory.json`. The `__MACOSX` members are archive metadata sidecars and are excluded from analysis.

## Next gate

The PI spatial input is now ready for spatial QC and coordinate/image validation. Healthy spatial reference `GSE206621` remains a separate acquisition task; no cross-cohort spatial integration should begin until its TAR archive passes size and extraction checks.
