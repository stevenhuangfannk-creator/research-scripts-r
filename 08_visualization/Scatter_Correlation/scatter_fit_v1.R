plot_scatter_fit <- function(data, x, y, method = "pearson") {
  stopifnot(all(is.finite(data[[x]])), all(is.finite(data[[y]])))
  test <- stats::cor.test(data[[x]], data[[y]], method = method, exact = FALSE)
  ggplot2::ggplot(data, ggplot2::aes(x = .data[[x]], y = .data[[y]])) +
    ggplot2::geom_point(color = "#0072B2", size = 1.4, alpha = 0.65) +
    ggplot2::geom_smooth(method = "lm", se = TRUE, linewidth = 0.5, color = "#333333", fill = "#D9D9D9") +
    ggplot2::labs(subtitle = sprintf("%s r = %.2f; P = %.2g; n = %d", method, test$estimate, test$p.value, nrow(data)),
                   caption = "Shading: linear-model 95% CI; correlation is not causation.") + theme_research()
}
