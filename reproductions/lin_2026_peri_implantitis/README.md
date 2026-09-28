---
status: phase4a_preliminary
paper_doi: "10.1038/s41368-026-00447-2"
source_dataset: "Zenodo 10.5281/zenodo.19697596; GSE164241; GSE206621"
research_os_note: "10_Projects/README.md"
last_updated: "2026-09-28"
---

# Lin 2026 Peri-implantitis Flagship Reproduction

## Scientific question

This project reconstructs the computational logic used to study how inflammatory myofibroblasts shape neutrophil states in peri-implantitis. It covers the paper-wide computational architecture rather than a single cell type or figure.

## Evidence vocabulary

Every module uses one of these labels:

- **PAPER-REPORTED METHOD** — explicitly described in the paper or supplement.
- **EXACTLY REPRODUCED STEP** — the same public input, stated method and recoverable parameters were executed, with matching evidence.
- **METHOD-BASED RECONSTRUCTION** — the reported method was rebuilt, but author code or parameters were unavailable.
- **MODERNIZED IMPLEMENTATION** — a current reproducible implementation replaces an older or incomplete technical path while preserving the analytical question.
- **USER/CODEX ANALYTICAL CHOICE** — a documented decision added to make the reconstruction executable or auditable.
- **UNRESOLVED / UNAVAILABLE INFORMATION** — the source does not provide enough information for a defensible choice.

These labels describe individual steps. The project will not present reconstructed code as the authors' original code.

## Scope and scientific order

| Phase | Scope | Entry condition | Current status |
|---|---|---|---|
| 4A | PI scRNA-seq, healthy gingiva reference/integration, QC, annotation, abundance and state foundations | Public PI count matrices and a working isolated environment | preliminary integrated object generated; validation documented |
| 4B | PI and healthy spatial transcriptomics, cell2location and spatial programs | Stable 4A reference with defensible cell labels | not started |
| 4C | trajectory, communication, SCENIC, CellOracle, NMF and supported enrichment | Validated 4A/4B inputs for each module | not started |
| 4D | key figure reconstruction, code refactor and reusable asset extraction | Working analyses have been scientifically validated | not started |

The complete dependency graph is in [`notes/DEPENDENCY_GRAPH.md`](notes/DEPENDENCY_GRAPH.md). Modules are intentionally not executed in parallel.

## Public inputs

- PI scRNA-seq filtered 10x HDF5 files: Zenodo concept DOI `10.5281/zenodo.19697596`.
- PI spatial transcriptomics Space Ranger output: the same Zenodo record.
- Healthy oral/gingival scRNA-seq reference: GEO `GSE164241`.
- Healthy gingival spatial reference: GEO `GSE206621`.
- User-provided paper PDF and the official supplementary PDF are recorded in [`source/SOURCE.md`](source/SOURCE.md).

Raw data and generated binary objects remain outside Git. Acquisition scripts, checksums and provenance records are versioned.

## Phase 4A current result

The current preliminary integrated object contains 92,112 prior-corrected singlets across 21 PI/healthy samples and 21,934 intersected genes. It uses a scVI base model trained before doublet filtering, then projects the corrected singlets for clustering. This is a **MODERNIZED IMPLEMENTATION** and remains a preliminary foundation until donor-aware diagnostics, label review and paper-oriented figure comparisons are complete. The reported paper total is 90,551 cells; the difference is recorded in [`notes/PHASE4A_VALIDATION.md`](notes/PHASE4A_VALIDATION.md) and is not treated as an exact reproduction.

## Paper-reported computational methods

- Cell Ranger 7.0.0 with GRCh38-2020-A for PI scRNA-seq.
- Mitochondrial fraction filter `>25%`; doublets excluded, with the detection method not reported.
- Seurat and Scanpy for analysis, scVI for integration, and `schard` for object conversion.
- Space Ranger 1.3.1 with GRCh38-2020-A for Visium FFPE data.
- MiloR/edgeR for differential abundance; GO/GSEA for functional interpretation.
- cell2location and NMF for spatial mapping/programs.
- CellChat and COMMOT for communication analysis.
- Slingshot for trajectories; SCENIC and CellOracle for regulatory analysis.

Package versions, several thresholds, random seeds and intermediate annotations are not fully reported. The matrix in [`notes/METHOD_STATUS_MATRIX.md`](notes/METHOD_STATUS_MATRIX.md) records those gaps before execution.

## Phase 4A execution order

1. Create and verify the isolated Python environment.
2. Download the PI scRNA-seq archive from Zenodo and verify its published MD5.
3. Inventory all filtered 10x matrices and reproduce the reported per-sample and total cell counts.
4. Acquire and inventory the healthy reference from GSE164241.
5. Build per-sample objects; preserve raw counts and donor/sample metadata.
6. Apply documented QC and doublet reconstruction choices.
7. Train a donor-aware scVI integration model.
8. Cluster and annotate major cell types with marker evidence.
9. Reconstruct the major-cell landscape and supported differential-abundance results.
10. Validate each result before any refactor or reusable extraction.

## Validation targets

### Minimum success

- Verify the public PI archive checksum.
- Read all eight PI matrices.
- Reproduce the supplementary table total of 39,393 PI cells and its per-sample counts.

### Target success

- Reconstruct the 21-sample PI/healthy integrated reference.
- Compare total high-quality cells with the paper's 90,551.
- Recover the major cell classes and the qualitative disease shifts underlying Figure 1 and Supplementary Figure 1.

### Stretch success

- Produce validated neutrophil and fibroblast state objects that can safely feed Phase 4C.

## Environment

Phase 4A uses a project-local Python 3.12 virtual environment. Exact installed versions are recorded after successful installation; no global R or Python package library is modified. Advanced modules will receive separate dependency decisions only when their prerequisites exist.

## Current limitations

- No author analysis code or environment lockfile was released.
- Doublet detection, many clustering parameters, annotation rules and random seeds are not reported.
- PI donor D6 contributed two samples; sample and donor must not be treated as equivalent statistical units.
- The Zenodo metadata publication date is inconsistent with the record creation date and is preserved as a provenance anomaly.
- Cross-OS validation has not been performed.

## Project layout

- `source/` — immutable source/provenance records, not copied author code.
- `config/` — centralized reconstruction parameters.
- `scripts/` — numbered executable steps.
- `data/` — acquisition instructions; downloaded data are ignored by Git.
- `results/` and `figures/` — generated evidence locations; binaries are ignored by Git.
- `notes/` — dependency graph, feasibility audit and method/status decisions.
- `environment/` — isolated environment specification and exact package record.

