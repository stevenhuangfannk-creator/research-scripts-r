# Parameterized extraction of the APAP inference sequence. No private namespace patching.
infer_cellchat <- function(expression, metadata, config) {
  stopifnot(config$species %in% c("human", "mouse"),
            identical(config$expression_scale, "lognormalized_RNA"),
            config$group_column %in% names(metadata),
            identical(colnames(expression), rownames(metadata)),
            all(is.finite(expression)), all(expression >= 0))
  if (anyNA(metadata[[config$group_column]])) stop("Missing communication labels: select cells explicitly first")
  if (any(table(metadata[[config$group_column]]) < config$min_cells)) stop("Too few cells in a communication group")
  set.seed(config$seed)
  cc <- CellChat::createCellChat(expression, meta = metadata, group.by = config$group_column)
  cc@DB <- getExportedValue("CellChat", paste0("CellChatDB.", config$species))
  if (!is.null(config$db_annotation)) cc@DB <- CellChat::subsetDB(cc@DB, search = config$db_annotation)
  cc <- CellChat::subsetData(cc)
  cc <- CellChat::identifyOverExpressedGenes(cc)
  cc <- CellChat::identifyOverExpressedInteractions(cc)
  if (isTRUE(config$ppi_projection)) {
    # PPI projection is an optional information projection step.
    cc <- CellChat::projectData(cc, getExportedValue("CellChat", paste0("PPI.", config$species)))
  }
  cc <- CellChat::computeCommunProb(cc, type = config$average,
           population.size = config$population_size, raw.use = !isTRUE(config$ppi_projection),
           nboot = config$nboot, seed.use = config$seed)
  cc <- CellChat::filterCommunication(cc, min.cells = config$min_cells)
  cc <- CellChat::computeCommunProbPathway(cc)
  cc <- CellChat::aggregateNet(cc)
  CellChat::netAnalysis_computeCentrality(cc, slot.name = "netP")
}
run_workflow <- function(input, config) {
  # Input list(expression = genes x cells log-normalized RNA, metadata = aligned data.frame).
  cc <- infer_cellchat(input$expression, input$metadata, config)
  source("04_cell_communication/CellChat/scripts/visualize.R")
  manifest <- cellchat_gallery(cc, config)
  list(object = cc, tables = list(ligand_receptor = CellChat::subsetCommunication(cc),
    pathway = CellChat::subsetCommunication(cc, slot.name = "netP"),
    count_matrix = data.frame(source = rownames(cc@net$count), cc@net$count, check.names = FALSE),
    strength_matrix = data.frame(source = rownames(cc@net$weight), cc@net$weight, check.names = FALSE),
    plot_manifest = manifest))
}
