# Exploratory cell-level markers, not replicate-aware condition DEG.
run_workflow <- function(input, config) {
  stopifnot(inherits(input, "Seurat"), config$group_column %in% names(input[[]]))
  SeuratObject::DefaultAssay(input) <- "RNA"
  Seurat::Idents(input) <- config$group_column
  result <- Seurat::FindAllMarkers(input, test.use = "wilcox", only.pos = config$only_positive,
                                   min.pct = config$min_pct, logfc.threshold = config$logfc_threshold,
                                   verbose = FALSE)
  list(object = NULL, tables = list(markers = result))
}
