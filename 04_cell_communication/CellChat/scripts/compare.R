# Rscript dispatcher uses method ID cellchat_compare; input is a named list of CellChat objects.
run_workflow <- function(input, config) {
  stopifnot(length(input) == 2L, !is.null(names(input)), all(vapply(input, inherits, logical(1), "CellChat")))
  if (!identical(levels(input[[1]]@idents), levels(input[[2]]@idents))) {
    stop("Cell-type ordering differs. Use the official different-composition tutorial and explicit liftCellChat alignment.")
  }
  source("04_cell_communication/CellChat/scripts/visualize.R")
  merged <- CellChat::mergeCellChat(input, add.names = names(input))
  out <- file.path(config$output_dir, "gallery")
  rows <- list()
  emit <- function(id, draw) { rows[[id]] <<- emit_cellchat_plot(id, out, draw) }
  for (measure in c("count", "weight")) {
    local({ m <- measure
      emit(paste0("cc_compare_total_", m, "_v1"), function() CellChat::compareInteractions(merged, measure = m))
      emit(paste0("cc_diff_circle_", m, "_v1"), function() CellChat::netVisual_diffInteraction(merged, measure = m, weight.scale = TRUE))
      emit(paste0("cc_diff_heatmap_", m, "_v1"), function() CellChat::netVisual_heatmap(merged, measure = m))
    })
  }
  emit("cc_compare_pathways_v1", function() CellChat::rankNet(merged, mode = "comparison", do.stat = FALSE))
  if (!is.null(config$sources) && !is.null(config$targets)) {
    for (dataset in 1:2) {
      local({ i <- dataset
        emit(paste0("cc_differential_lr_dataset", i, "_v1"), function() CellChat::netVisual_bubble(merged,
          sources.use = unlist(config$sources), targets.use = unlist(config$targets),
          comparison = c(1, 2), max.dataset = i, remove.isolate = TRUE))
      })
    }
    for (source in unlist(config$sources)) {
      local({ cell <- source
        emit(paste0("cc_role_change_", make.names(cell)), function() CellChat::netAnalysis_signalingChanges_scatter(merged, idents.use = cell))
      })
    }
  }
  if (isTRUE(config$embedding)) {
    set.seed(config$seed)
    for (type in c("functional", "structural")) {
      merged <- CellChat::computeNetSimilarityPairwise(merged, type = type)
      merged <- CellChat::netEmbedding(merged, type = type, umap.method = "uwot")
      merged <- CellChat::netClustering(merged, type = type, do.plot = FALSE, do.parallel = FALSE)
      local({ similarity <- type; current <- merged
        emit(paste0("cc_embedding_", similarity, "_v1"), function() CellChat::netVisual_embeddingPairwise(current, type = similarity))
      })
    }
  }
  a <- CellChat::subsetCommunication(input[[1]])
  b <- CellChat::subsetCommunication(input[[2]])
  keys <- c("source", "target", "interaction_name", "pathway_name")
  delta <- merge(a[, c(keys, "prob")], b[, c(keys, "prob")], by = keys, all = TRUE, suffixes = c("_first", "_second"))
  delta$prob_first[is.na(delta$prob_first)] <- 0
  delta$prob_second[is.na(delta$prob_second)] <- 0
  delta$delta <- delta$prob_second - delta$prob_first
  list(object = merged, tables = list(differential_lr = delta, plot_manifest = do.call(rbind, rows)))
}
