# 输出说明：单细胞质量控制

以下是当前工作流与统一入口实际写入的结果。执行验证：PASS，范围以[方法卡](METHOD_CARD.md)为准。

| 文件（相对于 output_dir） | 内容与用途 |
|---|---|
| `qc.tsv` | 过滤前每个细胞的 QC 指标与 qc_pass。 |
| `retention.tsv` | input_cells、retained_cells、pass_cells，核查过滤损失。 |
| `object.rds` | 带 QC 标记或按显式配置过滤后的 Seurat 对象。 |

统一入口另写入 sessionInfo.txt（运行环境）与 run_metadata.yml（方法、配置、生成时间和验证范围）。

代码：[workflow.R](scripts/workflow.R)；参数及科研判断见[方法卡](METHOD_CARD.md)和[使用说明](README.md)。

图形应匹配数值尺度；表格足以表达结果时无需强行画图。可视化预览见[全局图例](../../GALLERY.md)。支持研究主张的输出可放主文，QC 与细节通常放补充材料，具体由论文证据链决定。

核心输出为上表。可选、高级或比较输出仅限方法卡明确支持的内容；未实现能力需要先作为独立候选复现与验证。
