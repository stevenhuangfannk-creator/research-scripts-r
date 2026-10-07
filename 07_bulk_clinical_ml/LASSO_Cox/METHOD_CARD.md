# Method Card

**Method:** lasso_cox

**Category:** 07_bulk_clinical_ml

**Status:** CANDIDATE

**Language:** R

**Package:** glmnet

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://glmnet.stanford.edu/articles/Coxnet.html

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Fit a penalized survival model with censor-aware validation.

**Biological question:** Fit a penalized survival model with censor-aware validation.

**When to use:** Features and Surv outcome plus patient-level folds.

**When NOT to use:** Do not select genes globally before CV or claim causality from selected features.

**Required input:** Features and Surv outcome plus patient-level folds.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Lambda selection; event balance; censoring-aware metrics.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Do not select genes globally before CV or claim causality from selected features.

**Outputs:** CV path; risk score; held-out discrimination/calibration.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Do not select genes globally before CV or claim causality from selected features.

**Assumptions:** Do not select genes globally before CV or claim causality from selected features.

**Common pitfalls:** Do not select genes globally before CV or claim causality from selected features.

**Alternatives:** Cox; elastic-net Cox

**When to prefer alternatives:** Cox; elastic-net Cox

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://glmnet.stanford.edu/articles/Coxnet.html
