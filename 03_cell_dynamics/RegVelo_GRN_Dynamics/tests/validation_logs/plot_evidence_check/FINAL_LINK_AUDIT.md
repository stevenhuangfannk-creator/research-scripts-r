# 最终文档链接与图册来源核查 / Final links and gallery provenance

状态：PASS_WITH_PENDING。使用Python标准库完成，只读取现有文档、CSV、JSON及PDF；未导入模型库或改变分析文件。

- 核对7份指定文档，共168个本地链接；非待生成的断链0处。
- Gallery catalog及README均覆盖A01–A04、B01–B07、C01–C05、D01–D05、E01–E06，共27项。
- 27份source CSV与本机正式输出逐文件SHA-256完全一致；27份PDF也完全一致。
- 27份metadata的科学问题、方法、证据标签、数值输入、解释边界、seed和状态与原始metadata一致；catalog内本地CSV、PNG及PDF路径可解析。
- PNG登记为压缩预览，preview_only=true；图册说明原300dpi PNG及SVG留在本地独立结果。

待生成：MODEL_QC_REPORT.md尚不存在，按父任务说明登记为待生成；涉及链接：
- gallery/README.md → ../MODEL_QC_REPORT.md

完整逐项记录见FINAL_LINK_AUDIT.json。
