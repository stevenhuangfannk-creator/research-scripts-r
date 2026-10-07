# Extracted from the GSE255834/APAP object-creation pattern, with explicit metadata.
run_workflow <- function(input, config) {
  stopifnot(is.list(input), !is.null(input$counts), !is.null(input$metadata))
  counts <- input$counts
  meta <- input$metadata
  stopifnot(!is.null(rownames(counts)), !is.null(colnames(counts)),
            !anyDuplicated(rownames(counts)), !anyDuplicated(colnames(counts)),
            setequal(colnames(counts), rownames(meta)))
  stopifnot(all(is.finite(counts)), all(counts >= 0))
  obj <- Seurat::CreateSeuratObject(counts, meta.data = meta[colnames(counts), , drop = FALSE],
                                    min.cells = 0, min.features = 0,
                                    project = config$project)
  list(object = obj, tables = list(features = data.frame(feature = rownames(counts)),
                                   cells = data.frame(cell = colnames(counts), meta[colnames(counts), , drop = FALSE])))
}
