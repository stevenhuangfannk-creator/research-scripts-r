# Phase 4B-4 independent spatial mapping status

Date: 2026-09-30. **PARTIAL / BLOCKED.** PI formal model and posterior completed;
PI global QC failed its predeclared depth gate. Healthy has not been fitted.
This is method reconstruction with documented analytical choices, not author code.

## Reference and input gate

Reference commit: `8496f3a4ea4c75eb35b269995e9e3a6e91f12925`; curated-v2,
89,974 cells / 14 types. Signature SHA256:
`9b244c33c045f47f2b9f5d63dee4a982eedcd6d150655b3684cfad23b39cb148`.
All nine inputs passed exact 17,211-gene order, uniqueness, integer counts,
sample/barcode and tissue coordinate checks. No old model/signature was used.
Unresolved was excluded as a mapping factor. Raw data and annotation are unchanged.

| Sample | Tissue spots | Median original counts | Mapping status |
|---|---:|---:|---|
| PI | 640 | 34,769 | Formal fit/posterior complete; global QC blocked |
| A1 | 231 | 236 | NOT RUN: PI gate failed |
| B1 | 284 | 286 | NOT RUN: PI gate failed |
| C1 | 295 | 636 | NOT RUN: PI gate failed |
| D1 | 319 | 300 | NOT RUN: PI gate failed |
| A2 | 1,088 | 4,539 | NOT RUN: PI gate failed |
| B2 | 415 | 23,197 | NOT RUN: PI gate failed |
| C2 | 160 | 35,348 | NOT RUN: PI gate failed |
| D2 | 501 | 5,038 | NOT RUN: PI gate failed |

Samples were never merged into a single dataset. Their IDs, condition, source,
depth group and original spatial/QC metadata are preserved in independent inputs.
Depth differences already prohibit direct cross-sample raw abundance comparison.
There is no PI-versus-Healthy mapping comparison or disease-effect inference yet.

## PI per-type internal reliability

The labels below are predeclared **internal marker-diagnostic categories**, not
final scientific acceptance. Every type remains blocked for downstream analysis
by global PI QC. All Healthy transfer/domain-shift assessments are NOT ASSESSED.
Correlations use normalized marker modules and abundance fractions; residual
correlations are descriptive adjustments for counts and detected genes.

| Cell type | Internal category | Abundance/module rho | Fraction/module rho | Depth-adjusted abundance/module rho |
|---|---|---:|---:|---:|
| B cells | reliable | 0.729 | 0.651 | 0.678 |
| Dendritic cells | partially reliable | 0.335 | 0.097 | 0.059 |
| Epithelial cells | reliable | 0.867 | 0.684 | 0.867 |
| Fibroblasts | reliable | 0.416 | 0.920 | 0.771 |
| Lymphatic endothelium | reliable | 0.620 | 0.421 | 0.538 |
| Macrophages | reliable | 0.482 | 0.359 | 0.219 |
| Mast cells | reliable | 0.626 | 0.573 | 0.566 |
| Monocytes | partially reliable | 0.187 | 0.347 | 0.143 |
| NK cells | partially reliable | 0.481 | 0.143 | 0.323 |
| Neutrophils | partially reliable | 0.109 | 0.246 | 0.162 |
| Plasma cells | partially reliable | 0.561 | 0.104 | 0.252 |
| Smooth muscle/pericytes | reliable | 0.519 | 0.711 | 0.663 |
| T cells | reliable | 0.639 | 0.659 | 0.580 |
| Vascular endothelium | reliable | 0.463 | 0.550 | 0.560 |

Macrophage's internal category requires caution: abundance/depth rho 0.922,
Macrophage/Monocyte abundance rho 0.919 and reference similarity rho 0.917.
Canonical macrophage gene correlations are positive, but specific attribution
and absolute density remain uncertain. Healthy macrophage domain shift cannot
be decided from PI alone. Neutrophil intervals are broad; plasma composition
concordance is weak despite narrow fitted intervals. Dendritic marker association
largely disappears after descriptive depth adjustment.

## Blocking diagnosis and next step

All numerical training/posterior gates passed. Total abundance/counts rho 0.981
and abundance/detected-genes rho 0.958 failed the depth gate. Median/max total
abundance is 30.52/233.39; no NaN, negative abundance or reversed quantile.
The model attributes substantial depth variation to abundance; this may mix
true density/RNA content with technical depth. Correlation alone does not identify
the cause. `N_cells_per_location=30` was not calibrated against gingival nuclei.

Before proceeding, diagnose PI-only nuclei density and prior/detection sensitivity
in separate outputs; establish whether composition/localization is robust without
relaxing the threshold merely to pass. No evidence currently mandates new
annotation changes or reference retraining. Healthy migration remains untested.
No cell type is approved for NMF/COMMOT while PI QC is blocked.

Detailed parameters, provenance, quantitative diagnosis and output inventory:
`notes/PHASE4B_CELL2LOCATION_PI_MAPPING.md`. Scripts: `21_map_cell2location.py`,
`22_qc_cell2location_mapping.py`, `23_diagnose_pi_mapping_depth.py`.
Models/results/figures remain local and Git-ignored. No git push.
