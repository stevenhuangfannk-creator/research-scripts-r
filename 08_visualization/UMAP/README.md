# UMAP 图资产

| Plot ID | 用途 | 代码 | 优先级／证据 |
|---|---|---|---|
| `umap_clean_v1` | 已计算的聚类在 UMAP 中如何分布？ | [代码](../../08_visualization/UMAP/umap_clean_v1.R) | CURRENT_DEFAULT；仅验证渲染 |
| `umap_fireworks_atlas` | 大量真实细胞的密集彩色 atlas 展示 | [代码](umap_fireworks_atlas.R) | ALTERNATIVE；并列风格，非 V2 |
| `umap_density_landscape` | 同一二维 UMAP 中各条件的密度山峦 | [代码](umap_density_landscape.R) | ALTERNATIVE；并列用途，非 UMAP 3 |

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

## 并列真实图例 / Parallel real-data examples

两个新图是并列资产，不替代 `umap_clean_v1`，不使用 V1/V2 命名，也不改变原默认选择。目标是更清楚地展示真实坐标和捕获分布，不是证明新聚类、疾病效应或更好算法。

![烟花风格 atlas UMAP](gallery/umap_fireworks_atlas.png)

图例：每点一个细胞，颜色与直接标签表示既有 `celltype_broad` 暂定注释。采用小点、密集彩色 atlas、白背景和简洁坐标轴，灵感来自[肾脏 atlas 原论文 Fig. 1f](https://www.nature.com/articles/s41586-026-10363-4)；“烟花”是展示称呼，**不是新 UMAP 算法，也不把坐标扩成放射线**。这里用小鼠牙龈 GSE188217 的 18,574 个细胞，不是原论文约 506 万细胞的肾脏数据，不能承诺得到一样外形。所有细胞包括 1,610 个 Unresolved 均保留；ggrepel 只挪标签、不挪细胞。12 类颜色沿用 `oral-scrna-atlas/scripts/plot_atlas.py` 的固定映射，见 [颜色表](gallery/umap_fireworks_atlas.colors.csv)。超过 8 类不宣称完整色盲安全；直接标签及图例提供辅助编码。

![共享 UMAP 的密度山峦](gallery/umap_density_landscape.png)

图例：X/Y 沿用同一个二维 UMAP；Z 是 Gaussian KDE **概率密度**，不是表达量、不是 cell count、不是 UMAP 3。Control 6,929 / db/db 11,645 个细胞，两面板共用坐标范围、bandwidth、100 × 100 网格、色域和 Z 范围；每面各自归一到数值积分 1，因此不能把更高山峰解释为更多捕获细胞。bandwidth 本次由合并坐标估计（约 0.6678 / 0.9257），不为让组间差异更大而单独调参；归一化补偿有限网格的尾部截断。使用 [MASS::kde2d 官方 API](https://stat.ethz.ch/R-manual/R-devel/library/MASS/html/kde2d.html)，接口暴露实际 Gaussian SD，内部传 `h=4*bandwidth` 以匹配 MASS 的参数定义。

**每个条件只有一个公开文库，条件与文库/批次混杂；两图仅作描述，不作疾病效应检验或独立动物重复推断。** 原对象来自既有口腔图鉴的 Scanpy 处理链，不是本次 Seurat 重跑；标签仍为 provisional。没有删除细胞、伪造重复、计算新 UMAP 或改动原始表达矩阵。

## 复用函数 / Function calls

从仓库根目录 source 两个函数；`source()` 不安装依赖、不读取数据、不自动生成图。

```r
source("08_visualization/UMAP/umap_fireworks_atlas.R")
# my_umap: x, y, group；fixed_colors: 命名向量，覆盖全部 group
p <- plot_umap_fireworks_atlas(my_umap, fixed_colors, point_size = 0.18)
ggplot2::ggsave("results/fireworks.png", p, width = 183, height = 135,
               units = "mm", dpi = 400, device = grDevices::png, type = "cairo")

source("08_visualization/UMAP/umap_density_landscape.R")
# my_umap 还需 condition；必须在同一二维嵌入上比较，不能拼接各组独立 UMAP
landscape <- compute_umap_density_landscape(my_umap, grid_n = 100)
grDevices::png("results/density.png", width = 183, height = 120,
               units = "mm", res = 400, type = "cairo")
draw_umap_density_landscape(landscape)
grDevices::dev.off()
```

先创建自己的 `results/` 目录；依赖 `ggplot2`、`ggrepel`、`MASS`、`viridisLite`，没有依赖 Seurat。大量类别或超过两三个密度面板时，应分多页并调整画布，不强挤在本例两面板尺寸。PNG 用 base Cairo，避免本机中文路径与 ragg 设备兼容问题；PDF 使用 `cairo_pdf()`。

## 重跑本例 / Reproduce this example

输入取自 [口腔图鉴 GSE188217](https://github.com/stevenhuangfannk-creator/oral-scrna-atlas/tree/main/datasets/GSE188217)，GEO 来源 [GSE188217](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE188217)。原始公开文库 GSM5672499/GSM5672500；既有对象的 counts/注释与 QC 限制遵循图鉴。H5AD、逐细胞坐标 CSV 留本地（Git 忽略），不会随 clone 自动取得。公开的 [source receipt](gallery/GSE188217_umap.source.json) 记录对象/导出 SHA-256、样本与标签数和 UMAP seed 17。

在已有兼容 AnnData 环境下仅导出坐标；Python 在这里只做数据转换，全部图由 R 生成：

```powershell
python scripts/export_umap_input.py --input "YOUR_DATA/GSE188217_annotated_v0.1.h5ad" --output results/umap/GSE188217_umap.csv
Rscript scripts/test_umap_alternatives.R results/umap/GSE188217_umap.csv
Rscript scripts/generate_umap_alternatives.R results/umap/GSE188217_umap.csv
```

导出器拒绝覆盖已有 CSV；没有该对象时按口腔图鉴获取/重建，重新计算的坐标可能变化，不能假装与快照完全一致。生成器是此 12 类 GSE188217 的固定图例，自己的数据直接用函数接口。生成器写 gallery PNG/PDF、KDE [网格值](gallery/umap_density_landscape.grid.csv)、颜色表、[运行记录](gallery/umap_alternatives.validation.json) 和 [环境](gallery/umap_alternatives.sessionInfo.txt)；会更新本例文件，不改旧 clean 图或原始数据。

验证范围：实际 18,574 行通过坐标/行数保留、共同网格、概率积分与错误输入拒绝检查；实际 PNG/PDF 检查字号和布局。未做生物学验证、bandwidth 敏感性或跨重复统计推断。预览是二维投影的静态 3D surface，不承诺浏览器交互。

QA 注：有效 PDF 最小字号为 atlas 7 pt、密度图约 8.4 pt，PNG 检查无文字遮挡；所有图由 R 绘制。通用投稿静态检查提示此 GitHub 示例未提供 SVG/TIFF 和默认 600 dpi，未宣称满足完整投稿导出。Cairo 原始 Tf=1 使用文本矩阵缩放，字号采用非可视化 PyMuPDF 提取的有效值核对。两个新登记项的合并保留逻辑已测；旧 Seurat 全画廊生成器未在本次默认环境重跑。

来源：公众号 [3D KDE UMAP](https://mp.weixin.qq.com/s/tp-vlARTlMtbG1d4rBagLw)、[烟花 UMAP](https://mp.weixin.qq.com/s/SAdVUeyYZLDn0OQtbXbMhg)，访问 2026-10-08；[原论文](https://www.nature.com/articles/s41586-026-10363-4) 和 [作者代码](https://github.com/Woopsydaisy/Spatial-Human-Kidney-Map) 只作风格/定义核对，未复制原论文图或下载其 8.7 GB 数据。English summary: Parallel descriptive displays of unchanged real UMAP coordinates; no new embedding or biological certification.
