# 独立未来调用证据 / Independent forward-use evidence

此目录保留 `work/forwardtest` 的原始独立验收文本。原文件未经改写；[copied_evidence_manifest.json](copied_evidence_manifest.json) 列出逐文件 SHA256。H5AD 和逐细胞表不复制到公开验证材料，记录中的绝对本地路径用于解释当时实际命令，不保证在其他机器可运行。

[FORWARDTEST_REPORT.md](FORWARDTEST_REPORT.md) 记录修复前的观察，包括未适配 edge-list、runtime 缺 pip、audit 缺层时未写综合证据、report 留有 RUNNING 等缺陷。这些初始失败记录保留以追溯修复原因，不能作为现版本仍有这些缺陷的证据。

## 修复后复查 / Post-fix check

`postfix/` 保存最新 CLI 对原真实审计切片的独立复查；仅改变派生 job 的 `grn_format="edge_list"`、列映射和 output 路径，复用原 32 个已注释 fibroblast / 21,934 基因切片。没有添加剪接层，没有运行模型或虚拟 KO。

| 检查 | 实际结果 | 证据 |
|---|---|---|
| 缺 S/U 的 `audit` | exit 1；`FAIL/NOT_READY`，保存缺层和 GRN 检查 | [INPUT_AUDIT.json](postfix/run/INPUT_AUDIT.json)、[audit log](postfix/audit_stdout_stderr.log) |
| CollecTRI 命名边读取 | 40,877条双端匹配边；覆盖不能代替动力学准入 | 同一 `INPUT_AUDIT.json` 的 `grn` |
| `report` | exit 0；报告内 audit FAIL、report PASS，其余7个建模/图件阶段 NOT_RUN | [ANALYSIS_REPORT.md](postfix/run/ANALYSIS_REPORT.md)、[run_state.json](postfix/run/run_state.json) |
| pip 与工程回归 | pip26.2.1；pip check PASS；17 tests和14 subtests PASS | [收尾命令记录](../finish_checks_summary.json)、[pytest log](../pytest_module_refresh.log) |

软件回归另外覆盖“缺层与无效 GRN 同时记录”及“无历史状态的 report 最终 PASS/其余8阶段 NOT_RUN”。测试中的微型表达对象只用于软件验证，不是研究数据。前后全部检查均不支持当前数据已经具备 velocity 或 JUND KO 可执行性；真实准入仍为 `NOT_READY`。
