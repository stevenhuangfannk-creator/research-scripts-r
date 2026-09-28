# Environment

Run from the reproduction root:

```powershell
& "C:\Program Files\R\R-4.3.1\bin\Rscript.exe" scripts/00_environment_check.R
```

The script writes `package_status.tsv` and `sessionInfo.txt` here.

## Phase 2 finding

R 4.3.1 is present. The installed Seurat stack is internally incompatible: `SeuratObject` requires `Matrix >= 1.6.4`, while the installed Matrix version is 1.5-4.1. The upstream project also uses several packages that are absent locally.

No package was installed during Phase 2. A later phase should create an isolated, project-specific environment and record the resolved versions before any data download.

## Phase 3 shared workflow

The project-specific script remains as the recoverable first-use implementation. Phase 3 generalized only its namespace-checking core into [`library/workflows/r_namespace_preflight/preflight.R`](../../../library/workflows/r_namespace_preflight/preflight.R).

`packages.tsv` now separates this reproduction's package requirements from the shared checker. The shared script was run here without code changes and reproduced the Phase 2 result: 5 of 7 required packages load; Seurat and reshape2 remain blocked. `preflight_summary.txt`, `package_status.tsv` and `sessionInfo.txt` contain the current evidence.

