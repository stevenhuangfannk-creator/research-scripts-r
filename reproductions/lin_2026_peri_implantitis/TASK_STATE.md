# Task State

- 当前阶段：Phase 4B-3 curated-v1 reference QC failure；按停止条件暂停 Phase 4B-4
- 已完成：独立 GPU 环境与 smoke test；初始和 curated-v1 两次全量 92,112-cell reference fit（各 250 epochs）；posterior/signature/history 导出；low-confidence、batch、marker 与 signature-dominance QC
- 已定位旧模型阻塞：Neutrophil 标签由 Leiden 33（可信）和 Leiden 47（FDCSP/TACSTD2/SPRR2A 高、PTPRC/FCGR3B/CSF3R 缺失）混合构成；cluster 47 占 nominal neutrophils 的 72.2%，使 reference signature 生物学异常
- 修复结果：已单独生成 curated-v1 派生输入，仅将 Leiden 47 的 702 cells 重标为 epithelial；原始输入、92,112 总细胞和 2,080 low-confidence cells 保留；GPU 250 epochs 与 posterior 导出已完成，中性粒细胞 FDCSP 污染已消除
- 新阻塞：巨噬细胞 signature 的 IGKC/IGKV4-1/IGHG1 高，C1QA/B/C 与 CD68 均排在 2,500 名之后；其 81.2% cells 来自 IGT3，可能存在标签或样本混杂。自动 QC 未通过，空间映射不得启动
- low-confidence 结论：2,080 cells 保留影响较小（最低 retain-vs-provisional 相关 0.990）；neutrophils 中没有 low-confidence cells，因此删除它们不能修复该问题
- 下一步：回到 Phase 4A 对 myeloid 与 plasma-like 簇及样本污染/双细胞进行针对性复核，生成新的版本化 reference 后再拟合与 QC；QC 通过前不进行空间映射
- 关键输出：`scripts/16_curate_reference_labels.py`、`scripts/16_train_cell2location_reference.py`、`scripts/17_qc_cell2location_reference.py`、`notes/PHASE4B_CELL2LOCATION_REFERENCE.md`
- 是否通过 QC：否；Phase 4B-4 未启动
- 是否 push：否
