# Method Card

**Method:** monocle3

**Category:** 03_cell_dynamics

**Status:** CANDIDATE

**Language:** R

**Package:** monocle3

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://cole-trapnell-lab.github.io/monocle3/docs/trajectories/

**Original paper:** https://doi.org/10.1038/s41586-019-0969-x

**Purpose:** Learn a principal graph and order expression states from justified roots.

**Biological question:** Learn a principal graph and order expression states from justified roots.

**When to use:** list(counts, aligned cell_metadata, gene_metadata with gene_short_name); explicit root cell IDs.

**When NOT to use:** Pseudotime ≠ real biological time. Disconnected partitions need justified roots. A graph branch is a hypothesis, not proof of cell fate.

**Required input:** list(counts, aligned cell_metadata, gene_metadata with gene_short_name); explicit root cell IDs.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** num_dim = 30; root_cells = mandatory biological choice; use_partition = True; close_loop = False; minimal_branch_len = 10; seed = 42

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Pseudotime ≠ real biological time. Disconnected partitions need justified roots. A graph branch is a hypothesis, not proof of cell fate.

**Outputs:** CDS; principal graph nodes/edges; pseudotime and reachability; trajectory and expression plots

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Pseudotime ≠ real biological time. Disconnected partitions need justified roots. A graph branch is a hypothesis, not proof of cell fate.

**Assumptions:** Pseudotime ≠ real biological time. Disconnected partitions need justified roots. A graph branch is a hypothesis, not proof of cell fate.

**Common pitfalls:** Pseudotime ≠ real biological time. Disconnected partitions need justified roots. A graph branch is a hypothesis, not proof of cell fate.

**Alternatives:** Slingshot fits lineages through clusters; tradeSeq tests trends along supplied trajectories; RNA velocity uses splicing kinetics; CellRank estimates fate probabilities.

**When to prefer alternatives:** Slingshot fits lineages through clusters; tradeSeq tests trends along supplied trajectories; RNA velocity uses splicing kinetics; CellRank estimates fate probabilities.

**Validated datasets:** None

**Validation status:** BLOCKED — Workflow not executed; required namespace/data unavailable

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 03_cell_dynamics/monocle3/scripts/workflow.R

**References:** https://cole-trapnell-lab.github.io/monocle3/docs/trajectories/; https://doi.org/10.1038/s41586-019-0969-x
