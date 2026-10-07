# Input = list(ranks: named numeric vector, pathways: named gene-set list).
run_workflow <- function(input, config) {
  stopifnot(is.list(input), is.numeric(input$ranks), !anyDuplicated(names(input$ranks)),
            !is.null(names(input$ranks)), all(is.finite(input$ranks)))
  set.seed(config$seed)
  ranks <- sort(input$ranks, decreasing = TRUE)
  result <- fgsea::fgseaMultilevel(pathways = input$pathways, stats = ranks,
                                   minSize = config$min_size, maxSize = config$max_size)
  result$leadingEdge <- vapply(result$leadingEdge, paste, character(1), collapse = ";")
  list(object = NULL, tables = list(gsea = as.data.frame(result)))
}
