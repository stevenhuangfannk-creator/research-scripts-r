# Phase 4A Validation Record

Date: 2026-09-28

## Scope

This record covers the executed PI/healthy scRNA-seq foundation only. Spatial reconstruction, advanced analysis modules and final figure matching remain gated on this validation.

## Evidence and counts

| Check | Observed result | Classification |
|---|---:|---|
| Released PI filtered H5 matrices | 8 files; 66,041 barcodes; archive MD5 verified | EXACTLY REPRODUCED STEP for the released archive |
| Supplementary Table 1 PI final total | 39,393 cells | PAPER-REPORTED METHOD / target |
| PI QC using selected 1,000–6,000 genes and ≤25% mitochondrial fraction | 40,055 cells | USER/CODEX ANALYTICAL CHOICE |
| Healthy GSE164241 GM matrices | 13 samples; 65,547 raw barcodes | EXACTLY REPRODUCED STEP for the selected public files |
| Healthy QC using source-paper thresholds | 55,049 cells | METHOD-BASED RECONSTRUCTION |
| Pre-doublet combined object | 95,104 cells; 21,934 genes; 21 samples; 20 donors | METHOD-BASED RECONSTRUCTION |
| SOLO raw hard calls | 24,792 flagged doublets | MODERNIZED IMPLEMENTATION; not used as final calls |
| Prior-corrected SOLO calls | 2,992 flagged doublets; 92,112 retained singlets | MODERNIZED IMPLEMENTATION / USER analytical choice |
| Paper reported integrated high-quality total | 90,551 cells | PAPER-REPORTED METHOD / comparison target |

The retained object is 1,561 cells larger than the paper-reported total. The paper does not provide the complete PI gene/count thresholds, exact doublet tool, intermediate object or all exclusion rules. The difference is therefore unresolved rather than evidence of a failed download.

## Preliminary integration

`results/phase4a/phase4a_preliminary_integrated.h5ad` contains a scVI latent representation, Leiden clusters and provisional marker-score labels. The base scVI model was trained on the pre-doublet object and the corrected singlets were projected into that model. This keeps the first pass reproducible and avoids silently changing the trained reference while calibrating SOLO, but a clean post-doublet retraining should be considered before final figure comparison.

The current object has 61 Leiden clusters and 14 broad marker-score classes. Low-margin clusters remain explicitly marked `low` in `annotation_confidence`; labels are not treated as ground truth. The preliminary UMAP is `figures/phase4a/figure1a_preliminary_umap.png` and `.pdf`.

## Validation limits and next gate

- No numeric exact-reproduction claim is made for the integrated cell total, cluster identities, abundance statistics or Figure 1 geometry.
- Donor D6 contributes two PI samples; downstream differential abundance must use donor-aware designs.
- The current object is sufficient to start a visual and marker audit, not sufficient to start SCENIC, CellOracle or final cell2location interpretation.
- Next scientific gate: review provisional labels and retrain or formally accept the post-doublet integration, then proceed to spatial input inventory (Phase 4B).
