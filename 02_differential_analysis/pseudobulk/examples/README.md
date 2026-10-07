# 示例与验证：按样本与细胞类型汇总原始计数

PASS：pbmc_small 只有一个原始样本，现有验证仅覆盖原始 counts 求和及计数守恒；有生物学重复的处理组检验仍未验证。

这是对现有 registry 与方法卡验证记录的中文说明，本次汉化未重新运行科研分析。

输入要求：含 RNA raw counts 的 Seurat 对象（RDS），元数据中有 sample_column 指定的真实生物学样本列，以及 celltype_column 指定的审核后细胞类型列。

核对[使用说明](../README.md)中的参数和占位字段后，从仓库根目录运行：

```powershell
Rscript scripts/run_method.R pseudobulk 02_differential_analysis/pseudobulk/config/default.yml
```

所指 input.rds 需由用户提供；这里没有随仓库分发真实数据。现有小型验证不代表你的真实数据已验证。

现有验证逻辑见[共享 smoke tests](../../../scripts/smoke_tests.R)。其中演示标签或计数示例仅用于程序行为检查，不能作为研究证据。
