# RegVelo 新手使用指南 / Beginner guide

## 1. 到哪里找 / Locate the module

从本仓库 [METHOD_INDEX](../../METHOD_INDEX.md) 搜索 `regvelo_grn_dynamics`，或直接进入 `03_cell_dynamics/RegVelo_GRN_Dynamics`。真实数据、模型、环境和运行目录从配置及 `resolved_config.json` 查找；它们不全部存入 GitHub。

先读 [数据要求](DATA_REQUIREMENTS.md) 和 [环境报告](ENVIRONMENT_REPORT.md)。不要在现有Seurat/Scanpy环境里直接升级全部包。文档可读、CLI可启动与模型可用是不同状态。

## 2. 启动环境 / Start the environment

环境报告列出本次已验证解释器和依赖锁。Windows使用该隔离环境的 `Scripts/python.exe`；WSL/Linux使用 `bin/python`。`python --version`、`python -m pip check` 是环境核查，不能替代模型测试。

以下命令在**本模块目录**执行；将 `python` 替换为环境报告中的实际解释器。仅复制命令不会下载全部来源；先按官方清单准备已校验数据。

```powershell
python scripts/regvelo.py --help
python scripts/regvelo.py audit --config config/official_zebrafish.json
```

审计失败先查看配置、输入层、名称与日志；不要为了出现结果而删除校验。执行阶段和耗时记录在配置 `output` 下 `run_state.json`。

## 3. 官方数据在哪里 / Official data

API为 `rgv.datasets.zebrafish_nc()` 与 `rgv.datasets.zebrafish_grn()`，具体来源、文件名、下载大小、hash和缓存见 `OFFICIAL_SOURCE_MANIFEST.csv` / 官方案例记录。真实Perturb-seq是另一个输入，不能用基础发育数据替代。源码的版本与数据下载API要一致。

`config/official_zebrafish.json` 指向正式数据和独立输出；`config/smoke.json` 是明确缩小的接口测试。先核对两者输出路径，不能让smoke覆盖正式模型。

## 4. 重跑官方案例 / Rerun the case

```powershell
python scripts/regvelo.py all --config config/official_zebrafish.json --resume
```

需要分步检查时按 `audit → prepare → fit → velocity → fate → grn → perturb → visualize → report`。实际 `all` 阶段顺序由CLI源码确定；各阶段依赖已经保存的产物。不要把 `fit` 成功解释为CellRank/KO也成功。

```powershell
python scripts/regvelo.py fit --config config/official_zebrafish.json
python scripts/regvelo.py velocity --config config/official_zebrafish.json
python scripts/regvelo.py fate --config config/official_zebrafish.json
python scripts/regvelo.py grn --config config/official_zebrafish.json
```

已有结果直接查看Gallery无需训练；重新出图运行 `visualize`，汇集当前状态运行 `report`。模型训练策略、后验/seed及终末定义修改后，应使用新的独立输出并保留旧配置。

[教学 notebook](examples/official_zebrafish/01_regvelo_teaching.ipynb) 按相同阶段读取真实状态、QC、数值表和图件索引。其代码单元全部 `execution_count=null`、无预填输出，默认只读结果；只有显式开启对应运行开关才调用训练或重算命令。Notebook 尚未执行，不将已有 CLI 结果冒充 notebook 输出。

## 5. 用自己的数据 / Use your own data

复制已有JSON配置到自己的项目工作目录，替换 `input`、`grn`、`output`、`group_key`、`time_key` 和对应参数。相对路径按**配置目录**解释。填写实际物种、gene ID和已有QC来源；保留sample/donor和病理分组。没有真实时间列可使用null，疾病分组不能填作连续真实时间。

H5AD必须存在真实 `spliced` / `unspliced`。普通10x expression、log1p或integrated数据不满足这一条件。先运行audit；缺层时检查已有原始测序文件是否能计数，或按数据要求转向不依赖velocity的方法。

```powershell
python scripts/regvelo.py audit --config path/to/my_regvelo.json
python scripts/regvelo.py all --config path/to/my_regvelo.json --resume
```

第二条只在审计及动力学问题成立后执行。CellRank是否适用还需要同一谱系连续状态与可信终末定义；准入不是“找到文件即可READY”。

## 6. 加入GRN / Add a prior

命名矩阵 CSV 使用默认 `grn_format="matrix"`；TF Atlas / CollecTRI 的 `source,target,weight` CSV 使用 `grn_format="edge_list"`，不需要把重复 source 行删成每个 TF 只有一条边。两者都声明 regulator/target 方向：`target_by_regulator` 表示行 target、列 TF；`regulator_by_target` 相反。auto 方向不能唯一识别时应改配置而非猜测。

