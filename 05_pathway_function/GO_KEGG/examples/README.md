# 输入与最小验证约定

当前验证：**BLOCKED**，没有已执行的代表性数据结果。

输入：RDS 保存的 list(genes, universe)。universe 非空，所有 genes 必须属于 universe；基因 ID、物种与数据库须匹配。

完整准备步骤、参数和输出限制见[中文使用说明](../README.md)。从仓库根目录运行：

```sh
Rscript scripts/run_method.R go_kegg_ora 05_pathway_function/GO_KEGG/config/default.yml --allow-unvalidated
```

先填写真实输入、审查配置并确认依赖可加载。`--allow-unvalidated` 不能代替验证。

默认 ontology/key_type/organism 是占位符，GO 还缺 orgdb_package，必须先修订。核对 genes 属于真实背景、物种/ID/数据库匹配和输出字段；代码固定 BH，不读取 p_adjust。工作流当前不绘图。

共享[冒烟检查脚本](../../../scripts/smoke_tests.R)是验证入口之一，存在该脚本不代表本方法已通过。
