# Minimal CLI example; generated public demo data stays in ignored results/.
dir.create("results/demo", recursive = TRUE, showWarnings = FALSE)
write.csv(datasets::iris, "results/demo/iris.csv", row.names = FALSE)
jsonlite::write_json(list(input = "results/demo/iris.csv", output_dir = "results/demo/correlation",
  variables = names(datasets::iris)[1:4], method = "pearson", missing = "error"),
  "results/demo/correlation.yml", auto_unbox = TRUE, pretty = TRUE)
cat("Run: Rscript scripts/run_method.R correlation results/demo/correlation.yml\n")
