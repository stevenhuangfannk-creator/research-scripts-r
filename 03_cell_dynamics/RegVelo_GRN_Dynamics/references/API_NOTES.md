# RegVelo 官方实现核查 / Official API audit

核查日期：2026-10-10。此文件证明源码、API 与来源经过核查；模型是否实际执行以运行目录的 stage 状态、日志和 QC 为准。

## 版本、许可与依赖 / Versions

| 来源 | 固定版本 | 许可与获取状态 |
|---|---|---|
| `theislab/regvelo` | `ae68f699b154b0559598e8f09e9ae4f30206975d`，2026-09-24 | BSD-3-Clause；直接 Git clone 因 github.com:443 超时失败，GitHub API 取得 SHA 后 Codeload 固定 SHA 的 ZIP 成功 |
| `theislab/regvelo_reproducibility` | `c3a696dcd44519fdfaa07b0fec26e4d327a0a683`，2026-05-12 | BSD-3-Clause；同上 |
| PyPI | 最新 `regvelo==0.4.2` | 2026-10-10 查询确认；本次源码快照单独锁定 |
| 文档 | https://regvelo.readthedocs.io/en/latest/ | HTTP 200，服务器最后修改时间 2026-08-29；源码快照更新于 9 月 |

快照保存在此目录的 `regvelo/`、`regvelo_reproducibility/`，不是成功的 Git clone，不能把 ZIP 目录的 Git 历史视为已获取。

源码 `pyproject.toml` 要求：Python >=3.10；`anndata>=0.10.8`；`scanpy>=1.10.3`；`scvelo>=0.3.2`；`scvi-tools>=1.0.0,<1.2.1`；`torch<2.6.0`；`torchode>=0.1.6`；`cellrank>=2.0.0`；`numpy>=1.25.2`；`scipy>=1.11.1,<1.16.0`；`pandas>=2.0.3`；`matplotlib>=3.7.3`；`seaborn>=0.13.2`；`cloudpickle>=3.0.0`；`mplscience>=0.0.7`。Python 3.10 是复现仓库明确推荐版本。

完整复现仓库额外依赖 CellOracle、Dynamo、UnitVelo、arboreto 等，并锁定 `distributed==2024.2.1`、`dask==2024.2.1`、`dask-expr==0.5.3`。运行 RegVelo 主案例无需为所有可选基线安装这一整套依赖。源码快照使用 `setuptools_scm`，因为没有 `.git`，安装时须设置 `SETUPTOOLS_SCM_PRETEND_VERSION_FOR_REGVELO=0.4.2`，同时记录实际源码 SHA；这不是宣称所有源码等同 PyPI 发布版。

## 论文及数据来源 / Sources

Crossref 验证 DOI `10.1016/j.cell.2026.04.022`，标题 *RegVelo: Gene-regulatory-informed dynamics of single cells*，Cell **189**(12), 3773–3800.e44，2026 年 6 月。官方完整文本入口为 https://www.cell.com/cell/fulltext/S0092-8674(26)00457-5 。Crossref 作者还包括 Daniel M. Fountain 和 Julianna O. Haug，README 的简版 BibTeX 未列出这两位，应使用正式元数据生成参考文献。

Figshare 官方项目 https://figshare.com/projects/RegVelo_reproducibility_datasets/226860 来自复现仓库 README。项目网页和 `https://api.figshare.com/v2/projects/226860/articles` 均返回 HTTP 403；未独立取得文章文件 ID、数据版本与数据许可。使用现行 `regvelo.datasets` 源码内的 Google Drive 链接成功取得首案例所需的两文件；不据此声称 Figshare 文件已核验。

| 文件 | 官方 API 与文件大小 | 本地 SHA256 |
|---|---|---|
| `adata_zebrafish_preprocessed.h5ad` | `datasets.zebrafish_nc(file_path)`；42,148,628 bytes | `eccab081c44cfe335b726aec8172bbcda072241b4f006f6420bb5d46d39611cb` |
| `prior_GRN.csv` | `datasets.zebrafish_grn(file_path)`；81,355,039 bytes | `356bfde785af53e36f9334c4f5032c06f111d67d30b881b41e24a8ebde7a536a` |

实际下载、服务器 `Last-Modified`、CRC32C、来源及本地路径见 `OFFICIAL_SOURCE_MANIFEST.csv` 和 `outputs/regvelo_data/raw/*.manifest.json`。本地 SHA256 是本次获取的可追溯标识；尚无独立发布的官方 SHA256 对照。

