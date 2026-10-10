# RegVelo Skill 独立未来调用验收 / Independent forward-use check

执行日期：2026-10-10。现实请求：在现有 Lin 2026 种植体周围炎成纤维细胞数据中对 JUND 做 RegVelo 虚拟 KO，先判断可执行性并提供可复用步骤。

## 结论 / Decision

当前 `NOT_READY`。能启动 CLI、导入官方 RegVelo，但现有真实 H5AD 没有 `spliced/unspliced`，不能运行 velocity 或 JUND KO。没有训练、下载安装、真实/虚构预测或 GitHub 发布。本检查在读取 Skill 后独立完成，没有读取已有 peri_implantitis_audit 报告或其他代理结论。

## 实测输入 / Observed input

指定候选 `C:/Users/13683/Desktop/scriptsR/reproductions/lin_2026_peri_implantitis/data/processed` 不存在。按项目 README、文件目录和来源 metadata 定位至：

- canonical：`results/phase4a/phase4a_preliminary_integrated.h5ad`，92,112 cells × 21,934 genes；只含 `counts` 层；15,939 `major_cell_type=Fibroblasts`；JUND 在基因轴；cell/gene IDs 均唯一。
- curated-v2 cell2location 输入：`results/phase4b/cell2location_input/curated_v2/scrna_reference_counts.h5ad`，89,974 × 17,211；只含 `counts`；同有 15,939 Fibroblasts，但 JUND 不在基因轴。不可将该参考对象作为 JUND 保留的 RegVelo 输入。
- 既有 annotation 列来源于本地复现，不当作已验证作者亚群或终末状态。保留 `donor_id/sample_id/condition/source_dataset`，`time_key=null`。疾病分组不能作为时间。
- CollecTRI CSV 是 `source,target,weight,resources,references,sign_decision` 边列表，共 43,175 边，无重复 source-target 对；JUND 有 108 条确切边，其中 105 targets 在 canonical gene axis；匹配 canonical 两端的边共 40,877。这个先验覆盖不等于模型有效 target 数。
- 在本项目 `data/raw` 范围限定检索没有找到 BAM/FASTQ/loom；可见 PI 10x、healthy 10x、spatial 目录。不据此声称全电脑或公共来源没有测序文件。

完整只读 metadata 在 `input_evidence.json`。原对象不覆写；`source_readonly_hashes.json` 记录两对象复核前后 SHA256、大小和 mtime 完全相同。canonical SHA256 `c96701c4e0d079b8e9c08b8fbcd754910040367399f6884300852b8ea72e9f0a`，同时匹配已有来源记录；curated-v2 SHA256 `819926cc643ebc44c83f2fea7ea31133b809f5c63cd0308b6ae50deec99b7b1b`。

## 实际命令与证据 / Executed commands

工作目录为当前 workspace。命令中的 `python.exe` 是明确的已装隔离环境：

```powershell
$regveloPython = 'C:/Users/13683/Documents/Codex/2026-10-10/files-pasted-by-the-user-codex/outputs/regvelo_runtime/.venv/Scripts/python.exe'
$regveloCli = 'C:/Users/13683/Documents/Codex/2026-10-10/files-pasted-by-the-user-codex/outputs/research-scripts-r/03_cell_dynamics/RegVelo_GRN_Dynamics/scripts/regvelo.py'
& $regveloPython $regveloCli --help
& $regveloPython $regveloCli audit --config 'C:/Users/13683/Documents/Codex/2026-10-10/files-pasted-by-the-user-codex/work/forwardtest/job.json'
& $regveloPython $regveloCli report --config 'C:/Users/13683/Documents/Codex/2026-10-10/files-pasted-by-the-user-codex/work/forwardtest/job.json'
& $regveloPython -m pip check
```

| 检查 | exit | 观察 |
|---|---:|---|
| --help | 0 | 找到 audit/prepare/fit/velocity/fate/grn/perturb/visualize/report/all；--config 必填 |
| audit | 1 | 2.328s；`Missing required RNA layers: spliced, unspliced. Expression cannot reconstruct splicing counts.` |
| report | 0 | 生成真实失败汇总；没有模型或 KO 图 |
| python -m pip check | 1 | `No module named pip`；只影响指南给出的依赖核查命令，不据此断言模型损坏 |
| 官方 API import | 0 | `0.4.2+ae68f699b154`，`REGVELOVI` 和 `tl.in_silico_block_simulation` 存在 |

`commands.json` 与 `*_stdout_stderr.log` 保存完整命令和退出码；`run/logs/audit_error.log`、`run/run_state.json` 保存 traceback 与阶段状态。

