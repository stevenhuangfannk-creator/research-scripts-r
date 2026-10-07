# 方法卡：PPI 蛋白互作网络

**方法 ID:** ppi

**分类:** 06_gene_networks

**状态:** CANDIDATE

**语言:** R

**包 / 工具:** igraph / ggraph / STRING

**包版本:** 见[包加载与版本证据](../../docs/validation/package_status.tsv)；不能仅因包已安装就推断版本或方法可用。

**最近验证:** 尚未验证

**官方文档:** [igraph / ggraph / STRING 官方文档](https://string-db.org/help/api/)

**原始论文:** 从官方文档核对引用；本次整理未独立认证论文元数据。

**目的:** 分析具有实际互作证据的蛋白网络，并报告网络拓扑。

**科研问题:** 分析具有实际互作证据的蛋白网络，并报告网络拓扑。

**适用情况:** 完成物种特异映射的蛋白 ID，以及具有来源信息的 STRING 互作边。

**不适用情况 / 使用边界:** MCC 需要明确的 CytoHubba 实现，不能用 degree 代替；CellChat 的 PPI 投影属于另一类操作。

**必需输入:** 完成物种特异映射的蛋白 ID，以及具有来源信息的 STRING 互作边。

**可选输入:** 当前输入和参数是规划规范；尚无 workflow.R 支持可选字段。

**主要参数:** review_required = 物种；STRING 评分；证据通道；是否为有向网络。

**推荐起点:** 文档中的参数只是起点，应结合具体数据审查。知名包不自动获得 DEFAULT 状态。

**需要科研判断的参数:** MCC 需要明确的 CytoHubba 实现，不能用 degree 代替；CellChat 的 PPI 投影属于另一类操作。 具体配置见 [README](README.md)。

**输出:** 互作网络；度（degree）/ 介数（betweenness）；枢纽节点表；Cytoscape 导出。这些是拟实现的目标输出，当前没有执行结果。

**优势:** 输入要求、来源和目标输出明确，方法范围较小。

**局限:** MCC 需要明确的 CytoHubba 实现，不能用 degree 代替；CellChat 的 PPI 投影属于另一类操作。

**假设:** MCC 需要明确的 CytoHubba 实现，不能用 degree 代替；CellChat 的 PPI 投影属于另一类操作。

**常见问题:** MCC 需要明确的 CytoHubba 实现，不能用 degree 代替；CellChat 的 PPI 投影属于另一类操作。

**替代方法:** 共表达问题使用 WGCNA；转录调控子问题使用 SCENIC

**何时选择替代方案:** 共表达问题使用 WGCNA；转录调控子问题使用 SCENIC；仍需核对其输入和验证范围。

**已验证数据:** 无

**验证状态:** UNVALIDATED — 当前构建没有此方法的可执行证据。

**运行时间:** 小型示例不能代表性能基准；正式数据需记录耗时和线程设置。

**内存:** 在适用情况下保留稀疏表示，避免将整个大型图谱转为稠密矩阵；大对象内存占用尚未评测。

**绘图选择:** 先读[输出目录](OUTPUT_CATALOG.md)，再核对已登记的[图例](../../GALLERY.md)。未生成预览的图不视为可视化推荐。

**推荐脚本:** 无。此目录目前是方法卡和实现规划。

**参考资料:** [igraph / ggraph / STRING 官方文档](https://string-db.org/help/api/)
