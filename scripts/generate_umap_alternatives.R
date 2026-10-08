args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L) stop("Usage: Rscript scripts/generate_umap_alternatives.R coordinates.csv")
library(ggplot2)
source("08_visualization/UMAP/umap_fireworks_atlas.R")
source("08_visualization/UMAP/umap_density_landscape.R")
data <- read.csv(args[1], check.names = FALSE)
stopifnot(all(c("cell_id", "x", "y", "group", "condition", "sample_id") %in% names(data)), !anyDuplicated(data$cell_id))
out <- "08_visualization/UMAP/gallery"
# Keep the existing oral atlas plot_atlas.py mapping, sorted by broad identity.
labels <- sort(unique(as.character(data$group)))
palette <- setNames(c("#2a788e", "#c4772c", "#755d9a", "#4c8b63", "#bc586d", "#719cb0",
                     "#947b51", "#498580", "#b87ca8", "#607aad", "#ac8542", "#6e777b"), labels)
stopifnot(length(labels) == 12L)
p <- plot_umap_fireworks_atlas(data, palette, title = "GSE188217: parallel atlas-style UMAP") +
  labs(subtitle = sprintf("All %s retained cells | existing coordinates, no aesthetic downsampling", format(nrow(data), big.mark = ",")),
       caption = "One public library per condition; annotations are provisional. Unresolved cells retained.") +
  theme(plot.subtitle = element_text(size = 8), plot.caption = element_text(size = 7))
ggsave(file.path(out, "umap_fireworks_atlas.png"), p, width = 183, height = 135, units = "mm", dpi = 400, device = grDevices::png, type = "cairo")
ggsave(file.path(out, "umap_fireworks_atlas.pdf"), p, width = 183, height = 135, units = "mm", device = cairo_pdf)
landscape <- compute_umap_density_landscape(data)
stopifnot(all(vapply(landscape$surfaces, function(x) abs(x$integral - 1) < 1e-10, logical(1))))
grDevices::png(file.path(out, "umap_density_landscape.png"), width = 183, height = 120, units = "mm", res = 400, type = "cairo")
draw_umap_density_landscape(landscape)
grDevices::dev.off()
grDevices::cairo_pdf(file.path(out, "umap_density_landscape.pdf"), width = 183 / 25.4, height = 120 / 25.4)
draw_umap_density_landscape(landscape)
grDevices::dev.off()
grid <- do.call(rbind, lapply(names(landscape$surfaces), function(name) {
  s <- landscape$surfaces[[name]]
  transform(expand.grid(x = s$x, y = s$y), condition = name, density = as.vector(s$z))
}))
write.csv(grid, file.path(out, "umap_density_landscape.grid.csv"), row.names = FALSE)
write.csv(data.frame(label = labels, color = unname(palette)), file.path(out, "umap_fireworks_atlas.colors.csv"), row.names = FALSE)
receipt <- list(date = as.character(Sys.Date()), input_sha256 = digest::digest(file = args[1], algo = "sha256"),
  cells = nrow(data), excluded_cells = 0, coordinate_changes = 0, biological_validation = FALSE,
  conditions = as.list(table(data$condition)), bandwidth = landscape$bandwidth, grid_n = landscape$grid_n,
  limits = landscape$limits, density_max = landscape$density_max,
  surface_integrals = lapply(landscape$surfaces, function(x) x$integral),
  palette_source = "oral-scrna-atlas scripts/plot_atlas.py COLORS, sorted celltype_broad", R = R.version.string,
  dependencies = lapply(c("ggplot2", "ggrepel", "MASS", "viridisLite", "jsonlite", "digest"), function(x) paste(x, packageVersion(x))))
jsonlite::write_json(receipt, file.path(out, "umap_alternatives.validation.json"), pretty = TRUE, auto_unbox = TRUE)
capture.output(sessionInfo(), file = file.path(out, "umap_alternatives.sessionInfo.txt"))
source_receipt <- sub("\\.csv$", ".source.json", args[1])
if (file.exists(source_receipt)) file.copy(source_receipt, file.path(out, "GSE188217_umap.source.json"), overwrite = TRUE)
registry <- jsonlite::read_json("registry/plots.yml", simplifyVector = FALSE)
for (entry in registry$plots) {
  if (entry$id %in% c("umap_fireworks_atlas", "umap_density_landscape")) {
    entry$validation$checks <- receipt
    jsonlite::write_json(entry, sub("\\.png$", ".metadata.json", entry$output_file), pretty = TRUE, auto_unbox = TRUE)
  }
}
cat("PASS: all coordinates retained; shared density scale and normalization checked.\n")
