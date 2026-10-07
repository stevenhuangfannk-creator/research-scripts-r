# Method Card

**Method:** seurat_integration

**Category:** 01_scrna_core

**Status:** CANDIDATE

**Language:** R

**Package:** Seurat

**Package version:** See [build package evidence](../../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://satijalab.org/seurat/articles/integration_introduction

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Build a shared geometry with Seurat anchor integration.

**Biological question:** Build a shared geometry with Seurat anchor integration.

**When to use:** Seurat with RNA and explicit batch IDs; sufficiently populated batches.

**When NOT to use:** Baseline uses the stable anchor interface, not an asserted default v5 layer workflow. Avoid integrated values for DEG/CellChat; compare mixing and overcorrection.

**Required input:** Seurat with RNA and explicit batch IDs; sufficiently populated batches.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** batch_column = technical batch; nfeatures = 2000; npcs = 30

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Baseline uses the stable anchor interface, not an asserted default v5 layer workflow. Avoid integrated values for DEG/CellChat; compare mixing and overcorrection.

**Outputs:** integrated assay; retained RNA assay

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Baseline uses the stable anchor interface, not an asserted default v5 layer workflow. Avoid integrated values for DEG/CellChat; compare mixing and overcorrection.

**Assumptions:** Baseline uses the stable anchor interface, not an asserted default v5 layer workflow. Avoid integrated values for DEG/CellChat; compare mixing and overcorrection.

**Common pitfalls:** Baseline uses the stable anchor interface, not an asserted default v5 layer workflow. Avoid integrated values for DEG/CellChat; compare mixing and overcorrection.

**Alternatives:** Harmony; Seurat v5 IntegrateLayers after separate version-specific validation.

**When to prefer alternatives:** Harmony; Seurat v5 IntegrateLayers after separate version-specific validation.

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 01_scrna_core/batch_integration/Seurat/scripts/workflow.R

**References:** https://satijalab.org/seurat/articles/integration_introduction
