# SoupX 环境 RNA 去污染（候选）（soupx）

结合原始液滴、过滤后细胞与 cluster 结构估计环境 RNA 污染。

方法状态：CANDIDATE；执行验证：UNVALIDATED。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

规划输入为原始/过滤后的计数矩阵和 cluster 标签；当前仓库尚无实现该输入契约的 workflow。

## 包在这里如何使用

当前没有 scripts/workflow.R；run_method.R 会直接提示此方法无可执行工作流。先依据官方文档复现、验证，再提炼可复用代码。

## 配置哪些参数

review_required 只是审核提示，涉及污染比例（soup fraction）与不表达 marker；不是可运行的包参数配置。

## 当前能否运行

当前没有 scripts/workflow.R；run_method.R 会直接提示此方法无可执行工作流。先依据官方文档复现、验证，再提炼可复用代码。

先在仓库根目录打开 R/终端，核对本地依赖（SoupX）。脚本不会自动安装包。这里的配置是规划说明，尚不能执行。

--allow-unvalidated 不能使未实现的方法运行。config/default.yml 仅为规划入口；请先阅读官方 SoupX 仓库和本方法卡。

## 结果与边界

[输出说明](OUTPUT_CATALOG.md)中的结果属于规划输出，当前仓库没有生成它们。

依赖有信息量的环境 RNA 谱，应核查校正后真实生物表达的保留情况。

UNVALIDATED：没有可执行工作流、已验证数据集或执行结果。
