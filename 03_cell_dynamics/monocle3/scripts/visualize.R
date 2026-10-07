monocle_gallery <- function(cds, config) {
  source("08_visualization/themes/theme_research.R")
  out <- file.path(config$output_dir, "gallery")
  manifest <- list()
  emit <- function(id, plot) {
    save_research_plot(plot, file.path(out, id), width_mm = 170, height_mm = 120)
    manifest[[id]] <<- data.frame(plot_id = id, png = file.path(out, paste0(id, ".png")), pdf = file.path(out, paste0(id, ".pdf")))
  }
  emit("m3_cluster_trajectory_v1", monocle3::plot_cells(cds, color_cells_by = "cluster"))
  emit("m3_celltype_trajectory_v1", monocle3::plot_cells(cds, color_cells_by = config$celltype_column, label_groups_by_cluster = FALSE))
  emit("m3_pseudotime_v1", monocle3::plot_cells(cds, color_cells_by = "pseudotime", label_cell_groups = FALSE))
  emit("m3_graph_nodes_v1", monocle3::plot_cells(cds, color_cells_by = config$celltype_column,
     label_cell_groups = FALSE, label_roots = TRUE, label_branch_points = TRUE, label_leaves = TRUE))
  emit("m3_backbone_v1", monocle3::plot_cells(cds, color_cells_by = config$celltype_column,
      label_cell_groups = FALSE, cell_size = 0.2, trajectory_graph_segment_size = 1))
  genes <- unlist(config$genes)
  if (length(genes)) {
    names_short <- SummarizedExperiment::rowData(cds)$gene_short_name
    selected <- which(names_short %in% genes | rownames(cds) %in% genes)
    if (length(selected) != length(unique(genes))) stop("Selected genes are missing or ambiguous; use unique feature IDs")
    emit("m3_gene_expression_v1", monocle3::plot_cells(cds, genes = genes, label_cell_groups = FALSE, show_trajectory_graph = FALSE))
    finite <- is.finite(monocle3::pseudotime(cds))
    emit("m3_genes_pseudotime_v1", monocle3::plot_genes_in_pseudotime(cds[selected, finite], color_cells_by = config$celltype_column))
  }
  emit("m3_publication_v1", monocle3::plot_cells(cds, color_cells_by = "pseudotime", label_cell_groups = FALSE,
       label_leaves = FALSE, label_branch_points = FALSE) + theme_research_clean() +
       ggplot2::labs(caption = "Pseudotime is expression-state ordering, not elapsed biological time."))
  do.call(rbind, manifest)
}