实际 AnnData 审计显示 697 细胞、8012 基因，`obs` 有 `cell_type, initial_size, initial_size_spliced, initial_size_unspliced, n_counts, stage`，index 名称为 `CellID`；没有 `hpf`。stage 为 `3ss, 6-7ss, 10ss, 12-13ss, 17-18ss, 21-22ss`，计数分别 `2,105,105,156,146,183`。这些是 somite stage，不应改名为 hours post fertilization。README/数据 docstring 宣称跨七个时间点，而本次下载对象实际仅含六个 stage，应按对象事实报告。先验 CSV 是 4508×4508 方阵，实际有 202 个非零 regulator rows、4459 个非零 target columns、25,617 条边；不能把全部 4508 行当作 TF 数量，也不能仅凭方阵识别方向。AnnData `is_tf` 标注 125 个 TF；官方教程是将这些 TF 与最终保留特征取交集。

`datasets.zebrafish_grn(file_path)` 当前实现总是重新 `pd.read_csv(remote)` 再写本地，不检查已有缓存，且不主动创建父目录。生产流程应在首次下载后读取本地 CSV。`zebrafish_perturb()` API 当前存在，描述 12,393 cells、27,599 genes、9 pools、22 TF targets；此次未下载该额外数据，不能标为已验证实验对照。

原始实验的来源可追溯到官方复现仓库链接的 Hu 等项目 `zhiyhu/neural-crest-scmultiomics`。其 README 指向 bioRxiv DOI `10.1101/2024.09.17.613303`，题目 *Single-cell multi-omics, spatial transcriptomics and systematic perturbation decode circuitry of neural crest fate decisions*。本次读取其 v1 全文（HTTP200），Methods 明确 Smart-seq3、Illumina NovaSeq 150-bp paired-end、zUMIs、STAR 2.7.3a、GRCz11 Ensembl105；Smart-seq3 BAM 经 velocyto `run --vv --umi-extension Gene -d 1 --without-umi` 计算剪接层。v1 Data availability 仅提供 Cell Browser 与 GRN viewer，未列出本次 Smart-seq3 的 GEO/SRA accession，故记录 `UNKNOWN`。全文出现的 `GSE106676` 是旧 bulk RNA-seq 用于 foxd3 参考序列构造，**不是此次斑马鱼单细胞数据 accession**。RegVelo Cell 原文当前 HTTP403，EuropePMC 验证 PMID `42119563`、首次在线 2026-05-12，但无 OA 全文。

## GRN 方向 / Matrix orientation

1. 生物学 prior CSV 与 Getting Started 接受 regulator×target。
2. `rgv.pp.set_prior_grn(adata, prior_net.T, keep_dim=False, cor_filter=True)` 的函数输入是 **target 行、regulator 列**。
3. 函数内部转置，输出 `adata.uns['skeleton']` 为 **regulator 行、target 列**，基因按输出 AnnData 顺序重排；对相关性加权后以绝对值 >=0.01 二值化并去除 self-loop；默认删除无输入/输出边的孤立基因。
4. `REGVELOVI(..., W=W.T, ...)` 的 **W 是 target 行、regulator 列**。
5. 模型 `module.v_encoder.fc1.weight`、`rgv.tl.inferred_grn(..., data_frame=True)` 返回 **target 行、regulator 列**；`GRN.loc[:, TF]` 是 TF 的下游。
6. `cell_specific_grn=True` 返回 `cells × targets × regulators`。

所有阶段应同时断言矩阵行列基因、顺序与特征对应；不能仅靠 4508×4508 的形状判断转置。

## 最小官方斑马鱼流程 / Minimal zebrafish workflow

依据 `docs/tutorials/zebrafish/tutorial.ipynb` 和 `grn_tutorial.ipynb` 核查，不把 notebook 已存图片当成本次复现产物。

