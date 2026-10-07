# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Normalized Seurat with PCA and explicit batch column.

For executable methods, run `Rscript scripts/run_method.R harmony 01_scrna_core/batch_integration/Harmony/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../../scripts/smoke_tests.R).
