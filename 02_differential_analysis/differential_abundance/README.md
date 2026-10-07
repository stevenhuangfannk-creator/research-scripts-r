# 差异丰度分析（候选）（differential_abundance）

在有生物学重复的设计下检验细胞群/邻域丰度变化，并考虑组成效应。

方法状态：CANDIDATE；执行验证：UNVALIDATED。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

规划输入为 counts/邻域图以及生物学样本设计；当前仓库尚无实现该输入契约的 workflow。

## 包在这里如何使用

当前没有 scripts/workflow.R；run_method.R 会提示此方法无可执行工作流。Milo 与 scCODA 属于不同路线，尚未在此统一封装。

## 配置哪些参数

review_required 是审核提示，涉及邻域覆盖、contrast 和样本结构；不是可运行的包参数配置。

## 当前能否运行

当前没有 scripts/workflow.R；run_method.R 会提示此方法无可执行工作流。Milo 与 scCODA 属于不同路线，尚未在此统一封装。

先在仓库根目录打开 R/终端，核对本地依赖（Milo / scCODA）。脚本不会自动安装包。这里的配置是规划说明，尚不能执行。

配置入口仅记录未来审核要求，不能直接调用 Milo/scCODA。--allow-unvalidated 不能绕过缺少脚本这一限制。

## 结果与边界

[输出说明](OUTPUT_CATALOG.md)中的结果属于规划输出，当前仓库没有生成它们。

样本量、capture 偏差和组成效应会影响推断；细胞比例柱状图只提供描述，不能替代重复样本层级的检验。

UNVALIDATED：没有可执行工作流、已验证数据集或执行结果。
