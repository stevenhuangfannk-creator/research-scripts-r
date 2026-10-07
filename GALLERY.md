# Visualization Gallery

Look at the preview → choose a Plot ID → resolve the registered code and parameters.

**34 actual R-rendered PNG/PDF examples.** Built-in real examples and explicitly synthetic styles are labeled below. Template validation certifies rendering on its demo, not biological findings. Native CellChat/Monocle3 previews remain blocked.

## UMAP / annotation / single-cell

| Plot ID / purpose | Preview | Method / code / parameters / vector | Status and data |
|---|---|---|---|
| `umap_clean_v1`<br>Where are computed clusters in UMAP? | [![umap_clean_v1](08_visualization/UMAP/gallery/umap_clean_v1.png)](08_visualization/UMAP/gallery/umap_clean_v1.png) | [method](01_scrna_core/clustering/METHOD_CARD.md) · [code](08_visualization/UMAP/umap_clean_v1.R) · [parameters](08_visualization/UMAP/gallery/umap_clean_v1.metadata.json) · [PDF](08_visualization/UMAP/gallery/umap_clean_v1.pdf) | Rendering PASS; SeuratObject::pbmc_small; all 80 cells; CURRENT_DEFAULT |
| `feature_clean_v1`<br>Where is LYZ expressed? | [![feature_clean_v1](08_visualization/FeaturePlot/gallery/feature_clean_v1.png)](08_visualization/FeaturePlot/gallery/feature_clean_v1.png) | [method](01_scrna_core/normalization/lognormalize/METHOD_CARD.md) · [code](08_visualization/FeaturePlot/feature_clean_v1.R) · [parameters](08_visualization/FeaturePlot/gallery/feature_clean_v1.metadata.json) · [PDF](08_visualization/FeaturePlot/gallery/feature_clean_v1.pdf) | Rendering PASS; pbmc_small; all 80 cells; CURRENT_DEFAULT |
| `dotplot_clean_v1`<br>Which selected markers distinguish clusters? | [![dotplot_clean_v1](08_visualization/DotPlot/gallery/dotplot_clean_v1.png)](08_visualization/DotPlot/gallery/dotplot_clean_v1.png) | [method](02_differential_analysis/differential_expression/METHOD_CARD.md) · [code](08_visualization/DotPlot/dotplot_clean_v1.R) · [parameters](08_visualization/DotPlot/gallery/dotplot_clean_v1.metadata.json) · [PDF](08_visualization/DotPlot/gallery/dotplot_clean_v1.pdf) | Rendering PASS; pbmc_small; CURRENT_DEFAULT |
| `marker_heatmap_v1`<br>How do selected marker means vary by cluster? | [![marker_heatmap_v1](08_visualization/Heatmap/gallery/marker_heatmap_v1.png)](08_visualization/Heatmap/gallery/marker_heatmap_v1.png) | [method](02_differential_analysis/differential_expression/METHOD_CARD.md) · [code](08_visualization/Heatmap/heatmap_clean_v1.R) · [parameters](08_visualization/Heatmap/gallery/marker_heatmap_v1.metadata.json) · [PDF](08_visualization/Heatmap/gallery/marker_heatmap_v1.pdf) | Rendering PASS; pbmc_small; CURRENT_DEFAULT |
| `cluster_heatmap_v1`<br>What expression patterns occur across clusters? | [![cluster_heatmap_v1](08_visualization/Heatmap/gallery/cluster_heatmap_v1.png)](08_visualization/Heatmap/gallery/cluster_heatmap_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Heatmap/gallery/cluster_heatmap_v1.metadata.json) · [PDF](08_visualization/Heatmap/gallery/cluster_heatmap_v1.pdf) | Rendering PASS; pbmc_small; demo asset |
| `violin_clean_v1`<br>What is the per-cell LYZ distribution? | [![violin_clean_v1](08_visualization/Violin/gallery/violin_clean_v1.png)](08_visualization/Violin/gallery/violin_clean_v1.png) | [method](01_scrna_core/normalization/lognormalize/METHOD_CARD.md) · [code](08_visualization/Violin/violin_clean_v1.R) · [parameters](08_visualization/Violin/gallery/violin_clean_v1.metadata.json) · [PDF](08_visualization/Violin/gallery/violin_clean_v1.pdf) | Rendering PASS; pbmc_small; all 80 cells including zeros; CURRENT_DEFAULT |
| `stacked_violin_v1`<br>How do several marker distributions vary? | [![stacked_violin_v1](08_visualization/Violin/gallery/stacked_violin_v1.png)](08_visualization/Violin/gallery/stacked_violin_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Violin/gallery/stacked_violin_v1.metadata.json) · [PDF](08_visualization/Violin/gallery/stacked_violin_v1.pdf) | Rendering PASS; pbmc_small; demo asset |
| `composition_sample_v1`<br>What fraction of this capture belongs to each cluster? | [![composition_sample_v1](08_visualization/Composition/gallery/composition_sample_v1.png)](08_visualization/Composition/gallery/composition_sample_v1.png) | [visual library](08_visualization/README.md) · [code](08_visualization/Composition/composition_sample_v1.R) · [parameters](08_visualization/Composition/gallery/composition_sample_v1.metadata.json) · [PDF](08_visualization/Composition/gallery/composition_sample_v1.pdf) | Rendering PASS; pbmc_small: one captured sample; CURRENT_DEFAULT |
| `cluster_count_bar_v1`<br>How many cells were assigned to each cluster? | [![cluster_count_bar_v1](08_visualization/Barplot/gallery/cluster_count_bar_v1.png)](08_visualization/Barplot/gallery/cluster_count_bar_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Barplot/gallery/cluster_count_bar_v1.metadata.json) · [PDF](08_visualization/Barplot/gallery/cluster_count_bar_v1.pdf) | Rendering PASS; pbmc_small; demo asset |
| `multipanel_pbmc_v1`<br>PBMC demo overview | [![multipanel_pbmc_v1](08_visualization/MultiPanel/gallery/multipanel_pbmc_v1.png)](08_visualization/MultiPanel/gallery/multipanel_pbmc_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/MultiPanel/gallery/multipanel_pbmc_v1.metadata.json) · [PDF](08_visualization/MultiPanel/gallery/multipanel_pbmc_v1.pdf) | Rendering PASS; pbmc_small; demo asset |

