# Method Card

**Method:** liana_plus

**Category:** 04_cell_communication

**Status:** CANDIDATE

**Language:** R

**Package:** liana

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://liana-py.readthedocs.io/en/latest/

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Compare/aggregate communication evidence with multiple methods.

**Biological question:** Compare/aggregate communication evidence with multiple methods.

**When to use:** AnnData or supported R interface, labels and compatible LR resource.

**When NOT to use:** Newness is not default eligibility; interface and resources need validation.

**Required input:** AnnData or supported R interface, labels and compatible LR resource.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Resource; methods; ranking aggregation.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Newness is not default eligibility; interface and resources need validation.

**Outputs:** Consensus LR ranks; multi-condition/context evidence.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Newness is not default eligibility; interface and resources need validation.

**Assumptions:** Newness is not default eligibility; interface and resources need validation.

**Common pitfalls:** Newness is not default eligibility; interface and resources need validation.

**Alternatives:** CellChat; NicheNet

**When to prefer alternatives:** CellChat; NicheNet

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://liana-py.readthedocs.io/en/latest/
