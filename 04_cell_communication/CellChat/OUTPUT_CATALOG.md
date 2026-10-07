# CellChat 输出目录

这是已审核 API 的能力目录。当前执行状态 **BLOCKED**；没有已生成的原生分析图例。下表登记 ID 是概括能力名，实际文件名以 plot_manifest.tsv 为准；例如 cc_celltype_bubble_v1 对应脚本的 cc_bubble_v1，通路图会附加通路后缀。

| 图/输出 ID | 类别 | 科学问题/适用场景 | 图形 | 代码 | 需要审核的参数 | 正文/补充材料定位 | 证据 |
|---|---|---|---|---|---|---|---|
| `cc_circle_count_v1` | CORE / VISUAL | 有多少受支持的 LR 相互作用连接细胞群？ | 环形图 | [代码](scripts/visualize.R) | min.cells、阈值、节点大小 | 正文概览；密集网络放补充材料 | BLOCKED / UNVALIDATED |
| `cc_circle_strength_v1` | CORE / VISUAL | 各方向汇总的模型相互作用强度是多少？ | 环形图 | [代码](scripts/visualize.R) | average、population.size、边尺度 | 正文概览；条件间保持匹配尺度 | BLOCKED / UNVALIDATED |
| `cc_count_heatmap_v1` | CORE / TABLE / VISUAL | 哪些发送 → 接收组合有更多模型相互作用？ | 发送–接收热图 | [代码](scripts/visualize.R) | 标签顺序、count 或 weight | 重点细胞类型放正文，其余放补充材料 | BLOCKED / UNVALIDATED |
| `cc_strength_heatmap_v1` | CORE / TABLE / VISUAL | 哪些发送 → 接收组合有较大汇总模型强度？ | 发送–接收热图 | [代码](scripts/visualize.R) | 物种数据库、聚合概率 | 重点假设可放正文 | BLOCKED / UNVALIDATED |
| `cc_celltype_bubble_v1` | OPTIONAL / VISUAL | 指定发送/接收群中有哪些受支持的 LR 对？ | 气泡图 | [代码](scripts/visualize.R) | sources、targets、signaling、pairLR.use | 有依据的少量重点组合可放正文 | BLOCKED / UNVALIDATED |
| `cc_pathway_circle_v1` | CORE / VISUAL | 哪些细胞群参与所选通路？ | 通路环形图 | [代码](scripts/visualize.R) | pathways、条件间共同边最大值 | 需有明确生物学依据 | BLOCKED / UNVALIDATED |
| `cc_pathway_hierarchy_v1` | OPTIONAL / VISUAL | 所选通路如何指向指定接收群？ | 层级图 | [代码](scripts/visualize.R) | 明确 receiver_indices；标签/边尺度 | 适合小型网络正文 | BLOCKED / UNVALIDATED |
| `cc_pathway_chord_v1` | OPTIONAL / VISUAL | 所选通路如何连接细胞群？ | 弦图 | [代码](scripts/visualize.R) | pathways、颜色、分组、间距 | 密集网络放补充材料 | BLOCKED / UNVALIDATED |
| `cc_pathway_heatmap_v1` | CORE / VISUAL | 所选通路的发送 → 接收强度模式是什么？ | 热图 | [代码](scripts/visualize.R) | 通路、相同尺度与标签顺序 | 重点通路可放正文 | BLOCKED / UNVALIDATED |
| `cc_lr_circle_v1` | CORE / VISUAL | 哪些细胞群支持单个 LR 相互作用？ | LR 环形图 | [代码](scripts/visualize.R) | pair、pair_pathway、阈值 | 需独立验证支持 | BLOCKED / UNVALIDATED |
| `cc_lr_table_v1` | CORE / TABLE | 哪些 LR 对有模型概率和原生置换支持？ | 可排序表/气泡图 | [代码](scripts/workflow.R) | 物种数据库、nboot、average | 完整表放补充材料 | BLOCKED / UNVALIDATED |
| `cc_centrality_v1` | ADVANCED / VISUAL | 哪些细胞群是模型发送者、接收者、中介或影响者？ | 中心性角色热图 | [代码](scripts/visualize.R) | netP 中心性、所选通路 | 角色非核心结论时放补充材料 | BLOCKED / UNVALIDATED |
| `cc_role_scatter_v1` | CORE / VISUAL | 哪些细胞群的模型 outgoing/incoming 强度较大？ | 角色散点图 | [代码](scripts/visualize.R) | 共同轴/点尺度、信号子集 | 正文概览；避免因果标签 | BLOCKED / UNVALIDATED |
| `cc_outgoing_heatmap_v1` | CORE / VISUAL | 各发送群对应哪些通路？ | 信号角色热图 | [代码](scripts/visualize.R) | 通路选择、细胞顺序 | 按信息密度决定正文/补充材料 | BLOCKED / UNVALIDATED |
| `cc_incoming_heatmap_v1` | CORE / VISUAL | 各接收群对应哪些通路？ | 信号角色热图 | [代码](scripts/visualize.R) | 通路选择、细胞顺序 | 按信息密度决定正文/补充材料 | BLOCKED / UNVALIDATED |
| `cc_contribution_v1` | CORE / VISUAL | 哪些 LR 对对所选通路的估计贡献较大？ | 贡献条形图 | [代码](scripts/visualize.R) | 通路、source/target 筛选 | 机制假设参考，不能替代扰动证据 | BLOCKED / UNVALIDATED |
| `cc_pathway_rank_v1` | CORE / VISUAL | 总模型通路强度如何排序？ | 排序条形图 | [代码](scripts/visualize.R) | measure、通路/资源版本 | 发现性排序放补充材料 | BLOCKED / UNVALIDATED |
| `cc_pattern_outgoing_heatmap_v1` | ADVANCED / VISUAL | 哪些发送群共享潜在信号模式？ | NMF 模式热图 | [代码](scripts/visualize.R) | pattern_k 需经 selectK 与敏感性审查 | 补充材料；评估稳定性 | BLOCKED / UNVALIDATED |
| `cc_pattern_incoming_heatmap_v1` | ADVANCED / VISUAL | 哪些接收群共享潜在信号模式？ | NMF 模式热图 | [代码](scripts/visualize.R) | pattern_k、NMF 稳定性 | 补充材料 | BLOCKED / UNVALIDATED |
| `cc_pattern_outgoing_river_v1` | ADVANCED / VISUAL | 发送群、模式和通路如何相连？ | 河流/桑基图 | [代码](scripts/visualize.R) | pattern_k、贡献阈值 | 补充材料 | BLOCKED / UNVALIDATED |
| `cc_pattern_incoming_river_v1` | ADVANCED / VISUAL | 接收群、模式和通路如何相连？ | 河流/桑基图 | [代码](scripts/visualize.R) | pattern_k、贡献阈值 | 补充材料 | BLOCKED / UNVALIDATED |
| `cc_pattern_outgoing_dot_v1` | ADVANCED / VISUAL | 哪些发送群–模式/通路贡献占主导？ | 模式点图 | [代码](scripts/visualize.R) | 阈值、通路/细胞群子集 | 补充材料 | BLOCKED / UNVALIDATED |
| `cc_pattern_incoming_dot_v1` | ADVANCED / VISUAL | 哪些接收群–模式/通路贡献占主导？ | 模式点图 | [代码](scripts/visualize.R) | 阈值、通路/细胞群子集 | 补充材料 | BLOCKED / UNVALIDATED |
| `cc_compare_total_count_v1` | COMPARISON / VISUAL | 条件间汇总相互作用数量如何不同？ | 比较条形图 | [代码](scripts/compare.R) | 相同数据库/标签/过滤；first/second 顺序 | 正文描述性比较 | BLOCKED / UNVALIDATED |
| `cc_compare_total_weight_v1` | COMPARISON / VISUAL | 条件间汇总模型强度如何不同？ | 比较条形图 | [代码](scripts/compare.R) | 相同平均方法/population.size、采样设计 | 正文描述性比较 | BLOCKED / UNVALIDATED |
| `cc_diff_circle_count_v1` | COMPARISON / VISUAL | 哪些方向的相互作用数量增加/减少？ | 差异环形图 | [代码](scripts/compare.R) | second − first、数量尺度 | 小型网络放正文，密集网络放补充材料 | BLOCKED / UNVALIDATED |
| `cc_diff_circle_weight_v1` | COMPARISON / VISUAL | 哪些方向的模型强度增加/减少？ | 差异环形图 | [代码](scripts/compare.R) | second − first、匹配尺度 | 重点假设可放正文 | BLOCKED / UNVALIDATED |
| `cc_diff_heatmap_count_v1` | COMPARISON / VISUAL | 发送/接收数量变化集中在哪里？ | 差异热图 | [代码](scripts/compare.R) | 标签顺序、共同尺度 | 正文或补充材料 | BLOCKED / UNVALIDATED |
| `cc_diff_heatmap_weight_v1` | COMPARISON / VISUAL | 发送/接收强度变化集中在哪里？ | 差异热图 | [代码](scripts/compare.R) | 标签顺序、共同尺度 | 正文或补充材料 | BLOCKED / UNVALIDATED |
| `cc_differential_lr_v1` | COMPARISON / TABLE / VISUAL | 指定细胞方向中的 LR 概率如何变化？ | 增加/减少气泡图与差值表 | [代码](scripts/compare.R) | sources/targets、max.dataset、缺失处理 | 重点集合放正文，完整表放补充材料 | BLOCKED / UNVALIDATED |
| `cc_role_change_v1` | COMPARISON / VISUAL | 细胞群在各通路的 incoming/outgoing 角色是否改变？ | 信号变化散点图 | [代码](scripts/compare.R) | idents.use、被排除通路 | 需有生物学支持 | BLOCKED / UNVALIDATED |
| `cc_compare_pathways_v1` | COMPARISON / VISUAL | 哪些通路的整体模型强度不同？ | 通路比较排序 | [代码](scripts/compare.R) | 描述性 do.stat=FALSE；匹配设计 | 重点通路可放正文；不宣称供者级显著性 | BLOCKED / UNVALIDATED |
| `cc_embedding_functional_v1` | ADVANCED / COMPARISON / VISUAL | 哪些信号网络具有相似的细胞角色结构？ | 功能网络流形 | [代码](scripts/compare.R) | 一致细胞标签、核/嵌入、通路数量 | 补充材料/探索性 | BLOCKED / UNVALIDATED |
| `cc_embedding_structural_v1` | ADVANCED / COMPARISON / VISUAL | 哪些网络拓扑相似？ | 结构网络流形 | [代码](scripts/compare.R) | 拓扑、通路覆盖、嵌入敏感性 | 补充材料/探索性 | BLOCKED / UNVALIDATED |
| `cc_object_v1` | CORE / OBJECT | 能否复用并审计完整推断模型？ | 对象，无图 | [代码](scripts/workflow.R) | 包/数据库版本和配置 | 本地存档；不提交 RDS | BLOCKED / UNVALIDATED |

