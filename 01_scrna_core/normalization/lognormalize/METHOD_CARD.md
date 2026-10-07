# 方法卡：LogNormalize 标准化

| 字段 | 内容 |
|---|---|
| 方法 ID | lognormalize |
| 分类 | 01_scrna_core |
| 状态 | VALIDATED |
| 语言 | R |
| 包 | Seurat |
| 最近验证 | 2026-10-07 |

包版本见[构建环境记录](../../../docs/validation/package_status.tsv)；安装过某个包不等于它能够正常加载，也不等于方法经过验证。

官方文档：https://satijalab.org/seurat/articles/pbmc3k_tutorial

原始论文：原始论文见官方文档所列引用；本次构建未独立核验论文元数据。

## 科研问题与用途

按细胞总计数进行标准化并取对数，供探索性表达分析与后续降维使用。

## 适用条件与输入契约

含 RNA counts 的 Seurat 对象（RDS）。

可选输入仅限工作流与配置实际支持的字段；候选方法的输入契约是规划规格，不能视为已实现功能。

## 实际调用与主要参数

将 DefaultAssay 设为 RNA，调用 Seurat::NormalizeData(normalization.method = "LogNormalize", scale.factor = ...)，生成 RNA data layer。

scale_factor 是标准化缩放因子，配置起点为 10000。

参数值是起点，须结合物种、数据规模和样本设计审核。包广泛使用或参数有默认值，不意味着方法被提升为 DEFAULT。

## 假设、局限与常见误区

标准化不等于批次校正。保留 raw counts 给计数模型；不要把 RNA data layer 当作 pseudobulk 原始整数计数。

优点是输入、参数和输出范围明确，便于复用与追溯；该小型工作流不覆盖完整科研分析流程。

## 替代路线与选择依据

需要基于计数模型的方差稳定化时可评估 SCTransform；计数推断应使用与设计匹配的模型。

## 输出与图形

实际输出见[输出说明](OUTPUT_CATALOG.md)。需要画图时先查该输出说明，再查[全局图例](../../../GALLERY.md)；没有已渲染预览的图不能当作已验证图形建议。

## 验证证据

验证数据：Seurat::pbmc_small。

PASS：在 pbmc_small 上验证 LogNormalize 分支，原始 counts 保留且 RNA data layer 数值有限；不代表批次效应已处理。

运行和内存：小型演示不是性能基准，目标数据需记录耗时与线程设置；尽量保留稀疏计数，不要将整张图谱转为稠密矩阵。大型对象的内存消耗尚未基准测试。

## 脚本与参考

脚本：[workflow.R](scripts/workflow.R)（01_scrna_core/normalization/lognormalize/scripts/workflow.R）。运行命令与配置说明见 [README](README.md)。

参考：https://satijalab.org/seurat/articles/pbmc3k_tutorial
