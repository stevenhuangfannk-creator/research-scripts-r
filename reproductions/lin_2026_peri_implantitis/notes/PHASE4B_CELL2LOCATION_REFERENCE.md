# Phase 4B-3 Cell2location Reference Model

Date: 2026-09-29

## Status

**QC FAIL — spatial mapping must not start.** The numerical fit converged and
posterior sampling succeeded, but the reference labels contain a biologically
invalid neutrophil component. This is a reference-annotation failure rather than
a compute, CUDA or low-confidence-cell failure.

## GPU and environment decision

- Windows and `nvidia-smi` detect an NVIDIA GeForce RTX 4070 Laptop GPU with
  8,188 MiB memory; driver 596.08 reports CUDA 13.2 support.
- The working CPU `.venv` remains unchanged (`torch 2.14.0+cpu`).
- A separate `.venv-gpu` was cloned and only PyTorch was replaced with the
  official `torch 2.14.0+cu132` wheel.
- GPU smoke test passed imports of torch, scvi-tools and cell2location, a CUDA
  tensor operation, model initialisation and two training epochs.
- Formal environment: Python 3.12.14, torch 2.14.0+cu132, scvi-tools 1.5.1,
  cell2location 0.1.5, seed 20260928.

`pip check` reports only `cell2location 0.1.5 requires opencv-python`. Package
source inspection found the only OpenCV import in `cell2location.plt.RotateCrop`,
which is outside reference fitting, posterior export and matplotlib QC. OpenCV
was therefore not installed solely to make `pip check` green.

## Formal fit

| Setting | Value |
|---|---:|
| Cells | 92,112 |
| Genes | 17,211 |
| Cell types | 14 |
| Epochs | 250 |
| Batch size | 2,500 |
| Learning rate | 0.002 |
| Accelerator | GPU |
| Training time | 2,801 seconds |
| Initial ELBO | 500,446,784 |
| Final ELBO | 419,834,848 |
| Last-25-epoch relative slope | -6.44e-06 per epoch |

The 250-epoch choice follows the cell2location reference tutorial and was
checked against the observed loss trajectory. Loss was finite, decreased and
was stable over the last 25 epochs. No NaN, divergence or memory failure
occurred. The model, 1,000-sample posterior, signatures and training history are
saved under the required Phase 4B paths.

Two compatibility issues were repaired without retraining: current scvi-tools
expects `accelerator`/`device` rather than the legacy `use_gpu` posterior
argument; anndata 0.13 also requires DataFrame-valued `varm` entries to be
stored as matrices when a valid cell-type label contains `/`. Original factor
names remain preserved in `uns["mod"]["factor_names"]`.

## Quantitative QC

- all 14 signatures are finite, non-negative and non-zero;
- minimum posterior-signature versus raw cluster-mean correlation: 0.857;
- minimum median within-cell-type sample correlation: 0.832;
- minimum retained-versus-provisional-only correlation among cell types
  affected by low-confidence labels: 0.990;
- every cell type has at least one canonical marker among its top 500 genes.

The 2,080 low-confidence cells do not explain the failure. They affect seven
cell types, but neutrophils contain no low-confidence cells. Their removal would
therefore leave the invalid neutrophil component unchanged.

## Blocking biological finding

The 972 cells labelled `Neutrophils` comprise two Leiden clusters:

| Leiden cluster | Cells | FDCSP mean | FCGR3B mean | CSF3R mean | PTPRC mean | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| 33 | 270 | 0.83 | 1.95 | 3.63 | 4.50 | compatible with neutrophils |
| 47 | 702 | 6,324.74 | 0.001 | 0.017 | 0.063 | incompatible with leukocytes |

Cluster 47 expresses FDCSP, TACSTD2 and SPRR2A, lacks the leukocyte marker PTPRC
and lacks FCGR3B/CSF3R. Because it constitutes 72.2% of the nominal neutrophil
reference, FDCSP becomes 16.7% of the posterior neutrophil signature. This is
not a plausible broad neutrophil reference and would create misleading spatial
abundance estimates. Plasma-cell concentration in IGKC is biologically
expected and is not the blocking issue.

## Gate decision and required repair

The initial Phase 4B-3 attempt was **NOT PASSED** and Phase 4B-4 was not
started. It required review of Leiden 33/47 and a separately versioned
reference refit rather than a hidden cell2location parameter adjustment.
That correction and its new QC outcome are recorded below.

