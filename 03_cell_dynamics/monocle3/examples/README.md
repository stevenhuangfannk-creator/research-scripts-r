# 输入与最小验证约定

当前验证：**BLOCKED**，没有已执行的代表性数据结果。

输入：RDS 保存的 list(counts, cell_metadata, gene_metadata)。counts 为基因 × 细胞计数矩阵；其列名须与 cell_metadata 行名完全同序、行名须与 gene_metadata 行名完全同序；gene_metadata 须含 gene_short_name。配置必须提供真实且有生物学依据的 root_cells 条形码。

完整准备步骤、参数和输出限制见[中文使用说明](../README.md)。从仓库根目录运行：

```sh
Rscript scripts/run_method.R monocle3 03_cell_dynamics/monocle3/config/default.yml --allow-unvalidated
Rscript scripts/run_method.R monocle3_dynamics 03_cell_dynamics/monocle3/config/dynamics.yml --allow-unvalidated
```

先填写真实输入、审查配置并确认依赖可加载。`--allow-unvalidated` 不能代替验证。

升级前应验证 CDS 对齐、从预处理到排序的全流程、非空主图、可达性报告及实际 PNG/PDF。比较多个有依据的根和图设置；无限拟时序不得改为 0。3D 未实现；选定分支的 knn 关联不是正式分支间检验。动态分支输出还需检查 gene 标识是否保留。

共享[冒烟检查脚本](../../../scripts/smoke_tests.R)是验证入口之一，存在该脚本不代表本方法已通过。
