# 单细胞基础模型探索

方法 ID：`foundation_models`。将预训练表征迁移的效果与简单基线进行比较。

当前状态：**EXPERIMENTAL**；执行验证：**UNVALIDATED**。先读[方法卡](METHOD_CARD.md)、[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例](gallery/README.md)和[配置](config/default.yml)。

## 当前可用内容

本目录提供中文方法说明、输入要求、待审查参数和目标输出，**尚无可执行工作流**。注册表中的 `script` 为 `null`，不能用 `run_method.R` 运行此方法；`--allow-unvalidated` 也不会生成缺失的实现。

## 使用前准备

1. 准备输入：模型兼容的表达 token、模型检查点，以及训练领域审查信息。
2. 审查规划参数：review_required = 模型检查点；词表；标准化；评价数据划分。
3. 参考[官方文档](https://github.com/bowang-lab/scGPT)完成小型可复现实例，再记录输入、参数、依赖版本与实际输出；实现及验证完成后才可在本仓库运行或升级状态。

`config/default.yml` 中的 `input`、`output_dir` 和 `review_required` 是规划占位，不能视为已实现的输入接口。在领域偏移、信息泄漏和相对基线收益得到审查前，仅限实验探索；没有默认推荐的模型检查点。
