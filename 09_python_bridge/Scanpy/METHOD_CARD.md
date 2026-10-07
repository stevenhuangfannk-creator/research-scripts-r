# Method Card

**Method:** scanpy

**Category:** 09_python_bridge

**Status:** CANDIDATE

**Language:** Python

**Package:** scanpy

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://scanpy.readthedocs.io/

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Provide an independently managed Python route for core scRNA analysis.

**Biological question:** Provide an independently managed Python route for core scRNA analysis.

**When to use:** AnnData counts, metadata and environment specification.

**When NOT to use:** R is the primary route; no shared giant Python environment is imposed.

**Required input:** AnnData counts, metadata and environment specification.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Normalization; PCA; neighbors; clustering seeds.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** R is the primary route; no shared giant Python environment is imposed.

**Outputs:** AnnData; embeddings; marker tables.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** R is the primary route; no shared giant Python environment is imposed.

**Assumptions:** R is the primary route; no shared giant Python environment is imposed.

**Common pitfalls:** R is the primary route; no shared giant Python environment is imposed.

**Alternatives:** Seurat

**When to prefer alternatives:** Seurat

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://scanpy.readthedocs.io/
