# 示例与验证上下文

- [原始项目映射](../99_legacy_projects/README.md)：历史来源；缺少 APAP／GSE255834 输入，不能认证原项目结果。
- [R 小型执行检查](../scripts/smoke_tests.R)：使用 Seurat `pbmc_small`、`iris` 与 `survival::lung`，每个方法单独记录检查范围。
- [验证证据](../docs/validation/)：实际日志、包状态与限定范围的 PASS／BLOCKED 结果。
- [论文复现历史](../reproductions/README.md)：保留原记录，不扩展空间分析流程。
- [中文入门示例](../docs/USAGE_ZH_CN.md)：运行内置 iris 相关性流程，了解配置与输出。

大型／中间生成对象不进入 Git；内置数据从已安装包加载，合成绘图数据保留在明确标识的演示代码中。重新运行 smoke 检查会更新验证记录。
