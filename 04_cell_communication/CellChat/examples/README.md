# 输入与最小验证约定

当前验证：**BLOCKED**，没有已执行的代表性数据结果。

输入：RDS 保存的 list(expression, metadata)。expression 为基因 × 细胞的非整合、对数归一化 RNA 表达矩阵；metadata 行名须与 expression 列名完全同序，且含 group_column 指定的细胞标签。使用匹配的 human 或 mouse 数据库。

完整准备步骤、参数和输出限制见[中文使用说明](../README.md)。从仓库根目录运行：

```sh
Rscript scripts/run_method.R cellchat 04_cell_communication/CellChat/config/default.yml --allow-unvalidated
Rscript scripts/run_method.R cellchat_compare 04_cell_communication/CellChat/config/compare.yml --allow-unvalidated
```

先填写真实输入、审查配置并确认依赖可加载。`--allow-unvalidated` 不能代替验证。

升级前应验证单数据集推断、有效 LR/通路表和实际 PNG/PDF，再以同数据库、设置和标签顺序比较两个独立对象。模式/相似性分析需要单独证据；两条件汇总比较是描述性的，细胞置换不能证明供者级处理显著性。

共享[冒烟检查脚本](../../../scripts/smoke_tests.R)是验证入口之一，存在该脚本不代表本方法已通过。
