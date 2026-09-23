# APAP 小鼠肝脏单细胞图谱与细胞通讯

## 研究目的

整合 Ben-Moshe et al. 2022（PMID 35659879）与 De Ponti et al. 2025（GSE280652）的 Control/APAP 24 h 小鼠肝脏 scRNA-seq，完成大类、免疫、巨噬和 T/NK 注释，并分析 SPP1⁺巨噬细胞与其他细胞的通讯。

## 模块结构

```text
modules/
├── 01_data_ingestion/          # 未接入主链的早期对象构建脚本
├── 02_integration_clustering/  # 两数据集整合、DoubletFinder、Harmony、聚类、UMAP
├── 03_annotation/              # 一级、二级、三级注释及旧拆分对象分支
├── 04_cell_communication/      # CellChat、LIANA/CellPhoneDB
├── 05_reports/                 # 读取预计算结果的专题报告
└── 99_legacy/                  # 报告中提取的历史代码块
```

## 当前主流程

1. `02_integration_clustering/integrate_GSE280652_2022.qmd`
2. `03_annotation/mouse_liver_level1_annotation.qmd`
3. `03_annotation/mouse_liver_level2_immune_annotation.qmd`
4. 恢复 `mouse_liver_final_object.qmd` 中被标为不执行的最终对象合并步骤
5. `03_annotation/mouse_liver_level3_macrophage_annotation.qmd`
6. `03_annotation/mouse_liver_level3_T_annotation.qmd`
7. `04_cell_communication/mouse_liver_ccc_cellchat_cellphonedb.qmd`
8. 根据需要运行 `05_reports/` 的两个专题报告

`macrophage_annotation.qmd`、`T_NK_annotation.qmd`、`macrophage_TNK_cellchat.qmd` 和 `SPP1_vs_Others_*` 使用旧拆分对象，属于历史平行分支。

## 数据来源

- `whole_atlas_control_24h_seurat.rds`：Ben-Moshe 2022 对象。
- `data/GSE280652/`：GSM8603014–GSM8603017 的 4 个 H5。
- 下游需要多个 `integrated_*.rds` 和预计算 CellChat 目录，原目录均未提供。

两数据集采样方式不同（全肝与分选），细胞比例不应直接跨数据集比较。

## 依赖与状态

主要依赖：`Seurat`, `SeuratObject`, `Matrix`, `data.table`, `dplyr`, `ggplot2`, `patchwork`, `harmony`, `DoubletFinder`, `CellChat`, `liana`, `circlize`, `cowplot`, `ggh4x`, `ggrepel`, `RColorBrewer`, `magrittr`, `knitr`, `kableExtra`。

CellChat 文档注明使用 1.6.1，并含 igraph 2.x 兼容修复。当前缺少数据、对象、R/Quarto 和 `renv.lock`，没有运行验证。关键对象链和重复关系见 `Notes/workflow-audit.md`。
