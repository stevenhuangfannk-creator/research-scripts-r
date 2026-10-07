# V1 构建报告 / V1 build report

## 中文决策摘要 / Decision summary

本页是 **2026-10-07 V1 构建时的历史快照**。后续 V1 已合并到主分支，重要指南已经汉化；下方英文记录的分支、发布步骤和“未合并 main”描述属于当时状态。此次文档更新不新增科研执行证据，原始日志与登记表保持原样。

V1 总体为 `PARTIAL`（部分完成）：方法库结构、核心可复用流程及实际示例画廊已经交付，CellChat／Monocle3 原生执行、整合与富集等验证尚未全部完成。

| 关键决策 | 理由与使用边界 |
|---|---|
| 从科研问题进入方法索引 | 先确认输入、物种、样本设计和输出，再选包；避免把不同项目脚本当成可直接互换的通用工具 |
| 44 个入口分开标明执行状态 | 21 个有脚本、23 个尚无封装；10 个限定范围 PASS、8 个 BLOCKED、26 个 UNVALIDATED，不能把候选写成已完成 |
| 不设置通用 DEFAULT | 小型示例通过不等于真实图谱、生物学注释、条件效应或临床预测已验证；晋升需要问题特定的比较证据 |
| 保留原项目和历史路径 | 120 个来源文件与 28 个原 R／Quarto 脚本保留；旧的绝对路径、输入缺失和对象链问题在原项目说明中记录 |
| 分开管理分析与图形验证 | 34 个实际画廊项包括内置数据、合成演示和原创示意图；CURRENT_DEFAULT 只表示该范围的模板优选，不认证上游分析 |
| 原始对象与包库不进入 Git | 大型矩阵、RDS/H5、演示运行对象、安装包和缓存保留在本地，不把仓库变成数据镜像 |

### 下一步先做什么 / Next steps

1. 准备兼容的 R／Bioconductor 和源代码编译环境，用官方小数据完成 CellChat／Monocle3 原生流程及主要输出验证。
2. 再用真实多供者、多条件对象检查通讯比较、整合和样本级下游分析；记录起始细胞、身份、对照、物种／数据库与质控阈值的生物学依据。
3. 完成 ORA／fgsea 与真实富集曲线，逐项实现其他候选；比较过替代方法后再考虑 RECOMMENDED／DEFAULT。

历史包版本和范围见下方原始记录。当前入门操作见[中文使用指南](USAGE_ZH_CN.md)、[环境说明](ENVIRONMENTS.md)与[方法索引](../METHOD_INDEX.md)。

## 原始英文执行记录 / Original execution record

Date: 2026-10-07. **V1 status: PARTIAL.** The method-first architecture, reusable core
workflows, machine-readable registries and actual visualization/schematic gallery are
delivered. Priority-A CellChat/Monocle3 native execution and major-output galleries remain
BLOCKED; integration and enrichment validation are also incomplete. This build does not
claim to meet every V1 scientific capability acceptance criterion.

Evidence: [structural results](validation/structural_results.json), [execution results](validation/method_results.json),
[delivery checks](validation/delivery_checks.json), [figure QA](FIGURE_QA.md),
[preservation](validation/preservation.json), [Gallery](../GALLERY.md).

## What changed

The repository now starts from research questions in METHOD_INDEX, resolves method IDs in
registry/methods.yml, and links each method to an input contract, parameters, outputs and
validation boundaries. Graphics have their own registry, code, previews and metadata.
CODEX_RULES requires querying these assets before selecting new packages or templates.

- 44 method registry entries across 42 physical method units; 21 entries have executable
  parameterized workflows, and 23 explicitly have no runnable workflow yet.
- 10 methods have narrow PASS execution evidence; 8 are BLOCKED and 26 are UNVALIDATED.
  Three of the unvalidated entries are EXPERIMENTAL. No method is promoted to DEFAULT
  or RECOMMENDED without comparison evidence.
