# 方法卡：Seurat 降维与聚类

| 字段 | 内容 |
|---|---|
| 方法 ID | seurat_clustering |
| 分类 | 01_scrna_core |
| 状态 | VALIDATED |
| 语言 | R |
| 包 | Seurat |
| 最近验证 | 2026-10-07 |

包版本见[构建环境记录](../../docs/validation/package_status.tsv)；安装过某个包不等于它能够正常加载，也不等于方法经过验证。

官方文档：https://satijalab.org/seurat/articles/pbmc3k_tutorial

原始论文：原始论文见官方文档所列引用；本次构建未独立核验论文元数据。

## 科研问题与用途

识别变量基因，依次完成缩放、PCA、近邻图、聚类和 UMAP。

## 适用条件与输入契约

已标准化的 Seurat 对象（RDS）。脚本使用当前默认 assay，运行前须确认其适合所选流程。

可选输入仅限工作流与配置实际支持的字段；候选方法的输入契约是规划规格，不能视为已实现功能。

## 实际调用与主要参数

FindVariableFeatures() → ScaleData() → RunPCA() → FindNeighbors(reduction = "pca") → FindClusters() → RunUMAP(reduction = "pca")。

nfeatures 为变量基因数；npcs 为请求的 PCA 维数；resolution 为聚类分辨率；n_neighbors 为 UMAP 邻居数；seed 为随机种子。脚本会按变量基因数/细胞数降低实际 PCA 维数，并限制 UMAP 邻居数。

参数值是起点，须结合物种、数据规模和样本设计审核。包广泛使用或参数有默认值，不意味着方法被提升为 DEFAULT。

## 假设、局限与常见误区

resolution 不直接等于细胞类型数；UMAP 距离不是定量谱系距离。显著子集化后应重算。脚本固定基于 pca，不能通过当前配置选择 Harmony reduction 或其他聚类算法。

优点是输入、参数和输出范围明确，便于复用与追溯；该小型工作流不覆盖完整科研分析流程。

## 替代路线与选择依据

Leiden 等算法需单独验证；需要批次校正分析空间时，可先评估 Harmony，再明确写下游 reduction 使用方式。

## 输出与图形

实际输出见[输出说明](OUTPUT_CATALOG.md)。需要画图时先查该输出说明，再查[全局图例](../../GALLERY.md)；没有已渲染预览的图不能当作已验证图形建议。

## 验证证据

验证数据：Seurat::pbmc_small。

PASS：在 pbmc_small 的全部 80 个细胞上验证 PCA/近邻/聚类/UMAP；未验证大图谱稳健性或生物学分类。

运行和内存：小型演示不是性能基准，目标数据需记录耗时与线程设置；尽量保留稀疏计数，不要将整张图谱转为稠密矩阵。大型对象的内存消耗尚未基准测试。

## 脚本与参考

脚本：[workflow.R](scripts/workflow.R)（01_scrna_core/clustering/scripts/workflow.R）。运行命令与配置说明见 [README](README.md)。

参考：https://satijalab.org/seurat/articles/pbmc3k_tutorial
