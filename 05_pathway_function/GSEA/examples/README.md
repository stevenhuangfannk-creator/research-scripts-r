# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: list(ranks: complete signed named statistic, pathways: gene-set list); unique compatible IDs.

For executable methods, run `Rscript scripts/run_method.R fgsea 05_pathway_function/GSEA/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
