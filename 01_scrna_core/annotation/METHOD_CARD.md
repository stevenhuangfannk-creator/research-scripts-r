# 方法卡：分层细胞注释

| 字段 | 内容 |
|---|---|
| 方法 ID | hierarchical_annotation |
| 分类 | 01_scrna_core |
| 状态 | VALIDATED |
| 语言 | R |
| 包 | Seurat |
| 最近验证 | 2026-10-07 |

包版本见[构建环境记录](../../docs/validation/package_status.tsv)；安装过某个包不等于它能够正常加载，也不等于方法经过验证。

官方文档：https://satijalab.org/seurat/articles/pbmc3k_tutorial

原始论文：原始论文见官方文档所列引用；本次构建未独立核验论文元数据。

## 科研问题与用途

将人工审核后的 L1/L2/L3 cluster-to-label 映射写回对象，同时保留 cluster ID 和证据。

## 适用条件与输入契约

含 cluster_column 指定分群列的 Seurat 对象（RDS）。labels 须是命名层级列表，每层为命名的 cluster-to-label 映射；evidence 须是非空证据字符串。

可选输入仅限工作流与配置实际支持的字段；候选方法的输入契约是规划规格，不能视为已实现功能。

## 实际调用与主要参数

逐层按 cluster ID 查 labels 映射，将标签写入 Seurat 元数据并生成 annotation.tsv。脚本不进行 marker 自动鉴定或参考库映射。

cluster_column 起点为 seurat_clusters；labels 的层级名可设为 celltype_l1/celltype_l2/celltype_l3。未映射的 cluster 会标为 Unknown；映射中出现输入不存在的 cluster 会报错。

参数值是起点，须结合物种、数据规模和样本设计审核。包广泛使用或参数有默认值，不意味着方法被提升为 DEFAULT。

## 假设、局限与常见误区

示例仅验证标签写回。真实标签须结合组织 marker、阴性 marker 与必要的子集重聚类审核；增殖/cycling 是状态而非谱系。evidence 非空校验不等于证据内容正确。

优点是输入、参数和输出范围明确，便于复用与追溯；该小型工作流不覆盖完整科研分析流程。

## 替代路线与选择依据

有合适且经验证的参考库时可评估 SingleR/Azimuth/reference mapping，并保留人工证据。

## 输出与图形

实际输出见[输出说明](OUTPUT_CATALOG.md)。需要画图时先查该输出说明，再查[全局图例](../../GALLERY.md)；没有已渲染预览的图不能当作已验证图形建议。

## 验证证据

验证数据：Seurat::pbmc_small。

PASS：在 pbmc_small 上仅验证标签写回和 Unknown 回退；没有验证标签的生物学正确性。

运行和内存：小型演示不是性能基准，目标数据需记录耗时与线程设置；尽量保留稀疏计数，不要将整张图谱转为稠密矩阵。大型对象的内存消耗尚未基准测试。

## 脚本与参考

脚本：[workflow.R](scripts/workflow.R)（01_scrna_core/annotation/scripts/workflow.R）。运行命令与配置说明见 [README](README.md)。

参考：https://satijalab.org/seurat/articles/pbmc3k_tutorial
