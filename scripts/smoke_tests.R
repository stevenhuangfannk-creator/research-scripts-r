args <- commandArgs(trailingOnly = TRUE)
evidence <- "docs/validation"
dir.create(evidence, recursive = TRUE, showWarnings = FALSE)
dir.create("results/smoke", recursive = TRUE, showWarnings = FALSE)
results <- list()
check <- function(id, dataset, scope, fun) {
  started <- proc.time()[["elapsed"]]
  notes <- character()
  results[[id]] <<- tryCatch({
    withCallingHandlers(fun(), warning = function(w) {
      notes <<- c(notes, conditionMessage(w))
      invokeRestart("muffleWarning")
    })
    list(status = "PASS", dataset = dataset, scope = scope, date = "2026-10-07",
         elapsed_seconds = round(proc.time()[["elapsed"]] - started, 2),
         warning_count = length(notes), warnings = unique(notes))
  }, error = function(e) list(status = "FAIL", dataset = dataset, scope = scope,
                             date = "2026-10-07", error = conditionMessage(e)))
  cat(id, results[[id]]$status, results[[id]]$error, "\n")
}
packages <- c("Seurat", "SeuratObject", "Matrix", "ggplot2", "patchwork", "ragg", "svglite",
              "harmony", "CellChat", "monocle3", "scDblFinder", "celda", "clusterProfiler",
              "fgsea", "GSVA", "UCell", "AUCell", "survival", "glmnet", "randomForest", "pROC", "yaml")
