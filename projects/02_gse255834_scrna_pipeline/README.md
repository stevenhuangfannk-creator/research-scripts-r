# GSE255834 单细胞分析流程

## 研究目的

处理 GSE255834 的 8 个 10x Genomics raw H5。代码从文件名解析 Control/APAP、48/72 小时和 hepatocyte/NPC，目标是完成细胞识别、QC、双细胞检测、环境 RNA 去污染、降维聚类和细胞注释。

## 模块结构

```text
modules/
├── 01_data_ingestion/       # H5 读取、barcode calling、对象构建、断点恢复
├── 02_quality_control/      # scDblFinder、严格 QC、诊断、UMAP 替代分支
├── 03_decontamination/      # DecontX
└── 04_annotation/           # marker score 与分层细胞注释
```

## 建议主流程

1. `01_data_ingestion/build_GSE255834_seurat.R`
2. 补齐 `GSE255834_seurat_object.rds` 到 `GSE255834_seurat_object_joined.rds` 的明确步骤
3. `02_quality_control/add_scDblFinder_to_GSE255834.R`
4. `02_quality_control/strict_qc_umap_70_workers.R`
5. `03_decontamination/decontX_GSE255834.R`
6. `04_annotation/annotate_GSE255834_strict.R`

辅助脚本：

- `finish_GSE255834_seurat_from_samples.R` 用于从每样本缓存恢复。
- `summarize_barcoderanks.R`、两个 `diagnose_qc_*` 用于诊断。
- `recompute_singlet_umap.R` 是输入来源不明的旧替代分支。

## 数据与输出

输入是 GSE255834 的 8 个 `*_raw_feature_bc_matrix.h5`。原目录没有原始数据、结果、样本说明或下载记录，因此未创建空目录。

建议后续把输入放在 `Data/`，输出放在 `Results/`。在完成路径重构前，现有脚本仍指向 `C:/Users/zhaozize/Desktop/APAP`。

## 依赖与状态

主要 R 包：`Seurat`, `Matrix`, `DropletUtils`, `SingleCellExperiment`, `scDblFinder`, `BiocParallel`, `future`, `future.apply`, `data.table`, `ggplot2`, `patchwork`, `celda`, `uwot`, `SummarizedExperiment`。

当前不能认定为开箱即用：缺少数据和 R 环境，硬编码路径尚未参数化，两个中间对象缺少生产步骤。详细问题见 `Notes/pipeline-audit.md`。