## 解释与版本边界

CORE 包括 LR 结果表、对象中的模型概率数组、数量/强度矩阵和通路网络。OPTIONAL 提供重点发送/接收群及 hierarchy/chord 视图；ADVANCED 包括中心性、NMF 模式和通讯流形；COMPARISON 使用分别推断的模型及明确 first/second 顺序。VISUAL/TABLE/OBJECT 分类如表所示，对象和完整矩阵留在 Git 之外。

原生置换 P 值不是供者级处理检验，也不能自动称为 BH 校正的 LR FDR。数量/强度依赖数据库、表达覆盖、标签和采样设计。功能相似性需匹配细胞角色，结构相似性比较拓扑；两种嵌入均不能证明时间或因果进展。pattern_k 需 selectK 和稳定性审查，当前脚本不自动选择 k。

PPI 投影是可选的表达信息投影/平滑步骤。传统 STRING/蛋白相互作用拓扑、hub 基因及 CytoHubba MCC 属于 [06_gene_networks/PPI](../../06_gene_networks/PPI/README.md)。

本次 API 审核参考[作者仓库](https://github.com/jinworks/CellChat)、[单数据集教程](https://github.com/jinworks/CellChat/blob/main/tutorial/CellChat-vignette.Rmd)、[比较教程](https://github.com/jinworks/CellChat/blob/main/tutorial/Comparison_analysis_of_multiple_datasets.Rmd)、[原始论文](https://doi.org/10.1038/s41467-021-21246-9)及[协议](https://doi.org/10.1038/s41596-024-01045-4)。审核时稳定目标为 v2.1.2，参考开发文档为 2.2.0.9001；API 审核不能证明 Windows 运行兼容性，旧代码 igraph 补丁未引入。实际运行、配置及输出限制见 [README](README.md)。
