# 复现计划与执行证据 / Reproduction plan

本计划针对官方斑马鱼 neural crest 数据，按完整分析优先级执行。下表记录2026-10-10实际状态；**当前真实状态读取运行输出 `run_state.json` 和交付报告**，本文件不把预期功能当执行结果。

| 阶段 | 实際任务 / 验收产物 | 本次实际状态 |
|---|---|---|
| Phase 0 | 官方SHA/API/许可、Figshare来源、独立环境、依赖锁与硬件报告 | PARTIAL（源码/数据/环境PASS；全文/项目页403） |
| Phase 1 | `zebrafish_nc`、`zebrafish_grn`真数据下载与hash，原/处理QC、GRN覆盖 | PASS |
| Phase 2 | 官方REGVELOVI正式训练、模型保存与reload、loss/QC | PARTIAL（hard正式PASS；三模式smoke PASS；正式多模式未比） |
| Phase 3 | velocity/latent time/scVelo基线，CellRank转移与命运 | PASS |
| Phase 4 | prior/inferred GRN、TF–target、regulon与局部网络 | PASS |
| Phase 5 | 官方有效TF regulon KO、同终末定义、no-op及敏感性 | PASS（KO/零效应对照PASS；后验稳定性PASS） |
| Phase 6 | 从真表生成PNG/SVG/PDF、逐图CSV与metadata、Gallery | PASS（27/27真实图） |
| Phase 7 | 稳定CLI、配置、方法卡、Codex Skill与有意义工程测试 | PASS |
| Phase 8 | 本地PI数据只读准入审计、评级及替代路线 | PASS（8 NOT_READY、1 BLOCKED） |
| Phase 9 | 工程/方法/结果真实性审查，明确未执行项 | PARTIAL（计算/对照PASS；真实扰动与多训练seed未跑） |
| Phase 10 | 既有Index/registry关联，Git commit/push真实记录 | 代码/索引/Gallery准备PASS；commit/push由当前分支Git历史及最终交付记录核验 |

## P0 / Source, data and smoke

固定核心与复现仓库SHA，核查最新教程和所安装API；取得官方zebrafish H5AD和命名GRN，下载后校验大小及hash。记录真实层、细胞注释、样本/时间与平台，检查现成归一化/embedding来源。smoke使用明确小规模配置验证官方preprocess/fit/save/load；写明细胞数、epochs、后验样本数，不做全数据性能结论。

## P1 / Formal dynamics and perturbation

在完整官方数据上执行推荐默认hard策略，保存模型、loss、参数和输出。继续velocity→GRN→CellRank→至少一个有效官方TF KO。当前官方教程以 `elf1`、`nr2f5` 作regulon示例；先检查有效target，不凭名称直接套用 Gabpa/Mitf/Sox10。baseline terminal definition冻结后进行扰动比较。

## P2 / Comparison, QC and gallery

scVelo基线、posterior/no-op、不同seed、cutoff/target敏感性，按资源完成三种GRN策略正式比较。没有资源时先留下各策略可执行配置和smoke证据，正式比较保持NOT_RUN/BLOCKED。对有效实际数值生成标准图件，逐图保存来源、CSV、命令与真实状态。

## P3 / Peri-implantitis admission

只读检查Oral Atlas、Lin2026、GSE310110、GSE272774、GSE266897等已存在资产。核实疾病分组/物种/样本/层及GRN交集；缺剪接层拒绝正式训练，检查现有BAM/FASTQ，记录计数方案和预算。不存在可信trajectory时保留GRN活性/其他适用引擎路线，不强行fate预测。

## P4 / Registration and recovery

更新主库现有METHOD_INDEX、GALLERY、registry，按真实结果状态链接外部平台，不重建平台。模型、raw data、缓存、环境、日志留在Git外。保存 `--resume` 命令、产物和错误；记录Git分支/commit/push，无强制推送。

## 停止与恢复 / Stop and resume

数据下载失败保留校验信息，避免接受不完整文件；依赖或GPU受阻保留独立环境报告；训练中止保留可恢复checkpoint及日志，明确官方API是否支持继续训练。CLI `--resume` 的含义是跳过同配置且产物存在的已成功阶段，不自动保证能从任意optimizer状态继续训练。不能把中断训练或smoke标为完整复现。
