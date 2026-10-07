# limma 差异表达

方法 ID：`limma`。拟合样本级线性模型，并使用经验贝叶斯方法稳定方差估计。

当前状态：**CANDIDATE**；执行验证：**UNVALIDATED**。先读[方法卡](METHOD_CARD.md)、[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例](gallery/README.md)和[配置](config/default.yml)。

## 当前可用内容

本目录提供中文方法说明、输入要求、待审查参数和目标输出，**尚无可执行工作流**。注册表中的 `script` 为 `null`，不能用 `run_method.R` 运行此方法；`--allow-unvalidated` 也不会生成缺失的实现。

## 使用前准备

1. 准备输入：用于 voom 的计数矩阵，或适当的对数表达矩阵；设计矩阵与对比。
2. 审查规划参数：review_required = 实验设计；voom 权重；对比；trend。
3. 参考[官方文档](https://bioconductor.org/packages/limma)完成小型可复现实例，再记录输入、参数、依赖版本与实际输出；实现及验证完成后才可在本仓库运行或升级状态。

`config/default.yml` 中的 `input`、`output_dir` 和 `review_required` 是规划占位，不能视为已实现的输入接口。输入尺度决定分析路线；校正技术批次不能消除完全混杂的实验设计。
