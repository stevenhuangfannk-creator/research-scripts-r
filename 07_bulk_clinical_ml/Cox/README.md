# Cox 比例风险回归

方法 ID：`cox`。估计未调整 / 已调整的风险比，并检查比例风险假设。

当前状态：**VALIDATED**；执行验证：**PASS**。先读[方法卡](METHOD_CARD.md)、[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例](gallery/README.md)和[配置](config/default.yml)。

工作流为 [workflow.R](scripts/workflow.R)，统一入口为 [run_method.R](../../scripts/run_method.R)。输入和配置的具体示例见下文；默认配置含说明性占位值，必须先替换。

## 运行前检查

R 需要能加载 `yaml` 与 `survival`；此入口不会自动安装包。输入可为 RDS、CSV 或 TSV。配置中的路径按**仓库根目录**解析。运行前核对所用列名、数值类型、事件 / 缺失值编码和研究设计。

需明确连续变量的效应形式和分类编码，检查比例风险假设、事件数、有影响的观测和混杂。预测用途还需独立验证。

## 如何运行

将下面示例保存为 `07_bulk_clinical_ml/Cox/config/my_config.yml`，再替换为自己的输入路径和真实列名。YAML key、方法 ID 和枚举值保留英文，中文只是解释。

~~~yaml
input: data/my_clinical.rds
output_dir: results/cox_run1
time_column: followup_days
event_column: event
covariates:
  - age
  - group
~~~

默认 `config/default.yml` 目前缺少 `time_column` / `event_column`，且 `covariates` 是说明文字；上面的配置补齐实际工作流所需字段。事件使用数值 0 / 1（0 = 删失，1 = 事件），时间使用有限非负数值。所用列都必须无缺失；调用者还需检查非有限值，因为封装没有完整的有限值校验。

单因素模型在 `covariates` 中放一个列名；多因素模型放多个有研究依据的列名。该入口每次只拟合一个模型，不会自动遍历全部变量进行单因素筛选。分类协变量请事先设为 `factor`，明确参考水平；保存为 RDS 可保留 R 中的类型。数值型编码可能被解释为连续效应。

在仓库根目录执行：

~~~shell
Rscript scripts/run_method.R cox 07_bulk_clinical_ml/Cox/config/my_config.yml
~~~

## 到哪里看结果

`results/cox_run1/` 下包含 `object.rds`、`cox.tsv` 与 `proportional_hazards.tsv`，以及环境和参数记录。重点查看 HR、95% 置信区间、P 值和 `cox.zph` 诊断；工作流不会自动画森林图或生成独立验证集预测。

## 当前验证范围

已有验证使用 `survival::lung` 的 `age` / `sex` 协变量，只检查 HR / CI 与比例风险诊断输出。不能由此宣称模型具有预测性能或因果效应。协变量选择、非线性关系、事件数、缺失数据和时间依赖效应仍需要针对研究设计处理。
