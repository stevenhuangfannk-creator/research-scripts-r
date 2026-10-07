# Method Card

**Method:** bulk_deseq2

**Category:** 07_bulk_clinical_ml

**Status:** CANDIDATE

**Language:** R

**Package:** DESeq2

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://bioconductor.org/packages/DESeq2

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Test replicated condition changes from raw bulk/pseudobulk counts.

**Biological question:** Test replicated condition changes from raw bulk/pseudobulk counts.

**When to use:** Raw integer counts and aligned sample design/contrast.

**When NOT to use:** Do not input TPM/FPKM as counts; paired design and confounding require explicit handling.

**Required input:** Raw integer counts and aligned sample design/contrast.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Design formula; reference level; shrinkage; independent filtering.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Do not input TPM/FPKM as counts; paired design and confounding require explicit handling.

**Outputs:** DEG effects/FDR; normalized counts; dispersion/MA diagnostics.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Do not input TPM/FPKM as counts; paired design and confounding require explicit handling.

**Assumptions:** Do not input TPM/FPKM as counts; paired design and confounding require explicit handling.

**Common pitfalls:** Do not input TPM/FPKM as counts; paired design and confounding require explicit handling.

**Alternatives:** limma-voom; edgeR

**When to prefer alternatives:** limma-voom; edgeR

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://bioconductor.org/packages/DESeq2
