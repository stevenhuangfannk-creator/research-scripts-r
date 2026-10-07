# Method Card

**Method:** random_forest

**Category:** 07_bulk_clinical_ml

**Status:** CANDIDATE

**Language:** R

**Package:** randomForest

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://cran.r-project.org/package=randomForest

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Predict outcomes with a baseline ensemble and held-out performance.

**Biological question:** Predict outcomes with a baseline ensemble and held-out performance.

**When to use:** Sample-level features/outcome and leakage-free train/test split.

**When NOT to use:** OOB does not replace independent external validation; importance is not mechanism.

**Required input:** Sample-level features/outcome and leakage-free train/test split.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = ntree; mtry; class weights; seed.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** OOB does not replace independent external validation; importance is not mechanism.

**Outputs:** OOB error; held-out predictions; importance; ROC when appropriate.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** OOB does not replace independent external validation; importance is not mechanism.

**Assumptions:** OOB does not replace independent external validation; importance is not mechanism.

**Common pitfalls:** OOB does not replace independent external validation; importance is not mechanism.

**Alternatives:** ranger; regularized logistic regression

**When to prefer alternatives:** ranger; regularized logistic regression

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://cran.r-project.org/package=randomForest
