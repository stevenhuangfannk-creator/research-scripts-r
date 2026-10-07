# 示例与验证：Harmony 批次整合

UNVALIDATED：本构建没有可执行验证证据，也没有已验证的数据集。

这是对现有 registry 与方法卡验证记录的中文说明，本次汉化未重新运行科研分析。

输入要求：已标准化、已有 pca reduction 的 Seurat 对象（RDS），含 batch_column 指定的技术批次列，并至少有两个批次。

核对[使用说明](../README.md)中的参数和占位字段后，从仓库根目录运行：

```powershell
Rscript scripts/run_method.R harmony 01_scrna_core/batch_integration/Harmony/config/default.yml --allow-unvalidated
```

所指 input.rds 需由用户提供；这里没有随仓库分发真实数据。--allow-unvalidated 不会安装依赖，也不会改变方法验证状态。

现有验证逻辑见[共享 smoke tests](../../../../scripts/smoke_tests.R)。其中演示标签或计数示例仅用于程序行为检查，不能作为研究证据。
