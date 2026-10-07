# 创建 Seurat 对象（seurat_ingestion）

将原始计数矩阵与细胞元数据对齐，创建可追溯的 Seurat 对象。

方法状态：VALIDATED；执行验证：PASS。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

一个 RDS 文件，内容为 list(counts = counts, metadata = metadata)。counts 是非负、有限的基因 × 细胞计数矩阵，须有唯一的行名和列名；metadata 是 data.frame，其行名须与细胞条形码集合一致。

## 包在这里如何使用

Seurat::CreateSeuratObject() 创建 RNA assay；元数据按 counts 的列名重排。该工作流不会直接读取 10x 文件、判定细胞条形码或替换基因 ID。

## 配置哪些参数

project 为项目标签。配置中的 min.cells、min.features 当前不被脚本读取；脚本固定为 0，建对象时不进行这两类过滤。

## 运行方式

先在仓库根目录打开 R/终端，核对本地依赖（Seurat，以及统一入口使用的 yaml）。脚本不会自动安装包。将配置中的 input 指向真实输入 RDS，output_dir 设为本次运行目录；所有相对路径按仓库根目录解析。每次运行使用独立 output_dir，避免覆盖前次结果。

默认配置是起点，请先复制为自己的配置或修改必要字段。核对输入要求与参数后，在仓库根目录运行：

```powershell
Rscript scripts/run_method.R seurat_ingestion 01_scrna_core/data_ingestion/config/default.yml
```

工作流：[workflow.R](scripts/workflow.R)；统一入口：[run_method.R](../../scripts/run_method.R)。现有 PASS 仅覆盖方法卡所列范围，首次用于真实数据仍应核查结果。

可在 R 中保存输入：

```r
# counts 和 metadata 来自你已核对的真实数据；data/ 需已存在。
saveRDS(list(counts = counts, metadata = metadata), "data/input.rds")
```

这里的 input.rds 不是一个已创建好的示例文件。

## 结果与边界

输出写入配置的 output_dir，具体文件见[输出说明](OUTPUT_CATALOG.md)。统一入口还会保存 sessionInfo.txt 和 run_metadata.yml。

原始液滴中的细胞判定需要上游单独处理。不要静默合并重复基因 ID 或自行补造基因名；本步骤仅检查计数非负且有限，不验证整数性或其来源。

PASS：仅验证 counts/metadata 对齐与计数保留，测试数据为 pbmc_small（230 个基因、80 个细胞）；不代表任意真实数据都完成了预处理。
