# Task State

- 当前阶段：Phase 4B-3 cell2location reference QC failure diagnosis
- 已完成：独立 GPU 环境与 smoke test；全量 92,112-cell reference fit（250 epochs）；posterior/signature/history 导出；low-confidence、batch、marker 与 signature-dominance QC
- 当前阻塞：Neutrophil 标签由 Leiden 33（可信）和 Leiden 47（FDCSP/TACSTD2/SPRR2A 高、PTPRC/FCGR3B/CSF3R 缺失）混合构成；cluster 47 占 nominal neutrophils 的 72.2%，使 reference signature 生物学异常
- low-confidence 结论：2,080 cells 保留影响较小（最低 retain-vs-provisional 相关 0.990）；neutrophils 中没有 low-confidence cells，因此删除它们不能修复该问题
- 下一步：回到 Phase 4A 注释证据，人工复核并重标 Leiden 47；重建 4B-2 reference input 后重新训练 reference
- 关键输出：`scripts/16_train_cell2location_reference.py`、`scripts/17_qc_cell2location_reference.py`、`notes/PHASE4B_CELL2LOCATION_REFERENCE.md`
- 是否通过 QC：否；Phase 4B-4 未启动
- 是否 push：否
