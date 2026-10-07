# 相关性图形

Pearson 用于数值测量的线性关联，应检查离群点与混杂；Spearman 描述单调的秩关联，适用于序数或偏态测量，重复值会影响推断。两者都不能证明因果。独立单位应是生物学样本，重复观测需要合适模型。[相关性流程](../../07_bulk_clinical_ml/correlation/README.md)记录缺失值策略、完整配对数及 BH 校正检验集合。

[散点＋拟合／置信区间函数](scatter_fit_v1.R)、密度分箱散点、双变量对面板及 BH 相关热图见[画廊](../../GALLERY.md)。`iris` 示例合并物种，存在混杂；线性模型阴影是拟合的 95% 置信区间，不是 Spearman rho 的置信区间。

## 调用示例

在仓库根目录的 R／RStudio 控制台运行，需已安装 `ggplot2`、`ragg`：

```r
source("08_visualization/themes/theme_research.R")
source("08_visualization/Scatter_Correlation/scatter_fit_v1.R")
p <- plot_scatter_fit(iris, "Sepal.Length", "Petal.Length", method = "pearson")
save_research_plot(p, "results/my_figures/iris_scatter")
```

输出为自己的 `results/my_figures/iris_scatter.png` 和 `.pdf`，不覆盖画廊。换成自己的 data.frame 和数值列名时，先处理缺失、非有限值并检查观测独立性。
