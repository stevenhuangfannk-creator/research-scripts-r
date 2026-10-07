# Method Card

**Method:** cellrank

**Category:** 09_python_bridge

**Status:** EXPERIMENTAL

**Language:** Python

**Package:** cellrank

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://cellrank.readthedocs.io/

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Estimate state-transition and fate probabilities using explicit kernels.

**Biological question:** Estimate state-transition and fate probabilities using explicit kernels.

**When to use:** AnnData, kernel and justified terminal-state definitions.

**When NOT to use:** Transition-kernel assumptions and terminal choices dominate interpretation.

**Required input:** AnnData, kernel and justified terminal-state definitions.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Kernel weights; estimator; terminal states.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Transition-kernel assumptions and terminal choices dominate interpretation.

**Outputs:** Macrostates; absorption/fate probabilities; driver candidates.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Transition-kernel assumptions and terminal choices dominate interpretation.

**Assumptions:** Transition-kernel assumptions and terminal choices dominate interpretation.

**Common pitfalls:** Transition-kernel assumptions and terminal choices dominate interpretation.

**Alternatives:** Trajectory ordering or velocity for different questions

**When to prefer alternatives:** Trajectory ordering or velocity for different questions

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://cellrank.readthedocs.io/
