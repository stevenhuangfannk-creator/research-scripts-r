run_workflow <- function(input, config) {
  stopifnot(inherits(input, "Seurat"))
  SeuratObject::DefaultAssay(input) <- "RNA"
  obj <- Seurat::NormalizeData(input, normalization.method = "LogNormalize",
                              scale.factor = config$scale_factor, verbose = FALSE)
  list(object = obj, tables = list())
}
