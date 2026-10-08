# Regression checks use the actual exported example, not invented observations.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L) stop("Usage: Rscript scripts/test_umap_alternatives.R coordinates.csv")
source("08_visualization/UMAP/umap_fireworks_atlas.R")
source("08_visualization/UMAP/umap_density_landscape.R")
data <- read.csv(args[1])
original <- data
labels <- unique(as.character(data$group))
colors <- setNames(grDevices::hcl.colors(length(labels)), labels)
p <- plot_umap_fireworks_atlas(data, colors)
built <- ggplot2::ggplot_build(p)
stopifnot(nrow(built$data[[1]]) == nrow(data), identical(built$data[[1]]$x, data$x),
          identical(built$data[[1]]$y, data$y), identical(data, original))
s <- compute_umap_density_landscape(data)
stopifnot(sum(vapply(s$surfaces, function(x) x$cells, numeric(1))) == nrow(data),
          all(vapply(s$surfaces, function(x) abs(x$integral - 1) < 1e-10, logical(1))))
first <- s$surfaces[[1]]
stopifnot(all(vapply(s$surfaces, function(x) identical(x$x, first$x) && identical(x$y, first$y), logical(1))))
expect_error <- function(expr) stopifnot(inherits(tryCatch({force(expr); NULL}, error = identity), "error"))
bad <- data; bad$x[1] <- NA_real_
expect_error(plot_umap_fireworks_atlas(bad, colors))
expect_error(compute_umap_density_landscape(bad))
expect_error(plot_umap_fireworks_atlas(data, colors[-1]))
expect_error(compute_umap_density_landscape(data, bandwidth = c(0, 1)))
bad <- data; bad$condition[1] <- NA
expect_error(compute_umap_density_landscape(bad))
registry <- jsonlite::read_json("registry/plots.yml", simplifyVector = FALSE)$plots
planned <- jsonlite::read_json("registry/planned_plots.yml", simplifyVector = FALSE)$plots
generated_ids <- vapply(Filter(function(p) identical(p$example_script, "scripts/generate_gallery.R"), registry), `[[`, character(1), "id")
replaced_ids <- c(generated_ids, vapply(planned, `[[`, character(1), "id"))
independent <- Filter(function(p) !p$id %in% replaced_ids, registry)
stopifnot(setequal(vapply(independent, `[[`, character(1), "id"), c("umap_fireworks_atlas", "umap_density_landscape")))
cat("PASS: retained rows/coordinates, common grid, probability integrals and rejection checks.\n")
cat("PASS: registry merge preserves the independently generated alternatives.\n")
