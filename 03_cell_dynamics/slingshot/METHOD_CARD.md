# Method Card

**Method:** slingshot

**Category:** 03_cell_dynamics

**Status:** CANDIDATE

**Language:** R

**Package:** slingshot

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://bioconductor.org/packages/slingshot

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Fit lineage curves through a cluster scaffold.

**Biological question:** Fit lineage curves through a cluster scaffold.

**When to use:** Embedding, cluster labels, justified starting cluster.

**When NOT to use:** Topology depends on clustering and starting assumptions.

**Required input:** Embedding, cluster labels, justified starting cluster.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = start.clus; end.clus; shrinkage.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Topology depends on clustering and starting assumptions.

**Outputs:** Lineages; pseudotime; curve weights.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Topology depends on clustering and starting assumptions.

**Assumptions:** Topology depends on clustering and starting assumptions.

**Common pitfalls:** Topology depends on clustering and starting assumptions.

**Alternatives:** Monocle3; tradeSeq downstream

**When to prefer alternatives:** Monocle3; tradeSeq downstream

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://bioconductor.org/packages/slingshot
