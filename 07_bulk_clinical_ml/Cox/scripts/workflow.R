run_workflow <- function(input, config) {
  fields <- c(config$time_column, config$event_column, config$covariates)
  stopifnot(all(fields %in% names(input)), all(complete.cases(input[, fields, drop = FALSE])),
            all(input[[config$event_column]] %in% 0:1), all(input[[config$time_column]] >= 0))
  formula <- reformulate(config$covariates,
               response = paste0("survival::Surv(`", config$time_column, "`, `", config$event_column, "`)"))
  fit <- survival::coxph(formula, data = input, x = TRUE)
  s <- summary(fit)
  estimates <- data.frame(term = rownames(s$coefficients), s$conf.int, p = s$coefficients[, "Pr(>|z|)"], row.names = NULL)
  ph <- survival::cox.zph(fit)
  list(object = fit, tables = list(cox = estimates,
       proportional_hazards = data.frame(term = rownames(ph$table), ph$table, row.names = NULL)))
}
