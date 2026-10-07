# 方法卡：探索性 cluster marker 分析

| 字段 | 内容 |
|---|---|
| 方法 ID | cell_markers |
| 分类 | 02_differential_analysis |
| 状态 | VALIDATED |
| 语言 | R |
| 包 | Seurat |
| 最近验证 | 2026-10-07 |

包版本见[构建环境记录](../../docs/validation/package_status.tsv)；安装过某个包不等于它能够正常加载，也不等于方法经过验证。

官方文档：https://satijalab.org/seurat/articles/pbmc3k_tutorial

原始论文：原始论文见官方文档所列引用；本次构建未独立核验论文元数据。

## 科研问题与用途

寻找细胞/cluster 的探索性 marker，供分群解释和注释证据整理。

## 适用条件与输入契约

含标准化 RNA 表达 data layer 的 Seurat 对象（RDS），元数据中存在 group_column 指定的分组列。

可选输入仅限工作流与配置实际支持的字段；候选方法的输入契约是规划规格，不能视为已实现功能。

## 实际调用与主要参数

将 DefaultAssay 设为 RNA，按 group_column 设置 Idents，再调用 Seurat::FindAllMarkers(test.use = "wilcox")。

group_column 起点为 seurat_clusters；only_positive: true 只报告正向 marker；min_pct = 0.1 与 logfc_threshold = 0.25 是筛选起点。检验固定为 wilcox。

参数值是起点，须结合物种、数据规模和样本设计审核。包广泛使用或参数有默认值，不意味着方法被提升为 DEFAULT。

## 假设、局限与常见误区

细胞级 P 值可能受伪重复影响。本输出不提供样本/供体层级处理组推断；marker 本身也不能单独证明细胞类型或处理效应。

优点是输入、参数和输出范围明确，便于复用与追溯；该小型工作流不覆盖完整科研分析流程。

## 替代路线与选择依据

要回答处理组 DEG，优先准备 sample × cell type pseudobulk，并使用匹配设计的 DESeq2/edgeR/limma；细胞级混合模型需有明确设计依据。

## 输出与图形

实际输出见[输出说明](OUTPUT_CATALOG.md)。需要画图时先查该输出说明，再查[全局图例](../../GALLERY.md)；没有已渲染预览的图不能当作已验证图形建议。

## 验证证据

验证数据：Seurat::pbmc_small。

PASS：在 pbmc_small 上验证探索性 cluster-marker 表；没有验证样本层级处理组推断。

运行和内存：小型演示不是性能基准，目标数据需记录耗时与线程设置；尽量保留稀疏计数，不要将整张图谱转为稠密矩阵。大型对象的内存消耗尚未基准测试。

## 脚本与参考

脚本：[workflow.R](scripts/workflow.R)（02_differential_analysis/differential_expression/scripts/workflow.R）。运行命令与配置说明见 [README](README.md)。

参考：https://satijalab.org/seurat/articles/pbmc3k_tutorial
