# Method Card

**Method:** decontx

**Category:** 01_scrna_core

**Status:** CANDIDATE

**Language:** R

**Package:** celda

**Package version:** See [build package evidence](../../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://bioconductor.org/packages/release/bioc/vignettes/celda/inst/doc/decontX.html

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Estimate and reduce ambient RNA separately by capture.

**Biological question:** Estimate and reduce ambient RNA separately by capture.

**When to use:** list(counts, aligned metadata, backgrounds = capture-named empty-droplet matrices); background can be absent.

**When NOT to use:** Background feature IDs must exactly match cell counts. Do not use already normalized counts; compare marker specificity and retained biology before adoption.

**Required input:** list(counts, aligned metadata, backgrounds = capture-named empty-droplet matrices); background can be absent.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** capture_column = capture ID; seed = 42

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Background feature IDs must exactly match cell counts. Do not use already normalized counts; compare marker specificity and retained biology before adoption.

**Outputs:** corrected counts per capture; contamination estimates

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Background feature IDs must exactly match cell counts. Do not use already normalized counts; compare marker specificity and retained biology before adoption.

**Assumptions:** Background feature IDs must exactly match cell counts. Do not use already normalized counts; compare marker specificity and retained biology before adoption.

**Common pitfalls:** Background feature IDs must exactly match cell counts. Do not use already normalized counts; compare marker specificity and retained biology before adoption.

**Alternatives:** SoupX when raw/filtered droplets and cluster information are available.

**When to prefer alternatives:** SoupX when raw/filtered droplets and cluster information are available.

**Validated datasets:** None

**Validation status:** BLOCKED — Workflow not executed; required namespace/data unavailable

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 01_scrna_core/ambient_rna/DecontX/scripts/workflow.R

**References:** https://bioconductor.org/packages/release/bioc/vignettes/celda/inst/doc/decontX.html
