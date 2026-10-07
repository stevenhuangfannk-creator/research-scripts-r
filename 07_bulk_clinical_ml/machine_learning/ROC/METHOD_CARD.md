# Method Card

**Method:** roc

**Category:** 07_bulk_clinical_ml

**Status:** CANDIDATE

**Language:** R

**Package:** pROC / timeROC

**Package version:** See [build package evidence](../../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://cran.r-project.org/package=pROC

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Assess discrimination from held-out binary or time-to-event predictions.

**Biological question:** Assess discrimination from held-out binary or time-to-event predictions.

**When to use:** Held-out outcomes/scores; event times and censoring for time-dependent ROC.

**When NOT to use:** Conventional ROC is inappropriate for censored survival outcomes; horizon and calibration also matter.

**Required input:** Held-out outcomes/scores; event times and censoring for time-dependent ROC.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Positive class; score direction; horizons; IPCW estimator.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Conventional ROC is inappropriate for censored survival outcomes; horizon and calibration also matter.

**Outputs:** ROC/AUC and CI; time-dependent AUC.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Conventional ROC is inappropriate for censored survival outcomes; horizon and calibration also matter.

**Assumptions:** Conventional ROC is inappropriate for censored survival outcomes; horizon and calibration also matter.

**Common pitfalls:** Conventional ROC is inappropriate for censored survival outcomes; horizon and calibration also matter.

**Alternatives:** PR curve for severe imbalance; calibration curves

**When to prefer alternatives:** PR curve for severe imbalance; calibration curves

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://cran.r-project.org/package=pROC
