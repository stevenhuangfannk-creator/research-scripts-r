---
name: regvelo-grn-dynamics
description: 使用官方RegVelo模型执行GRN感知RNA动力学、CellRank命运和TF regulon虚拟KO；先审查真实spliced/unspliced与命名GRN，复用已有单细胞QC/注释，保留逐阶段运行和稳定性证据。不用普通表达矩阵伪造velocity，不负责重新建立完整Atlas。
---

# RegVelo科研调用 / RegVelo workflow

定位已安装模块：优先读取同Skill的 `scripts/module_path.json`（若安装记录提供），否则在用户当前方法库查 `registry/methods.yml` 的稳定ID `regvelo_grn_dynamics`，进入其 `path`。仓库源码位置是 `03_cell_dynamics/RegVelo_GRN_Dynamics`；本SKILL源码位于模块 `codex_skill/`。路径未确认时做限定检索，不全盘搜索或重新复制开发一套模型。

先读模块 `README.md`、`DATA_REQUIREMENTS.md` 和运行输出中的 `run_state.json`。首次配置/恢复读 `BEGINNER_GUIDE.md` 与 `ENVIRONMENT_REPORT.md`；结果解读读 `METHOD_CARD.md`、`MODEL_VALIDATION.md` 和 `OUTPUT_CATALOG.md`。调用统一 `scripts/regvelo.py`，不从R runner启动，不将模型或大矩阵复制到Skill目录。

## 输入与入口

使用用户指定的H5AD、命名prior、目标谱系/既有注释、TF和独立输出。保留物种、gene/cell/sample/donor ID及QC来源；未知状态身份不凭列名猜测。JSON必填 `input`、`grn`、`output`，相对config目录；gene names大小写敏感。

```powershell
python "<module>/scripts/regvelo.py" audit --config "<job.json>"
python "<module>/scripts/regvelo.py" all --config "<job.json>" --resume
python "<module>/scripts/regvelo.py" perturb --config "<job.json>" --tf JUND
```

`python`指向模块隔离环境。先audit，再依任务使用prepare/fit/velocity/fate/grn/perturb/visualize/report；已有可比模型与产物可复用。`--resume`跳过同配置且产物存在的PASS阶段，不保证任意checkpoint可继续optimizer训练。

先验可用带名称矩阵，或 `grn_format: "edge_list"` 与显式 `grn_columns` 接TF Atlas的source/target/weight；重复边拒绝，物种与ID映射仍须审核。缺剪接层时audit会保存完整INPUT_AUDIT与GRN证据后失败，不能因GRN覆盖足够而继续建模。

已有正式模型后，使用 `scripts/validate_perturbation.py --config <job.json> --resume` 检查预先指定的后验seed 0/1/2、cutoff与最强50%靶集；读取独立stability目录。恢复会校验配置、保护源和已完成条件的hash。它固定一个训练模型，不证明多训练种子稳健性；不能把继承的旧速度投影或SD当新抽样结果。单阶段/稳定性任务可重用模型；修改TF后不要使用all --resume触发配置变更重训。

## 核心决策边界

- 缺真实spliced/unspliced拒绝velocity；普通normalized/counts不能代替。检查已有BAM/FASTQ和计数可能性，记录来源与预算，不无边界下载。
- GRN regulator→target生物方向与矩阵方向都要验证。auto方阵歧义拒绝；显式orientation与名称对齐后才调用官方模型。
- 使用官方REGVELOVI及官方regulon阻断；确认TF存在、有有效target/cutoff，保存baseline。原/KO使用同cells/features和冻结baseline terminal cell IDs。
- KO是Model-predicted regulon阻断，fate差不是实验log2FC，depletion likelihood不是实验显著性。先验边、推断边、实验支持分开。
- 官方depletion likelihood为ROC AUC，0.5中性，>0.5指向模型内depletion；pooled-cell单侧ranksums及每TF内BH不提供供者级实验显著性。CellRank使用显式use_petsc=False保留SciPy direct求解和终末类别顺序断言。
- disease分组不是时间；没有可信同谱系连续动态/终末状态时不强行CellRank。JUND不预设为驱动因子。
- no-op、种子/后验及cutoff对照按验证标准执行；smoke和完整数据训练分别记录。已有DoseDirKO的effect/delta与RegVelo不同尺度。
- 用实际 `run_state.json`、QC、日志和逐图metadata报告PASS/PARTIAL/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE；不沿用官方教程图片或旧例PASS证明本次成功。

完成后给中文输入/真实执行/图件/模型QC/限制/恢复命令。资源受阻保存有效产物与可复现错误，继续可独立进行的审计和报告。GitHub只同步用户授权范围内的代码、说明和已核验小型Gallery；环境、原始患者信息、模型、大矩阵和凭据留在Git外。
