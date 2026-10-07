# Rscript scripts/resolve_asset.R method|plot|palette <id>
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2L)
kind <- switch(args[[1]], method = "methods", plot = "plots", palette = "palettes",
               stop("Use method, plot or palette"))
source("scripts/read_registry.R")
items <- read_registry(file.path("registry", paste0(kind, ".yml")))[[kind]]
hit <- Filter(function(x) identical(x$id, args[[2]]), items)
if (length(hit) != 1L) stop("Asset ID does not resolve uniquely")
cat(yaml::as.yaml(hit[[1]]))
