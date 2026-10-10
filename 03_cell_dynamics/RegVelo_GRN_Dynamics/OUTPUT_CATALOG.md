# 输出图谱 / Output catalog

本表登记理论支持的主要输出，**不自动代表已复现**。本次697细胞正式案例已生成27/27类图件，均PASS（渲染与数值来源范围）；真实状态以 `run_state.json`、逐图metadata及[Gallery](gallery/README.md)更新PASS/PARTIAL/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE。没有可用输入时说明原因，不生成占位图。每张实际图保存PNG/SVG/PDF与来源CSV、参数、生成命令和输入路径。

统一代码入口为 `scripts/regvelo.py visualize --config <job.json>`；数值阶段按表指定。本次实际文件名为 `figures/<ID>.{png,svg,pdf}`，来源表为 `<ID>_source.csv`；各科学问题与算法见下表，真实预览与逐图命令见Gallery。相同cell_type固定配色，连续数值使用viridis或适用diverging palette；Control / Perturbation清楚标记。所有数值图来自实际计算，不转载官方图冒充复现。

## A. 数据QC / Data QC

| ID / 英文图名 / 中文图名 | 科学问题 | 输入与计算 | 输出与代码阶段 | 生物解释 / 不适用情况 | 本次实际状态 |
|---|---|---|---|---|---|
| A01 Cell Type UMAP / 细胞类型 | 已有注释在低维空间如何分布？ | 真实X_umap + cell_type，原坐标散点 | `figures/A01.{png,svg,pdf}`；audit/prepare→visualize | 展示注释而非重新认证；无embedding/注释不适用 | PASS |
| A02 Development Time UMAP / 发育时间 | 真实采样时间与状态一致吗？ | 实际time_key及UMAP | `figures/A02.{png,svg,pdf}`；prepare→visualize | 疾病分组不是真实时间；无时间标签NOT_APPLICABLE | PASS |
| A03 Spliced / Unspliced QC / 剪接质量 | 两层有足够信号吗？ | cell totals/detection/sparsity，分布与关系图 | `figures/A03.{png,svg,pdf}` + input_cell_qc.csv；audit→visualize | 计数深度不能代表动态强度；无真层阻断 | PASS |
| A04 GRN Coverage / 先验覆盖 | 保留多少TF、target和edge？ | 原/处理名称与先验，交集与过滤统计 | `figures/A04.{png,svg,pdf}`；prepare→visualize | 交集不是本组织有效调控证据；无来源先验阻断 | PASS |

## B. RNA动力学 / Dynamics

| ID / 英文图名 / 中文图名 | 科学问题 | 输入与计算 | 输出与代码阶段 | 生物解释 / 不适用情况 | 本次实际状态 |
|---|---|---|---|---|---|
| B01 Velocity Stream / 速度流 | 估计局部变化方向是什么？ | 正式velocity_graph + UMAP，scVelo stream | `figures/B01.{png,svg,pdf}`；velocity→visualize | 投影的模型场，非实测迁移/谱系 | PASS |
| B02 Velocity Arrow / 速度箭头 | 单细胞/网格方向是否一致？ | velocity_embedding + UMAP | `figures/B02.{png,svg,pdf}`；velocity→visualize | UMAP投影会失真，无有效velocity不适用 | PASS |
| B03 Latent Time / 潜在时间 | 模型相对动态状态如何排序？ | posterior latent time及UMAP/分布 | `figures/B03.{png,svg,pdf}`；velocity→visualize | 不等于采样年龄或临床病程时间 | PASS |
| B04 Velocity Phase Portrait / 基因相图 | 代表基因动力学拟合合理吗？ | 真spliced/unspliced、moments、gene velocity | `figures/B04.{png,svg,pdf}`；velocity→visualize | 代表基因有选择依据；无信号基因说明不适用 | PASS |
| B05 Training Curve / 训练曲线 | 训练有收敛/数值异常吗？ | 真实train/validation history | `figures/B05.{png,svg,pdf}` + tables/training_history.csv；fit→visualize | loss下降不保证生物方向正确 | PASS |
| B06 Velocity Uncertainty / 速度不确定性 | 后验动态估计稳定吗？ | 保存的posterior SD（velocity_std），跨基因均值 | `figures/B06.{png,svg,pdf}`；velocity→visualize | 采样变异不是供者置信区间；单draw不足 | PASS |
| B07 RegVelo vs scVelo / 速度基线 | 相同数据不同模型差异在哪里？ | 正式RegVelo与实际scVelo baseline | `figures/B07.{png,svg,pdf}`；velocity基线→visualize | 同输入方法相关证据，不是独立实验验证 | PASS |

## C. 细胞命运 / Cell fate