## Enrichment styles

| Plot ID / purpose | Preview | Method / code / parameters / vector | Status and data |
|---|---|---|---|
| `enrichment_dot_style_v1`<br>Enrichment dot style | [![enrichment_dot_style_v1](08_visualization/Enrichment/gallery/enrichment_dot_style_v1.png)](08_visualization/Enrichment/gallery/enrichment_dot_style_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Enrichment/gallery/enrichment_dot_style_v1.metadata.json) · [PDF](08_visualization/Enrichment/gallery/enrichment_dot_style_v1.pdf) | Rendering PASS; **SYNTHETIC**; demo asset |
| `nes_heatmap_style_v1`<br>Signed pathway-effect heatmap style | [![nes_heatmap_style_v1](08_visualization/Enrichment/gallery/nes_heatmap_style_v1.png)](08_visualization/Enrichment/gallery/nes_heatmap_style_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Enrichment/gallery/nes_heatmap_style_v1.metadata.json) · [PDF](08_visualization/Enrichment/gallery/nes_heatmap_style_v1.pdf) | Rendering PASS; **SYNTHETIC**; demo asset |

## Network styles

| Plot ID / purpose | Preview | Method / code / parameters / vector | Status and data |
|---|---|---|---|
| `alluvial_style_v1`<br>Alluvial style | [![alluvial_style_v1](08_visualization/Sankey_Alluvial/gallery/alluvial_style_v1.png)](08_visualization/Sankey_Alluvial/gallery/alluvial_style_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Sankey_Alluvial/gallery/alluvial_style_v1.metadata.json) · [PDF](08_visualization/Sankey_Alluvial/gallery/alluvial_style_v1.pdf) | Rendering PASS; **SYNTHETIC**; demo asset |
| `network_style_v1`<br>Network style | [![network_style_v1](08_visualization/Network/gallery/network_style_v1.png)](08_visualization/Network/gallery/network_style_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Network/gallery/network_style_v1.metadata.json) · [PDF](08_visualization/Network/gallery/network_style_v1.pdf) | Rendering PASS; **SYNTHETIC**; demo asset |
| `chord_style_v1`<br>chord_style_v1 | [![chord_style_v1](08_visualization/Circle_Chord/gallery/chord_style_v1.png)](08_visualization/Circle_Chord/gallery/chord_style_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Circle_Chord/gallery/chord_style_v1.metadata.json) · [PDF](08_visualization/Circle_Chord/gallery/chord_style_v1.pdf) | Rendering PASS; **SYNTHETIC**; demo asset |

