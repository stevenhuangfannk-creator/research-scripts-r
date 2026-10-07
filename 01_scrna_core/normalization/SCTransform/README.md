# SCTransform 方差稳定化（sctransform）

建模测序深度效应，生成用于后续探索的 SCT assay 和变量基因。

方法状态：CANDIDATE；执行验证：UNVALIDATED。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

含 RNA counts 的 Seurat 对象（RDS）。若指定 vars_to_regress，相应协变量须存在于元数据。

## 包在这里如何使用

Seurat::SCTransform(assay = "RNA", vst.flavor = "v2", vars.to.regress = ..., seed.use = ...) 返回带 SCT assay 的对象。

## 配置哪些参数

vars_to_regress 默认为 null；seed 固定随机种子。配置中的 vst_flavor 当前不被读取，脚本固定 vst.flavor = "v2"。

## 运行方式

先在仓库根目录打开 R/终端，核对本地依赖（Seurat，以及统一入口使用的 yaml）。脚本不会自动安装包。将配置中的 input 指向真实输入 RDS，output_dir 设为本次运行目录；所有相对路径按仓库根目录解析。每次运行使用独立 output_dir，避免覆盖前次结果。

默认配置是起点，请先复制为自己的配置或修改必要字段。核对输入要求与参数后，在仓库根目录运行：

```powershell
Rscript scripts/run_method.R sctransform 01_scrna_core/normalization/SCTransform/config/default.yml --allow-unvalidated
```

工作流：[workflow.R](scripts/workflow.R)；统一入口：[run_method.R](../../../scripts/run_method.R)。本方法尚未验证，--allow-unvalidated 仅表示你已阅读限制并显式尝试，不代表结果已通过验证。

它是 CANDIDATE，运行必须显式添加 --allow-unvalidated。有脚本不等于已验证；应在目标数据上记录模型拟合与内存情况。

## 结果与边界

输出写入配置的 output_dir，具体文件见[输出说明](OUTPUT_CATALOG.md)。统一入口还会保存 sessionInfo.txt 和 run_metadata.yml。

回归协变量需要生物学理由，避免把研究目标相关信号一并去掉。保留 RNA assay 供后续需要该表达尺度的通信分析；极小稀疏示例不能代表真实模型拟合可靠性。

UNVALIDATED：本构建没有可执行验证证据，也没有已验证的数据集。
