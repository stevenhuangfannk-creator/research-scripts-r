---
status: planned
pilot_status: environment_blocked
paper_doi: "10.1016/j.cell.2021.05.013"
paper_pmid: "34129837"
source_repository: "https://github.com/williamsdrake/oralAtlas"
source_revision: "f7e0c736022ba35b269351fe459e4ee6e251ac50"
source_dataset: "GSE164241"
research_os_note: "01_Literature/Neutrophil_Reverse_Migration_Review/reproduction_roadmap.md"
last_updated: "2026-09-28"
---

# Williams 2021 Oral Mucosa Atlas Reproduction

## Paper and provenance

- **Paper:** Williams DW et al. *Human oral mucosa cell atlas reveals a stromal-neutrophil axis regulating tissue immunity*. Cell, 2021.
- **DOI / PMID:** [10.1016/j.cell.2021.05.013](https://doi.org/10.1016/j.cell.2021.05.013) / 34129837.
- **Upstream code:** [williamsdrake/oralAtlas](https://github.com/williamsdrake/oralAtlas), MIT license.
- **Pinned upstream revision:** `f7e0c736022ba35b269351fe459e4ee6e251ac50`.
- **Dataset:** GEO [GSE164241](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE164241), SRA SRP300271.
- **Related Research OS:** `01_Literature/Neutrophil_Reverse_Migration_Review/reproduction_roadmap.md`.

The upstream `README.Rmd` and license are preserved in `source/`; provenance and checksums are in [`source/SOURCE.md`](source/SOURCE.md).

## Reproduction objective

Phase 2 tests one narrow path: prepare the environment and reproduce the oral-dataset QC family corresponding to Figure S1A–C before attempting integration, annotation or NicheNet.

Success requires actual GSE164241 counts, reproducible pre/post-QC cell counts, QC violin plots, and an explicit comparison with the upstream thresholds. A package smoke test or toy dataset does not count as paper reproduction.

## Current status

| Component | Status | Evidence |
|---|---|---|
| Upstream source snapshot | reproduced | Pinned `README.Rmd` and MIT license saved with SHA-256 |
| R executable | reproduced | R 4.3.1 found at `C:/Program Files/R/R-4.3.1/bin/Rscript.exe` |
| Package environment | not reproduced | Installed Seurat cannot load because `Matrix` is too old |
| GSE164241 data | not reproduced | No data downloaded during Phase 2 |
| Figure S1A–C QC | not tested | Blocked by environment and data |
| Downstream atlas/interaction analyses | not tested | Outside pilot scope |

The project therefore remains `planned` with `environment_blocked`; no scientific result is claimed.

## Upstream workflow

```text
GSE164241 10x matrices and sample metadata
→ build per-sample Seurat objects
→ merge BM / GM / PD groups
→ nFeature_RNA and percent.mt QC
→ integration and clustering
→ major-cell annotation
→ endothelial / fibroblast / epithelial / immune subset analysis
→ disease comparison and stromal–neutrophil interaction analysis
```

The upstream file contains 99 R chunks; 98 are marked `eval=FALSE`. It contains placeholder paths and assumes objects created earlier in the same interactive analysis.

## Local execution order

1. Run `Rscript scripts/00_environment_check.R`.
2. Resolve the recorded R/Matrix/Seurat compatibility problem in an isolated project environment.
3. Download and verify GSE164241 data according to [`data/README.md`](data/README.md).
4. Adapt only the upstream oral data import and Figure S1A–C QC blocks.
5. Compare cell counts, thresholds and plots with the paper/source material.
6. Update the validation table and complete the Asset Extraction Review.

## Expected outputs

- Per-sample pre/post-QC cell-count table.
- Pre/post-QC violin plots for healthy gingiva, buccal mucosa and periodontitis.
- QC cell-count comparison corresponding to Figure S1C.
- Session information and deviation log.

Generated results and figures stay outside Git by default. Their locations and regeneration commands are documented in `results/` and `figures/`.

## Environment

- Windows 11 environment observed during Phase 2.
- R 4.3.1 is installed but not on PATH.
- Installed Seurat was built under R 4.3.3.
- `SeuratObject` requires `Matrix >= 1.6.4`; installed `Matrix` is 1.5-4.1.
- Several upstream packages are absent; see `environment/package_status.tsv` after running the preflight.
- No packages were installed and no lockfile was fabricated.

## Deviations and known problems

- No human dataset was downloaded during this phase.
- Upstream code is a monolithic interactive R Markdown rather than a directly executable pipeline.
- Package versions are not locked upstream.
- Placeholder and object-state dependencies must be resolved incrementally.
- Donor-level statistical units must be preserved; cells cannot be treated as independent biological replicates.
- This atlas can identify cell states and stromal signals, but it cannot establish neutrophil migration history.

## Validation and asset review

- Detailed validation: [`notes/VALIDATION.md`](notes/VALIDATION.md)
- Asset review: [`ASSET_EXTRACTION_REVIEW.md`](ASSET_EXTRACTION_REVIEW.md)

