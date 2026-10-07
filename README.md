# Research Scripts R

**Personal Bioinformatics Methods & Visualization Library**

R-first, reusable, validated and publication-oriented bioinformatics skill library.

Research question → method → reusable workflow → visualization → validated example.
Methods and figures are primary assets; projects preserve their origins and validation context.

- [Choose a method](METHOD_INDEX.md)
- [Look at the Gallery](GALLERY.md)
- [Choose a palette](PALETTE_INDEX.md)
- [Machine-readable registries](registry/README.md)
- [V1 build evidence and blockers](docs/V1_BUILD_REPORT.md)

## What this repository is

A personal library of documented bioinformatics decisions, portable R interfaces, versioned
figure styles and scoped execution evidence. A smoke-tested example is clearly separated
from a validated real-study analysis. Candidate code is never silently treated as a default.

## How to choose a method

Read METHOD_INDEX, then the registry, METHOD_CARD and OUTPUT_CATALOG. Check input scale,
species, sample design, package versions and validation scope. For a known Plot ID, resolve
its source and example from the plot registry before changing parameters.

```sh
Rscript scripts/resolve_asset.R method scrna_qc
Rscript scripts/resolve_asset.R plot umap_clean_v1
Rscript scripts/run_method.R METHOD_ID CONFIG.yml
Rscript scripts/validate_library.R
```

## Core capabilities

| Area | Entry |
|---|---|
| scRNA creation, QC, normalization, clustering, annotation | [01_scrna_core](01_scrna_core/README.md) |
| Exploratory markers and pseudobulk | [02_differential_analysis](02_differential_analysis/README.md) |
| Trajectory and gene dynamics | [Monocle3](03_cell_dynamics/monocle3/README.md) |
| Communication, roles, patterns and condition comparison | [CellChat](04_cell_communication/CellChat/README.md) |
| ORA, GSEA and activity decisions | [05_pathway_function](05_pathway_function/README.md) |
| PPI, coexpression and regulons | [06_gene_networks](06_gene_networks/README.md) |
| Bulk, correlation, survival and ML | [07_bulk_clinical_ml](07_bulk_clinical_ml/README.md) |
| Figures, palettes and themes | [08_visualization](08_visualization/README.md) |
| Original editable schematic components | [10_scientific_schematics](10_scientific_schematics/README.md) |

## Visualization Gallery

[GALLERY](GALLERY.md) shows actual PNG previews linked to code, parameters and vector files.
Synthetic style demonstrations are visibly labeled; missing CellChat/Monocle3 outputs are
documented with their blockers. No attractive preview substitutes for analytical validation.

## Method status

CANDIDATE → VALIDATED → RECOMMENDED → DEFAULT; EXPERIMENTAL and DEPRECATED are explicit.
UNVALIDATED/BLOCKED describe execution evidence separately. V1 does not promote a package
to DEFAULT on reputation. Read the actual per-method evidence in the registry.

## R-first / Python bridge

R is the primary workflow and figure backend. Python-only tools use independent environments
under [09_python_bridge](09_python_bridge/README.md). No complete spatial-only workflow is
introduced; existing reproduction history is preserved.

## How Codex should use this repository

Follow [CODEX_RULES](CODEX_RULES.md): retrieve existing methods and CURRENT_DEFAULT templates,
verify versions and scientific fit, then reuse. An unvalidated workflow requires explicit review.

## How to add a new method

Use [HOW_TO_ADD_METHOD](docs/HOW_TO_ADD_METHOD.md). Add the method, output catalog,
visualizations, actual gallery, comparison and registry evidence together.

## Legacy / validated projects

[99_legacy_projects](99_legacy_projects/README.md) maps the three original projects without
moving their executable paths. [90_examples](90_examples/README.md) links historical and
scoped smoke evidence. Original [projects](projects/) and [reproductions](reproductions/README.md)
remain intact. Their historical claims are not certified by this refactor.
