# Input list(counts, cell_metadata, gene_metadata); gene_metadata includes gene_short_name.
run_workflow <- function(input, config) {
  stopifnot(is.list(input), identical(colnames(input$counts), rownames(input$cell_metadata)),
            identical(rownames(input$counts), rownames(input$gene_metadata)),
            "gene_short_name" %in% names(input$gene_metadata),
            length(config$root_cells) > 0,
            all(unlist(config$root_cells) %in% colnames(input$counts)))
  set.seed(config$seed)
  cds <- monocle3::new_cell_data_set(input$counts, cell_metadata = input$cell_metadata,
                                     gene_metadata = input$gene_metadata)
  cds <- monocle3::preprocess_cds(cds, num_dim = config$num_dim)
  if (!is.null(config$alignment_group)) cds <- monocle3::align_cds(cds, alignment_group = config$alignment_group)
  cds <- monocle3::reduce_dimension(cds, reduction_method = "UMAP", umap.fast_sgd = FALSE, cores = 1)
  cds <- monocle3::cluster_cells(cds, random_seed = config$seed)
  cds <- monocle3::learn_graph(cds, use_partition = config$use_partition,
            close_loop = config$close_loop, learn_graph_control = list(minimal_branch_len = config$minimal_branch_len))
  cds <- monocle3::order_cells(cds, root_cells = unlist(config$root_cells))
  pt <- monocle3::pseudotime(cds)
  if (any(!is.finite(pt))) warning("Unreachable cells have infinite pseudotime: choose justified roots for each partition")
  graph <- monocle3::principal_graph(cds)[["UMAP"]]
  degree <- igraph::degree(graph)
  nodes <- data.frame(node = names(degree), degree = unname(degree),
                       role = ifelse(degree > 2, "branch", ifelse(degree == 1, "leaf", "internal")))
  source("03_cell_dynamics/monocle3/scripts/visualize.R")
  manifest <- monocle_gallery(cds, config)
  list(object = cds, tables = list(pseudotime = data.frame(cell = names(pt), pseudotime = unname(pt), reachable = is.finite(pt)),
                                    graph_nodes = nodes, graph_edges = igraph::as_data_frame(graph), plot_manifest = manifest))
}
