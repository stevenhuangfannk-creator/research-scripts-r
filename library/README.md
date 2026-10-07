# Reusable Research Assets

本目录是经过真实项目验证后才进入的共享资产入口。Phase 2 不预建空的 workflow、function 或 visualization 分类。

## Promotion rule

资产通常需要经过：

`USE → REPEAT → VALIDATE → ABSTRACT → REUSE`

进入共享库前应完成：

1. 去除项目专属路径、对象名和生物学假设；
2. 明确输入、输出、依赖和限制；
3. 提供最小可运行示例；
4. 在代表性数据上验证；
5. 保存来源项目和 Research OS 方法说明链接；
6. 绘图资产同时提供小型示例图。

## Maturity

- `candidate`：有复用价值，但没有完成第二场景验证。
- `validated`：在至少两个真实场景中成功使用；仍需遵守记录的边界。
- `stable`：经过多次使用，接口和限制已经稳定。
- `deprecated`：不再建议用于新分析。

## Current assets

| Asset | Type | Maturity | Promotion decision |
|---|---|---|---|
| [`r_namespace_preflight`](workflows/r_namespace_preflight/README.md) | Environment workflow | validated | PROMOTED WITH LIMITATIONS |

候选项及未晋升原因见 [`docs/phase3-candidate-review.md`](../docs/phase3-candidate-review.md)。

