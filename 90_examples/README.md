# Validation contexts

- [Original project mapping](../99_legacy_projects/README.md): historical sources; absent APAP/GSE255834 inputs prevent certification.
- [R smoke suite](../scripts/smoke_tests.R): Seurat pbmc_small, iris and survival::lung; scope is recorded per method.
- [Validation evidence](../docs/validation/): actual logs, package status and scoped PASS/BLOCKED results.
- [Existing reproduction history](../reproductions/README.md): preserved without extending spatial workflows.

Generated large/intermediate objects stay outside Git. Built-in datasets are loaded from installed packages; synthetic plot fixtures are kept in explicit demo code.
