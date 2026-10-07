# Method Card

**Method:** go_kegg_ora

**Category:** 05_pathway_function

**Status:** CANDIDATE

**Language:** R

**Package:** clusterProfiler

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://yulab-smu.top/biomedical-knowledge-mining-book/

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Test over-representation of selected genes against the actually tested universe.

**Biological question:** Test over-representation of selected genes against the actually tested universe.

**When to use:** list(genes, universe), matched IDs, species and database.

**When NOT to use:** The universe is tested/detectable genes, not the whole genome by habit. GO hierarchy yields dependent terms; report database version and mapping losses. KEGG access/licensing needs review.

**Required input:** list(genes, universe), matched IDs, species and database.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** ontology = BP / MF / CC / KEGG; key_type = database-compatible ID; organism = explicit; p_adjust = BH

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** The universe is tested/detectable genes, not the whole genome by habit. GO hierarchy yields dependent terms; report database version and mapping losses. KEGG access/licensing needs review.

**Outputs:** enrichment effect/count/FDR table; enrichResult object

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** The universe is tested/detectable genes, not the whole genome by habit. GO hierarchy yields dependent terms; report database version and mapping losses. KEGG access/licensing needs review.

**Assumptions:** The universe is tested/detectable genes, not the whole genome by habit. GO hierarchy yields dependent terms; report database version and mapping losses. KEGG access/licensing needs review.

**Common pitfalls:** The universe is tested/detectable genes, not the whole genome by habit. GO hierarchy yields dependent terms; report database version and mapping losses. KEGG access/licensing needs review.

**Alternatives:** GSEA when a complete ranked test statistic is available; cell-level score for cell states.

**When to prefer alternatives:** GSEA when a complete ranked test statistic is available; cell-level score for cell states.

**Validated datasets:** None

**Validation status:** BLOCKED — Workflow not executed; required namespace/data unavailable

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 05_pathway_function/GO_KEGG/scripts/workflow.R

**References:** https://yulab-smu.top/biomedical-knowledge-mining-book/
