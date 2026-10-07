# Pearson / Spearman 相关分析

方法 ID：`correlation`。估计 Pearson / Spearman 相关性，明确缺失值处理，并进行 BH 多重检验校正。

当前状态：**VALIDATED**；执行验证：**PASS**。先读[方法卡](METHOD_CARD.md)、[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例](gallery/README.md)和[配置](config/default.yml)。

工作流为 [workflow.R](scripts/workflow.R)，统一入口为 [run_method.R](../../scripts/run_method.R)。输入和配置的具体示例见下文；默认配置含说明性占位值，必须先替换。

## 运行前检查

R 需要能加载 `yaml` 与 `stats`；此入口不会自动安装包。输入可为 RDS、CSV 或 TSV。配置中的路径按**仓库根目录**解析。运行前核对所用列名、数值类型、事件 / 缺失值编码和研究设计。

相关不等于因果。Pearson 衡量线性关联，Spearman 衡量单调的秩关联；重复测量或存在混杂时需要其他模型。

## 如何运行

将下面示例保存为 `07_bulk_clinical_ml/correlation/config/my_config.yml`，再替换为自己的输入路径和真实列名。YAML key、方法 ID 和枚举值保留英文，中文只是解释。

~~~yaml
input: data/my_measurements.csv
output_dir: results/correlation_run1
variables:
  - gene_A
  - gene_B
  - score
method: spearman
missing: error
~~~

`variables` 至少两个不同的数值列名；`method` 只能为 `pearson` 或 `spearman`。`missing: error` 遇到任何所选变量对中的缺失 / 非有限值时中止；`missing: pairwise` 则按每一对变量分别排除，并记录 `n` 和 `excluded`。每一对至少保留 4 个观测，且不能有常量列。

在仓库根目录执行：

~~~shell
Rscript scripts/run_method.R correlation 07_bulk_clinical_ml/correlation/config/my_config.yml
~~~

## 到哪里看结果

打开 `results/correlation_run1/correlations.tsv`。其中 `r` 在 Pearson 模式为 r，在 Spearman 模式为 rho；`p_adjust` 对所选变量的全部两两比较统一进行 BH 校正。Pearson 输出默认 95% 置信区间，当前 Spearman 实现的 `ci_low` / `ci_high` 为 NA，P 值采用 `exact = FALSE`。环境与参数记录见同目录的 `sessionInfo.txt` / `run_metadata.yml`。

## 当前验证范围

已有验证使用 `datasets::iris` 的 150 个观测，包含两种检验、BH 校正和缺失 / 常量列检查。混合物种存在混杂，仅用于检查代码输出；不能将此演示当作研究证据。正式数据中的协变量、重复测量和混杂需要另选模型。
