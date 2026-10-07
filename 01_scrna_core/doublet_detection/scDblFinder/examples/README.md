# 示例与验证：scDblFinder 双细胞检测

BLOCKED：现有构建环境缺少 scDblFinder，工作流未执行；提供真实输入并解决依赖后仍需验证。

这是对现有 registry 与方法卡验证记录的中文说明，本次汉化未重新运行科研分析。

输入要求：含 RNA 原始 counts 的 Seurat 对象（RDS），元数据中存在 capture_column 指定的建库/capture 列。capture ID 不能自动用 donor ID 替代。

核对[使用说明](../README.md)中的参数和占位字段后，从仓库根目录运行：

```powershell
Rscript scripts/run_method.R scdblfinder 01_scrna_core/doublet_detection/scDblFinder/config/default.yml --allow-unvalidated
```

所指 input.rds 需由用户提供；这里没有随仓库分发真实数据。--allow-unvalidated 不会安装依赖，也不会改变方法验证状态。

现有验证逻辑见[共享 smoke tests](../../../../scripts/smoke_tests.R)。其中演示标签或计数示例仅用于程序行为检查，不能作为研究证据。
