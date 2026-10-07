plot_composition <- function(data, colors) {
  stopifnot(all(c("sample", "celltype", "count") %in% names(data)), all(data$count >= 0))
  totals <- ave(data$count, data$sample, FUN = sum)
  if (any(totals == 0)) stop("Zero-cell sample")
  data$proportion <- data$count / totals
  ggplot2::ggplot(data, ggplot2::aes(sample, proportion, fill = celltype)) +
    ggplot2::geom_col(width = 0.72) + ggplot2::scale_fill_manual(values = colors) +
    ggplot2::scale_y_continuous(labels = scales::label_percent()) +
    ggplot2::labs(x = NULL, y = "Fraction of captured cells") + theme_research()
}
