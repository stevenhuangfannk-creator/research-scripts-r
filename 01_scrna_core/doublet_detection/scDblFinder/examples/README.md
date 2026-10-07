# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Seurat RNA counts with capture/library identifiers (not automatically donor labels).

For executable methods, run `Rscript scripts/run_method.R scdblfinder 01_scrna_core/doublet_detection/scDblFinder/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../../scripts/smoke_tests.R).
