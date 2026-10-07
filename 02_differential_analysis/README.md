# 差异分析（02_differential_analysis）

先区分问题：探索 cluster marker，与在独立生物学样本之间检验处理效应，是不同的任务。细胞不能直接当作独立样本重复。

| 科研问题 | 入口 | 能做什么 |
|---|---|---|
| 哪些基因区分 cluster？ | [cell_markers](differential_expression/README.md) | FindAllMarkers 的探索性 marker 表，不提供 donor 层级处理组推断 |
| 如何准备样本层级 counts？ | [pseudobulk](pseudobulk/README.md) | 按生物学样本 × 细胞类型求和；不执行 DEG 检验 |
| 细胞群/邻域丰度是否变化？ | [differential_abundance](differential_abundance/README.md) | 仅候选说明，尚无可执行 workflow |

要做 condition DEG，先核查生物学重复、样本/细胞类型标签和设计表，再汇总 raw RNA counts；随后选用与设计匹配的 DESeq2/edgeR/limma 等模型。仓库中的 bulk_deseq2 仍为候选，不是已完成的整套差异分析流程。

先读[方法索引](../METHOD_INDEX.md)、[图例](../GALLERY.md)与[注册表说明](../registry/README.md)，再查每个方法的输入、参数、命令和输出。目录存在或示例 PASS 都不能扩大方法卡中写明的验证范围。
