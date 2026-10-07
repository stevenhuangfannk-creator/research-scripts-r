# Figure QA record

Date: 2026-10-07. Backend: **R only** (ggplot2/patchwork/grid/igraph; ragg PNG,
Cairo PDF, svglite schematic SVG). Python serialized evidence and inspected PDF text;
it did not draw or edit figures.

## Scope and result

All 34 generated previews were inspected in rendered contact sheets; corrected survival,
synthetic-caption and schematic examples were inspected again individually. No unresolved
cropped panels, overlapping labels, obscured legends or glyph corruption were found at the
declared export sizes. This is demo/template QA, not journal acceptance or validation of
unexecuted biological workflows. Every preview links to code, parameters and a vector output
in the [Gallery](../GALLERY.md). Registry structure and per-preview metadata also passed.

Exports use Arial, a 9 pt baseline, 400 dpi PNG and selectable vector text. The effective-text
audit passed for all 34 PDFs with a minimum observed size of 6 pt at their exported dimensions:
[PDF evidence](validation/pdf_effective_text.json), [audit code](../scripts/audit_pdf_text.py).
Do not shrink a final manuscript figure without checking effective text sizes again.

## Corrections made during QA

- The Windows R process uses a C locale. Literal Unicode arrows/dashes rendered incorrectly
  in early captions; final rendered text uses ASCII-compatible labels. UTF-8 registries use
  an explicit UTF-8 reader, protected by a regression test.
- The KM risk table and survival panel now use identical day limits and tick positions.
- Schematic SVG export uses svglite so text remains editable rather than outlined glyphs.
- Matrix/QC arithmetic, one-group pseudobulk, missing/constant correlation inputs and
  invalid annotation mappings have regression checks in the execution suite.

## Reviewed static warnings and tool limits

The Nature-figure source preflight recorded **14 PASS / 6 WARN / 0 FAIL** in
[source audit](validation/figure_source_audit.txt). Its basic delimiter warning is resolved
by the real R parser (46 new sources). Lowercase `group=1`/`group=2` are internal KM keys;
display labels are Sex 1/Sex 2. PNG is the requested preview format and 400 dpi exceeds
the 300 dpi floor; submission TIFF/600 dpi can be exported after a journal is selected.
160 mm is a documented library example width, not a journal column-width guarantee.
The simulation warning is intentional: eight style fixtures are labeled SYNTHETIC and
cannot be used as experimental evidence.

The skill's raw PDF token audit reported 1 pt `Tf` operands in Cairo files. Cairo applies
a text transformation matrix, so raw `Tf` alone is not the displayed font size. A separate
PyMuPDF audit reads effective transformed text spans and found no spans below 6 pt. This
tool limitation was checked rather than treating the raw-token warning as a real 1 pt label.

Cell-marker execution emitted 187 tied-value Wilcoxon warnings: exact p-values are
unavailable with ties, and R uses its asymptotic test. The output is an exploratory cluster
marker table, not replicated condition-level DEG evidence. QC's dense-to-sparse coercion
and UMAP's UWOT default notice are recorded in [method evidence](validation/method_results.json).
Package build-version and Windows locale startup warnings remain in the execution log.

## Per-preview review

