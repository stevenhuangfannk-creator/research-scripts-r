# UMAP 图资产

| Plot ID | 用途 | 代码 | 优先级／证据 |
|---|---|---|---|
| `umap_clean_v1` | 已计算的聚类在 UMAP 中如何分布？ | [代码](../../08_visualization/UMAP/umap_clean_v1.R) | CURRENT_DEFAULT；仅验证渲染 |

预览与完整输入／参数／来源元数据见[总画廊](../../GALLERY.md)。保留提供的全部数值观测，合成数据明确标记。`CURRENT_DEFAULT` 表示该输入范围内的优选模板，不表示分析结论已验证；
演示生成器使用固定数据，用自己的结果时请调用对应图形函数，步骤见[中文指南](../../docs/USAGE_ZH_CN.md)。

## 调用自己的 UMAP 坐标

`plot_umap_clean()` 接受含 `x`、`y`、`group` 的 data.frame，以及名称覆盖全部 group 的颜色向量。它不会计算 UMAP。在仓库根目录的 R 控制台按以下接口调用（`my_umap` 必须先由自己的分析生成）：

```r
source("08_visualization/themes/theme_research.R")
source("08_visualization/palettes/palettes.R")
source("08_visualization/UMAP/umap_clean_v1.R")
# my_umap: data.frame(x, y, group)，x/y 为有限数值
labels <- unique(as.character(my_umap$group))
colors <- setNames(research_palette("okabe_ito", n = length(labels)), labels)
p <- plot_umap_clean(my_umap, colors, title = "UMAP")
save_research_plot(p, "results/my_figures/umap")
```

Okabe–Ito 最多支持 8 个分类；颜色不足时应换编码或分面。已有细胞类型应使用登记的固定颜色，避免换图后颜色含义改变。
