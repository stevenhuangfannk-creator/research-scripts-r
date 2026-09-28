# Original State

The upstream repository contains four root files: `.gitignore`, `LICENSE`, `README.Rmd` and rendered `README.md`.

The preserved `README.Rmd` has:

- 3,837 local text lines;
- 99 R chunks;
- 98 chunks marked `eval=FALSE`;
- 12 placeholder or absolute-path references;
- one sequential interactive workflow covering QC, integration, annotation, subsets, disease comparison and cell interaction analysis.

It is valuable as an analysis record and figure map. It is not directly executable from a fresh checkout because it depends on downloaded datasets, previously created in-memory objects, local package versions and manual cluster decisions.

Phase 2 leaves this upstream file unchanged and places all local validation around it.

