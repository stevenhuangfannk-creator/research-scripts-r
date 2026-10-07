source("10_scientific_schematics/reusable_components/components.R")
draw_cell_interaction <- function() {
  grid::grid.newpage()
  grid::grid.text("Cell interaction hypothesis", y = 0.92, gp = grid::gpar(fontsize = 13, fontface = "bold"))
  for (cell in list(list(x = 0.23, label = "Macrophage", color = "#D55E00", type = "circle"),
                   list(x = 0.77, label = "Fibroblast", color = "#8C6BB1", type = "fibroblast"))) {
    grid::pushViewport(grid::viewport(x = cell$x, y = 0.52, width = 0.25, height = 0.55))
    grid::grid.draw(cell_grob(cell$label, cell$color, cell$type))
    grid::popViewport()
  }
  grid::grid.draw(arrow_grob(0.34, 0.52, 0.65, 0.52))
  grid::grid.text("Ligand to receptor", x = 0.5, y = 0.64, gp = grid::gpar(fontsize = 9))
  grid::grid.text("Template relationship only; no specific mechanism is asserted", y = 0.14, gp = grid::gpar(fontsize = 8, col = "#555555"))
}
