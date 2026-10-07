# Method Card

**Method:** seurat_ingestion

**Category:** 01_scrna_core

**Status:** VALIDATED

**Language:** R

**Package:** Seurat

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** 2026-10-07

**Official documentation:** https://satijalab.org/seurat/articles/pbmc3k_tutorial

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Build an auditable Seurat object from aligned counts and sample metadata.

**Biological question:** Build an auditable Seurat object from aligned counts and sample metadata.

**When to use:** RDS list(counts: nonnegative gene × barcode matrix, metadata: barcode-indexed data.frame).

**When NOT to use:** Barcode calling on raw droplets is a separate upstream decision. Do not invent symbols or collapse duplicated IDs silently.

**Required input:** RDS list(counts: nonnegative gene × barcode matrix, metadata: barcode-indexed data.frame).

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** project = user label; min.cells = 0; min.features = 0

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Barcode calling on raw droplets is a separate upstream decision. Do not invent symbols or collapse duplicated IDs silently.

**Outputs:** feature inventory; cell/sample inventory; Seurat counts object

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Barcode calling on raw droplets is a separate upstream decision. Do not invent symbols or collapse duplicated IDs silently.

**Assumptions:** Barcode calling on raw droplets is a separate upstream decision. Do not invent symbols or collapse duplicated IDs silently.

**Common pitfalls:** Barcode calling on raw droplets is a separate upstream decision. Do not invent symbols or collapse duplicated IDs silently.

**Alternatives:** Read10X/Read10X_h5 for supported 10x files; SingleCellExperiment for Bioconductor workflows.

**When to prefer alternatives:** Read10X/Read10X_h5 for supported 10x files; SingleCellExperiment for Bioconductor workflows.

**Validated datasets:** Seurat::pbmc_small (230 genes, 80 cells)

**Validation status:** PASS — Counts/metadata alignment and counts preservation only

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 01_scrna_core/data_ingestion/scripts/workflow.R

**References:** https://satijalab.org/seurat/articles/pbmc3k_tutorial
