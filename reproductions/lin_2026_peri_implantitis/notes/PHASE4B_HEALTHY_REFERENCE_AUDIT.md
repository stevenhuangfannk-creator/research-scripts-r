# Phase 4B Healthy Spatial Reference Audit

Date: 2026-09-28

## Public input

GEO `GSE206621` exposes a `GSE206621_RAW.tar` archive of 133,652,480 bytes. The official file list contains eight spatial samples (`A1`, `B1`, `C1`, `D1`, `A2`, `B2`, `C2`, `D2`) and, for each sample, the expected 10x matrix components, tissue-position CSV, scale-factor JSON, high/low-resolution tissue images and fiducial/detected-tissue images.

## Access state

The official NCBI file list was readable. The binary archive download was attempted but the current connection was too slow and did not complete; partial files remain ignored and were not used. Therefore the archive contents are **NOT INSPECTED / ACCESS NOT AVAILABLE** in this run.

No spatial matrix, image or coordinate file has been treated as available. The file list is sufficient to define the expected input contract, but not to run spatial analysis.

## Input contract for Phase 4B

For each sample, verify these assets before analysis:

1. `barcodes.tsv.gz`
2. `features.tsv.gz`
3. `matrix.mtx.gz`
4. `tissue_positions_list.csv.gz`
5. `scalefactors_json.json.gz`
6. tissue high/low-resolution images
7. aligned fiducial and detected-tissue images

The PI spatial archive remains separately blocked by the Zenodo HTTP 403 recorded in `PHASE4B_INPUT_AUDIT.md`.

## Download endpoint check

The `filelist.txt` entries describe members of `GSE206621_RAW.tar`; direct URLs formed from those member names returned HTTP 404. The supported acquisition path is therefore the official TAR archive, followed by local extraction and per-file size checks.
