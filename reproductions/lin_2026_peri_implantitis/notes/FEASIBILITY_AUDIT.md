# Feasibility Audit

## Assessment

**Overall difficulty: VERY HIGH.** The project combines 21 scRNA-seq samples, two spatial cohorts, several probabilistic or graph-based models, mixed R/Python tools and unavailable author code. Public processed counts make the foundational reconstruction feasible, but exact reproduction is not possible for steps whose parameters or intermediate annotations were not released.

## Available

- Full paper PDF supplied by the user.
- Official supplementary PDF.
- Eight PI filtered 10x H5 files and a PI Space Ranger output archive on Zenodo.
- Healthy oral scRNA-seq reference `GSE164241`.
- Healthy spatial reference `GSE206621`.
- Reported software names and some versions/reference builds.

## Unavailable or unresolved

- Author analysis code and environment lockfiles.
- Raw PI FASTQ files and Cell Ranger invocation details.
- Exact doublet procedure, most QC thresholds, seeds and integration hyperparameters.
- Complete annotation decision rules and intermediate objects.
- Exact parameters/databases for MiloR, CellChat, COMMOT, SCENIC, CellOracle, cell2location and NMF.
- Experimental inputs required to reproduce wet-lab and animal panels.

## Resource estimate and sequencing

- The two Zenodo archives total about 346 MB compressed. Expanded counts and derived objects will be larger but fit current local storage.
- scVI can run on CPU but model tuning may be slow. GPU availability will be checked rather than assumed.
- SCENIC, CellOracle and full spatial probabilistic fitting may require substantial compute and external databases. They remain downstream gated modules.
- A project-local Python environment is practical. R-only modules may require a later isolated `renv` environment; the known global R 4.3.1 package incompatibility will not be reused.

## Primary risks

1. Healthy sample selection may not match the unpublished integrated metadata exactly.
2. Differences in QC/doublet removal can propagate to cell states and abundance estimates.
3. Cell annotation and trajectory roots contain biological judgment not fully specified by the paper.
4. Donor D6 has two PI samples, so naive sample-level tests can pseudoreplicate one donor.
5. Tool/database drift may change ligand-receptor and regulatory-network results.
6. Exact numerical agreement may be impossible without author objects even when the overall analytical logic is recovered.

## Decision

Proceed in gated scientific order. The absence of author code changes the claim level to transparent method reconstruction; it does not prevent the project. Refactor and reusable asset extraction are deferred until working outputs pass paper-oriented validation.

