# 稳定性恢复代码审查 / Stability resume source review

本审查仅阅读恢复版`validate_perturbation.py`文本，没有导入重型包、加载模型、重算数值、修改代码或操作进程。审查快照SHA256：`37073004c70cf46b32833b5f5205f550e5f30e520dd615e1302755a5291a3417`。旧版本数学审查和本次恢复审查分别保存，不能将源码审查当作实际结果PASS。

## 当前数学保持一致 / Mathematical equivalence

- `delta=p_KO−p_same_seed_baseline`、velocity L2、seed0 reference先建立、冻结categorical终末cell IDs、strongest-half/cutoff选择和posterior criterion均保持原定义。
- `simulate`与`compute`都执行seed重置；二者之间的权重clone、确定性排序和hash没有消耗采样RNG，因此第二次重置仍从旧代码相同的seed起点执行official load+sampling。
- fingerprint包括解析后的完整config及fate/model/terminal受保护文件hash，涵盖posterior、kernel及终末定义。cell/gene/lineage顺序及有限值、CSV/H5AD概率一致与行和在`cached()`中检查。
- 在同一fingerprint下，相同seed及修改后的完整fc1矩阵字节hash代表相同模型参数与抽样路径；重复cutoff可以复制真实已有simulation。`reused_identical_weight_matrix_and_seed`明确记录来源，不冒称再次计算。
- `release_model`在保存数值并复制返回buffer后显式注销当前adata，再删除本model_id桶；调用者也删除model。初始只用于取weights的模型同样释放。没有提前删除计算依赖或改权重/速度/命运结果。

## 保留的疑虑 / Remaining review notes

1. 此快照的`cached()`检查finite和row-sum，但没有显式检查概率`>=−1e−10`及`<=1+1e−10`。旧缓存由原`_save_fate`生成时已做上下界校验，当前来源可信时没有发现错误；恢复接口的检查范围不能描述为它自己已完成上下界检查。
2. `cached()`没有把targets JSON中的TF/seed/cutoff/fraction/blocked_targets逐项与当前计算的`target_record`比较，checkpoint也未记录modified-weight signature。config/model fingerprint和可信tag来源保护了当前运行；增强条件语义核验可防止未来导入错误tag的完成标记。
3. 删除velocity_std/velocity_umap/旧graph并重写归一化obs.latent_time，是派生字段清理，不改变velocity/fate的数学。但`uns.velocity_uncertainty`及`obs.velocity_self_transition`仍可能继承；它们不能表示当前posterior的重新估计。
4. `compute`中的`_`仍指向velocity kernel，删除`kernel/result`后，当前函数内的GC时该alias还活着。当前mix=1没有kernel循环，函数返回后alias释放；这不重建scvi类级注册泄漏。若未来使用mixed kernel，应在GC前一并删除该alias。
5. 本审查没有执行cache或读取完整H5AD来证明实际恢复正确。应以恢复日志、checksums、MANAGER_RELEASE_QC及最终STABILITY_QC判断计算与资源表现；多训练seed和生物学验证仍为NOT_RUN。

这些意见不要求中断已恢复的真实计算。后续清理与补充校验应单独留痕，保护正式model/fate/terminal输入。

## 磁盘新版复查 / Follow-up on the saved source

随后只读对比确认磁盘脚本SHA256已变为`bfd4a221118a56611308b486f057d8eb175ecbc696dab9cdcce12b35b77c7ff7`。**这只确认磁盘源码，不确认活动进程已加载此版本。** 新版加入cached fate上下界检查、targets JSON逐项条件/列表对照，并使用h5py只读所需缓存数组；compute也清除velocity_uncertainty、自转移概率及旧posterior mean time等继承元数据。上述第1–3项针对第一快照的主要缺项已在磁盘源码修正。

当前仍需注明的缓存边界：fingerprint没有数值helper/API源码或软件版本，未来算法变化应增加明确缓存版本契约；`_probability_validation.json`虽被复制但不在checksum清单。原始h5py读取绕过AnnData形状校验，因此恢复检查可补充显式velocity/fate shape。当前文件由可信原计算保存，并未发现当前缓存数值或条件错误。

若后续仅清理旧stability H5AD的继承派生字段，其file hash会改变；应保存清理前后hash并更新对应checkpoint清单，否则下一次`--resume`将按既有设计拒绝改变的文件。清理不应改正式model/fate/terminal，也不应更改已核验的velocity/fate数值。
