# CellPhoneDB 细胞通讯

方法 ID：`cellphonedb`。检验依赖细胞类型标签的配体—受体共表达。

当前状态：**CANDIDATE**；执行验证：**UNVALIDATED**。先读[方法卡](METHOD_CARD.md)、[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例](gallery/README.md)和[配置](config/default.yml)。

## 当前可用内容

本目录提供中文方法说明、输入要求、待审查参数和目标输出，**尚无可执行工作流**。注册表中的 `script` 为 `null`，不能用 `run_method.R` 运行此方法；`--allow-unvalidated` 也不会生成缺失的实现。

## 使用前准备

1. 准备输入：Python 表达矩阵、细胞元数据、数据库；小鼠数据还需经过确认的同源基因映射。
2. 审查规划参数：review_required = 数据库版本；表达阈值；置换次数。
3. 参考[官方文档](https://cellphonedb.readthedocs.io/en/latest/)完成小型可复现实例，再记录输入、参数、依赖版本与实际输出；实现及验证完成后才可在本仓库运行或升级状态。

`config/default.yml` 中的 `input`、`output_dir` 和 `review_required` 是规划占位，不能视为已实现的输入接口。历史 R 代码中的 LIANA MouseConsensus 调用，不代表已经运行原生 Python CellPhoneDB。
