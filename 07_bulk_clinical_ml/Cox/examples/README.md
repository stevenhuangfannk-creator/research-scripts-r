# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Complete observation table, explicit time/event and covariates.

For executable methods, run `Rscript scripts/run_method.R cox 07_bulk_clinical_ml/Cox/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
