# 官方斑马鱼复现 / Official zebrafish case

来源是官方 `rgv.datasets.zebrafish_nc()` 与 `rgv.datasets.zebrafish_grn()`，主教程数据为Smart-seq3 neural crest发育。数据大小、SHA与缓存位置以来源清单和本次真实审计为准。此文档不复制官方已经执行的notebook结果作为自己的成果。

本模块根执行：

```powershell
python scripts/regvelo.py audit --config config/official_zebrafish.json
python scripts/regvelo.py all --config config/official_zebrafish.json --resume
```

当前执行状态读取 `output/run_state.json`；完整模型QC、阶段日志与真实Gallery随实际运行生成。`config/smoke.json` 是明确缩小的工程/方法接口测试，不计作完整官方数据复现。

官方教程有效TF包括 `elf1` 与 `nr2f5`。命运状态示例包括mesenchymal、arch2、hox34、Pigment等，但实际终末定义必须依据本次对象、macrostate和生物学证据，不能生硬照搬或为了预期结果改名。
