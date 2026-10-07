plot_cox_forest <- function(data) {
  stopifnot(all(c("term", "hr", "lower", "upper") %in% names(data)), all(data$lower > 0))
  ggplot2::ggplot(data, ggplot2::aes(hr, reorder(term, hr))) +
    ggplot2::geom_vline(xintercept = 1, linetype = 2, linewidth = 0.35, color = "#999999") +
    ggplot2::geom_errorbar(ggplot2::aes(xmin = lower, xmax = upper), orientation = "y", width = 0.12) +
    ggplot2::geom_point(color = "#0072B2", size = 2) + ggplot2::scale_x_log10() +
    ggplot2::labs(x = "Hazard ratio (95% CI)", y = NULL) + theme_research()
}
