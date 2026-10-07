# 单细胞 RNA-seq 基础流程（01_scrna_core）

本目录整理从原始计数到细胞注释的常用步骤：counts → QC → 标准化 → 按设计评估批次整合 → 聚类 → 有证据的细胞注释。

先读[方法索引](../METHOD_INDEX.md)、[图例](../GALLERY.md)与[注册表说明](../registry/README.md)。方法目录存在不等于已实现或已验证；当前没有分析方法被提升为 DEFAULT。

| 要做什么 | 入口 | 当前边界 |
|---|---|---|
| 由 counts 和元数据建对象 | [seurat_ingestion](data_ingestion/README.md) | PASS 仅验证对齐与 counts 保留 |
| QC 审计与显式过滤 | [scrna_qc](quality_control/README.md) | 默认 thresholds/基因模式为占位，需自行填写 |
| doublet 标记 | [scdblfinder](doublet_detection/scDblFinder/README.md) | BLOCKED；当前仅标记，不自动删除 |
| ambient RNA 校正 | [decontx](ambient_rna/DecontX/README.md)、[soupx](ambient_rna/SoupX/README.md) | DecontX 为 BLOCKED；SoupX 无可执行工作流 |
| 标准化 | [lognormalize](normalization/lognormalize/README.md)、[sctransform](normalization/SCTransform/README.md) | LogNormalize 有有限 PASS；SCTransform 为 UNVALIDATED |
| 技术批次整合 | [harmony](batch_integration/Harmony/README.md)、[seurat_integration](batch_integration/Seurat/README.md) | 均未验证；须区分技术批次与真实生物差异 |
| 降维与聚类 | [seurat_clustering](clustering/README.md) | 脚本固定重算并使用 pca，不自动使用 Harmony |
| 审核后标签写回 | [hierarchical_annotation](annotation/README.md) | PASS 仅验证映射写回；不自动判断细胞类型 |

常用起点是建对象 → QC → LogNormalize → 聚类 → marker 审阅 → 注释。doublet、去污染和批次整合的位置应由输入条件与样本设计决定，不能机械串联全部目录。Harmony 需要先有 PCA，而本目录的聚类脚本不会读取 Harmony reduction，请先阅读具体方法说明。

每个方法的 README 说明包在脚本中如何调用、输入要求、配置字段、运行命令和结果文件。运行统一从仓库根目录执行，使用实际输入与独立输出目录。
