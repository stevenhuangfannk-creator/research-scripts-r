# Method Card

**Method:** cellphonedb

**Category:** 09_python_bridge

**Status:** CANDIDATE

**Language:** Python

**Package:** cellphonedb

**Package version:** See [build package evidence](../../docs/validation/package_status.tsv); never infer a version from package presence.

**Last validated:** Not validated

**Official documentation:** https://cellphonedb.readthedocs.io/en/latest/

**Original paper:** See official documentation citation; paper metadata not independently certified in this build.

**Purpose:** Test cell-label-dependent ligand–receptor coexpression.

**Biological question:** Test cell-label-dependent ligand–receptor coexpression.

**When to use:** Python expression matrix, metadata, database; approved orthology map for mouse.

**When NOT to use:** The legacy R LIANA MouseConsensus call is not execution of native Python CellPhoneDB.

**Required input:** Python expression matrix, metadata, database; approved orthology map for mouse.

**Optional input:** Only optional fields explicitly supported by the workflow/config; candidate contracts are planning specifications.

**Major parameters:** review_required = DB version; expression threshold; permutations.

**Recommended defaults:** Documented parameter starting points are not automatic biological defaults. No method is promoted to DEFAULT merely because the package is well known.

**Parameters requiring biological judgment:** The legacy R LIANA MouseConsensus call is not execution of native Python CellPhoneDB.

**Outputs:** Means/P values; significant LR pairs; source-target bubbles.

**Strengths:** Explicit data contract, provenance and outputs; small reusable scope.

**Weaknesses:** The legacy R LIANA MouseConsensus call is not execution of native Python CellPhoneDB.

**Assumptions:** The legacy R LIANA MouseConsensus call is not execution of native Python CellPhoneDB.

**Common pitfalls:** The legacy R LIANA MouseConsensus call is not execution of native Python CellPhoneDB.

**Alternatives:** CellChat; LIANA

**When to prefer alternatives:** CellChat; LIANA

**Validated datasets:** None

**Validation status:** UNVALIDATED — No executable evidence in this build

**Runtime notes:** Small demos are not benchmarks; record elapsed time and thread policy on the target data.

**Memory notes:** Keep sparse counts where possible; do not densify whole atlases. Large-object memory usage remains unbenchmarked.

**Best visualization:** Choose the matching [output catalog](OUTPUT_CATALOG.md), then inspect the registered gallery. No unrendered figure is a visual recommendation.

**Recommended scripts:** None: capability is a documented candidate.

**References:** https://cellphonedb.readthedocs.io/en/latest/
