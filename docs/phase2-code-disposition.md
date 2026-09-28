# Phase 2 Existing Code Disposition

Phase 2 does not move or rewrite the 28 existing R/Quarto files. Detailed responsibilities remain in [`script-catalog.md`](script-catalog.md); this page records only the migration decision.

| Existing material | Classification | Phase 2 decision |
|---|---|---|
| `projects/01_zilongjin_network_pharmacology/` | PROJECT-SPECIFIC | KEEP; inputs are absent, so no reusable asset is claimed |
| `projects/02_gse255834_scrna_pipeline/` main scripts | PROJECT-SPECIFIC | KEEP; preserve the current object chain and hard-coded-path findings |
| GSE255834 recovery/QC patterns | POTENTIAL REUSABLE ASSET | REVIEW LATER after the Williams donor-aware QC candidate is tested on real data |
| `projects/02_gse255834_scrna_pipeline/` historical alternatives | REVIEW LATER | KEEP in place; source-object gaps and overlaps remain documented in its audit note |
| `projects/03_apap_mouse_liver_atlas/` main workflow | PROJECT-SPECIFIC | KEEP; do not restructure an active atlas workflow during this pilot |
| APAP annotation and cell-communication patterns | POTENTIAL REUSABLE ASSET | REVIEW LATER after a second real use and validation |
| APAP historical parallel branches and `99_legacy/` | REVIEW LATER / UNKNOWN | KEEP in place; their provenance is not sufficient for promotion or deletion |

No existing script is promoted into `library/` in Phase 2.
