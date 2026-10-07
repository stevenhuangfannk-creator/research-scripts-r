run_workflow <- function(input, config) {
  stopifnot(all(c(config$time_column, config$event_column, config$group_column) %in% names(input)))
  d <- data.frame(time = input[[config$time_column]], event = input[[config$event_column]], group = input[[config$group_column]])
  stopifnot(all(is.finite(d$time)), all(d$time >= 0), all(d$event %in% 0:1), !anyNA(d$group))
  fit <- survival::survfit(survival::Surv(time, event) ~ group, data = d)
  s <- summary(fit)
  curves <- data.frame(time = s$time, survival = s$surv, lower = s$lower, upper = s$upper,
                        n_risk = s$n.risk, events = s$n.event, strata = as.character(s$strata))
  list(object = fit, tables = list(km = curves, groups = as.data.frame(table(d$group))))
}
