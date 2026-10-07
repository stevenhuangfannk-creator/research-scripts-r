# 示例与验证

当前验证：**PASS**。已有证据使用 `datasets::iris`（150 个花朵观测）检查 Pearson / Spearman、BH 校正以及缺失值 / 常量列的处理；混合物种存在混杂，这只是代码演示。

## 用公开数据试跑

从仓库根目录在 R 中执行以下准备代码；需要已能加载 `yaml`，不会自动安装依赖：

~~~r
dir.create("data/examples", recursive = TRUE, showWarnings = FALSE)
saveRDS(datasets::iris, "data/examples/iris.rds")
config <- list(
  input = "data/examples/iris.rds",
  output_dir = "results/correlation_example",
  variables = names(datasets::iris)[1:4],
  method = "pearson",
  missing = "error"
)
yaml::write_yaml(config, "data/examples/correlation.yml")
~~~

然后在仓库根目录的终端运行：

~~~shell
Rscript scripts/run_method.R correlation data/examples/correlation.yml
~~~

`results/correlation_example/correlations.tsv` 应有 6 个变量对，每对 `n = 150`、`excluded = 0`。改为 `method = "spearman"` 时，置信区间列应为 NA。此方法每对要求至少 4 个有限观测且无常量列；缺失值策略必须明确选择。

示例输入位于本地 `data/`，结果位于 `results/`；生成文件不需要提交 Git。已有检查细节见共享[smoke 脚本](../../../scripts/smoke_tests.R)和[验证证据](../../../docs/validation/method_results.json)。示例通过并不证明自己的数据满足独立性或没有混杂。
