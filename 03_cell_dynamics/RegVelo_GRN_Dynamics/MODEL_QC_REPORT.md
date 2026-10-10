# 模型 QC 与真实复现 / Executed model QC

正式计算入口统一CLI，源数据为官方zebrafish_nc与zebrafish_grn。完整证据见[执行快照](examples/official_zebrafish/execution_evidence/run_state.json)、[配置](config/official_zebrafish.json)、[数值指标](examples/official_zebrafish/execution_evidence/scientific_metrics.json)和[27张真实图](gallery/README.md)。PASS限于对应实际计算；本次不宣称论文全部数值精确复现。

## 训练与数值 / Training and numerics

- 保留全部697细胞，原8012基因按官方velocity/GRN规则筛至1007；82个TF，4380条先验边。S/U已处理且非整数，未重复归一化；GRN方向有25条命名边断言。
- 官方REGVELOVI hard模式，seed0，max_epochs1500，batch256；实际记录624 epochs、early stopping patience45，耗时735.531秒。validation loss由2970.6580到-2076.7166，最小-2129.4185在零基epoch578。所有单指标真实记录有限；history outer join的437个结构性空位不作为NaN训练失败。
- 权重有限、保存重载参数完全一致：PASS。保存最终模型及每50 epoch原生checkpoint；周期保存的最佳checkpoint为epoch549，不声称保存了每个epoch的最佳参数。optimizer自动续训NOT_IMPLEMENTED；--resume只跳过完整成功阶段。
- hard/soft/soft_regularized均200×894、2epochs小样本接口PASS，velocity维度与有限值PASS；soft两份注册AnnData的UUID造成文件hash改变，但全部表达、层、名称、图和GRN逐项相等。正式三策略比较NOT_RUN，正式多训练seed比较NOT_RUN。

## 动力学与基线 / Dynamics and baseline

velocity、fit_t、latent time、velocity graph及UMAP投影均真实计算。正式均值用30后验样本，velocity_std用10次后验采样；normalized latent_time范围[0,1]，mean fit_t范围[4.462356,8.327559]，二者字段已分别登记。

阶段ordinal与latent time Spearman rho=0.789570，支持阶段排序相符；不是小时标定，也不是供者级统计检验。数据3ss仅2细胞，阶段与样本不平衡须保留。

scVelo stochastic真实基线已运行。同细胞/基因的UMAP速度cosine中位数0.8855，20.23%投影方向相反。存在方法分歧；UMAP相似度不是高维/实验真值准确率。scVelo dynamical、veloVI和官方ModelComparison数值比较NOT_RUN。

## CellRank与终末定义 / Fate QC

纯VelocityKernel、GPCCA7macrostates、每terminal30细胞，按官方教程四个终末名称。transition非负、有限，所有当前行和误差≤5.6e-16；fate有限、[0,1]，直接求解baseline行和最大误差5.22e-15。

显式use_petsc=False使用SciPy direct，修复缺PETSc时默认fallback改成GMRES的历史误差3.83e-5。原失败概率/日志保留；当前概率没有人工归一化或放宽QC。

所有terminal细胞取自17–18ss或21–22ss，支持晚期状态；head/hox34/Pigment各30细胞均与同名注释相符。mNC_arch2集合22个arch2+8个arch1，保留这一混合边界，不能声称4组完全纯净。所有KO固定这120个终末cell IDs并显式保留列顺序，不按扰动重新挑选terminal。

## GRN与虚拟扰动 / GRN and regulon KO

0.001阈值有4379有效边，全部先验支持，丢失1条、新增0条；符合hard模式限制。fc1为target×regulator，expression Jacobian由官方API计算且分组独立归一化，只解释组内相对权重，不比较跨组绝对强度。边的实验支持NOT_CHECKED，不把prior或模型连接当已验证直接调控。

elf1阻断100条边、nr2f5阻断106条边，effects=0。配对load+抽样前同seed，no-op和无有效下游边gene BX571715.1的velocity/fate最大差均0：PASS。BX571715.1是软件无边对照，不是已知生物学阴性TF。实际结果集成5个检查PASS（训练/维度、transition/fate守恒、null、两个KO对齐及阻断）。

| 参考趋势 | 本次实际mean fate差 | 官方depletion AUC | 比较 |
|---|---:|---:|---|
| elf1 KO→Pigment depletion | -0.018420 | 0.543938 | 方向一致 |
| nr2f5 KO→head mesenchymal depletion | -0.011644 | 0.558396 | 方向一致 |

