# 示例与验证

当前验证：**PASS**。已有证据使用 `survival::lung` 的 228 条公开临床记录检查右删失 KM 对象和数值表；未作新的临床解释。

## 用公开数据试跑

从仓库根目录在 R 中准备输入和配置；需要已能加载 `survival` 与 `yaml`：

~~~r
dir.create("data/examples", recursive = TRUE, showWarnings = FALSE)
lung <- survival::lung
lung$event <- as.integer(lung$status == 2)
saveRDS(lung, "data/examples/lung.rds")
config <- list(
  input = "data/examples/lung.rds",
  output_dir = "results/survival_km_example",
  time_column = "time",
  event_column = "event",
  group_column = "sex"
)
yaml::write_yaml(config, "data/examples/survival_km.yml")
~~~

此数据的 `status` 原为 1 / 2；先按数据定义映射为 0 / 1。自己的数据也必须明确事件定义，不能照搬编码。

~~~shell
Rscript scripts/run_method.R survival_km data/examples/survival_km.yml
~~~

在 `results/survival_km_example/` 查看 `object.rds`、`km.tsv` 和 `groups.tsv`。生存率应在 0 到 1 之间；`groups.tsv` 为各组总人数。当前封装不自动绘图、不计算 log-rank 检验，单组表格构造也尚需验证。

本地示例输入和生成结果不需要提交 Git。已有检查细节见[smoke 脚本](../../../scripts/smoke_tests.R)和[验证证据](../../../docs/validation/method_results.json)。正式使用前仍需审查时间起点、删失假设和竞争事件。