| Plot ID | Render review | Interpretation / integrity checks |
|---|---|---|
| [`umap_clean_v1`](../08_visualization/UMAP/gallery/umap_clean_v1.png) | PASS at declared size | All 80 cells; numerical cluster labels, no cell-identity claim; consistent cluster colors. |
| [`feature_clean_v1`](../08_visualization/FeaturePlot/gallery/feature_clean_v1.png) | PASS at declared size | All 80 LYZ values retained; continuous viridis scale; no threshold-based cell exclusion. |
| [`dotplot_clean_v1`](../08_visualization/DotPlot/gallery/dotplot_clean_v1.png) | PASS at declared size | Size = percentage above zero; color = mean log expression; no DEG significance implied. |
| [`marker_heatmap_v1`](../08_visualization/Heatmap/gallery/marker_heatmap_v1.png) | PASS at declared size | Selected marker means; no row z-score or differential-effect claim. |
| [`cluster_heatmap_v1`](../08_visualization/Heatmap/gallery/cluster_heatmap_v1.png) | PASS at declared size | First ten variable features selected for display; every cell contributes to cluster means. |
| [`violin_clean_v1`](../08_visualization/Violin/gallery/violin_clean_v1.png) | PASS at declared size | All 80 observations and expression zeros retained; violin/box summaries visible. |
| [`stacked_violin_v1`](../08_visualization/Violin/gallery/stacked_violin_v1.png) | PASS at declared size | Faceted selected genes; free expression axes declared; all cells retained. |
| [`composition_sample_v1`](../08_visualization/Composition/gallery/composition_sample_v1.png) | PASS at declared size | Single captured sample; fractions sum to one; no donor/condition inference. |
| [`cluster_count_bar_v1`](../08_visualization/Barplot/gallery/cluster_count_bar_v1.png) | PASS at declared size | Computed cluster counts; numerical clusters use the same PBMC colors. |
| [`multipanel_pbmc_v1`](../08_visualization/MultiPanel/gallery/multipanel_pbmc_v1.png) | PASS at declared size | A/B/C/D layout checked for complete panels, aligned axes and consistent cluster colors. |
| [`boxplot_iris_v1`](../08_visualization/Boxplot/gallery/boxplot_iris_v1.png) | PASS at declared size | All 150 flowers contribute to species-wise box summaries; no inferential comparison. |
| [`violin_iris_v1`](../08_visualization/Violin/gallery/violin_iris_v1.png) | PASS at declared size | All observed values; same species palette as box/density/ridge examples. |
| [`density_iris_v1`](../08_visualization/Density/gallery/density_iris_v1.png) | PASS at declared size | Species-specific kernel densities; smoothing is a descriptive estimate. |
| [`ridge_iris_v1`](../08_visualization/Ridge/gallery/ridge_iris_v1.png) | PASS at declared size | Density-height scale 0.6 declared; species axis and complete ribbons visible. |
| [`scatter_fit_v1`](../08_visualization/Scatter_Correlation/gallery/scatter_fit_v1.png) | PASS at declared size | All 150 points; pooled Pearson/lm relationship is confounded by species; lm 95% CI. |
| [`density_scatter_v1`](../08_visualization/Scatter_Correlation/gallery/density_scatter_v1.png) | PASS at declared size | All 150 observations binned; no downsampling; count legend visible. |
| [`correlation_bh_heatmap_v1`](../08_visualization/Scatter_Correlation/gallery/correlation_bh_heatmap_v1.png) | PASS at declared size | Six unique tests define the BH family; mirrored cells do not double the test count; diagonal omitted. |
| [`pairplot_iris_v1`](../08_visualization/Scatter_Correlation/gallery/pairplot_iris_v1.png) | PASS at declared size | Two specified pairs with A/B labels; every observation retained in both panels. |
| [`survival_km_v1`](../08_visualization/SurvivalPlot/gallery/survival_km_v1.png) | PASS at declared size | 228 records; explicit status==2 event mapping; step CI and risk counts share the same time axis. |
| [`forest_cox_v1`](../08_visualization/ForestPlot/gallery/forest_cox_v1.png) | PASS at declared size | Age+sex model; 95% HR CI on a log x-axis and null=1 line; no prognostic certification. |
| [`roc_holdout_v1`](../08_visualization/ROC/gallery/roc_holdout_v1.png) | PASS at declared size | Stratified seed-42 split: 105 train / 45 test; held-out versicolor-versus-rest scores; no clinical generalization. |
| [`volcano_clean_v1`](../08_visualization/Volcano/gallery/volcano_clean_v1.png) | PASS at declared size | Synthetic fixture prominently labeled; thresholds and direction colors visible; no real DEG claim. |
| [`enrichment_dot_style_v1`](../08_visualization/Enrichment/gallery/enrichment_dot_style_v1.png) | PASS at declared size | Synthetic pathway labels/scores; demonstrates size/color encoding, not computed enrichment. |
| [`lollipop_style_v1`](../08_visualization/Lollipop/gallery/lollipop_style_v1.png) | PASS at declared size | Synthetic ordered values; baseline/stems/points legible. |
| [`waterfall_style_v1`](../08_visualization/Waterfall/gallery/waterfall_style_v1.png) | PASS at declared size | Synthetic changes; zero reference and signed direction colors visible. |
| [`alluvial_style_v1`](../08_visualization/Sankey_Alluvial/gallery/alluvial_style_v1.png) | PASS at declared size | Synthetic aggregate flows; labels and edges complete; no cell lineage interpretation. |
| [`network_style_v1`](../08_visualization/Network/gallery/network_style_v1.png) | PASS at declared size | Synthetic directed graph; arrowheads and labels legible; not a CellChat or PPI result. |
| [`nes_heatmap_style_v1`](../08_visualization/Enrichment/gallery/nes_heatmap_style_v1.png) | PASS at declared size | Synthetic signed scores; diverging scale centered at zero; not an fgsea result. |
| [`palette_swatches_v1`](../08_visualization/palettes/gallery/palette_swatches_v1.png) | PASS at declared size | Nine palette IDs and swatches checked; journal-inspired palettes are not certified CVD-safe. |
| [`chord_style_v1`](../08_visualization/Circle_Chord/gallery/chord_style_v1.png) | PASS at declared size | Synthetic directed matrix; native R/grid example; not a native CellChat chord output. |
| [`schematic_workflow_v1`](../10_scientific_schematics/workflow_diagrams/gallery/schematic_workflow_v1.png) | PASS at declared size | Original workflow scaffold; arrows, labels and complete panel inspected. |
| [`schematic_cell_interaction_v1`](../10_scientific_schematics/cell_interaction/gallery/schematic_cell_interaction_v1.png) | PASS at declared size | Original macrophage/fibroblast hypothesis scaffold; no specific LR mechanism asserted. |
| [`schematic_mechanism_v1`](../10_scientific_schematics/mechanism_diagrams/gallery/schematic_mechanism_v1.png) | PASS at declared size | Original generic mechanism scaffold; arrows represent template relationships only. |
| [`schematic_components_v1`](../10_scientific_schematics/reusable_components/gallery/schematic_components_v1.png) | PASS at declared size | Eleven original vector primitives; complete component labels; no downloaded journal/BioRender icons. |

## Excluded claims and remaining visual gaps

Native CellChat/Monocle3 figures were not generated. Their 43 planned plot records have
null output paths, null generation dates and no current-default preference. The synthetic
network/chord/alluvial figures do not stand in for those native outputs. Actual GSEA curves,
pathway activity UMAP/violin and ComplexHeatmap annotation examples also remain to be
validated; no corresponding preview is claimed. Journal-inspired categorical colors require
task-specific accessibility review. Schematic templates provide original editable shapes,
not experimental mechanism evidence.
