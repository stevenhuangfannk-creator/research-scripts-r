# Method Card

**Method:** sctransform

**Category:** 01_scrna_core

**Status:** CANDIDATE

**Language:** R

**Package:** Seurat

**Package version:** See [build package evidence](../../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://satijalab.org/seurat/articles/sctransform_vignette

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Model count-depth effects and stabilize variance.

**Biological question:** Model count-depth effects and stabilize variance.

**When to use:** Seurat RNA counts.

**When NOT to use:** Regression covariates need biological justification. Preserve RNA for communication; sparse tiny demos may not exercise model fitting reliably.

**Required input:** Seurat RNA counts.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** vst_flavor = v2; vars_to_regress = None; seed = 42

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Regression covariates need biological justification. Preserve RNA for communication; sparse tiny demos may not exercise model fitting reliably.

**Outputs:** SCT assay; residuals and variable features

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Regression covariates need biological justification. Preserve RNA for communication; sparse tiny demos may not exercise model fitting reliably.

**Assumptions:** Regression covariates need biological justification. Preserve RNA for communication; sparse tiny demos may not exercise model fitting reliably.

**Common pitfalls:** Regression covariates need biological justification. Preserve RNA for communication; sparse tiny demos may not exercise model fitting reliably.

**Alternatives:** LogNormalize; appropriate count-based models for inference.

**When to prefer alternatives:** LogNormalize; appropriate count-based models for inference.

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 01_scrna_core/normalization/SCTransform/scripts/workflow.R

**References:** https://satijalab.org/seurat/articles/sctransform_vignette