- 34 actual PNG/PDF gallery items, 9 palettes, 4 editable schematic templates and
  11 original vector primitives. Eight rendered helpers are CURRENT_DEFAULT for their
  declared template/input scope; this does not promote an underlying scientific method.
- Portable R entry points for ID lookup, configuration-driven execution, demo-input creation,
  registry integrity checks and smoke execution; lightweight R structural checks in CI.

## Old architecture

The initial entry point emphasized three projects: network pharmacology,
GSE255834 scRNA and the APAP mouse liver atlas. Project scripts mixed data-specific
paths, labels, workflow choices and graphics. Reproductions and library audit material
were already present and remain historical context. The starting tree, existing docs,
script catalog and all 28 original R/Quarto sources were reviewed before extraction.
See [pre-refactor audit](V1_AUDIT.md) and [complete tracked tree](validation/pre_refactor_tree.txt).

## New architecture

```text
METHOD_INDEX / registry -> method card -> workflow -> output catalog -> gallery
01_scrna_core                 02_differential_analysis
03_cell_dynamics              04_cell_communication
05_pathway_function           06_gene_networks
07_bulk_clinical_ml           08_visualization
09_python_bridge              10_scientific_schematics
90_examples                   95_inbox
99_legacy_projects            scripts / docs / registry
```

Units contain README, METHOD_CARD, OUTPUT_CATALOG, configuration, references and explicit
example/gallery status. Large CellChat and Monocle3 modules provide specialized code and
detailed output inventories. Smaller candidates document capability and gaps rather than
fabricating successful examples. YAML files use JSON syntax, which is valid YAML 1.2, and
are read with an explicit UTF-8 loader. Spatial-specific pipelines were not expanded.

## Files moved

**None.** The three projects are mapped by 99_legacy_projects instead of moved, preserving
existing relative paths. New small demonstrations live through 90_examples and the new
method/visualization units. Original historical example objects were not supplied locally.

## Files preserved

120 original project, reproduction, library and documentation files remain byte-identical
on this machine. SHA-256 and canonical Git blob IDs are recorded; CI accepts only Git line
ending normalization if a raw hash differs. The three projects and all 28 original R/Quarto
scripts remain at their original paths. Root README and .gitignore changed for the new
entry point and safe generated-asset allowlists.

The original checkout remains on phase4-flagship-reconstruction with its four pre-existing
untracked sensitivity files untouched. Work took place in a separate worktree on
`refactor/bioinformatics-skill-library-v1`. No reset, force push, stash, project deletion or
destructive history operation was used. The refactor starts from existing local commit
`2f12bd7850407fdae44497a116fab8368613526b`, retaining 23 earlier commits beyond the observed
remote main `3868aefa81d4d9ff635f20aa95675cb7cbe398df`. These are inherited work, not V1 changes.
Main was not merged or rewritten. Publish-history inspection found no prohibited data
extensions or blobs above 10 MiB in the inherited and V1 implementation range; see [history check](validation/publish_history_check.json).

## Methods extracted

From GSE255834/APAP: count+metadata alignment, explicit QC metrics/thresholds,
doublet/ambient candidate interfaces, LogNormalize/SCT, integration candidates,
PCA/neighbors/clusters/UMAP, hierarchical label writeback, exploratory markers and
CellChat communication input/output handling. New pseudobulk code performs raw-count
aggregation with an explicit sample/cell-type grouping contract.

Whole old scripts were not copied under new names. Tissue-specific decisions, automatic
APAP cell selection, old absolute paths, worker counts and igraph namespace patches were
not transplanted. CellChat PPI projection is documented as an optional information
projection; genuine STRING/Cytoscape/hub analysis is a separate PPI candidate.

