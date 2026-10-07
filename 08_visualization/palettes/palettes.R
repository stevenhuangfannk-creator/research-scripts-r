source("scripts/read_registry.R")
research_palette <- function(id = "okabe_ito", n = 8L) {
  palettes <- read_registry("registry/palettes.yml")$palettes
  hit <- Filter(function(x) identical(x$id, id), palettes)
  if (length(hit) != 1L) stop("Unknown palette ID")
  colors <- unlist(hit[[1]]$hex_colors)
  if (hit[[1]]$type == "categorical" && n > length(colors)) stop("Palette capacity exceeded; use facets or another encoding")
  if (hit[[1]]$type == "categorical") colors[seq_len(n)] else grDevices::colorRampPalette(colors)(n)
}
celltype_palette <- function(labels) {
  colors <- unlist(read_registry("registry/celltype_colors.yml")$colors)
  if (any(!labels %in% names(colors))) stop("Register new cell types explicitly before plotting")
  colors[labels]
}
