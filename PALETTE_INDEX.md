# 配色索引 / Palette index

期刊风格配色来自 ggsci，不是期刊官方要求。实际使用时应结合任务、文字标签与对比度检查色觉障碍（CVD）可读性；`not_certified` 表示尚未认证，`designed_for_common_CVD` 也不能替代具体图形检查。

![配色色卡](08_visualization/palettes/gallery/palette_swatches_v1.png)

| 配色 ID | 类型 | 建议数量 | 十六进制颜色 | 适合 | 不适合 | CVD 状态 | 来源 |
|---|---|---|---|---|---|---|---|
| npg_ggsci | 分类 | 6 | #E64B35FF, #4DBBD5FF, #00A087FF, #3C5488FF, #F39B7FFF, #8491B4FF, #91D1C2FF, #DC0000FF, #7E6148FF, #B09C85FF | 少量、彼此分离的分类 | 大量相邻分类或连续值 | not_certified | https://nanx.me/ggsci/ (包提供的期刊风格配色，不是期刊官方规定) |
| aaas_ggsci | 分类 | 6 | #3B4992FF, #EE0000FF, #008B45FF, #631879FF, #008280FF, #BB0021FF, #5F559BFF, #A20056FF, #808180FF, #1B1919FF | 分类概览 | 需要高可读性区分且没有文字／形状辅助 | not_certified | https://nanx.me/ggsci/ (包提供的期刊风格配色，不是期刊官方规定) |
| nejm_ggsci | 分类 | 5 | #BC3C29FF, #0072B5FF, #E18727FF, #20854EFF, #7876B1FF, #6F99ADFF, #FFDC91FF, #EE4C97FF | 少量临床组别 | 超过 8 类 | not_certified | https://nanx.me/ggsci/ (包提供的期刊风格配色，不是期刊官方规定) |
| lancet_ggsci | 分类 | 5 | #00468BFF, #ED0000FF, #42B540FF, #0099B4FF, #925E9FFF, #FDAF91FF, #AD002AFF, #ADB6B6FF, #1B1919FF | 分类分组 | 连续定量数值 | not_certified | https://nanx.me/ggsci/ (包提供的期刊风格配色，不是期刊官方规定) |
| jama_ggsci | 分类 | 5 | #374E55FF, #DF8F44FF, #00A1D5FF, #B24745FF, #79AF97FF, #6A6599FF, #80796BFF | 少量柔和色分类 | 超过 7 类 | not_certified | https://nanx.me/ggsci/ (包提供的期刊风格配色，不是期刊官方规定) |
| okabe_ito | 分类 | 8 | #E69F00, #56B4E9, #009E73, #F0E442, #0072B2, #D55E00, #CC79A7, #000000 | 最多 8 个离散分组，配合文字／形状 | 白底黄色细线或超过容量的分类 | designed_for_common_CVD; 检查具体任务对比度 | https://jfly.uni-koeln.de/color/ |
| viridis | 连续 | continuous | #440154FF, #414487FF, #2A788EFF, #22A884FF, #7AD151FF, #FDE725FF | 非负表达量／活性 | 围绕零的有方向比较 | designed_for_common_CVD | https://cran.r-project.org/package=viridisLite |
| cividis | 连续 | continuous | #00204DFF, #31446BFF, #666970FF, #958F78FF, #CBBA69FF, #FFEA46FF | 需要可读性的有序数值 | 没有顺序关系的分类 | designed_for_common_CVD | https://cran.r-project.org/package=viridisLite |
| blue_white_red | 发散 | 连续 | #2166AC, #F7F7F7, #B2182B | 以有意义的零为中心的带方向差异 | 没有正负方向的表达量 | not_certified; 增加方向标签 | https://colorbrewer2.org/ |

[配色代码](08_visualization/palettes/palettes.R) · [登记表](registry/palettes.yml) · [固定细胞与条件颜色](registry/celltype_colors.yml). 容量检查会拒绝超出分类颜色数量的请求，不对任意细胞身份插值造色。

## 在 R 中使用

在仓库根目录运行，需 `yaml`：

```r
source("08_visualization/palettes/palettes.R")
research_palette("okabe_ito", n = 5)
research_palette("viridis", n = 100)
```

分类颜色用于组别，连续颜色用于表达量，发散颜色用于有明确零点的正负差异。固定细胞类型颜色通过 `celltype_palette(labels)` 查询；未登记的标签会停止，先确认并登记，不随意改变已有颜色。

另登记项目专用 `GSE188217_fixed_broad_12`（12 类、未认证 CVD-safe），沿用既有口腔图鉴映射，完整类别/颜色见 [命名颜色表](08_visualization/UMAP/gallery/umap_fireworks_atlas.colors.csv) 与 [并列 UMAP 图例](08_visualization/UMAP/README.md)。上方历史色卡尚未重绘新增这一行；不要把此项目的第 N 个颜色随意配给别的数据标签，也不覆盖全局 `celltype_colors.yml`。
