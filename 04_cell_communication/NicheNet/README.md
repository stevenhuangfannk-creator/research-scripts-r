# nichenetr：优先筛选能够解释接收细胞转录响应的发送细胞配体

方法 ID：`nichenet`。当前为 **CANDIDATE · UNVALIDATED**。

## 准备什么

发送/接收细胞表达、接收细胞的差异表达基因、背景表达基因和先验网络。

需要事先判断：review_required：接收细胞基因集/背景、表达阈值和先验网络物种。当前只是待核对清单，尚未接入可执行脚本。

## 现在能否直接运行

本仓库尚未为 `nichenet` 实现可执行工作流，registry 中的 `script` 为 `null`。因此不能通过 `scripts/run_method.R` 运行；即使添加 `--allow-unvalidated` 也不能补齐实现。

`config/default.yml` 是规划占位配置，`review_required` 记录待核对内容。请先查[方法卡](METHOD_CARD.md)和[官方文档](https://github.com/saeyslab/nichenetr)，完成最小复现与验证后再接入脚本。

## 结果和解释

配体活性排序、配体–靶基因矩阵、LR 网络和优先级图（规划输出）。

先验模型和接收细胞对比设计会影响结果；配体活性属于预测证据，不能证明因果。

继续查阅：[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例状态](gallery/README.md)、[配置](config/default.yml)。
