# Phase 4B-4 PI spatial mapping

Date: 2026-09-30. Status: formal PI fit/posterior complete; PI QC BLOCKED by
depth association. Healthy mapping not started.

## Inputs and provenance

This is METHOD-BASED RECONSTRUCTION / MODERNIZED IMPLEMENTATION, not recovered
author code. The reference is the audited curated-v2 89,974-cell, 14-type model,
recorded at commit `8496f3a4ea4c75eb35b269995e9e3a6e91f12925`. Only its newly
trained `reference_signatures.tsv.gz` is supplied to spatial mapping; the old
reference signatures are not read. The signature SHA256 is
`9b244c33c045f47f2b9f5d63dee4a982eedcd6d150655b3684cfad23b39cb148`.

All nine input samples passed exact gene-set/order, duplicate-symbol, integer
count-layer, barcode, sample and coordinate checks. Each has 17,211 shared
genes and is fitted independently. `Unresolved` is not a mapping factor.
PI has 640 tissue spots and median original counts of 34,769. The Phase 4B-2
PI matrix did not carry coordinates; its mapping derivative restores them by
exact barcode join to the previously validated Space Ranger QC table. Original
counts, detected genes, array/pixel coordinates, condition, source and tissue
membership are retained. No raw inputs or reference objects are overwritten.

The complete preflight, including sample/input hashes, is saved as
`results/phase4b/cell2location_mapping/pi/input_preflight.json`.

## Implementation and choices

`scripts/21_map_cell2location.py` runs one independent sample. PI completed a
20-epoch/20-posterior-sample smoke test in isolated `smoke/pi/` paths. The
formal run uses the existing separate GPU environment, seed 20260928, full
sample batches, 30,000 epochs, learning rate 0.002 and 1,000 posterior samples.
The official cell2location tutorial uses full batches and 30,000 epochs:
https://cell2location.readthedocs.io/en/latest/notebooks/cell2location_tutorial.html

`detection_alpha=20` follows its relaxed detection-sensitivity guidance.
`N_cells_per_location=30` is a USER/CODEX ANALYTICAL CHOICE borrowed as an
initial prior from that tutorial, not a gingiva-specific nuclei count or a
paper-reported parameter. Absolute counts per spot therefore remain
uncalibrated; this limitation persists even if the internal mapping QC passes.

Earlier import attempts were interrupted after repeated slow package imports
before any training. A fresh import test passed after project write access was
granted. The exact source of the earlier slowdown is unproven; no packages,
credentials or environment versions were changed. Direct-module/stub import
experiments were diagnostic only; the formal script imports the normal package.

## QC contract

`scripts/22_qc_cell2location_mapping.py` exports means, 5%/95% quantiles,
per-type abundance distributions, credible widths, rare-spot concentration,
gene-level and module-level marker concordance, depth associations and
exploratory co-localization matrices. Quantile/mean tissue maps retain the
original orientation and are overlaid on unchanged histology with alpha 0.35.
Displayed axes crop to the full tissue-spot bounding box with 5% margin;
every input tissue spot remains visible and the underlying image is unmodified.
Individual cell-type maps use their own scales; they cannot be compared by
color across types. No statistical disease comparison is performed.

Marker concordance is an internal diagnostic using the same expression data
that entered the model. It is not independent validation. Module scores are
means of log1p(counts per 10,000 shared-gene library) over available canonical
markers. Raw-marker correlations are also recorded to expose shared depth
effects. Posterior intervals describe fitted-model uncertainty, not biological
replicate uncertainty.

Predeclared diagnostic heuristics: loss finite and decreasing, absolute relative
tail slope <2e-5 per epoch, finite nonnegative posterior, ordered quantiles,
median total abundance <500 and maximum <1,000; no well-detected lineage with
both abundance/module and fraction/module Spearman rho below -0.25. Depth
dominance is flagged if total abundance correlates above 0.85 in absolute value
with both original counts and detected genes. These are analytical QC choices,
not published validation thresholds. A failed gate stops Healthy mapping for
diagnosis. Passing gates still requires spatial-image review.

Reliability categories are conservative diagnostics: reliable requires
normalized marker rho >=0.30, composition/module rho >=0.20, median relative
90% credible width <2 and marker detection in >=10% spots. Partially reliable
requires marker rho >=0.10, composition/module rho >=-0.10 and detection in
>=5% spots. Other cases are questionable; rarity alone does not prove absence.
Overlapping macrophage/monocyte markers limit separation of broad myeloid
states and must be reported separately from numerical fit success.

