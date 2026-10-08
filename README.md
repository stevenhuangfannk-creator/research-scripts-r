# Research Scripts R｜科研方法与绘图库 / Research methods library

以 R 为主的个人生物信息学方法库：从科研问题出发，找到方法、准备数据、运行可复用流程，再生成图表。方法与图形是主要入口，原始项目保留来源和验证上下文。

English summary: An R-first bioinformatics methods and visualization library. Start with the method index, check the input contract and validation scope, then configure and run the workflow. Chinese-first guidance retains English package names, commands and stable asset IDs.

## 从这里开始 / Start here

- [中文使用指南](docs/USAGE_ZH_CN.md)：第一次使用、依赖检查、配置参数、完整小示例与常见报错。
- [方法索引](METHOD_INDEX.md)：按“我想研究什么”选择方法或包。
- [图形画廊](GALLERY.md)：查看预览，找到对应代码、参数和可编辑矢量图。
- [配色索引](PALETTE_INDEX.md)：选择分类、连续或发散配色。
- [环境说明](docs/ENVIRONMENTS.md)：查看版本证据和未解决的依赖。

包名、函数名、文件路径、方法 ID 和配置字段保留英文，便于直接运行命令和查阅官方文档；用途、输入要求、参数解释和操作步骤采用中文。

## 功能与选择 / Capabilities and choices

| 想做的分析 | 中文说明入口 | 主要工具或内容 |
|---|---|---|
| 单细胞对象构建、质控、标准化、整合、聚类和注释 | [单细胞基础分析](01_scrna_core/README.md) | Seurat、scDblFinder、DecontX、Harmony |
| 找 cluster marker、按样本汇总 pseudobulk | [差异分析](02_differential_analysis/README.md) | Seurat；区分探索性 marker 与有生物学重复的条件比较 |
| 拟时序、轨迹和基因动态 | [细胞动态](03_cell_dynamics/README.md) | Monocle3；Slingshot、tradeSeq 为候选 |
| 细胞通讯、通讯角色、条件比较 | [细胞通讯](04_cell_communication/README.md) | CellChat；LIANA、NicheNet、CellPhoneDB 为候选 |
| GO/KEGG、GSEA、通路活性 | [通路与功能分析](05_pathway_function/README.md) | clusterProfiler、fgsea；其他方法见状态说明 |
| PPI、共表达、转录调控网络 | [基因网络](06_gene_networks/README.md) | 方法卡与候选规划，尚无可运行封装 |
| Bulk RNA-seq、生存分析、Cox、相关性和机器学习 | [Bulk 与临床分析](07_bulk_clinical_ml/README.md) | 部分流程可运行，部分仍为候选 |
| UMAP、表达图、热图、森林图等 | [绘图库](08_visualization/README.md) | R 图形函数、统一主题、配色和画廊 |
| Python 工具衔接 | [Python 桥接](09_python_bridge/README.md) | 独立环境规划；尚无可运行封装 |
| 可编辑科研示意图 | [示意图](10_scientific_schematics/README.md) | 原创 R/grid 组件、PNG/PDF/SVG 示例 |

## 快速开始 / Quick start

在仓库根目录打开终端，确认 `Rscript` 可用，且 `yaml`、`jsonlite` 已安装，然后运行：

```sh
Rscript scripts/create_demo_inputs.R
Rscript scripts/run_method.R correlation results/demo/correlation.yml
```

示例读取 R 内置 `iris` 数据，计算四个数值变量之间的相关性，将表格和运行信息写入 `results/demo/correlation/`。这是验证操作方式的小示例；混合物种的相关性可能受物种影响，不能直接解释为科研结论。Windows 找不到 `Rscript` 时见[中文指南](docs/USAGE_ZH_CN.md)。

## 使用自己的数据 / Use your own data

1. 在[方法索引](METHOD_INDEX.md)选择方法，阅读它的 `README.md`、`METHOD_CARD.md`（方法卡）和 `OUTPUT_CATALOG.md`（输出说明）。
2. 检查物种、表达量尺度、样本设计、依赖版本和已验证范围。
3. 复制该方法的配置到自己的工作目录，填写 `input`、`output_dir` 及方法参数。默认配置中的说明性占位文字必须替换。
4. 在仓库根目录运行 `Rscript scripts/run_method.R 方法ID 配置文件.yml`，或使用方法文档指定的直接函数接口。
5. 查看输出表、对象、`sessionInfo.txt` 和 `run_metadata.yml`；绘图时按画廊中的 Plot ID 查找代码。

```sh
Rscript scripts/resolve_asset.R method scrna_qc
Rscript scripts/resolve_asset.R plot umap_clean_v1
Rscript scripts/validate_library.R
```

## 验证范围与限制 / Validation and limitations

V1 登记 44 个方法入口：21 个有可执行脚本，23 个目前只有方法说明和规划。10 个方法有小型数据或内置数据上的限定范围 `PASS`，8 个记录为 `BLOCKED`，26 个为 `UNVALIDATED`。准确版本和各方法的具体证据见[登记表](registry/methods.yml)及[V1 交付报告](docs/V1_BUILD_REPORT.md)。

- `CANDIDATE`（候选）与 `VALIDATED`（限定范围已验证）描述方法成熟度。
- `PASS`、`UNVALIDATED`（未验证）、`BLOCKED`（受阻）与 `FAIL` 描述执行证据。
- 目前没有分析方法被设为通用 `DEFAULT`。能加载包、能运行示例、能生成图，分别对应不同范围的证据。
- CellChat、Monocle3 的本机完整执行和原生结果画廊仍受依赖与数据条件阻塞；汉化文档不改变它们的状态。
- 画廊包含 36 个实际渲染的示例，其中新增 [并列 UMAP 图例](08_visualization/UMAP/README.md)：真实 GSE188217 的烟花风格 atlas 与共享二维坐标的 3D 密度山峦，不替代旧默认图。`SYNTHETIC` 表示合成风格演示，不能作为实验结果。

## 维护与历史项目 / Maintenance and provenance

新增方法按[添加方法说明](docs/HOW_TO_ADD_METHOD.md)记录输入、参数、输出、来源和验证范围；自动化复用遵循[仓库使用规则](CODEX_RULES.md)。[登记表说明](registry/README.md)解释稳定 ID 和状态字段。

后续重要指南遵循[双语文档规则](AGENTS.md)：中文正文完整说明操作和决策，英文术语与命令保持可直接查阅和运行。

[历史项目索引](99_legacy_projects/README.md)保留三个原始项目的路径；[示例与验证上下文](90_examples/README.md)、[原始项目](projects/)、[论文复现](reproductions/README.md)保留各自的历史说明。原始数据、大型中间对象、凭据和本机包库不进入 Git。旧项目缺少输入或有硬编码路径时，应先阅读对应 README，再考虑运行。
