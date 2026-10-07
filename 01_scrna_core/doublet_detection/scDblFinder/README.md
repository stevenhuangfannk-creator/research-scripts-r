# scDblFinder 双细胞检测（scdblfinder）

按独立液滴 capture 标记疑似 doublet，并保留每个细胞的得分和分类。

方法状态：CANDIDATE；执行验证：BLOCKED。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

含 RNA 原始 counts 的 Seurat 对象（RDS），元数据中存在 capture_column 指定的建库/capture 列。capture ID 不能自动用 donor ID 替代。

## 包在这里如何使用

从 RNA counts 建 SingleCellExperiment，调用 scDblFinder::scDblFinder(samples = capture, dbr = ...)，再写回 scDblFinder.score/scDblFinder.class。当前脚本只标记，不移除 doublet。

## 配置哪些参数

capture_column 改为真实元数据列名；dbr: null 将预期 doublet 率留给包估计；seed 固定随机种子。脚本使用 BiocParallel::SerialParam() 串行运行。

## 运行方式

先在仓库根目录打开 R/终端，核对本地依赖（scDblFinder，以及统一入口使用的 yaml）。脚本不会自动安装包。将配置中的 input 指向真实输入 RDS，output_dir 设为本次运行目录；所有相对路径按仓库根目录解析。每次运行使用独立 output_dir，避免覆盖前次结果。

默认配置是起点，请先复制为自己的配置或修改必要字段。核对输入要求与参数后，在仓库根目录运行：

```powershell
Rscript scripts/run_method.R scdblfinder 01_scrna_core/doublet_detection/scDblFinder/config/default.yml --allow-unvalidated
```

工作流：[workflow.R](scripts/workflow.R)；统一入口：[run_method.R](../../../scripts/run_method.R)。本方法尚未验证，--allow-unvalidated 仅表示你已阅读限制并显式尝试，不代表结果已通过验证。

依赖还包括 SeuratObject、SingleCellExperiment、SummarizedExperiment、BiocParallel。--allow-unvalidated 只允许进入未验证工作流，不会安装缺失包或使 BLOCKED 自动变成通过。

## 结果与边界

输出写入配置的 output_dir，具体文件见[输出说明](OUTPUT_CATALOG.md)。统一入口还会保存 sessionInfo.txt 和 run_metadata.yml。

doublet 率依赖技术与回收细胞量；同型 doublet 难以检出。删除标记细胞前须保留审计，并检查每个 capture 的得分分布。

BLOCKED：现有构建环境缺少 scDblFinder，工作流未执行；提供真实输入并解决依赖后仍需验证。