## Formal result and stop decision

The full 640-spot fit completed 30,000 epochs in 2,256 seconds on the existing
RTX 4070 GPU environment. Initial/final loss: 27,544,052 / 7,712,862.5;
last-1,000-epoch relative slope: -9.00e-10. All loss values are finite.
The 1,000-sample posterior completed all five local batches and global sampling.
Means/stds/q05/q95 are finite, nonnegative and correctly ordered/aligned.
Total inferred abundance median/max: 30.52 / 233.39. No predefined severe
negative lineage-marker mismatch was detected. These numerical checks passed.

**The overall PI QC did not pass.** Total abundance has Spearman rho 0.9814
with original counts and 0.9577 with detected genes, exceeding the predeclared
0.85/0.85 depth gate. Healthy fitting was therefore stopped before its first
sample. The threshold was not relaxed after seeing the result.

This association does NOT prove a purely technical artifact: true tissue cell
density, RNA content, capture efficiency and library depth are confounded.
Posterior detection sensitivity varies (mean 0.2734, CV 0.325; p05/p95
0.1662/0.3910), but correlates only 0.6425 with counts, while total abundance
correlates 0.9814. The fitted model places much depth variation into abundance.
Without independent nuclei counts or prior/detection sensitivity comparisons,
that allocation cannot be accepted as calibrated cells per spot.

`scripts/23_diagnose_pi_mapping_depth.py` adds descriptive rank-residual marker
correlations controlling original counts and detected genes. This is a diagnostic,
not a causal adjustment, a replacement model, or independent validation.
Macrophage marker rho drops from 0.4822 to 0.2186 (fraction residual rho 0.2486).
Macrophage/monocyte abundance rho is 0.9187; their log1p reference-signature
correlation is 0.9174. Shared myeloid markers support a broad myeloid component,
but cannot uniquely establish macrophage versus monocyte attribution.

Plasma is the largest inferred component (median 18.36, maximum 190.44);
its abundance/counts rho is 0.9647, fraction/module rho only 0.1040 and
depth-adjusted fraction/module rho -0.0740. High fitted precision is not proof
of correct absolute density. Neutrophil marker rho is only 0.1093 and median
relative 90% credible width 2.43: localization remains weakly supported.
The validated Leiden 47 correction was not changed.

Manual review covered the all-14 tissue overview, macrophage, plasma,
neutrophil and abundance/depth plots. Full sample coordinates are displayed,
and histology orientation is retained. Concentrated epithelial signal is
recorded rather than removed (top 1% spots carry 25.5% epithelial abundance).
Macrophage top 1% share is 4.7%; no single extreme macrophage spot explains
the depth gate. All 14 distributions and concentration metrics are retained.

## Outputs and next diagnostic boundary

- Model: `models/phase4b/cell2location_mapping/pi/model.pt`.
- Posterior, abundance statistics, training history, input hashes, full package
  inventory, per-type/marker/spot QC, correlation matrices and depth diagnostics:
  `results/phase4b/cell2location_mapping/pi/`.
- PNG/PDF/SVG tissue maps, distributions, correlation and depth diagnostics:
  `figures/phase4b/cell2location/pi/` (training loss from the formal process
  initially exported PNG/PDF; SVG added from the same saved history).
- Isolated smoke outputs remain under `smoke/pi/`; they are not formal results.

No cell type is released into NMF or downstream interpretation while the global
PI gate is blocked. The next required diagnostic is nuclei-density calibration
where feasible and a separately preserved PI-only prior/detection sensitivity
comparison. Do not normalize the raw input to force the gate green, relabel
cells without evidence, or interpret the strong correlation as a disease effect.
No new reference annotation problem has been demonstrated by this mapping.
Healthy domain shift remains NOT ASSESSED because Healthy was not fitted.

Verification: three scripts compile; formal posterior was reopened and checked;
19 PNG/PDF/SVG figure sets exist, all 19 PDF text audits pass a 5-pt floor.
Spatial overview, key lineage maps, convergence and depth figures were visually
reviewed. Source validator recognizes scripts 21/22 exports; its missing-export
flags for script 23 are false positives from dynamic filename suffixes, checked
against the actual three exports. The 300-dpi previews and wide diagnostic
layouts are intentional; these are QC artifacts, not final journal figures.
