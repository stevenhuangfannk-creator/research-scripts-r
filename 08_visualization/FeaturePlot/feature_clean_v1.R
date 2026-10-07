plot_feature_clean <- function(data, title) {
  stopifnot(all(c("x", "y", "expression") %in% names(data)), all(is.finite(data$expression)))
  ggplot2::ggplot(data, ggplot2::aes(x, y, color = expression)) +
    ggplot2::geom_point(size = 0.8) + ggplot2::scale_color_viridis_c(option = "C") +
    ggplot2::coord_equal() + ggplot2::labs(x = "UMAP 1", y = "UMAP 2", title = title, color = "Log expression") + theme_research()
}
