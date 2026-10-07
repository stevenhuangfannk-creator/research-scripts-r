# DecontX 环境 RNA 去污染（decontx）

按 capture 独立估计并减少环境 RNA 污染。

方法状态：CANDIDATE；执行验证：BLOCKED。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

RDS 中保存 list(counts, metadata, backgrounds)。counts 为原始基因 × 细胞计数；metadata 的行名顺序须与 counts 列名完全一致，并含 capture_column。backgrounds 若提供，为按 capture ID 命名的空液滴计数矩阵列表；背景可缺省。

## 包在这里如何使用

用 SingleCellExperiment::SingleCellExperiment() 包装原始计数，调用 celda::decontX(background = ...)，返回按 capture 命名的 SingleCellExperiment 结果列表。

## 配置哪些参数

capture_column 改为真实元数据列名；seed 固定随机种子。工作流按 capture 拆分，每个 capture 独立调用 decontX。

## 运行方式

先在仓库根目录打开 R/终端，核对本地依赖（celda，以及统一入口使用的 yaml）。脚本不会自动安装包。将配置中的 input 指向真实输入 RDS，output_dir 设为本次运行目录；所有相对路径按仓库根目录解析。每次运行使用独立 output_dir，避免覆盖前次结果。

默认配置是起点，请先复制为自己的配置或修改必要字段。核对输入要求与参数后，在仓库根目录运行：

```powershell
Rscript scripts/run_method.R decontx 01_scrna_core/ambient_rna/DecontX/config/default.yml --allow-unvalidated
```

工作流：[workflow.R](scripts/workflow.R)；统一入口：[run_method.R](../../../scripts/run_method.R)。本方法尚未验证，--allow-unvalidated 仅表示你已阅读限制并显式尝试，不代表结果已通过验证。

输入的示意结构如下；这些变量须来自真实数据并完成对齐检查：

```r
saveRDS(list(counts = counts, metadata = metadata,
             backgrounds = backgrounds), "data/input.rds")
```

依赖还包括 SingleCellExperiment、SummarizedExperiment。--allow-unvalidated 不会解决缺失依赖。

## 结果与边界

输出写入配置的 output_dir，具体文件见[输出说明](OUTPUT_CATALOG.md)。统一入口还会保存 sessionInfo.txt 和 run_metadata.yml。

背景矩阵的基因行名和顺序必须与细胞计数完全一致。不要使用已标准化矩阵。采用校正结果前，比较 marker 特异性与生物信号保留情况；脚本不会自动合并为新的 Seurat 对象。

BLOCKED：现有构建环境缺少 celda，工作流未执行；没有已验证的数据集。
