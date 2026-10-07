# 探索性 cluster marker 分析（cell_markers）

寻找细胞/cluster 的探索性 marker，供分群解释和注释证据整理。

方法状态：VALIDATED；执行验证：PASS。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

含标准化 RNA 表达 data layer 的 Seurat 对象（RDS），元数据中存在 group_column 指定的分组列。

## 包在这里如何使用

将 DefaultAssay 设为 RNA，按 group_column 设置 Idents，再调用 Seurat::FindAllMarkers(test.use = "wilcox")。

## 配置哪些参数

group_column 起点为 seurat_clusters；only_positive: true 只报告正向 marker；min_pct = 0.1 与 logfc_threshold = 0.25 是筛选起点。检验固定为 wilcox。

## 运行方式

先在仓库根目录打开 R/终端，核对本地依赖（Seurat，以及统一入口使用的 yaml）。脚本不会自动安装包。将配置中的 input 指向真实输入 RDS，output_dir 设为本次运行目录；所有相对路径按仓库根目录解析。每次运行使用独立 output_dir，避免覆盖前次结果。

默认配置是起点，请先复制为自己的配置或修改必要字段。核对输入要求与参数后，在仓库根目录运行：

```powershell
Rscript scripts/run_method.R cell_markers 02_differential_analysis/differential_expression/config/default.yml
```

工作流：[workflow.R](scripts/workflow.R)；统一入口：[run_method.R](../../scripts/run_method.R)。现有 PASS 仅覆盖方法卡所列范围，首次用于真实数据仍应核查结果。

Seurat v5 对象若含未合并的多批次 layers，须在目标对象上确认 FindAllMarkers 的输入要求；本脚本不负责 layer 合并。优先检查基因名、cluster、效应方向与表达比例，再结合 marker 证据注释。

## 结果与边界

输出写入配置的 output_dir，具体文件见[输出说明](OUTPUT_CATALOG.md)。统一入口还会保存 sessionInfo.txt 和 run_metadata.yml。

细胞级 P 值可能受伪重复影响。本输出不提供样本/供体层级处理组推断；marker 本身也不能单独证明细胞类型或处理效应。

PASS：在 pbmc_small 上验证探索性 cluster-marker 表；没有验证样本层级处理组推断。
