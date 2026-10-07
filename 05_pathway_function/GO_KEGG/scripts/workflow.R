# Input = list(genes, universe); gene IDs must already match the specified database.
run_workflow <- function(input, config) {
  stopifnot(is.list(input), length(input$universe) > 0, all(input$genes %in% input$universe))
  if (config$ontology == "KEGG") {
    result <- clusterProfiler::enrichKEGG(gene = input$genes, universe = input$universe,
              organism = config$organism, keyType = config$key_type, pAdjustMethod = "BH")
  } else {
    db <- getExportedValue(config$orgdb_package, config$orgdb_package)
    result <- clusterProfiler::enrichGO(gene = input$genes, universe = input$universe, OrgDb = db,
              keyType = config$key_type, ont = config$ontology, pAdjustMethod = "BH")
  }
  list(object = result, tables = list(enrichment = as.data.frame(result)))
}
