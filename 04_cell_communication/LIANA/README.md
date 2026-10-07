# liana：比较和汇总多种方法的细胞通讯证据

方法 ID：`liana_plus`。当前为 **CANDIDATE · UNVALIDATED**。

## 准备什么

AnnData 或受支持的 R 接口、细胞标签和兼容的 LR 资源。

需要事先判断：review_required：LR 资源、方法列表和排序汇总规则。当前只是待核对清单，尚未接入可执行脚本。

## 现在能否直接运行

本仓库尚未为 `liana_plus` 实现可执行工作流，registry 中的 `script` 为 `null`。因此不能通过 `scripts/run_method.R` 运行；即使添加 `--allow-unvalidated` 也不能补齐实现。

`config/default.yml` 是规划占位配置，`review_required` 记录待核对内容。请先查[方法卡](METHOD_CARD.md)和[官方文档](https://liana-py.readthedocs.io/en/latest/)，完成最小复现与验证后再接入脚本。

## 结果和解释

一致性 LR 排名、多条件/情境证据（规划输出）。

方法较新不代表能够成为 DEFAULT；接口和资源必须验证。当前登记为 R / liana，而参考文档指向 LIANA+ Python，使用前需要明确实际接口，不能视为已实现的跨语言工作流。

继续查阅：[输出目录](OUTPUT_CATALOG.md)、[示例与验证](examples/README.md)、[图例状态](gallery/README.md)、[配置](config/default.yml)。
