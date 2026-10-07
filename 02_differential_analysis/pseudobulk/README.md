# 按样本与细胞类型汇总原始计数（pseudobulk）

按生物学样本 × 细胞类型对 RNA 原始 counts 求和，为样本层级分析准备矩阵。

方法状态：VALIDATED；执行验证：PASS。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

含 RNA raw counts 的 Seurat 对象（RDS），元数据中有 sample_column 指定的真实生物学样本列，以及 celltype_column 指定的审核后细胞类型列。

## 包在这里如何使用

Seurat::AggregateExpression(assays = "RNA", return.seurat = FALSE, group.by = c(sample_column, celltype_column)) 返回汇总 count 矩阵；Matrix::colSums() 计算各汇总组文库大小。

## 配置哪些参数

sample_column 与 celltype_column 必须替换为真实元数据列名，不是说明性的“biological sample”/“reviewed annotation”占位值。

## 运行方式

先在仓库根目录打开 R/终端，核对本地依赖（Seurat，以及统一入口使用的 yaml）。脚本不会自动安装包。将配置中的 input 指向真实输入 RDS，output_dir 设为本次运行目录；所有相对路径按仓库根目录解析。每次运行使用独立 output_dir，避免覆盖前次结果。

默认配置是起点，请先复制为自己的配置或修改必要字段。核对输入要求与参数后，在仓库根目录运行：

```powershell
Rscript scripts/run_method.R pseudobulk 02_differential_analysis/pseudobulk/config/default.yml
```

工作流：[workflow.R](scripts/workflow.R)；统一入口：[run_method.R](../../scripts/run_method.R)。现有 PASS 仅覆盖方法卡所列范围，首次用于真实数据仍应核查结果。

下游读取 counts <- readRDS("results/pseudobulk/object.rds")，核对列名与设计表再建模型。不要把 normalized data/SCT 残差当作此步骤的原始计数。

## 结果与边界

输出写入配置的 output_dir，具体文件见[输出说明](OUTPUT_CATALOG.md)。统一入口还会保存 sessionInfo.txt 和 run_metadata.yml。

汇总不等于 DEG 检验，细胞不能充当独立生物学重复。须另保留 condition/covariate 样本表、足够独立 donor，并在需要时考虑配对/个体内设计。输出列名是组合分组名，脚本不另生成样本设计表。

PASS：pbmc_small 只有一个原始样本，现有验证仅覆盖原始 counts 求和及计数守恒；有生物学重复的处理组检验仍未验证。
