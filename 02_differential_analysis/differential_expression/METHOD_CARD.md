# Method Card

**Method:** cell_markers

**Category:** 02_differential_analysis

**Status:** VALIDATED

**Language:** R

**Package:** Seurat

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** 2026-10-07

**Official documentation:** https://satijalab.org/seurat/articles/pbmc3k_tutorial

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Find exploratory cell/cluster markers without claiming donor-level treatment inference.

**Biological question:** Find exploratory cell/cluster markers without claiming donor-level treatment inference.

**When to use:** Normalized RNA Seurat with grouping labels.

**When NOT to use:** Cell-level P values can reflect pseudoreplication. Marker evidence does not by itself identify a cell type or treatment effect.

**Required input:** Normalized RNA Seurat with grouping labels.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** group_column = seurat_clusters; only_positive = True; min_pct = 0.1; logfc_threshold = 0.25

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Cell-level P values can reflect pseudoreplication. Marker evidence does not by itself identify a cell type or treatment effect.

**Outputs:** marker effect/test table

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Cell-level P values can reflect pseudoreplication. Marker evidence does not by itself identify a cell type or treatment effect.

**Assumptions:** Cell-level P values can reflect pseudoreplication. Marker evidence does not by itself identify a cell type or treatment effect.

**Common pitfalls:** Cell-level P values can reflect pseudoreplication. Marker evidence does not by itself identify a cell type or treatment effect.

**Alternatives:** Sample × cell-type pseudobulk with DESeq2/edgeR/limma for condition effects.

**When to prefer alternatives:** Sample × cell-type pseudobulk with DESeq2/edgeR/limma for condition effects.

**Validated datasets:** Seurat::pbmc_small

**Validation status:** PASS — Exploratory cluster-marker table; no sample-level treatment inference

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 02_differential_analysis/differential_expression/scripts/workflow.R

**References:** https://satijalab.org/seurat/articles/pbmc3k_tutorial
