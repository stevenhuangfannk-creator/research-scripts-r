# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Seurat metadata with clusters; explicit cluster-to-label mappings by level plus evidence string.

For executable methods, run `Rscript scripts/run_method.R hierarchical_annotation 01_scrna_core/annotation/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
