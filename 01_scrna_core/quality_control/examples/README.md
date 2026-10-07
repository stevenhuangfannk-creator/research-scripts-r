# 示例与验证：单细胞质量控制

PASS：pbmc_small 本身缺少线粒体/核糖体基因，现有验证覆盖审计/过滤及额外三基因测试中的精确比例计算；没有验证真实组织的最佳 QC 阈值。

这是对现有 registry 与方法卡验证记录的中文说明，本次汉化未重新运行科研分析。

输入要求：含 RNA counts 的 Seurat 对象（RDS）。基因名应能够匹配所选物种的 mt_pattern/ribo_pattern；元数据须含 nFeature_RNA 和 nCount_RNA。

核对[使用说明](../README.md)中的参数和占位字段后，从仓库根目录运行：

```powershell
Rscript scripts/run_method.R scrna_qc 01_scrna_core/quality_control/config/default.yml
```

所指 input.rds 需由用户提供；这里没有随仓库分发真实数据。现有小型验证不代表你的真实数据已验证。

现有验证逻辑见[共享 smoke tests](../../../scripts/smoke_tests.R)。其中演示标签或计数示例仅用于程序行为检查，不能作为研究证据。
