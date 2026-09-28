args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) != 1L) stop("Run this file with Rscript")

script_path <- normalizePath(sub("^--file=", "", file_arg), winslash = "/")
project_root <- dirname(dirname(script_path))
environment_dir <- file.path(project_root, "environment")
dir.create(environment_dir, recursive = TRUE, showWarnings = FALSE)

package_groups <- list(
  pilot_core = c("Seurat", "dplyr", "ggplot2", "patchwork", "reshape2", "cowplot", "knitr"),
  upstream_extended = c(
    "tidyr", "scales", "gdata", "ggraph", "scater", "SingleR", "data.table",
    "paletteer", "R.utils", "ComplexHeatmap", "clustree", "viridis", "pheatmap",
    "devtools", "Scillus", "scFunctions", "ggcharts", "schex", "Cairo",
    "cartography", "kableExtra", "gsfisher", "BiocParallel", "nichenetr",
    "easyalluvial", "purrr"
  )
)

rows <- do.call(rbind, lapply(names(package_groups), function(group) {
  do.call(rbind, lapply(package_groups[[group]], function(package) {
    installed <- package %in% rownames(installed.packages())
    version <- if (installed) as.character(packageVersion(package)) else NA_character_
    load_result <- if (!installed) {
      "not installed"
    } else {
      tryCatch({
        loadNamespace(package)
        "ok"
      }, error = function(e) paste0("error: ", conditionMessage(e)))
    }
    data.frame(
      group = group,
      package = package,
      installed = installed,
      version = version,
      load_status = load_result,
      stringsAsFactors = FALSE
    )
  }))
}))

write.table(
  rows,
  file.path(environment_dir, "package_status.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE,
  na = ""
)
writeLines(capture.output(sessionInfo()), file.path(environment_dir, "sessionInfo.txt"))

core <- rows[rows$group == "pilot_core", , drop = FALSE]
failed_core <- core$package[core$load_status != "ok"]
cat("R:", R.version.string, "\n")
cat("Project:", project_root, "\n")
cat("Core packages ready:", nrow(core) - length(failed_core), "/", nrow(core), "\n")
if (length(failed_core)) {
  cat("Blocked core packages:", paste(failed_core, collapse = ", "), "\n")
  quit(status = 2L)
}

