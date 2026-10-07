# Method Card

**Method:** scdblfinder

**Category:** 01_scrna_core

**Status:** CANDIDATE

**Language:** R

**Package:** scDblFinder

**Package version:** See [build package evidence](../../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://bioconductor.org/packages/release/bioc/vignettes/scDblFinder/inst/doc/scDblFinder.html

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Flag likely doublets within independent droplet captures.

**Biological question:** Flag likely doublets within independent droplet captures.

**When to use:** Seurat RNA counts with capture/library identifiers (not automatically donor labels).

**When NOT to use:** Doublet rate depends on technology and recovered cells. Homotypic doublets remain difficult; retain audits before removing flagged cells.

**Required input:** Seurat RNA counts with capture/library identifiers (not automatically donor labels).

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** capture_column = capture ID; dbr = None; seed = 42

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Doublet rate depends on technology and recovered cells. Homotypic doublets remain difficult; retain audits before removing flagged cells.

**Outputs:** per-cell doublet score/class; labeled object

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Doublet rate depends on technology and recovered cells. Homotypic doublets remain difficult; retain audits before removing flagged cells.

**Assumptions:** Doublet rate depends on technology and recovered cells. Homotypic doublets remain difficult; retain audits before removing flagged cells.

**Common pitfalls:** Doublet rate depends on technology and recovered cells. Homotypic doublets remain difficult; retain audits before removing flagged cells.

**Alternatives:** DoubletFinder; Scrublet in Python. Compare on the same capture.

**When to prefer alternatives:** DoubletFinder; Scrublet in Python. Compare on the same capture.

**Validated datasets:** None

**Validation status:** BLOCKED — Workflow not executed; required namespace/data unavailable

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 01_scrna_core/doublet_detection/scDblFinder/scripts/workflow.R

**References:** https://bioconductor.org/packages/release/bioc/vignettes/scDblFinder/inst/doc/scDblFinder.html
