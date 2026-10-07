# GSVA：估计样本层面的基因集活性，用于有生物学重复的组间比较

方法 ID：`gsva_ssgsea`。当前为 **CANDIDATE · UNVALIDATED**。

## 准备什么

归一化的基因 × 独立样本表达矩阵，以及基因集。

需要事先判断：review_required：GSVA 或 ssGSEA、核函数、基因集大小和已安装的 API 版本。当前只是待核对清单，尚未接入可执行脚本。

## 现在能否直接运行

本仓库尚未为 `gsva_ssgsea` 实现可执行工作流，registry 中的 `script` 为 `null`。因此不能通过 `scripts/run_method.R` 运行；即使添加 `--allow-unvalidated` 也不能补齐实现。

`config/default.yml` 是规划占位配置，`review_required` 记录待核对内容。请先查[方法卡](METHOD_CARD.md)和[官方文档](https://bioconductor.org/packages/GSVA)，完成最小复现与验证后再接入脚本。

## 结果和解释

通路 × 样本矩阵、组间热图/小提琴图（规划输出）。

较新的 GSVA API 使用参数对象；不能假定旧式 gsva(expr, sets) 调用仍可用。组间推断需要独立样本层面的重复。

继续查阅：[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例状态](gallery/README.md)、[配置](config/default.yml)。
