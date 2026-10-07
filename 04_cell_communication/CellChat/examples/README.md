# Input and smoke validation

Assemble `list(expression = lognormalized_RNA, metadata = cell_metadata)` with matching
column/row names. Input must be non-integrated log-normalized RNA, not scaled residuals.
Select species, labels, sampling design and pathways in `config/default.yml`.
Run from repository root:

```sh
Rscript scripts/run_method.R cellchat 04_cell_communication/CellChat/config/default.yml --allow-unvalidated
Rscript scripts/run_method.R cellchat_compare 04_cell_communication/CellChat/config/compare.yml --allow-unvalidated
```

Before promotion: load the pinned package, run one dataset, assert nonempty LR/pathway tables,
check both PNG/PDF exports, then compare two independently inferred condition objects with
identical cell labels, DB and settings. Register actual paths/parameters/sessionInfo after inspection.
Patterns and manifold comparisons need separate evidence. A pooled two-condition comparison
is descriptive; permutations over cells do not establish donor-level treatment significance.
