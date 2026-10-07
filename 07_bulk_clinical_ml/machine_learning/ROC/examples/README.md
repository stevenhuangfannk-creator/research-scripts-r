# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Held-out outcomes/scores; event times and censoring for time-dependent ROC.

For executable methods, run `Rscript scripts/run_method.R roc 07_bulk_clinical_ml/machine_learning/ROC/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../../scripts/smoke_tests.R).
