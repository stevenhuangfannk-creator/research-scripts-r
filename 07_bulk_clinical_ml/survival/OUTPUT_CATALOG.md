# 输出目录：Kaplan–Meier 生存分析

以下文件由 [workflow.R](scripts/workflow.R) 经统一运行入口写入配置的 `output_dir`。方法执行验证为 **PASS**，范围限于 survival::lung（228 条公开临床记录）：使用明确 0 / 1 事件映射的右删失 KM 曲线和置信区间表；不支持新的临床解释。

| 文件 | 内容和用途 |
|---|---|
| `object.rds` | survfit 模型对象。 |
| `km.tsv` | time、survival、lower、upper、n_risk、events、strata；默认汇总的事件时间点。 |
| `groups.tsv` | 输入各组观测数；不是各时间点的风险集人数。 |
| `sessionInfo.txt` | 本次 R 与包环境。 |
| `run_metadata.yml` | 方法 ID、实际配置、生成时间及既有验证范围。 |

这些是数值 / 对象输出；工作流不自动生成科研图片。绘图预览及源代码需另查[全局图例](../../GALLERY.md)。支持核心研究结论的结果可用于主文，质控和细节可放补充材料；具体由证据作用决定。

同一个 `output_dir` 中的同名输出可能被覆盖；每次正式分析建议使用独立输出目录。新增可选、进阶或对比结果应先说明实现和验证范围。
