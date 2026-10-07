# No universal QC cutoff: thresholds and species-sensitive gene patterns are supplied.
run_workflow <- function(input, config) {
  stopifnot(inherits(input, "Seurat"), all(c("mt_pattern", "ribo_pattern", "thresholds") %in% names(config)))
  obj <- input
  for (nm in c("mt", "ribo")) {
    pattern <- config[[paste0(nm, "_pattern")]]
    if (!any(grepl(pattern, rownames(obj)))) warning("No genes match ", nm, " pattern; check species / feature IDs")
    obj[[paste0("percent.", nm)]] <- Seurat::PercentageFeatureSet(obj, pattern = pattern, assay = "RNA")
  }
  q <- config$thresholds
  stopifnot(all(c("min_features", "max_features", "min_counts", "max_counts", "max_mt") %in% names(q)))
  m <- obj[[]]
  obj$qc_pass <- with(m, nFeature_RNA >= q$min_features & nFeature_RNA <= q$max_features &
                      nCount_RNA >= q$min_counts & nCount_RNA <= q$max_counts & percent.mt <= q$max_mt)
  audit <- data.frame(cell = colnames(obj), obj[[]], check.names = FALSE)
  # Preserve all cells in the returned audit. Filtering is explicit and records before/after.
  if (isTRUE(config$filter)) obj <- subset(obj, cells = colnames(obj)[obj$qc_pass])
  list(object = obj, tables = list(qc = audit,
       retention = data.frame(input_cells = ncol(input), retained_cells = ncol(obj),
                              pass_cells = sum(audit$qc_pass))))
}
