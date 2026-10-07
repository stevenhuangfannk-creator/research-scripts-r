# Structural/promotion regression checks. Does not certify analytical validity.
source("scripts/read_registry.R")
methods <- read_registry("registry/methods.yml")$methods
plots <- read_registry("registry/plots.yml")$plots
palettes <- read_registry("registry/palettes.yml")$palettes
schematics <- read_registry("registry/schematics.yml")$schematics
statuses <- c("CANDIDATE", "VALIDATED", "RECOMMENDED", "DEFAULT", "EXPERIMENTAL", "DEPRECATED")
stopifnot(!anyDuplicated(vapply(methods, `[[`, character(1), "id")),
          !anyDuplicated(vapply(plots, `[[`, character(1), "id")),
          !anyDuplicated(vapply(palettes, `[[`, character(1), "id")))
for (method in methods) {
  stopifnot(method$status %in% statuses, file.exists(method$config),
            all(file.exists(file.path(method$path, c("README.md", "METHOD_CARD.md", "OUTPUT_CATALOG.md", "references.yml", "examples/README.md", "gallery/README.md")))))
  if (!is.null(method$script)) stopifnot(file.exists(method$script))
  if (isTRUE(method$validated)) stopifnot(method$validation$status == "PASS", !is.null(method$validation$dataset), !is.null(method$validation$date))
  if (method$status %in% c("DEFAULT", "RECOMMENDED")) stopifnot(isTRUE(method$validated), !is.null(method$comparison_evidence))
}
for (plot in plots) {
  stopifnot(plot$status %in% statuses)
  if (!is.null(plot$script)) stopifnot(file.exists(plot$script))
  if (!is.null(plot$output_file)) {
    required <- c("dataset", "input_object", "major_parameters", "palette", "theme", "script", "vector_file", "last_generated")
    stopifnot(all(vapply(required, function(x) !is.null(plot[[x]]), logical(1))), plot$validation$status == "PASS",
              file.exists(plot$output_file), file.exists(plot$vector_file))
    stopifnot(identical(readBin(plot$output_file, "raw", 8), as.raw(c(137, 80, 78, 71, 13, 10, 26, 10))))
    stopifnot(rawToChar(readBin(plot$vector_file, "raw", 5)) == "%PDF-")
    metadata_path <- sub("\\.png$", ".metadata.json", plot$output_file)
    stopifnot(file.exists(metadata_path))
    metadata <- read_registry(metadata_path)
    stopifnot(identical(metadata$id, plot$id), identical(metadata$script, plot$script),
              identical(metadata$output_file, plot$output_file))
  } else stopifnot(is.null(plot$selection), is.null(plot$last_generated))
  if (identical(plot$selection, "CURRENT_DEFAULT")) stopifnot(!is.null(plot$output_file))
}
for (p in palettes) {
  stopifnot(p$type %in% c("categorical", "continuous", "diverging"),
            all(grepl("^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$", unlist(p$hex_colors))))
}
for (s in schematics) stopifnot(file.exists(s$editable_source), file.exists(s$vector_file), !is.null(s$license_provenance))
preservation <- read_registry("docs/validation/preservation.json")
preserved <- preservation$file_hashes
for (path in names(preserved)) {
  stopifnot(file.exists(path))
  if (!identical(digest::digest(file = path, algo = "sha256"), preserved[[path]])) {
    # Git normalizes text line endings on other hosts; verify canonical content as well.
    blob <- system2("git", c("hash-object", shQuote(path)), stdout = TRUE)
    stopifnot(identical(blob, preservation$git_blobs[[path]]))
  }
}
dirs <- c("scripts", "01_scrna_core", "02_differential_analysis", "03_cell_dynamics", "04_cell_communication",
          "05_pathway_function", "07_bulk_clinical_ml", "08_visualization", "10_scientific_schematics")
sources <- unlist(lapply(dirs, function(x) list.files(x, pattern = "\\.R$", full.names = TRUE, recursive = TRUE)))
for (path in sources) {
  parse(path)
  text <- readLines(path, warn = FALSE)
  if (any(grepl("(^|[\"'[:space:]])[A-Za-z]:[/\\\\]", text))) stop("Absolute local path in ", path)
}
summary <- list(date = "2026-10-07", structural_status = "PASS", method_entries = length(methods),
   smoke_validated_methods = sum(vapply(methods, function(x) isTRUE(x$validated), logical(1))),
   generated_gallery = sum(vapply(plots, function(x) !is.null(x$output_file), logical(1))),
   planned_gallery = sum(vapply(plots, function(x) is.null(x$output_file), logical(1))),
   palettes = length(palettes), schematics = length(schematics), preserved_files = length(preserved),
   parsed_new_r_sources = length(sources))
jsonlite::write_json(summary, "docs/validation/structural_results.json", pretty = TRUE, auto_unbox = TRUE)
cat(jsonlite::toJSON(summary, auto_unbox = TRUE, pretty = TRUE), "\n")
