# Method Card

**Method:** lasso

**Category:** 07_bulk_clinical_ml

**Status:** CANDIDATE

**Language:** R

**Package:** glmnet

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://glmnet.stanford.edu/articles/glmnet.html

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Fit penalized regression with separated tuning and test assessment.

**Biological question:** Fit penalized regression with separated tuning and test assessment.

**When to use:** Training features/outcome, fixed sample-level folds, held-out validation.

**When NOT to use:** All filtering/scaling/selection must occur inside training folds.

**Required input:** Training features/outcome, fixed sample-level folds, held-out validation.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Family; alpha=1; lambda.min vs lambda.1se; fold design.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** All filtering/scaling/selection must occur inside training folds.

**Outputs:** CV curve; coefficient path; selected coefficients; held-out predictions.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** All filtering/scaling/selection must occur inside training folds.

**Assumptions:** All filtering/scaling/selection must occur inside training folds.

**Common pitfalls:** All filtering/scaling/selection must occur inside training folds.

**Alternatives:** Elastic net; prespecified simpler models

**When to prefer alternatives:** Elastic net; prespecified simpler models

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://glmnet.stanford.edu/articles/glmnet.html
