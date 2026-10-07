source("10_scientific_schematics/reusable_components/components.R")
draw_mechanism_template <- function() {
  grid::grid.newpage()
  grid::grid.text("Mechanism hypothesis scaffold", y = 0.94, gp = grid::gpar(fontsize = 13, fontface = "bold"))
  labels <- c("Stimulus", "Receptor", "Signaling pathway", "Transcription factor", "Phenotype")
  ys <- seq(0.8, 0.2, length.out = length(labels))
  for (i in seq_along(labels)) {
    grid::pushViewport(grid::viewport(x = 0.5, y = ys[i], width = 0.5, height = 0.13))
    grid::grid.draw(pathway_node_grob(labels[i]))
    grid::popViewport()
    if (i < length(labels)) grid::grid.draw(arrow_grob(0.5, ys[i] - 0.044, 0.5, ys[i + 1] + 0.044))
  }
  grid::grid.text("Populate each arrow with study-specific evidence", y = 0.06, gp = grid::gpar(fontsize = 8, col = "#555555"))
}
