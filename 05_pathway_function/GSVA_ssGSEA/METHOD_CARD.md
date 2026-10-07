# Method Card

**Method:** gsva_ssgsea

**Category:** 05_pathway_function

**Status:** CANDIDATE

**Language:** R

**Package:** GSVA

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://bioconductor.org/packages/GSVA

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Estimate sample-level gene-set activity for replicated group comparisons.

**Biological question:** Estimate sample-level gene-set activity for replicated group comparisons.

**When to use:** Normalized gene × independent-sample matrix and gene sets.

**When NOT to use:** Recent GSVA uses parameter objects; never assume old gsva(expr, sets) API.

**Required input:** Normalized gene × independent-sample matrix and gene sets.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = GSVA vs ssGSEA; kernel; set sizes; installed API version.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Recent GSVA uses parameter objects; never assume old gsva(expr, sets) API.

**Outputs:** Pathway × sample matrix; group heatmap/violin.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Recent GSVA uses parameter objects; never assume old gsva(expr, sets) API.

**Assumptions:** Recent GSVA uses parameter objects; never assume old gsva(expr, sets) API.

**Common pitfalls:** Recent GSVA uses parameter objects; never assume old gsva(expr, sets) API.

**Alternatives:** GSEA for ranked group contrasts; UCell for cells

**When to prefer alternatives:** GSEA for ranked group contrasts; UCell for cells

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://bioconductor.org/packages/GSVA
