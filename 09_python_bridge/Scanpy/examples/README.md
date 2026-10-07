# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: AnnData counts, metadata and environment specification.

For executable methods, run `Rscript scripts/run_method.R scanpy 09_python_bridge/Scanpy/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
