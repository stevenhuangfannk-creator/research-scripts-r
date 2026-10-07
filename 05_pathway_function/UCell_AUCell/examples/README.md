# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Cell expression ranks/counts and specified signature gene sets.

For executable methods, run `Rscript scripts/run_method.R ucell_aucell 05_pathway_function/UCell_AUCell/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
