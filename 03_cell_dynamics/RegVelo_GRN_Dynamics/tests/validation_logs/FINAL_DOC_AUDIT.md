# 最终文档一致性审查 / Final documentation consistency audit

最新审查快照：2026-10-10 13:45 UTC（Asia/Shanghai 21:45）。状态：**PASS：文档、链接、编码与当前执行证据一致。** 此PASS只针对文档一致性，不是生物学有效性结论；正式多训练seed、正式全模式比较与独立实验验证仍NOT_RUN，Phase10最终Git发布仍待主任务完成。初次13:22快照中报告尚未生成、稳定性仍在执行；这些历史限制已由新证据更新。没有导入重型模型包、训练模型、重算后验或修改共享分析代码/报告。

## 已确认事实 / Confirmed evidence

| 核对项 | 实际证据 | 结论与解释范围 |
|---|---|---|
| 正式运行 | `official_zebrafish/hard_seed0/run_state.json` | audit/prepare/fit/velocity/fate/grn/perturb/visualize/report 9阶段均为执行 PASS；fit 收敛和 velocity 方向仍为 REVIEW_REQUIRED，不能升级为科学有效性 PASS。 |
| 数据与训练 | run_state、fit_qc、velocity_qc | 保留697细胞，8,012基因输入处理为1,007基因；82 regulators，4,380 aligned prior edges；hard training seed0，max_epochs=1500、early stopping 后实际624 epochs、batch256。full-batch偏离明确记录。 |
| 潜在时间 | 当前 `velocity_qc.json` | 未归一的 mean fit_t 范围4.462356–8.327559；normalized latent time范围0–1。stage 仅为明确ordinal，不是elapsed time。Spearman rho=0.7895703不证明方向真值。 |
| 27类图件 | 正式FIGURE_CATALOG、RENDER_QA；公开gallery/catalog及文件清单 | 正式27 PASS、0 FAIL、0 NOT_RUN；公开目录27 metadata、27 PNG、27 PDF、27 source CSV，catalog均PASS。公开SVG为0，原SVG保存在正式本机输出，符合公开压缩预览说明。实际PDF最小7pt、SVG最小7px；最终投稿机械缩小仍需重排版。 |
| GRN与虚拟KO | GRN_QC、perturb_qc、相关source CSV | 4,379/4,380有效prior edges，hard模式0新边；elf1阻断100边、nr2f5阻断106边；no-op和无有效下游边BX571715.1对照差为0。这是模型预测而非CRISPR实验。 |
| PI准入 | `examples/peri_implantitis_audit/audit.csv`及报告 | 准入状态精确为8 NOT_READY、1 BLOCKED、0 READY。8个H5AD均缺真实spliced/unspliced/Ms/Mu。GSE266897独立GEO只有元信息，并不是种植体周围黏膜炎。 |
| 模式smoke | `mode_smoke_summary.json`及comparison CSV | hard/soft/soft_regularized 200细胞、2 epochs、seed0接口检查PASS；明确标SMOKE_TEST_ONLY，不是正式三策略比较。正式多训练seed与完整多策略比较NOT_RUN。 |
| 教学notebook | README/BEGINNER_GUIDE及notebook验证记录 | 所有代码单元execution_count=null，无预填输出；已有CLI结果不冒充notebook执行。 |
| 独立链接与公开来源核对 | 初次 `plot_evidence_check/FINAL_LINK_AUDIT.md` / `.json`；最新 `FINAL_DOC_SNAPSHOT.json` | 新快照10份文档共176个本地链接，0断链；MODEL_QC_REPORT已生成并可解析。初次27份公开source CSV和27份PDF与正式输出SHA-256完全一致；metadata关键输入/科学字段一致，压缩PNG明确preview_only。 |
| 稳定性最终证据 | 正式STABILITY_QC/summary/comparisons与公开execution_evidence副本 | 15条件完成，后验稳定性PASS；3份公开QC/数值文件与正式文件SHA-256完全一致。最低effect rho=0.9999507395、最低fate-delta rho=0.9969062839；16个非微小后验均值比较16同号。 |
| 新文档编码 | `FINAL_DOC_SNAPSHOT.json`；人工阅读MODEL_QC/NEXT_STEPS/README/REPRODUCTION_PLAN | 10份文档严格UTF-8可读，未发现U+FFFD或常见mojibake串。PI报告明确备注GSE188217历史subcluster_state损坏；原审计源JSON不猜测修复。 |

