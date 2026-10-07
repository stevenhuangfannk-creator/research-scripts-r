# Method Card

**Method:** differential_abundance

**Category:** 02_differential_analysis

**Status:** CANDIDATE

**Language:** R

**Package:** Milo / scCODA

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://bioconductor.org/packages/miloR

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Test replicated abundance shifts while considering composition.

**Biological question:** Test replicated abundance shifts while considering composition.

**When to use:** Counts/neighbor graph and biological-sample design.

**When NOT to use:** Sample size, capture bias and composition affect inference; barplots alone are descriptive.

**Required input:** Counts/neighbor graph and biological-sample design.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Neighborhood coverage; contrasts; sample structure.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Sample size, capture bias and composition affect inference; barplots alone are descriptive.

**Outputs:** Neighborhood effect/FDR; abundance graph.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Sample size, capture bias and composition affect inference; barplots alone are descriptive.

**Assumptions:** Sample size, capture bias and composition affect inference; barplots alone are descriptive.

**Common pitfalls:** Sample size, capture bias and composition affect inference; barplots alone are descriptive.

**Alternatives:** Sample-level compositional models

**When to prefer alternatives:** Sample-level compositional models

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://bioconductor.org/packages/miloR
