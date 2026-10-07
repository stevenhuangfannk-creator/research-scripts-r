run_workflow <- function(input, config) {
  stopifnot(inherits(input, "Seurat"), config$batch_column %in% names(input[[]]))
  objects <- Seurat::SplitObject(input, split.by = config$batch_column)
  if (length(objects) < 2L) stop("At least two batches required")
  objects <- lapply(objects, function(x) {
    x <- Seurat::NormalizeData(x, verbose = FALSE)
    Seurat::FindVariableFeatures(x, nfeatures = config$nfeatures, verbose = FALSE)
  })
  features <- Seurat::SelectIntegrationFeatures(objects, nfeatures = config$nfeatures)
  anchors <- Seurat::FindIntegrationAnchors(objects, anchor.features = features, dims = seq_len(config$npcs))
  obj <- Seurat::IntegrateData(anchors, dims = seq_len(config$npcs))
  # Keep RNA counts/data for DEG and communication; integrated values are for geometry.
  list(object = obj, tables = list())
}
