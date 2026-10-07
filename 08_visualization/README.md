# 科研绘图库

这里提供带明确输入字段、版本化代码、模板选择状态、PNG／PDF 与来源记录的绘图资产。先从[总画廊](../GALLERY.md)选择图，再按 [Plot ID 登记表](../registry/plots.yml)查找代码和参数；分析方法见[方法索引](../METHOD_INDEX.md)。

绘图函数接受已经计算的结果，不自动完成上游分析。合成风格演示标为 `SYNTHETIC`；目录存在或模板好看不等于分析已验证。颜色和导出主题见[配色索引](../PALETTE_INDEX.md)、[图形约定](../docs/FIGURE_CONTRACT.md)。

## 用自己的数据

1. 选 Plot ID 并查看所属目录 README、R 函数和元数据。
2. 将自己的结果整理成函数要求的字段；保留样本单位、数值尺度和颜色对应。
3. 加载 `themes/theme_research.R` 与相应绘图函数，按函数参数绘图。
4. 用 `save_research_plot()` 保存到自己的结果目录，检查 PNG 和可编辑文本 PDF。

UMAP 和相关散点图目录提供直接调用示例。完整入门见[中文使用指南](../docs/USAGE_ZH_CN.md)。画廊生成器使用固定演示数据并更新登记表，查看现有图不必重新运行它。
