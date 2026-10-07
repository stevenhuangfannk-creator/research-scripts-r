# Examples and validation

Current validation: **UNVALIDATED** — No executable evidence in this build.

Input: Normalized gene × independent-sample matrix and gene sets.

For executable methods, run `Rscript scripts/run_method.R gsva_ssgsea 05_pathway_function/GSVA_ssGSEA/config/default.yml` from repository root after supplying real input and reviewing config. Unvalidated methods require the explicit `--allow-unvalidated` flag. Candidate-only methods have no runnable example. See the shared [smoke suite](../../../scripts/smoke_tests.R).