status <- do.call(rbind, lapply(packages, function(p) {
  error <- NA_character_
  loaded <- tryCatch({ loadNamespace(p); TRUE }, error = function(e) { error <<- conditionMessage(e); FALSE })
  version <- if (p %in% rownames(installed.packages())) as.character(packageVersion(p)) else NA_character_
  data.frame(package = p, version = version, loaded = loaded, error = error)
}))
write.table(status, file.path(evidence, "package_status.tsv"), sep = "\t", quote = FALSE, row.names = FALSE, na = '""')
suppressPackageStartupMessages(library(Seurat))
data("pbmc_small", package = "SeuratObject")
raw <- SeuratObject::GetAssayData(pbmc_small, assay = "RNA", layer = "counts")
input <- list(counts = raw, metadata = pbmc_small[[]])
cfg <- list(project = "pbmc_small_smoke")
obj <- NULL
check("seurat_ingestion", "Seurat::pbmc_small (230 genes, 80 cells)", "Counts/metadata alignment and counts preservation only", function() {
  source("01_scrna_core/data_ingestion/scripts/workflow.R")
  obj <<- run_workflow(input, cfg)$object
  stopifnot(all(dim(raw) == dim(obj)), identical(colnames(raw), colnames(obj)),
            sum(raw) == sum(SeuratObject::GetAssayData(obj, layer = "counts")))
  shuffled <- input; shuffled$metadata <- input$metadata[rev(rownames(input$metadata)), , drop = FALSE]
  aligned <- run_workflow(shuffled, cfg)$object
  stopifnot(identical(rownames(aligned[[]]), colnames(raw)))
})
check("scrna_qc", "pbmc_small plus explicit three-gene arithmetic fixture", "pbmc_small lacks mitochondrial/ribosomal genes; audit/filter and exact arithmetic guards only", function() {
  source("01_scrna_core/quality_control/scripts/workflow.R")
  q <- list(mt_pattern = "^MT-", ribo_pattern = "^RP[SL]", filter = TRUE,
            thresholds = list(min_features = 0, max_features = Inf, min_counts = 0, max_counts = Inf, max_mt = 100))
  z <- suppressWarnings(run_workflow(obj, q))
  stopifnot(nrow(z$tables$qc) == 80, ncol(z$object) == 80)
  fixture <- matrix(c(2, 3, 5, 0, 4, 6), nrow = 3, dimnames = list(c("MT-A", "RPL1", "GENE"), c("a", "b")))
  mini <- Seurat::CreateSeuratObject(fixture, min.cells = 0, min.features = 0)
  q$thresholds$max_mt <- 10
  z <- run_workflow(mini, q)
  stopifnot(all(z$tables$qc$percent.mt == c(20, 0)), all(z$tables$qc$percent.ribo == c(30, 40)),
            nrow(z$tables$qc) == 2, identical(colnames(z$object), "b"))
})
check("lognormalize", "Seurat::pbmc_small", "LogNormalize branch; preserves counts and creates finite RNA data layer", function() {
  source("01_scrna_core/normalization/lognormalize/scripts/workflow.R")
  obj <<- run_workflow(obj, list(scale_factor = 10000))$object
  stopifnot(all(is.finite(SeuratObject::GetAssayData(obj, layer = "data"))), sum(SeuratObject::GetAssayData(obj, layer = "counts")) == sum(raw))
})
check("seurat_clustering", "Seurat::pbmc_small", "PCA/neighbors/clustering/UMAP on all 80 cells; not full-atlas robustness", function() {
  source("01_scrna_core/clustering/scripts/workflow.R")
  config <- list(seed = 42, nfeatures = 100, npcs = 10, resolution = 0.8, n_neighbors = 15)
  obj <<- run_workflow(obj, config)$object
  stopifnot(nrow(Seurat::Embeddings(obj, "umap")) == 80, all(is.finite(Seurat::Embeddings(obj, "umap"))), !anyNA(obj$seurat_clusters))
  saveRDS(obj, "results/smoke/pbmc_clustered.rds")
})
check("hierarchical_annotation", "Seurat::pbmc_small", "Label writeback and Unknown fallback; biological annotations are not validated", function() {
  source("01_scrna_core/annotation/scripts/workflow.R")
  clusters <- unique(as.character(obj$seurat_clusters))
  labels <- setNames(paste("Cluster", clusters), clusters)
  obj <<- run_workflow(obj, list(cluster_column = "seurat_clusters", labels = list(celltype_l1 = as.list(labels)),
                               evidence = "Numerical demo labels only; not biological annotation"))$object
  stopifnot(identical(unname(obj$celltype_l1), unname(labels[as.character(obj$seurat_clusters)])))
  partial <- list(cluster_column = "seurat_clusters", labels = list(celltype_l2 = as.list(labels[1])),
                  evidence = "Partial numerical mapping regression fixture")
  z <- run_workflow(obj, partial)$object
  stopifnot(all(z$celltype_l2[as.character(obj$seurat_clusters) != clusters[1]] == "Unknown"))
  invalid <- partial; invalid$labels <- "mandatory named maps"
  stopifnot(inherits(try(run_workflow(obj, invalid), silent = TRUE), "try-error"))
})
check("cell_markers", "Seurat::pbmc_small", "Exploratory cluster-marker table; no sample-level treatment inference", function() {
  source("02_differential_analysis/differential_expression/scripts/workflow.R")
  z <- run_workflow(obj, list(group_column = "seurat_clusters", only_positive = TRUE, min_pct = 0.1, logfc_threshold = 0.25))
  stopifnot(nrow(z$tables$markers) > 0, "gene" %in% names(z$tables$markers))
  write.csv(z$tables$markers, "results/smoke/markers.csv", row.names = FALSE)
})
check("pseudobulk", "Seurat::pbmc_small (one original sample)", "Raw-count summation/count conservation only; replicated condition testing is unvalidated", function() {
  source("02_differential_analysis/pseudobulk/scripts/workflow.R")
  z <- run_workflow(obj, list(sample_column = "orig.ident", celltype_column = "celltype_l1"))
  stopifnot(sum(z$object) == sum(raw), nrow(z$tables$library_sizes) > 0)
  single <- obj
  single$single_group <- "All cells"
  one <- run_workflow(single, list(sample_column = "orig.ident", celltype_column = "single_group"))
  stopifnot(ncol(one$object) == 1L, sum(one$object) == sum(raw), nrow(one$tables$library_sizes) == 1L)
})
check("registry_unicode", "UTF-8 parser regression fixture", "Registry Unicode preserved under Windows C locale", function() {
  source("scripts/read_registry.R")
  tmp <- tempfile(fileext = ".yml")
  writeLines('id: "sender\u2192receiver"', tmp, useBytes = TRUE)
  stopifnot(identical(read_registry(tmp)$id, "sender\u2192receiver"))
  unlink(tmp)
})
check("correlation", "datasets::iris (150 observed flowers)", "Pearson/Spearman tests, BH adjustment and missing/constant-input regression cases; pooled species are confounded", function() {
  source("07_bulk_clinical_ml/correlation/scripts/workflow.R")
  cfg <- list(variables = names(iris)[1:4], method = "pearson", missing = "error")
  z <- run_workflow(iris, cfg)$tables$correlations
  stopifnot(nrow(z) == 6, all(z$n == 150), all(z$p_adjust >= z$p))
  missing <- iris; missing$Sepal.Length[1] <- NA
  error <- try(run_workflow(missing, cfg), silent = TRUE)
  stopifnot(inherits(error, "try-error"))
  cfg$missing <- "pairwise"; cfg$method <- "spearman"
  z <- run_workflow(missing, cfg)$tables$correlations
  stopifnot(sum(z$excluded) == 3, all(is.na(z$ci_low)))
  constant <- iris; constant$Sepal.Length <- 1
  stopifnot(inherits(try(run_workflow(constant, cfg), silent = TRUE), "try-error"))
})
lung <- survival::lung
lung$event <- as.integer(lung$status == 2)
check("survival_km", "survival::lung (228 public clinical records)", "Right-censored KM curve/CI table with explicit 0/1 event mapping; no new clinical interpretation", function() {
  source("07_bulk_clinical_ml/survival/scripts/workflow.R")
  z <- run_workflow(lung, list(time_column = "time", event_column = "event", group_column = "sex"))
  stopifnot(inherits(z$object, "survfit"), nrow(z$tables$km) > 0, all(z$tables$km$survival >= 0 & z$tables$km$survival <= 1))
  saveRDS(z, "results/smoke/km.rds")
})
check("cox", "survival::lung (age and sex covariates)", "Cox HR/CI and proportional-hazards diagnostic output only; no predictive or causal certification", function() {
  source("07_bulk_clinical_ml/Cox/scripts/workflow.R")
  z <- run_workflow(lung, list(time_column = "time", event_column = "event", covariates = c("age", "sex")))
  stopifnot(nrow(z$tables$cox) == 2, nrow(z$tables$proportional_hazards) == 3)
  saveRDS(z, "results/smoke/cox.rds")
})
blocked <- list(cellchat = "CellChat", cellchat_compare = "CellChat", monocle3 = "monocle3", monocle3_dynamics = "monocle3",
                scdblfinder = "scDblFinder", decontx = "celda", go_kegg_ora = "clusterProfiler", fgsea = "fgsea")
for (id in names(blocked)) {
  package <- blocked[[id]]
  row <- status[status$package == package, ]
  results[[id]] <- list(status = if (isTRUE(row$loaded)) "UNVALIDATED" else "BLOCKED",
                        dataset = NULL, scope = "Workflow not executed; required namespace/data unavailable",
                        date = NULL, blocker = if (isTRUE(row$loaded)) "Representative input not supplied" else row$error)
}
writeLines(capture.output(sessionInfo()), file.path(evidence, "sessionInfo.txt"))
jsonlite::write_json(results, file.path(evidence, "method_results.json"), auto_unbox = TRUE, pretty = TRUE, null = "null")
stopifnot(!any(vapply(results, function(x) x$status == "FAIL", logical(1))))
