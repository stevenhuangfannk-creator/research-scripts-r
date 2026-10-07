# 方法卡：单细胞质量控制

| 字段 | 内容 |
|---|---|
| 方法 ID | scrna_qc |
| 分类 | 01_scrna_core |
| 状态 | VALIDATED |
| 语言 | R |
| 包 | Seurat |
| 最近验证 | 2026-10-07 |

包版本见[构建环境记录](../../docs/validation/package_status.tsv)；安装过某个包不等于它能够正常加载，也不等于方法经过验证。

官方文档：https://satijalab.org/seurat/articles/pbmc3k_tutorial

原始论文：原始论文见官方文档所列引用；本次构建未独立核验论文元数据。

## 科研问题与用途

计算线粒体/核糖体比例，结合 feature 和 UMI 数检查细胞质量，并记录保留情况。

## 适用条件与输入契约

含 RNA counts 的 Seurat 对象（RDS）。基因名应能够匹配所选物种的 mt_pattern/ribo_pattern；元数据须含 nFeature_RNA 和 nCount_RNA。

可选输入仅限工作流与配置实际支持的字段；候选方法的输入契约是规划规格，不能视为已实现功能。

## 实际调用与主要参数

Seurat::PercentageFeatureSet() 计算 percent.mt/percent.ribo；按给定阈值生成 qc_pass，必要时用 subset() 过滤。qc.tsv 始终记录过滤前的全部细胞。

mt_pattern、ribo_pattern 为正则表达式；thresholds 必须是包含 min_features、max_features、min_counts、max_counts、max_mt 的数值列表。filter: false 仅标记 qc_pass，true 才过滤细胞。核糖体比例会计算，但当前不用于 qc_pass。

参数值是起点，须结合物种、数据规模和样本设计审核。包广泛使用或参数有默认值，不意味着方法被提升为 DEFAULT。

## 假设、局限与常见误区

没有通用的线粒体比例阈值。统一阈值可能去除真实损伤状态，应按组织与 capture 检查分布。QC 不能替代 doublet/ambient RNA 检测；使用 Ensembl ID 时不能直接假定 ^MT- 能匹配。

优点是输入、参数和输出范围明确，便于复用与追溯；该小型工作流不覆盖完整科研分析流程。

## 替代路线与选择依据

需要稳健离群值判定时可评估 scater；原始液滴中的细胞判定可评估 EmptyDrops。

## 输出与图形

实际输出见[输出说明](OUTPUT_CATALOG.md)。需要画图时先查该输出说明，再查[全局图例](../../GALLERY.md)；没有已渲染预览的图不能当作已验证图形建议。

## 验证证据

验证数据：pbmc_small，以及专门用于比例计算检查的三基因测试数据。

PASS：pbmc_small 本身缺少线粒体/核糖体基因，现有验证覆盖审计/过滤及额外三基因测试中的精确比例计算；没有验证真实组织的最佳 QC 阈值。

运行和内存：小型演示不是性能基准，目标数据需记录耗时与线程设置；尽量保留稀疏计数，不要将整张图谱转为稠密矩阵。大型对象的内存消耗尚未基准测试。

## 脚本与参考

脚本：[workflow.R](scripts/workflow.R)（01_scrna_core/quality_control/scripts/workflow.R）。运行命令与配置说明见 [README](README.md)。

参考：https://satijalab.org/seurat/articles/pbmc3k_tutorial
