# CellChat：细胞通讯推断与使用说明

方法 ID 为 `cellchat` 和 `cellchat_compare`。当前 **CANDIDATE · BLOCKED**：登记时没有安装 CellChat，也缺少已验证的代表性输入；以下命令是使用入口，不是已运行成功的证明。

## 适合解决什么问题

用非整合的对数归一化 RNA 表达和已审核的细胞标签，推断表达支持的配体–受体（LR）通讯假设，并查看通路、数量/强度和发送/接收角色。结果不能证明物理接触、因果信号或供者级处理效应。

## 输入和环境准备

从仓库根目录运行。R 环境需能加载 `CellChat`、`yaml`、`ragg`、`ComplexHeatmap`、`ggplot2` 及所选 CellChat 功能的依赖；脚本不会安装包。依赖版本见[构建记录](../../docs/validation/package_status.tsv)。

主工作流读取一个 RDS：

```r
# expression：基因 × 细胞、有限非负、对数归一化的 RNA 表达
# metadata：含细胞标签的数据框，行名为细胞条形码
stopifnot(identical(colnames(expression), rownames(metadata)))
dir.create("data", showWarnings = FALSE)
saveRDS(list(expression = expression, metadata = metadata),
        "data/cellchat_input.rds")
```

这里的变量必须由你准备的真实数据提供。不能用整合表达、缩放残差或缺少标签的细胞代替。每个通讯组的细胞数必须不少于 `min_cells`；标签含 NA 时会停止。

## 先改哪些配置

复制并编辑[default.yml](config/default.yml)，也可直接使用自己准备的配置路径；下表中的 key 保留英文，以便与脚本一致。

| key | 含义与需要确认的内容 |
|---|---|
| `input` / `output_dir` | 输入 RDS 和本地输出目录；路径相对仓库根目录 |
| `species` | 只能为 `human` 或 `mouse`，必须与数据/基因命名匹配 |
| `expression_scale` | 当前必须为 `lognormalized_RNA` |
| `group_column` | metadata 中的细胞标签列，默认 `celltype` |
| `average` | 传给 computeCommunProb 的表达汇总方法，默认 `triMean` |
| `population_size` | 是否考虑群体比例；默认 false，按捕获/分选设计决定 |
| `min_cells` / `nboot` / `seed` | 默认 10 / 100 / 42；分别控制最小组规模、置换次数和随机种子 |
| `db_annotation` | 可选数据库子集；null 表示不额外筛选 |
| `ppi_projection` | 默认 false；开启时做表达信息投影，不是 PPI/hub 网络分析 |
| `pathways` | 关注的通路名；必须存在于推断后的 netP 通路中；空列表跳过通路专项图 |
| `receiver_indices` | 只要 pathways 非空，脚本也会绘制 hierarchy 图，因此必须提供有依据的接收者索引，按 CellChat 标签顺序核对 |
| `pair` / `pair_pathway` | 可选单个 interaction_name 及其通路；需一起审核 |
| `sources` / `targets` | 两者都有值时绘制指定发送/接收群的气泡图 |
| `patterns` / `pattern_k` | 默认关闭；开启须明确给出数值 k ≥ 2，并先做 selectK/稳定性判断，脚本不自动选择 k |

## 运行单个数据集

```sh
Rscript scripts/run_method.R cellchat 04_cell_communication/CellChat/config/default.yml --allow-unvalidated
```

若另存了自己的配置，将命令中的配置路径替换为该文件。标志 `--allow-unvalidated` 仅表示你已阅读限制并允许尝试，不会让依赖、输入或结果自动通过验证。

脚本顺序为：建立对象和选择物种数据库 → 筛选信号数据 → 识别过表达基因/相互作用 → 可选 PPI 投影 → computeCommunProb → 小组过滤 → 通路聚合 → 网络汇总 → 中心性和图形输出。

## 比较两个条件

先分别完成两次 `cellchat` 推断，再将结果组织为具名列表；列表顺序就是 first/second：

```r
conditions <- list(
  control = readRDS("results/cellchat_control/object.rds"),
  treatment = readRDS("results/cellchat_treatment/object.rds")
)
saveRDS(conditions, "data/cellchat_conditions.rds")
```

上述路径为示例。输入必须恰好包含两个 CellChat 对象，细胞标签及 levels 顺序完全一致；数据库、表达处理、过滤和采样设计也应匹配。标签不一致时，当前脚本会停止，并要求按照官方不同组成教程明确使用 `liftCellChat` 对齐；脚本不代替你完成对齐。

编辑[compare.yml](config/compare.yml)的输入/输出，可选 sources/targets 和 embedding。默认 embedding 为 false；开启 functional/structural 相似性分析需要额外依赖、足够的通路和单独验证。

```sh
Rscript scripts/run_method.R cellchat_compare 04_cell_communication/CellChat/config/compare.yml --allow-unvalidated
```

差值方向为 **second − first**。LR 表先按两组已导出的相互作用合并，缺失概率置 0；这并不证明生物学上的相互作用不存在。通路比较使用 `do.stat = FALSE`，是描述性比较，不是供者层面的显著性检验。

## 去哪里找结果

| 模式 | 实际输出 |
|---|---|
| `cellchat` | object.rds；ligand_receptor.tsv；pathway.tsv；count_matrix.tsv；strength_matrix.tsv；plot_manifest.tsv；gallery/ 下 PNG/PDF |
| `cellchat_compare` | 合并对象 object.rds；differential_lr.tsv；plot_manifest.tsv；gallery/ 下比较图 |
| 两者共有 | sessionInfo.txt 和 run_metadata.yml，记录环境、配置和登记的验证范围 |

默认输出目录分别为 `results/cellchat`、`results/cellchat_comparison`。模式分析目前生成图，不单独保存 NMF 分解对象，也不把局部模式计算写回主工作流保存的对象。实际图路径以 plot_manifest.tsv 为准：例如气泡图文件 ID 为 `cc_bubble_v1`，通路图会带通路后缀；目录中的登记 ID 可能是概括名称。

## 已知限制与继续工作的起点

当前尚无端到端运行证据、原生图例或 Windows 兼容性证明。已有 API 审核针对稳定目标 v2.1.2，并参考开发文档 2.2.0.9001；仍需核对实际安装版本。原生置换 P 值不是供者级检验，也不是自动 BH 校正的 LR FDR。数量/强度依赖数据库、基因覆盖、标签和采样设计，图上差异需有独立实验支持。

下一步从一个已审核标签的代表性小数据集开始，确认依赖可加载、LR/通路表有效、PNG/PDF 可正常打开，并记录参数、版本和研究设计；之后再尝试两条件比较、模式及相似性分析。

继续查阅：[方法卡](METHOD_CARD.md)、[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例状态](gallery/README.md)、[官方文档](https://github.com/jinworks/CellChat)。
