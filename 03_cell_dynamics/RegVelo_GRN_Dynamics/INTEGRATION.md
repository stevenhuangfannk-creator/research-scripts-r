# 既有体系连接 / Integration boundaries

RegVelo独立处理剪接动力学、regulon阻断和CellRank命运。Atlas负责既有数据/QC/注释，TF Atlas提供有出处的prior，Toolkit负责不同扰动引擎的选择与证据分层，Workbench链接方法和结果。本次不重写这些项目核心分析。

| 既有组件 | 可复用资产 | 接口与限制 |
|---|---|---|
| [Oral scRNA Atlas](https://github.com/stevenhuangfannk-creator/oral-scrna-atlas) | dataset registry、来源、样本、processed H5AD与注释 | 只读读取，RegVelo另建派生数据；未有剪接层的表达资产不能直接velocity |
| [TF Regulatory Network Atlas](https://github.com/stevenhuangfannk-creator/tf-regulatory-network-atlas) | CollecTRI prior、TF来源、方法/图件契约 | 物种与gene ID匹配后导出命名网络；TF活性不是动态调控验证 |
| Virtual Perturbation Toolkit | 原注释、raw-count审查、donor/source和证据层级 | RegVelo是external_module关系；未有可运行平台adapter时不标IMPLEMENTED |
| [Bioinformatics Workbench](https://github.com/stevenhuangfannk-creator/bioinformatics-research-workbench) | Methods registry、案例、Gallery与方法节点 | 外部已运行与平台adapter执行分开；新知识关联保留pending/planned |

## Toolkit外部引擎契约 / External engine contract

当前Toolkit已实现DoseDirKO；CellOracle/scTenifoldKnk为NOT_INTEGRATED。RegVelo CLI可以独立调用，但这不等于Toolkit `Run.ps1` 已集成它。

RegVelo输入需要剪接层、moments、prior和动态问题；DoseDirKO的raw counts网络嵌入距离不要求相同输入。RegVelo输出包括模型velocity、latent time和fate差；DoseDirKO effect/delta不是相同单位。共用cell/source/donor ID及四层证据边界，不共用效应量定义或生物验证PASS。

未来adapter最小职责是：验证RegVelo准入→调用此模块CLI→保留 `run_state.json` / 数值 / Gallery→单独登记输入、执行、预测稳定性和生物验证。无需复制官方模型源码、重建全部扰动平台或修改旧历史JUND结果。

## 方法注册 / Registration

主库稳定ID为 `regvelo_grn_dynamics`，分类 `03_cell_dynamics`，语言Python。现有R `run_method.R`不执行Python；按本模块README直接调用CLI。新方法成熟度与实际stage状态独立。官方真实运行、smoke、工程夹具和外部adapter分别记录证据。

外部项目需要连接时优先更新其现有入口，保留真实API与来源，不复制另一个registry。GitHub只分享代码、配置、中文说明和已核验小型图件；大型H5AD/模型留在本地可复现路径清单。
