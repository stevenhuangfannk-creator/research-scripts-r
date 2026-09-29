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

Phase 4B-3 remains **NOT PASSED**. Phase 4B-4 was not started. The next step is
to return to the Phase 4A annotation evidence for clusters 33 and 47, reassign
cluster 47 to an evidence-supported epithelial/oral tissue label or mark it
unresolved, rebuild the 4B-2 reference input, and refit the reference model.
This changes a previously provisional biological label and must be reviewed
explicitly; it should not be hidden as a cell2location parameter adjustment.

## Outputs

- `models/phase4b/cell2location_reference/`
- `results/phase4b/cell2location_reference/reference_posterior.h5ad`
- `results/phase4b/cell2location_reference/reference_signatures.tsv.gz`
- `results/phase4b/cell2location_reference/training_history.tsv`
- `results/phase4b/cell2location_reference/reference_qc_summary.json`
- `results/phase4b/cell2location_reference/neutrophil_cluster_diagnosis.tsv`
- `figures/phase4b/cell2location_reference/`
