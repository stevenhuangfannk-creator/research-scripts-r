# 方法卡：按样本与细胞类型汇总原始计数

| 字段 | 内容 |
|---|---|
| 方法 ID | pseudobulk |
| 分类 | 02_differential_analysis |
| 状态 | VALIDATED |
| 语言 | R |
| 包 | Seurat |
| 最近验证 | 2026-10-07 |

包版本见[构建环境记录](../../docs/validation/package_status.tsv)；安装过某个包不等于它能够正常加载，也不等于方法经过验证。

官方文档：https://satijalab.org/seurat/reference/aggregateexpression

原始论文：原始论文见官方文档所列引用；本次构建未独立核验论文元数据。

## 科研问题与用途

按生物学样本 × 细胞类型对 RNA 原始 counts 求和，为样本层级分析准备矩阵。

## 适用条件与输入契约

含 RNA raw counts 的 Seurat 对象（RDS），元数据中有 sample_column 指定的真实生物学样本列，以及 celltype_column 指定的审核后细胞类型列。

可选输入仅限工作流与配置实际支持的字段；候选方法的输入契约是规划规格，不能视为已实现功能。

## 实际调用与主要参数

Seurat::AggregateExpression(assays = "RNA", return.seurat = FALSE, group.by = c(sample_column, celltype_column)) 返回汇总 count 矩阵；Matrix::colSums() 计算各汇总组文库大小。

sample_column 与 celltype_column 必须替换为真实元数据列名，不是说明性的“biological sample”/“reviewed annotation”占位值。

参数值是起点，须结合物种、数据规模和样本设计审核。包广泛使用或参数有默认值，不意味着方法被提升为 DEFAULT。

## 假设、局限与常见误区

汇总不等于 DEG 检验，细胞不能充当独立生物学重复。须另保留 condition/covariate 样本表、足够独立 donor，并在需要时考虑配对/个体内设计。输出列名是组合分组名，脚本不另生成样本设计表。

优点是输入、参数和输出范围明确，便于复用与追溯；该小型工作流不覆盖完整科研分析流程。

## 替代路线与选择依据

组间效应检验可用 DESeq2/edgeR/limma-voom；只有设计依据充分时才用细胞级混合模型。

## 输出与图形

实际输出见[输出说明](OUTPUT_CATALOG.md)。需要画图时先查该输出说明，再查[全局图例](../../GALLERY.md)；没有已渲染预览的图不能当作已验证图形建议。

## 验证证据

验证数据：Seurat::pbmc_small（仅一个原始样本）。

PASS：pbmc_small 只有一个原始样本，现有验证仅覆盖原始 counts 求和及计数守恒；有生物学重复的处理组检验仍未验证。

运行和内存：小型演示不是性能基准，目标数据需记录耗时与线程设置；尽量保留稀疏计数，不要将整张图谱转为稠密矩阵。大型对象的内存消耗尚未基准测试。

## 脚本与参考

脚本：[workflow.R](scripts/workflow.R)（02_differential_analysis/pseudobulk/scripts/workflow.R）。运行命令与配置说明见 [README](README.md)。

参考：https://satijalab.org/seurat/reference/aggregateexpression