| ID / 英文图名 / 中文图名 | 科学问题 | 输入与计算 | 输出与代码阶段 | 生物解释 / 不适用情况 | 本次实际状态 |
|---|---|---|---|---|---|
| C01 Macrostates / 宏状态 | transition支持哪些状态？ | CellRank kernel + GPCCA | `figures/C01.{png,svg,pdf}`；fate→visualize | 模型状态而非重新命名细胞类型 | PASS |
| C02 Terminal States / 终末状态 | 终末细胞由什么支持？ | terminal cell IDs、注释/时间、macrostate | `figures/C02.{png,svg,pdf}`；fate→visualize | 无可信终末定义NOT_APPLICABLE | PASS |
| C03 Fate Probability / 命运概率 | 细胞对指定终末状态的吸收概率？ | 实际fate矩阵与UMAP | `figures/C03.{png,svg,pdf}`；fate→visualize | 以模型/terminal为条件，不是体内观测频率 | PASS |
| C04 Commitment Score / 命运集中度 | fate分布是否集中？ | 1−Shannon entropy(p)/log₂(4)，保留逐细胞值 | `figures/C04.{png,svg,pdf}`；fate→visualize | 自定义指标注明公式，非实验commitment | PASS |
| C05 Fate Probability Heatmap / 命运热图 | 细胞/状态概率模式？ | 同terminal列fate表，明确聚合/排序 | `figures/C05.{png,svg,pdf}`；fate→visualize | 聚合不创造独立重复；保留cell-level表 | PASS |

## D. GRN与regulon / Regulatory networks

| ID / 英文图名 / 中文图名 | 科学问题 | 输入与计算 | 输出与代码阶段 | 生物解释 / 不适用情况 | 本次实际状态 |
|---|---|---|---|---|---|
| D01 TF–Target Network / 调控网络 | 候选TF连接哪些target？ | 实际edge表、weight/cutoff、prior标记 | `figures/D01.{png,svg,pdf}`；grn→visualize | 网络边不自动是已证实直接调控 | PASS |
| D02 GRN Adjacency / 邻接热图 | 对齐后的网络结构与符号？ | named prior/inferred matrix、可审查子集 | `figures/D02.{png,svg,pdf}`；grn→visualize | 子集选择透明，未显示边仍保留全表 | PASS |
| D03 Regulon Ranking / 调控子排序 | 有效target及TF排行？ | actual edge/target weight或官方regulon | `figures/D03.{png,svg,pdf}`；grn→visualize | 排名定义保留，不证明TF必需性 | PASS |
| D04 Regulatory Weights / 权重分布 | 参数/局部GRN有何结构？ | fc1 weights与inferred Jacobian分开 | `figures/D04.{png,svg,pdf}`；grn→visualize | 权重与Jacobian不同，不是表达log2FC | PASS |
| D05 Prior vs Inferred / 先验与推断 | 哪些边保留或新出现？ | 对齐prior、inferred、同cutoff | `figures/D05.{png,svg,pdf}`；grn→visualize | 新边仅计算预测；hard/soft规则分别解释 | PASS |

## E. TF虚拟扰动 / Perturbation

| ID / 英文图名 / 中文图名 | 科学问题 | 输入与计算 | 输出与代码阶段 | 生物解释 / 不适用情况 | 本次实际状态 |
|---|---|---|---|---|---|
| E01 Baseline vs KO Velocity / 阻断前后速度 | regulon阻断改变预测场吗？ | 同cells/features baseline/KO velocity | `figures/E01.{png,svg,pdf}`；perturb→visualize | Model-predicted，非真实CRISPR | PASS |
| E02 Cell-wise Perturbation Effect / 每细胞效应 | 哪些cell预测变化较大？ | `||v_KO−v_base||₂`等明确公式 + UMAP | `figures/E02.{png,svg,pdf}`；perturb→visualize | 速度空间距离，不是表达量或患者效应 | PASS |
| E03 Fate Probability Difference / 命运概率差 | 冻结终末定义下概率变化？ | `p_KO−p_base`、相同terminal cell IDs | `figures/E03.{png,svg,pdf}`；perturb→visualize | 概率差有正负，不是实验富集量 | PASS |
| E04 Depletion / Enrichment / 命运减少增加 | 官方统计量支持何种倾向？ | 官方cellfate_perturbation及其定义 | `figures/E04.{png,svg,pdf}`；perturb→visualize | depletion likelihood不是实验P值/效应量 | PASS |
| E05 TF Perturbation Ranking / TF扰动排行 | 不同有效TF的预测如何排序？ | 多TF同输入/terminal、明确效应指标 | `figures/E05.{png,svg,pdf}`；perturb→visualize | 单TF不能多TF比较；无有效target不适用 | PASS |
| E06 GRN Before / After KO / 网络阻断对照 | 实际阻断哪些连接？ | baseline与perturbed named weights及cutoff | `figures/E06.{png,svg,pdf}`；perturb→visualize | 模型阻断，不代表真实细胞全部功能消失 | PASS |

## 数值与对象 / Tables and objects

必需配套：输入/处理统计、带名称GRN、TF–target edge表、权重矩阵、regulon排名、loss、velocity/latent time AnnData、transition稀疏矩阵、macrostate/terminal IDs、baseline/KO fate CSV、cell-wise effect、no-op/稳定性表、配置/软件版本/来源hash/模型hash/执行日志。某阶段未完成时不建立空科研表假装结果。

cell-state相关TF Jacobian、Markov模拟与真实Perturb-seq比较可作为附加图，但必须有实际结果、定义和独立状态。所有已生成图的metadata含科学问题、方法、input path、source CSV、命令、参数、palette、theme、状态和解释边界；Gallery保留可点击完整入口。
