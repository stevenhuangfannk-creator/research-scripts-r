# Method Card

**Method:** soupx

**Category:** 01_scrna_core

**Status:** CANDIDATE

**Language:** R

**Package:** SoupX

**Package version:** See [build package evidence](../../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://github.com/constantAmateur/SoupX

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Estimate ambient contamination using raw droplets and cluster structure.

**Biological question:** Estimate ambient contamination using raw droplets and cluster structure.

**When to use:** Raw and filtered count matrices, cluster labels.

**When NOT to use:** Requires informative ambient profile; validate retained biological expression.

**Required input:** Raw and filtered count matrices, cluster labels.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Soup fraction; non-expressing markers.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Requires informative ambient profile; validate retained biological expression.

**Outputs:** Contamination fraction; adjusted counts.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Requires informative ambient profile; validate retained biological expression.

**Assumptions:** Requires informative ambient profile; validate retained biological expression.

**Common pitfalls:** Requires informative ambient profile; validate retained biological expression.

**Alternatives:** DecontX

**When to prefer alternatives:** DecontX

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://github.com/constantAmateur/SoupX
