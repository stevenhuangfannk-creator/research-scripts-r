# 示例与验证

当前验证：**PASS**。已有证据使用 `survival::lung` 的 `age` / `sex` 协变量检查 Cox 风险比、置信区间和比例风险诊断，不验证预测性能或因果关系。

## 用公开数据试跑

从仓库根目录在 R 中准备输入和配置；需要已能加载 `survival` 与 `yaml`：

~~~r
dir.create("data/examples", recursive = TRUE, showWarnings = FALSE)
lung <- survival::lung
lung$event <- as.integer(lung$status == 2)
saveRDS(lung, "data/examples/lung.rds")
config <- list(
  input = "data/examples/lung.rds",
  output_dir = "results/cox_example",
  time_column = "time",
  event_column = "event",
  covariates = c("age", "sex")
)
yaml::write_yaml(config, "data/examples/cox.yml")
~~~

~~~shell
Rscript scripts/run_method.R cox data/examples/cox.yml
~~~

查看 `results/cox_example/cox.tsv` 与 `proportional_hazards.tsv`。此示例的两个数值协变量通常对应两个估计项和包含 GLOBAL 行的三个诊断项；分类编码展开后，行数会改变。

本示例保留既有验证中 `sex` 的数值编码以便复现。实际研究若把它作为分类变量，应先转换为 `factor` 并说明参考组；连续变量则需明确单位和效应形式。所用列不能缺失，封装不会自动删除缺失行。

本地示例输入和生成结果不需要提交 Git。已有检查细节见[smoke 脚本](../../../scripts/smoke_tests.R)和[验证证据](../../../docs/validation/method_results.json)。比例风险诊断通过也不能代替独立预测验证。
