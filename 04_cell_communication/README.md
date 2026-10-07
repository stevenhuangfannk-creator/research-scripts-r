# 细胞通讯分析

这里用于配体–受体通讯假设，以及配体 → 靶基因响应模型。单凭表达不能证明因果信号或细胞物理接触。

| 需求 | 入口 | 当前实现 |
|---|---|---|
| 推断 LR 网络、通路和发送/接收角色 | [CellChat](CellChat/README.md) | 有脚本，CANDIDATE / BLOCKED，尚未执行验证 |
| 描述两个独立推断模型的差异 | [cellchat_compare](CellChat/README.md#比较两个条件) | 有脚本；要求恰好两个对象及相同标签顺序 |
| 解释接收细胞转录响应、优先筛选配体 | [NicheNet](NicheNet/README.md) | 候选说明，尚无脚本 |
| 汇总多方法通讯证据 | [LIANA](LIANA/README.md) | 候选说明，接口需明确 |
| Python CellPhoneDB | [接口说明](CellPhoneDB/README.md) | 参照原生 Python 方法目录 |

先读[方法索引](../METHOD_INDEX.md)、[图例](../GALLERY.md)和[登记规则](../registry/README.md)。目录存在不等于验证证据；细胞置换不等于供者级组间检验。
