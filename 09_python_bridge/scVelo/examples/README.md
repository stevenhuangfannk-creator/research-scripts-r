# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: AnnData with spliced/unspliced layers, preprocessing/QC.

For executable methods, run `Rscript scripts/run_method.R scvelo 09_python_bridge/scVelo/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