Monocle3, correlation, survival and Cox supply new general interfaces grounded in official
APIs. CellChat's catalog covers 35 output types, including counts/weights, pathway/LR
networks, roles, patterns and multi-condition comparisons. Monocle3 covers CDS, graph,
biological root decisions, pseudotime and gene dynamics; pseudotime is explicitly distinct
from real time. Selected-branch expression is exploratory, not a formal between-lineage
contrast. Optional 3D remains planned. Target source tags/commits are in each references.yml.

## Methods validated

VALIDATED means only the declared smoke scope on the named input. It is not a certification
of a full atlas, biological annotation, treatment effect or clinical prediction.

| Method ID | Input | Executed acceptance scope |
|---|---|---|
| [`seurat_ingestion`](../01_scrna_core/data_ingestion/METHOD_CARD.md) | Seurat::pbmc_small (230 genes, 80 cells) | Counts/metadata alignment and counts preservation only |
| [`scrna_qc`](../01_scrna_core/quality_control/METHOD_CARD.md) | pbmc_small plus explicit three-gene arithmetic fixture | pbmc_small lacks mitochondrial/ribosomal genes; audit/filter and exact arithmetic guards only |
| [`lognormalize`](../01_scrna_core/normalization/lognormalize/METHOD_CARD.md) | Seurat::pbmc_small | LogNormalize branch; preserves counts and creates finite RNA data layer |
| [`seurat_clustering`](../01_scrna_core/clustering/METHOD_CARD.md) | Seurat::pbmc_small | PCA/neighbors/clustering/UMAP on all 80 cells; not full-atlas robustness |
| [`hierarchical_annotation`](../01_scrna_core/annotation/METHOD_CARD.md) | Seurat::pbmc_small | Label writeback and Unknown fallback; biological annotations are not validated |
| [`cell_markers`](../02_differential_analysis/differential_expression/METHOD_CARD.md) | Seurat::pbmc_small | Exploratory cluster-marker table; no sample-level treatment inference |
| [`pseudobulk`](../02_differential_analysis/pseudobulk/METHOD_CARD.md) | Seurat::pbmc_small (one original sample) | Raw-count summation/count conservation only; replicated condition testing is unvalidated |
| [`correlation`](../07_bulk_clinical_ml/correlation/METHOD_CARD.md) | datasets::iris (150 observed flowers) | Pearson/Spearman tests, BH adjustment and missing/constant-input regression cases; pooled species are confounded |
| [`survival_km`](../07_bulk_clinical_ml/survival/METHOD_CARD.md) | survival::lung (228 public clinical records) | Right-censored KM curve/CI table with explicit 0/1 event mapping; no new clinical interpretation |
| [`cox`](../07_bulk_clinical_ml/Cox/METHOD_CARD.md) | survival::lung (age and sex covariates) | Cox HR/CI and proportional-hazards diagnostic output only; no predictive or causal certification |

Regression checks cover shuffled metadata alignment, exact mt/ribo arithmetic and retained
cell identity, invalid annotation maps and Unknown fallback, one-group pseudobulk count
conservation, correlation missingness/constant inputs, and UTF-8 registry parsing under a
Windows C locale. All ten method checks plus the parser regression passed. The CSV CLI
produced a correlation table/session/metadata; Plot-ID resolution passed; an unvalidated
CellChat request without an explicit opt-in failed before input loading as intended.
See [CLI evidence](validation/cli_checks.txt), [smoke log](validation/smoke_log.txt).

Cell markers produced tied-value Wilcoxon warnings and use asymptotic inference; they are
exploratory markers. QC's tiny arithmetic fixture is synthetic and explicitly separate from
the observed PBMC input, which lacks mitochondrial/ribosomal features. Numerical Cluster
labels validate annotation writeback, not immune-cell biological identities. Package
startup/locale warnings are preserved, with interpretation in the figure QA record.

## Methods unvalidated

