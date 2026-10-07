plot_research_violin <- function(data, colors, ylab = "Value") {
  stopifnot(all(c("group", "value") %in% names(data)), all(is.finite(data$value)))
  ggplot2::ggplot(data, ggplot2::aes(group, value, fill = group)) +
    ggplot2::geom_violin(scale = "width", trim = TRUE, linewidth = 0.3, alpha = 0.65) +
    ggplot2::geom_boxplot(width = 0.13, outlier.shape = NA, linewidth = 0.3, fill = "white") +
    ggplot2::scale_fill_manual(values = colors) + ggplot2::guides(fill = "none") +
    ggplot2::labs(x = NULL, y = ylab) + theme_research()
}
