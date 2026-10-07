# Harmony 批次整合（harmony）

对已有 PCA 嵌入进行技术批次校正，获得 Harmony 嵌入。

方法状态：CANDIDATE；执行验证：UNVALIDATED。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

已标准化、已有 pca reduction 的 Seurat 对象（RDS），含 batch_column 指定的技术批次列，并至少有两个批次。

## 包在这里如何使用

harmony::RunHarmony(group.by.vars = ..., reduction.use = "pca", dims.use = seq_len(npcs), theta = ...) 在对象中增加 Harmony reduction。

## 配置哪些参数

batch_column 改为真实元数据列名；npcs 不得超过已有 PCA 的维数；theta 为 Harmony 多样性惩罚参数，配置起点为 2。

## 运行方式

先在仓库根目录打开 R/终端，核对本地依赖（harmony，以及统一入口使用的 yaml）。脚本不会自动安装包。将配置中的 input 指向真实输入 RDS，output_dir 设为本次运行目录；所有相对路径按仓库根目录解析。每次运行使用独立 output_dir，避免覆盖前次结果。

默认配置是起点，请先复制为自己的配置或修改必要字段。核对输入要求与参数后，在仓库根目录运行：

```powershell
Rscript scripts/run_method.R harmony 01_scrna_core/batch_integration/Harmony/config/default.yml --allow-unvalidated
```

工作流：[workflow.R](scripts/workflow.R)；统一入口：[run_method.R](../../../scripts/run_method.R)。本方法尚未验证，--allow-unvalidated 仅表示你已阅读限制并显式尝试，不代表结果已通过验证。

下游若需基于 Harmony 构建 neighbors、clusters 和 UMAP，应在项目中明确使用 reduction = "harmony"，再单独验证；不要把当前 clustering 脚本直接接在后面视作 Harmony 聚类。

## 结果与边界

输出写入配置的 output_dir，具体文件见[输出说明](OUTPUT_CATALOG.md)。统一入口还会保存 sessionInfo.txt 和 run_metadata.yml。

批次与处理组完全混杂时，整合不能可靠恢复处理效应。Harmony 校正的是嵌入而非原始计数，须比较批次混合与谱系保留。当前 seurat_clustering 会重算并使用 pca，不会自动用 Harmony 嵌入。

UNVALIDATED：本构建没有可执行验证证据，也没有已验证的数据集。
