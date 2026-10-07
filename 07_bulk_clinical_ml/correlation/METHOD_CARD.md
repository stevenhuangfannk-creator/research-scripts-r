# 方法卡：Pearson / Spearman 相关分析

**方法 ID:** correlation

**分类:** 07_bulk_clinical_ml

**状态:** VALIDATED

**语言:** R

**包 / 工具:** stats

**包版本:** 见[包加载与版本证据](../../docs/validation/package_status.tsv)；不能仅因包已安装就推断版本或方法可用。本次已有验证记录为 stats 4.3.1。

**最近验证:** 2026-10-07

**官方文档:** [stats 官方文档](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/cor.test.html)

**原始论文:** 从官方文档核对引用；本次整理未独立认证论文元数据。

**目的:** 估计 Pearson / Spearman 相关性，明确缺失值处理，并进行 BH 多重检验校正。

**科研问题:** 估计 Pearson / Spearman 相关性，明确缺失值处理，并进行 BH 多重检验校正。

**适用情况:** 每行一个独立观测单位的 data.frame，至少两个不同的数值型变量列；每一对变量至少有 4 个共同的有限观测，且两列都不能为常量。

**不适用情况 / 使用边界:** 相关不等于因果。Pearson 衡量线性关联，Spearman 衡量单调的秩关联；重复测量或存在混杂时需要其他模型。

**必需输入:** 每行一个独立观测单位的 data.frame，至少两个不同的数值型变量列；每一对变量至少有 4 个共同的有限观测，且两列都不能为常量。

**可选输入:** 仅限 workflow.R 和配置实际支持的字段；该封装未实现的方法或参数不能仅凭包的功能推断。

**主要参数:** variables = 明确指定数值列；method = pearson / spearman；missing = error / pairwise

**推荐起点:** 文档中的参数只是起点，应结合具体数据审查。知名包不自动获得 DEFAULT 状态。

**需要科研判断的参数:** 相关不等于因果。Pearson 衡量线性关联，Spearman 衡量单调的秩关联；重复测量或存在混杂时需要其他模型。 具体配置见 [README](README.md)。

**输出:** r / rho、P 值、BH 校正 P 值、样本数与排除数；Pearson 置信区间；当前实现不提供 Spearman 置信区间。实际文件和字段见[输出目录](OUTPUT_CATALOG.md)。

**优势:** 输入要求、来源和目标输出明确，方法范围较小。

**局限:** 相关不等于因果。Pearson 衡量线性关联，Spearman 衡量单调的秩关联；重复测量或存在混杂时需要其他模型。

**假设:** 相关不等于因果。Pearson 衡量线性关联，Spearman 衡量单调的秩关联；重复测量或存在混杂时需要其他模型。

**常见问题:** 相关不等于因果。Pearson 衡量线性关联，Spearman 衡量单调的秩关联；重复测量或存在混杂时需要其他模型。

**替代方法:** 需要控制协变量时使用偏相关 / 回归；重复测量使用混合模型。

**何时选择替代方案:** 需要控制协变量时使用偏相关 / 回归；重复测量使用混合模型。；仍需核对其输入和验证范围。

**已验证数据:** datasets::iris（150 个真实花朵观测）

**验证状态:** PASS — Pearson / Spearman 检验、BH 校正，以及缺失值 / 常量列的回归检查；混合物种存在混杂。

**运行时间:** 小型示例不能代表性能基准；正式数据需记录耗时和线程设置。

**内存:** 在适用情况下保留稀疏表示，避免将整个大型图谱转为稠密矩阵；大对象内存占用尚未评测。

**绘图选择:** 先读[输出目录](OUTPUT_CATALOG.md)，再核对已登记的[图例](../../GALLERY.md)。未生成预览的图不视为可视化推荐。

**推荐脚本:** [workflow.R](scripts/workflow.R)

**参考资料:** [stats 官方文档](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/cor.test.html)
