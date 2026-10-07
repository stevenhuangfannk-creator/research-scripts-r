# Method Card

**Method:** ppi

**Category:** 06_gene_networks

**Status:** CANDIDATE

**Language:** R

**Package:** igraph / ggraph / STRING

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://string-db.org/help/api/

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Analyze an actual protein-interaction graph and report network topology.

**Biological question:** Analyze an actual protein-interaction graph and report network topology.

**When to use:** Species-specific mapped protein IDs and provenance-bearing STRING edges.

**When NOT to use:** MCC requires a specified CytoHubba implementation; do not substitute degree. CellChat projection is a different operation.

**Required input:** Species-specific mapped protein IDs and provenance-bearing STRING edges.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Species; STRING score; evidence channel; directedness.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** MCC requires a specified CytoHubba implementation; do not substitute degree. CellChat projection is a different operation.

**Outputs:** Network; degree/betweenness; hub table; Cytoscape export.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** MCC requires a specified CytoHubba implementation; do not substitute degree. CellChat projection is a different operation.

**Assumptions:** MCC requires a specified CytoHubba implementation; do not substitute degree. CellChat projection is a different operation.

**Common pitfalls:** MCC requires a specified CytoHubba implementation; do not substitute degree. CellChat projection is a different operation.

**Alternatives:** WGCNA for coexpression; SCENIC for regulons

**When to prefer alternatives:** WGCNA for coexpression; SCENIC for regulons

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://string-db.org/help/api/
