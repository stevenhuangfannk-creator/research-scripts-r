# Rscript scripts/generate_gallery.R [plot_id] -- renders explicit demo data only.
suppressPackageStartupMessages({library(ggplot2); library(patchwork); library(Seurat)})
source("08_visualization/themes/theme_research.R")
source("08_visualization/palettes/palettes.R")
for (script in c("UMAP/umap_clean_v1.R", "FeaturePlot/feature_clean_v1.R", "DotPlot/dotplot_clean_v1.R",
                 "Heatmap/heatmap_clean_v1.R", "Violin/violin_clean_v1.R", "Volcano/volcano_clean_v1.R",
                 "Scatter_Correlation/scatter_fit_v1.R", "Composition/composition_sample_v1.R", "ForestPlot/forest_cox_v1.R")) {
  source(file.path("08_visualization", script))
}
args <- commandArgs(trailingOnly = TRUE)
only <- if (length(args)) args[[1]] else NULL
plots <- list()
theme_set(theme_research(base_size = 9, base_family = "Arial"))
emit <- function(id, family, p, dataset, input_object, purpose, method = "visualization", parameters = list(),
                 script = "scripts/generate_gallery.R", selection = NULL, synthetic = FALSE,
                 width_mm = 160, height_mm = 110, palette = "okabe_ito") {
  if (!is.null(only) && id != only) return(invisible(NULL))
  prefix <- file.path("08_visualization", family, "gallery", id)
  caption <- if (synthetic) "SYNTHETIC STYLE DEMO: no experimental or inferential result" else paste("Built-in public demo:", dataset)
  if (inherits(p, "patchwork")) p <- p + plot_annotation(title = purpose, caption = caption)
  else p <- p + labs(title = if (is.null(p$labels$title)) purpose else p$labels$title,
                      caption = paste(p$labels$caption, caption, sep = "\n"))
  save_research_plot(p, prefix, width_mm, height_mm, dpi = 400)
  plots[[length(plots) + 1L]] <<- list(id = id, method = method, purpose = purpose, script = script,
    example_script = "scripts/generate_gallery.R", dataset = dataset, input_object = input_object,
    major_parameters = c(parameters, list(width_mm = width_mm, height_mm = height_mm, dpi = 400)),
    palette = palette, theme = "theme_research", output_file = paste0(prefix, ".png"), vector_file = paste0(prefix, ".pdf"),
    status = "VALIDATED", selection = selection, synthetic = synthetic,
    validation = list(status = "PASS", scope = "Rendering on the declared demo only; no study-level analytical certification"),
    source_inspiration = "Original repository implementation using official R APIs", last_generated = "2026-10-07")
}
obj <- readRDS("results/smoke/pbmc_clustered.rds")
coord <- as.data.frame(Seurat::Embeddings(obj, "umap")); names(coord) <- c("x", "y")
coord$group <- factor(paste("Cluster", obj$seurat_clusters))
colors <- setNames(research_palette(n = nlevels(coord$group)), levels(coord$group))
umap <- plot_umap_clean(coord, colors, "PBMC demo clusters")
emit("umap_clean_v1", "UMAP", umap, "SeuratObject::pbmc_small; all 80 cells", "results/smoke/pbmc_clustered.rds",
     "Where are computed clusters in UMAP?", "seurat_clustering", list(seed = 42, npcs = 10, resolution = 0.8, n_neighbors = 15),
     "08_visualization/UMAP/umap_clean_v1.R", "CURRENT_DEFAULT")
rna <- SeuratObject::GetAssayData(obj, assay = "RNA", layer = "data")
genes <- intersect(c("LYZ", "CD3E", "MS4A1", "PPBP", "GNLY"), rownames(rna))
stopifnot(length(genes) >= 3, "LYZ" %in% genes)
feature <- coord; feature$expression <- as.numeric(rna["LYZ", ])
emit("feature_clean_v1", "FeaturePlot", plot_feature_clean(feature, "LYZ expression"), "pbmc_small; all 80 cells", "RNA log-normalized data + UMAP",
     "Where is LYZ expressed?", "lognormalize", list(gene = "LYZ", scale = "LogNormalize; factor 10000"),
     "08_visualization/FeaturePlot/feature_clean_v1.R", "CURRENT_DEFAULT", palette = "viridis")
