# Run from repository root: Rscript scripts/run_method.R <id> <config.yml> [--allow-unvalidated]
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2L) stop("Usage: <method_id> <config.yml> [--allow-unvalidated]")
source("scripts/read_registry.R")
registry <- read_registry("registry/methods.yml")$methods
hit <- Filter(function(x) identical(x$id, args[[1]]), registry)
if (length(hit) != 1L) stop("Unknown or duplicate method ID")
method <- hit[[1]]
if (is.null(method$script)) stop("This method has no executable workflow; read its card")
if (!isTRUE(method$validated) && !"--allow-unvalidated" %in% args) {
  stop("Workflow is unvalidated. Read METHOD_CARD, then explicitly use --allow-unvalidated.")
}
config <- read_registry(args[[2]])
stopifnot(is.character(config$input), is.character(config$output_dir))
input <- switch(tolower(tools::file_ext(config$input)),
                rds = readRDS(config$input),
                csv = read.csv(config$input, check.names = FALSE),
                tsv = read.delim(config$input, check.names = FALSE),
                stop("Input must be RDS, CSV or TSV"))
source(method$script)
result <- run_workflow(input, config)
dir.create(config$output_dir, recursive = TRUE, showWarnings = FALSE)
if (!is.null(result$object)) saveRDS(result$object, file.path(config$output_dir, "object.rds"))
for (nm in names(result$tables)) {
  utils::write.table(result$tables[[nm]], file.path(config$output_dir, paste0(nm, ".tsv")),
                     sep = "\t", quote = FALSE, row.names = FALSE)
}
writeLines(capture.output(sessionInfo()), file.path(config$output_dir, "sessionInfo.txt"))
yaml::write_yaml(list(method = method$id, config = config, generated = as.character(Sys.time()),
                      validation_scope = method$validation$scope),
                 file.path(config$output_dir, "run_metadata.yml"))
cat("Completed", method$id, "at", config$output_dir, "\n")
