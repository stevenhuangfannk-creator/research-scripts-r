run_workflow <- function(input, config) {
  stopifnot(inherits(input, "Seurat"))
  obj <- Seurat::SCTransform(input, assay = "RNA", vst.flavor = "v2",
                             vars.to.regress = config$vars_to_regress,
                             seed.use = config$seed, verbose = FALSE)
  list(object = obj, tables = list())
}
