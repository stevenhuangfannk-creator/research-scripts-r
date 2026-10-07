# Advanced exploratory graph association and modules; no Monocle2 BEAM substitution.
run_workflow <- function(input, config) {
  stopifnot(inherits(input, "cell_data_set"))
  tests <- monocle3::graph_test(input, neighbor_graph = "principal_graph", cores = config$cores)
  genes <- rownames(tests)[!is.na(tests$q_value) & tests$q_value < config$q_value]
  if (length(genes) < 2L) stop("Too few graph-associated genes for modules")
  modules <- monocle3::find_gene_modules(input[genes, ], resolution = config$resolution,
                                         random_seed = config$seed, cores = config$cores)
  cell_groups <- data.frame(cell = colnames(input), group = SummarizedExperiment::colData(input)[[config$celltype_column]])
  aggregate <- monocle3::aggregate_gene_expression(input, modules, cell_groups)
  source("08_visualization/themes/theme_research.R")
  source("08_visualization/Heatmap/heatmap_clean_v1.R")
  d <- as.data.frame(as.table(aggregate)); names(d) <- c("y", "x", "value")
  save_research_plot(plot_research_heatmap(d, title = "Gene modules by cell group"),
                     file.path(config$output_dir, "gallery", "m3_gene_modules_v1"))
  # Branch membership is supplied from an explicitly selected subgraph, not inferred from arbitrary cluster IDs.
  if (!is.null(config$branch_cells)) {
    cells <- unlist(config$branch_cells)
    stopifnot(all(cells %in% colnames(input)))
    branch <- input[, cells]
    branch_tests <- monocle3::graph_test(branch, neighbor_graph = "knn", cores = config$cores)
  } else branch_tests <- data.frame()
  tests$gene <- rownames(tests)
  list(object = modules, tables = list(graph_association = tests, gene_modules = modules, branch_association = branch_tests))
}
