# 工作流审计与不确定项

## 主流程对象链

```text
whole_atlas_control_24h_seurat.rds + data/GSE280652/*.h5
  -> integrated_control_24h_seurat.rds
  -> integrated_control_24h_seurat_l1_annotated.rds
  -> integrated_immune_subset_seurat.rds
  -> integrated_immune_subset_l2_annotated.rds
  -> [缺少可执行合并步骤]
  -> integrated_liver_final_seurat.rds
  -> 巨噬/T-NK 三级注释（原位覆盖最终对象）
  -> CellChat / LIANA 结果与报告
```

## 关键缺口

- `mouse_liver_final_object.qmd` 只描述如何将一级和二级元数据合并回基础对象，代码块设置为 `eval: false`，而且注释称源对象“已按约定删除”。没有输入对象时无法重建最终对象。
- 三级巨噬和 T/NK 文档都读取并覆盖 `integrated_liver_final_seurat.rds`。运行时必须保留备份并固定顺序，否则部分元数据可能因使用旧副本而丢失。
- `spp1_T_subsets_communication_report.qmd`、`upstream_signal_macrophage_T_subsets_report.qmd` 和 `macrophage_neutrophil_cellchat.qmd` 只消费预计算结果，不负责生成它们。

## 重复与历史版本

- `mouse_liver_ccc_cellchat_cellphonedb.qmd` 是以整合最终对象为基础的较完整通讯入口。
- `SPP1_vs_Others_*` 和 `macrophage_TNK_cellchat.qmd` 使用旧的 `whole_atlas_*`、`macrophages_*`、`T_NK_*` 对象，属于较早的平行分支。
- `all_r_code_extracted.R` 只含 4 个查询/汇总代码块，与上游通讯报告重叠，不应作为独立主流程运行。
- `build_seurat.R` 的输出 `APAP_merged_seurat.rds` 未被当前任何脚本读取，暂时无法确认它与 Ben-Moshe 2022 对象的关系。

## 运行风险

- 两个三级注释脚本原位覆盖最终 RDS，应先纳入可复现的版本化对象命名。
- CellChat 1.6.1 与 igraph 2.x 的兼容函数属于本地补丁，升级包时需要重新验证。
- 所有分析对象和结果均未提供，文档中的细胞数只能视为历史记录，不能在本次整理中验证。
- `.gitignore` 排除了 RDS、H5、矩阵、结果目录、渲染物和缓存。公开前仍需核查未来加入的自定义元数据和未发表结果。
