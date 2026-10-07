# slingshot：沿聚类骨架拟合细胞谱系曲线

方法 ID：`slingshot`。当前为 **CANDIDATE · UNVALIDATED**。

## 准备什么

低维嵌入、聚类标签，以及有生物学依据的起始聚类。

需要事先判断：review_required：start.clus；end.clus；shrinkage。当前只是待核对清单，尚未接入可执行脚本。

## 现在能否直接运行

本仓库尚未为 `slingshot` 实现可执行工作流，registry 中的 `script` 为 `null`。因此不能通过 `scripts/run_method.R` 运行；即使添加 `--allow-unvalidated` 也不能补齐实现。

`config/default.yml` 是规划占位配置，`review_required` 记录待核对内容。请先查[方法卡](METHOD_CARD.md)和[官方文档](https://bioconductor.org/packages/slingshot)，完成最小复现与验证后再接入脚本。

## 结果和解释

谱系、拟时序和曲线权重（规划输出）。

推断拓扑依赖聚类结果和起点假设。

继续查阅：[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例状态](gallery/README.md)、[配置](config/default.yml)。
