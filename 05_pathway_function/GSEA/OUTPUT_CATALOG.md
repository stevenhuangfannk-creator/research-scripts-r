# fgsea 输出目录

当前 **BLOCKED**，工作流未执行；以下区分现有输出和未实现的绘图能力。

| 输出 | 科学用途 | 代码状态 | 参数审查 | 正文/补充材料 | 执行证据 |
|---|---|---|---|---|---|
| gsea.tsv：NES、padj、leadingEdge 等 | 使用完整带方向排序统计量检验基因集富集；leadingEdge 以分号拼接 | [现有工作流](scripts/workflow.R) | min_size、max_size、seed；统计量方向、ID/基因集覆盖和版本 | 重点结果放正文，完整表放补充材料 | BLOCKED |
| 富集曲线 | 展示某个基因集在完整排序中的分布 | 规划能力；当前 workflow.R 不生成曲线 | 基因集、排序和比较尺度 | 对重点结论有帮助时放正文 | UNVALIDATED |

核心实际输出是数值表；当前返回 object = NULL，不保存分析对象。默认结果目录中的 sessionInfo.txt/run_metadata.yml 记录环境和配置。不存在已生成的原生视觉输出，不能把富集曲线标作已实现。排名方向、并列值、映射覆盖及 NES 比较边界见[方法卡](METHOD_CARD.md)，运行命令见[使用说明](README.md)。
