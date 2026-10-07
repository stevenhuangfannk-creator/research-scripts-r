# 输入与最小验证约定

当前验证：**BLOCKED**，没有已执行的代表性数据结果。

输入：RDS 保存的 list(ranks, pathways)。ranks 为命名、有限的带方向数值向量，基因名唯一；pathways 为命名基因集列表，两者须使用兼容的基因 ID。

完整准备步骤、参数和输出限制见[中文使用说明](../README.md)。从仓库根目录运行：

```sh
Rscript scripts/run_method.R fgsea 05_pathway_function/GSEA/config/default.yml --allow-unvalidated
```

先填写真实输入、审查配置并确认依赖可加载。`--allow-unvalidated` 不能代替验证。

核对完整带方向排序、唯一且兼容的 ID、并列值、基因集覆盖和 NES/padj/leadingEdge 输出。工作流当前只输出结果表，不画富集曲线。

共享[冒烟检查脚本](../../../scripts/smoke_tests.R)是验证入口之一，存在该脚本不代表本方法已通过。
