# Method Card

**Method:** hierarchical_annotation

**Category:** 01_scrna_core

**Status:** VALIDATED

**Language:** R

**Package:** Seurat

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** 2026-10-07

**Official documentation:** https://satijalab.org/seurat/articles/pbmc3k_tutorial

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Write reviewed level 1/2/3 annotations while preserving cluster IDs and evidence.

**Biological question:** Write reviewed level 1/2/3 annotations while preserving cluster IDs and evidence.

**When to use:** Seurat metadata with clusters; explicit cluster-to-label mappings by level plus evidence string.

**When NOT to use:** Demo labels validate writeback only. Tissue markers, negative markers and subset reclustering require biological review. Cycling is a state, not a lineage.

**Required input:** Seurat metadata with clusters; explicit cluster-to-label mappings by level plus evidence string.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** cluster_column = seurat_clusters; labels = mandatory named maps; evidence = mandatory biological evidence

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Demo labels validate writeback only. Tissue markers, negative markers and subset reclustering require biological review. Cycling is a state, not a lineage.

**Outputs:** annotation audit; labeled object; unmapped clusters remain Unknown

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Demo labels validate writeback only. Tissue markers, negative markers and subset reclustering require biological review. Cycling is a state, not a lineage.

**Assumptions:** Demo labels validate writeback only. Tissue markers, negative markers and subset reclustering require biological review. Cycling is a state, not a lineage.

**Common pitfalls:** Demo labels validate writeback only. Tissue markers, negative markers and subset reclustering require biological review. Cycling is a state, not a lineage.

**Alternatives:** SingleR, Azimuth/reference mapping with suitable validated references; retain manual evidence.

**When to prefer alternatives:** SingleR, Azimuth/reference mapping with suitable validated references; retain manual evidence.

**Validated datasets:** Seurat::pbmc_small

**Validation status:** PASS — Label writeback and Unknown fallback; biological annotations are not validated

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 01_scrna_core/annotation/scripts/workflow.R

**References:** https://satijalab.org/seurat/articles/pbmc3k_tutorial
