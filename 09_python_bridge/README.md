# Python 方法桥接（09_python_bridge）

本仓库以 R 为主要入口；Python 方法按方法分别管理环境，不共用一个庞大环境。当前不新增仅针对空间数据的流程。

| 使用目的 | 方法入口 | 当前状态 |
|---|---|---|
| Python 单细胞基础分析 | [Scanpy](Scanpy/README.md) | CANDIDATE / UNVALIDATED |
| 原生 Python 配体—受体分析 | [CellPhoneDB](CellPhoneDB/README.md) | CANDIDATE / UNVALIDATED |
| 剪接数据推断 RNA velocity | [scVelo](scVelo/README.md) | EXPERIMENTAL / UNVALIDATED |
| 状态转移与命运概率 | [CellRank](CellRank/README.md) | EXPERIMENTAL / UNVALIDATED |
| 预训练表征与基线比较 | [foundation_models](foundation_models/README.md) | EXPERIMENTAL / UNVALIDATED |

以上目录目前只有中文方法卡、输入和参数规划，没有 Python 工作流或可运行的本仓库示例。配置中的 `data/input.rds` 是规划占位，不代表这些 Python 包直接接受 RDS，也不代表已有 R / Python 转换实现。

先读[方法索引](../METHOD_INDEX.md)、[全局图例](../GALLERY.md)和[注册表说明](../registry/README.md)。具体依赖和版本需在相应方法实现、测试时记录；目录存在不能作为执行或验证证据。
