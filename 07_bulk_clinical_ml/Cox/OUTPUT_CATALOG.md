# 输出目录：Cox 比例风险回归

以下文件由 [workflow.R](scripts/workflow.R) 经统一运行入口写入配置的 `output_dir`。方法执行验证为 **PASS**，范围限于 survival::lung（age 与 sex 协变量）：仅验证 Cox HR / CI 和比例风险诊断输出；未验证预测能力或因果解释。

| 文件 | 内容和用途 |
|---|---|
| `object.rds` | coxph 模型对象。 |
| `cox.tsv` | 协变量项、exp(coef)、exp(-coef)、lower .95、upper .95，以及 P 值；实际列名经 data.frame 转换。 |
| `proportional_hazards.tsv` | cox.zph 的各协变量及 GLOBAL 诊断：chisq、df、p。 |
| `sessionInfo.txt` | 本次 R 与包环境。 |
| `run_metadata.yml` | 方法 ID、实际配置、生成时间及既有验证范围。 |

这些是数值 / 对象输出；工作流不自动生成科研图片。绘图预览及源代码需另查[全局图例](../../GALLERY.md)。支持核心研究结论的结果可用于主文，质控和细节可放补充材料；具体由证据作用决定。

同一个 `output_dir` 中的同名输出可能被覆盖；每次正式分析建议使用独立输出目录。新增可选、进阶或对比结果应先说明实现和验证范围。
