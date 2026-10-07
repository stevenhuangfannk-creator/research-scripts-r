# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Embedding, cluster labels, justified starting cluster.

For executable methods, run `Rscript scripts/run_method.R slingshot 03_cell_dynamics/slingshot/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