dot <- do.call(rbind, lapply(genes, function(g) do.call(rbind, lapply(levels(coord$group), function(group) {
  values <- as.numeric(rna[g, coord$group == group])
  data.frame(gene = g, group = group, average = mean(values), percent = mean(values > 0) * 100)
}))))
emit("dotplot_clean_v1", "DotPlot", plot_marker_dot(dot), "pbmc_small", "RNA expression summarized by computed cluster",
     "Which selected markers distinguish clusters?", "cell_markers", list(genes = genes, size = "percent > 0", color = "mean log expression"),
     "08_visualization/DotPlot/dotplot_clean_v1.R", "CURRENT_DEFAULT", palette = "viridis")
hm <- dot[, c("gene", "group", "average")]; names(hm) <- c("x", "y", "value")
emit("marker_heatmap_v1", "Heatmap", plot_research_heatmap(hm, title = "Selected marker means"), "pbmc_small", "Marker means; not scaled differential effects",
     "How do selected marker means vary by cluster?", "cell_markers", list(scale = "mean log expression", genes = genes),
     "08_visualization/Heatmap/heatmap_clean_v1.R", "CURRENT_DEFAULT", palette = "viridis")
top <- head(Seurat::VariableFeatures(obj), 10)
cluster_hm <- do.call(rbind, lapply(top, function(g) do.call(rbind, lapply(levels(coord$group), function(group)
  data.frame(x = group, y = g, value = mean(as.numeric(rna[g, coord$group == group])))))))
emit("cluster_heatmap_v1", "Heatmap", plot_research_heatmap(cluster_hm), "pbmc_small", "Top 10 variable genes summarized across all cells",
     "What expression patterns occur across clusters?", parameters = list(feature_selection = "first 10 FindVariableFeatures entries"), palette = "viridis")
v <- data.frame(group = coord$group, value = feature$expression)
emit("violin_clean_v1", "Violin", plot_research_violin(v, colors, "LYZ log expression"), "pbmc_small; all 80 cells including zeros", "RNA LYZ by cluster",
     "What is the per-cell LYZ distribution?", "lognormalize", list(gene = "LYZ", zero_policy = "retain"),
     "08_visualization/Violin/violin_clean_v1.R", "CURRENT_DEFAULT")
stacked <- do.call(rbind, lapply(genes, function(g) data.frame(gene = g, group = coord$group, value = as.numeric(rna[g, ]))))
p <- plot_research_violin(stacked, colors, "Log expression") + facet_grid(gene ~ ., scales = "free_y")
emit("stacked_violin_v1", "Violin", p, "pbmc_small", "Selected marker expression; all cells",
     "How do several marker distributions vary?", parameters = list(genes = genes), height_mm = 180)
comp <- as.data.frame(table(sample = obj$orig.ident, celltype = coord$group)); names(comp)[3] <- "count"
bar <- plot_composition(comp, colors)
emit("composition_sample_v1", "Composition", bar, "pbmc_small: one captured sample", "Counts of computed clusters, not biological labels",
     "What fraction of this capture belongs to each cluster?", parameters = list(unit = "captured cells; one sample, no condition comparison"),
     script = "08_visualization/Composition/composition_sample_v1.R", selection = "CURRENT_DEFAULT")
emit("cluster_count_bar_v1", "Barplot", ggplot(comp, aes(celltype, count, fill = celltype)) + geom_col(width = 0.7) +
       scale_fill_manual(values = colors) + guides(fill = "none") + labs(x = NULL, y = "Captured cells") + theme_research(),
     "pbmc_small", "Computed cluster counts", "How many cells were assigned to each cluster?")
