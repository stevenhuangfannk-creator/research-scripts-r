# Input is a list(counts, metadata, backgrounds): one raw empty-droplet matrix per capture.
run_workflow <- function(input, config) {
  stopifnot(is.list(input), identical(colnames(input$counts), rownames(input$metadata)),
            config$capture_column %in% names(input$metadata))
  capture <- as.character(input$metadata[[config$capture_column]])
  results <- lapply(unique(capture), function(s) {
    cells <- which(capture == s)
    sce <- SingleCellExperiment::SingleCellExperiment(assays = list(counts = input$counts[, cells, drop = FALSE]))
    bg <- input$backgrounds[[s]]
    if (!is.null(bg)) stopifnot(identical(rownames(bg), rownames(input$counts)))
    set.seed(config$seed)
    celda::decontX(sce, background = bg, verbose = FALSE)
  })
  names(results) <- unique(capture)
  audit <- do.call(rbind, lapply(names(results), function(s) data.frame(
    cell = colnames(results[[s]]), capture = s,
    contamination = SummarizedExperiment::colData(results[[s]])$decontX_contamination)))
  list(object = results, tables = list(contamination = audit))
}
