# 方法卡：SCTransform 方差稳定化

| 字段 | 内容 |
|---|---|
| 方法 ID | sctransform |
| 分类 | 01_scrna_core |
| 状态 | CANDIDATE |
| 语言 | R |
| 包 | Seurat |
| 最近验证 | 尚未验证 |

包版本见[构建环境记录](../../../docs/validation/package_status.tsv)；安装过某个包不等于它能够正常加载，也不等于方法经过验证。

官方文档：https://satijalab.org/seurat/articles/sctransform_vignette

原始论文：原始论文见官方文档所列引用；本次构建未独立核验论文元数据。

## 科研问题与用途

建模测序深度效应，生成用于后续探索的 SCT assay 和变量基因。

## 适用条件与输入契约

含 RNA counts 的 Seurat 对象（RDS）。若指定 vars_to_regress，相应协变量须存在于元数据。

可选输入仅限工作流与配置实际支持的字段；候选方法的输入契约是规划规格，不能视为已实现功能。

## 实际调用与主要参数

Seurat::SCTransform(assay = "RNA", vst.flavor = "v2", vars.to.regress = ..., seed.use = ...) 返回带 SCT assay 的对象。

vars_to_regress 默认为 null；seed 固定随机种子。配置中的 vst_flavor 当前不被读取，脚本固定 vst.flavor = "v2"。

参数值是起点，须结合物种、数据规模和样本设计审核。包广泛使用或参数有默认值，不意味着方法被提升为 DEFAULT。

## 假设、局限与常见误区

回归协变量需要生物学理由，避免把研究目标相关信号一并去掉。保留 RNA assay 供后续需要该表达尺度的通信分析；极小稀疏示例不能代表真实模型拟合可靠性。

优点是输入、参数和输出范围明确，便于复用与追溯；该小型工作流不覆盖完整科研分析流程。

## 替代路线与选择依据

简单的探索路线可用 LogNormalize；正式推断可选与设计匹配的计数模型。

## 输出与图形

实际输出见[输出说明](OUTPUT_CATALOG.md)。需要画图时先查该输出说明，再查[全局图例](../../../GALLERY.md)；没有已渲染预览的图不能当作已验证图形建议。

## 验证证据

验证数据：无。

UNVALIDATED：本构建没有可执行验证证据，也没有已验证的数据集。

运行和内存：小型演示不是性能基准，目标数据需记录耗时与线程设置；尽量保留稀疏计数，不要将整张图谱转为稠密矩阵。大型对象的内存消耗尚未基准测试。

## 脚本与参考

脚本：[workflow.R](scripts/workflow.R)（01_scrna_core/normalization/SCTransform/scripts/workflow.R）。运行命令与配置说明见 [README](README.md)。

参考：https://satijalab.org/seurat/articles/sctransform_vignette
