# GO/KEGG ORA：所选基因的功能富集

方法 ID：`go_kegg_ora`。当前 **CANDIDATE · BLOCKED**：clusterProfiler 未就绪，尚无执行验证。本方法将所选基因与实际受检/可检测背景比较；背景不能习惯性使用全基因组。

## 准备输入

以 RDS 保存 `list(genes, universe)`：genes 是待分析 ID 向量，universe 是非空背景向量，所有 genes 须在 universe 中。两者须使用相同物种、数据库兼容的 ID；脚本不自动转换 ID。报告数据库版本和映射损失。

```r
stopifnot(length(universe) > 0, all(genes %in% universe))
saveRDS(list(genes = genes, universe = universe), "data/input.rds")
```

上述变量由真实分析提供；先确保 data/ 存在。环境需有 clusterProfiler、yaml，GO 分析还需目标物种 OrgDb 包。

## 修改配置并运行

[default.yml](config/default.yml)含占位文本，**不能原样直接运行**。ontology 必须选一个 `BP`、`MF`、`CC` 或 `KEGG`；key_type 填合法 ID 类型。

- GO：补充 `orgdb_package`，例如人类用 `org.Hs.eg.db`（仅适用于匹配的人类输入），并选择兼容的 key_type，例如 ENTREZID。
- KEGG：填写真实 organism 代码（例如人类 hsa）及 enrichKEGG 支持的 key_type，核对访问/许可条件。
- input/output_dir：填真实输入和本地结果目录。

当前脚本固定 `pAdjustMethod = "BH"`，不读取配置中的 p_adjust。其他包默认阈值沿用实际安装版本的函数默认值，当前配置没有暴露这些参数。

从仓库根目录运行，必要时替换为你自己的配置路径：

```sh
Rscript scripts/run_method.R go_kegg_ora 05_pathway_function/GO_KEGG/config/default.yml --allow-unvalidated
```

ontology 为 KEGG 时调用 enrichKEGG，其他值进入 enrichGO。标志仅允许尝试未验证流程，不代表执行或科学结论有效。

## 输出与边界

output_dir（默认 results/go_kegg_ora）下为 enrichment.tsv、object.rds（enrichResult）、sessionInfo.txt 和 run_metadata.yml。当前不自动绘图。GO 层级条目存在依赖，富集结果不直接证明通路活化或机制因果。

下一步先修订配置、审查背景和 ID 映射，再用代表性小输入验证依赖及输出。继续查阅：[方法卡](METHOD_CARD.md)、[输出目录](OUTPUT_CATALOG.md)、[示例](examples/README.md)、[图例状态](gallery/README.md)。