## 必须保留的科学限制 / Scientific limits

1. `figures/C02_source.csv` 显示冻结的 `mNC_arch2` 终末集合包含22个原注释mNC_arch2和8个mNC_arch1。其余head_mesenchymal、hox34、Pigment各30个同名细胞。arch2名称不能解释为纯arch2生物终末身份；不能为了图名改变原细胞注释。最终QC须说明此组成。
2. 已执行基线是scVelo **stochastic**；dynamical为NOT_RUN。静态B07_source.csv的2D投影cosine平均0.5343008444、中位0.8855272470，141/697（20.2296%）<0；dNC_hoxa2b为37/42反向（均值−0.7272674），dNC_nohox为48/104（均值0.0568321），NPB_hox3为12/19（均值−0.1907490）。这些是保存的UMAP投影的描述性结果，不能推出高维方向真值，也不能忽略分歧而声称全面方法一致。
3. 最新 `STABILITY_QC.json` 确认15预设条件完成，后验稳定性PASS。cutoff及half-target仍是诊断，不能一起归入后验验收PASS；half nr2f5 hox34逐细胞fate-delta相关0.6567522845，虽均值同号仍显示靶集依赖。固定训练seed0模型的后验seed敏感性不是多训练seed稳定性。正式多训练seed、全模式及真实生物学/独立Perturb-seq验证NOT_RUN。初次13:22仍未完成的状态已由当前完整QC更新。
4. E04 ROC AUC以0.5为中性；baseline=1、KO=0。官方pooled-cell单侧ranksums及各TF内部BH不提供donor/embryo级独立重复证据。API_NOTES、Skill和Gallery对此解释一致。

## 已反馈并修正的文档问题 / Resolved documentation findings

| 文件与位置 | 初次问题 | 最新核对 |
|---|---|---|
| `references/API_NOTES.md` 最小流程，fate调用 | 两次direct调用遗漏 `use_petsc=False`。 | 已显式补充，两次均为SciPy direct。 |
| 同一最小流程，KO后VelocityKernel调用 | 示例未显式更新继承graph/embedding。 | 已重算KO velocity_graph/embedding，清理未重算SD，并冻结categorical终末细胞及列顺序。 |
| `OUTPUT_CATALOG.md` B06计算栏 | SD与variance混称。 | 已改为保存posterior SD（velocity_std）、跨基因均值。 |
| `BEGINNER_GUIDE.md` 稳定性段 | 输出目录措辞可能被误读为当前已完整。 | 已区分运行中SENSITIVITY_STATE和最终STABILITY_QC。 |
| `gallery/README.md` 第6行与BEGINNER_GUIDE | MODEL_QC_REPORT当时尚不存在。 | 已生成，全部176个本地链接可解析；QC保留22arch2+8arch1、20.23%投影反向及未执行验证边界。 |
| `README.md` 本次执行 | 新稿曾把cutoff/half诊断并称稳定性PASS。 | 已改“后验seed稳定性PASS；cutoff/靶集敏感性已完成并作为诊断”，与最终QC验收范围一致。 |

最终数值快查读取真实CSV/JSON，未重算模型。cutoff的effect rho范围[0.9999990077,1]、fate-delta范围[0.9999814059,1]、16/16非微小同号；half-target的effect rho范围[0.9978928920,0.9999335515]、fate-delta范围[0.6567522845,0.9967445291]、8/8非微小同号，均与MODEL_QC_REPORT一致。NEXT_STEPS将正式多seed/全模式、arch2与基线分歧、raw剪接重计数、实验验证、clean-room/WSL及Planned adapter列为后续工作；未误写为完成。

初次与最新审查证据分别保留；没有直接改动共享文档或分析源。当前未发现需要进一步修正的文档一致性问题。Git最终发布由主任务单独执行与记录。
