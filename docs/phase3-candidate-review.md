# Phase 3 Candidate Review

## Final classification

| Asset | Origin | Purpose | Expected input → output | Dependencies | Project assumptions and limits | Phase 3 status |
|---|---|---|---|---|---|---|
| R namespace preflight | Williams reproduction `scripts/00_environment_check.R` and environment lesson | Stop analysis when declared R namespaces cannot load | Package manifest → status TSV, summary, session info and exit code | Base R | Checks only the current library; does not resolve versions or test analysis logic | ALREADY PROMOTED — WITH LIMITATIONS |
| Donor-aware pre/post-QC audit | Williams Figure S1A-C workflow | Compare retained cells and thresholds by biological unit | Per-cell QC metadata plus donor/sample identity → count/threshold audit | R data handling; Seurat only if reading a Seurat object | A `sample` column is not automatically a donor; both datasets and outputs are absent | CANDIDATE — NOT YET READY |
| Hierarchical major-cell then subset annotation | Williams atlas; conceptually similar to APAP annotation | Preserve lineage decisions before subset reanalysis | Expression object, markers and lineage rules → labels and audit trail | Seurat and project marker definitions | Marker biology and cluster decisions are tissue-specific; neither workflow is executable here | CANDIDATE — NOT YET READY |
| Pre/post-QC violin and retained-cell panel | Williams Figure S1A-C | Make QC loss visible by biological unit | QC metadata and before/after flags → plot and count panel | ggplot2/patchwork or equivalent | No real Williams or GSE255834 QC output is available; visual transfer is untested | CANDIDATE — NOT YET READY |
| Oral sample construction | Williams reproduction | Build study-specific objects and groups | GSE164241 files → oral Seurat objects | Upstream package stack | Accession, sample identifiers and tissue groups are study-specific | PROJECT-SPECIFIC |
| Oral cluster renaming and markers | Williams reproduction | Reproduce paper annotations | Oral clusters and marker evidence → labels | Seurat plus manual biological decisions | Bound to the paper's atlas and manual decisions | PROJECT-SPECIFIC |

No Phase 2 candidate was classified as invalid. The environment workflow was the only candidate with enough real execution evidence for promotion.

## Duplication classification

| Material | Relationship | Decision |
|---|---|---|
| Williams `scripts/00_environment_check.R` and shared `preflight.R` | SHOULD SHARE CORE | Preserve the Phase 2 script as first-use history; use the shared workflow for future checks |
| Williams and GSE255834 package lists | SIMILAR BUT CONTEXT-SPECIFIC | Keep separate manifests; package requirements describe different analyses |
| Williams and GSE255834 QC summaries | SIMILAR BUT CONTEXT-SPECIFIC | Do not consolidate until both run on real data and the biological-unit semantics are verified |
| Existing GSE255834 diagnostic scripts | UNKNOWN for general reuse | Leave unchanged and recoverable |

## Reproduction structure finding

The Phase 2 reproduction layout was sufficient for provenance, environment results and an extraction review. The second context was an existing formal project, so imposing the reproduction template would have added overhead. No template change is justified by this test.
