# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Raw RNA Seurat plus sample and cell-type identifiers.

For executable methods, run `Rscript scripts/run_method.R pseudobulk 02_differential_analysis/pseudobulk/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
