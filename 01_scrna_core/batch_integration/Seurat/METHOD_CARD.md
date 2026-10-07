# 方法卡：Seurat anchors 批次整合

| 字段 | 内容 |
|---|---|
| 方法 ID | seurat_integration |
| 分类 | 01_scrna_core |
| 状态 | CANDIDATE |
| 语言 | R |
| 包 | Seurat |
| 最近验证 | 尚未验证 |

包版本见[构建环境记录](../../../docs/validation/package_status.tsv)；安装过某个包不等于它能够正常加载，也不等于方法经过验证。

官方文档：https://satijalab.org/seurat/articles/integration_introduction

原始论文：原始论文见官方文档所列引用；本次构建未独立核验论文元数据。

## 科研问题与用途

通过 Seurat anchors 对多个技术批次建立共享分析空间。

## 适用条件与输入契约

含 RNA assay 与 batch_column 指定列的 Seurat 对象（RDS），至少两个批次；每批次须有足够细胞支持指定维数。

可选输入仅限工作流与配置实际支持的字段；候选方法的输入契约是规划规格，不能视为已实现功能。

## 实际调用与主要参数

SplitObject() 按批次拆分；NormalizeData()/FindVariableFeatures() 逐批处理；SelectIntegrationFeatures() → FindIntegrationAnchors() → IntegrateData()。

batch_column 改为真实列名；nfeatures 为用于整合的变量基因数，起点 2000；npcs 为 anchors/integration 使用的维数，起点 30。

参数值是起点，须结合物种、数据规模和样本设计审核。包广泛使用或参数有默认值，不意味着方法被提升为 DEFAULT。

## 假设、局限与常见误区

当前是 anchors 接口，不是已验证的 Seurat v5 IntegrateLayers 路线。保留 RNA assay 做 DEG/通信，integrated 表达用于分析空间；评估批次混合和过度校正，不要将 integrated 值用于原始计数推断。

优点是输入、参数和输出范围明确，便于复用与追溯；该小型工作流不覆盖完整科研分析流程。

## 替代路线与选择依据

可比较 Harmony；Seurat v5 IntegrateLayers 需另行进行版本特定验证。

## 输出与图形

实际输出见[输出说明](OUTPUT_CATALOG.md)。需要画图时先查该输出说明，再查[全局图例](../../../GALLERY.md)；没有已渲染预览的图不能当作已验证图形建议。

## 验证证据

验证数据：无。

UNVALIDATED：本构建没有可执行验证证据，也没有已验证的数据集。

运行和内存：小型演示不是性能基准，目标数据需记录耗时与线程设置；尽量保留稀疏计数，不要将整张图谱转为稠密矩阵。大型对象的内存消耗尚未基准测试。

## 脚本与参考

脚本：[workflow.R](scripts/workflow.R)（01_scrna_core/batch_integration/Seurat/scripts/workflow.R）。运行命令与配置说明见 [README](README.md)。

参考：https://satijalab.org/seurat/articles/integration_introduction
