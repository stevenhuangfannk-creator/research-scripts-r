# 按科研问题选择方法 / Choose a method

先看本页，再查找包。“起始路线”表示可以优先了解的分析方向，不等于已晋升为 `DEFAULT`。V1 尚无分析流程达到默认级别；运行前请查看[方法登记表](registry/methods.yml)的执行证据及数据适配要求。

`METHOD_CARD.md` 是方法卡；同目录 `README.md` 是中文用法，`OUTPUT_CATALOG.md` 解释输出。首次运行见[中文使用指南](docs/USAGE_ZH_CN.md)。

| 科研问题 | 起始路线／方法入口 | 替代方法 | 进阶方法 | 实验性方法 | 语言 | 登记状态 |
|---|---|---|---|---|---|---|
| 构建单细胞对象 | [seurat_ingestion](01_scrna_core/data_ingestion/METHOD_CARD.md) | Scanpy | — | — | R | VALIDATED |
| 单细胞质量控制 | [scrna_qc](01_scrna_core/quality_control/METHOD_CARD.md) | scater | — | — | R | VALIDATED |
| 双细胞识别 | [scdblfinder](01_scrna_core/doublet_detection/scDblFinder/METHOD_CARD.md) | DoubletFinder | — | — | R | CANDIDATE |
| 环境 RNA 去污染 | [decontx](01_scrna_core/ambient_rna/DecontX/METHOD_CARD.md) | [soupx](01_scrna_core/ambient_rna/SoupX/METHOD_CARD.md) | — | — | R | CANDIDATE |
| 标准化 | [lognormalize](01_scrna_core/normalization/lognormalize/METHOD_CARD.md) | [sctransform](01_scrna_core/normalization/SCTransform/METHOD_CARD.md) | — | — | R | VALIDATED |
| 批次整合 | [harmony](01_scrna_core/batch_integration/Harmony/METHOD_CARD.md) | [seurat_integration](01_scrna_core/batch_integration/Seurat/METHOD_CARD.md) | — | [foundation_models](09_python_bridge/foundation_models/METHOD_CARD.md) | R | CANDIDATE |
| 降维／聚类 | [seurat_clustering](01_scrna_core/clustering/METHOD_CARD.md) | [scanpy](09_python_bridge/Scanpy/METHOD_CARD.md) | — | — | R / Python | VALIDATED |
| 细胞一级／二级／三级注释 | [hierarchical_annotation](01_scrna_core/annotation/METHOD_CARD.md) | SingleR／Azimuth（未实现） | — | — | R | VALIDATED |
| 探索性 cluster marker | [cell_markers](02_differential_analysis/differential_expression/METHOD_CARD.md) | — | — | — | R | VALIDATED |
| 有生物学重复的条件差异表达 | [pseudobulk](02_differential_analysis/pseudobulk/METHOD_CARD.md) + [bulk_deseq2](07_bulk_clinical_ml/bulk_RNAseq/METHOD_CARD.md) | [limma](07_bulk_clinical_ml/bulk_RNAseq/limma/METHOD_CARD.md) | — | — | R | CANDIDATE；查看具体方法卡 |
| 细胞组成变化／差异丰度 | 先确定样本级设计，暂无默认方法 | [differential_abundance](02_differential_analysis/differential_abundance/METHOD_CARD.md) | — | — | R / Python | CANDIDATE；查看具体方法卡 |
| 拟时序／轨迹 | [monocle3](03_cell_dynamics/monocle3/METHOD_CARD.md) | [slingshot](03_cell_dynamics/slingshot/METHOD_CARD.md) | [tradeseq](03_cell_dynamics/tradeSeq/METHOD_CARD.md) | — | R | CANDIDATE |
| RNA velocity（RNA 速率） | 暂无默认方法 | [scvelo](09_python_bridge/scVelo/METHOD_CARD.md) | — | — | Python | 查看方法卡中的 CANDIDATE／EXPERIMENTAL 状态 |
| 细胞命运 | 暂无默认方法 | [cellrank](09_python_bridge/CellRank/METHOD_CARD.md) | — | — | Python | 查看方法卡中的 CANDIDATE／EXPERIMENTAL 状态 |
| 细胞通讯 | [cellchat](04_cell_communication/CellChat/METHOD_CARD.md) | [cellphonedb](09_python_bridge/CellPhoneDB/METHOD_CARD.md) | [liana_plus](04_cell_communication/LIANA/METHOD_CARD.md) | — | R / Python | CANDIDATE |
| 配体到靶基因响应 | [nichenet](04_cell_communication/NicheNet/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| GO／KEGG 过度富集分析（ORA） | [go_kegg_ora](05_pathway_function/GO_KEGG/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| 排序基因列表的通路富集 | [fgsea](05_pathway_function/GSEA/METHOD_CARD.md) | clusterProfiler GSEA（未实现） | — | — | R | CANDIDATE |
| 样本级通路活性 | [gsva_ssgsea](05_pathway_function/GSVA_ssGSEA/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| 细胞级通路活性 | [ucell_aucell](05_pathway_function/UCell_AUCell/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| PPI／枢纽基因拓扑 | [ppi](06_gene_networks/PPI/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| 共表达网络 | [wgcna](06_gene_networks/WGCNA/METHOD_CARD.md) | [hdwgcna](06_gene_networks/hdWGCNA/METHOD_CARD.md) | — | — | R | CANDIDATE |
| 转录调控子（regulon） | [scenic](06_gene_networks/SCENIC/METHOD_CARD.md) | — | — | — | R / Python | CANDIDATE |
| 生存／Kaplan–Meier | [survival_km](07_bulk_clinical_ml/survival/METHOD_CARD.md) | — | [cox](07_bulk_clinical_ml/Cox/METHOD_CARD.md) | — | R | VALIDATED |
| 单因素／多因素 Cox | [cox](07_bulk_clinical_ml/Cox/METHOD_CARD.md) | [lasso_cox](07_bulk_clinical_ml/LASSO_Cox/METHOD_CARD.md) | — | — | R | VALIDATED |
| LASSO | [lasso](07_bulk_clinical_ml/LASSO/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| 随机森林 | [random_forest](07_bulk_clinical_ml/random_forest/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| ROC／时间依赖 ROC | [roc](07_bulk_clinical_ml/machine_learning/ROC/METHOD_CARD.md) | — | — | — | R | CANDIDATE |
| Pearson／Spearman 相关性 | [correlation](07_bulk_clinical_ml/correlation/METHOD_CARD.md) | 控制混杂时考虑回归 | — | — | R | VALIDATED |

实际运行分三种情况：`script` 有路径且 `validated: true`，可按已验证范围尝试；有路径但 `validated: false`，阅读限制并确认适配后才使用 `--allow-unvalidated`；`script: null`，当前没有可运行封装。

绘图：[画廊](GALLERY.md) → Plot ID → [图形登记表](registry/plots.yml)。颜色：[配色索引](PALETTE_INDEX.md)。
