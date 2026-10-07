# 方法卡：CellPhoneDB 细胞通讯

**方法 ID:** cellphonedb

**分类:** 09_python_bridge

**状态:** CANDIDATE

**语言:** Python

**包 / 工具:** cellphonedb

**包版本:** 见[包加载与版本证据](../../docs/validation/package_status.tsv)；不能仅因包已安装就推断版本或方法可用。

**最近验证:** 尚未验证

**官方文档:** [cellphonedb 官方文档](https://cellphonedb.readthedocs.io/en/latest/)

**原始论文:** 从官方文档核对引用；本次整理未独立认证论文元数据。

**目的:** 检验依赖细胞类型标签的配体—受体共表达。

**科研问题:** 检验依赖细胞类型标签的配体—受体共表达。

**适用情况:** Python 表达矩阵、细胞元数据、数据库；小鼠数据还需经过确认的同源基因映射。

**不适用情况 / 使用边界:** 历史 R 代码中的 LIANA MouseConsensus 调用，不代表已经运行原生 Python CellPhoneDB。

**必需输入:** Python 表达矩阵、细胞元数据、数据库；小鼠数据还需经过确认的同源基因映射。

**可选输入:** 当前输入和参数是规划规范；尚无 workflow.R 支持可选字段。

**主要参数:** review_required = 数据库版本；表达阈值；置换次数。

**推荐起点:** 文档中的参数只是起点，应结合具体数据审查。知名包不自动获得 DEFAULT 状态。

**需要科研判断的参数:** 历史 R 代码中的 LIANA MouseConsensus 调用，不代表已经运行原生 Python CellPhoneDB。 具体配置见 [README](README.md)。

**输出:** 均值与 P 值；显著配体—受体对；发送—接收细胞气泡图。这些是拟实现的目标输出，当前没有执行结果。

**优势:** 输入要求、来源和目标输出明确，方法范围较小。

**局限:** 历史 R 代码中的 LIANA MouseConsensus 调用，不代表已经运行原生 Python CellPhoneDB。

**假设:** 历史 R 代码中的 LIANA MouseConsensus 调用，不代表已经运行原生 Python CellPhoneDB。

**常见问题:** 历史 R 代码中的 LIANA MouseConsensus 调用，不代表已经运行原生 Python CellPhoneDB。

**替代方法:** CellChat；LIANA

**何时选择替代方案:** CellChat；LIANA；仍需核对其输入和验证范围。

**已验证数据:** 无

**验证状态:** UNVALIDATED — 当前构建没有此方法的可执行证据。

**运行时间:** 小型示例不能代表性能基准；正式数据需记录耗时和线程设置。

**内存:** 在适用情况下保留稀疏表示，避免将整个大型图谱转为稠密矩阵；大对象内存占用尚未评测。

**绘图选择:** 先读[输出目录](OUTPUT_CATALOG.md)，再核对已登记的[图例](../../GALLERY.md)。未生成预览的图不视为可视化推荐。

**推荐脚本:** 无。此目录目前是方法卡和实现规划。

**参考资料:** [cellphonedb 官方文档](https://cellphonedb.readthedocs.io/en/latest/)
