# 中文使用指南 / Usage guide

这份指南帮助你确认每个方法需要什么数据、怎么配置、怎么运行以及输出在哪里。步骤依据本库现有脚本，包名、参数和方法 ID 保留英文。

## 1. 找到要用的方法 / Choose a method

先看[方法索引](../METHOD_INDEX.md)。例如“过滤低质量细胞”对应 `scrna_qc`，“批次整合”对应 `harmony`，“细胞通讯”对应 `cellchat`。进入方法目录，依次查看：

| 文件 | 应该确认什么 |
|---|---|
| `README.md` | 方法用途与实际运行步骤 |
| `METHOD_CARD.md` | 输入、表达量尺度、参数、适用边界和依赖 |
| `OUTPUT_CATALOG.md` | 输出表／对象／图分别代表什么 |
| `config/default.yml` 等 | 脚本识别的参数名称与默认值 |
| `examples/README.md`、`gallery/README.md` | 已验证的数据范围、图形状态 |
| `references.yml` | 官方来源与目标版本 |

准确路径和状态可以在仓库根目录查询：

```sh
Rscript scripts/resolve_asset.R method scrna_qc
```

如果登记项 `script: null`，本库尚无可执行封装。`--allow-unvalidated` 只能解除已有未验证流程的运行限制，不能运行尚未实现的方法。

## 2. 准备 R 与工作目录 / Environment and working directory

使用自己的 R／RStudio，下载或克隆仓库。在终端进入包含 `README.md`、`scripts/` 和 `registry/` 的仓库根目录；RStudio 用户也可以把工作目录设到这里。包版本见[环境说明](ENVIRONMENTS.md)。

示例命令默认 `Rscript` 已在 PATH 中。Windows 提示“无法识别 Rscript”时，可在 PowerShell 使用完整路径。以下路径对应本机已存在的 R 4.3.1，其他电脑需替换为实际安装位置：

```powershell
& 'C:\Program Files\R\R-4.3.1\bin\Rscript.exe' scripts/resolve_asset.R method scrna_qc
```

后面的所有 `Rscript` 命令也可采用这一写法。阅读中文说明不需要安装插件。

通用命令读取配置需要 `yaml`；小示例生成脚本还需要 `jsonlite`。`Seurat`、`survival`、`CellChat` 等按所选方法分别准备。已有包也应检查 namespace 是否能加载，见[环境检查代码](ENVIRONMENTS.md)。

## 3. 跑通完整的小示例 / Run the small example

这个示例无需外部科研数据，使用 R 自带 `iris`。在仓库根目录执行：

```sh
Rscript scripts/create_demo_inputs.R
Rscript scripts/run_method.R correlation results/demo/correlation.yml
```

第一条创建 `results/demo/iris.csv` 和 `results/demo/correlation.yml`；第二条调用 `correlation` 流程。示例配置相当于：

```yaml
input: results/demo/iris.csv
output_dir: results/demo/correlation
variables: [Sepal.Length, Sepal.Width, Petal.Length, Petal.Width]
method: pearson
missing: error
```

输出在 `results/demo/correlation/`：

| 文件 | 用途 |
|---|---|
| `correlations.tsv` | 六对变量的相关系数、样本量、P 值、BH 校正值及支持的置信区间 |
| `sessionInfo.txt` | 本次运行的 R、平台和包环境 |
| `run_metadata.yml` | 方法 ID、实际配置、生成时间和登记的验证范围 |

`method: spearman` 改为秩相关；`missing: error` 遇缺失值停止，`pairwise` 按变量对排除缺失并记录数量。Spearman 分支当前不提供置信区间。示例混合了不同鸢尾物种，关联可能受物种混杂，主要用于练习运行。

## 4. 换成自己的数据 / Configure your own input

复制所选方法的配置到自己的本地工作目录，再修改参数。许多默认配置含提示性占位文字，必须替换为真实值；不要直接运行，也不要套用别人的样本字段和生物学选择。

| 需要修改的内容 | 含义 |
|---|---|
| `input` | 输入文件；通用命令支持 `.rds`、`.csv`、`.tsv` |
| `output_dir` | 本次结果目录；每次分析使用单独目录，避免覆盖已有结果 |
| 方法专属参数 | 如质控阈值、样本列、物种、轨迹起点；只使用脚本支持的字段 |

相对路径从仓库根目录解析。YAML 路径推荐正斜杠，如 `data/my_object.rds`，含空格的路径可以加引号。输入原始数据不被修改，结果写入配置的输出目录；重复使用同一目录会覆盖同名生成文件。

通用运行形式：

```sh
Rscript scripts/run_method.R scrna_qc local_config/qc.yml
```

已有但未验证的流程会主动停止。阅读方法卡、确认环境和输入适配后，可显式运行：

```sh
Rscript scripts/run_method.R cellchat local_config/cellchat.yml --allow-unvalidated
```

该参数不代表流程已经验证，也不会安装缺失包。`local_config/...` 是你自己准备的路径，不是仓库已经附带的文件。

