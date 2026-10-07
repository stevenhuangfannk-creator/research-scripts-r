# Method Card

**Method:** lognormalize

**Category:** 01_scrna_core

**Status:** VALIDATED

**Language:** R

**Package:** Seurat

**Package version:** See [build package evidence](../../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** 2026-10-07

**Official documentation:** https://satijalab.org/seurat/articles/pbmc3k_tutorial

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Library-size normalize RNA counts for exploratory expression and downstream geometry.

**Biological question:** Library-size normalize RNA counts for exploratory expression and downstream geometry.

**When to use:** Seurat RNA counts.

**When NOT to use:** Normalization does not remove batch effects. Keep raw counts for count models; do not treat data-layer values as integer pseudobulk.

**Required input:** Seurat RNA counts.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** scale_factor = 10000

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Normalization does not remove batch effects. Keep raw counts for count models; do not treat data-layer values as integer pseudobulk.

**Outputs:** RNA data layer with log-normalized expression

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Normalization does not remove batch effects. Keep raw counts for count models; do not treat data-layer values as integer pseudobulk.

**Assumptions:** Normalization does not remove batch effects. Keep raw counts for count models; do not treat data-layer values as integer pseudobulk.

**Common pitfalls:** Normalization does not remove batch effects. Keep raw counts for count models; do not treat data-layer values as integer pseudobulk.

**Alternatives:** SCTransform for model-based variance stabilization.

**When to prefer alternatives:** SCTransform for model-based variance stabilization.

**Validated datasets:** Seurat::pbmc_small

**Validation status:** PASS — LogNormalize branch; preserves counts and creates finite RNA data layer

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 01_scrna_core/normalization/lognormalize/scripts/workflow.R

**References:** https://satijalab.org/seurat/articles/pbmc3k_tutorial
