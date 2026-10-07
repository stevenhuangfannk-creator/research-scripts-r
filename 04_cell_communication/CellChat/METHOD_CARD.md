# 方法卡

**方法 ID：** cellchat

**分类：** 04_cell_communication

**状态：** CANDIDATE

**语言：** R

**依赖包：** CellChat

**包版本：** 见[构建时依赖记录](../../docs/validation/package_status.tsv)。不能仅根据包是否存在推断其版本。

**最近验证：** 尚未验证。

**官方文档：** [CellChat](https://github.com/jinworks/CellChat)

**原始论文：** [论文](https://doi.org/10.1038/s41467-021-21246-9)

**目的：** 推断并可视化由表达数据支持的配体–受体细胞通讯假设。

**生物学问题：** 推断并可视化由表达数据支持的配体–受体细胞通讯假设。

**适用条件：** RDS 保存的 list(expression, metadata)。expression 为基因 × 细胞的非整合、对数归一化 RNA 表达矩阵；metadata 行名须与 expression 列名完全同序，且含 group_column 指定的细胞标签。使用匹配的 human 或 mouse 数据库。

**不适用条件与结论边界：** 推断不能证明物理接触、因果信号或供者层面的处理效应。population_size 取决于捕获/分选设计；ppi_projection 是可选的信息投影步骤。原生置换 P 值不能直接视为供者级检验或 BH 校正的 LR FDR。

**必需输入：** RDS 保存的 list(expression, metadata)。expression 为基因 × 细胞的非整合、对数归一化 RNA 表达矩阵；metadata 行名须与 expression 列名完全同序，且含 group_column 指定的细胞标签。使用匹配的 human 或 mouse 数据库。

**可选输入：** 仅使用工作流/配置明确支持的可选字段。仅有 CANDIDATE 文档的方法，其输入约定仍是规划规范。

**主要参数：** species = human / mouse；expression_scale = lognormalized_RNA；average = triMean；population_size = false；min_cells = 10；nboot = 100；seed = 42；ppi_projection = false。路径、接收者、配体–受体对和 pattern_k 须按研究问题选择。

**建议起点：** 文档中的参数起点不等于通用生物学默认值。包知名不构成升级为 DEFAULT 的依据。

**需要生物学判断的内容：** 推断不能证明物理接触、因果信号或供者层面的处理效应。population_size 取决于捕获/分选设计；ppi_projection 是可选的信息投影步骤。原生置换 P 值不能直接视为供者级检验或 BH 校正的 LR FDR。

**输出：** LR 模型概率及原生置换 P 值；数量/强度矩阵；通路聚合；网络角色和可选模式图。cellchat_compare 输出见 README。

**优点：** 输入约定、来源和输出明确，复用范围小。

**局限：** 推断不能证明物理接触、因果信号或供者层面的处理效应。population_size 取决于捕获/分选设计；ppi_projection 是可选的信息投影步骤。原生置换 P 值不能直接视为供者级检验或 BH 校正的 LR FDR。

**假设：** 使用者必须确认上述输入和研究设计适用；推断不能证明物理接触、因果信号或供者层面的处理效应。population_size 取决于捕获/分选设计；ppi_projection 是可选的信息投影步骤。原生置换 P 值不能直接视为供者级检验或 BH 校正的 LR FDR。

**常见误区：** 推断不能证明物理接触、因果信号或供者层面的处理效应。population_size 取决于捕获/分选设计；ppi_projection 是可选的信息投影步骤。原生置换 P 值不能直接视为供者级检验或 BH 校正的 LR FDR。

**替代方案：** 需要配体 → 靶基因响应解释时考虑 NicheNet；CellPhoneDB/LIANA 提供互补的 LR 证据。

**何时考虑替代方案：** 需要配体 → 靶基因响应解释时考虑 NicheNet；CellPhoneDB/LIANA 提供互补的 LR 证据。

**已验证数据集：** 无。

**验证状态：** BLOCKED — 工作流未执行，所需依赖/数据尚未就绪。

**运行时间：** 小型演示不代表性能基准；在目标数据上记录耗时与线程设置。

**内存：** 尽量保留稀疏计数，不要将整个大型图谱转为稠密矩阵。大对象内存尚未做基准测试。

**可视化入口：** 先查[输出目录](OUTPUT_CATALOG.md)，再看已登记的图例。尚未实际生成并检查的图不能视为视觉推荐。

**推荐脚本：** [`workflow.R`](scripts/workflow.R)；具体运行和限制见 [README](README.md)。

**参考来源：** [官方文档](https://github.com/jinworks/CellChat)；[原始论文](https://doi.org/10.1038/s41467-021-21246-9)。