```python
import anndata as ad
import numpy as np
import pandas as pd
import torch, scanpy as sc, scvelo as scv, scvi, cellrank as cr
import regvelo as rgv
from regvelo import REGVELOVI

scvi.settings.seed = 0
adata = ad.read_h5ad('adata_zebrafish_preprocessed.h5ad')
prior = pd.read_csv('prior_GRN.csv', index_col=0)
TF_list = adata.var_names[adata.var['is_tf']].tolist()
sc.pp.neighbors(adata, n_neighbors=30, n_pcs=50)
scv.pp.moments(adata, n_pcs=None, n_neighbors=None)
# Preserve a copy here for stochastic scVelo; RegVelo below min-max scales Ms/Mu.
adata = rgv.pp.preprocess_data(adata)
adata = rgv.pp.set_prior_grn(adata, prior.T)
TF_list = [g for g in TF_list if g in adata.var_names]
W = torch.tensor(np.asarray(adata.uns['skeleton']), dtype=torch.float32).T
REGVELOVI.setup_anndata(adata, spliced_layer='Ms', unspliced_layer='Mu')
model = REGVELOVI(adata, W=W, regulators=TF_list, soft_constraint=False)
model.train()
model.save('rgv_model')
adata = model.add_regvelo_outputs_to_adata(adata=adata, n_samples=30)
scv.tl.velocity_graph(adata)
terminal = ['mNC_head_mesenchymal', 'mNC_arch2', 'mNC_hox34', 'Pigment']
vk = cr.kernels.VelocityKernel(adata).compute_transition_matrix()
estimator = cr.estimators.GPCCA(vk)
estimator.compute_macrostates(n_states=7, cluster_key='cell_type')
estimator.set_terminal_states(terminal)
estimator.compute_fate_probabilities(solver='direct', use_petsc=False)
adata.obsm['lineages_fwd'] = estimator.fate_probabilities
terminal_sets = {state: estimator.terminal_states.index[
    estimator.terminal_states == state].tolist() for state in terminal}
ko, ko_model = rgv.tl.in_silico_block_simulation(
    model='rgv_model', adata=adata.copy(), TF='elf1', effects=0, cutoff=0)
ko.layers.pop('velocity_std', None)  # Source SD was not recomputed for this KO.
ko.uns.pop('velocity_uncertainty', None)
scv.tl.velocity_graph(ko)
scv.tl.velocity_embedding(ko, basis='umap')
kp = cr.kernels.VelocityKernel(ko).compute_transition_matrix()
ep = cr.estimators.GPCCA(kp)
labels = pd.Series(pd.Categorical([None] * ko.n_obs, categories=terminal), index=ko.obs_names)
for name, cells in terminal_sets.items():
    labels.loc[cells] = name
ep.set_terminal_states(labels)
ep.compute_fate_probabilities(solver='direct', use_petsc=False)
ko.obsm['lineages_fwd'] = ep.fate_probabilities
stats = rgv.mt.cellfate_perturbation({'elf1': ko}, adata, terminal_state=terminal)
grn = rgv.tl.inferred_grn(model, adata, label='cell_type', group='all',
                         data_frame=True, device='cpu')
```

对于已存在有效 `Ms/Mu` 的输入，模块默认保留 moments，避免重复处理；用户可显式请求重算。官方教程在本案例训练 hard 模式，Getting Started 的通用默认是 soft。论文复现仓库训练使用 full batch，而当前模块允许显式资源参数 batch=256，并在 `fit_qc.json` 登记这一偏离；不能把小批训练与论文完全相同的训练设置混淆。

官方教程的演示 TF 是斑马鱼 `nr2f5` 与 `elf1`；`Gabpa` 是通用 Getting Started 示例而非此斑马鱼分析依据。教程文字期望 `nr2f5` knockout 对 `mNC_head_mesenchymal` depletion、`elf1` knockout 对 Pigment depletion；这些是**待比较的参考结果**，不可预写为本次计算结论。

## 模式、采样与输出 / Training and outputs

| 模式 | 现行官方参数 |
|---|---|
| Hard GRN constraint | `soft_constraint=False, lam2=0`；prior mask 固定，没有新边 |
| Soft GRN constraint | `soft_constraint=True, lam=1, lam2=0`；prior 外的边有图惩罚 |
| Soft regularized | `soft_constraint=True, lam=1, lam2 in (0,1]`；另加 Jacobian L1 惩罚 |

`REGVELOVI.train(max_epochs=1500, lr=1e-2, weight_decay=1e-5, eps=1e-16, train_size=.9, batch_size=None, early_stopping=True, gradient_clip_val=10, optimizer='AdamW', **trainer_kwargs)`。`batch_size=None` 等于所有 cells；early stopping patience 固定 45，monitor=`elbo_validation`。`accelerator,devices` 通过 trainer kwargs 传递。

`add_regvelo_outputs_to_adata(n_samples=30, adata=None, batch_size=None)` 返回新 AnnData；输出 `layers['velocity'],layers['latent_time_regvelo'],layers['fit_t']` 和 `var['fit_scaling']=1.0`。实际代码没有写 `layers['fit_scaling']`，虽然 docstring 把它列为 layer。`fit_t` 按基因把 latent time 最大值缩放到 20，velocity 相应除以缩放因子。模块报告 per-cell mean fit_t min-max 以及原 posterior mean，不把两者当作绝对物理时间。

