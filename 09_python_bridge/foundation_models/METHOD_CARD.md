# Method Card

**Method:** foundation_models

**Category:** 09_python_bridge

**Status:** EXPERIMENTAL

**Language:** Python

**Package:** model-specific

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://github.com/bowang-lab/scGPT

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Evaluate pretrained representation transfer against simple baselines.

**Biological question:** Evaluate pretrained representation transfer against simple baselines.

**When to use:** Model-compatible expression tokens, checkpoints, training-domain audit.

**When NOT to use:** Experimental until domain shift, leakage and baseline benefit are audited; no default checkpoint.

**Required input:** Model-compatible expression tokens, checkpoints, training-domain audit.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Checkpoint; vocabulary; normalization; evaluation split.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Experimental until domain shift, leakage and baseline benefit are audited; no default checkpoint.

**Outputs:** Embeddings or task predictions with baseline comparison.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Experimental until domain shift, leakage and baseline benefit are audited; no default checkpoint.

**Assumptions:** Experimental until domain shift, leakage and baseline benefit are audited; no default checkpoint.

**Common pitfalls:** Experimental until domain shift, leakage and baseline benefit are audited; no default checkpoint.

**Alternatives:** PCA; validated integration/reference methods

**When to prefer alternatives:** PCA; validated integration/reference methods

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://github.com/bowang-lab/scGPT
