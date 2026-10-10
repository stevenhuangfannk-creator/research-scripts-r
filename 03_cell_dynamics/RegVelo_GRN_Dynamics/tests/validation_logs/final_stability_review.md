# 最终稳定性只读验收 / Final read-only stability acceptance

数值产物验收 **PASS**。不重训、不重算模型、不修改输入、缓存、共享源或报告；HDF5 使用 `r` 模式，仅标准库、h5py、numpy。

- 15 条件完整：3 个 baseline、12 个 TF；checkpoint 的 60 个文件 SHA256 全部匹配。配置/保护源 fingerprint 匹配，fate、model、terminal 三个保护源 SHA256 未改变。
- 15 份 H5AD：697×1007 velocity/fit_t、697×4 fate 形状和有限值通过；细胞、基因、CSV lineage 顺序及 120 个冻结 terminal IDs 一致。fate 在 [0,1] 且行和误差≤1e-10，CSV/H5AD 差≤1e-14；transition 有限、非负、行和通过。
- 15 份清理记录完整，当前 SHA256 与 cleanup-after 及刷新后的 checkpoint 一致；声明清除的旧 velocity 字段均不存在，latent_time 与当前 fit_t 归一化相符。清理前文件未保留，前后 velocity/fate 完全不变依据当时逐元素断言及 PASS 日志；本次不声称重新比较了已不存在的清理前文件。
- manager 有 8 个唯一新模拟记录，两种桶均为 0，与 STABILITY_QC 内嵌记录一致；6 份 execution_evidence 拷贝与运行目录逐字节相同。
- 独立 CSV 子审：summary 48 行、comparison 40 行；12 份 delta 与同 seed fate 差最大 2.22e-16，40 条 Spearman 复核最大差 3.33e-16。effect 均值差≤8.26e-9，符合 float32 保存与均值精度。

**PASS 范围**仅为同一个训练 seed0 模型的后验抽样稳定性：16 个后验比较中 effect Spearman 最低 0.9999507395，fate-delta 最低 0.9969062839，16/16 非微小均值同号。实际门槛为 effect 相关≥0.8、两侧 mean 差绝对值>1e-4 时同号；fate 相关不是额外验收阈值。

cutoff 和最强 50% 靶集仅为诊断，设计为分轴测试而非全因子组合。nr2f5 半靶集 mNC_hox34 的逐细胞 fate-delta rho=0.6567522845，不能概括所有条件稳健；训练 seed 稳定性和生物学验证仍为 NOT_RUN。MODEL_QC_REPORT 的范围说明正确。

文档问题已修复并只读复验：运行目录 `hard_seed0/MODEL_QC_REPORT.md` 副本原有 7 个相对链接断链，主任务已改为真实模块绝对路径；本次确认 7/7 路径存在。模块根报告的 7 个相对链接原本正常。本审查未修改共享报告。

逐文件哈希与逐条件结果见同目录 `final_stability_review.json`。
