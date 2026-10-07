# Method Card

**Method:** cox

**Category:** 07_bulk_clinical_ml

**Status:** VALIDATED

**Language:** R

**Package:** survival

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** 2026-10-07

**Official documentation:** https://cran.r-project.org/package=survival

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Estimate adjusted/unadjusted hazard ratios and inspect proportional hazards.

**Biological question:** Estimate adjusted/unadjusted hazard ratios and inspect proportional hazards.

**When to use:** Complete observation table, explicit time/event and covariates.

**When NOT to use:** Specify continuous-effect forms and coding; assess PH, events, influential observations and confounding. Predictive claims require independent validation.

**Required input:** Complete observation table, explicit time/event and covariates.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** covariates = one for univariate; several justified covariates for multivariate

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Specify continuous-effect forms and coding; assess PH, events, influential observations and confounding. Predictive claims require independent validation.

**Outputs:** Cox model; HR and 95% CI table; cox.zph diagnostics

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Specify continuous-effect forms and coding; assess PH, events, influential observations and confounding. Predictive claims require independent validation.

**Assumptions:** Specify continuous-effect forms and coding; assess PH, events, influential observations and confounding. Predictive claims require independent validation.

**Common pitfalls:** Specify continuous-effect forms and coding; assess PH, events, influential observations and confounding. Predictive claims require independent validation.

**Alternatives:** Time-varying effects or alternative survival models when PH fails.

**When to prefer alternatives:** Time-varying effects or alternative survival models when PH fails.

**Validated datasets:** survival::lung (age and sex covariates)

**Validation status:** PASS — Cox HR/CI and proportional-hazards diagnostic output only; no predictive or causal certification

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 07_bulk_clinical_ml/Cox/scripts/workflow.R

**References:** https://cran.r-project.org/package=survival
