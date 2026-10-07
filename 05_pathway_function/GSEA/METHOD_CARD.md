# Method Card

**Method:** fgsea

**Category:** 05_pathway_function

**Status:** CANDIDATE

**Language:** R

**Package:** fgsea

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://bioconductor.org/packages/release/bioc/vignettes/fgsea/inst/doc/fgsea-tutorial.html

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Test ranked gene-set enrichment without an arbitrary DEG cutoff.

**Biological question:** Test ranked gene-set enrichment without an arbitrary DEG cutoff.

**When to use:** list(ranks: complete signed named statistic, pathways: gene-set list); unique compatible IDs.

**When NOT to use:** Rank by a meaningful signed statistic, not P alone or arbitrary PPI degree for transcriptional enrichment. Record ties and mapped coverage; NES comparisons need identical gene-set definitions.

**Required input:** list(ranks: complete signed named statistic, pathways: gene-set list); unique compatible IDs.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** min_size = 15; max_size = 500; seed = 42

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Rank by a meaningful signed statistic, not P alone or arbitrary PPI degree for transcriptional enrichment. Record ties and mapped coverage; NES comparisons need identical gene-set definitions.

**Outputs:** NES, adjusted P, leading-edge table; enrichment curves

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Rank by a meaningful signed statistic, not P alone or arbitrary PPI degree for transcriptional enrichment. Record ties and mapped coverage; NES comparisons need identical gene-set definitions.

**Assumptions:** Rank by a meaningful signed statistic, not P alone or arbitrary PPI degree for transcriptional enrichment. Record ties and mapped coverage; NES comparisons need identical gene-set definitions.

**Common pitfalls:** Rank by a meaningful signed statistic, not P alone or arbitrary PPI degree for transcriptional enrichment. Record ties and mapped coverage; NES comparisons need identical gene-set definitions.

**Alternatives:** ORA for a justified selected list; clusterProfiler GSEA for its result/visualization interface.

**When to prefer alternatives:** ORA for a justified selected list; clusterProfiler GSEA for its result/visualization interface.

**Validated datasets:** None

**Validation status:** BLOCKED — Workflow not executed; required namespace/data unavailable

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 05_pathway_function/GSEA/scripts/workflow.R

**References:** https://bioconductor.org/packages/release/bioc/vignettes/fgsea/inst/doc/fgsea-tutorial.html
