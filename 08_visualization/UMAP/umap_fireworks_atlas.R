# Parallel atlas display; coordinates and labels are never changed.
plot_umap_fireworks_atlas <- function(data, colors, point_size = 0.18, title = "Atlas UMAP") {
  stopifnot(all(c("x", "y", "group") %in% names(data)), nrow(data) > 0,
            is.numeric(data$x), is.numeric(data$y), all(is.finite(data$x)), all(is.finite(data$y)),
            !anyNA(data$group), all(nzchar(as.character(data$group))), point_size > 0)
  if (!all(unique(as.character(data$group)) %in% names(colors))) stop("Incomplete named color mapping")
  labels <- stats::aggregate(cbind(x, y) ~ group, data, stats::median)
  ggplot2::ggplot(data, ggplot2::aes(x, y, colour = group)) +
    ggplot2::geom_point(size = point_size, alpha = 0.85, stroke = 0) +
    ggrepel::geom_text_repel(data = labels, ggplot2::aes(label = group), colour = "#222222",
      size = 2.6, seed = 42, max.overlaps = Inf, box.padding = 0.4, min.segment.length = 0,
      segment.colour = "#888888", segment.size = 0.2, show.legend = FALSE) +
    ggplot2::scale_colour_manual(values = colors) + ggplot2::coord_equal() +
    ggplot2::labs(title = title, x = "UMAP 1", y = "UMAP 2", colour = "Provisional broad identity") +
    ggplot2::theme_classic(base_size = 10, base_family = "Arial") +
    ggplot2::theme(axis.text = ggplot2::element_blank(), axis.ticks = ggplot2::element_blank(),
      legend.title = ggplot2::element_text(size = 8), legend.text = ggplot2::element_text(size = 7),
      plot.title = ggplot2::element_text(face = "bold")) +
    ggplot2::guides(colour = ggplot2::guide_legend(override.aes = list(size = 2, alpha = 1)))
}
