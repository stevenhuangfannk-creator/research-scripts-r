# Seurat 降维与聚类（seurat_clustering）

识别变量基因，依次完成缩放、PCA、近邻图、聚类和 UMAP。

方法状态：VALIDATED；执行验证：PASS。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

已标准化的 Seurat 对象（RDS）。脚本使用当前默认 assay，运行前须确认其适合所选流程。

## 包在这里如何使用

FindVariableFeatures() → ScaleData() → RunPCA() → FindNeighbors(reduction = "pca") → FindClusters() → RunUMAP(reduction = "pca")。

## 配置哪些参数

nfeatures 为变量基因数；npcs 为请求的 PCA 维数；resolution 为聚类分辨率；n_neighbors 为 UMAP 邻居数；seed 为随机种子。脚本会按变量基因数/细胞数降低实际 PCA 维数，并限制 UMAP 邻居数。

## 运行方式

先在仓库根目录打开 R/终端，核对本地依赖（Seurat，以及统一入口使用的 yaml）。脚本不会自动安装包。将配置中的 input 指向真实输入 RDS，output_dir 设为本次运行目录；所有相对路径按仓库根目录解析。每次运行使用独立 output_dir，避免覆盖前次结果。

默认配置是起点，请先复制为自己的配置或修改必要字段。核对输入要求与参数后，在仓库根目录运行：

```powershell
Rscript scripts/run_method.R seurat_clustering 01_scrna_core/clustering/config/default.yml
```

工作流：[workflow.R](scripts/workflow.R)；统一入口：[run_method.R](../../scripts/run_method.R)。现有 PASS 仅覆盖方法卡所列范围，首次用于真实数据仍应核查结果。

默认 nfeatures = 2000、npcs = 30、resolution = 0.5 是参数起点，应检查 PCA 维数、marker 证据及不同 resolution 下的稳定性。

## 结果与边界

输出写入配置的 output_dir，具体文件见[输出说明](OUTPUT_CATALOG.md)。统一入口还会保存 sessionInfo.txt 和 run_metadata.yml。

resolution 不直接等于细胞类型数；UMAP 距离不是定量谱系距离。显著子集化后应重算。脚本固定基于 pca，不能通过当前配置选择 Harmony reduction 或其他聚类算法。

PASS：在 pbmc_small 的全部 80 个细胞上验证 PCA/近邻/聚类/UMAP；未验证大图谱稳健性或生物学分类。
