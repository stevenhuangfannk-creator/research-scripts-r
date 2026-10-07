# Monocle3 输出目录

这是已审核 API 的能力目录。当前执行状态 **BLOCKED**，没有已生成的原生分析图例。

| 图/输出 ID | 类别 | 科学问题/适用场景 | 图形 | 代码 | 需要审核的参数 | 正文/补充材料定位 | 证据 |
|---|---|---|---|---|---|---|---|
| `m3_cluster_trajectory_v1` | CORE / VISUAL | 聚类在学习到的表达状态图中如何分布？ | 聚类轨迹图 | [代码](scripts/visualize.R) | num_dim、聚类设置、partition/主图设置 | 正文概览 | BLOCKED / UNVALIDATED |
| `m3_celltype_trajectory_v1` | CORE / VISUAL | 审核过的细胞身份是否与图拓扑一致？ | 细胞类型轨迹图 | [代码](scripts/visualize.R) | celltype_column、标签证据 | 正文 | BLOCKED / UNVALIDATED |
| `m3_pseudotime_v1` | CORE / VISUAL / TABLE | 可达细胞相对有依据的根如何排序？ | 拟时序梯度图 | [代码](scripts/visualize.R) | root_cells、可达性、图拓扑 | 正文；公开根选择理由 | BLOCKED / UNVALIDATED |
| `m3_graph_nodes_v1` | CORE / VISUAL / TABLE | 主图的根、分支点和叶节点在哪里？ | 标记主图 | [代码](scripts/visualize.R) | minimal_branch_len、close_loop、根 | 补充材料中的拓扑审计 | BLOCKED / UNVALIDATED |
| `m3_backbone_v1` | OPTIONAL / VISUAL | 推断主图的骨架是什么？ | 小细胞标记的主图骨架 | [代码](scripts/visualize.R) | 线段大小、partition | 补充材料 | BLOCKED / UNVALIDATED |
| `m3_gene_expression_v1` | CORE / VISUAL | 所选标记基因在哪些状态发生变化？ | 基因表达叠加图 | [代码](scripts/visualize.R) | 明确唯一特征 ID；保留零表达 | 所选标记基因可放正文 | BLOCKED / UNVALIDATED |
| `m3_genes_pseudotime_v1` | CORE / VISUAL | 所选基因表达如何沿有限拟时序变化？ | 基因–拟时序曲线 | [代码](scripts/visualize.R) | 基因列表、根；排除的不可达细胞数 | 重点基因放正文，详细面板放补充材料 | BLOCKED / UNVALIDATED |
| `m3_gene_modules_v1` | ADVANCED / VISUAL / TABLE | 哪些图关联基因在细胞群间具有共同活性？ | 模块 × 细胞群热图 | [代码](scripts/gene_dynamics.R) | q_value、模块 resolution、细胞群 | 模块非主要结论时放补充材料 | BLOCKED / UNVALIDATED |
| `m3_branch_expression_v1` | ADVANCED / TABLE | 哪些基因与选定分支区域内部变化相关？ | 选定分支关联表；表达叠加需另行实现 | [代码](scripts/gene_dynamics.R) | 明确 branch_cells；graph_test(knn) | 补充材料；不是正式分支间对比 | BLOCKED / UNVALIDATED |
| `m3_publication_v1` | CORE / VISUAL | 如何清晰展示表达状态排序？ | 简洁拟时序图 | [代码](scripts/visualize.R) | 大小、主题；不添加无证据的时间标签 | 正文 | BLOCKED / UNVALIDATED |
| `m3_3d_v1` | OPTIONAL / VISUAL | 3D 拓扑是否比 2D 提供额外信息？ | 交互 3D 轨迹 | 规划能力；尚无脚本 | 另行重算三分量 UMAP/主图；plot_cells_3d | 仅在有信息且依赖就绪时使用补充材料 | BLOCKED / UNVALIDATED |
| `m3_cds_v1` | CORE / OBJECT | 能否检查和复用 CDS、主图与元数据？ | 对象与主图节点/边表 | [代码](scripts/workflow.R) | 对齐输入、版本、种子 | 对象本地存档；不提交 RDS | BLOCKED / UNVALIDATED |

## 解释与替代方法

拟时序不等于真实生物时间。根选择确定表达状态排序的方向，互不连通的 partition 可能产生无限拟时序；需报告不可达细胞数及根选择依据。主图分支/叶节点只是拓扑，不是实验已证明的命运决定。

Slingshot 沿聚类骨架拟合谱系曲线；tradeSeq 在给定拟时序和权重上检验表达趋势/谱系对比；RNA velocity 从 spliced/unspliced 数据估计动力学方向；CellRank 在核和终末状态假设下估计转移/命运概率。它们不是同一个统计量的互换版本。

CORE 为 CDS/主图/拟时序；OPTIONAL 包括尚未实现的 3D；ADVANCED 包括图关联和基因模块。正式分支比较或条件间轨迹对比需要独立验证的模型，V1 分支子集代码没有这些能力。动态工作流输出的 object.rds 是模块结果，不是 CDS；模块聚合数值矩阵尚未单独导出，分支表的基因 ID 保留问题见 [README](README.md)。

本次审核参考[轨迹教程](https://cole-trapnell-lab.github.io/monocle3/docs/trajectories/)、[基因动态教程](https://cole-trapnell-lab.github.io/monocle3/docs/differential/)、[作者仓库](https://github.com/cole-trapnell-lab/monocle3)、[Cao 等论文](https://doi.org/10.1038/s41586-019-0969-x)和[Packer 等论文](https://doi.org/10.1126/science.aax1971)。审核目标标签 v1.4.27 增加 BPCells 等依赖，执行前仍需验证编译和 namespace 加载。未生成的轨迹不能作为研究证据。