**切片 audit 只用于安全的软件入口验收，不作为全量科学结果。** 输入由 canonical 中首 32 个真实已注释 fibroblast 行复制，保留所有 21,934 基因、原 `X/counts` 数值和全部已有层；没有合成 `spliced/unspliced`。全量两对象缺层的结论来自直接读取 HDF5 `layers` metadata。切片 provenance 写在 `canonical_fibroblasts_32_audit_only.h5ad` 的 `uns`。

## Skill 与 CLI 缺陷 / Reuse issues

1. Skill 的 `scripts/module_path.json` 当前源码不存在；可依稳定 registry ID 正确找到模块。路由可用，但安装到独立 Skill 目录时必须生成路径记录或确保方法库位置可发现。
2. CLI 要求命名矩阵，不能直接接收给定 TF Atlas 边列表。直接调用真实 `validate_grn(pd.read_csv(collectri, index_col=0), genes, 'regulator_by_target')` 得到 `GRN has duplicate gene labels; resolve gene IDs before alignment.`。该 CSV 有意重复 source，属于有效边列表；报错未识别格式不符，容易诱导错误去重。Skill/指南缺具体 edge-list→named-matrix 接入或明确适配入口。
3. `BEGINNER_GUIDE.md` 推荐的 `python -m pip check` 在该已装 runtime 无 pip。ENV报告记录的是 `uv pip check`；指南应提供实际可用的 uv 路径/命令，不能要求重装全局环境。
4. audit 在缺层时立刻抛异常，不写 `INPUT_AUDIT.json`，所以无法在一次 CLI audit 中同时汇总 GRN、JUND、元数据及缺层缺口。新 agent 需按 Skill 继续独立只读 metadata/prior 检查，避免把首个错误当作全部问题。
5. 本次完成后 `run_state.json` 的 report 为 PASS，但 `ANALYSIS_REPORT.md` 自身行显示 `report | RUNNING`；未执行阶段也没有显式 NOT_RUN 行。用户须以最终 state 判断状态，建议在报告生成完成时刷新正确终态。

## 恢复与未来可复用步骤 / Recovery

1. 找到与 canonical fibroblast cells 匹配的已有 BAM/FASTQ、barcode、sample/donor 对照和 GRCh38 注释；若必须新取得大型测序数据，先确认 accession/大小预算。不能从普通 counts 重建剪接计数。
2. 在独立派生 H5AD 中按 cell/gene IDs 对齐真实 spliced/unspliced，保留 canonical 注释及 sample/donor/QC provenance。保留 JUND 及有效 target，拒绝静默按行填入、改名或以 cell2location feature-filtered 对象替代。
3. 用完整 CollecTRI 边列表导出带 regulator/target 名称的矩阵，明确 `grn_orientation=regulator_by_target` 或反向规范。保存原 signed weights/resources/references 及转换记录；二值 skeleton 不代表验证过的激活/抑制。
4. 新建 job 配置：真实 H5AD、矩阵、独立 output 三个绝对路径；species、gene IDs、QC/annotation/计数来源；`time_key=null`；`perturb.tfs=['JUND']`。不要把当前 32-cell 审计 config 升格为正式训练配置。
5. 运行 audit，只有格式及真实动态/连续谱系 QC 可接受才依次 prepare、fit、velocity、grn。检查预处理后的 JUND 有效 regulator 与 target/cutoff。fate 需要可证终末状态，横断面 condition 不足以自动指定终末状态。
6. 若 fate 适用且完成基线，固定 baseline terminal cell IDs 再 perturb JUND，然后 visualize/report；保留 no-op、posterior/seed、cutoff 与供者稳定性结果。`--resume` 只跳过同配置且产物完整的 PASS 阶段，不是 optimizer 续训。

```powershell
# 以下 job 的真实剪接层和命名矩阵准备完成且已科学准入之后才能执行。
& $regveloPython $regveloCli audit --config '<new_verified_job.json>'
& $regveloPython $regveloCli prepare --config '<new_verified_job.json>'
& $regveloPython $regveloCli fit --config '<new_verified_job.json>'
& $regveloPython $regveloCli velocity --config '<new_verified_job.json>'
& $regveloPython $regveloCli grn --config '<new_verified_job.json>'
# 可信终末状态/baseline fate 准入后：
& $regveloPython $regveloCli fate --config '<new_verified_job.json>'
& $regveloPython $regveloCli perturb --config '<new_verified_job.json>' --tf JUND
& $regveloPython $regveloCli visualize --config '<new_verified_job.json>'
& $regveloPython $regveloCli report --config '<new_verified_job.json>'
```

当前可复用的是审计入口和失败证据，不是 KO 结果。若最终无法取得剪接数据，可评估不依赖 velocity 的已准入 TF 活性/其他扰动方法；其效应尺度与 RegVelo fate shift 分开表述。
