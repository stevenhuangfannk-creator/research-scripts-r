args <- commandArgs(trailingOnly = TRUE)

parse_args <- function(values) {
  parsed <- list()
  i <- 1L
  while (i <= length(values)) {
    if (!startsWith(values[[i]], "--") || i == length(values)) {
      stop("Arguments must be --name value pairs")
    }
    key <- sub("^--", "", values[[i]])
    parsed[[key]] <- values[[i + 1L]]
    i <- i + 2L
  }
  parsed
}

options <- parse_args(args)
required_args <- c("manifest", "output-dir", "context")
missing_args <- required_args[!required_args %in% names(options)]
if (length(missing_args)) {
  stop("Missing arguments: ", paste(missing_args, collapse = ", "))
}

manifest_path <- normalizePath(options[["manifest"]], winslash = "/", mustWork = TRUE)
output_dir <- normalizePath(options[["output-dir"]], winslash = "/", mustWork = FALSE)
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

manifest <- read.delim(manifest_path, stringsAsFactors = FALSE, check.names = FALSE)
expected_columns <- c("group", "package", "required")
if (!identical(names(manifest), expected_columns)) {
  stop("Manifest columns must be: ", paste(expected_columns, collapse = ", "))
}
if (!nrow(manifest) || anyDuplicated(manifest$package)) {
  stop("Manifest must contain at least one unique package")
}

required_text <- tolower(trimws(as.character(manifest$required)))
valid_required <- required_text %in% c("true", "false")
if (!all(valid_required)) stop("Manifest required values must be TRUE or FALSE")
manifest$required <- required_text == "true"

installed <- installed.packages()
rows <- lapply(seq_len(nrow(manifest)), function(i) {
  package <- manifest$package[[i]]
  is_installed <- package %in% rownames(installed)
  version <- if (is_installed) installed[package, "Version"] else NA_character_
  load_status <- if (!is_installed) {
    "not installed"
  } else {
    tryCatch({
      loadNamespace(package)
      "ok"
    }, error = function(e) paste0("error: ", conditionMessage(e)))
  }
  data.frame(
    group = manifest$group[[i]],
    package = package,
    required = manifest$required[[i]],
    installed = is_installed,
    version = version,
    load_status = load_status,
    stringsAsFactors = FALSE
  )
})
status <- do.call(rbind, rows)

write.table(
  status,
  file.path(output_dir, "package_status.tsv"),
  sep = "\t",
  quote = FALSE,
  row.names = FALSE,
  na = ""
)
session_lines <- sub("[[:space:]]+$", "", capture.output(sessionInfo()))
writeLines(session_lines, file.path(output_dir, "sessionInfo.txt"))

failed_required <- status$package[status$required & status$load_status != "ok"]
summary_lines <- c(
  paste0("context: ", options[["context"]]),
  paste0("r: ", R.version.string),
  paste0("manifest: ", manifest_path),
  paste0("packages_checked: ", nrow(status)),
  paste0("required_ready: ", sum(status$required & status$load_status == "ok"), "/", sum(status$required)),
  paste0("blocked_required: ", if (length(failed_required)) paste(failed_required, collapse = ", ") else "none")
)
writeLines(summary_lines, file.path(output_dir, "preflight_summary.txt"))
cat(paste(summary_lines, collapse = "\n"), "\n")

if (length(failed_required)) quit(status = 2L)
