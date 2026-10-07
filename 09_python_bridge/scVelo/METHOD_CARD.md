# Method Card

**Method:** scvelo

**Category:** 09_python_bridge

**Status:** EXPERIMENTAL

**Language:** Python

**Package:** scvelo

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://scvelo.readthedocs.io/

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Estimate kinetic expression-state direction from spliced/unspliced RNA.

**Biological question:** Estimate kinetic expression-state direction from spliced/unspliced RNA.

**When to use:** AnnData with spliced/unspliced layers, preprocessing/QC.

**When NOT to use:** Velocity is not automatically causal lineage evidence; splicing data are mandatory.

**Required input:** AnnData with spliced/unspliced layers, preprocessing/QC.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Steady-state/dynamical assumptions; gene filtering.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Velocity is not automatically causal lineage evidence; splicing data are mandatory.

**Outputs:** Velocity; stream/grid plots; latent time.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Velocity is not automatically causal lineage evidence; splicing data are mandatory.

**Assumptions:** Velocity is not automatically causal lineage evidence; splicing data are mandatory.

**Common pitfalls:** Velocity is not automatically causal lineage evidence; splicing data are mandatory.

**Alternatives:** Monocle3/Slingshot when only expression states are available

**When to prefer alternatives:** Monocle3/Slingshot when only expression states are available

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://scvelo.readthedocs.io/
