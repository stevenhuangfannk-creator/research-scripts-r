# Environments

No giant shared Python environment or fabricated renv lockfile is provided.
R package evidence is in validation/package_status.tsv and validation/sessionInfo.txt.
The build used an isolated extra R library (via R_LIBS) to add Matrix 1.6-5 and missing
CRAN Windows binaries; the user's original library was not overwritten. Package binaries
and cache are outside the repository. Paths are local build evidence, not workflow dependencies.

Reproduce on a compatible R release, install the method-specific packages, and run namespace
preflight plus smoke tests before using any recorded status on a new machine. Use renv per
validated workflow after capturing a complete successful environment; avoid inventing a lock
with unavailable CellChat/Monocle3 dependencies. CellChat targets tag v2.1.2; the currently
audited development docs report 2.2.0.9001. Monocle3 targets tag v1.4.27.

CellChat and Monocle3 require source compilation and additional dependencies here. Rtools
is absent. A compatible user-managed R/Bioconductor environment and official small demo
inputs are the next validation requirements. Do not infer runtime compatibility from API review.

Python methods remain candidates. Each must add its own tested environment and pinned package
versions when reproduced; no untested requirements lock is claimed.
