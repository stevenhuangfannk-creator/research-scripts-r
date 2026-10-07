plot_research_volcano <- function(data, fdr = 0.05, effect = 1) {
  stopifnot(all(c("gene", "log2FC", "padj") %in% names(data)),
            all(is.finite(data$log2FC)), all(is.finite(data$padj)), all(data$padj >= 0 & data$padj <= 1))
  data$direction <- ifelse(data$padj < fdr & abs(data$log2FC) >= effect,
                            ifelse(data$log2FC > 0, "Higher", "Lower"), "Other")
  data$display_p <- pmax(data$padj, .Machine$double.xmin)
  ggplot2::ggplot(data, ggplot2::aes(log2FC, -log10(display_p), color = direction)) +
    ggplot2::geom_point(size = 1.1, alpha = 0.7) +
    ggplot2::geom_vline(xintercept = c(-effect, effect), linetype = 2, linewidth = 0.3) +
    ggplot2::geom_hline(yintercept = -log10(fdr), linetype = 2, linewidth = 0.3) +
    ggplot2::scale_color_manual(values = c(Higher = "#D55E00", Lower = "#0072B2", Other = "#B3B3B3")) +
    ggplot2::labs(x = "Log2 fold change", y = "-log10 adjusted P") + theme_research()
}
