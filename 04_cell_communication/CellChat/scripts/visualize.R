# Native CellChat, ggplot2, base graphics and ComplexHeatmap have different print contracts.
emit_cellchat_plot <- function(id, out, draw, width = 7.2, height = 5.2) {
  dir.create(out, recursive = TRUE, showWarnings = FALSE)
  for (ext in c("png", "pdf")) {
    file <- file.path(out, paste0(id, ".", ext))
    if (ext == "png") ragg::agg_png(file, width = width, height = height, units = "in", res = 400)
    else grDevices::cairo_pdf(file, width = width, height = height)
    tryCatch({
      p <- draw()
      if (inherits(p, "ggplot") || inherits(p, "patchwork")) print(p)
      else if (inherits(p, "Heatmap") || inherits(p, "HeatmapList")) ComplexHeatmap::draw(p)
    }, finally = grDevices::dev.off())
  }
  data.frame(plot_id = id, png = file.path(out, paste0(id, ".png")),
             pdf = file.path(out, paste0(id, ".pdf")), generated = as.character(Sys.Date()))
}
cellchat_gallery <- function(cc, config) {
  out <- file.path(config$output_dir, "gallery")
  rows <- list()
  emit <- function(id, draw) { rows[[id]] <<- emit_cellchat_plot(id, out, draw) }
  emit("cc_circle_count_v1", function() CellChat::netVisual_circle(cc@net$count, weight.scale = TRUE, title.name = "Interaction count"))
  emit("cc_circle_strength_v1", function() CellChat::netVisual_circle(cc@net$weight, weight.scale = TRUE, title.name = "Interaction strength"))
  emit("cc_count_heatmap_v1", function() CellChat::netVisual_heatmap(cc, measure = "count"))
  emit("cc_strength_heatmap_v1", function() CellChat::netVisual_heatmap(cc, measure = "weight"))
  emit("cc_role_scatter_v1", function() CellChat::netAnalysis_signalingRole_scatter(cc))
  for (pattern in c("incoming", "outgoing")) {
    local({ direction <- pattern
      emit(paste0("cc_", direction, "_heatmap_v1"), function() CellChat::netAnalysis_signalingRole_heatmap(cc, pattern = direction))
    })
  }
  # Biological pathway, receiver and pair selection must be supplied, not silently inferred.
  for (pathway in config$pathways) {
    if (!pathway %in% cc@netP$pathways) stop("Requested pathway not inferred: ", pathway)
    for (layout in c("circle", "chord", "hierarchy")) {
      local({ pw <- pathway; ly <- layout
        if (ly == "hierarchy" && is.null(config$receiver_indices)) stop("Hierarchy requires explicit receiver_indices")
        emit(paste0("cc_pathway_", ly, "_", make.names(pw)), function()
          CellChat::netVisual_aggregate(cc, signaling = pw, layout = ly, vertex.receiver = config$receiver_indices))
      })
    }
    local({ pw <- pathway
      emit(paste0("cc_pathway_heatmap_", make.names(pw)), function() CellChat::netVisual_heatmap(cc, signaling = pw))
      emit(paste0("cc_contribution_", make.names(pw)), function() CellChat::netAnalysis_contribution(cc, signaling = pw))
      emit(paste0("cc_centrality_", make.names(pw)), function() CellChat::netAnalysis_signalingRole_network(cc, signaling = pw))
    })
  }
  if (!is.null(config$pair)) {
    pair <- data.frame(interaction_name = config$pair)
    emit("cc_lr_circle_v1", function() CellChat::netVisual_individual(cc, signaling = config$pair_pathway, pairLR.use = pair, layout = "circle"))
  }
  if (!is.null(config$sources) && !is.null(config$targets)) {
    emit("cc_bubble_v1", function() CellChat::netVisual_bubble(cc, sources.use = unlist(config$sources),
                                               targets.use = unlist(config$targets), remove.isolate = FALSE))
  }
  emit("cc_pathway_rank_v1", function() CellChat::rankNet(cc, mode = "single", measure = "weight"))
  if (isTRUE(config$patterns)) {
    stopifnot(is.numeric(config$pattern_k), config$pattern_k >= 2)
    for (pattern in c("incoming", "outgoing")) {
      cc <- CellChat::identifyCommunicationPatterns(cc, pattern = pattern, k = config$pattern_k, heatmap.show = FALSE)
      local({ direction <- pattern; current <- cc
        cell <- current@netP$pattern[[direction]]$pattern$cell
        signal <- current@netP$pattern[[direction]]$pattern$signaling
        emit(paste0("cc_pattern_", direction, "_heatmap_v1"), function() {
          p <- ggplot2::ggplot(cell, ggplot2::aes(Pattern, CellGroup, fill = Contribution)) +
            ggplot2::geom_tile() + ggplot2::scale_fill_viridis_c() + ggplot2::theme_minimal(base_size = 9)
          p
        })
        emit(paste0("cc_pattern_", direction, "_river_v1"), function() CellChat::netAnalysis_river(current, pattern = direction))
        emit(paste0("cc_pattern_", direction, "_dot_v1"), function() CellChat::netAnalysis_dot(current, pattern = direction))
      })
    }
  }
  do.call(rbind, rows)
}
