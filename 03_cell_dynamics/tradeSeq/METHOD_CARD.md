# Method Card

**Method:** tradeseq

**Category:** 03_cell_dynamics

**Status:** CANDIDATE

**Language:** R

**Package:** tradeSeq

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://bioconductor.org/packages/tradeSeq

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Test lineage-associated expression trends and differences.

**Biological question:** Test lineage-associated expression trends and differences.

**When to use:** Counts plus trajectory pseudotime and cell weights.

**When NOT to use:** Uses a supplied trajectory; it does not infer lineage by itself.

**Required input:** Counts plus trajectory pseudotime and cell weights.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Knots; lineage contrasts; covariates.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Uses a supplied trajectory; it does not infer lineage by itself.

**Outputs:** GAM fits; association/pattern/endpoint tests.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Uses a supplied trajectory; it does not infer lineage by itself.

**Assumptions:** Uses a supplied trajectory; it does not infer lineage by itself.

**Common pitfalls:** Uses a supplied trajectory; it does not infer lineage by itself.

**Alternatives:** Monocle3 graph association

**When to prefer alternatives:** Monocle3 graph association

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://bioconductor.org/packages/tradeSeq
