# 方法卡：Harmony 批次整合

| 字段 | 内容 |
|---|---|
| 方法 ID | harmony |
| 分类 | 01_scrna_core |
| 状态 | CANDIDATE |
| 语言 | R |
| 包 | harmony |
| 最近验证 | 尚未验证 |

包版本见[构建环境记录](../../../docs/validation/package_status.tsv)；安装过某个包不等于它能够正常加载，也不等于方法经过验证。

官方文档：https://portals.broadinstitute.org/harmony/articles/quickstart.html

原始论文：https://doi.org/10.1038/s41592-019-0619-0

## 科研问题与用途

对已有 PCA 嵌入进行技术批次校正，获得 Harmony 嵌入。

## 适用条件与输入契约

已标准化、已有 pca reduction 的 Seurat 对象（RDS），含 batch_column 指定的技术批次列，并至少有两个批次。

可选输入仅限工作流与配置实际支持的字段；候选方法的输入契约是规划规格，不能视为已实现功能。

## 实际调用与主要参数

harmony::RunHarmony(group.by.vars = ..., reduction.use = "pca", dims.use = seq_len(npcs), theta = ...) 在对象中增加 Harmony reduction。

batch_column 改为真实元数据列名；npcs 不得超过已有 PCA 的维数；theta 为 Harmony 多样性惩罚参数，配置起点为 2。

参数值是起点，须结合物种、数据规模和样本设计审核。包广泛使用或参数有默认值，不意味着方法被提升为 DEFAULT。

## 假设、局限与常见误区

批次与处理组完全混杂时，整合不能可靠恢复处理效应。Harmony 校正的是嵌入而非原始计数，须比较批次混合与谱系保留。当前 seurat_clustering 会重算并使用 pca，不会自动用 Harmony 嵌入。

优点是输入、参数和输出范围明确，便于复用与追溯；该小型工作流不覆盖完整科研分析流程。

## 替代路线与选择依据

可比较 Seurat anchors；不能分离技术批次与真实生物差异时，考虑保留未整合分析。

## 输出与图形

实际输出见[输出说明](OUTPUT_CATALOG.md)。需要画图时先查该输出说明，再查[全局图例](../../../GALLERY.md)；没有已渲染预览的图不能当作已验证图形建议。

## 验证证据

验证数据：无。

UNVALIDATED：本构建没有可执行验证证据，也没有已验证的数据集。

运行和内存：小型演示不是性能基准，目标数据需记录耗时与线程设置；尽量保留稀疏计数，不要将整张图谱转为稠密矩阵。大型对象的内存消耗尚未基准测试。

## 脚本与参考

脚本：[workflow.R](scripts/workflow.R)（01_scrna_core/batch_integration/Harmony/scripts/workflow.R）。运行命令与配置说明见 [README](README.md)。

参考：https://portals.broadinstitute.org/harmony/articles/quickstart.html; https://doi.org/10.1038/s41592-019-0619-0
