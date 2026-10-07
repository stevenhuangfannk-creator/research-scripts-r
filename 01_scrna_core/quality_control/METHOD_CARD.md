# Method Card

**Method:** scrna_qc

**Category:** 01_scrna_core

**Status:** VALIDATED

**Language:** R

**Package:** Seurat

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** 2026-10-07

**Official documentation:** https://satijalab.org/seurat/articles/pbmc3k_tutorial

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Inspect mitochondrial/ribosomal, feature and UMI metrics and record cell retention.

**Biological question:** Inspect mitochondrial/ribosomal, feature and UMI metrics and record cell retention.

**When to use:** Seurat object with RNA counts; explicit species-sensitive patterns and numeric threshold bounds.

**When NOT to use:** A universal mitochondrial cutoff can remove meaningful injury states. Inspect each capture and tissue; QC does not detect all doublets or ambient RNA.

**Required input:** Seurat object with RNA counts; explicit species-sensitive patterns and numeric threshold bounds.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** mt_pattern = ^MT- (human) / ^mt- (mouse); review IDs; ribo_pattern = ^RP[SL] / ^Rp[sl]; thresholds = mandatory, study-specific; filter = False

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** A universal mitochondrial cutoff can remove meaningful injury states. Inspect each capture and tissue; QC does not detect all doublets or ambient RNA.

**Outputs:** per-cell QC table; retention audit; QC-marked or explicitly filtered Seurat object

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** A universal mitochondrial cutoff can remove meaningful injury states. Inspect each capture and tissue; QC does not detect all doublets or ambient RNA.

**Assumptions:** A universal mitochondrial cutoff can remove meaningful injury states. Inspect each capture and tissue; QC does not detect all doublets or ambient RNA.

**Common pitfalls:** A universal mitochondrial cutoff can remove meaningful injury states. Inspect each capture and tissue; QC does not detect all doublets or ambient RNA.

**Alternatives:** scater robust outlier QC; EmptyDrops for calling cells in raw droplets.

**When to prefer alternatives:** scater robust outlier QC; EmptyDrops for calling cells in raw droplets.

**Validated datasets:** pbmc_small plus explicit three-gene arithmetic fixture

**Validation status:** PASS — pbmc_small lacks mitochondrial/ribosomal genes; audit/filter and exact arithmetic guards only

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 01_scrna_core/quality_control/scripts/workflow.R

**References:** https://satijalab.org/seurat/articles/pbmc3k_tutorial
