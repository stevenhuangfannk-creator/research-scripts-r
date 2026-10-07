# 方法卡：创建 Seurat 对象

| 字段 | 内容 |
|---|---|
| 方法 ID | seurat_ingestion |
| 分类 | 01_scrna_core |
| 状态 | VALIDATED |
| 语言 | R |
| 包 | Seurat |
| 最近验证 | 2026-10-07 |

包版本见[构建环境记录](../../docs/validation/package_status.tsv)；安装过某个包不等于它能够正常加载，也不等于方法经过验证。

官方文档：https://satijalab.org/seurat/articles/pbmc3k_tutorial

原始论文：原始论文见官方文档所列引用；本次构建未独立核验论文元数据。

## 科研问题与用途

将原始计数矩阵与细胞元数据对齐，创建可追溯的 Seurat 对象。

## 适用条件与输入契约

一个 RDS 文件，内容为 list(counts = counts, metadata = metadata)。counts 是非负、有限的基因 × 细胞计数矩阵，须有唯一的行名和列名；metadata 是 data.frame，其行名须与细胞条形码集合一致。

可选输入仅限工作流与配置实际支持的字段；候选方法的输入契约是规划规格，不能视为已实现功能。

## 实际调用与主要参数

Seurat::CreateSeuratObject() 创建 RNA assay；元数据按 counts 的列名重排。该工作流不会直接读取 10x 文件、判定细胞条形码或替换基因 ID。

project 为项目标签。配置中的 min.cells、min.features 当前不被脚本读取；脚本固定为 0，建对象时不进行这两类过滤。

参数值是起点，须结合物种、数据规模和样本设计审核。包广泛使用或参数有默认值，不意味着方法被提升为 DEFAULT。

## 假设、局限与常见误区

原始液滴中的细胞判定需要上游单独处理。不要静默合并重复基因 ID 或自行补造基因名；本步骤仅检查计数非负且有限，不验证整数性或其来源。

优点是输入、参数和输出范围明确，便于复用与追溯；该小型工作流不覆盖完整科研分析流程。

## 替代路线与选择依据

10x 文件可先用 Read10X()/Read10X_h5() 读取，再按本输入契约组织；Bioconductor 路线可考虑 SingleCellExperiment。

## 输出与图形

实际输出见[输出说明](OUTPUT_CATALOG.md)。需要画图时先查该输出说明，再查[全局图例](../../GALLERY.md)；没有已渲染预览的图不能当作已验证图形建议。

## 验证证据

验证数据：Seurat::pbmc_small（230 个基因、80 个细胞）。

PASS：仅验证 counts/metadata 对齐与计数保留，测试数据为 pbmc_small（230 个基因、80 个细胞）；不代表任意真实数据都完成了预处理。

运行和内存：小型演示不是性能基准，目标数据需记录耗时与线程设置；尽量保留稀疏计数，不要将整张图谱转为稠密矩阵。大型对象的内存消耗尚未基准测试。

## 脚本与参考

脚本：[workflow.R](scripts/workflow.R)（01_scrna_core/data_ingestion/scripts/workflow.R）。运行命令与配置说明见 [README](README.md)。

参考：https://satijalab.org/seurat/articles/pbmc3k_tutorial