## Survival

| Plot ID / purpose | Preview | Method / code / parameters / vector | Status and data |
|---|---|---|---|
| `survival_km_v1`<br>KM survival with uncertainty and risk counts | [![survival_km_v1](08_visualization/SurvivalPlot/gallery/survival_km_v1.png)](08_visualization/SurvivalPlot/gallery/survival_km_v1.png) | [method](07_bulk_clinical_ml/survival/METHOD_CARD.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/SurvivalPlot/gallery/survival_km_v1.metadata.json) · [PDF](08_visualization/SurvivalPlot/gallery/survival_km_v1.pdf) | Rendering PASS; survival::lung; 228 records; demo asset |
| `forest_cox_v1`<br>Hazard ratios with 95% confidence intervals | [![forest_cox_v1](08_visualization/ForestPlot/gallery/forest_cox_v1.png)](08_visualization/ForestPlot/gallery/forest_cox_v1.png) | [method](07_bulk_clinical_ml/Cox/METHOD_CARD.md) · [code](08_visualization/ForestPlot/forest_cox_v1.R) · [parameters](08_visualization/ForestPlot/gallery/forest_cox_v1.metadata.json) · [PDF](08_visualization/ForestPlot/gallery/forest_cox_v1.pdf) | Rendering PASS; survival::lung; CURRENT_DEFAULT |

## ML

| Plot ID / purpose | Preview | Method / code / parameters / vector | Status and data |
|---|---|---|---|
| `roc_holdout_v1`<br>Show held-out discrimination | [![roc_holdout_v1](08_visualization/ROC/gallery/roc_holdout_v1.png)](08_visualization/ROC/gallery/roc_holdout_v1.png) | [method](07_bulk_clinical_ml/random_forest/METHOD_CARD.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/ROC/gallery/roc_holdout_v1.metadata.json) · [PDF](08_visualization/ROC/gallery/roc_holdout_v1.pdf) | Rendering PASS; datasets::iris; stratified 105 train / 45 test; demo asset |

## General plots

