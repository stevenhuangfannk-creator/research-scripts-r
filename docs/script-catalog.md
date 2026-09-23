# 脚本模块目录

本页记录 28 个原始代码文件的职责、流程位置和当前判断。所有“历史/可选”标记都表示尚未能与主对象链严格衔接，并不表示文件可以删除。

## 01 紫龙金网络药理学

| 模块 | 脚本 | 职责 | 主要输入 | 主要输出/状态 |
|---|---|---|---|---|
| 功能分析 | `6-9_analysis.qmd` | 药材组成、成分-靶点网络、PPI、CytoHubba、GO/KEGG、GSEA 与机制汇总 | 交集基因、药材-成分-靶点表、STRING 边、KEGG GMT、可选 MCC Top 20 | 综合 HTML 与 `results/` 表；缺输入，未运行 |

## 02 GSE255834 scRNA-seq

### 数据导入

| 脚本 | 职责 | 流程角色 |
|---|---|---|
| `build_GSE255834_seurat.R` | 读取 8 个 raw 10x H5，barcodeRanks cell calling，自适应 QC，合并、PCA、聚类和 UMAP | 主入口 |
| `finish_GSE255834_seurat_from_samples.R` | 从每样本缓存 RDS 恢复合并和降维 | 中断恢复；与主脚本后半段重复 |
| `summarize_barcoderanks.R` | 汇总每个 H5 的 knee/inflection | 输入诊断，可选 |

### 质量控制

| 脚本 | 职责 | 流程角色 |
|---|---|---|
| `add_scDblFinder_to_GSE255834.R` | 每样本运行 scDblFinder 并回写 doublet 标签 | 主链；读取的 `_object_joined.rds` 缺少生产步骤 |
| `strict_qc_umap_70_workers.R` | 按样本严格过滤 singlet，重新 PCA/聚类/UMAP | 主链 |
| `diagnose_qc_distributions.R` | 检查样本对象的 QC 分布 | 诊断 |
| `diagnose_qc_from_doublet.R` | 在 doublet 对象上检查 QC 分布 | 诊断 |
| `recompute_singlet_umap.R` | 从独立 singlet 对象重新计算 UMAP | 历史替代分支；输入没有生产者 |

### 去污染与注释

| 脚本 | 职责 | 流程角色 |
|---|---|---|
| `decontX_GSE255834.R` | 按样本运行 DecontX，合并校正计数并重新降维 | 主链 |
| `annotate_GSE255834_strict.R` | marker module score、cluster 决策、一级和二级注释 | 主链；输入可用环境变量选择 |

建议链：构建 → 补齐 JoinLayers/对象命名步骤 → scDblFinder → strict QC → DecontX → annotation。

## 03 APAP 小鼠肝脏图谱

### 数据导入、整合与聚类

| 脚本 | 职责 | 流程角色 |
|---|---|---|
| `build_seurat.R` | 从单一 UMI 矩阵和元数据建立 `APAP_merged_seurat.rds` | 历史/待确认；输出未被其他脚本引用 |
| `integrate_GSE280652_2022.qmd` | 整合 Ben-Moshe 2022 与 GSE280652，DoubletFinder、Harmony、聚类、UMAP | 当前主入口 |

### 细胞注释

| 脚本 | 职责 | 流程角色 |
|---|---|---|
| `mouse_liver_level1_annotation.qmd` | 肝脏一级大类注释并导出免疫子集 | 主链 |
| `mouse_liver_level2_immune_annotation.qmd` | Myeloid/Lymphoid 二级注释 | 主链 |
| `mouse_liver_final_object.qmd` | 记录一级和二级标签合并，验证最终对象 | 主链说明；实际合并代码不执行 |
| `mouse_liver_level3_macrophage_annotation.qmd` | KC/巨噬三级注释并回写最终对象 | 主链 |
| `mouse_liver_level3_T_annotation.qmd` | T/NK 三级注释并回写最终对象 | 主链 |
| `macrophage_annotation.qmd` | 旧拆分巨噬对象注释 | 历史平行分支 |
| `T_NK_annotation.qmd` | 旧拆分 T/NK 对象注释 | 历史平行分支 |

### 细胞通讯

| 脚本 | 职责 | 流程角色 |
|---|---|---|
| `mouse_liver_ccc_cellchat_cellphonedb.qmd` | 基于整合最终对象运行 CellChat 与 LIANA/MouseConsensus | 当前较完整入口 |
| `macrophage_TNK_cellchat.qmd` | 旧拆分巨噬 × T/NK 的 CellChat 双条件比较 | 历史平行分支 |
| `SPP1_vs_Others_cellchat.qmd` | SPP1⁺巨噬 vs 其他细胞的 CellChat | 历史平行分支 |
| `SPP1_vs_Others_cellphonedb.qmd` | 同一问题的 LIANA/MouseConsensus 分析 | 历史平行分支 |
| `macrophage_neutrophil_cellchat.qmd` | 巨噬 × 中性粒细胞通讯结果展示 | 报告型；只读取预计算对象 |

### 报告与历史代码

| 脚本 | 职责 | 流程角色 |
|---|---|---|
| `spp1_T_subsets_communication_report.qmd` | SPP1⁺巨噬与 T/NK 亚群的上下游通讯深度报告 | 读取预计算对象和 CSV |
| `upstream_signal_macrophage_T_subsets_report.qmd` | 巨噬与 T 亚群双向上游信号报告 | 读取预计算对象和 CSV |
| `all_r_code_extracted.R` | 从报告抽出的 4 个查询/汇总代码块 | 历史记录，与完整报告重叠 |

建议主链：数据整合 → 一级注释 → 免疫二级注释 → 恢复最终对象合并步骤 → 巨噬/T-NK 三级注释 → 整合对象通讯入口 → 专题报告。
