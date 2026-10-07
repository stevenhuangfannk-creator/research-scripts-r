# Method Card

**Method:** seurat_clustering

**Category:** 01_scrna_core

**Status:** VALIDATED

**Language:** R

**Package:** Seurat

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** 2026-10-07

**Official documentation:** https://satijalab.org/seurat/articles/pbmc3k_tutorial

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Find variable features, PCA, neighbors, clusters and reproducible UMAP.

**Biological question:** Find variable features, PCA, neighbors, clusters and reproducible UMAP.

**When to use:** Normalized Seurat object.

**When NOT to use:** Resolution is a biological decision, not a cell-type count estimator. UMAP distances are not quantitative lineage distances. Recompute after meaningful subsetting.

**Required input:** Normalized Seurat object.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** nfeatures = 2000; npcs = 30; resolution = 0.5; n_neighbors = 30; seed = 42

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Resolution is a biological decision, not a cell-type count estimator. UMAP distances are not quantitative lineage distances. Recompute after meaningful subsetting.

**Outputs:** PCA and UMAP embeddings; cluster labels; neighbor graph

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Resolution is a biological decision, not a cell-type count estimator. UMAP distances are not quantitative lineage distances. Recompute after meaningful subsetting.

**Assumptions:** Resolution is a biological decision, not a cell-type count estimator. UMAP distances are not quantitative lineage distances. Recompute after meaningful subsetting.

**Common pitfalls:** Resolution is a biological decision, not a cell-type count estimator. UMAP distances are not quantitative lineage distances. Recompute after meaningful subsetting.

**Alternatives:** Leiden or other Seurat algorithms after validation; Harmony embedding for batch-corrected geometry.

**When to prefer alternatives:** Leiden or other Seurat algorithms after validation; Harmony embedding for batch-corrected geometry.

**Validated datasets:** Seurat::pbmc_small

**Validation status:** PASS — PCA/neighbors/clustering/UMAP on all 80 cells; not full-atlas robustness

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 01_scrna_core/clustering/scripts/workflow.R

**References:** https://satijalab.org/seurat/articles/pbmc3k_tutorial
