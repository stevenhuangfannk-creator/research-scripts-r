# 通路与功能分析

先按输入和研究问题选择方法。

| 手头的数据/问题 | 入口 | 当前实现 |
|---|---|---|
| 所选基因和实际受检背景基因；过度代表性富集 | [GO/KEGG ORA](GO_KEGG/README.md) | 有脚本，CANDIDATE / BLOCKED；默认配置含占位符 |
| 完整带方向排序统计量；基因集富集 | [fgsea](GSEA/README.md) | 有脚本，CANDIDATE / BLOCKED；仅导出结果表 |
| 独立样本表达矩阵；样本级通路活性 | [GSVA/ssGSEA](GSVA_ssGSEA/README.md) | 候选说明，尚无脚本 |
| 单细胞状态；每细胞签名评分 | [UCell/AUCell](UCell_AUCell/README.md) | 候选说明，尚无脚本 |

样本级推断需要生物学重复；每细胞评分本身不构成供者层面的组间显著性。先查[方法索引](../METHOD_INDEX.md)、[图例](../GALLERY.md)和[登记规则](../registry/README.md)。目录存在不等于验证证据。
