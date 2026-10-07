# 方法卡：DecontX 环境 RNA 去污染

| 字段 | 内容 |
|---|---|
| 方法 ID | decontx |
| 分类 | 01_scrna_core |
| 状态 | CANDIDATE |
| 语言 | R |
| 包 | celda |
| 最近验证 | 尚未验证 |

包版本见[构建环境记录](../../../docs/validation/package_status.tsv)；安装过某个包不等于它能够正常加载，也不等于方法经过验证。

官方文档：https://bioconductor.org/packages/release/bioc/vignettes/celda/inst/doc/decontX.html

原始论文：原始论文见官方文档所列引用；本次构建未独立核验论文元数据。

## 科研问题与用途

按 capture 独立估计并减少环境 RNA 污染。

## 适用条件与输入契约

RDS 中保存 list(counts, metadata, backgrounds)。counts 为原始基因 × 细胞计数；metadata 的行名顺序须与 counts 列名完全一致，并含 capture_column。backgrounds 若提供，为按 capture ID 命名的空液滴计数矩阵列表；背景可缺省。

可选输入仅限工作流与配置实际支持的字段；候选方法的输入契约是规划规格，不能视为已实现功能。

## 实际调用与主要参数

用 SingleCellExperiment::SingleCellExperiment() 包装原始计数，调用 celda::decontX(background = ...)，返回按 capture 命名的 SingleCellExperiment 结果列表。

capture_column 改为真实元数据列名；seed 固定随机种子。工作流按 capture 拆分，每个 capture 独立调用 decontX。

参数值是起点，须结合物种、数据规模和样本设计审核。包广泛使用或参数有默认值，不意味着方法被提升为 DEFAULT。

## 假设、局限与常见误区

背景矩阵的基因行名和顺序必须与细胞计数完全一致。不要使用已标准化矩阵。采用校正结果前，比较 marker 特异性与生物信号保留情况；脚本不会自动合并为新的 Seurat 对象。

优点是输入、参数和输出范围明确，便于复用与追溯；该小型工作流不覆盖完整科研分析流程。

## 替代路线与选择依据

同时有 raw/filtered droplets 和 cluster 信息时可评估 SoupX；本仓库 SoupX 仍只有候选说明。

## 输出与图形

实际输出见[输出说明](OUTPUT_CATALOG.md)。需要画图时先查该输出说明，再查[全局图例](../../../GALLERY.md)；没有已渲染预览的图不能当作已验证图形建议。

## 验证证据

验证数据：无。

BLOCKED：现有构建环境缺少 celda，工作流未执行；没有已验证的数据集。

运行和内存：小型演示不是性能基准，目标数据需记录耗时与线程设置；尽量保留稀疏计数，不要将整张图谱转为稠密矩阵。大型对象的内存消耗尚未基准测试。

## 脚本与参考

脚本：[workflow.R](scripts/workflow.R)（01_scrna_core/ambient_rna/DecontX/scripts/workflow.R）。运行命令与配置说明见 [README](README.md)。

参考：https://bioconductor.org/packages/release/bioc/vignettes/celda/inst/doc/decontX.html
