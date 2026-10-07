# Input data.frame(x, y, group); caller supplies actual computed UMAP coordinates.
plot_umap_clean <- function(data, colors, title = "UMAP") {
  stopifnot(all(c("x", "y", "group") %in% names(data)), all(is.finite(data$x)), all(is.finite(data$y)))
  if (!all(unique(as.character(data$group)) %in% names(colors))) stop("Incomplete named color mapping")
  ggplot2::ggplot(data, ggplot2::aes(x, y, color = group)) +
    ggplot2::geom_point(size = 0.65, alpha = 0.8) +
    ggplot2::scale_color_manual(values = colors) + ggplot2::coord_equal() +
    ggplot2::labs(x = "UMAP 1", y = "UMAP 2", title = title) + theme_research()
}
