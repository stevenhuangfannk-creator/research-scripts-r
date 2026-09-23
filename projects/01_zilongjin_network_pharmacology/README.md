# 紫龙金片网络药理学

## 研究目的

研究紫龙金片 8 味药材与结直肠癌肝转移（CRLM）候选靶点的关系。现有流程覆盖药材成分靶点网络、PPI、CytoHubba、GO/KEGG、药材-成分-靶点-通路网络和基于 PPI 连接度的 GSEA。

## 模块

```text
modules/
└── 06_functional_analysis/
    └── 6-9_analysis.qmd
```

这份 qmd 是一条顺序完整的综合分析，继续拆分会增加对象传递和运行状态管理，因此当前按“功能分析模块”整体保留。

## 必要输入

项目根目录需要：

- `input/IntersectionGenes.csv`
- `input/herb_compound_target_intersection.csv`
- `input/string_interactions_short.tsv`
- `input/kegg_human_full.gmt`
- 可选 `MCCtop20.csv`（Cytoscape/CytoHubba 输出）

原目录没有这些文件，来源和许可需在补入时记录。

## 运行

从本项目目录执行：

```powershell
quarto render modules/06_functional_analysis/6-9_analysis.qmd
```

文档内部顺序：输入标准化 → 中药组成 → 药材/成分/靶点网络 → PPI/Cytoscape → CytoHubba → GO/KEGG → 四维网络 → GSEA → 机制总结。

主要结果写入项目根目录的 `results/`。

## 依赖与状态

需要 R、Quarto、Cytoscape/CytoHubba，以及 `TCMNP`, `ggplot2`, `dplyr`, `tidyr`, `data.table`, `openxlsx`, `knitr`, `igraph`, `ggraph`, `clusterProfiler`, `org.Hs.eg.db`, `enrichplot`。

当前缺少输入、R/Quarto 和版本锁文件，尚未执行验证。报告中的药材剂量、候选靶点数量和机制文字需在补入真实输入后再次核对。
