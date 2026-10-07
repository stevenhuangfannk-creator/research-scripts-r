# Method Card

**Method:** survival_km

**Category:** 07_bulk_clinical_ml

**Status:** VALIDATED

**Language:** R

**Package:** survival

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** 2026-10-07

**Official documentation:** https://cran.r-project.org/package=survival

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Estimate right-censored survival curves and uncertainty by explicit group.

**Biological question:** Estimate right-censored survival curves and uncertainty by explicit group.

**When to use:** data.frame with nonnegative time, event explicitly coded 0/1 and group.

**When NOT to use:** Requires appropriately independent censoring and correct time origin. KM does not adjust covariates; competing risks require cumulative-incidence methods.

**Required input:** data.frame with nonnegative time, event explicitly coded 0/1 and group.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** time_column = explicit; event_column = explicit 0/1; group_column = explicit

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Requires appropriately independent censoring and correct time origin. KM does not adjust covariates; competing risks require cumulative-incidence methods.

**Outputs:** survfit object; survival, 95% CI, risk counts and event table

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Requires appropriately independent censoring and correct time origin. KM does not adjust covariates; competing risks require cumulative-incidence methods.

**Assumptions:** Requires appropriately independent censoring and correct time origin. KM does not adjust covariates; competing risks require cumulative-incidence methods.

**Common pitfalls:** Requires appropriately independent censoring and correct time origin. KM does not adjust covariates; competing risks require cumulative-incidence methods.

**Alternatives:** Cox for covariates; competing-risk analysis for competing events.

**When to prefer alternatives:** Cox for covariates; competing-risk analysis for competing events.

**Validated datasets:** survival::lung (228 public clinical records)

**Validation status:** PASS — Right-censored KM curve/CI table with explicit 0/1 event mapping; no new clinical interpretation

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 07_bulk_clinical_ml/survival/scripts/workflow.R

**References:** https://cran.r-project.org/package=survival
