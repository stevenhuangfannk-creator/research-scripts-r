# bulk RNA、临床关联与机器学习（07_bulk_clinical_ml）

本分类涵盖有生物学重复的 bulk RNA 分析、临床关联和预测。预测模型的训练、调参、测试与外部验证需要分别安排。

| 使用目的 | 方法入口 | 当前可用范围 |
|---|---|---|
| Pearson / Spearman 相关性 | [correlation](correlation/README.md) | VALIDATED / PASS；已有基础数值实现 |
| 分组 Kaplan–Meier 生存曲线 | [survival_km](survival/README.md) | VALIDATED / PASS；已有右删失实现 |
| 单因素 / 多因素 Cox | [cox](Cox/README.md) | VALIDATED / PASS；已有模型与诊断实现 |
| bulk / pseudobulk 差异表达 | [DESeq2](bulk_RNAseq/README.md)、[limma](bulk_RNAseq/limma/README.md) | CANDIDATE；尚无工作流 |
| LASSO 回归 / 生存预测 | [LASSO](LASSO/README.md)、[LASSO-Cox](LASSO_Cox/README.md) | CANDIDATE；尚无工作流 |
| 随机森林预测 | [random_forest](random_forest/README.md) | CANDIDATE；尚无工作流 |
| 普通 / 时间依赖 ROC | [ROC](machine_learning/ROC/README.md) | CANDIDATE；尚无工作流 |

三个已实现方法的 README 都有中文输入要求、完整配置、运行命令和输出说明。默认配置中仍有提示性占位值，不能直接原样运行。VALIDATED 仅对应现有测试数据和范围，不是所有数据设计的 DEFAULT 推荐。

从[方法索引](../METHOD_INDEX.md)、[全局图例](../GALLERY.md)和[注册表](../registry/README.md)进入；先核对独立样本单位、缺失值、事件编码、混杂和验证范围。