`ModelComparison(adata, terminal_states=None,state_transition=None,n_states=None).train(model_list=['hard','soft','soft_regularized'],lam2=0.1,n_repeat=1,batch_size=...)` 支持正式模式比较；依赖 `var['TF']` 和 `uns['skeleton']`。该封装未公开 max_epochs 参数（内部 train 默认），有限 smoke epochs 宜直接用模型接口并明确区分 smoke 与正式比较。支持 `Real_Time`, `Pseudo_Time`, `Stemness_Score`, `TSI`, `CBC` 指标，但后两者要提供有依据的 terminal states / state transitions，不能为通过指标而补造。

## Perturbation 与对照 / Knockout controls

`rgv.tl.in_silico_block_simulation(model,adata,TF,effects=0,cutoff=1e-3,customized_GRN=None,batch_size=None,n_samples=30)` 的参数是 **effects（复数）**；`effect` 是其 docstring 误写。函数加载模型，然后针对 TF 列中 `abs(weight)>cutoff` 的 target 把权重替换为 effects，保留 baseline RNA 状态；并返回 `(perturbed_AnnData, perturbed_REGVELOVI)`。这是一种 regulon 层面的模拟阻断，不是把真实细胞的 TF RNA counts 归零。

`customized_GRN=原 fc1.weight.detach().clone()` 与 `TF=[]` 是官方可接受的 no-op 路由；函数没有独立的 `null` 名称。由于 `REGVELOVI.load` 的初始化会消耗 RNG，模块在每次相同 load+simulation 前固定 seed，以官方 no-op 生成配对 baseline，再对 KO / null 采用同样随机序列。另找零有效权重 column 作为无下游边阴性对照并注明其 gene 身份；不能误称为已知阴性 TF。

CellRank terminal cells 必须采用 baseline 同一批 obs_names，而非在每个 KO 后重命名 macrostates 来适配预期。保存 forward terminal definitions、transition matrix、fate probability columns 并核对细胞/特征索引一致。模块在 KO 后重算 velocity graph/embedding，避免继承 baseline 的 `velocity_umap` 造成假对照图。

`rgv.mt.cellfate_perturbation(...,method='likelihood')` 的 depletion likelihood 当前实现是把 baseline 标为 1、KO 为 0 的 ROC AUC，等价于带 tie 处理的归一化 Mann–Whitney U 概率。>0.5 表示 baseline fate 分布更高，即预测 depletion；<0.5 表示预测 enrichment。p-value 来自 `scipy.stats.ranksums(KO,baseline,alternative='less')`，不是实验验证的 knockout 显著性；BH 校正在各 TF 的 terminal states 内执行，而非全部 TF×state 全局校正。模块原样标明 `FDR adjusted p-value`，跨 TF 汇总要清楚其校正范围。

局部 cosine effect = `1-cosine(v_baseline,v_KO)`，零范数 cells 应标缺失；fate difference = `KO-baseline`，二者是不同尺度，不能互相替代。官方 commitment score 是 `1-H(p)/log2(n_lineages)`，高分仅表示当前模型的命运分布集中；可靠性取决于速度方向和 terminal definitions。

## 已发现的 API 边界 / Implementation limitations

- `inferred_grn()` docstring 声称 `label/group=None` 可用，但非 cell-specific 分支实际访问 `adata.obs[label]` 并迭代 group。始终显式传 `label='cell_type', group='all'`，不要调用无参数全局 GRN。
- `inferred_grn` 默认 device=`cuda:0`；模型会移动到该设备，CPU 路由应显式传 device。返回 Jacobian 会除以平均绝对非零权重；全零网络会出现 NaN，必须独立核查。
- `compute_TF_regulon(adata,rgv_model,cluster_key,TF,TERMINAL_STATES,threshold=.4,n_states=7,n_samples=50,n_cells=30,solver='direct')` 不是简单权重排序，它会对上下游边逐条做 CellRank perturbation，可能昂贵。仅权重排序的图不得误称此官方功能已完成。
- Tutorial 中 `.transition_matrix.A` 对 scipy 新版不稳，模块采用 sparse 的 `.toarray()` 或 `sparse.save_npz`，并遵守 scipy<1.16。
- 官方 GRN tutorial 有局部 motif 图的 `fl1a` 拼写和 from/to 权重方向不一致，应以明确 `GRN.loc[target,regulator]` 为准，而不是复制这段图表数组。
- 官方 FAQ 要求先比较 scVelo stochastic/dynamical 或 veloVI；若基线无法识别轨迹，不能凭 RegVelo commitment score 宣称疾病进程。横断面病组不能自动当成真实时间。

源代码核查结束；下载成功不代表原始 count 层、所有原始测序 accession、所有模型模式或 Perturb-seq 对照已完成验证。有关这些结果应由实际审计与执行报告分别记录。
