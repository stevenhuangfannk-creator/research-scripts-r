# Method Card

**Method:** cellchat

**Category:** 04_cell_communication

**Status:** CANDIDATE

**Language:** R

**Package:** CellChat

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://github.com/jinworks/CellChat

**Original paper:** https://doi.org/10.1038/s41467-021-21246-9

**Purpose:** Infer and visualize expression-supported ligand–receptor communication hypotheses.

**Biological question:** Infer and visualize expression-supported ligand–receptor communication hypotheses.

**When to use:** list(expression: aligned log-normalized RNA, metadata: cell labels); human or mouse DB.

**When NOT to use:** Inference is not physical contact, causal signaling or donor-level inference. population.size depends on capture/sorting design. PPI projection is an optional information projection step.

**Required input:** list(expression: aligned log-normalized RNA, metadata: cell labels); human or mouse DB.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** species = mandatory; expression_scale = lognormalized_RNA; average = triMean; population_size = False; min_cells = 10; nboot = 100; seed = 42; ppi_projection = False

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Inference is not physical contact, causal signaling or donor-level inference. population.size depends on capture/sorting design. PPI projection is an optional information projection step.

**Outputs:** LR probabilities and native permutation P values; count/strength matrices; pathway aggregation; network roles and optional patterns

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Inference is not physical contact, causal signaling or donor-level inference. population.size depends on capture/sorting design. PPI projection is an optional information projection step.

**Assumptions:** Inference is not physical contact, causal signaling or donor-level inference. population.size depends on capture/sorting design. PPI projection is an optional information projection step.

**Common pitfalls:** Inference is not physical contact, causal signaling or donor-level inference. population.size depends on capture/sorting design. PPI projection is an optional information projection step.

**Alternatives:** NicheNet for ligand → target response; CellPhoneDB/LIANA for complementary LR evidence.

**When to prefer alternatives:** NicheNet for ligand → target response; CellPhoneDB/LIANA for complementary LR evidence.

**Validated datasets:** None

**Validation status:** BLOCKED — Workflow not executed; required namespace/data unavailable

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** 04_cell_communication/CellChat/scripts/workflow.R

**References:** https://github.com/jinworks/CellChat; https://doi.org/10.1038/s41467-021-21246-9
