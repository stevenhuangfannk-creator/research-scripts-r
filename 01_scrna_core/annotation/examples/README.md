# 示例与验证：分层细胞注释

PASS：在 pbmc_small 上仅验证标签写回和 Unknown 回退；没有验证标签的生物学正确性。

这是对现有 registry 与方法卡验证记录的中文说明，本次汉化未重新运行科研分析。

输入要求：含 cluster_column 指定分群列的 Seurat 对象（RDS）。labels 须是命名层级列表，每层为命名的 cluster-to-label 映射；evidence 须是非空证据字符串。

核对[使用说明](../README.md)中的参数和占位字段后，从仓库根目录运行：

```powershell
Rscript scripts/run_method.R hierarchical_annotation 01_scrna_core/annotation/config/default.yml
```

所指 input.rds 需由用户提供；这里没有随仓库分发真实数据。现有小型验证不代表你的真实数据已验证。

现有验证逻辑见[共享 smoke tests](../../../scripts/smoke_tests.R)。其中演示标签或计数示例仅用于程序行为检查，不能作为研究证据。
