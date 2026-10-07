# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Features and Surv outcome plus patient-level folds.

For executable methods, run `Rscript scripts/run_method.R lasso_cox 07_bulk_clinical_ml/LASSO_Cox/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