emit("multipanel_pbmc_v1", "MultiPanel", (umap | plot_feature_clean(feature, "LYZ")) /
       (plot_marker_dot(dot) | bar) + plot_annotation(tag_levels = "A"),
     "pbmc_small", "UMAP, expression, marker summary and capture composition", "PBMC demo overview",
     parameters = list(layout = "2 by 2; A/B/C/D", color_map = colors), width_mm = 190, height_mm = 180)

iris_colors <- setNames(research_palette(n = 3), levels(iris$Species))
d <- data.frame(group = iris$Species, value = iris$Petal.Length)
emit("boxplot_iris_v1", "Boxplot", ggplot(d, aes(group, value, fill = group)) + geom_boxplot(width = 0.6, linewidth = 0.35) +
       scale_fill_manual(values = iris_colors) + guides(fill = "none") + labs(x = NULL, y = "Petal length (cm)"),
     "datasets::iris; all 150 flowers", "Petal.Length by Species", "What is the observed distribution across species?")
emit("violin_iris_v1", "Violin", plot_research_violin(d, iris_colors, "Petal length (cm)"), "datasets::iris", "Petal.Length",
     "Compare observed flower measurements")
emit("density_iris_v1", "Density", ggplot(iris, aes(Petal.Length, fill = Species)) + geom_density(alpha = 0.35) +
       scale_fill_manual(values = iris_colors) + labs(x = "Petal length (cm)", y = "Density"),
     "datasets::iris", "All Petal.Length observations", "How do measurement densities differ?", parameters = list(bandwidth = "stats::density default"))
ridge <- do.call(rbind, lapply(seq_along(levels(iris$Species)), function(i) {
  species <- levels(iris$Species)[i]; den <- density(iris$Petal.Length[iris$Species == species])
  data.frame(x = den$x, bottom = i, top = i + den$y * 0.6, Species = species)
}))
emit("ridge_iris_v1", "Ridge", ggplot(ridge, aes(x)) + geom_ribbon(aes(ymin = bottom, ymax = top, fill = Species), alpha = 0.7) +
       scale_fill_manual(values = iris_colors) + scale_y_continuous(breaks = 1:3, labels = levels(iris$Species)) +
       guides(fill = "none") + labs(x = "Petal length (cm)", y = NULL), "datasets::iris", "Kernel density of all species-specific observations",
     "Compare distribution shapes by species", parameters = list(density_height_scale = 0.6))
scatter <- plot_scatter_fit(iris, "Sepal.Length", "Petal.Length")
emit("scatter_fit_v1", "Scatter_Correlation", scatter, "datasets::iris (pooled species; potential confounding)", "All 150 flowers",
     "Show linear association and uncertainty", "correlation", list(method = "pearson", fit = "lm; 95% CI"),
     "08_visualization/Scatter_Correlation/scatter_fit_v1.R", "CURRENT_DEFAULT")
emit("density_scatter_v1", "Scatter_Correlation", ggplot(iris, aes(Sepal.Length, Petal.Length)) +
       geom_bin_2d(bins = 15) + scale_fill_viridis_c() + labs(x = "Sepal length (cm)", y = "Petal length (cm)", fill = "Count"),
     "datasets::iris", "All 150 flowers, binned without downsampling", "Where are observations concentrated?", parameters = list(bins = 15), palette = "viridis")
source("07_bulk_clinical_ml/correlation/scripts/workflow.R")
corr <- run_workflow(iris, list(variables = names(iris)[1:4], method = "pearson", missing = "error"))$tables$correlations
ch <- rbind(data.frame(x = corr$x, y = corr$y, value = corr$r, q = corr$p_adjust),
            data.frame(x = corr$y, y = corr$x, value = corr$r, q = corr$p_adjust))
p <- plot_research_heatmap(ch, TRUE, "Pearson correlations (BH across six tests)") +
       geom_text(aes(label = ifelse(q < 0.05, "*", "")), size = 3) +
       labs(caption = "* BH-adjusted P < 0.05; pooled species can confound association.")
