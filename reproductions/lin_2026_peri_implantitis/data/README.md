# Data Acquisition

Downloaded datasets are intentionally ignored by Git. Run commands from the project root.

## Phase 4A PI scRNA-seq

```powershell
.\.venv\Scripts\python.exe scripts\00_download_public_data.py --dataset pi-scrna
.\.venv\Scripts\python.exe scripts\01_inventory_pi_h5.py
```

The downloader resolves the fixed Zenodo record, streams the archive, verifies the published MD5 and extracts into `data/raw/pi_scrna/`. It never overwrites a verified archive unless `--force` is explicitly supplied.

## Deferred inputs

- `GSE164241` healthy gingiva scRNA-seq is acquired after the PI archive inventory passes.
- The Zenodo spatial archive and `GSE206621` are deferred until the Phase 4A reference and labels are validated.

Do not commit `.zip`, `.h5`, matrices, spatial images or derived `.h5ad` objects.

