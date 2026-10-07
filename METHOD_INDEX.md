# Choose a method by research question

**Read this index before package search.** The Default column describes the preferred starting *route*, not a DEFAULT promotion. Check registry execution evidence and data suitability before running. No analysis workflow has yet earned DEFAULT in V1.

| Research question | Default / starting route | Alternative | Advanced | Experimental | Language | Status |
|---|---|---|---|---|---|---|
| Object creation | [seurat_ingestion](01_scrna_core/data_ingestion/METHOD_CARD.md) | Scanpy | — | — | R | VALIDATED |
| scRNA QC | [scrna_qc](01_scrna_core/quality_control/METHOD_CARD.md) | scater | — | — | R | VALIDATED |
| Doublet detection | [scdblfinder](01_scrna_core/doublet_detection/scDblFinder/METHOD_CARD.md) | DoubletFinder | — | — | R | CANDIDATE |
| Ambient RNA | [decontx](01_scrna_core/ambient_rna/DecontX/METHOD_CARD.md) | [soupx](01_scrna_core/ambient_rna/SoupX/METHOD_CARD.md) | — | — | R | CANDIDATE |
| Normalization | [lognormalize](01_scrna_core/normalization/lognormalize/METHOD_CARD.md) | [sctransform](01_scrna_core/normalization/SCTransform/METHOD_CARD.md) | — | — | R | VALIDATED |
| Batch integration | [harmony](01_scrna_core/batch_integration/Harmony/METHOD_CARD.md) | [seurat_integration](01_scrna_core/batch_integration/Seurat/METHOD_CARD.md) | — | [foundation_models](09_python_bridge/foundation_models/METHOD_CARD.md) | R | CANDIDATE |
| Dimensionality reduction / clustering | [seurat_clustering](01_scrna_core/clustering/METHOD_CARD.md) | [scanpy](09_python_bridge/Scanpy/METHOD_CARD.md) | — | — | R / Python | VALIDATED |
| Cell annotation (L1/L2/L3) | [hierarchical_annotation](01_scrna_core/annotation/METHOD_CARD.md) | SingleR / Azimuth (not implemented) | — | — | R | VALIDATED |
| Exploratory cluster DEG | [cell_markers](02_differential_analysis/differential_expression/METHOD_CARD.md) | — | — | — | R | VALIDATED |
| Replicate-aware condition DEG | pseudobulk + bulk_deseq2 | [limma](07_bulk_clinical_ml/bulk_RNAseq/limma/METHOD_CARD.md) | — | — | R | CANDIDATE / check component cards |
| Composition change / differential abundance | No default; sample-level design first | [differential_abundance](02_differential_analysis/differential_abundance/METHOD_CARD.md) | — | — | R / Python | CANDIDATE / check component cards |
| Pseudotime / trajectory | [monocle3](03_cell_dynamics/monocle3/METHOD_CARD.md) | [slingshot](03_cell_dynamics/slingshot/METHOD_CARD.md) | [tradeseq](03_cell_dynamics/tradeSeq/METHOD_CARD.md) | — | R | CANDIDATE |
| RNA velocity | No default | [scvelo](09_python_bridge/scVelo/METHOD_CARD.md) | — | — | Python | CANDIDATE / check component cards |
| Cell fate | No default | [cellrank](09_python_bridge/CellRank/METHOD_CARD.md) | — | — | Python | CANDIDATE / check component cards |
| Cell communication | [cellchat](04_cell_communication/CellChat/METHOD_CARD.md) | [cellphonedb](09_python_bridge/CellPhoneDB/METHOD_CARD.md) | [liana_plus](04_cell_communication/LIANA/METHOD_CARD.md) | — | R / Python | CANDIDATE |
| Ligand → target response | [nichenet](04_cell_communication/NicheNet/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| Pathway ORA (GO/KEGG) | [go_kegg_ora](05_pathway_function/GO_KEGG/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| Ranked pathway enrichment | [fgsea](05_pathway_function/GSEA/METHOD_CARD.md) | clusterProfiler GSEA (not implemented) | — | — | R | CANDIDATE |
| Sample-level pathway activity | [gsva_ssgsea](05_pathway_function/GSVA_ssGSEA/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| Cell-level pathway activity | [ucell_aucell](05_pathway_function/UCell_AUCell/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| PPI / hub topology | [ppi](06_gene_networks/PPI/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| Coexpression | [wgcna](06_gene_networks/WGCNA/METHOD_CARD.md) | [hdwgcna](06_gene_networks/hdWGCNA/METHOD_CARD.md) | — | — | R | CANDIDATE |
| Regulon | [scenic](06_gene_networks/SCENIC/METHOD_CARD.md) | — | — | — | R / Python | CANDIDATE |
| Survival / Kaplan–Meier | [survival_km](07_bulk_clinical_ml/survival/METHOD_CARD.md) | — | [cox](07_bulk_clinical_ml/Cox/METHOD_CARD.md) | — | R | VALIDATED |
| Univariate / multivariate Cox | [cox](07_bulk_clinical_ml/Cox/METHOD_CARD.md) | [lasso_cox](07_bulk_clinical_ml/LASSO_Cox/METHOD_CARD.md) | — | — | R | VALIDATED |
| LASSO | [lasso](07_bulk_clinical_ml/LASSO/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| Random forest | [random_forest](07_bulk_clinical_ml/random_forest/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| ROC / time-dependent ROC | [roc](07_bulk_clinical_ml/machine_learning/ROC/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| Pearson / Spearman association | [correlation](07_bulk_clinical_ml/correlation/METHOD_CARD.md) | regression for confounders | — | — | R | VALIDATED |

For plotting: [GALLERY](GALLERY.md) → Plot ID → [registry/plots.yml](registry/plots.yml). For colors: [PALETTE_INDEX](PALETTE_INDEX.md).
