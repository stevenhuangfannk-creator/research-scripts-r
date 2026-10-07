# Shared original theme. Font, physical size and export settings are explicit.
theme_research <- function(base_size = 9, base_family = "Arial") {
  ggplot2::theme_classic(base_size = base_size, base_family = base_family) +
    ggplot2::theme(axis.line = ggplot2::element_line(linewidth = 0.35),
      axis.ticks = ggplot2::element_line(linewidth = 0.35),
      legend.position = "right", legend.key.size = grid::unit(3.5, "mm"),
      panel.spacing = grid::unit(3, "mm"),
      plot.title = ggplot2::element_text(face = "bold", size = base_size + 1),
      plot.subtitle = ggplot2::element_text(size = base_size - 1),
      plot.caption = ggplot2::element_text(size = max(6, base_size - 2), hjust = 0))
}
theme_research_clean <- function(...) theme_research(...) + ggplot2::theme(axis.line = ggplot2::element_blank())
theme_research_network <- function(...) theme_research(...) +
  ggplot2::theme(axis.title = ggplot2::element_blank(), axis.text = ggplot2::element_blank(),
                 axis.ticks = ggplot2::element_blank(), axis.line = ggplot2::element_blank())
theme_research_heatmap <- function(...) theme_research_clean(...) +
  ggplot2::theme(axis.ticks = ggplot2::element_blank())
save_research_plot <- function(plot, prefix, width_mm = 160, height_mm = 110, dpi = 400) {
  dir.create(dirname(prefix), recursive = TRUE, showWarnings = FALSE)
  ggplot2::ggsave(paste0(prefix, ".png"), plot, device = ragg::agg_png,
                   width = width_mm, height = height_mm, units = "mm", dpi = dpi, bg = "white")
  ggplot2::ggsave(paste0(prefix, ".pdf"), plot, device = grDevices::cairo_pdf,
                   width = width_mm, height = height_mm, units = "mm", bg = "white")
}
