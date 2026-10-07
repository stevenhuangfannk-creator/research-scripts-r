# Method Card

**Method:** harmony

**Category:** 01_scrna_core

**Status:** CANDIDATE

**Language:** R

**Package:** harmony

**Package version:** See [build package evidence](../../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://portals.broadinstitute.org/harmony/articles/quickstart.html

**Original paper:** https://doi.org/10.1038/s41592-019-0619-0

**Purpose:** Align a PCA embedding across measured technical batches.

**Biological question:** Align a PCA embedding across measured technical batches.

**When to use:** Normalized Seurat with PCA and explicit batch column.

**When NOT to use:** Cannot recover treatment effects perfectly confounded with batch. Harmony corrects an embedding, not raw counts; evaluate mixing and lineage preservation.

**Required input:** Normalized Seurat with PCA and explicit batch column.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** batch_column = technical batch; npcs = 30; theta = 2

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Cannot recover treatment effects perfectly confounded with batch. Harmony corrects an embedding, not raw counts; evaluate mixing and lineage preservation.

**Outputs:** Harmony embedding

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Cannot recover treatment effects perfectly confounded with batch. Harmony corrects an embedding, not raw counts; evaluate mixing and lineage preservation.

**Assumptions:** Cannot recover treatment effects perfectly confounded with batch. Harmony corrects an embedding, not raw counts; evaluate mixing and lineage preservation.

**Common pitfalls:** Cannot recover treatment effects perfectly confounded with batch. Harmony corrects an embedding, not raw counts; evaluate mixing and lineage preservation.

**Alternatives:** Seurat anchors; unintegrated analysis when batch biology cannot be separated.

**When to prefer alternatives:** Seurat anchors; unintegrated analysis when batch biology cannot be separated.

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 01_scrna_core/batch_integration/Harmony/scripts/workflow.R

**References:** https://portals.broadinstitute.org/harmony/articles/quickstart.html; https://doi.org/10.1038/s41592-019-0619-0
