# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Normalized RNA Seurat with grouping labels.

For executable methods, run `Rscript scripts/run_method.R cell_markers 02_differential_analysis/differential_expression/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
