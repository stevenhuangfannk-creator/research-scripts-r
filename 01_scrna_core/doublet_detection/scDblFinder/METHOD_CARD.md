# 方法卡：scDblFinder 双细胞检测

| 字段 | 内容 |
|---|---|
| 方法 ID | scdblfinder |
| 分类 | 01_scrna_core |
| 状态 | CANDIDATE |
| 语言 | R |
| 包 | scDblFinder |
| 最近验证 | 尚未验证 |

包版本见[构建环境记录](../../../docs/validation/package_status.tsv)；安装过某个包不等于它能够正常加载，也不等于方法经过验证。

官方文档：https://bioconductor.org/packages/release/bioc/vignettes/scDblFinder/inst/doc/scDblFinder.html

原始论文：原始论文见官方文档所列引用；本次构建未独立核验论文元数据。

## 科研问题与用途

按独立液滴 capture 标记疑似 doublet，并保留每个细胞的得分和分类。

## 适用条件与输入契约

含 RNA 原始 counts 的 Seurat 对象（RDS），元数据中存在 capture_column 指定的建库/capture 列。capture ID 不能自动用 donor ID 替代。

可选输入仅限工作流与配置实际支持的字段；候选方法的输入契约是规划规格，不能视为已实现功能。

## 实际调用与主要参数

从 RNA counts 建 SingleCellExperiment，调用 scDblFinder::scDblFinder(samples = capture, dbr = ...)，再写回 scDblFinder.score/scDblFinder.class。当前脚本只标记，不移除 doublet。

capture_column 改为真实元数据列名；dbr: null 将预期 doublet 率留给包估计；seed 固定随机种子。脚本使用 BiocParallel::SerialParam() 串行运行。

参数值是起点，须结合物种、数据规模和样本设计审核。包广泛使用或参数有默认值，不意味着方法被提升为 DEFAULT。

## 假设、局限与常见误区

doublet 率依赖技术与回收细胞量；同型 doublet 难以检出。删除标记细胞前须保留审计，并检查每个 capture 的得分分布。

优点是输入、参数和输出范围明确，便于复用与追溯；该小型工作流不覆盖完整科研分析流程。

## 替代路线与选择依据

可在同一 capture 上比较 DoubletFinder；Python 路线可比较 Scrublet。

## 输出与图形

实际输出见[输出说明](OUTPUT_CATALOG.md)。需要画图时先查该输出说明，再查[全局图例](../../../GALLERY.md)；没有已渲染预览的图不能当作已验证图形建议。

## 验证证据

验证数据：无。

BLOCKED：现有构建环境缺少 scDblFinder，工作流未执行；提供真实输入并解决依赖后仍需验证。

运行和内存：小型演示不是性能基准，目标数据需记录耗时与线程设置；尽量保留稀疏计数，不要将整张图谱转为稠密矩阵。大型对象的内存消耗尚未基准测试。

## 脚本与参考

脚本：[workflow.R](scripts/workflow.R)（01_scrna_core/doublet_detection/scDblFinder/scripts/workflow.R）。运行命令与配置说明见 [README](README.md)。

参考：https://bioconductor.org/packages/release/bioc/vignettes/scDblFinder/inst/doc/scDblFinder.html