emit("correlation_bh_heatmap_v1", "Scatter_Correlation", p, "datasets::iris", "Six unique Pearson pair tests; diagonal omitted",
     "Which associations pass the stated multiple-testing rule?", "correlation", list(adjustment = "BH over 6 pairs"), palette = "blue_white_red", height_mm = 130)
emit("pairplot_iris_v1", "Scatter_Correlation", (scatter | plot_scatter_fit(iris, "Sepal.Width", "Petal.Width")) + plot_annotation(tag_levels = "A"),
     "datasets::iris", "Two stated measurement pairs; all 150 observations", "Compare two association views", width_mm = 190)

km <- readRDS("results/smoke/km.rds")$object
s <- summary(km, censored = TRUE)
curve <- data.frame(time = s$time, survival = s$surv, lower = s$lower, upper = s$upper, group = s$strata)
initial <- data.frame(time = 0, survival = 1, lower = 1, upper = 1, group = names(km$strata))
curve <- rbind(initial, curve)
km_colors <- setNames(c("#0072B2", "#D55E00"), names(km$strata))
times <- c(0, 250, 500, 750, 1000)
time_limits <- c(0, max(survival::lung$time))
kp <- ggplot(curve, aes(time, survival, color = group)) + geom_step(linewidth = 0.65) +
      geom_step(aes(y = lower), linetype = 2, linewidth = 0.25) + geom_step(aes(y = upper), linetype = 2, linewidth = 0.25) +
      scale_color_manual(values = km_colors, labels = c("Sex 1", "Sex 2")) +
      scale_x_continuous(limits = time_limits, breaks = times) +
      labs(x = "Days", y = "Survival probability", color = NULL, caption = "Dashed step curves: 95% CI; right-censored public example.")
risk <- summary(km, times = times, extend = TRUE)
rd <- data.frame(time = risk$time, group = risk$strata, n = risk$n.risk)
rp <- ggplot(rd, aes(time, group, label = n)) + geom_text(size = 3) +
      scale_x_continuous(limits = time_limits, breaks = times) +
      scale_y_discrete(labels = c("group=1" = "Sex 1", "group=2" = "Sex 2")) +
      labs(x = "Days", y = "At risk") + theme_research_clean()
emit("survival_km_v1", "SurvivalPlot", kp / rp + plot_layout(heights = c(3, 1)), "survival::lung; 228 records", "Time, explicit event status=2, sex strata",
     "KM survival with uncertainty and risk counts", "survival_km", list(time_origin = "dataset time", event = "status == 2"), height_mm = 150)
cox <- readRDS("results/smoke/cox.rds")$object
ci <- summary(cox)$conf.int
forest <- data.frame(term = c("Age (per year)", "Sex (2 vs 1)"), hr = ci[, 1], lower = ci[, 3], upper = ci[, 4])
emit("forest_cox_v1", "ForestPlot", plot_cox_forest(forest), "survival::lung", "Multivariate Cox(age + sex)",
     "Hazard ratios with 95% confidence intervals", "cox", list(covariates = c("age", "sex")),
     "08_visualization/ForestPlot/forest_cox_v1.R", "CURRENT_DEFAULT")

set.seed(42)
train <- unlist(lapply(split(seq_len(nrow(iris)), iris$Species), function(i) sample(i, 35)))
test <- setdiff(seq_len(nrow(iris)), train)
rf <- randomForest::randomForest(Species ~ ., data = iris[train, ], ntree = 200)
scores <- predict(rf, iris[test, ], type = "prob")[, "versicolor"]
roc <- pROC::roc(iris$Species[test] == "versicolor", scores, levels = c(FALSE, TRUE), direction = "<", quiet = TRUE)
rocdata <- data.frame(fpr = 1 - roc$specificities, tpr = roc$sensitivities)
emit("roc_holdout_v1", "ROC", ggplot(rocdata, aes(fpr, tpr)) + geom_path(color = "#0072B2", linewidth = 0.7) +
      geom_abline(slope = 1, intercept = 0, linetype = 2, color = "#999999") + coord_equal() +
      labs(x = "False positive rate", y = "True positive rate", subtitle = sprintf("Held-out one-vs-rest AUC = %.3f; n = %d", pROC::auc(roc), length(test))),
     "datasets::iris; stratified 105 train / 45 test", "Random forest held-out versicolor probabilities", "Show held-out discrimination",
     "random_forest", list(seed = 42, ntree = 200, test_n = 45, positive_class = "versicolor"))

