# Phase 4A targeted myeloid and plasma/B annotation audit

Date: 2026-09-30. This is a method-based reconstruction and a USER/CODEX
analytical choice, not a recovered author annotation. The source count matrices
and the validated Leiden 47 epithelial correction were not changed.

## Scope and sources

- Source labels: `results/phase4b/cell2location_input/scrna_reference_counts_curated_v1.h5ad` (92,112 cells, 17,211 shared genes).
- Full-gene count/QC source: `results/phase4a/phase4a_preliminary_integrated.h5ad` (21,934 genes). The shared-gene reference excludes all mitochondrial and ribosomal genes; Ig/ribosomal/mitochondrial count fractions were therefore calculated from the full-gene count layer.
- No whole-data reclustering. A local 20,157-cell subset included existing macrophage, monocyte, dendritic, B and plasma labels. It used 2,500 HVGs, 30 PCs, 20 neighbors, Leiden resolution 0.6 and seed 20260928. Batch-aware HVG selection failed because the LOESS fit was singular; the local diagnostic used unstratified HVGs. The graph has five connected components, so distances between disconnected UMAP islands have no biological interpretation.
- Reproduce: `scripts/18_audit_myeloid_plasma.py`, then `scripts/19_myeloid_plasma_neighborhood.py`, then `scripts/20_curate_myeloid_plasma_labels.py` in the existing `.venv-gpu` environment. These scripts write versioned derivative tables and figures; they do not write into either source H5AD.

## Original macrophage label

The 1,885 original macrophage-labelled cells came from Leiden 12 (1,039), 7
(298), 22 (203), 36 (202), 44 (54), 54 (54) and 35 (35). IGT3 contributed
1,531/1,885 (81.2%). IGT3 contained 10,862 of all 92,112 cells, so the
original macrophage-label rate was 14.1% within IGT3 versus 0.44% outside it.
Cell-level sample, donor, Leiden, UMI, detected genes, mitochondrial fraction,
SOLO doublet score, confidence and provenance are in `macrophage_cells.tsv.gz`.
The requested contingency tables are in `macrophage_by_leiden.tsv`,
`macrophage_by_sample.tsv`, `macrophage_by_igt_group.tsv`,
`macrophage_by_confidence.tsv` and `macrophage_leiden_by_sample.tsv`.

The IGT3-labelled macrophage cells had median full-gene Ig count fraction 0.163,
versus 0.002 outside IGT3; median UMI 3,582 versus 2,957; detected genes
1,499 versus 1,432; and SOLO doublet probability 0.0077 versus 0.0090.
IGH/IGK/IGL enrichment was not a sample-wide finding in IGT3 B cells or
monocytes. Original macrophage cluster 12 co-detected MZB1 and COL1A1 in
77% of cells, and MZB1 and PTPRC in 70%. Cluster 7 showed analogous plasma
and stromal co-detection. These data support a mixed/incorrect broad label;
they do not by themselves prove whether individual cells are doublets, ambient
RNA affected, true hybrid states or another sample-specific effect. Low SOLO
scores do not rule out doublets. IGT3 enrichment alone was not used for deletion.

Marker-level evidence contradicts a single macrophage identity for the old
label. Leiden 12 has high MZB1/JCHAIN/IGKC/IGHG1 and COL1A1 but weak C1QA,
CD68 and LST1; Leiden 7 is similarly stromal/plasma-like. Leiden 22 expresses
DCT/PMEL/TYRP1/MLANA/TYR (melanocyte-like); Leiden 54 is epithelial-like;
Leiden 36/35 has CTSK/ACP5/MMP9 and Ig; Leiden 44 has stromal/pericyte
features. The old cell2location macrophage signature ranked IGKC third,
IGKV4-1 fifth and IGHG1 sixth, while C1QA/B/C and CD68 were all below rank
2,500. Marker means, detected fractions and per-Leiden top markers are in the
audit result directory. Dot plots, a cluster-average heatmap, marker and QC
violin plots, and local UMAPs are in `figures/phase4a/myeloid_plasma_audit/`.

## Local neighborhood and evidence-based annotation

Local Leiden 5 contains 1,423 cells, including 1,417 originally labelled
Monocytes in whole-data Leiden 25. The latter 1,417 cells show a coherent
C1QA/B/C, CD68, LST1, TYROBP, FCER1G, CTSS, MS4A7, CCL18 and APOE program,
with low MZB1/JCHAIN/IGKC and COL1A1. Median Ig count fraction is 0.001 and
median SOLO probability is 0.003. They occur across PI samples (IGT3 554,
IGT4 463, IGT5 165, IGT8 134, IGT7 71 and smaller counts elsewhere).
This is sufficient for a provisional macrophage label, although the PI-heavy
sample composition may limit transfer to healthy tissue. IGT3 contributes
554/1,417 (39.1%) of the revised macrophage population, down from 81.2% of
the invalid old label; 1,704 of the 2,138 unresolved cells are from IGT3.
Nearby local Leiden
11 includes other whole-data Leiden 25 monocytes with partial C1Q and
FCER1A/CLEC10A; it was left as Monocytes rather than forcing a split.

The versioned `curated_v2_annotations.tsv.gz` makes only these changes:

| Prior label/source | New label | Cells | Reason |
|---|---|---:|---|
| Macrophages, original seven Leiden clusters | Unresolved | 1,885 | Incompatible plasma/stromal/myeloid/melanocyte/epithelial programs; no defensible single lineage |
| Monocytes, Leiden 27 | Unresolved | 253 | CTSK/ACP5/MMP9 osteoclast-like, preliminary low-confidence label |
| Monocytes, Leiden 25 and local Leiden 5 | Macrophages | 1,417 | Multiple concordant myeloid markers, low Ig/stromal signal, several PI samples |

The 2,138 `Unresolved` cells remain in the annotation ledger and source data;
they are excluded only from the new cell2location fit. The revised reference
has 89,974 cells and 14 broad cell types. It keeps the 702 Leiden 47 epithelial
cells and 270 verified neutrophils as previously corrected. The exact
cell-level before/after labels, sample and cluster are in
`curated_v2_cell_changes.tsv.gz`; aggregated decisions are in
`curated_v2_change_by_cluster_sample.tsv`. These are reconstruction choices,
not proof of a unique biological identity for unresolved cells.

## Reference rebuilding and gate

Phase 4B-2 input preparation was rerun with `--curated-v2`, writing to
`results/phase4b/cell2location_input/curated_v2/` without overwriting v1.
The new scRNA matrix contains 89,974 cells by the same 17,211 shared genes;
the nine spatial sample derivatives retained their sample identities and
unchanged spot counts. The new reference fit uses seed 20260928, 250 epochs,
batch size 2,500 and the separate GPU environment. The fit and biological and
numerical QC passed; exact before/after signature comparisons and limitations
are in `notes/PHASE4B_CELL2LOCATION_REFERENCE.md`. No Phase 4B-4 spatial
mapping was started under this audit request.

## Remaining uncertainty

The mechanism behind the old IGT3 mixed expression is unresolved: an incorrect
cluster-level label is clear, whereas ambient Ig, doublets, tissue mixing and
true coexpression cannot be distinguished conclusively here. Some myeloid
states may remain grouped under broad Monocytes or excluded as Unresolved.
Per-cell marker co-detection and SOLO are diagnostic but are not definitive
doublet or ambient-RNA tests. If downstream analysis requires those cells,
additional targeted validation should precede any relabelling.
