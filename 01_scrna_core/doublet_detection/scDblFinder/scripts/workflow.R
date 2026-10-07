run_workflow <- function(input, config) {
  stopifnot(inherits(input, "Seurat"), config$capture_column %in% names(input[[]]))
  counts <- SeuratObject::GetAssayData(input, assay = "RNA", layer = "counts")
  sce <- SingleCellExperiment::SingleCellExperiment(assays = list(counts = counts))
  set.seed(config$seed)
  sce <- scDblFinder::scDblFinder(sce, samples = input[[config$capture_column]][, 1],
                                 dbr = config$dbr, BPPARAM = BiocParallel::SerialParam())
  input$scDblFinder.score <- SummarizedExperiment::colData(sce)$scDblFinder.score
  input$scDblFinder.class <- SummarizedExperiment::colData(sce)$scDblFinder.class
  list(object = input, tables = list(doublets = data.frame(cell = colnames(input),
       score = input$scDblFinder.score, class = input$scDblFinder.class)))
}