# Explicitly synthetic fixtures demonstrate style contracts only, isolated from real workflows.
set.seed(42)
volcano <- data.frame(gene = paste0("DemoGene", 1:120), log2FC = rnorm(120, 0, 1.4), padj = runif(120)^3)
emit("volcano_clean_v1", "Volcano", plot_research_volcano(volcano), "Synthetic fixture; seed 42", "120 artificial feature effects/P values",
     "Volcano style template", parameters = list(fdr = 0.05, effect = 1), script = "08_visualization/Volcano/volcano_clean_v1.R", synthetic = TRUE)
enrichment <- data.frame(pathway = paste("Demo set", LETTERS[1:7]), score = c(4.2, 3.6, 2.8, 2.3, 1.9, 1.5, 1.2), count = c(18, 15, 14, 11, 9, 8, 7))
emit("enrichment_dot_style_v1", "Enrichment", ggplot(enrichment, aes(score, reorder(pathway, score), size = count, color = score)) +
      geom_point() + scale_color_viridis_c() + labs(x = "Illustrative -log10 adjusted P", y = NULL),
     "Synthetic fixture", "Artificial set ranking", "Enrichment dot style", synthetic = TRUE, palette = "viridis")
emit("lollipop_style_v1", "Lollipop", ggplot(enrichment, aes(score, reorder(pathway, score))) +
      geom_segment(aes(x = 0, xend = score, yend = reorder(pathway, score)), color = "#BBBBBB") + geom_point(size = 3, color = "#0072B2") +
      labs(x = "Illustrative score", y = NULL), "Synthetic fixture", "Artificial scores", "Ranking lollipop style", synthetic = TRUE)
emit("waterfall_style_v1", "Waterfall", ggplot(data.frame(item = factor(LETTERS[1:8]), change = c(-40, -25, -10, 2, 8, 15, 23, 35)), aes(item, change, fill = change > 0)) +
      geom_col(width = 0.75) + geom_hline(yintercept = 0, linewidth = 0.3) + scale_fill_manual(values = c("#0072B2", "#D55E00"), guide = "none") +
      labs(x = "Illustrative observation", y = "Illustrative change"), "Synthetic fixture", "Artificial signed changes", "Waterfall style", synthetic = TRUE)
flow <- data.frame(source = c("Group A", "Group A", "Group B", "Group B"), target = c("State 1", "State 2", "State 1", "State 2"), count = c(18, 7, 9, 16))
emit("alluvial_style_v1", "Sankey_Alluvial", ggplot(flow, aes(axis1 = source, axis2 = target, y = count)) +
      ggalluvial::geom_alluvium(aes(fill = source), width = 0.12, alpha = 0.7) + ggalluvial::geom_stratum(width = 0.14, fill = "#EEEEEE") +
      ggalluvial::stat_stratum(geom = "text", aes(label = after_stat(stratum)), size = 3) + scale_x_discrete(limits = c("Source", "Target"), expand = c(0.12, 0.12)) +
      scale_fill_manual(values = c("Group A" = "#0072B2", "Group B" = "#D55E00")) + labs(y = "Illustrative count", x = NULL),
     "Synthetic fixture", "Artificial transitions, not lineage evidence", "Alluvial style", synthetic = TRUE)
