# fgsea：完整排序的基因集富集

方法 ID：`fgsea`。当前 **CANDIDATE · BLOCKED**：fgsea 未就绪，尚无执行验证。适用于完整、带方向的基因统计量，避免任意 DEG 阈值。

## 准备输入

以 RDS 保存 `list(ranks, pathways)`。ranks 为命名数值向量，名称是唯一的基因 ID、值须有限；pathways 为命名基因集列表，使用兼容 ID。

```r
stopifnot(is.numeric(ranks), !is.null(names(ranks)),
          !anyDuplicated(names(ranks)), all(is.finite(ranks)))
saveRDS(list(ranks = ranks, pathways = pathways), "data/input.rds")
```

这些变量须来自真实分析；先确保 data/ 存在。排序应使用有意义的带方向统计量，不能只用 P 值或任意 PPI 度数解释转录富集。保留完整受检排序、记录并列值及映射覆盖率，比较 NES 时使用相同基因集定义。

## 配置与运行

环境需有 fgsea 和 yaml。编辑[default.yml](config/default.yml)的 input/output_dir；min_size = 15、max_size = 500 为参与富集的基因集大小范围，seed = 42 为随机种子，须按实际研究审查。

从仓库根目录运行；若另存配置，将命令中的路径替换为该文件：

```sh
Rscript scripts/run_method.R fgsea 05_pathway_function/GSEA/config/default.yml --allow-unvalidated
```

脚本将 ranks 降序排序，调用 fgseaMultilevel，并把 leadingEdge 以分号拼接。标志仅允许尝试未验证流程，不代表依赖、输入或结果已验证。

## 实际输出

output_dir（默认 results/fgsea）下为 gsea.tsv、sessionInfo.txt 和 run_metadata.yml。gsea.tsv 包含 NES、校正 P 值、leadingEdge 等 fgsea 返回字段。当前脚本不保存分析对象，也不生成富集曲线；曲线是后续独立绘图能力，不能视为已实现。

下一步先核对排序统计量、基因集物种/ID/版本和映射覆盖率，再用代表性小输入验证结果。继续查阅：[方法卡](METHOD_CARD.md)、[输出目录](OUTPUT_CATALOG.md)、[示例](examples/README.md)、[图例状态](gallery/README.md)。
