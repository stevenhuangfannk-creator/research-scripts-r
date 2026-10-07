# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: data.frame with nonnegative time, event explicitly coded 0/1 and group.

For executable methods, run `Rscript scripts/run_method.R survival_km 07_bulk_clinical_ml/survival/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
