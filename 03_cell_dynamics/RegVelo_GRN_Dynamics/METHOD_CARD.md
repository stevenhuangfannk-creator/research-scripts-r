# RegVelo 方法卡 / Method card

## 科研问题 / Scientific question

在具有可识别 RNA 剪接动力学和可信调控先验的同一细胞谱系中，基因调控如何约束 RNA velocity？阻断某个有效 TF 的 regulon 后，模型预测的方向及终末命运概率如何变化？这是模型条件下的候选生成，不是疾病驱动因子或实验 KO 的自动判定。

核心论文：Wang et al., *RegVelo: gene-regulatory-informed dynamics of single cells*, Cell (2026), [10.1016/j.cell.2026.04.022](https://doi.org/10.1016/j.cell.2026.04.022)。官方代码 [theislab/regvelo](https://github.com/theislab/regvelo)，完整复现 [theislab/regvelo_reproducibility](https://github.com/theislab/regvelo_reproducibility)。采用版本、SHA、许可与真实 API 见 `OFFICIAL_SOURCE_MANIFEST.csv`，不从论文年份猜测安装版本。

## 原理 / Model logic

RegVelo 使用官方 `REGVELOVI` 深度生成模型。RNA 动力学的基本关系为 `du/dt = α(s, GRN) − βu`、`ds/dt = βu − γs`：未剪接 RNA 的转录由调控网络约束，剪接与降解决定 mature RNA 变化。模型联合推断细胞动态状态和调控参数；后验估计提供 velocity 与 latent time。数学形式不代表每条边已得到实验验证，非线性模型的权重/局部调控效应也不应解释为普通表达 fold change。

`Ms` / `Mu` 是速度分析 moments，并非原始 spliced/unspliced counts。训练前应保留原始层，明确归一化、特征选择、neighbors 和 moments 的来源。官方数据已处理时优先复用；本模块将派生对象写入独立输出。

## 输入契约 / Input contract

H5AD 需要唯一 cell/gene ID、真实 `spliced` 和 `unspliced`、既有 QC 与注释；GRN 需要明确 regulator/target 名称、物种及证据来源。训练还需对齐的 `Ms`、`Mu` 与有效 TF。支持人/动物取决于网络和基因映射，不因为输入格式正确就视为生物学适用。完整准入见 [DATA_REQUIREMENTS.md](DATA_REQUIREMENTS.md)。

GRN 生物学边为 `TF → target`。本模块内部规范是行 target、列 regulator；外部可声明 `regulator_by_target` 或 `target_by_regulator`。`auto` 只在名称证据能唯一确定时使用，方阵方向歧义会拒绝。官方 `set_prior_grn` / 模型张量接入时的转置以安装源码及名称断言为准，不能仅看尺寸。

## 模型模式与参数 / Constraints and parameters

| 模式 | 官方参数 | 科学含义 |
|---|---|---|
| Hard | `soft_constraint=False` | 调控结构受先验约束；先验遗漏可能限制有效动力学 |
| Soft | `soft_constraint=True`, `lam2=0` | 网络偏离先验按模型损失惩罚，允许模型估计额外关系 |
| Soft regularized | `soft_constraint=True`, `lam2>0` | 在 soft 的基础上使用官方附加正则项；取值需记录 |

该映射已核查官方 `REGVELOVI` / `ModelComparison` 源码。实际配置由本模块 `train` 字段解释；未正式训练的模式在比较报告标 `NOT_RUN`。模型默认 `lam`、`lam2` 与训练 `max_epochs`、`batch_size` 不应混淆。smoke 缩小细胞数、epochs 或采样数必须明确显示，不用于正式三策略比较。

主要可配置项：输入/输出路径、GRN 方向、细胞类型列 `group_key`、真实时间列 `time_key`、随机种子、prepare 过滤/邻居设置、train 参数、posterior 样本数、fate macrostate/terminal 定义、perturb TF/cutoff。TF 名称大小写敏感；`elf1` 是当前官方 zebrafish 教程案例之一，Gabpa/Mitf/Sox10/JUND 需在对应物种与模型中重新核实。

## 组合输出 / Composable outputs

- 核心：审计、处理后 AnnData、模型权重与参数、速度、latent time、GRN 权重、实际执行日志。
- 可组合：CellRank transition / GPCCA / fate、regulon 排名、TF 局部网络、虚拟 KO velocity/fate 对照。
- 质量对照：scVelo 基线、no-op、阴性 TF、后验/种子稳定性、cutoff 敏感性、已知发育信息。
- 独立实验比较：仅当匹配的真实 Perturb-seq 数据和有效设计可用；应分别标 Observed 与 Model-predicted。

全部图件状态及输入、方法、输出登记见 [OUTPUT_CATALOG.md](OUTPUT_CATALOG.md)。本方法登记的候选成熟度不因某一张图渲染成功而晋升。

## 解释与限制 / Interpretation and limits

CellRank fate 是选定 transition 和终末状态下的吸收概率，不是疾病发生概率。终末状态应由真实注释/发育信息与模型结果共同支持；原始和扰动使用相同 cell/gene 顺序及 baseline terminal cell IDs。commitment 定义必须记录，例如 `max fate probability` 只表示概率集中度，不能冒充官方统一生物学指标。

`in_silico_block_simulation` 对训练模型指定 TF 的有效下游权重进行阻断，再推断 perturbed velocity。不是将 TF RNA counts 置零，也不是细胞内全部生物学功能消失。cutoff 控制被移除边，效应依赖先验、模型、后验和状态定义。

官方 depletion likelihood 是对模型命运概率比较的统计量；应按所用版本记录定义、返回值和比较方向。不能称实验效应量、真实 KO 显著性或正确率。本模块自定义 cell-wise velocity 距离/概率差时保留公式、单位和来源，不挪用官方指标名称。

炎症激活可能是循环/可逆状态；横断面 donor、批次或测序深度可能主导方向。没有可信动态过程时不强行 CellRank 终末命运。先验网络中的边分为 prior-supported、model-inferred、experimentally-supported，文献 prior 不等于本组织直接验证。

## 验证与晋升 / Validation

工程契约、官方真实模型执行、模型 QC、稳定性、生物支持分别记录。按 [MODEL_VALIDATION.md](MODEL_VALIDATION.md) 验收，实际状态读取每次 `run_state.json` 和 QC 报告。完整训练、reload、no-op、fate 一致性、baseline 等未通过时保留 `PARTIAL/FAIL/BLOCKED/NOT_RUN`，不能在 README 宣布 PASS。