通用命令仅在 `result$object` 非 `NULL` 时保存 `object.rds`，把 `result$tables` 中每张表保存为同名 `.tsv`，并保存运行环境和元数据。相关性与 cluster marker 流程只返回表格，不生成 `object.rds`。某些方法还有专属文件或后续绘图脚本，详见对应中文说明。

## 5. 常用包在本库里怎么用 / Package entry points

| 工具／方法 | 需要准备什么 | 中文说明 |
|---|---|---|
| Seurat 对象构建 | 含 `counts` 与 `metadata` 的 R 列表；基因×细胞计数矩阵与对齐的 metadata | [构建对象](../01_scrna_core/data_ingestion/README.md) |
| Seurat 质控 | 含 RNA counts 的对象；物种匹配的线粒体／核糖体基因模式与阈值 | [质控](../01_scrna_core/quality_control/README.md) |
| LogNormalize／SCTransform | 原始 counts 对象；选择一条标准化路线 | [LogNormalize](../01_scrna_core/normalization/lognormalize/README.md)、[SCTransform](../01_scrna_core/normalization/SCTransform/README.md) |
| Harmony | 已有 PCA 的对象与 metadata 批次列；本库聚类脚本固定使用 PCA，不能自动衔接 Harmony | [Harmony](../01_scrna_core/batch_integration/Harmony/README.md) |
| scDblFinder | 含原始 counts 的 Seurat 对象与实际建库 capture 列；capture 不自动等于生物学样本 | [双细胞](../01_scrna_core/doublet_detection/scDblFinder/README.md) |
| DecontX | `list(counts, metadata, backgrounds)`；metadata 含 capture 列，backgrounds 可选 | [去污染](../01_scrna_core/ambient_rna/DecontX/README.md) |
| CellChat | 标准化表达、细胞分组、物种；比较时准备各条件对象列表 | [CellChat](../04_cell_communication/CellChat/README.md) |
| Monocle3 | 按流程约定的细胞对象；生物学依据明确的起始细胞 | [轨迹与基因动态](../03_cell_dynamics/monocle3/README.md) |
| clusterProfiler／fgsea | ORA 的基因与背景集合，或 GSEA 的有名排序向量与通路集合 | [GO／KEGG](../05_pathway_function/GO_KEGG/README.md)、[GSEA](../05_pathway_function/GSEA/README.md) |
| survival | 随访时间、明确的 0/1 事件、分组或协变量表 | [KM](../07_bulk_clinical_ml/survival/README.md)、[Cox](../07_bulk_clinical_ml/Cox/README.md) |
| stats 相关性 | 行为观测、列为数值变量的表；指定方法与缺失值策略 | [相关性](../07_bulk_clinical_ml/correlation/README.md) |
| WGCNA／SCENIC／Python 工具 | 先阅读方法卡；本库尚无可运行封装 | [基因网络](../06_gene_networks/README.md)、[Python 桥接](../09_python_bridge/README.md) |

这些说明面向本库封装，不代替包的完整手册。缺依赖、未验证或尚无脚本的方法，保持原登记状态。

## 6. 找到并复用图形 / Reuse plots

从[画廊](../GALLERY.md)选择 Plot ID，再查询代码和数据：

```sh
Rscript scripts/resolve_asset.R plot umap_clean_v1
Rscript scripts/resolve_asset.R palette okabe_ito
```

查看函数输入，将自己的分析结果整理成对应字段后调用。绘图函数绘制已有结果，不替你计算 UMAP、差异表达或通讯。

画廊生成器 `scripts/generate_gallery.R` 使用固定演示数据，依赖已生成的 smoke 对象，也会写入已有画廊和登记表。只想查看图时，直接打开预览；用自己的数据时调用对应函数。图中英文标签保留原样，需要中文图标签时应准备中文字体并重新检查导出。

## 7. 常见问题 / Troubleshooting

| 提示／现象 | 如何处理 |
|---|---|
| `Unknown or duplicate method ID` | 从登记表复制准确 ID，注意小写、下划线和拼写 |
| `This method has no executable workflow` | 当前只有方法卡和规划，不能通过参数强制运行 |
| `Workflow is unvalidated` | 先阅读限制，确认适配后才加 `--allow-unvalidated` |
| 找不到配置、脚本或数据 | 确认工作目录是仓库根目录，并核对相对路径 |
| `there is no package called ...` | 准备所选方法的依赖 |
| 包已安装但加载失败 | 检查实际 R／包版本及 namespace 兼容性 |
| 找不到 metadata 列 | 按自己的列名修改配置，不补造样本或细胞标签 |
| 没有图或只产生表 | 查输出说明；通用命令不会自动执行所有绘图脚本 |

维护方法库时运行 `Rscript scripts/validate_library.R` 检查路径、结构和晋升规则。`scripts/smoke_tests.R` 会生成演示对象并更新已有验证记录，应在依赖已准备好且确实要重新验证时使用。
