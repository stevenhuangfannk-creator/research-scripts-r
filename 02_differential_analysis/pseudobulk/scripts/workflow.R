# Replicates are samples, not cells. Return raw sums; downstream DESeq2 design is explicit.
run_workflow <- function(input, config) {
  stopifnot(inherits(input, "Seurat"), all(c(config$sample_column, config$celltype_column) %in% names(input[[]])))
  counts <- Seurat::AggregateExpression(input, assays = "RNA", return.seurat = FALSE,
                group.by = c(config$sample_column, config$celltype_column))$RNA
  if (is.null(colnames(counts))) colnames(counts) <- "all_cells"
  list(object = counts, tables = list(library_sizes = data.frame(group = colnames(counts), counts = Matrix::colSums(counts))))
}
