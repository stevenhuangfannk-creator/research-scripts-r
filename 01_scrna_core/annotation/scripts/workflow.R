# Reuse the hierarchical label-writeback pattern; tissue labels are explicit decisions.
run_workflow <- function(input, config) {
  stopifnot(inherits(input, "Seurat"), config$cluster_column %in% names(input[[]]))
  if (!is.list(config$labels) || !length(config$labels) ||
      is.null(names(config$labels)) || any(!nzchar(names(config$labels)))) {
    stop("Supply named annotation levels containing named cluster-to-label maps")
  }
  stopifnot(is.character(config$evidence), length(config$evidence) == 1L,
            nzchar(config$evidence))
  obj <- input
  clusters <- as.character(obj[[config$cluster_column]][, 1])
  audit <- data.frame(cell = colnames(obj), cluster = clusters)
  for (level in names(config$labels)) {
    map <- unlist(config$labels[[level]])
    stopifnot(length(map) > 0L, !is.null(names(map)), all(nzchar(names(map))),
              !anyDuplicated(names(map)))
    if (any(!names(map) %in% unique(clusters))) stop("Mapping includes unknown cluster")
    labels <- unname(map[clusters])
    labels[is.na(labels)] <- "Unknown"
    obj[[level]] <- labels
    audit[[level]] <- labels
  }
  audit$evidence <- config$evidence
  list(object = obj, tables = list(annotation = audit))
}
