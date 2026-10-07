plot_marker_dot <- function(data) {
  stopifnot(all(c("gene", "group", "average", "percent") %in% names(data)), all(data$percent >= 0 & data$percent <= 100))
  ggplot2::ggplot(data, ggplot2::aes(gene, group, color = average, size = percent)) +
    ggplot2::geom_point() + ggplot2::scale_color_viridis_c() +
    ggplot2::scale_size_area(max_size = 6, limits = c(0, 100)) +
    ggplot2::labs(x = NULL, y = NULL, color = "Mean log expression", size = "% expressing") +
    theme_research() + ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 45, hjust = 1))
}
