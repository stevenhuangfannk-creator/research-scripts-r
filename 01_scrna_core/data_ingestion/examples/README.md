# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: RDS list(counts: nonnegative gene × barcode matrix, metadata: barcode-indexed data.frame).

For executable methods, run `Rscript scripts/run_method.R seurat_ingestion 01_scrna_core/data_ingestion/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