graph <- igraph::graph_from_data_frame(data.frame(from = c("A", "A", "B", "C", "D"), to = c("B", "C", "D", "D", "A")), directed = TRUE)
emit("network_style_v1", "Network", ggraph::ggraph(graph, layout = "circle") +
      ggraph::geom_edge_link(color = "#AAAAAA", arrow = grid::arrow(length = grid::unit(2, "mm")), end_cap = ggraph::circle(4, "mm")) +
      ggraph::geom_node_point(size = 7, color = "#0072B2") + ggraph::geom_node_text(aes(label = name), color = "white", size = 3) + theme_research_network(),
     "Synthetic directed graph", "Artificial nodes/edges; not STRING or CellChat", "Network style", synthetic = TRUE)
nes <- expand.grid(x = c("Contrast A", "Contrast B"), y = paste("Demo set", LETTERS[1:6]))
nes$value <- seq(-2.2, 2.2, length.out = nrow(nes))
emit("nes_heatmap_style_v1", "Enrichment", plot_research_heatmap(nes, TRUE), "Synthetic fixture", "Artificial NES-like scores; not fgsea output",
     "Signed pathway-effect heatmap style", synthetic = TRUE, palette = "blue_white_red")

palettes <- read_registry("registry/palettes.yml")$palettes
swatches <- do.call(rbind, lapply(palettes, function(p) data.frame(palette = p$id, x = seq_along(p$hex_colors), color = unlist(p$hex_colors))))
emit("palette_swatches_v1", "palettes", ggplot(swatches, aes(x, palette, fill = color)) + geom_tile(width = 0.94, height = 0.8) +
      scale_fill_identity() + labs(x = "Color index", y = NULL) + theme_research_heatmap(), "Installed ggsci/viridisLite and documented color specifications",
     "registry/palettes.yml", "Palette reference swatches", parameters = list(source_versions = c(ggsci = as.character(packageVersion("ggsci")))), width_mm = 180, height_mm = 150)

# Base/grid/complex graphics are exported through their native R device contract.
emit_native <- function(id, prefix, draw, dataset, source, method = "schematic", width = 7, height = 4) {
  if (!is.null(only) && id != only) return(invisible(NULL))
  dir.create(dirname(prefix), recursive = TRUE, showWarnings = FALSE)
  for (ext in c("png", "pdf", "svg")) {
    if (ext == "png") ragg::agg_png(paste0(prefix, ".png"), width = width, height = height, units = "in", res = 400)
    else if (ext == "pdf") grDevices::cairo_pdf(paste0(prefix, ".pdf"), width = width, height = height)
    else svglite::svglite(paste0(prefix, ".svg"), width = width, height = height)
    tryCatch(draw(), finally = grDevices::dev.off())
  }
  plots[[length(plots) + 1L]] <<- list(id = id, method = method, purpose = id, script = source,
    example_script = "scripts/generate_gallery.R", dataset = dataset, input_object = "Original vector components / explicit fixture",
    major_parameters = list(width_in = width, height_in = height, dpi = 400), palette = "celltype_registry / okabe_ito",
    theme = "original grid vector", output_file = paste0(prefix, ".png"), vector_file = paste0(prefix, ".pdf"),
    svg_file = paste0(prefix, ".svg"), status = "VALIDATED", selection = NULL, synthetic = TRUE,
    validation = list(status = "PASS", scope = "Original schematic/style rendering only; no mechanism certification"),
    source_inspiration = "Original repository drawing; no external art", last_generated = "2026-10-07")
}
emit_native("chord_style_v1", "08_visualization/Circle_Chord/gallery/chord_style_v1", function() {
  m <- matrix(c(0, 3, 2, 1, 0, 4, 2, 1, 0), 3, dimnames = list(c("A", "B", "C"), c("A", "B", "C")))
  circlize::circos.clear()
  circlize::chordDiagram(m, grid.col = c(A = "#0072B2", B = "#D55E00", C = "#009E73"), transparency = 0.35)
  title("SYNTHETIC chord style; not inferred communication", cex.main = 0.8)
  circlize::circos.clear()
}, "Synthetic directed matrix", "scripts/generate_gallery.R", "visualization")
source("10_scientific_schematics/workflow_diagrams/workflow_v1.R")
emit_native("schematic_workflow_v1", "10_scientific_schematics/workflow_diagrams/gallery/schematic_workflow_v1", draw_scrna_workflow,
            "Original workflow template", "10_scientific_schematics/workflow_diagrams/workflow_v1.R", width = 9, height = 3.5)
