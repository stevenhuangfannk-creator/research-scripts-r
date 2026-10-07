# Scanpy 单细胞分析路线

方法 ID：`scanpy`。为单细胞 RNA 分析提供独立管理的 Python 路线。

当前状态：**CANDIDATE**；执行验证：**UNVALIDATED**。先读[方法卡](METHOD_CARD.md)、[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例](gallery/README.md)和[配置](config/default.yml)。

## 当前可用内容

本目录提供中文方法说明、输入要求、待审查参数和目标输出，**尚无可执行工作流**。注册表中的 `script` 为 `null`，不能用 `run_method.R` 运行此方法；`--allow-unvalidated` 也不会生成缺失的实现。

## 使用前准备

1. 准备输入：AnnData 原始计数、细胞元数据，以及 Python 环境说明。
2. 审查规划参数：review_required = 标准化方法；PCA；近邻图；聚类随机种子。
3. 参考[官方文档](https://scanpy.readthedocs.io/)完成小型可复现实例，再记录输入、参数、依赖版本与实际输出；实现及验证完成后才可在本仓库运行或升级状态。

`config/default.yml` 中的 `input`、`output_dir` 和 `review_required` 是规划占位，不能视为已实现的输入接口。本仓库以 R 为主要路线；Python 方法应使用各自独立的环境，不合并为一个庞大环境。
