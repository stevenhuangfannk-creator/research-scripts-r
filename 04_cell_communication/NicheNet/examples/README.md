# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Sender/receiver expression, receiver DEG, background expressed genes, prior networks.

For executable methods, run `Rscript scripts/run_method.R nichenet 04_cell_communication/NicheNet/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
