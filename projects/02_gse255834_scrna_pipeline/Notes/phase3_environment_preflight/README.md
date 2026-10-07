# Phase 3 Second-Use Validation

## Why this context was selected

GSE255834 is an existing, scientifically meaningful APAP liver-injury scRNA-seq workflow. It has explicit package requirements and known environment uncertainty, so it can test the shared namespace preflight without changing the analysis code or requiring unavailable input data.

## Preserved original state

- **Checkpoint:** commit `11c6fc9d6a858163dc1c647e9ca099c708057546`.
- **Original project tree:** `6790cca6b34e201162639cd337e755b883301c8c`.
- **Structure:** 10 R scripts in ingestion, QC, decontamination and annotation modules; existing README and pipeline audit.
- **Working state:** code is present; the eight GSE255834 H5 inputs, intermediate objects and results are unavailable.
- **Known constraints:** nine scripts contain the old `C:/Users/zhaozize/Desktop/APAP` path; object-chain gaps remain documented in `../pipeline-audit.md`.

No original R script was edited. The Phase 2 commit and tree hash preserve the exact starting implementation.

## Validation goal

Run the same Base R namespace checker used for the Williams reproduction against the packages referenced by the recommended GSE255834 main workflow.

Expected output is an honest environment readiness report, not a scientific result.

## Command and transfer result

```powershell
& 'C:\Program Files\R\R-4.3.1\bin\Rscript.exe' `
  library\workflows\r_namespace_preflight\preflight.R `
  --manifest projects\02_gse255834_scrna_pipeline\Notes\phase3_environment_preflight\packages.tsv `
  --output-dir projects\02_gse255834_scrna_pipeline\Notes\phase3_environment_preflight `
  --context gse255834_apap_scrna_pipeline
```

**Transfer classification:** worked with parameter changes. The shared script was unchanged; only the manifest, output directory and context label differed.

## Observed result

- R 4.3.1 started and the checker completed.
- 6 of 14 required namespaces loaded.
- Required blockers: Seurat, DropletUtils, future, SingleCellExperiment, scDblFinder, BiocParallel, future.apply and celda.
- Seurat is installed but fails because Matrix 1.5-4.1 does not satisfy the installed SeuratObject requirement of Matrix >= 1.6.4.
- Exit code `2` correctly prevented the environment from being described as ready.

Files in this directory provide the manifest, complete package status, concise summary and session information.

## Evidence boundary

The environment workflow transferred successfully. The GSE255834 analysis did not run because data are absent and the package environment is incomplete. No QC threshold, retained-cell count, UMAP, annotation or biological result was validated.
