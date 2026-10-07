# 示例与验证

当前验证：**UNVALIDATED**。此方法尚无可执行工作流，也没有本仓库可运行的分析示例。

预期输入：用于 voom 的计数矩阵，或适当的对数表达矩阵；设计矩阵与对比。

建议先按[官方文档](https://bioconductor.org/packages/limma)准备小型示例，审查[方法卡](../METHOD_CARD.md)中的参数和使用边界，记录环境及实际输出，再实现和验证。本目录的 `config/default.yml` 仅保留规划提示。

`run_method.R` 会拒绝 `script=null` 的方法；`--allow-unvalidated` 只允许执行已经存在但未验证的脚本，不能使规划方法变成可运行方法。共享[smoke 检查](../../../../scripts/smoke_tests.R)不包含此方法的成功验证证据。
