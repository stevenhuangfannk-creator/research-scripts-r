# 分层细胞注释（hierarchical_annotation）

将人工审核后的 L1/L2/L3 cluster-to-label 映射写回对象，同时保留 cluster ID 和证据。

方法状态：VALIDATED；执行验证：PASS。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

含 cluster_column 指定分群列的 Seurat 对象（RDS）。labels 须是命名层级列表，每层为命名的 cluster-to-label 映射；evidence 须是非空证据字符串。

## 包在这里如何使用

逐层按 cluster ID 查 labels 映射，将标签写入 Seurat 元数据并生成 annotation.tsv。脚本不进行 marker 自动鉴定或参考库映射。

## 配置哪些参数

cluster_column 起点为 seurat_clusters；labels 的层级名可设为 celltype_l1/celltype_l2/celltype_l3。未映射的 cluster 会标为 Unknown；映射中出现输入不存在的 cluster 会报错。

## 运行方式

先在仓库根目录打开 R/终端，核对本地依赖（Seurat，以及统一入口使用的 yaml）。脚本不会自动安装包。将配置中的 input 指向真实输入 RDS，output_dir 设为本次运行目录；所有相对路径按仓库根目录解析。每次运行使用独立 output_dir，避免覆盖前次结果。

默认配置是起点，请先复制为自己的配置或修改必要字段。核对输入要求与参数后，在仓库根目录运行：

```powershell
Rscript scripts/run_method.R hierarchical_annotation 01_scrna_core/annotation/config/default.yml
```

工作流：[workflow.R](scripts/workflow.R)；统一入口：[run_method.R](../../scripts/run_method.R)。现有 PASS 仅覆盖方法卡所列范围，首次用于真实数据仍应核查结果。

默认 labels 是占位字符串，不能直接运行。配置格式示例如下；"0" 须为实际存在的 cluster，标签与 evidence 须换成你的审核结果：

```yaml
cluster_column: seurat_clusters
labels:
  celltype_l1:
    "0": "示例标签，需替换"
evidence: "格式示例，需替换为真实 marker 与审核记录"
```

同时保留默认配置的 input/output_dir。不要将此格式示例当作生物学注释。

## 结果与边界

输出写入配置的 output_dir，具体文件见[输出说明](OUTPUT_CATALOG.md)。统一入口还会保存 sessionInfo.txt 和 run_metadata.yml。

示例仅验证标签写回。真实标签须结合组织 marker、阴性 marker 与必要的子集重聚类审核；增殖/cycling 是状态而非谱系。evidence 非空校验不等于证据内容正确。

PASS：在 pbmc_small 上仅验证标签写回和 Unknown 回退；没有验证标签的生物学正确性。