AUC=0.5为中性，>0.5指向模型内depletion，<0.5指向enrichment。官方p来自pooled-cell单侧ranksums(KO<baseline)，BH在每TF四个terminal内校正，不能解释为独立供者/胚胎重复或真实CRISPR实验显著性。mean fate差是条件概率差，不是表达log2FC。

## 稳定性 / Prespecified sensitivity

状态 **PASS**；[完整QC](examples/official_zebrafish/execution_evidence/STABILITY_QC.json)、[汇总](examples/official_zebrafish/execution_evidence/sensitivity_summary.csv)、[逐比较](examples/official_zebrafish/execution_evidence/sensitivity_comparisons.csv)。同一训练seed0模型，后验seed0/1/2，各30样本，cutoff0/0.001/0.01和最强绝对权重50%靶集，均在运行前指定。

后验cell-effect Spearman最低0.999951；cell-fate差Spearman最低0.996906；两侧mean差绝对值>1e-4的方向一致率1.0。验收阈值为effect相关≥0.8且上述非微小方向同号；cutoff/half-target作为诊断，不自动归入训练稳健性。无非微小差时方向没有可检验证据。

保护的正式模型/fate/terminal源hash未改变：True。独立稳定性H5AD清除未重算的旧velocity_std/graph/umap投影，保留本次velocity、fate、transition、CSV；不将继承SD或箭头当新结果。

- cutoff：cell-effect Spearman范围[0.999999, 1.000000]；cell-fate差Spearman范围[0.999981, 1.000000]；16个非微小均值比较中16个同号。实际值见逐比较CSV，不把诊断自动当实验稳健性。
- target_subset：cell-effect Spearman范围[0.997893, 0.999934]；cell-fate差Spearman范围[0.656752, 0.996745]；8个非微小均值比较中8个同号。实际值见逐比较CSV，不把诊断自动当实验稳健性。

最强50% nr2f5靶集阻断53边，head mesenchymal meanΔfate=-0.008628（全靶集-0.011644）；hox34逐细胞Δfate与全靶集相关降到0.656752，尽管均值方向同号。这显示命运变化的空间分布和幅度仍依赖靶集，不能用后验稳定性PASS概括为所有条件稳健。

模拟后显式注销仅本次模型manager，真实记录见MANAGER_RELEASE_QC；不清空无关注册表。早期运行在内存压力下中断，来源审查确认强引用机制，但没有测量其对耗时的因果贡献。恢复版曾在DataFrame.pop(key,None)清理时失败，已修复并完成3项复现回归；旧失败日志保留。缓存校验保护源、配置、完成产物hash及名称/概率；fingerprint没有纳入软件/算法版本，跨版本需独立结果目录与版本核验。

15个预设条件已完成，其中3个baseline、12个TF条件；相同seed与完全相同修改权重的3个cutoff条件复用真实结果，并在targets JSON逐条标记。恢复进程8次新模拟完成后两种manager桶计数均为0。恢复日志记录4个完整条件的checksum校验和复用；没有重训或挑选后验seed。

## 偏离与未执行 / Limits

正式保留全697细胞；batch256不同于教程默认fullbatch，PCA30不同于教程50，KO cutoff0.001不同于示例cutoff0。后验配对方式与冻结terminal是本模块对照选择。因此这是官方API与真实完整案例复现，不是所有论文数值的精确复刻。

Perturb-seq真实实验对照、多个完整训练seed、正式soft策略比较、邻域/terminal敏感性、dynamical/veloVI基线、clean-room环境重建、WSL/Linux验证均NOT_RUN。论文Cell全文与Figshare项目页403；DOI、固定源码与直接官方数据文件可核验，原始Smart-seq3 GEO/SRA accession UNKNOWN。种植体周围炎输入审计已完成但目前没有READY队列，不能执行其RegVelo/JUND命运预测。

## 历史错误及修复 / Preserved diagnostics

wrapper遮蔽官方regvelo导入、object-dtype history检查、outer-join空位判断、missing-PETSc solver fallback、dict terminal排序、stream linewidth NaN、Gallery NULL标签解析与状态配色已修复并重验。历史记录用于追溯，不代表当前阶段FAIL。所有分析/图件由实际数值生成，无复制教程结果、占位图片或研究数据替代。
