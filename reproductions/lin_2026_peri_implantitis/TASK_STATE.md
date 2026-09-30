# Task State

- 当前阶段：Phase 4A 定向髓系／浆细胞 annotation audit 与 Phase 4B-3 curated-v2 reference QC 已完成；按用户要求停在 Phase 4B-4 之前
- 已完成：独立 GPU 环境与 smoke test；初始和 curated-v1 两次全量 92,112-cell reference fit（各 250 epochs）；posterior/signature/history 导出；low-confidence、batch、marker 与 signature-dominance QC
- 已定位旧模型阻塞：Neutrophil 标签由 Leiden 33（可信）和 Leiden 47（FDCSP/TACSTD2/SPRR2A 高、PTPRC/FCGR3B/CSF3R 缺失）混合构成；cluster 47 占 nominal neutrophils 的 72.2%，使 reference signature 生物学异常
- 修复结果：已单独生成 curated-v1 派生输入，仅将 Leiden 47 的 702 cells 重标为 epithelial；原始输入、92,112 总细胞和 2,080 low-confidence cells 保留；GPU 250 epochs 与 posterior 导出已完成，中性粒细胞 FDCSP 污染已消除
- 新阻塞：巨噬细胞 signature 的 IGKC/IGKV4-1/IGHG1 高，C1QA/B/C 与 CD68 均排在 2,500 名之后；其 81.2% cells 来自 IGT3，可能存在标签或样本混杂。自动 QC 未通过，空间映射不得启动
- low-confidence 结论：2,080 cells 保留影响较小（最低 retain-vs-provisional 相关 0.990）；neutrophils 中没有 low-confidence cells，因此删除它们不能修复该问题
- 定向审计结果：原 1,885 macrophage-labelled cells 跨多个不相容谱系，1,531 来自 IGT3；全部标记为 Unresolved。原 Monocytes/Leiden 27 的 253 个 osteoclast-like cells 也标为 Unresolved。Monocytes/Leiden 25 内局部 Leiden 5 的 1,417 个细胞具备多基因 macrophage 程序，修订为 Macrophages。原始数据与 Leiden 47 修正未变；逐细胞证据见 `notes/PHASE4A_MYELOID_PLASMA_AUDIT.md`。
- 新输入：Phase 4B-2 以 curated-v2 标签重新制备 89,974-cell、14-type reference；2,138 个 Unresolved 仅从拟合中排除，仍保存在派生标签表与源数据中。GPU 正式拟合使用 seed 20260928、250 epochs、batch 2,500，已完成模型、posterior、signature、history 和 QC 图导出。
- curated-v2 QC：全部自动门槛通过，人工审查确认 macrophage 的 C1QA/B/C、TYROBP、FCER1G、CTSS、MS4A7、CD68、LST1 均进入 top 500；Ig signature fraction 由 3.59% 降至 0.12%，top 10 无 Ig 基因；14 类 signature 有效，loss 收敛。Plasma/B、Monocytes、Neutrophils 的 marker 结构保留。Macrophages 偏向 PI 样本，健康组织迁移的验证仍有限。
- 下一步：先向用户汇报审计和 reference QC，等待 Phase 4B-4 的单独指令；当前不要进行 mapping
- 关键输出：`scripts/18_audit_myeloid_plasma.py`、`scripts/19_myeloid_plasma_neighborhood.py`、`scripts/20_curate_myeloid_plasma_labels.py`、`notes/PHASE4A_MYELOID_PLASMA_AUDIT.md`、`scripts/16_train_cell2location_reference.py`、`scripts/17_qc_cell2location_reference.py`
- 是否通过 QC：curated-v2 reference 通过；Phase 4B-4 未启动
- 是否 push：否
