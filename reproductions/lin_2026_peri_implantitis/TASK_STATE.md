# Task State

- 当前阶段：Phase 4B-1 Spatial QC 与映射检查
- 已完成：PI spatial 与 8 个 healthy spatial 样本的矩阵、barcode、坐标、比例尺、图像及 tissue mask 检查；生成 QC 汇总与覆盖图；未过滤 spot
- 当前阻塞：无输入完整性阻塞；healthy A1-D1 与 A2-D2 存在明显测序深度/批次差异
- 下一步：Phase 4B-2，准备 cell2location 的 scRNA reference、逐样本 spatial 输入与严格 gene intersection
- 关键输出：`results/phase4b/qc/`、`figures/phase4b/qc/`、`notes/PHASE4B_SPATIAL_QC.md`
- 最近一次分析 commit：本阶段提交（提交后由 Git 生成 hash）
- 是否通过 QC：是；附带 batch-depth warning
- 是否 push：否
