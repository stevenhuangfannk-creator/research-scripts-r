# Z is a KDE probability density on supplied 2D UMAP, not UMAP 3 or expression.
compute_umap_density_landscape <- function(data, bandwidth = NULL, grid_n = 100L) {
  stopifnot(all(c("x", "y", "condition") %in% names(data)), nrow(data) > 1,
            is.numeric(data$x), is.numeric(data$y), all(is.finite(data$x)), all(is.finite(data$y)),
            !anyNA(data$condition), all(nzchar(as.character(data$condition))), grid_n >= 30)
  if (is.null(bandwidth)) bandwidth <- c(stats::bw.nrd0(data$x), stats::bw.nrd0(data$y))
  stopifnot(length(bandwidth) == 2L, all(is.finite(bandwidth)), all(bandwidth > 0))
  # MASS kde2d divides h by 4; compensate to expose actual Gaussian SDs.
  limits <- c(range(data$x) + c(-3, 3) * bandwidth[1], range(data$y) + c(-3, 3) * bandwidth[2])
  surfaces <- lapply(split(data, as.character(data$condition)), function(group) {
    if (nrow(group) < 2L) stop("Each displayed condition needs at least two cells")
    fit <- MASS::kde2d(group$x, group$y, h = 4 * bandwidth, n = grid_n, lims = limits)
    area <- diff(fit$x)[1] * diff(fit$y)[1]
    fit$z <- fit$z / (sum(fit$z) * area)
    list(x = fit$x, y = fit$y, z = fit$z, cells = nrow(group), integral = sum(fit$z) * area)
  })
  list(surfaces = surfaces, bandwidth = bandwidth, limits = limits, grid_n = grid_n,
       density_max = max(vapply(surfaces, function(s) max(s$z), numeric(1))), excluded_cells = 0)
}

draw_umap_density_landscape <- function(landscape) {
  old <- graphics::par(no.readonly = TRUE)
  on.exit(graphics::par(old))
  count <- length(landscape$surfaces)
  graphics::par(mfrow = c(1, count), mar = c(2, 1, 3, 1), oma = c(3, 0, 2, 0), family = "Arial")
  ramp <- viridisLite::viridis(100)
  for (name in names(landscape$surfaces)) {
    s <- landscape$surfaces[[name]]
    z <- s$z
    face <- (z[-1, -1] + z[-nrow(z), -1] + z[-1, -ncol(z)] + z[-nrow(z), -ncol(z)]) / 4
    graphics::persp(s$x, s$y, s$z, theta = 35, phi = 28, expand = 0.8,
      zlim = c(0, landscape$density_max), col = ramp[pmax(1, ceiling(face / landscape$density_max * 100))],
      border = NA, shade = 0.25, ticktype = "detailed", nticks = 3, cex.axis = 0.7,
      cex.lab = 0.8, xlab = "UMAP 1", ylab = "UMAP 2", zlab = "",
      main = sprintf("%s (n = %s)", name, format(s$cells, big.mark = ",")), cex.main = 0.95)
  }
  graphics::mtext("Shared 2D UMAP: density landscapes", outer = TRUE, side = 3, line = 0.4, font = 2, cex = 1)
  graphics::mtext("Z: probability density. Same coordinates, bandwidth and Z scale.\nUnit integral per surface; one library per condition, descriptive only.",
    outer = TRUE, side = 1, line = 0.7, cex = 0.72)
}
