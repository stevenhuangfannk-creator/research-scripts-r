# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Sample-level features/outcome and leakage-free train/test split.

For executable methods, run `Rscript scripts/run_method.R random_forest 07_bulk_clinical_ml/random_forest/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
