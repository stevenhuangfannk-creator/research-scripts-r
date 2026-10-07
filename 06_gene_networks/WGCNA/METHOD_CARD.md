# Method Card

**Method:** wgcna

**Category:** 06_gene_networks

**Status:** CANDIDATE

**Language:** R

**Package:** WGCNA

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://horvath.genetics.ucla.edu/html/CoexpressionNetwork/Rpackages/WGCNA/

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Find coexpression modules across independent biological samples.

**Biological question:** Find coexpression modules across independent biological samples.

**When to use:** Normalized sample × gene matrix, QC and sample traits.

**When NOT to use:** Too few samples or pooled cells produce unstable/confounded modules.

**Required input:** Normalized sample × gene matrix, QC and sample traits.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Soft threshold; signedness; minimum module size; covariates.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Too few samples or pooled cells produce unstable/confounded modules.

**Outputs:** Modules; eigengenes; module-trait associations; hub candidates.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Too few samples or pooled cells produce unstable/confounded modules.

**Assumptions:** Too few samples or pooled cells produce unstable/confounded modules.

**Common pitfalls:** Too few samples or pooled cells produce unstable/confounded modules.

**Alternatives:** hdWGCNA for validated metacell designs

**When to prefer alternatives:** hdWGCNA for validated metacell designs

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://horvath.genetics.ucla.edu/html/CoexpressionNetwork/Rpackages/WGCNA/
