# Method Card

**Method:** pseudobulk

**Category:** 02_differential_analysis

**Status:** VALIDATED

**Language:** R

**Package:** Seurat

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** 2026-10-07

**Official documentation:** https://satijalab.org/seurat/reference/aggregateexpression

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Sum raw counts per biological sample and cell type.

**Biological question:** Sum raw counts per biological sample and cell type.

**When to use:** Raw RNA Seurat plus sample and cell-type identifiers.

**When NOT to use:** Summation is not a DEG test. Retain condition/covariate sample table, sufficient independent donors and within-subject design where needed.

**Required input:** Raw RNA Seurat plus sample and cell-type identifiers.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** sample_column = biological sample; celltype_column = reviewed annotation

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Summation is not a DEG test. Retain condition/covariate sample table, sufficient independent donors and within-subject design where needed.

**Outputs:** pseudobulk count matrix; library-size audit

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Summation is not a DEG test. Retain condition/covariate sample table, sufficient independent donors and within-subject design where needed.

**Assumptions:** Summation is not a DEG test. Retain condition/covariate sample table, sufficient independent donors and within-subject design where needed.

**Common pitfalls:** Summation is not a DEG test. Retain condition/covariate sample table, sufficient independent donors and within-subject design where needed.

**Alternatives:** DESeq2/edgeR/limma-voom for sample-level testing; mixed models for justified cell-level designs.

**When to prefer alternatives:** DESeq2/edgeR/limma-voom for sample-level testing; mixed models for justified cell-level designs.

**Validated datasets:** Seurat::pbmc_small (one original sample)

**Validation status:** PASS — Raw-count summation/count conservation only; replicated condition testing is unvalidated

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 02_differential_analysis/pseudobulk/scripts/workflow.R

**References:** https://satijalab.org/seurat/reference/aggregateexpression
