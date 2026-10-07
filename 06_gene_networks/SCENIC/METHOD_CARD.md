# Method Card

**Method:** scenic

**Category:** 06_gene_networks

**Status:** CANDIDATE

**Language:** R

**Package:** SCENIC / AUCell

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://github.com/aertslab/SCENIC

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Infer candidate transcription-factor regulons and activity.

**Biological question:** Infer candidate transcription-factor regulons and activity.

**When to use:** Expression, species-compatible motif databases and TF annotations.

**When NOT to use:** Motif support and coexpression are not perturbation-validated regulation.

**Required input:** Expression, species-compatible motif databases and TF annotations.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Network algorithm; motif resource; AUCell thresholds.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Motif support and coexpression are not perturbation-validated regulation.

**Outputs:** TF-target regulons; activity matrix; regulon specificity.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Motif support and coexpression are not perturbation-validated regulation.

**Assumptions:** Motif support and coexpression are not perturbation-validated regulation.

**Common pitfalls:** Motif support and coexpression are not perturbation-validated regulation.

**Alternatives:** pySCENIC in separate Python environment

**When to prefer alternatives:** pySCENIC in separate Python environment

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://github.com/aertslab/SCENIC
