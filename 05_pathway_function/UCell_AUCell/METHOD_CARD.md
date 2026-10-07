# Method Card

**Method:** ucell_aucell

**Category:** 05_pathway_function

**Status:** CANDIDATE

**Language:** R

**Package:** UCell / AUCell

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://bioconductor.org/packages/UCell

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Score signatures per cell using rank-based enrichment.

**Biological question:** Score signatures per cell using rank-based enrichment.

**When to use:** Cell expression ranks/counts and specified signature gene sets.

**When NOT to use:** Cell scores describe state; group significance requires donor-aware aggregation/modeling.

**Required input:** Cell expression ranks/counts and specified signature gene sets.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Rank cutoff; gene coverage; signature direction.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Cell scores describe state; group significance requires donor-aware aggregation/modeling.

**Outputs:** Cell × signature score; UMAP/violin/heatmap.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Cell scores describe state; group significance requires donor-aware aggregation/modeling.

**Assumptions:** Cell scores describe state; group significance requires donor-aware aggregation/modeling.

**Common pitfalls:** Cell scores describe state; group significance requires donor-aware aggregation/modeling.

**Alternatives:** GSVA for sample-level activity

**When to prefer alternatives:** GSVA for sample-level activity

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://bioconductor.org/packages/UCell