| Plot ID / purpose | Preview | Method / code / parameters / vector | Status and data |
|---|---|---|---|
| `boxplot_iris_v1`<br>What is the observed distribution across species? | [![boxplot_iris_v1](08_visualization/Boxplot/gallery/boxplot_iris_v1.png)](08_visualization/Boxplot/gallery/boxplot_iris_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Boxplot/gallery/boxplot_iris_v1.metadata.json) · [PDF](08_visualization/Boxplot/gallery/boxplot_iris_v1.pdf) | Rendering PASS; datasets::iris; all 150 flowers; demo asset |
| `violin_iris_v1`<br>Compare observed flower measurements | [![violin_iris_v1](08_visualization/Violin/gallery/violin_iris_v1.png)](08_visualization/Violin/gallery/violin_iris_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Violin/gallery/violin_iris_v1.metadata.json) · [PDF](08_visualization/Violin/gallery/violin_iris_v1.pdf) | Rendering PASS; datasets::iris; demo asset |
| `density_iris_v1`<br>How do measurement densities differ? | [![density_iris_v1](08_visualization/Density/gallery/density_iris_v1.png)](08_visualization/Density/gallery/density_iris_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Density/gallery/density_iris_v1.metadata.json) · [PDF](08_visualization/Density/gallery/density_iris_v1.pdf) | Rendering PASS; datasets::iris; demo asset |
| `ridge_iris_v1`<br>Compare distribution shapes by species | [![ridge_iris_v1](08_visualization/Ridge/gallery/ridge_iris_v1.png)](08_visualization/Ridge/gallery/ridge_iris_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Ridge/gallery/ridge_iris_v1.metadata.json) · [PDF](08_visualization/Ridge/gallery/ridge_iris_v1.pdf) | Rendering PASS; datasets::iris; demo asset |
| `scatter_fit_v1`<br>Show linear association and uncertainty | [![scatter_fit_v1](08_visualization/Scatter_Correlation/gallery/scatter_fit_v1.png)](08_visualization/Scatter_Correlation/gallery/scatter_fit_v1.png) | [method](07_bulk_clinical_ml/correlation/METHOD_CARD.md) · [code](08_visualization/Scatter_Correlation/scatter_fit_v1.R) · [parameters](08_visualization/Scatter_Correlation/gallery/scatter_fit_v1.metadata.json) · [PDF](08_visualization/Scatter_Correlation/gallery/scatter_fit_v1.pdf) | Rendering PASS; datasets::iris (pooled species; potential confounding); CURRENT_DEFAULT |
| `density_scatter_v1`<br>Where are observations concentrated? | [![density_scatter_v1](08_visualization/Scatter_Correlation/gallery/density_scatter_v1.png)](08_visualization/Scatter_Correlation/gallery/density_scatter_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Scatter_Correlation/gallery/density_scatter_v1.metadata.json) · [PDF](08_visualization/Scatter_Correlation/gallery/density_scatter_v1.pdf) | Rendering PASS; datasets::iris; demo asset |
| `correlation_bh_heatmap_v1`<br>Which associations pass the stated multiple-testing rule? | [![correlation_bh_heatmap_v1](08_visualization/Scatter_Correlation/gallery/correlation_bh_heatmap_v1.png)](08_visualization/Scatter_Correlation/gallery/correlation_bh_heatmap_v1.png) | [method](07_bulk_clinical_ml/correlation/METHOD_CARD.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Scatter_Correlation/gallery/correlation_bh_heatmap_v1.metadata.json) · [PDF](08_visualization/Scatter_Correlation/gallery/correlation_bh_heatmap_v1.pdf) | Rendering PASS; datasets::iris; demo asset |
| `pairplot_iris_v1`<br>Compare two association views | [![pairplot_iris_v1](08_visualization/Scatter_Correlation/gallery/pairplot_iris_v1.png)](08_visualization/Scatter_Correlation/gallery/pairplot_iris_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Scatter_Correlation/gallery/pairplot_iris_v1.metadata.json) · [PDF](08_visualization/Scatter_Correlation/gallery/pairplot_iris_v1.pdf) | Rendering PASS; datasets::iris; demo asset |
| `volcano_clean_v1`<br>Volcano style template | [![volcano_clean_v1](08_visualization/Volcano/gallery/volcano_clean_v1.png)](08_visualization/Volcano/gallery/volcano_clean_v1.png) | [visual library](08_visualization/README.md) · [code](08_visualization/Volcano/volcano_clean_v1.R) · [parameters](08_visualization/Volcano/gallery/volcano_clean_v1.metadata.json) · [PDF](08_visualization/Volcano/gallery/volcano_clean_v1.pdf) | Rendering PASS; **SYNTHETIC**; demo asset |
| `lollipop_style_v1`<br>Ranking lollipop style | [![lollipop_style_v1](08_visualization/Lollipop/gallery/lollipop_style_v1.png)](08_visualization/Lollipop/gallery/lollipop_style_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Lollipop/gallery/lollipop_style_v1.metadata.json) · [PDF](08_visualization/Lollipop/gallery/lollipop_style_v1.pdf) | Rendering PASS; **SYNTHETIC**; demo asset |
| `waterfall_style_v1`<br>Waterfall style | [![waterfall_style_v1](08_visualization/Waterfall/gallery/waterfall_style_v1.png)](08_visualization/Waterfall/gallery/waterfall_style_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/Waterfall/gallery/waterfall_style_v1.metadata.json) · [PDF](08_visualization/Waterfall/gallery/waterfall_style_v1.pdf) | Rendering PASS; **SYNTHETIC**; demo asset |

## Schematics

