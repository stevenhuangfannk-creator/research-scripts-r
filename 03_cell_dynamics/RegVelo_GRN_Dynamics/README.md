# RegVelo｜GRN 感知的 RNA 动力学与虚拟扰动 / GRN-informed dynamics

本模块以官方 `REGVELOVI` 为模型，提供独立 Python CLI，将输入审计、GRN 对齐、预处理、训练、RNA velocity、CellRank 命运分析、regulon 与虚拟 TF 扰动串成可追溯流程。输入需要真实剪接计数；横断面疾病分组不自动视为时间进程。

English summary: An independent Python workflow for the official RegVelo model, with named GRN alignment, RNA dynamics, CellRank fate probabilities and regulon-level in silico perturbations. Execution evidence is recorded per run; method availability does not establish biological validity.

**执行状态以本次输出目录的 `run_state.json`、模型 QC 和 Gallery 记录为准。** `NOT_RUN` 是尚未执行；smoke test 仅验证小样本接口。文档、代码或安装成功不等于官方论文完整复现。查看 [复现计划](REPRODUCTION_PLAN.md)、[验证标准](MODEL_VALIDATION.md) 和 [输出目录](OUTPUT_CATALOG.md)。

## 本次真实执行 / Executed case

697细胞正式hard模型训练624 epochs，velocity/scVelo stochastic/CellRank/GRN、elf1与nr2f5 regulon KO及零效应对照均PASS；27/27图已生成。后验seed稳定性PASS；cutoff/靶集敏感性已完成并作为诊断，详见[实际模型QC](MODEL_QC_REPORT.md)。三种策略各200细胞/2epochs smoke PASS，正式多策略和多训练seed比较未执行；当前PI审计8项NOT_READY、1项BLOCKED。

## 入门入口 / Start here

- [RegVelo 新手使用指南](BEGINNER_GUIDE.md)：环境、官方案例、自有数据、TF KO、恢复与报错。
- [方法卡](METHOD_CARD.md)：模型、模式、科学解释和方法边界。
- [数据要求](DATA_REQUIREMENTS.md)：counts、spliced/unspliced、注释与 GRN 准入。
- [Gallery](gallery/README.md)：真实预览、数据、代码、参数与生成命令。
- [官方案例](examples/official_zebrafish/README.md) 与 [种植体周围炎审计](examples/peri_implantitis_audit/README.md)。
- [官方斑马鱼教学 notebook](examples/official_zebrafish/01_regvelo_teaching.ipynb)：读取真实运行证据，所有代码单元尚未执行。
- [Codex Skill 源码](codex_skill/regvelo-grn-dynamics/SKILL.md)：未来任务的薄路由入口。

## 统一 CLI / Unified CLI

在本模块根目录使用已经隔离且检查版本的 Python 环境运行：

```powershell
python scripts/regvelo.py audit --config config/official_zebrafish.json
python scripts/regvelo.py all --config config/official_zebrafish.json --resume
python scripts/regvelo.py perturb --config config/official_zebrafish.json --tf elf1 --resume
```

首次运行前按 [环境报告](ENVIRONMENT_REPORT.md) 准备固定依赖与官方数据。示例 TF `elf1` 仅对应官方斑马鱼案例，不能替换为未检查的基因。命令中的 `python` 必须指向 RegVelo 独立环境；现有 R/Scanpy 环境不应被批量升级。

| stage | 作用 | 前置输入 / 结果 |
|---|---|---|
| `audit` | 检查 layers、名称、注释与 GRN 条件 | H5AD + 带名称的 GRN |
| `prepare` | 速度特征、moments、官方预处理、GRN 对齐 | audit 准入 |
| `fit` | 官方模型训练并保存 | `Ms`、`Mu`、有效 regulator、先验 |
| `velocity` | 后验速度、latent time、velocity graph | 已训练模型 |
| `fate` | transition、GPCCA、终末状态、fate | 有效速度与生物学支持 |
| `grn` | TF–target 权重、regulon 与 prior 对照 | 已训练模型与对齐先验 |
| `perturb` | 官方 regulon-level TF 阻断和 fate 对照 | 有效 TF、baseline 与一致终末状态 |
| `visualize` | 从真实数值导出科研图 | 对应阶段已经产出 |
| `report` | 汇集状态、参数、异常与输出 | 当前运行记录 |
| `all` | 按依赖顺序执行全流程 | 条件不足则记录失败，不补造结果 |

JSON 配置的 `input`、`grn`、`output` 是必填路径，**相对于配置文件所在目录解析**；未解析的环境变量会报错。`output` 必须是独立派生目录。CLI 不通过主库的 R `run_method.R` 启动。

## 命名先验与 CollecTRI / Named priors

GRN 支持命名矩阵 CSV（默认 `grn_format="matrix"`）和 TF Atlas / CollecTRI 命名边列表 CSV（`grn_format="edge_list"`）。边列表默认读取 `source,target,weight`；其他列名通过 `grn_columns` 显式映射。两种格式都应声明 `grn_orientation`，详见 [数据要求](DATA_REQUIREMENTS.md#grn-命名与方向--named-network-orientation) 和 [加入 GRN](BEGINNER_GUIDE.md#6-加入grn--add-a-prior)。

边列表适配器保留输入权重符号，限定两端都在输入基因轴中的边，并拒绝重复 regulator–target 对。物种与 ID 来源由用户核实；同名匹配不等于已验证物种兼容。官方预处理进一步生成二值 skeleton，不将 CollecTRI 的激活/抑制注释直接当成模型已验证调控方向。缺少剪接层时 `audit` 仍保存 `INPUT_AUDIT.json` 的 GRN 检查证据，并以 `FAIL/NOT_READY` 拒绝动力学建模。

## 复用与限制 / Reuse and limitations

与 [TF Atlas](https://github.com/stevenhuangfannk-creator/tf-regulatory-network-atlas) 复用有出处且物种匹配的 prior，与 [Oral Atlas](https://github.com/stevenhuangfannk-creator/oral-scrna-atlas) 复用已有 QC/注释。与 [Workbench](https://github.com/stevenhuangfannk-creator/bioinformatics-research-workbench) 共享方法与实际图件入口；平台是否执行过 adapter 独立记录。Virtual Perturbation Toolkit 当前 DoseDirKO 分数与 RegVelo fate shift 不同尺度，不能合并比较。详见 [外部接口](INTEGRATION.md)。

虚拟 KO 表示阻断模型中的 TF 下游权重，不能称为真实 CRISPR KO。latent time 不是临床病程时间；UMAP 箭头不是实测谱系追踪。缺剪接层时保留数据，进入审计与替代路线，不用 normalized 表达伪造计数。
