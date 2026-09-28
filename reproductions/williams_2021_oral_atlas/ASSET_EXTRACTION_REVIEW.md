# Asset Extraction Review — Williams 2021 Oral Atlas

## Current evidence boundary

The environment preflight was executed, but paper data and figures were not reproduced. No asset is ready for promotion.

## Project-specific assets

| Asset | Reason | Decision |
|---|---|---|
| Upstream cluster renaming and marker choices | Depends on this atlas, paper figures and manual decisions | KEEP PROJECT-SPECIFIC |
| Oral sample/group object construction | Uses GSE164241 identifiers and study design | KEEP PROJECT-SPECIFIC |

## Potential reusable workflows

| Candidate | General use | Validation still needed | Decision |
|---|---|---|---|
| Donor-aware pre/post-QC audit | Compare retained cells and thresholds by donor before integration | Run on GSE164241 and a second scRNA-seq project | PROMOTE AFTER SECOND USE |
| Hierarchical major-cell then subset annotation | Preserve major lineage decisions before subset analysis | Compare with current APAP annotation workflows | CANDIDATE — NOT YET READY |

## Potential visualization recipes

| Candidate | Required input | Example output | Decision |
|---|---|---|---|
| Pre/post-QC violin and retained-cell panel | Per-cell QC metadata plus donor ID | Figure S1A–C style panel | CANDIDATE — NOT YET READY |

## Potential reusable functions

None. The upstream helpers have not been isolated or tested outside their original object model.

## Environment knowledge

- Package presence does not guarantee a loadable environment.
- R 4.3.1 with the current user library contains Seurat packages built under R 4.3.3.
- `SeuratObject` fails because installed `Matrix` 1.5-4.1 does not satisfy `>= 1.6.4`.
- Environment validation must attempt namespace loading rather than checking `installed.packages()` alone.

## Debugging knowledge

- Run environment preflight before downloading a 759.5 MB dataset.
- Preserve the upstream source revision and checksum before adapting interactive analysis code.
- Treat placeholder paths and implicit in-memory objects as explicit reproducibility blockers.

## Methodological knowledge for Research OS

- Donor is the biological unit for group comparisons; cell-level tests alone create pseudoreplication risk.
- Low-RNA neutrophils require QC review that distinguishes biological low complexity from damaged cells.
- Single-cell states and ligand–receptor scores do not establish migration history.

## Ideas generated

- Compare the Williams oral neutrophil QC behavior with the existing APAP scRNA-seq QC pipeline after both workflows are executable.
- Test whether a donor-aware QC report can become a shared workflow only after the second use.

## Promotion decision

No asset is promoted in Phase 2. The QC audit and plot remain candidates pending real-data reproduction and second validation.