| Plot ID / purpose | Preview | Method / code / parameters / vector | Status and data |
|---|---|---|---|
| `schematic_workflow_v1`<br>schematic_workflow_v1 | [![schematic_workflow_v1](10_scientific_schematics/workflow_diagrams/gallery/schematic_workflow_v1.png)](10_scientific_schematics/workflow_diagrams/gallery/schematic_workflow_v1.png) | [schematics](10_scientific_schematics/README.md) · [code](10_scientific_schematics/workflow_diagrams/workflow_v1.R) · [parameters](10_scientific_schematics/workflow_diagrams/gallery/schematic_workflow_v1.metadata.json) · [PDF](10_scientific_schematics/workflow_diagrams/gallery/schematic_workflow_v1.pdf) | Rendering PASS; **SYNTHETIC**; demo asset |
| `schematic_cell_interaction_v1`<br>schematic_cell_interaction_v1 | [![schematic_cell_interaction_v1](10_scientific_schematics/cell_interaction/gallery/schematic_cell_interaction_v1.png)](10_scientific_schematics/cell_interaction/gallery/schematic_cell_interaction_v1.png) | [schematics](10_scientific_schematics/README.md) · [code](10_scientific_schematics/cell_interaction/cell_interaction_v1.R) · [parameters](10_scientific_schematics/cell_interaction/gallery/schematic_cell_interaction_v1.metadata.json) · [PDF](10_scientific_schematics/cell_interaction/gallery/schematic_cell_interaction_v1.pdf) | Rendering PASS; **SYNTHETIC**; demo asset |
| `schematic_mechanism_v1`<br>schematic_mechanism_v1 | [![schematic_mechanism_v1](10_scientific_schematics/mechanism_diagrams/gallery/schematic_mechanism_v1.png)](10_scientific_schematics/mechanism_diagrams/gallery/schematic_mechanism_v1.png) | [schematics](10_scientific_schematics/README.md) · [code](10_scientific_schematics/mechanism_diagrams/mechanism_v1.R) · [parameters](10_scientific_schematics/mechanism_diagrams/gallery/schematic_mechanism_v1.metadata.json) · [PDF](10_scientific_schematics/mechanism_diagrams/gallery/schematic_mechanism_v1.pdf) | Rendering PASS; **SYNTHETIC**; demo asset |
| `schematic_components_v1`<br>schematic_components_v1 | [![schematic_components_v1](10_scientific_schematics/reusable_components/gallery/schematic_components_v1.png)](10_scientific_schematics/reusable_components/gallery/schematic_components_v1.png) | [schematics](10_scientific_schematics/README.md) · [code](10_scientific_schematics/reusable_components/components.R) · [parameters](10_scientific_schematics/reusable_components/gallery/schematic_components_v1.metadata.json) · [PDF](10_scientific_schematics/reusable_components/gallery/schematic_components_v1.pdf) | Rendering PASS; **SYNTHETIC**; demo asset |

## Palettes

| Plot ID / purpose | Preview | Method / code / parameters / vector | Status and data |
|---|---|---|---|
| `palette_swatches_v1`<br>Palette reference swatches | [![palette_swatches_v1](08_visualization/palettes/gallery/palette_swatches_v1.png)](08_visualization/palettes/gallery/palette_swatches_v1.png) | [visual library](08_visualization/README.md) · [code](scripts/generate_gallery.R) · [parameters](08_visualization/palettes/gallery/palette_swatches_v1.metadata.json) · [PDF](08_visualization/palettes/gallery/palette_swatches_v1.pdf) | Rendering PASS; Installed ggsci/viridisLite and documented color specifications; demo asset |

## CellChat

Native inference/gallery is **BLOCKED**, with no generated-preview claim. The
[35-output catalog](04_cell_communication/CellChat/OUTPUT_CATALOG.md) links actual code for
overall/pathway/LR networks, roles, patterns and comparisons. Planned registry items have null
output paths and cannot be CURRENT_DEFAULT.

## Trajectory / Monocle3

Native inference/gallery is **BLOCKED**. The [catalog](03_cell_dynamics/monocle3/OUTPUT_CATALOG.md)
documents CDS/graph/pseudotime, expression/modules and optional 3D. A synthetic network or curve
elsewhere in this gallery is not a Monocle3 result.

## Reproduce and reuse

```sh
Rscript scripts/smoke_tests.R
Rscript scripts/build_palettes.R
Rscript scripts/generate_gallery.R
Rscript scripts/generate_gallery.R umap_clean_v1
Rscript scripts/resolve_asset.R plot umap_clean_v1
```

Run from repository root in a compatible environment. A single Plot ID reproduces its *demo*;
use the registered helper's declared input contract for your own data. Export metadata lives beside
each PNG; registry/plots.yml remains the canonical index. Inspect all new figures before adding
them as recommendations. No raw inputs, RDS objects or large datasets are committed.
