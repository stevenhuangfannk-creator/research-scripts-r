# CellChat Output Catalog

API-audited capability catalog. **Execution BLOCKED** in this build; no native analytical preview is claimed.

| Plot/output ID | Class | Scientific question / suitable scene | Figure | Code | Parameters to review | Figure role | Evidence |
|---|---|---|---|---|---|---|---|
| `cc_circle_count_v1` | CORE / VISUAL | How many significant LR interactions connect cell groups? | circle | [code](scripts/visualize.R) | min.cells, threshold, vertex size | Main overview; dense network in Supplement | BLOCKED / UNVALIDATED |
| `cc_circle_strength_v1` | CORE / VISUAL | How much modeled interaction strength is aggregated per direction? | circle | [code](scripts/visualize.R) | average, population.size, edge scale | Main overview; keep scale matched across conditions | BLOCKED / UNVALIDATED |
| `cc_count_heatmap_v1` | CORE / TABLE / VISUAL | Which sender → receiver pairs have more modeled interactions? | source-target heatmap | [code](scripts/visualize.R) | cell label ordering, count vs weight | Supplement or main for focused cell types | BLOCKED / UNVALIDATED |
| `cc_strength_heatmap_v1` | CORE / TABLE / VISUAL | Which sender → receiver pairs carry greater aggregate modeled strength? | source-target heatmap | [code](scripts/visualize.R) | species DB, aggregate probabilities | Main for focused hypothesis | BLOCKED / UNVALIDATED |
| `cc_celltype_bubble_v1` | OPTIONAL / VISUAL | Which significant LR pairs occur in selected sender/receiver groups? | bubble | [code](scripts/visualize.R) | sources, targets, signaling, pairLR.use | Main when limited to a justified focused set | BLOCKED / UNVALIDATED |
| `cc_pathway_circle_v1` | CORE / VISUAL | Which cell groups participate in a selected pathway? | pathway circle | [code](scripts/visualize.R) | pathways, common edge maximum | Main with targeted biological rationale | BLOCKED / UNVALIDATED |
| `cc_pathway_hierarchy_v1` | OPTIONAL / VISUAL | How does a pathway flow toward specified receiver groups? | hierarchy | [code](scripts/visualize.R) | explicit receiver_indices; label/edge scale | Main for small networks | BLOCKED / UNVALIDATED |
| `cc_pathway_chord_v1` | OPTIONAL / VISUAL | How does a selected pathway connect cell groups? | chord | [code](scripts/visualize.R) | pathways, colors, grouping, gaps | Supplement for dense connectivity | BLOCKED / UNVALIDATED |
| `cc_pathway_heatmap_v1` | CORE / VISUAL | What is a pathway-specific source → target strength pattern? | heatmap | [code](scripts/visualize.R) | pathway, same limits/order | Main for a focused pathway | BLOCKED / UNVALIDATED |
| `cc_lr_circle_v1` | CORE / VISUAL | Which groups support a single ligand–receptor interaction? | LR circle | [code](scripts/visualize.R) | pair, pair_pathway, threshold | Main with independent validation | BLOCKED / UNVALIDATED |
| `cc_lr_table_v1` | CORE / TABLE | Which pairs have modeled probability and native permutation support? | sortable table / bubble | [code](scripts/workflow.R) | species DB, nboot, average | Supplement with complete table | BLOCKED / UNVALIDATED |
| `cc_centrality_v1` | ADVANCED / VISUAL | Which groups are modeled senders, receivers, mediators or influencers? | centrality role heatmap | [code](scripts/visualize.R) | netP centrality; selected pathway | Supplement unless role is central to claim | BLOCKED / UNVALIDATED |
| `cc_role_scatter_v1` | CORE / VISUAL | Which groups have larger modeled outgoing and incoming strength? | role scatter | [code](scripts/visualize.R) | common axis/dot limits, signaling subset | Main overview; avoid causal labels | BLOCKED / UNVALIDATED |
| `cc_outgoing_heatmap_v1` | CORE / VISUAL | Which pathways are associated with each sender? | signaling-role heatmap | [code](scripts/visualize.R) | pathway selection, cell ordering | Main or Supplement by density | BLOCKED / UNVALIDATED |
| `cc_incoming_heatmap_v1` | CORE / VISUAL | Which pathways are associated with each receiver? | signaling-role heatmap | [code](scripts/visualize.R) | pathway selection, cell ordering | Main or Supplement by density | BLOCKED / UNVALIDATED |
| `cc_contribution_v1` | CORE / VISUAL | Which LR pairs contribute to a selected pathway estimate? | contribution barplot | [code](scripts/visualize.R) | pathway, source/target filters | Main for mechanism hypothesis; not perturbation evidence | BLOCKED / UNVALIDATED |
| `cc_pathway_rank_v1` | CORE / VISUAL | How do total modeled pathway strengths rank? | ranking barplot | [code](scripts/visualize.R) | measure, pathway/resource version | Supplement for discovery ranking | BLOCKED / UNVALIDATED |
| `cc_pattern_outgoing_heatmap_v1` | ADVANCED / VISUAL | Which sender groups share latent signaling patterns? | NMF pattern heatmap | [code](scripts/visualize.R) | pattern_k must be selected via selectK + sensitivity | Supplement; assess stability | BLOCKED / UNVALIDATED |
| `cc_pattern_incoming_heatmap_v1` | ADVANCED / VISUAL | Which receiver groups share latent signaling patterns? | NMF pattern heatmap | [code](scripts/visualize.R) | pattern_k, NMF stability | Supplement | BLOCKED / UNVALIDATED |
| `cc_pattern_outgoing_river_v1` | ADVANCED / VISUAL | How do sender groups, patterns and pathways connect? | river/alluvial | [code](scripts/visualize.R) | pattern_k, contribution cutoff | Supplement | BLOCKED / UNVALIDATED |
| `cc_pattern_incoming_river_v1` | ADVANCED / VISUAL | How do receiver groups, patterns and pathways connect? | river/alluvial | [code](scripts/visualize.R) | pattern_k, contribution cutoff | Supplement | BLOCKED / UNVALIDATED |
| `cc_pattern_outgoing_dot_v1` | ADVANCED / VISUAL | Which sender-pattern/pathway contributions dominate? | pattern dotplot | [code](scripts/visualize.R) | cutoff, pathway/group subset | Supplement | BLOCKED / UNVALIDATED |
| `cc_pattern_incoming_dot_v1` | ADVANCED / VISUAL | Which receiver-pattern/pathway contributions dominate? | pattern dotplot | [code](scripts/visualize.R) | cutoff, pathway/group subset | Supplement | BLOCKED / UNVALIDATED |
| `cc_compare_total_count_v1` | COMPARISON / VISUAL | How do aggregate interaction counts differ between conditions? | comparison barplot | [code](scripts/compare.R) | same DB/labels/filtering; first/second order | Main descriptive comparison | BLOCKED / UNVALIDATED |
| `cc_compare_total_weight_v1` | COMPARISON / VISUAL | How do aggregate modeled strengths differ? | comparison barplot | [code](scripts/compare.R) | same averaging/population.size, cell sampling design | Main descriptive comparison | BLOCKED / UNVALIDATED |
| `cc_diff_circle_count_v1` | COMPARISON / VISUAL | Which directions have increased/decreased counts? | differential circle | [code](scripts/compare.R) | second minus first, count scale | Main small networks; Supplement dense | BLOCKED / UNVALIDATED |
| `cc_diff_circle_weight_v1` | COMPARISON / VISUAL | Which directions have increased/decreased modeled strengths? | differential circle | [code](scripts/compare.R) | second minus first, matched scales | Main focused hypothesis | BLOCKED / UNVALIDATED |
| `cc_diff_heatmap_count_v1` | COMPARISON / VISUAL | Where are source/target count changes concentrated? | differential heatmap | [code](scripts/compare.R) | label order, common limits | Main or Supplement | BLOCKED / UNVALIDATED |
| `cc_diff_heatmap_weight_v1` | COMPARISON / VISUAL | Where are source/target strength changes concentrated? | differential heatmap | [code](scripts/compare.R) | label order, common limits | Main or Supplement | BLOCKED / UNVALIDATED |
| `cc_differential_lr_v1` | COMPARISON / TABLE / VISUAL | Which LR probabilities change in selected cell directions? | increased/decreased bubble + delta table | [code](scripts/compare.R) | sources/targets, max.dataset, absence policy | Main focused set; full table Supplement | BLOCKED / UNVALIDATED |
| `cc_role_change_v1` | COMPARISON / VISUAL | Does a cell group change its incoming/outgoing role by pathway? | signaling-change scatter | [code](scripts/compare.R) | idents.use, excluded pathways | Main with biological support | BLOCKED / UNVALIDATED |
| `cc_compare_pathways_v1` | COMPARISON / VISUAL | Which pathway estimates differ in overall strength? | pathway comparison rank | [code](scripts/compare.R) | descriptive do.stat=FALSE; matched design | Main focused; no donor-level significance claim | BLOCKED / UNVALIDATED |
| `cc_embedding_functional_v1` | ADVANCED / COMPARISON / VISUAL | Which signaling networks have similar cell-role structure? | functional network manifold | [code](scripts/compare.R) | identical cell labels, kernel/embedding, number of pathways | Supplement / exploratory | BLOCKED / UNVALIDATED |
| `cc_embedding_structural_v1` | ADVANCED / COMPARISON / VISUAL | Which network topologies resemble each other? | structural network manifold | [code](scripts/compare.R) | topology, pathway coverage, embedding sensitivity | Supplement / exploratory | BLOCKED / UNVALIDATED |
| `cc_object_v1` | CORE / OBJECT | Can the complete inferred model be reused and audited? | object, no figure | [code](scripts/workflow.R) | package/DB versions and configuration | Archive locally; do not commit RDS | BLOCKED / UNVALIDATED |

