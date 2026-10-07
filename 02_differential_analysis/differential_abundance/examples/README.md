# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Counts/neighbor graph and biological-sample design.

For executable methods, run `Rscript scripts/run_method.R differential_abundance 02_differential_analysis/differential_abundance/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
