# Seurat anchors 批次整合（seurat_integration）

通过 Seurat anchors 对多个技术批次建立共享分析空间。

方法状态：CANDIDATE；执行验证：UNVALIDATED。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

含 RNA assay 与 batch_column 指定列的 Seurat 对象（RDS），至少两个批次；每批次须有足够细胞支持指定维数。

## 包在这里如何使用

SplitObject() 按批次拆分；NormalizeData()/FindVariableFeatures() 逐批处理；SelectIntegrationFeatures() → FindIntegrationAnchors() → IntegrateData()。

## 配置哪些参数

batch_column 改为真实列名；nfeatures 为用于整合的变量基因数，起点 2000；npcs 为 anchors/integration 使用的维数，起点 30。

## 运行方式

先在仓库根目录打开 R/终端，核对本地依赖（Seurat，以及统一入口使用的 yaml）。脚本不会自动安装包。将配置中的 input 指向真实输入 RDS，output_dir 设为本次运行目录；所有相对路径按仓库根目录解析。每次运行使用独立 output_dir，避免覆盖前次结果。

默认配置是起点，请先复制为自己的配置或修改必要字段。核对输入要求与参数后，在仓库根目录运行：

```powershell
Rscript scripts/run_method.R seurat_integration 01_scrna_core/batch_integration/Seurat/config/default.yml --allow-unvalidated
```

工作流：[workflow.R](scripts/workflow.R)；统一入口：[run_method.R](../../../scripts/run_method.R)。本方法尚未验证，--allow-unvalidated 仅表示你已阅读限制并显式尝试，不代表结果已通过验证。

小批次可能无法支持 npcs = 30，应依据细胞数/数据秩调整；脚本不会自动降低该参数。

## 结果与边界

输出写入配置的 output_dir，具体文件见[输出说明](OUTPUT_CATALOG.md)。统一入口还会保存 sessionInfo.txt 和 run_metadata.yml。

当前是 anchors 接口，不是已验证的 Seurat v5 IntegrateLayers 路线。保留 RNA assay 做 DEG/通信，integrated 表达用于分析空间；评估批次混合和过度校正，不要将 integrated 值用于原始计数推断。

UNVALIDATED：本构建没有可执行验证证据，也没有已验证的数据集。
