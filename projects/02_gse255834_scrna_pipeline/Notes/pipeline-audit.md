# 流程审计与未解决问题

## 输入输出链缺口

1. `build_GSE255834_seurat.R` 生成 `GSE255834_seurat_object.rds`，而 `add_scDblFinder_to_GSE255834.R` 读取 `GSE255834_seurat_object_joined.rds`。原目录没有生成或解释 `object_joined` 的代码。很可能需要 Seurat v5 的 `JoinLayers()`，但在看到实际对象前不应自动补写。
2. `recompute_singlet_umap.R` 读取 `GSE255834_seurat_singlet.rds`，现有脚本没有保存这个文件。主流程可直接由 `strict_qc_umap_70_workers.R` 完成 singlet 过滤，因此该脚本视为历史替代分支。
3. `annotate_GSE255834_strict.R` 默认读取严格 QC 对象，而不是 DecontX 输出。它支持 `GSE255834_ANNOTATION_INPUT` 和 `GSE255834_ANNOTATION_OUTDIR` 环境变量；若以去污染对象为最终输入，需要显式设置。

## 重复与历史版本

- `finish_GSE255834_seurat_from_samples.R` 与 `build_GSE255834_seurat.R` 后半段的合并、标准化、聚类和保存逻辑重复。前者具有恢复价值，因此保留。
- 两个 `diagnose_qc_*` 脚本检查不同阶段，不完全重复。
- `recompute_singlet_umap.R` 和严格 QC 脚本都重新计算降维；前者输入来源不明，标记为历史分支。

## 可移植性与性能

- 10 个文件中有 9 个包含 `C:/Users/zhaozize/Desktop/APAP` 绝对路径。
- 多处固定使用 8、32、70 或 72 个工作线程。应按机器内存和 CPU 调整，尤其不要在 Windows 多进程中复制大型 Seurat 对象。
- `build_GSE255834_seurat.R` 和恢复脚本使用不同压缩方式（`xz` 与 `gzip`），不会改变分析内容，但会影响速度和体积。
- 没有版本锁定文件，`Seurat` v5 layer 语义、`scDblFinder` 和 `celda::decontX` 版本差异可能影响运行。

## 数据与 Git

未发现真实数据或结果。`.gitignore` 排除了 H5、RDS、矩阵、压缩包、原始数据、结果、图和环境缓存。上传前仍应检查将来加入的样本元数据是否含内部样本编号或其他未公开信息。
