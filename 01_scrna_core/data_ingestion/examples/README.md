# 示例与验证：创建 Seurat 对象

PASS：仅验证 counts/metadata 对齐与计数保留，测试数据为 pbmc_small（230 个基因、80 个细胞）；不代表任意真实数据都完成了预处理。

这是对现有 registry 与方法卡验证记录的中文说明，本次汉化未重新运行科研分析。

输入要求：一个 RDS 文件，内容为 list(counts = counts, metadata = metadata)。counts 是非负、有限的基因 × 细胞计数矩阵，须有唯一的行名和列名；metadata 是 data.frame，其行名须与细胞条形码集合一致。

核对[使用说明](../README.md)中的参数和占位字段后，从仓库根目录运行：

```powershell
Rscript scripts/run_method.R seurat_ingestion 01_scrna_core/data_ingestion/config/default.yml
```

所指 input.rds 需由用户提供；这里没有随仓库分发真实数据。现有小型验证不代表你的真实数据已验证。

现有验证逻辑见[共享 smoke tests](../../../scripts/smoke_tests.R)。其中演示标签或计数示例仅用于程序行为检查，不能作为研究证据。
