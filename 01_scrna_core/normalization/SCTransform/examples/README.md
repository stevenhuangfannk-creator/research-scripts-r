# 示例与验证：SCTransform 方差稳定化

UNVALIDATED：本构建没有可执行验证证据，也没有已验证的数据集。

这是对现有 registry 与方法卡验证记录的中文说明，本次汉化未重新运行科研分析。

输入要求：含 RNA counts 的 Seurat 对象（RDS）。若指定 vars_to_regress，相应协变量须存在于元数据。

核对[使用说明](../README.md)中的参数和占位字段后，从仓库根目录运行：

```powershell
Rscript scripts/run_method.R sctransform 01_scrna_core/normalization/SCTransform/config/default.yml --allow-unvalidated
```

所指 input.rds 需由用户提供；这里没有随仓库分发真实数据。--allow-unvalidated 不会安装依赖，也不会改变方法验证状态。

现有验证逻辑见[共享 smoke tests](../../../../scripts/smoke_tests.R)。其中演示标签或计数示例仅用于程序行为检查，不能作为研究证据。
