# Method Card

**Method:** hdwgcna

**Category:** 06_gene_networks

**Status:** CANDIDATE

**Language:** R

**Package:** hdWGCNA

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://smorabit.github.io/hdWGCNA/

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Build coexpression modules using explicitly defined single-cell aggregation.

**Biological question:** Build coexpression modules using explicitly defined single-cell aggregation.

**When to use:** Annotated Seurat, donor/celltype design and metacell choices.

**When NOT to use:** Metacells are not new independent biological replicates.

**Required input:** Annotated Seurat, donor/celltype design and metacell choices.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Metacells; donor preservation; soft threshold.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Metacells are not new independent biological replicates.

**Outputs:** Modules; eigengene activity; module networks.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Metacells are not new independent biological replicates.

**Assumptions:** Metacells are not new independent biological replicates.

**Common pitfalls:** Metacells are not new independent biological replicates.

**Alternatives:** WGCNA on sample-level profiles

**When to prefer alternatives:** WGCNA on sample-level profiles

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://smorabit.github.io/hdWGCNA/
