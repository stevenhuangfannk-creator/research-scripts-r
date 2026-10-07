# 登记表字段与状态说明

登记表使用 UTF-8 YAML 1.2，也使用与其兼容的 JSON 语法。ID 必须稳定且唯一；中文说明不改变机器读取的字段或 ID。

## 方法与执行证据

| 字段／值 | 含义 |
|---|---|
| `status: CANDIDATE` | 候选方法，尚未完成晋升所需验证 |
| `VALIDATED` | 有实际成功执行证据，使用时仍须遵守验证范围 |
| `RECOMMENDED` | 有比较证据支持推荐 |
| `DEFAULT` | 对明确问题有记录的默认优先选择 |
| `EXPERIMENTAL` | 实验性方法 |
| `DEPRECATED` | 已弃用，须保留原因与替代项 |
| `validation.status: PASS` | 指定数据与分支上的执行检查通过 |
| `UNVALIDATED` | 尚未验证执行 |
| `BLOCKED` | 受依赖、输入或其他条件阻塞 |
| `FAIL` | 实际检查失败 |
| `validated: true` | 只有真实成功运行后才能设置 |
| `script: null` | 当前没有可执行封装，仅有方法说明或规划 |

成熟度 `status` 与执行证据 `validation.status` 相互独立。内置小数据上的 `PASS` 只覆盖所记录的数据和执行分支，不能证明完整真实图谱的有效性或方法普遍优越性。V1 无自动默认的分析方法；比较与生物学适用性未记录前，`default_for` 保持为空。

## 图形选择

图形 `selection` 可以是 `CURRENT_DEFAULT`（当前优选模板）、`RECOMMENDED_ALT`（推荐替代模板）、`ARCHIVED`（归档）或 `null`。它只选择声明的输入／演示范围内的模板，不会晋升上游分析方法。

已经生成的图必须记录 `script`、`dataset`、`input_object`、`major_parameters`、`palette`、`theme`、`output_file`、`vector_file`、`last_generated` 及验证证据。计划中的图使用空输出路径和日期，不能设为 `CURRENT_DEFAULT`。弃用时保留旧稳定 ID，用 `replaced_by` 指向替代项。

## 查询与检查

在仓库根目录运行：

```sh
Rscript scripts/resolve_asset.R method scrna_qc
Rscript scripts/resolve_asset.R plot umap_clean_v1
Rscript scripts/resolve_asset.R palette okabe_ito
Rscript scripts/validate_library.R
```

前三条查询对应方法、图形和配色。最后一条检查结构与晋升规则，并更新结构检查记录；它不会执行完整科研分析。
