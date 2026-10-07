run_workflow <- function(input, config) {
  stopifnot(inherits(input, "Seurat"), config$batch_column %in% names(input[[]]),
            "pca" %in% names(input@reductions))
  if (length(unique(input[[config$batch_column]][, 1])) < 2L) stop("At least two batches required")
  obj <- harmony::RunHarmony(input, group.by.vars = config$batch_column,
                             reduction.use = "pca", dims.use = seq_len(config$npcs),
                             theta = config$theta, verbose = FALSE)
  list(object = obj, tables = list())
}
