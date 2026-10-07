# Method Card

**Method:** limma

**Category:** 07_bulk_clinical_ml

**Status:** CANDIDATE

**Language:** R

**Package:** limma

**Package version:** See [build package evidence](../../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://bioconductor.org/packages/limma

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Fit sample-level linear models with empirical-Bayes variance moderation.

**Biological question:** Fit sample-level linear models with empirical-Bayes variance moderation.

**When to use:** Count matrix for voom or appropriate log expression, design and contrasts.

**When NOT to use:** Input scale determines workflow; technical batches cannot resolve complete design confounding.

**Required input:** Count matrix for voom or appropriate log expression, design and contrasts.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Design; voom weights; contrasts; trend.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Input scale determines workflow; technical batches cannot resolve complete design confounding.

**Outputs:** Moderated effects/FDR; fit diagnostics.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Input scale determines workflow; technical batches cannot resolve complete design confounding.

**Assumptions:** Input scale determines workflow; technical batches cannot resolve complete design confounding.

**Common pitfalls:** Input scale determines workflow; technical batches cannot resolve complete design confounding.

**Alternatives:** DESeq2; edgeR

**When to prefer alternatives:** DESeq2; edgeR

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://bioconductor.org/packages/limma
