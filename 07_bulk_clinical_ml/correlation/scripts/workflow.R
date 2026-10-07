run_workflow <- function(input, config) {
  stopifnot(is.data.frame(input), all(config$variables %in% names(input)),
            config$method %in% c("pearson", "spearman"))
  x <- input[, config$variables, drop = FALSE]
  stopifnot(all(vapply(x, is.numeric, logical(1))))
  pairs <- combn(names(x), 2, simplify = FALSE)
  result <- do.call(rbind, lapply(pairs, function(pair) {
    keep <- is.finite(x[[pair[1]]]) & is.finite(x[[pair[2]]])
    if (!all(keep) && !identical(config$missing, "pairwise")) stop("Missing/non-finite values: choose explicit pairwise policy")
    a <- x[[pair[1]]][keep]; b <- x[[pair[2]]][keep]
    if (length(a) < 4L || sd(a) == 0 || sd(b) == 0) stop("Correlation needs >=4 complete, variable observations")
    test <- cor.test(a, b, method = config$method, exact = FALSE)
    ci <- if (is.null(test$conf.int)) c(NA_real_, NA_real_) else test$conf.int
    data.frame(x = pair[1], y = pair[2], n = length(a), excluded = sum(!keep),
               r = unname(test$estimate), p = test$p.value, ci_low = ci[1], ci_high = ci[2])
  }))
  result$p_adjust <- p.adjust(result$p, method = "BH")
  list(object = NULL, tables = list(correlations = result))
}
