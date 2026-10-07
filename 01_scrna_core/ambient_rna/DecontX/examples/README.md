# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: list(counts, aligned metadata, backgrounds = capture-named empty-droplet matrices); background can be absent.

For executable methods, run `Rscript scripts/run_method.R decontx 01_scrna_core/ambient_rna/DecontX/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../../scripts/smoke_tests.R).
