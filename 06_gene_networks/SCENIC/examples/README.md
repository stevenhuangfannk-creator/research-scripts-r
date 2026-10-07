# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Expression, species-compatible motif databases and TF annotations.

For executable methods, run `Rscript scripts/run_method.R scenic 06_gene_networks/SCENIC/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
