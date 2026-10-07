# LogNormalize 标准化（lognormalize）

按细胞总计数进行标准化并取对数，供探索性表达分析与后续降维使用。

方法状态：VALIDATED；执行验证：PASS。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

含 RNA counts 的 Seurat 对象（RDS）。

## 包在这里如何使用

将 DefaultAssay 设为 RNA，调用 Seurat::NormalizeData(normalization.method = "LogNormalize", scale.factor = ...)，生成 RNA data layer。

## 配置哪些参数

scale_factor 是标准化缩放因子，配置起点为 10000。

## 运行方式

先在仓库根目录打开 R/终端，核对本地依赖（Seurat，以及统一入口使用的 yaml）。脚本不会自动安装包。将配置中的 input 指向真实输入 RDS，output_dir 设为本次运行目录；所有相对路径按仓库根目录解析。每次运行使用独立 output_dir，避免覆盖前次结果。

默认配置是起点，请先复制为自己的配置或修改必要字段。核对输入要求与参数后，在仓库根目录运行：

```powershell
Rscript scripts/run_method.R lognormalize 01_scrna_core/normalization/lognormalize/config/default.yml
```

工作流：[workflow.R](scripts/workflow.R)；统一入口：[run_method.R](../../../scripts/run_method.R)。现有 PASS 仅覆盖方法卡所列范围，首次用于真实数据仍应核查结果。

下一步可进入 seurat_clustering。若用于 marker 分析，确认 grouping 列和 RNA data layer 已准备好。

## 结果与边界

输出写入配置的 output_dir，具体文件见[输出说明](OUTPUT_CATALOG.md)。统一入口还会保存 sessionInfo.txt 和 run_metadata.yml。

标准化不等于批次校正。保留 raw counts 给计数模型；不要把 RNA data layer 当作 pseudobulk 原始整数计数。

PASS：在 pbmc_small 上验证 LogNormalize 分支，原始 counts 保留且 RNA data layer 数值有限；不代表批次效应已处理。
