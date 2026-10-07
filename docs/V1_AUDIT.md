# V1 重构前审计 / Pre-refactor audit

## 中文说明 / Chinese overview

这份记录对应 V1 开始前的状态：基准为 `2f12bd7850407fdae44497a116fab8368613526b`，原分支为 `phase4-flagship-reconstruction`。原工作副本有四个未跟踪的敏感性分析文件，因此使用独立 worktree 整理，保护正在进行的研究工作。

审计阅读了原目录、已有文档、脚本目录和 28 个原 R／Quarto 文件，并为保留文件登记 SHA-256。原有问题包括绝对路径、RDS／原始输入缺失、对象生产步骤不全、APAP 最终对象合并不执行、旧 CellChat igraph namespace 补丁；这些仍记录在原项目，不因文档翻译而修复或消失。

整理决定是保留来源与历史，不把旧补丁、固定线程数或组织特定自动标签搬进通用方法，也没有增加大型数据。下方英文原记录保留具体来源链接。

Base: `2f12bd7850407fdae44497a116fab8368613526b`. Original branch: `phase4-flagship-reconstruction`.
The original checkout had four untracked sensitivity notes/scripts in an active reproduction.
They remain in the original checkout; a separate Git worktree protects them from this refactor.
No reset, forced overwrite, stash, project move or deletion was used.

Complete committed tree: [pre-refactor tree](validation/pre_refactor_tree.txt).
Every preserved project/reproduction/library/original doc has a SHA-256 record in
[preservation.json](validation/preservation.json). Existing README/docs and all 28 original
R/Quarto source files were reviewed through the script catalog and source patterns.

Known pre-existing problems: legacy absolute paths, absent RDS/raw inputs, gaps in object
production, APAP final-object merge marked non-executing, and old CellChat igraph namespace
patches. They stay documented in the original project audits. New code does not inherit these
patches, hardcoded worker counts or tissue-specific auto-labels. No large data was added.
