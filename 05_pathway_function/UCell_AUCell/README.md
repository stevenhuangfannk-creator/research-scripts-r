# UCell / AUCell：基于表达排序的富集为每个细胞计算基因签名评分

方法 ID：`ucell_aucell`。当前为 **CANDIDATE · UNVALIDATED**。

## 准备什么

细胞表达排序/计数和指定的签名基因集。

需要事先判断：review_required：排序截断、基因覆盖率和签名方向。当前只是待核对清单，尚未接入可执行脚本。

## 现在能否直接运行

本仓库尚未为 `ucell_aucell` 实现可执行工作流，registry 中的 `script` 为 `null`。因此不能通过 `scripts/run_method.R` 运行；即使添加 `--allow-unvalidated` 也不能补齐实现。

`config/default.yml` 是规划占位配置，`review_required` 记录待核对内容。请先查[方法卡](METHOD_CARD.md)和[官方文档](https://bioconductor.org/packages/UCell)，完成最小复现与验证后再接入脚本。

## 结果和解释

细胞 × 签名评分、UMAP/小提琴图/热图（规划输出）。

细胞评分描述状态；组间显著性需要按供者聚合或使用考虑供者结构的模型。

继续查阅：[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例状态](gallery/README.md)、[配置](config/default.yml)。
