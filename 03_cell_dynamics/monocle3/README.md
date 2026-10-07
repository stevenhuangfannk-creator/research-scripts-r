# Monocle3：轨迹、拟时序与基因动态

方法 ID 为 `monocle3` 和 `monocle3_dynamics`。当前 **CANDIDATE · BLOCKED**：登记时没有安装 monocle3，尚无端到端执行或原生图例证据。

## 适合解决什么问题

学习表达状态的主图，并从有生物学依据的根细胞出发排序。拟时序不是经过的真实时间，图分支也不能证明命运决定。根细胞选择决定方向，互不连通的 partition 可能需要各自的合理根细胞。

## 输入和环境准备

从仓库根目录运行。R 环境需能加载 `monocle3`、`igraph`、`SummarizedExperiment`、`yaml`、`ggplot2`、`ragg` 及所用功能的依赖；脚本不安装包。目标标签 v1.4.27 涉及 BPCells 等依赖，编译及 namespace 加载需要在实际环境确认。

保存如下 RDS 输入：

```r
# counts：基因 × 细胞计数矩阵；metadata 行名须和矩阵完全同序
stopifnot(
  identical(colnames(counts), rownames(cell_metadata)),
  identical(rownames(counts), rownames(gene_metadata)),
  "gene_short_name" %in% names(gene_metadata)
)
dir.create("data", showWarnings = FALSE)
saveRDS(list(counts = counts, cell_metadata = cell_metadata,
             gene_metadata = gene_metadata), "data/monocle_input.rds")
```

这些变量必须来自你准备的数据；建议先选择生物学上连通、与研究问题相关的谱系。使用可追溯的特征 ID，避免重复 gene_short_name 导致基因选择歧义。

## 主轨迹配置

复制并编辑[default.yml](config/default.yml)，确认下列 key：

| key | 需要确认的内容 |
|---|---|
| `input` / `output_dir` | 输入 RDS 和本地输出；路径相对仓库根目录 |
| `root_cells` | 默认空列表，必须填真实条形码并说明生物学依据；脚本不会交互选择或任意指定根 |
| `celltype_column` | 用于轨迹图的元数据列，默认 celltype；须实际存在 |
| `num_dim` | 预处理维数，默认 30，需按数据规模审查 |
| `alignment_group` | 可选批次/对齐分组列；null 时不调用 align_cds |
| `use_partition` / `close_loop` | 默认 true / false；影响图拓扑，应做敏感性分析 |
| `minimal_branch_len` | 默认 10，影响短分支保留 |
| `seed` | 默认 42；UMAP 固定 cores = 1 且 umap.fast_sgd = FALSE |
| `genes` | 可选基因名/特征 ID 列表；必须能唯一匹配，空列表跳过基因专项图 |

这里没有对外暴露聚类 resolution 的配置 key；不要添加无效参数并假定脚本会使用。

```sh
Rscript scripts/run_method.R monocle3 03_cell_dynamics/monocle3/config/default.yml --allow-unvalidated
```

若另存自己的配置，替换命令中的路径。运行顺序为 new_cell_data_set → preprocess_cds → 可选 align_cds → UMAP → cluster_cells → learn_graph → order_cells → 可达性/图节点审计和图形输出。

无法从指定根到达的细胞会保留无限拟时序并给出警告，不会替换为 0；基因–拟时序曲线仅使用有限拟时序细胞。

## 下游基因动态

主轨迹成功后，[dynamics.yml](config/dynamics.yml)读取其 `object.rds`（cell_data_set）。确认 cores、q_value、resolution、seed 和 celltype_column；默认 q_value = 0.05、resolution = 0.01、cores = 1。

```sh
Rscript scripts/run_method.R monocle3_dynamics 03_cell_dynamics/monocle3/config/dynamics.yml --allow-unvalidated
```

脚本先对 principal_graph 做 graph_test（Moran 图关联），选择 q_value 达标基因，再 find_gene_modules、按 celltype_column 聚合并画模块热图。少于两个图关联基因时会停止。

可选 `branch_cells` 必须是从明确选择的分支子图得到的真实条形码。提供后，脚本只对子集使用 `graph_test(neighbor_graph = "knn")`；这是分支区域内部变化的探索性关联，**不是正式分支间对比、Monocle2 BEAM 或条件间轨迹检验**。

## 实际输出

| 模式 | 实际输出 |
|---|---|
| `monocle3` | object.rds（CDS）；pseudotime.tsv（cell、pseudotime、reachable）；graph_nodes.tsv；graph_edges.tsv；plot_manifest.tsv；gallery/ 下 PNG/PDF |
| `monocle3_dynamics` | object.rds（模块结果，不是 CDS）；graph_association.tsv；gene_modules.tsv；branch_association.tsv；gallery/m3_gene_modules_v1.png 和 .pdf |
| 两者共有 | sessionInfo.txt 和 run_metadata.yml |

默认目录分别为 `results/monocle3` 与 `results/monocle3_dynamics`。动态脚本在内存中计算了模块 × 细胞群聚合矩阵，但当前不单独导出该数值矩阵，也不返回图形 manifest。未设置 branch_cells 时 branch_association 为空。当前分支表未显式写入 gene 列，而统一导出关闭 row.names，可能丢失基因标识；解释该输出前需要检查并修正这个已有问题。

## 限制与继续工作的起点

`--allow-unvalidated` 允许尝试候选流程，不表示分析通过验证。应先确认 namespace、CDS 输入对齐、非空主图、可达细胞数及实际 PNG/PDF，再比较多个有依据的根细胞和图参数。当前没有实现 3D 轨迹；该能力需单独重算三分量 UMAP/图及使用 plot_cells_3d。正式分支/条件比较需要另行建立并验证模型。

下一步先准备一条连通谱系的计数、标签、基因信息和根细胞依据，从主轨迹开始；确认主轨迹可解释后，再运行基因动态。

继续查阅：[方法卡](METHOD_CARD.md)、[输出目录](OUTPUT_CATALOG.md)、[输入与验证](examples/README.md)、[图例状态](gallery/README.md)、[官方轨迹教程](https://cole-trapnell-lab.github.io/monocle3/docs/trajectories/)。