## Curated-v1 repair and repeat QC (2026-09-30)

Marker review identified Leiden 47 as an oral epithelial population: high
FDCSP, KRT13, SPRR2A and TACSTD2 with near-absent PTPRC, FCGR3B and CSF3R.
The new `16_curate_reference_labels.py` preserves the original input and writes
a separate `scrna_reference_counts_curated_v1.h5ad`, changing only those 702
cells from `Neutrophils` to `Epithelial cells`. All 92,112 cells and the 2,080
low-confidence cells remain. The exact before/after counts and marker evidence
are in `curated_v1_annotation_audit.json`.

The formal GPU reference refit used the same seed, 250 epochs and 2,500-cell
batches. Outputs are isolated under `curated_v1/` paths. The 250 training epochs
and 1,000-sample posterior sampling completed. A Windows Matplotlib/Tk error
occurred only when drawing the loss figure; switching to the non-interactive
`Agg` backend and loading the saved model/posterior completed postprocessing
without retraining. Exact training elapsed time and GPU peak allocation were
not preserved by this recovery path, so the machine-readable summary records
them as null; the live progress meter showed about 89 minutes of training.

| Curated-v1 check | Result |
|---|---:|
| Initial/final ELBO | 501,362,464 / 419,649,728 |
| Last-25-epoch relative slope | -6.54e-06 per epoch |
| Finite, nonnegative signatures | 14/14 |
| Minimum posterior-vs-raw-mean correlation | 0.781 |
| Minimum low-confidence retained-vs-provisional mean correlation | 0.990 |
| Minimum median sample correlation among qualifying samples | 0.832 |

The old and curated-v1 neutrophil signatures correlate only 0.193, confirming
the correction was consequential. FDCSP fell from 1,865.32 to 0.0076 in the
neutrophil signature, while CSF3R rose from 0.498 to 1.680. FCGR3B and CSF3R
now rank 193 and 41; the epithelial signature contains FDCSP/KRT13/TACSTD2.
The other 12 cell-type signatures each have old-vs-curated correlation at least
0.994 except epithelial, which is 0.684. The 2,080 low-confidence cells remain;
they do not explain the current failure.

**Curated-v1 reference QC remains FAILED.** Macrophage top genes include IGKC
(rank 3), IGKV4-1 (5) and IGHG1 (6). Its C1QA/B/C and CD68 ranks are 2,724,
2,976, 3,286 and 2,589, respectively, and their expression is greater in the
`Monocytes` signature. At the preliminary Phase 4A cluster level, the dominant
macrophage-labelled clusters 7/12 show MZB1/JCHAIN with weak C1Q/LST1/LYZ,
whereas monocyte cluster 25 has a stronger C1Q/LST1/LYZ pattern. This is a
biological label/mixture problem, not a numerical convergence problem. The
macrophage reference is also concentrated in one donor: IGT3 provides
1,531/1,885 cells (81.2%); only three samples provide at least 50 cells for
its within-type correlation check. Corrected neutrophils have 270 cells across
12 samples, but only IGT3 supplies at least 50, so a robust cross-sample
neutrophil signature check is also unavailable.

The automatic QC gate fails `macrophage_core_marker_top500`; inspection of the
marker heatmap supports the same conclusion. **Phase 4B-4 spatial mapping was
not started.** The next scientific step is a targeted review of myeloid and
plasma-like Phase 4A clusters and sample-level contamination/doublets, then a
new versioned reference input and fit. Do not silently reassign these clusters
or proceed with the current macrophage signature.

The GPU package freeze is in `environment/requirements-gpu-lock.txt`; the CUDA
PyTorch wheel is `torch 2.14.0+cu132` from the official PyTorch distribution.

## Outputs

- `models/phase4b/cell2location_reference/`
- `results/phase4b/cell2location_reference/reference_posterior.h5ad`
- `results/phase4b/cell2location_reference/reference_signatures.tsv.gz`
- `results/phase4b/cell2location_reference/training_history.tsv`
- `results/phase4b/cell2location_reference/reference_qc_summary.json`
- `results/phase4b/cell2location_reference/neutrophil_cluster_diagnosis.tsv`
- `figures/phase4b/cell2location_reference/`
