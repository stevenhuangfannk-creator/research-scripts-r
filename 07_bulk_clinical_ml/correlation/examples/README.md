# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: data.frame of numeric measurements on independent observational units.

For executable methods, run `Rscript scripts/run_method.R correlation 07_bulk_clinical_ml/correlation/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
