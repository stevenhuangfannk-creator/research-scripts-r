# Output Catalog

| Output | Scientific use / question | Figure | Code | Parameters | Main / Supplement | Execution |
|---|---|---|---|---|---|---|
| per-cell QC table | Inspect mitochondrial/ribosomal, feature and UMI metrics and record cell retention. | Match the numerical scale; use a table when no chart adds evidence | [workflow](scripts/workflow.R) | See method card | Main if it supports the study claim; QC/details in Supplement | PASS |
| retention audit | Inspect mitochondrial/ribosomal, feature and UMI metrics and record cell retention. | Match the numerical scale; use a table when no chart adds evidence | [workflow](scripts/workflow.R) | See method card | Main if it supports the study claim; QC/details in Supplement | PASS |
| QC-marked or explicitly filtered Seurat object | Inspect mitochondrial/ribosomal, feature and UMI metrics and record cell retention. | Match the numerical scale; use a table when no chart adds evidence | [workflow](scripts/workflow.R) | See method card | Main if it supports the study claim; QC/details in Supplement | PASS |

CORE OUTPUTS: above. OPTIONAL/ADVANCED/COMPARISON OUTPUTS: only those described in the method card; unimplemented features require a separate candidate.

VISUAL OUTPUTS: source-linked entries in the global gallery. TABLE OUTPUTS: the above numeric audits/results. OBJECT OUTPUTS: the workflow object, when supported.
