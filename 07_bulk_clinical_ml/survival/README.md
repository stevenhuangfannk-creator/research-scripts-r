# Kaplan–Meier 生存分析

方法 ID：`survival_km`。按明确分组估计右删失生存曲线及其不确定性。

当前状态：**VALIDATED**；执行验证：**PASS**。先读[方法卡](METHOD_CARD.md)、[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例](gallery/README.md)和[配置](config/default.yml)。

工作流为 [workflow.R](scripts/workflow.R)，统一入口为 [run_method.R](../../scripts/run_method.R)。输入和配置的具体示例见下文；默认配置含说明性占位值，必须先替换。

## 运行前检查

R 需要能加载 `yaml` 与 `survival`；此入口不会自动安装包。输入可为 RDS、CSV 或 TSV。配置中的路径按**仓库根目录**解析。运行前核对所用列名、数值类型、事件 / 缺失值编码和研究设计。

需要合理的独立删失假设和正确的时间起点。KM 不调整协变量；存在竞争事件时应采用累积发生函数等竞争风险方法。

## 如何运行

将下面示例保存为 `07_bulk_clinical_ml/survival/config/my_config.yml`，再替换为自己的输入路径和真实列名。YAML key、方法 ID 和枚举值保留英文，中文只是解释。

~~~yaml
input: data/my_survival.csv
output_dir: results/survival_km_run1
time_column: followup_days
event_column: event
group_column: group
~~~

`time_column` 指向有限、非负的数值时间列；`event_column` 必须先映射为数值 0 / 1（0 = 删失，1 = 所研究事件）；`group_column` 指向无缺失的分组列。保持一致时间单位和起点，不能直接传入来源数据的 1 / 2 事件编码。

在仓库根目录执行：

~~~shell
Rscript scripts/run_method.R survival_km 07_bulk_clinical_ml/survival/config/my_config.yml
~~~

## 到哪里看结果

`results/survival_km_run1/` 下包含 `object.rds`、`km.tsv` 和 `groups.tsv`，以及环境和运行参数记录。KM 表包含默认汇总的事件时间点、生存率、95% 置信区间、风险集人数和事件数。工作流不自动画 KM 图，也不输出 log-rank 检验；`groups.tsv` 是各组总人数。

## 当前验证范围和已知问题

已有验证使用 `survival::lung` 的 228 条公开记录，将 `status == 2` 映射为事件 1，再按 `sex` 分组。只验证输出，没有作新的临床推论。

当前输出构造依赖 `summary(fit)$strata`。单组拟合时该字段可能为空，导致表格构造失败；请将此封装用于多个有效分组，单组 KM 需先另行验证。输入缺失值不会被自动清洗，协变量调整和竞争风险也未在此方法中实现。
