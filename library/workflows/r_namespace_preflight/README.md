---
status: validated
asset_type: workflow
language: R
dependencies: base R
promotion_decision: promoted_with_limitations
---

# R Namespace Preflight

## Purpose

Check whether the R packages required by a real analysis can be loaded before data download or computation begins. The workflow distinguishes package presence from namespace compatibility.

## Input

A tab-separated manifest with exactly three columns:

```text
group  package  required
core   Seurat  TRUE
```

`required` controls the exit code. Missing or unloadable optional packages are reported but do not make the command fail.

## Output

- `package_status.tsv`: installation, version and namespace-load status.
- `sessionInfo.txt`: runtime provenance.
- `preflight_summary.txt`: concise context and pass/fail summary.
- Exit code `2` when any required namespace cannot load; otherwise `0`.

## Command

```powershell
& 'C:\Program Files\R\R-4.3.1\bin\Rscript.exe' `
  library\workflows\r_namespace_preflight\preflight.R `
  --manifest path\to\packages.tsv `
  --output-dir path\to\environment `
  --context project_name
```

## Important boundary

This workflow verifies that declared namespaces load in the current R process. It does not install packages, resolve versions, create a lockfile, test data access or prove that an analysis is scientifically reproducible.

## Tested contexts

| Context | Adaptation | Result |
|---|---|---|
| Williams 2021 oral atlas reproduction | Supplied its 33-package manifest and existing environment output directory | Script ran unchanged; 5/7 required packages loaded; exit 2 |
| GSE255834 APAP scRNA-seq pipeline | Supplied its 14-package manifest and project Notes output directory | Script ran unchanged; 6/14 required packages loaded; exit 2 |

The transfer result is **worked with parameter changes**. Only the manifest, output directory and context label changed.

## Promotion decision

**PROMOTED WITH LIMITATIONS**, maturity `validated`.

The reusable unit is the environment workflow and manifest interface. Package lists remain project-specific. A failed preflight is a successful diagnostic result when it accurately prevents an incompatible analysis from starting.

## Provenance

**Origin:** Williams 2021 oral atlas reproduction environment check.

**Validated in:** Williams 2021 oral atlas reproduction and GSE255834 APAP scRNA-seq pipeline.

**Related Research OS:** `03_Methods/reproduction_environment_preflight.md`.

**Evidence:** each context keeps its package manifest, status table, summary and `sessionInfo.txt` beside the project documentation.