## Interpretation and version boundary

CORE OUTPUTS include significant LR tables, modeled probability arrays, count/weight source–target
matrices and pathway networks. OPTIONAL OUTPUTS add focused sender/receiver and hierarchy/chord
views. ADVANCED OUTPUTS include centrality, NMF patterns and communication manifolds.
COMPARISON OUTPUTS use independently inferred models and an explicit first/second order.
VISUAL/TABLE/OBJECT outputs are labeled above; objects and full matrices remain outside Git.

Native CellChat permutation P values are not donor-level treatment tests or automatically
BH-adjusted LR FDR. Counts/strength depend on DB, expression coverage, labels and sampling design.
Functional similarity needs matching cell roles; structural similarity compares topology. Neither
embedding demonstrates temporal or causal progression. Pattern k needs selectK and stability review.

PPI projection is an optional information projection step. It smooths signaling expression;
traditional STRING/protein-interaction topology, hub genes and CytoHubba MCC belong in
[06_gene_networks/PPI](../../06_gene_networks/PPI/README.md).

Sources reviewed: [author repository/documentation](https://github.com/jinworks/CellChat),
[single-dataset tutorial](https://github.com/jinworks/CellChat/blob/main/tutorial/CellChat-vignette.Rmd),
[comparison tutorial](https://github.com/jinworks/CellChat/blob/main/tutorial/Comparison_analysis_of_multiple_datasets.Rmd),
[original paper](https://doi.org/10.1038/s41467-021-21246-9),
[protocol](https://doi.org/10.1038/s41596-024-01045-4).
Stable target tag is v2.1.2; current documentation source is development 2.2.0.9001.
API review does not prove Windows runtime compatibility. The legacy igraph patch is not imported.
