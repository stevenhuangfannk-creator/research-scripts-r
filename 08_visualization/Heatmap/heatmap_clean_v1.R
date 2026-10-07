plot_research_heatmap <- function(data, diverging = FALSE, title = NULL) {
  stopifnot(all(c("x", "y", "value") %in% names(data)), all(is.finite(data$value)))
  p <- ggplot2::ggplot(data, ggplot2::aes(x, y, fill = value)) + ggplot2::geom_tile() +
    ggplot2::labs(x = NULL, y = NULL, title = title) + theme_research_heatmap() +
    ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 45, hjust = 1))
  if (diverging) p + ggplot2::scale_fill_gradient2(low = "#2166AC", mid = "white", high = "#B2182B", midpoint = 0)
  else p + ggplot2::scale_fill_viridis_c()
}
