# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: list(genes, universe), matched IDs, species and database.

For executable methods, run `Rscript scripts/run_method.R go_kegg_ora 05_pathway_function/GO_KEGG/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
