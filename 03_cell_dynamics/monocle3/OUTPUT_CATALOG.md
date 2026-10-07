# Monocle3 Output Catalog

API-audited capability catalog. **Execution BLOCKED** in this build; no native analytical preview is claimed.

| Plot/output ID | Class | Scientific question / suitable scene | Figure | Code | Parameters to review | Figure role | Evidence |
|---|---|---|---|---|---|---|---|
| `m3_cluster_trajectory_v1` | CORE / VISUAL | Where are clusters on the learned expression-state graph? | cluster trajectory | [code](scripts/visualize.R) | num_dim, clustering resolution, partition/graph settings | Main overview | BLOCKED / UNVALIDATED |
| `m3_celltype_trajectory_v1` | CORE / VISUAL | Do reviewed cell identities agree with graph topology? | cell-type trajectory | [code](scripts/visualize.R) | celltype_column; label evidence | Main | BLOCKED / UNVALIDATED |
| `m3_pseudotime_v1` | CORE / VISUAL / TABLE | How are reachable cells ordered relative to justified roots? | pseudotime gradient | [code](scripts/visualize.R) | root_cells; reachability; graph topology | Main; disclose root rationale | BLOCKED / UNVALIDATED |
| `m3_graph_nodes_v1` | CORE / VISUAL / TABLE | Where are roots, branch nodes and leaves in the principal graph? | annotated graph | [code](scripts/visualize.R) | minimal_branch_len, close_loop, roots | Supplement topology audit | BLOCKED / UNVALIDATED |
| `m3_backbone_v1` | OPTIONAL / VISUAL | What is the inferred principal-graph scaffold? | graph backbone with small cell marks | [code](scripts/visualize.R) | graph segment size; partitions | Supplement | BLOCKED / UNVALIDATED |
| `m3_gene_expression_v1` | CORE / VISUAL | Where do selected markers vary across states? | gene expression overlay | [code](scripts/visualize.R) | explicit unique feature IDs; zero expression retained | Main for selected markers | BLOCKED / UNVALIDATED |
| `m3_genes_pseudotime_v1` | CORE / VISUAL | How does selected gene expression vary along reachable pseudotime? | gene-versus-pseudotime curves | [code](scripts/visualize.R) | gene list, root; excluded unreachable-cell count | Main selected genes; detailed panels Supplement | BLOCKED / UNVALIDATED |
| `m3_gene_modules_v1` | ADVANCED / VISUAL / TABLE | Which graph-associated genes share activity across groups? | module-by-group heatmap | [code](scripts/gene_dynamics.R) | q_value; module resolution; cell groups | Supplement unless module is main claim | BLOCKED / UNVALIDATED |
| `m3_branch_expression_v1` | ADVANCED / TABLE | Which genes are associated with variation within a selected branch region? | selected-branch association table; expression overlays need separate implementation | [code](scripts/gene_dynamics.R) | explicit branch_cells; graph_test(knn) | Supplement; not a formal between-branch contrast | BLOCKED / UNVALIDATED |
| `m3_publication_v1` | CORE / VISUAL | Can an uncluttered panel communicate expression-state ordering? | publication pseudotime figure | [code](scripts/visualize.R) | size, theme; no unsupported temporal label | Main | BLOCKED / UNVALIDATED |
| `m3_3d_v1` | OPTIONAL / VISUAL | Is 3D topology informative beyond the 2D graph? | interactive 3D trajectory | Planned; no script | recompute 3-component UMAP/graph; plot_cells_3d | Supplement only if informative and dependency-ready | BLOCKED / UNVALIDATED |
| `m3_cds_v1` | CORE / OBJECT | Can CDS, graph and metadata be inspected and reused? | object + principal graph edge/node table | [code](scripts/workflow.R) | aligned input, versions, seeds | Local object archive; do not commit RDS | BLOCKED / UNVALIDATED |

## Interpretation and alternatives

Pseudotime ≠ real biological time. Root choice orients expression-state order; disconnected
partitions can have infinite pseudotime. Report the unreachable-cell count and root rationale.
Principal-graph branches/leaves are topology, not experimentally proven fate decisions.

Slingshot fits lineage curves through a cluster scaffold. tradeSeq tests gene trends/lineage
contrasts on supplied pseudotime and weights. RNA velocity estimates kinetic direction from
spliced/unspliced measurements. CellRank estimates transition/fate probabilities under kernels
and terminal-state assumptions. These methods are not interchangeable versions of one statistic.

CORE outputs are CDS/graph/pseudotime; OPTIONAL outputs include 3D; ADVANCED outputs include
graph association and modules. Formal branch comparisons and between-condition trajectory
contrasts require a separate validated model and are not claimed by the V1 branch subset code.

Sources reviewed: [trajectory tutorial](https://cole-trapnell-lab.github.io/monocle3/docs/trajectories/),
[gene-dynamics tutorial](https://cole-trapnell-lab.github.io/monocle3/docs/differential/),
[author repository](https://github.com/cole-trapnell-lab/monocle3),
[Cao et al.](https://doi.org/10.1038/s41586-019-0969-x),
[Packer et al.](https://doi.org/10.1126/science.aax1971).
The current tag v1.4.27 adds dependencies such as BPCells; compilation and namespace
loading must be verified before execution. No ungenerated trajectory is presented as evidence.
