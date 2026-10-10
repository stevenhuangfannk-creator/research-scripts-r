# 数据准入 / Data requirements

## 必需输入 / Required input

| 输入 | 必需证据 | 失败时处理 |
|---|---|---|
| `input` H5AD | 唯一 `obs_names`、`var_names`，可追溯物种、来源和细胞筛选 | 报错并保留原对象 |
| `spliced` / `unspliced` | 同 shape、非负、有限、真实剪接来源；区分 raw / normalized | 缺失层拒绝 velocity 建模 |
| raw counts | 可区分 counts 与 log1p/scaled/integrated；记录保留位置 | 来源不明则限制/阻断准入 |
| `group_key` | 既有细胞注释、QC及注释来源；必要时限定谱系 | 不自动发明亚群 |
| 样本元数据 | sample/donor、技术、组织、分组、批次 | 不将 cell 当独立生物重复 |
| `time_key` | 如提供，必须是真实采样时间/发育标签 | 疾病分组不能假装时间 |
| GRN | 命名矩阵或命名边列表 CSV、regulator/target方向、物种、ID、来源及证据类型 | 方向/名称歧义拒绝 |

JSON 的 `input`、`grn`、`output` 必填，相对配置文件解析。`output` 不能是输入文件本身。原始数据只读；不要把新结果写入 Atlas 已冻结的原对象。

## GRN 命名与方向 / Named network orientation

`grn_format="matrix"` 为默认：矩阵 CSV 第一个索引列为该矩阵行的 gene names，其余列名为另一轴。`regulator_by_target` 表示行 TF、列 target；`target_by_regulator` 表示行 target、列 TF。内部返回 `target_by_regulator`，训练时再次核对官方张量方向。当前读取器使用逗号分隔 CSV；TSV 应先在独立文件中转换为 CSV。不要给未命名数组强行指定方向。

`grn_format="edge_list"` 读取 TF Atlas / CollecTRI 命名边列表 CSV。默认列为 `source,target,weight`，可在已有配置中加入以下字段（`grn` 路径仍相对配置目录）：

```json
{
  "grn": "../data/collectri.csv",
  "grn_format": "edge_list",
  "grn_orientation": "regulator_by_target",
  "grn_columns": {"regulator": "source", "target": "target", "weight": "weight"}
}
```

适配器按名称保留 regulator 和 target 两端均在输入基因轴的边，使用 signed `weight` 建立命名矩阵；`grn_orientation` 决定返回的矩阵方向，不会倒置 source→target 的生物含义。匹配后没有边、缺列或重复 regulator–target 对会报错，不静默聚合冲突证据。`resources`、`references` 等来源列不作为模型参数，必须保留原 CSV 和版本/hash以追溯支持证据。

CollecTRI 的物种、gene ID及来源需先人工核实，读取器只做名称匹配，不能证明物种相容；人类 prior 不直接用于斑马鱼或小鼠。官方 `set_prior_grn` 可按表达相关性过滤，再按绝对值阈值生成二值 skeleton；因此输入 signed prior、模型权重和实验激活/抑制证据应分别记录。真实 CollecTRI 接口检查见 [collectri_adapter.json](tests/validation_logs/collectri_adapter.json)，其 PASS 只覆盖先验读取和对齐。

两轴唯一、值有限。TF 集合应来自官方 `is_tf`、物种匹配清单或有出处的先验，不能从矩阵较短轴自动认定所有基因均为 TF。gene symbol 大小写和 Ensembl 版本需明确映射，重复 symbol 不静默合并。必须导出对齐前后 cell/gene/TF/edge 数、覆盖率及排除记录。

`auto` 只用于名称交集唯一支持某方向的情况。如果两个轴都能解释为 regulator/target，特别是方阵，必须显式声明。signed prior 要保留来源和符号含义；二值 skeleton 不能解释为实验激活/抑制的证据。

## 预处理要求 / Preprocessing

先审核已有数据。原始层应复制或在原对象保留；normalized/spliced moments 不能替代 raw counts 来源。重新 normalization、HVG 或 UMAP 必须记录必要性，不能覆写既有层以冒充官方输入。

训练使用 `REGVELOVI.setup_anndata(..., spliced_layer="Ms", unspliced_layer="Mu")`。`Ms` / `Mu` 来源于实际适用的 moments 与官方特异 preprocessing；检查有限、非负、细胞/基因一致。若官方数据已有 PCA/UMAP，可复用并记录；moments/neighbors 若重建应保留参数。

## RNA 动力学适用性 / Biological admission

格式检查通过只是工程输入通过。正式建模还需要同一可比较谱系内的连续状态、足够动力学信号、可解释方向、受控批次和可信终末命运。无需强制所有数据具备真实 time series，但不能把 absence of time series 写成有时间证据。

疾病横断面健康/黏膜炎/种植体周围炎不能自动拼接成一条发育轨迹。先按 donor/assay 检查 state 分布、counts 与 velocity，检查循环、双向状态、深度假方向和终末状态不稳。JUND 是待核实候选，不是先验指定的致病主调控因子。

## 缺剪接层时 / Missing splice counts

若仅有 10x gene expression、H5Seurat/RDS 或普通表达矩阵，没有 `spliced` / `unspliced`，不能运行 RegVelo velocity。先检查已有 BAM/FASTQ、参考基因组/注释、barcode与样本映射及可重复计数流程；需要额外大型下载时记录 accession、大小预算和缺口，不无限下载。

CLI `audit` 会记录缺层与 GRN 检查（包括 GRN 自身失败原因）、输入 hash 和已有注释到独立 output 的 `INPUT_AUDIT.json` / `tables/input_cell_qc.csv`，然后返回 exit 1。GRN 覆盖合格不能抵消剪接层缺失；审计证据保留不代表 velocity 已运行。

保留原注释与 QC，速度计数后按 cell/gene IDs 对齐；有重复/缺失不能按行序填入。无原始测序文件时，可以采用 GRN/TF 活性或已准入的其他虚拟扰动引擎，明确其预测尺度和限制。

## 准入评级 / Dataset admission states

`READY`：关键输入与基础动力学 QC 都满足；`CONDITIONAL`：存在可解决且已明确的问题；`NOT_READY`：关键数据或动力学不足；`BLOCKED`：资源/文件不可获取而无法判断。每项写证据、实际检查、缺口和下一步，不能由文件格式或 README 单独赋予 READY。
