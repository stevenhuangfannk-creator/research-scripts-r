# 重复模拟内存引用审查 / Repeated-simulation reference review

仅以文本读取本机 scvi-tools1.2.0 的 `model/base/_base_model.py`、`data/_manager.py`、`data/_utils.py`，以及固定官方 RegVelo 源码的 load、setup、addoutputs 和 perturbation 路径。没有导入 torch/scvi/CellRank，没有加载模型、测量运行内存、修改运行中的代码或操作进程。因此本报告确认的是**强引用机制**，不把变慢或 paging 的因果与规模写成已测量结果。

## 确认的注册引用 / Confirmed registration references

1. `BaseModelMetaClass`（L58–77）为每个模型类创建普通字典 `_setup_adata_manager_store` 和 `_per_instance_manager_store`，不是 weak-reference store。
2. `BaseModelClass.__init__`（L102–108）每次产生新的 model `id`，并调用 `_register_manager_for_instance`。后者（L232–243）将 manager 放入类级字典 `model_id → adata_uuid → AnnDataManager`。
3. `AnnDataManager.register_fields`（L193–199）将输入对象直接赋给 `self.adata`。这条 class dictionary → manager → AnnData 的强引用会在局部 model 名称删除后继续存在；所读文件没有对应 `__del__` 或 weak-reference 自动清理。
4. `BaseModelClass.load`（L724–732）调用 `setup_anndata` 和模型构造；官方 `in_silico_block_simulation`（L48）每次都 load。稳定性脚本为每次调用提供 `data.copy()`，故每个新模型桶可保留一整份模拟输入。
5. 复制输入沿用 `_scvi_uuid`；`AnnDataManager._assign_uuid` 和 `_assign_adata_uuid(overwrite=False)`保留已有UUID，所以 `_setup_adata_manager_store` 对同UUID通常替换上一条，主要无边界增长位置是每次不同 model_id 的 `_per_instance_manager_store`。
6. 官方 addoutputs（`_model.py` L734–748）再次复制target subset并刷新velocity/latent-time/fit_t。`get_velocity`和`get_latent_time`采用`torch.inference_mode`及局部采样列表；这里没有发现把全部采样列表全局保留的代码。输出副本与被manager持有的输入副本是两个对象，不能将全部保留都归于输出数组。

## 释放时机 / Release timing

仅在该模型对应结果已经完整保存、后续不再调用它时释放。scvi 的公开 `model.deregister_manager(model.adata)`显式传adata，可删除当前manager的类/instance映射；**无参数 `deregister_manager()`特意保留自己的manager**，不适合用来释放当前模型。

公开接口要求class store中的最新manager对应同一个adata对象。因此应在此次load/sampling/save结束后立即调用，在下一个同UUID的数据副本load之前完成。若已经有多个仍需使用的模型，不应全局clear全部store。

固定scvi版本下可随后精准删除该已完成model_id的空instance桶，再在调用者中删除model/result/estimator/kernel及所有kernel alias，最后调用`gc.collect()`。helper内部`del model`只删除函数参数；调用者也须解除自己的model引用。`torch.cuda.empty_cache()`只涉及CUDA缓存，不能解除CPU AnnData的类级强引用，也不能证明pagefile问题已经解决。

内存释放应通过每次完成后两类manager桶数、private bytes/RSS与耗时实际记录验证。新进程天然丢弃旧进程所有Python注册表；旧simulation数值可在严格验过条件和完整产物后复用，不需要为释放注册而重算研究结果。

## CellRank 侧 / CellRank side

独立只读检查见 [CELLRANK_MEMORY_REFERENCE_REVIEW.md](CELLRANK_MEMORY_REFERENCE_REVIEW.md)。当前 `kernel_mix=1` 没有混合kernel父子引用环；直接`set_terminal_states`没有计算macrostates/Schur，也没有创建pyGPCCA分解缓存。所读CellRank路径的cache属于实例，未发现保存每次simulation的全局AnnData registry。

三组baseline只保留velocity/fate数组，按697×1007 float32速度和697×4 float64概率估算约8.1MiB；这是基于dtype假设的源码尺度估算，不是内存profiling。`np.asarray(Lineage)`只保留数组buffer和names/colors等元信息，不反向持有完整estimator/AnnData。复制返回数组可使输出buffer独立，但单纯copy/del/GC仍不能释放scvi类级可达引用。

## 缓存恢复原则 / Cache recovery

完成的targets JSON在`_save_fate`之后写入，适合作为完成标记，但仍应核验完整H5AD、cell/gene/lineage索引、finite、概率上下界/行和、CSV与H5AD一致，以及model/fate/terminal文件hash。KO delta/effect CSV在simulation返回后才写；若只有这些表缺失，可从已核验的同seed baseline/KO数值重建，不能把表缺失当作必须重做后验抽样。

配置、posterior/kernel参数、受保护输入hash及恢复脚本版本应写入checkpoint/fingerprint；不同posterior设置下的同tag不能复用。实际同posterior seed且修改后的完整`fc1`矩阵字节完全相同，其他配置和模型相同时，可以复用同一真实数值，并明确`reused_tag`，不宣称再次模拟。
