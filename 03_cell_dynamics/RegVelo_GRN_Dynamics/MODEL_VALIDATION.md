# 模型与方法验收 / Model validation

验收分工程、方法、稳定性和生物解释。`PASS` 只覆盖已实际执行且通过的检查；`PARTIAL`、`FAIL`、`BLOCKED`、`NOT_RUN`、`NOT_APPLICABLE` 都保留具体原因和日志。不把启动环境、教程已读、代码存在或静态语法检查升级为模型成功。

## 工程检查 / Engineering checks

- CLI help与所有 stage 可解析；JSON 缺键、无文件路径、未解析变量明确报错。
- 路径相对于 config 文件；输出自动创建，原始对象哈希不变。
- 缺 spliced/unspliced 拒绝；负值/NaN、名称重复、shape不符明确失败。
- GRN 通过名称与方向断言，auto 方阵歧义拒绝，TF与target实际对齐。
- 训练保存参数、权重、配置、版本和日志；重新加载恢复同细胞/特征。
- `--resume` 仅跳过相同配置且存在全部实际产物的已完成阶段；checkpoint恢复训练与阶段跳过是不同能力。

软件夹具可验证拒绝行为和路径语义，不能当论文数据或科研结果。

## 训练质量 / Training quality

正式训练记录完整输入的 cell/gene/TF/edge 数、策略、seed、max_epochs、实际停止 epoch、early stopping、batch、硬件及耗时。保存 train/validation loss、数值异常、警告和模型权重；smoke规模和正式规模分别报告。

检查 loss 趋势、有无NaN/Inf、异常发散/过早中止；loss下降并不证明动态方向正确。posterior velocity与latent time维度必须匹配输入、数值有限；latent time分布、边界堆积、细胞类型/真实时间一致性应真实检查。若不具备适合的真实时间列，时间相关性标 NOT_APPLICABLE。

`MODEL_QC_REPORT.md` 必须区分已检查、尚未检查、失败和计算资源限制；不能用统一“模型收敛”替代上述证据。

## Velocity 与基线 / Velocity and baseline

检查 graph/UMAP stream/arrow、代表基因 phase portrait、动力学信号、邻居敏感性与已知发育方向。scVelo stochastic / dynamical 使用相同可比较输入并保留自己的预处理与失败记录；未跑的基线不能仅用文献结论填表。速度不确定性按所用后验定义登记，不用 UMAP视觉相似替代稳定性检验。

## CellRank / Fate analysis

transition 每行和接近1、数值非负有限；fate 矩阵 cell IDs 与 baseline一致、概率界于0和1且每行和接近1。GPCCA宏状态、terminal定义和失败均记录；不为了预期结果任意改名。baseline terminal cell IDs 冻结后用于所有扰动，不能重新选择终末细胞以扩大差异。

## GRN / Regulatory network

先验、推断权重和本组织实验支持分开。hard模式新增有效边应符合官方结构约束；soft模式新增边是预测。保存TF–target edge表、符号、cutoff、prior标记和非零数。不同策略的正式网络比较需相同输入、合理随机重复及明确指标；小样本smoke不能替代正式比较。

## TF KO / Perturbation controls

- Unperturbed baseline：保存原模型、速度和命运定义。
- No-op：用未修改GRN与相同后验随机设置重算；允许定义清楚的采样误差，不能由不一致seed产生显著“扰动”。
- 阴性对照：在模型允许时使用无有效下游边TF或合适阴性TF；不可伪造一个生物学阴性结论。
- 后验/seed稳定性：报告重复数、方向一致性、排名/概率差相关与变化范围。
- target/cutoff敏感性：在预先记录阈值下检查被阻断边与预测变化。
- 原/扰动同cells/features、同terminal cells；TF不存在或无有效边时明示NOT_APPLICABLE/失败原因。

每细胞velocity差可以定义为 `||v_KO − v_baseline||₂`，是模型速度空间距离，不是表达log2FC。fate差是 `p_KO − p_baseline`，不是实验富集量。官方depletion likelihood应记录实现定义与采样条件，不改称实验显著性。

## 真实扰动验证 / Observed perturbations

只有匹配的真实Perturb-seq可用并完成QC时比较。Observed、Model-predicted、Experimentally validated分别标记。真实实验与模型一致/不一致都保留；显著性与共享数据关联不能直接证明因果。未运行该项标NOT_RUN，而非“验证成功”。

## 证据文件 / Evidence

当前运行输出至少保留 `resolved_config.json`、`run_state.json`、`logs/`、审计统计、处理后对象、模型、数值表及逐图生成记录。软件版本、输入hash、来源SHA、模型hash与复现命令是可恢复性证据；原始数据和模型不上传普通Git。实际报告随运行更新，本文是验收标准，不预设结果。
