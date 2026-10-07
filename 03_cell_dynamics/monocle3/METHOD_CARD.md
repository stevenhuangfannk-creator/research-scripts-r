# 方法卡

**方法 ID：** monocle3

**分类：** 03_cell_dynamics

**状态：** CANDIDATE

**语言：** R

**依赖包：** monocle3

**包版本：** 见[构建时依赖记录](../../docs/validation/package_status.tsv)。不能仅根据包是否存在推断其版本。

**最近验证：** 尚未验证。

**官方文档：** [monocle3](https://cole-trapnell-lab.github.io/monocle3/docs/trajectories/)

**原始论文：** [论文](https://doi.org/10.1038/s41586-019-0969-x)

**目的：** 从有生物学依据的根细胞出发，学习主图并对细胞的表达状态排序。

**生物学问题：** 从有生物学依据的根细胞出发，学习主图并对细胞的表达状态排序。

**适用条件：** RDS 保存的 list(counts, cell_metadata, gene_metadata)。counts 为基因 × 细胞计数矩阵；其列名须与 cell_metadata 行名完全同序、行名须与 gene_metadata 行名完全同序；gene_metadata 须含 gene_short_name。配置必须提供真实且有生物学依据的 root_cells 条形码。

**不适用条件与结论边界：** 拟时序不等于真实生物时间。互不连通的 partition 需要各自有依据的根细胞；主图分支只是表达状态拓扑假设，不能证明细胞命运。

**必需输入：** RDS 保存的 list(counts, cell_metadata, gene_metadata)。counts 为基因 × 细胞计数矩阵；其列名须与 cell_metadata 行名完全同序、行名须与 gene_metadata 行名完全同序；gene_metadata 须含 gene_short_name。配置必须提供真实且有生物学依据的 root_cells 条形码。

**可选输入：** 仅使用工作流/配置明确支持的可选字段。仅有 CANDIDATE 文档的方法，其输入约定仍是规划规范。

**主要参数：** num_dim = 30；root_cells = 必须人工判断；use_partition = true；close_loop = false；minimal_branch_len = 10；seed = 42。alignment_group 为可选元数据列名；celltype_column 和 genes 用于绘图。

**建议起点：** 文档中的参数起点不等于通用生物学默认值。包知名不构成升级为 DEFAULT 的依据。

**需要生物学判断的内容：** 拟时序不等于真实生物时间。互不连通的 partition 需要各自有依据的根细胞；主图分支只是表达状态拓扑假设，不能证明细胞命运。

**输出：** CDS；主图节点/边；拟时序与可达性表；轨迹与可选基因表达图。高级 monocle3_dynamics 输出见 README。

**优点：** 输入约定、来源和输出明确，复用范围小。

**局限：** 拟时序不等于真实生物时间。互不连通的 partition 需要各自有依据的根细胞；主图分支只是表达状态拓扑假设，不能证明细胞命运。

**假设：** 使用者必须确认上述输入和研究设计适用；拟时序不等于真实生物时间。互不连通的 partition 需要各自有依据的根细胞；主图分支只是表达状态拓扑假设，不能证明细胞命运。

**常见误区：** 拟时序不等于真实生物时间。互不连通的 partition 需要各自有依据的根细胞；主图分支只是表达状态拓扑假设，不能证明细胞命运。

**替代方案：** Slingshot 用聚类骨架拟合谱系曲线；tradeSeq 检验已给定轨迹上的表达趋势；RNA velocity 使用剪接动力学；CellRank 估计转移/命运概率。

**何时考虑替代方案：** Slingshot 用聚类骨架拟合谱系曲线；tradeSeq 检验已给定轨迹上的表达趋势；RNA velocity 使用剪接动力学；CellRank 估计转移/命运概率。

**已验证数据集：** 无。

**验证状态：** BLOCKED — 工作流未执行，所需依赖/数据尚未就绪。

**运行时间：** 小型演示不代表性能基准；在目标数据上记录耗时与线程设置。

**内存：** 尽量保留稀疏计数，不要将整个大型图谱转为稠密矩阵。大对象内存尚未做基准测试。

**可视化入口：** 先查[输出目录](OUTPUT_CATALOG.md)，再看已登记的图例。尚未实际生成并检查的图不能视为视觉推荐。

**推荐脚本：** [`workflow.R`](scripts/workflow.R)；具体运行和限制见 [README](README.md)。

**参考来源：** [官方文档](https://cole-trapnell-lab.github.io/monocle3/docs/trajectories/)；[原始论文](https://doi.org/10.1038/s41586-019-0969-x)。
