# Original base-grid vector primitives. No downloaded journal or BioRender icon.
cell_grob <- function(label, color = "#56B4E9", type = "circle") {
  outline <- if (type == "fibroblast") grid::polygonGrob(x = c(0.1, 0.4, 0.9, 0.6), y = c(0.2, 0.65, 0.8, 0.35),
                 gp = grid::gpar(fill = color, col = "#333333", lwd = 0.8)) else
    grid::circleGrob(r = 0.32, gp = grid::gpar(fill = color, col = "#333333", lwd = 0.8))
  grid::grobTree(outline, grid::circleGrob(r = 0.11, gp = grid::gpar(fill = "white", col = "#333333", lwd = 0.7)),
                  grid::textGrob(label, y = 0.06, gp = grid::gpar(fontsize = 9)))
}
arrow_grob <- function(x0, y0, x1, y1, color = "#333333") {
  grid::segmentsGrob(x0, y0, x1, y1, arrow = grid::arrow(length = grid::unit(2, "mm")), gp = grid::gpar(col = color, lwd = 1))
}
pathway_node_grob <- function(label, color = "#E6EEF4") {
  grid::grobTree(grid::roundrectGrob(width = 0.9, height = 0.65, r = grid::unit(2, "mm"),
                          gp = grid::gpar(fill = color, col = "#333333", lwd = 0.8)),
                grid::textGrob(label, gp = grid::gpar(fontsize = 9)))
}
vessel_grob <- function() grid::grobTree(
  grid::roundrectGrob(width = 0.85, height = 0.3, gp = grid::gpar(fill = "#FBE7DF", col = "#D55E00")),
  grid::textGrob("Vessel", gp = grid::gpar(fontsize = 9)))
receptor_ligand_grob <- function() grid::grobTree(
  grid::circleGrob(x = 0.28, y = 0.5, r = 0.09, gp = grid::gpar(fill = "#E69F00")),
  arrow_grob(0.4, 0.5, 0.6, 0.5),
  grid::rectGrob(x = 0.73, y = 0.5, width = 0.16, height = 0.25, gp = grid::gpar(fill = "#0072B2")))
nucleic_acid_grob <- function(kind = "DNA") {
  t <- seq(0.05, 0.95, length.out = 100)
  a <- 0.5 + 0.15 * sin(t * 6 * pi)
  lines <- list(grid::linesGrob(t, a, gp = grid::gpar(col = "#0072B2", lwd = 2)))
  if (kind == "DNA") lines[[2]] <- grid::linesGrob(t, 1 - a, gp = grid::gpar(col = "#D55E00", lwd = 2))
  do.call(grid::grobTree, c(lines, list(grid::textGrob(kind, y = 0.1, gp = grid::gpar(fontsize = 9)))))
}
cytokine_grob <- function() grid::grobTree(grid::circleGrob(r = 0.13, gp = grid::gpar(fill = "#E69F00")),
                                         grid::textGrob("Cytokine", y = 0.1, gp = grid::gpar(fontsize = 9)))
