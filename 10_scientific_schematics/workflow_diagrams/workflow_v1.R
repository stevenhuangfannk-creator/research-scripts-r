source("10_scientific_schematics/reusable_components/components.R")
draw_scrna_workflow <- function() {
  grid::grid.newpage()
  grid::grid.text("Sample-to-analysis workflow", y = 0.92, gp = grid::gpar(fontsize = 13, fontface = "bold"))
  stages <- c("Sample", "Dissociation", "scRNA-seq", "QC", "Clustering", "Annotation")
  xs <- seq(0.1, 0.9, length.out = length(stages))
  for (i in seq_along(stages)) {
    grid::pushViewport(grid::viewport(x = xs[i], y = 0.52, width = 0.15, height = 0.35))
    grid::grid.draw(pathway_node_grob(stages[i]))
    grid::popViewport()
    if (i < length(stages)) grid::grid.draw(arrow_grob(xs[i] + 0.068, 0.52, xs[i + 1] - 0.068, 0.52))
  }
  grid::grid.text("Editable original diagram | workflow template", y = 0.14, gp = grid::gpar(fontsize = 8, col = "#555555"))
}
