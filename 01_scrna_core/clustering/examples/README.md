# 示例与验证：Seurat 降维与聚类

PASS：在 pbmc_small 的全部 80 个细胞上验证 PCA/近邻/聚类/UMAP；未验证大图谱稳健性或生物学分类。

这是对现有 registry 与方法卡验证记录的中文说明，本次汉化未重新运行科研分析。

输入要求：已标准化的 Seurat 对象（RDS）。脚本使用当前默认 assay，运行前须确认其适合所选流程。

核对[使用说明](../README.md)中的参数和占位字段后，从仓库根目录运行：

```powershell
Rscript scripts/run_method.R seurat_clustering 01_scrna_core/clustering/config/default.yml
```

所指 input.rds 需由用户提供；这里没有随仓库分发真实数据。现有小型验证不代表你的真实数据已验证。

现有验证逻辑见[共享 smoke tests](../../../scripts/smoke_tests.R)。其中演示标签或计数示例仅用于程序行为检查，不能作为研究证据。
