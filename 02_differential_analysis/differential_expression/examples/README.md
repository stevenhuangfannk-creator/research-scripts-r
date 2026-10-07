# 示例与验证：探索性 cluster marker 分析

PASS：在 pbmc_small 上验证探索性 cluster-marker 表；没有验证样本层级处理组推断。

这是对现有 registry 与方法卡验证记录的中文说明，本次汉化未重新运行科研分析。

输入要求：含标准化 RNA 表达 data layer 的 Seurat 对象（RDS），元数据中存在 group_column 指定的分组列。

核对[使用说明](../README.md)中的参数和占位字段后，从仓库根目录运行：

```powershell
Rscript scripts/run_method.R cell_markers 02_differential_analysis/differential_expression/config/default.yml
```

所指 input.rds 需由用户提供；这里没有随仓库分发真实数据。现有小型验证不代表你的真实数据已验证。

现有验证逻辑见[共享 smoke tests](../../../scripts/smoke_tests.R)。其中演示标签或计数示例仅用于程序行为检查，不能作为研究证据。
