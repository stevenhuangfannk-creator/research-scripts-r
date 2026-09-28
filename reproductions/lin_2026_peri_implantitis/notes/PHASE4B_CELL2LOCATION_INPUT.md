# Phase 4B-2 Cell2location Input Preparation

Date: 2026-09-28

## Input decision

The Phase 4A object contains 92,112 cells, 14 broad cell types and raw counts in
the `counts` layer. Labels are usable as a preliminary broad reference, but they
are not final author annotations: 90,032 cells are `provisional` and 2,080 cells
belong to low-confidence clusters. Low-confidence cells remain included and are
explicitly tracked; no silent cell exclusion was applied.

## Exact gene matching

| Input | Unique gene symbols |
|---|---:|
| scRNA reference | 21,934 |
| PI spatial | 17,939 |
| Healthy A1-D1 | 36,581 per sample |
| Healthy A2-D2 | 36,925 per sample |
| Exact intersection across every input | 17,211 |

Only exact, unique gene symbols were retained. No fuzzy matching, alias expansion
or case normalization was used. The PI spatial input has two duplicated symbols
(`TBCE`, `HSPA14`); each healthy input has ten duplicated symbols. Ambiguous symbols
were excluded from the shared intersection rather than aggregated or guessed.

Mitochondrial and ribosomal genes were not removed at this preparation stage.
Their treatment belongs to the reference-model specification and must be recorded
there rather than silently changing the shared gene universe.

## Reference composition

The 14 cell types range from 662 dendritic cells to 19,559 vascular endothelial
cells. Neutrophils have 972 cells and fibroblasts 15,939. This is an imbalanced but
usable broad-cell reference; rare and abundant types require signature diagnostics
after model fitting.

## Spatial input composition

PI contains 640 tissue spots. Healthy samples contain 160-1,088 tissue spots each.
Every sample is saved independently with `sample_id`, `condition`, spatial metadata
and a raw `counts` layer. Healthy samples were not merged into a pseudo-sample.

## Outputs

- `results/phase4b/cell2location_input/scrna_reference_counts.h5ad`
- `results/phase4b/cell2location_input/PI_spatial.h5ad`
- `results/phase4b/cell2location_input/GSM*.h5ad`
- `results/phase4b/cell2location_input/gene_intersection.tsv`
- `results/phase4b/cell2location_input/cells_per_cell_type.tsv`
- `results/phase4b/cell2location_input/spots_per_sample.tsv`
- `results/phase4b/cell2location_input/duplicate_gene_summary.json`

## Gate decision

**PASS with annotation and imbalance warnings.** The inputs are technically ready
for a reference signature model. Reference-model QC must explicitly check whether
rare types, low-confidence clusters and the strong endothelial/fibroblast abundance
produce implausible signatures.
