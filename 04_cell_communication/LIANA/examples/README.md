# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: AnnData or supported R interface, labels and compatible LR resource.

For executable methods, run `Rscript scripts/run_method.R liana_plus 04_cell_communication/LIANA/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
