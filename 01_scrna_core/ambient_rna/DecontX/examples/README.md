# 示例与验证：DecontX 环境 RNA 去污染

BLOCKED：现有构建环境缺少 celda，工作流未执行；没有已验证的数据集。

这是对现有 registry 与方法卡验证记录的中文说明，本次汉化未重新运行科研分析。

输入要求：RDS 中保存 list(counts, metadata, backgrounds)。counts 为原始基因 × 细胞计数；metadata 的行名顺序须与 counts 列名完全一致，并含 capture_column。backgrounds 若提供，为按 capture ID 命名的空液滴计数矩阵列表；背景可缺省。

核对[使用说明](../README.md)中的参数和占位字段后，从仓库根目录运行：

```powershell
Rscript scripts/run_method.R decontx 01_scrna_core/ambient_rna/DecontX/config/default.yml --allow-unvalidated
```

所指 input.rds 需由用户提供；这里没有随仓库分发真实数据。--allow-unvalidated 不会安装依赖，也不会改变方法验证状态。

现有验证逻辑见[共享 smoke tests](../../../../scripts/smoke_tests.R)。其中演示标签或计数示例仅用于程序行为检查，不能作为研究证据。
