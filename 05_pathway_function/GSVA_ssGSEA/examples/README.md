# 输入准备与验证计划

当前验证：**UNVALIDATED**。本次构建没有可执行实现或运行证据。

输入约定：归一化的基因 × 独立样本表达矩阵，以及基因集。

本方法尚无可运行示例。registry 的 `script` 为 `null`，不能使用 `Rscript scripts/run_method.R gsva_ssgsea ...`，也不能用 `--allow-unvalidated` 绕过缺失实现。

实施前需阅读[方法卡](../METHOD_CARD.md)，确认 review_required：GSVA 或 ssGSEA、核函数、基因集大小和已安装的 API 版本。当前只是待核对清单，尚未接入可执行脚本。 再依照官方 API 建立最小复现并验证输入、输出和科学解释。共享[冒烟检查脚本](../../../scripts/smoke_tests.R)可供后续接入参考，但不构成本方法已验证的证据。
