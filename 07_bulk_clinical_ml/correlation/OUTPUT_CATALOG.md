# 输出目录：Pearson / Spearman 相关分析

以下文件由 [workflow.R](scripts/workflow.R) 经统一运行入口写入配置的 `output_dir`。方法执行验证为 **PASS**，范围限于 datasets::iris（150 个真实花朵观测）：Pearson / Spearman 检验、BH 校正，以及缺失值 / 常量列的回归检查；混合物种存在混杂。

| 文件 | 内容和用途 |
|---|---|
| `correlations.tsv` | 所有所选变量两两组合；x、y、n、excluded、r、p、ci_low、ci_high、p_adjust。Spearman 的 CI 为 NA。 |
| `sessionInfo.txt` | 本次 R 与包环境。 |
| `run_metadata.yml` | 方法 ID、实际配置、生成时间及既有验证范围。 |

这些是数值 / 对象输出；工作流不自动生成科研图片。绘图预览及源代码需另查[全局图例](../../GALLERY.md)。支持核心研究结论的结果可用于主文，质控和细节可放补充材料；具体由证据作用决定。

同一个 `output_dir` 中的同名输出可能被覆盖；每次正式分析建议使用独立输出目录。新增可选、进阶或对比结果应先说明实现和验证范围。
