# Method Card

**Method:** nichenet

**Category:** 04_cell_communication

**Status:** CANDIDATE

**Language:** R

**Package:** nichenetr

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://github.com/saeyslab/nichenetr

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Prioritize sender ligands that explain receiver transcriptional response.

**Biological question:** Prioritize sender ligands that explain receiver transcriptional response.

**When to use:** Sender/receiver expression, receiver DEG, background expressed genes, prior networks.

**When NOT to use:** Prior model and receiver contrast matter; ligand activity is predictive evidence, not causal proof.

**Required input:** Sender/receiver expression, receiver DEG, background expressed genes, prior networks.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = Receiver gene set/background; expression threshold; prior species.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** Prior model and receiver contrast matter; ligand activity is predictive evidence, not causal proof.

**Outputs:** Ligand activity ranking; ligand-target matrix; LR network; prioritization plots.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** Prior model and receiver contrast matter; ligand activity is predictive evidence, not causal proof.

**Assumptions:** Prior model and receiver contrast matter; ligand activity is predictive evidence, not causal proof.

**Common pitfalls:** Prior model and receiver contrast matter; ligand activity is predictive evidence, not causal proof.

**Alternatives:** CellChat for LR network without target explanation

**When to prefer alternatives:** CellChat for LR network without target explanation

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://github.com/saeyslab/nichenetr