在自己的完整配置中加入以下先验字段；列名与原文件不同则修改 `grn_columns` 的值：

```json
{
  "grn": "../data/collectri.csv",
  "grn_format": "edge_list",
  "grn_orientation": "regulator_by_target",
  "grn_columns": {"regulator": "source", "target": "target", "weight": "weight"}
}
```

```powershell
python scripts/regvelo.py audit --config path/to/my_regvelo.json
python scripts/regvelo.py report --config path/to/my_regvelo.json
```

检查 `output/INPUT_AUDIT.json` 的 `grn` 覆盖、缺层和 issues，再查看 `ANALYSIS_REPORT.md`。缺 S/U 时 audit 返回 exit 1，仍保存 GRN 证据；report 可完成失败汇总，未执行阶段显示 `NOT_RUN`。这时不要接着运行 `all` 或把覆盖量当作有效 KO target 数。

人类 CollecTRI 不直接用于斑马鱼或小鼠；名称匹配不会自动完成物种判断。记录 prior 出处、版本/hash、权重含义与 ID 映射，保留原 CSV 的 `resources/references`。适配器拒绝重复 source–target 对；原 signed weight 会进入命名矩阵，但官方预处理生成二值 skeleton，不能据此声称模型验证了激活/抑制。详见 [数据要求](DATA_REQUIREMENTS.md)。

训练策略Hard/Soft/Soft regularized见 [方法卡](METHOD_CARD.md)。不要只改变名字而实际运行相同参数；未执行的策略保持NOT_RUN。

## 7. 对指定TF虚拟KO / Virtual TF knockout

官方zebrafish教程的有效候选先检查 `elf1` / `nr2f5`。已有正式模型及baseline fate之后运行：

```powershell
python scripts/regvelo.py perturb --config config/official_zebrafish.json --tf elf1
python scripts/regvelo.py visualize --config config/official_zebrafish.json
python scripts/regvelo.py report --config config/official_zebrafish.json
```

自己的项目可用 `--tf JUND`，但必须先确认JUND在该模型的有效regulator中、有通过cutoff的下游连接，且输入人类数据真的满足velocity条件。gene names大小写敏感。找不到TF不是“KO无效”的生物学结论。

RegVelo阻断模型下游regulon权重，不是RNA counts置零或真实CRISPR。看baseline/KO velocity、cell-wise距离、fate差、官方统计量与no-op；预测稳定性失败和供者方向冲突必须保留。不要按期望方向反复改seed或target面板。

已有模型的后验和靶集敏感性另行运行（不会重训）：

```powershell
python scripts/validate_perturbation.py --config config/official_zebrafish.json --resume
```

固定同一训练模型，比较后验seed 0/1/2、cutoff 0/0.001/0.01和最强50% targets。结果保存在 `output/stability/`；运行中以 `SENSITIVITY_STATE.json` 查看已完成条件，只有最终 `STABILITY_QC.json` 才给出完整验收结论。它不是多个训练seed比较。修改TF仅运行perturb阶段，修改后的all --resume会因整体配置hash变化重新运行早期阶段。

## 8. 查看图与可信度 / Inspect the figures

[Gallery](gallery/README.md)按“预览→科学问题→数据→代码→数值表→命令”索引；[OUTPUT_CATALOG](OUTPUT_CATALOG.md)列出理论支持与实际状态。PNG用于预览，SVG/PDF用于编辑；公开Gallery是压缩代表图，本机输出保存高质量版本。

先看 `MODEL_QC_REPORT.md` / [验证标准](MODEL_VALIDATION.md)：loss、NaN、速度方向、prior覆盖、transition/fate概率守恒、同terminal定义、no-op、seed/posterior和cutoff稳定性、scVelo基线。训练loss下降或一张漂亮UMAP不支持疾病因果结论。

## 9. 继续中断任务 / Resume

```powershell
python scripts/regvelo.py all --config config/official_zebrafish.json --resume
```

`--resume` 仅跳过同解析配置且完整产物存在的PASS阶段。不要删除 `run_state.json` 来掩盖失败。模型checkpoint是否包含完整optimizer状态、能否继续训练，以实际保存接口和日志为准；CLI不是任意checkpoint自动恢复器。

错误详情在 `output/logs/<stage>_error.log`，统一日志在 `logs/workflow.log`。保存输入hash、seed、软件版本、解析配置和最后有效产物；环境/数据受阻仍可继续独立的本地数据审计和报告。
