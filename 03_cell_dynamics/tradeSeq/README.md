# tradeSeq：检验与谱系相关的基因表达趋势及差异

方法 ID：`tradeseq`。当前为 **CANDIDATE · UNVALIDATED**。

## 准备什么

计数矩阵、已推断轨迹的拟时序及细胞权重。

需要事先判断：review_required：样条结点数、谱系对比与协变量。当前只是待核对清单，尚未接入可执行脚本。

## 现在能否直接运行

本仓库尚未为 `tradeseq` 实现可执行工作流，registry 中的 `script` 为 `null`。因此不能通过 `scripts/run_method.R` 运行；即使添加 `--allow-unvalidated` 也不能补齐实现。

`config/default.yml` 是规划占位配置，`review_required` 记录待核对内容。请先查[方法卡](METHOD_CARD.md)和[官方文档](https://bioconductor.org/packages/tradeSeq)，完成最小复现与验证后再接入脚本。

## 结果和解释

GAM 拟合；association/pattern/endpoint 检验（规划输出）。

tradeSeq 使用给定轨迹，本身不推断谱系。

继续查阅：[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例状态](gallery/README.md)、[配置](config/default.yml)。
