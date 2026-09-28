# Phase 4B-3 Cell2location Reference Model Diagnostic

Date: 2026-09-28

## Environment

| Component | Actual environment |
|---|---|
| Python | 3.12.14 |
| PyTorch | 2.14.0+cpu |
| scvi-tools | 1.5.1 |
| cell2location | 0.1.5 |
| CUDA | unavailable |
| Accelerator used in smoke run | CPU |

`cell2location` was installed only inside the project-local `.venv`. Its
`RegressionModel` and `Cell2location` classes import successfully with the current
scvi-tools version. Package metadata declares `opencv-python` as a dependency; its
44 MB wheel download stalled and it remains absent. `pip check` therefore reports
this dependency gap, although the model classes used in the smoke run import and
start training without OpenCV.

## Training specification prepared

- input: 92,112 cells × 17,211 exact-intersection genes
- labels: 14 broad `major_cell_type` classes
- batch key: `sample_id`
- seed: `20260928`
- learning rate: `0.002`
- batch size: 2,500
- planned epochs: 100 for the first formal fit
- device: CPU because CUDA is unavailable

The versioned training script saves the model, posterior, reference signatures,
training history, loss plot and posterior-signature correlation diagnostics after
a completed fit.

## Smoke-run result and blocker

The model initialized correctly and entered training. Epoch 1 required about
54.8 seconds on the current CPU. A 100-epoch fit is therefore estimated at roughly
90 minutes before posterior sampling and QC; the commonly used longer reference
fits would require substantially more time.

The run was stopped after the timing measurement. No model, posterior or signature
file was presented as a trained result. This is primarily a **COMPUTE BLOCKER**,
with an additional environment-completeness warning for the missing declared OpenCV
dependency; it is not an input failure.

## Gate decision

**NOT PASSED.** Phase 4B-4 spatial mapping must not start until a complete reference
fit converges and its signature diagnostics pass. Recommended next action is to run
the existing script on a CUDA-capable environment, or explicitly accept a long CPU
run. Downsampling or shortening training solely to reach mapping is not accepted as
equivalent to the planned reference model.