source("10_scientific_schematics/cell_interaction/cell_interaction_v1.R")
emit_native("schematic_cell_interaction_v1", "10_scientific_schematics/cell_interaction/gallery/schematic_cell_interaction_v1", draw_cell_interaction,
            "Hypothesis scaffold; no specific LR mechanism", "10_scientific_schematics/cell_interaction/cell_interaction_v1.R")
source("10_scientific_schematics/mechanism_diagrams/mechanism_v1.R")
emit_native("schematic_mechanism_v1", "10_scientific_schematics/mechanism_diagrams/gallery/schematic_mechanism_v1", draw_mechanism_template,
            "Original generic mechanism hypothesis template", "10_scientific_schematics/mechanism_diagrams/mechanism_v1.R", width = 5, height = 7)
emit_native("schematic_components_v1", "10_scientific_schematics/reusable_components/gallery/schematic_components_v1", function() {
  grid::grid.newpage()
  grobs <- list(cell_grob("Cell"), cell_grob("Immune cell", "#D55E00"), cell_grob("Fibroblast", "#8C6BB1", "fibroblast"),
    cell_grob("Epithelial", "#66A61E"), vessel_grob(), arrow_grob(0.15, 0.5, 0.85, 0.5),
    receptor_ligand_grob(), nucleic_acid_grob("DNA"), nucleic_acid_grob("RNA"), cytokine_grob(), pathway_node_grob("Pathway node"))
  for (i in seq_along(grobs)) {
    col <- (i - 1) %% 4; row <- (i - 1) %/% 4
    grid::pushViewport(grid::viewport(x = 0.13 + col * 0.245, y = 0.82 - row * 0.29, width = 0.22, height = 0.25))
    grid::grid.draw(grobs[[i]])
    grid::popViewport()
  }
}, "11 original grid components", "10_scientific_schematics/reusable_components/components.R", width = 8, height = 5.5)

if (is.null(only)) {
  for (p in plots) {
    jsonlite::write_json(p, sub("\\.png$", ".metadata.json", p$output_file), auto_unbox = TRUE, pretty = TRUE, null = "null")
  }
  planned <- read_registry("registry/planned_plots.yml")$plots
  # Keep reviewed assets maintained by independent generators.
  replaced_ids <- vapply(c(plots, planned), `[[`, character(1), "id")
  independent <- Filter(function(p) !p$id %in% replaced_ids, read_registry("registry/plots.yml")$plots)
  jsonlite::write_json(list(schema_version = 1, plots = c(plots, independent, planned)), "registry/plots.yml", auto_unbox = TRUE, pretty = TRUE, null = "null")
  schematics <- Filter(function(x) x$method == "schematic", plots)
  for (i in seq_along(schematics)) {
    schematics[[i]]$inspiration <- "Original generic vector composition"
    schematics[[i]]$layout <- schematics[[i]]$id
    schematics[[i]]$components <- "10_scientific_schematics/reusable_components/components.R"
    schematics[[i]]$editable_source <- schematics[[i]]$script
    schematics[[i]]$license_provenance <- "Original repository code/art; no third-party icons. Owner redistribution license not specified."
  }
  jsonlite::write_json(list(schema_version = 1, schematics = schematics), "registry/schematics.yml", auto_unbox = TRUE, pretty = TRUE, null = "null")
}
cat("Generated", length(plots), "PNG/PDF gallery items\n")
