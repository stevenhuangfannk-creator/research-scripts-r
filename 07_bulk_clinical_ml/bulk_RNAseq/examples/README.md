# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Raw integer counts and aligned sample design/contrast.

For executable methods, run `Rscript scripts/run_method.R bulk_deseq2 07_bulk_clinical_ml/bulk_RNAseq/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
