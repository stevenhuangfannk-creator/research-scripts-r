# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Training features/outcome, fixed sample-level folds, held-out validation.

For executable methods, run `Rscript scripts/run_method.R lasso 07_bulk_clinical_ml/LASSO/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
