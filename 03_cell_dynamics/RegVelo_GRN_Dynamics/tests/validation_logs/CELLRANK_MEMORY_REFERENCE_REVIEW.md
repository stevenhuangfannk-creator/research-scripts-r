# CellRank / pyGPCCA 对象引用只读审查

审查日期：2026-10-10。仅以文本读取当前模块和已安装包；未 import torch/scvi/CellRank，未运行模型，未修改代码，未操作进程。此报告给出源码支持的引用关系，不能证明当前进程的实际 RSS、pagefile 或 allocator 行为。

## 结论

未在检查的 CellRank estimator/kernel/pyGPCCA 路径发现保存每次 simulation 的全局 AnnData/model registry。VelocityKernel 的 transition/data cache 属于实例，不能据此解释不受限的全局累积。scvi registry 属于另一条引用链，应由负责 scvi 的审查者独立核实。

当前 `validate_perturbation.py` 使用 `GPCCA(kernel).set_terminal_states(labels)`，labels 是 categorical Series；该路径直接走父类 setter，没有 `compute_macrostates` / `compute_schur`。`SchurMixin._gpcca` 初始化为 None，当前路径不创建 pyGPCCA 分解对象，因此其 Schur/stationary cache 不是这段逐 simulation 的累积来源。

正式 `kernel_mix=1.0` 时 `_kernel` 返回 `(velocity, velocity)`；没有 mixed-kernel expression 父子循环。`_` 仍是普通强引用名称，先接官方返回模型，随后被 `_kernel` 返回的 velocity kernel 覆盖；这不清除独立的 scvi 全局引用，但也不代表每个模型一直存于该局部变量。

## 已确认引用链

- `estimator._kernel -> kernel`：site-packages/cellrank/estimators/mixins/_kernel.py:18。`estimator.adata` 从 `kernel.adata` 读取，:29。
- `kernel._adata -> result`：cellrank/kernels/_base_kernel.py:606。
- `estimator._shadow_adata` 是独立的稀疏零 X / obs / var shadow，若 source 有 raw 则复制 raw：cellrank/estimators/_base_estimator.py:61–65。shadow context 在 finally 恢复原 adata；没有把 estimator 写回 AnnData 的代码。
- VelocityKernel 保留 `_xdata/_vdata/_vexp/_vvar`，分别为 dense float64 输入/速度及 moments；`_extract_data` :258–284，初始化 :92–106。另保留实例 `_logits`、`_transition_matrix`、`_conn` 和 `_params`。
- `_reuse_cache` 仅对比 `self._params` / `self.transition_matrix`，cellrank/kernels/_base_kernel.py:446；不是模块级 memoization。
- mixed expression 才有 `parent._kexprs -> children` 与 `child._parent -> parent`，cellrank/kernels/_base_kernel.py:861–863。这类环可由 GC 回收；当前 mix=1 不建立它。
- `_save_fate` 把 `estimator.fate_probabilities`（Lineage ndarray）保存到 `result.obsm['lineages_fwd']`，dynamics.py:334；没有把 estimator/kernel 本体保存进去。
- Lineage 的 `__new__` 使用 `np.array(input_array, copy=True).view(cls)`，cellrank/_utils/_lineage.py:257；元数据是 names/colors/counts，不含 estimator/AnnData back-reference。
- compute_fate_probabilities 使用独立 `abs_classes` ndarray，包装为 Lineage，并复制写入 AnnData/shadow，cellrank/estimators/mixins/_fate_probabilities.py:441–511。返回 `np.asarray(Lineage)` 可持有对应数组 buffer/base，源码不支持它持有完整 estimator/kernel/result。
- BaseEstimator._create_params 的 inspect frame 在 finally 中 `del frame`，:289，没有持续保存调用 frame。

## 脚本保留的对象与规模

`simulate` 返回两个数组和 target count（validate_perturbation.py:92）。正常返回后，局部 result/estimator/kernel 引用消失；若别处仍持有这些对象，单纯 del 局部名称不能释放它们。

`baselines` 明确保留 3 个 seed 的 velocity/fate 数组，:100；697×1007 float32 velocity 约 2.68 MiB，每个 697×4 float64 fate 约 0.021 MiB，三组约 8.1 MiB。`reference` 保存两个 TF 的 delta/effect，:116，只有小型 697×4 / 697 向量。外层 loop 旧 velocity/fate 在下一次 simulate 的 RHS 执行时仍存活，但只增加一个已有结果数组，不是所有 simulation 的列表。

VelocityKernel 每实例四个完整 697×1007 float64 arrays 约 21.4 MiB（若 gene_subset 筛选则更小），加稀疏 graph/logits。direct solver 在 `_solve_lin_system` 将 transient-state A/B 临时 dense 化，cellrank/_utils/_linear_solver.py:406–414；697×697 float64 A 的上限约 3.7 MiB。该分支局部对象正常返回后可释放；唯一可见 global 是 PETSc 错误提示 bool，不保存矩阵。

pyGPCCA 在 Python 3.10 采用 functools.cached_property（:51），stationary_probability 的 cache 是实例属性（:1264）。旧 Python fallback lru_cache(maxsize=1) 可能保留一个实例，但本机 Python 3.10 不走 fallback，当前 simulation 也不创建 pyGPCCA 对象。

这些只说明 CellRank 侧的源码尺度和局部生命周期；不能据此排除 scvi manager、PyTorch CPU/GPU allocator、JAX/joblib native cache、HDF5 buffers 或 OS paging。低 free RAM 与变慢存在一致性，但尚未做运行时 profiling，因此不称为已证明原因。

## 安全释放建议（尚未实施）

完成 `_save_fate` 和 targets JSON 后，可先复制独立输出数组，再删除所有局部 alias 并 `gc.collect()`，随后返回。示意：

```python
velocity_out = np.asarray(result.layers['velocity']).copy()
fate_out = np.asarray(estimator.fate_probabilities).copy()
del estimator, kernel, result, _, custom
gc.collect()
return velocity_out, fate_out, len(targets)
```

`.copy()` 提供独立返回 buffer，峰值额外约一个 velocity/fate 数组；按已读 Lineage 源码它并非释放完整 AnnData 的必需条件。`del` 只移除本地 refs；`gc.collect()` 只回收不可达对象/循环，不清除仍可达的 scvi registry，也不保证 native allocator 立即向 OS 归还内存。当前 mix=1 路径没有必须手工打断的 CellRank 父子环。

如果以后采用 mixed kernel，可在结果保存并输出数组复制后 `del` estimator / composite / 两个基础 kernel aliases，再 GC；不要提前修改 `kernel.adata=None`、清空 private cache 或破坏尚需保存的 fate/transition，因为这些都是研究计算依赖。

若希望减少官方模型局部保留，应将 `_` 拆成 `perturbed_model` 与 `velocity_kernel` 两个明确名称，在输出完整保存后释放它们；scvi 的安全 deregistration 要按其实际 API 和全局 manager key处理，不能由此报告推定可删除全部 registry。

## 当前是否修改

无。仅生成这份 work review。正在运行的 script、源码、模型、正式 run_state 和进程均未触碰。
