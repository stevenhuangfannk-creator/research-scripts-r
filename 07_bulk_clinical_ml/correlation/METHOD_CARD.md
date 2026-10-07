# Method Card

**Method:** correlation

**Category:** 07_bulk_clinical_ml

**Status:** VALIDATED

**Language:** R

**Package:** stats

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** 2026-10-07

**Official documentation:** https://stat.ethz.ch/R-manual/R-devel/library/stats/html/cor.test.html

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Estimate Pearson/Spearman associations with explicit missingness and BH adjustment.

**Biological question:** Estimate Pearson/Spearman associations with explicit missingness and BH adjustment.

**When to use:** data.frame of numeric measurements on independent observational units.

**When NOT to use:** Correlation ≠ causation. Pearson evaluates linear association; Spearman evaluates monotonic rank association. Repeated or confounded observations need another model.

**Required input:** data.frame of numeric measurements on independent observational units.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** variables = explicit numeric columns; method = pearson / spearman; missing = error / pairwise

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Correlation ≠ causation. Pearson evaluates linear association; Spearman evaluates monotonic rank association. Repeated or confounded observations need another model.

**Outputs:** r/rho, P, BH-adjusted P, n and exclusions; Pearson CI; Spearman CI unavailable in this baseline

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Correlation ≠ causation. Pearson evaluates linear association; Spearman evaluates monotonic rank association. Repeated or confounded observations need another model.

**Assumptions:** Correlation ≠ causation. Pearson evaluates linear association; Spearman evaluates monotonic rank association. Repeated or confounded observations need another model.

**Common pitfalls:** Correlation ≠ causation. Pearson evaluates linear association; Spearman evaluates monotonic rank association. Repeated or confounded observations need another model.

**Alternatives:** Partial/regression models for covariates; mixed models for repeated measurements.

**When to prefer alternatives:** Partial/regression models for covariates; mixed models for repeated measurements.

**Validated datasets:** datasets::iris (150 observed flowers)

**Validation status:** PASS — Pearson/Spearman tests, BH adjustment and missing/constant-input regression cases; pooled species are confounded

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 07_bulk_clinical_ml/correlation/scripts/workflow.R

**References:** https://stat.ethz.ch/R-manual/R-devel/library/stats/html/cor.test.html