| Method ID | Execution evidence | Workflow delivered? | Main limitation |
|---|---|---|---|
| [`scdblfinder`](../01_scrna_core/doublet_detection/scDblFinder/METHOD_CARD.md) | BLOCKED / CANDIDATE | Yes; not run | there is no package called 'scDblFinder' |
| [`decontx`](../01_scrna_core/ambient_rna/DecontX/METHOD_CARD.md) | BLOCKED / CANDIDATE | Yes; not run | there is no package called 'celda' |
| [`cellchat`](../04_cell_communication/CellChat/METHOD_CARD.md) | BLOCKED / CANDIDATE | Yes; not run | there is no package called 'CellChat' |
| [`cellchat_compare`](../04_cell_communication/CellChat/METHOD_CARD.md) | BLOCKED / CANDIDATE | Yes; not run | there is no package called 'CellChat' |
| [`monocle3`](../03_cell_dynamics/monocle3/METHOD_CARD.md) | BLOCKED / CANDIDATE | Yes; not run | there is no package called 'monocle3' |
| [`monocle3_dynamics`](../03_cell_dynamics/monocle3/METHOD_CARD.md) | BLOCKED / CANDIDATE | Yes; not run | there is no package called 'monocle3' |
| [`go_kegg_ora`](../05_pathway_function/GO_KEGG/METHOD_CARD.md) | BLOCKED / CANDIDATE | Yes; not run | there is no package called 'clusterProfiler' |
| [`fgsea`](../05_pathway_function/GSEA/METHOD_CARD.md) | BLOCKED / CANDIDATE | Yes; not run | there is no package called 'fgsea' |
| [`sctransform`](../01_scrna_core/normalization/SCTransform/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | Yes; not run | No executable evidence in this build |
| [`harmony`](../01_scrna_core/batch_integration/Harmony/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | Yes; not run | No executable evidence in this build |
| [`seurat_integration`](../01_scrna_core/batch_integration/Seurat/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | Yes; not run | No executable evidence in this build |
| [`soupx`](../01_scrna_core/ambient_rna/SoupX/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`slingshot`](../03_cell_dynamics/slingshot/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`tradeseq`](../03_cell_dynamics/tradeSeq/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`nichenet`](../04_cell_communication/NicheNet/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`cellphonedb`](../09_python_bridge/CellPhoneDB/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`liana_plus`](../04_cell_communication/LIANA/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`gsva_ssgsea`](../05_pathway_function/GSVA_ssGSEA/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`ucell_aucell`](../05_pathway_function/UCell_AUCell/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`ppi`](../06_gene_networks/PPI/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`wgcna`](../06_gene_networks/WGCNA/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`hdwgcna`](../06_gene_networks/hdWGCNA/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`scenic`](../06_gene_networks/SCENIC/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`bulk_deseq2`](../07_bulk_clinical_ml/bulk_RNAseq/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`limma`](../07_bulk_clinical_ml/bulk_RNAseq/limma/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`lasso`](../07_bulk_clinical_ml/LASSO/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`lasso_cox`](../07_bulk_clinical_ml/LASSO_Cox/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`random_forest`](../07_bulk_clinical_ml/random_forest/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`roc`](../07_bulk_clinical_ml/machine_learning/ROC/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`differential_abundance`](../02_differential_analysis/differential_abundance/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`scvelo`](../09_python_bridge/scVelo/METHOD_CARD.md) | UNVALIDATED / EXPERIMENTAL | No; method card/catalog only | No executable evidence in this build |
| [`cellrank`](../09_python_bridge/CellRank/METHOD_CARD.md) | UNVALIDATED / EXPERIMENTAL | No; method card/catalog only | No executable evidence in this build |
| [`scanpy`](../09_python_bridge/Scanpy/METHOD_CARD.md) | UNVALIDATED / CANDIDATE | No; method card/catalog only | No executable evidence in this build |
| [`foundation_models`](../09_python_bridge/foundation_models/METHOD_CARD.md) | UNVALIDATED / EXPERIMENTAL | No; method card/catalog only | No executable evidence in this build |

Candidate source retrieval is not scientific validation: official documentation URLs were
audited for 44 entries; 43 returned HTTP 200, while the historical WGCNA documentation
endpoint was not retrieved. Metadata/catalog depth outside the two exemplars varies and
requires full tutorial/paper review before implementation or promotion. Installed Harmony,
AUCell, glmnet and randomForest namespaces alone do not justify method validation.

## Gallery generated

34 actual R-rendered PNG/PDF pairs: 21 observed-data examples (10 PBMC, 8 iris descriptive/
correlation, 2 lung survival/Cox, 1 held-out iris ROC), 8 clearly synthetic style fixtures,
1 palette sheet and 4 original schematic templates. The schematics also have editable SVGs.
The total is gallery items, not 34 independent scientific workflows or all requested plot types.

The gallery covers UMAP, FeaturePlot, DotPlot, marker/cluster heatmaps, violin/stacked violin,
composition/count bars, multi-panel layouts, box/density/ridge, scatter/regression/CI,
BH-aware correlation heatmap, two-pair panels, KM+risk table, HR forest, held-out ROC,
volcano/enrichment dot/lollipop/waterfall, alluvial/chord/network styles and signed-score heatmap.
All previews link to method/code, input, parameters, palette/theme, date and vector output.

43 planned native examples (33 CellChat, 10 Monocle3) have no generated paths/dates and
cannot be CURRENT_DEFAULT. Actual GSEA curves, cell/sample pathway scores and advanced
ComplexHeatmap annotation are still absent. Synthetic enrichment or network illustrations
do not satisfy the native biological output requirements.

Nine palettes include ggsci NPG/AAAS/NEJM/Lancet/JAMA-inspired categories, Okabe-Ito,
viridis, cividis and a blue-white-red diverging specification, with capacity limits and source/
accessibility fields. Named cell/condition colors are independent assets. Journal-inspired
colors are not presented as official journal palettes or automatically CVD-safe.

## Data used

| Data | Size / use | Integrity boundary |
|---|---|---|
| SeuratObject::pbmc_small | 230 features, all 80 observed cells | No cell downsampling; selected marker/top-10 variable genes are display choices. One capture cannot validate batch integration or replicated DEG. |
| QC arithmetic fixture | Explicit three genes / two cells | Synthetic exact-percent and filtering regression fixture, not a biological dataset. |
| datasets::iris | All 150 observed flowers | Descriptive/correlation figures retain all records. Pooled species are a stated confounder. |
| Iris RF/ROC split | Seed 42; 35 training records/species; 105 train / 45 held-out | Held-out versicolor-versus-rest illustration. This sample split is the stated model design, not figure downsampling. |
| survival::lung | 228 public clinical records | Event = status==2; sex=1/2 and age used explicitly. No new causal or clinical recommendation. |
| Eight synthetic styles | Small deterministic fixtures, seed 42 where stochastic | Captions explicitly say SYNTHETIC STYLE DEMO; no experimental findings. |
| Schematics/palettes | Original grid shapes and public package color specifications | No protected journal figure or external icon downloaded; no specific mechanism asserted. |

No raw matrices, RDS, H5, sequencing data or compressed datasets were added. Runtime
objects/demo CSVs stay under ignored results/. Package binaries and installation caches
stay outside the repository. No blanket repository license was imposed; original components
and package/source licenses are recorded in [provenance](PROVENANCE_AND_LICENSE.md).

## Package versions

R 4.3.1, Windows x86_64. Extra CRAN Windows binaries were installed into an isolated build
library via R_LIBS; the user's existing package library was not replaced. Full package and
platform evidence: [package status](validation/package_status.tsv), [sessionInfo](validation/sessionInfo.txt),
[environment guidance](ENVIRONMENTS.md).

| Package | Observed installed version | Namespace preflight |
|---|---|---|
| Seurat | 5.2.1 | Loaded |
| SeuratObject | 5.0.2 | Loaded |
| Matrix | 1.6.5 | Loaded |
| ggplot2 | 3.5.2 | Loaded |
| patchwork | 1.3.1 | Loaded |
| ragg | 1.3.3 | Loaded |
| svglite | 2.1.3 | Loaded |
| harmony | 1.2.3 | Loaded |
| CellChat | Not installed | BLOCKED |
| monocle3 | Not installed | BLOCKED |
| scDblFinder | Not installed | BLOCKED |
| celda | Not installed | BLOCKED |
| clusterProfiler | Not installed | BLOCKED |
| fgsea | Not installed | BLOCKED |
| GSVA | Not installed | BLOCKED |
| UCell | Not installed | BLOCKED |
| AUCell | 1.24.0 | Loaded |
| survival | 3.8.3 | Loaded |
| glmnet | 4.1.8 | Loaded |
| randomForest | 4.7.1.2 | Loaded |
| pROC | 1.18.5 | Loaded |
| yaml | 2.3.10 | Loaded |

CellChat target tag v2.1.2 is API-reviewed but not installed; audited current development
documentation reports 2.2.0.9001. Monocle3 target tag v1.4.27 is not installed. Version
compatibility for either is unproven. The environment is not represented by a fabricated
renv lockfile. Installed binaries built under R 4.3.2/4.3.3 emitted build-version warnings.

## Remaining blockers

1. CellChat/Monocle3 and several Bioconductor dependencies are absent, and no Rtools/make
   toolchain is available for required source compilation on this host. The native inference,
   plots and comparison APIs remain execution-unverified.
2. Legacy Seurat/RDS and APAP inputs are absent. Built-in PBMC is too small and single-sample
   to validate multi-condition communication, biological trajectory roots, batch correction,
   replicated pseudobulk DEG or condition-specific composition inference.
3. Priority A integration, GO/KEGG/ORA and fgsea require representative inputs and actual
   execution; their catalogs and synthetic plotting styles are not acceptance evidence.
4. Many Priority B/C entries are documented candidates without reusable code or actual
   output galleries. WGCNA's historical documentation retrieval remains unresolved.
5. Clinical/ML pipelines beyond the demonstrated KM/Cox/ROC scope, time-dependent ROC,
   mature biological annotation dictionaries, GSEA curves, pathway activity figures and
   advanced heatmap annotations need further implementation/validation.

## V1 → V2 recommendations

First complete V1: establish a compatible R/Bioconductor/source-build environment, reproduce
official small CellChat and Monocle3 demonstrations, and generate every major native output
with the declared stable API. Then use a real multi-donor, multi-condition annotated object
to validate CellChat comparisons, integration and sample-aware downstream analyses. Roots,
cell identities, contrasts, species/database choices and QC cutoffs require documented
biological decisions. Record warnings, runtime/memory, exact input provenance and package
versions before promoting any method.

Next validate ORA/fgsea and a real enrichment curve; implement sample/cell-level scores with
appropriate inference units. Promote templates only after real-data inspection and compare
alternatives before setting analytical DEFAULTs. Add Priority B/C units one at a time rather
than increasing placeholder count. Capture per-workflow tested environments when complete;
extend CI to execute those specific small validated fixtures. Keep spatial-specific work in
its existing project context.

## Git commits created

- `ef94ea06bc98b4e4e9b9ae9f26ebf2a357a17abd` — `feat: initialize R-first bioinformatics method and visualization library`.
- V1 原始最终证据提交 / original evidence commit: `ba2079c0baf57f468998c6ae11deec72f84d078a` — `docs: record V1 build evidence and implementation commit`.
  这是 V1 的原始提交；后续文档翻译提交不计入原始 V1 构建范围。

Delivery branch: `refactor/bioinformatics-skill-library-v1`. The inherited 23 local commits
are preserved history and excluded from these two V1 commits. The branch is published
without merging or rewriting main. The final terminal status includes the delivery HEAD.
