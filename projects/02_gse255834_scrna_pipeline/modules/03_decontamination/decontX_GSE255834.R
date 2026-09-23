suppressPackageStartupMessages({
  library(Seurat)
  library(Matrix)
  library(DropletUtils)
  library(SingleCellExperiment)
  library(future)
  library(future.apply)
  library(ggplot2)
  library(patchwork)
})

options(stringsAsFactors = FALSE)
options(future.globals.maxSize = 20 * 1024^3)
Sys.setenv(OMP_NUM_THREADS = "1", OPENBLAS_NUM_THREADS = "1",
           MKL_NUM_THREADS = "1", BLAS_NUM_THREADS = "1")

root <- "C:/Users/zhaozize/Desktop/APAP"
input_dir <- file.path(root, "raw_data/scRNA/GSE255834_RAW")
out_dir <- file.path(root, "results/GSE255834_seurat")
stage_dir <- file.path(out_dir, "decontX_sample_outputs")
dir.create(stage_dir, recursive = TRUE, showWarnings = FALSE)

strict_path <- file.path(out_dir, "GSE255834_seurat_strict_qc_70w.rds")
strict <- readRDS(strict_path)
meta <- strict@meta.data
sample_names <- sort(unique(as.character(meta$sample)))
raw_files <- list.files(input_dir, pattern = "\\.h5$", full.names = TRUE)
file_sample <- sub("_raw_feature_bc_matrix\\.h5$", "", basename(raw_files))
file_sample <- sub("^GSM[0-9]+_", "", file_sample)
names(raw_files) <- file_sample
stopifnot(setequal(sample_names, names(raw_files)), ncol(strict) == 27870L)

raw_counts <- GetAssayData(strict, assay = "RNA", layer = "counts")
for (sample_id in sample_names) {
  cells <- rownames(meta)[as.character(meta$sample) == sample_id]
  cell_counts <- raw_counts[, cells, drop = FALSE]
  cell_meta <- meta[cells, , drop = FALSE]
  job <- list(
    sample = sample_id,
    raw_file = unname(raw_files[[sample_id]]),
    cell_rds = file.path(stage_dir, paste0(sample_id, "_strict_cells.rds")),
    result_rds = file.path(stage_dir, paste0(sample_id, "_decontX.rds")),
    cells = cells,
    clusters = as.character(cell_meta$seurat_clusters),
    knee_total = median(as.numeric(cell_meta$barcode_knee), na.rm = TRUE),
    seed = 4200L + match(sample_id, sample_names)
  )
  saveRDS(list(counts = cell_counts, cells = cells, clusters = job$clusters),
          job$cell_rds, compress = FALSE)
  saveRDS(job, file.path(stage_dir, paste0(sample_id, "_job.rds")), compress = FALSE)
  rm(cell_counts, cell_meta, job)
  gc(verbose = FALSE)
}
rm(raw_counts, strict, meta)
gc(verbose = FALSE)

run_decontx_sample <- function(job_file) {
  job <- readRDS(job_file)
  done_path <- job$result_rds
  if (file.exists(done_path)) {
    cached <- readRDS(done_path)
    if (identical(cached$cells, job$cells) && length(cached$contamination) == length(job$cells)) {
      return(data.frame(sample = job$sample, status = "cached", cells = length(job$cells),
                        background = cached$background_n, median_contamination = median(cached$contamination),
                        q90_contamination = as.numeric(quantile(cached$contamination, .9)),
                        pct_contamination_ge_0.2 = mean(cached$contamination >= .2) * 100))
    }
  }

  strict_data <- readRDS(job$cell_rds)
  cell_mat <- strict_data$counts
  rm(strict_data)
  gc(verbose = FALSE)

  raw_sce <- DropletUtils::read10xCounts(job$raw_file, col.names = TRUE)
  raw_mat <- SummarizedExperiment::assay(raw_sce, "counts")
  barcodes <- as.character(SummarizedExperiment::colData(raw_sce)$Barcode)
  symbols <- as.character(SummarizedExperiment::rowData(raw_sce)$Symbol)
  if (is.null(symbols)) symbols <- rep(NA_character_, nrow(raw_mat))
  missing_symbols <- is.na(symbols) | symbols == ""
  symbols[missing_symbols] <- rownames(raw_mat)[missing_symbols]
  rownames(raw_mat) <- make.unique(symbols)
  rm(symbols, missing_symbols)

  target_barcodes <- sub(paste0("^", job$sample, "_"), "", job$cells)
  target_idx <- match(target_barcodes, barcodes)
  if (anyNA(target_idx)) {
    stop(job$sample, ": ", sum(is.na(target_idx)), " strict cells missing from raw H5")
  }
  raw_cell_mat <- raw_mat[, target_idx, drop = FALSE]
  rownames(cell_mat) <- make.unique(rownames(cell_mat))
  if (!identical(rownames(raw_cell_mat), rownames(cell_mat))) {
    raw_cell_mat <- raw_cell_mat[rownames(cell_mat), , drop = FALSE]
  }
  colnames(raw_cell_mat) <- job$cells
  if (!identical(dim(raw_cell_mat), dim(cell_mat)) ||
      !identical(as.numeric(Matrix::colSums(raw_cell_mat)), as.numeric(Matrix::colSums(cell_mat)))) {
    stop(job$sample, ": strict-cell raw counts do not match the saved strict object")
  }

  totals <- Matrix::colSums(raw_mat)
  bg_max <- min(1000, floor(job$knee_total) - 1)
  bg_idx <- which(totals >= 20 & totals <= bg_max)
  if (length(bg_idx) < 1000L) {
    stop(job$sample, ": insufficient low-UMI empty-droplet background (", length(bg_idx), ")")
  }
  set.seed(job$seed)
  if (length(bg_idx) > 20000L) bg_idx <- sample(bg_idx, 20000L)
  bg_mat <- raw_mat[, bg_idx, drop = FALSE]
  colnames(bg_mat) <- paste0("background_", seq_len(ncol(bg_mat)))

  sce_cells <- SingleCellExperiment::SingleCellExperiment(assays = list(counts = cell_mat))
  sce_background <- SingleCellExperiment::SingleCellExperiment(assays = list(counts = bg_mat))
  rm(raw_sce, raw_mat, raw_cell_mat, totals, bg_idx, bg_mat, barcodes, cell_mat)
  gc(verbose = FALSE)

  fit <- celda::decontX(
    sce_cells, z = factor(job$clusters), background = sce_background,
    assayName = "counts", bgAssayName = "counts", maxIter = 500,
    seed = job$seed, verbose = TRUE
  )
  corrected <- SummarizedExperiment::assay(fit, "decontXcounts")
  corrected <- methods::as(round(corrected), "dgCMatrix")
  colnames(corrected) <- job$cells
  cd <- as.data.frame(SummarizedExperiment::colData(fit))
  contamination_col <- grep("contamination", colnames(cd), ignore.case = TRUE, value = TRUE)[1]
  if (is.na(contamination_col)) {
    stop(job$sample, ": DecontX contamination estimate missing; colData has: ",
         paste(colnames(cd), collapse = ", "))
  }
  contamination <- as.numeric(cd[[contamination_col]])
  names(contamination) <- job$cells
  saveRDS(list(counts = corrected, cells = job$cells, contamination = contamination,
               background_n = ncol(sce_background), background_max_umi = bg_max,
               input_n = length(job$cells)), done_path, compress = FALSE)
  data.frame(sample = job$sample, status = "completed", cells = length(job$cells),
             background = ncol(sce_background), median_contamination = median(contamination),
             q90_contamination = as.numeric(quantile(contamination, .9)),
             pct_contamination_ge_0.2 = mean(contamination >= .2) * 100)
}

job_files <- file.path(stage_dir, paste0(sample_names, "_job.rds"))
workers <- min(8L, length(job_files))
future::plan(future::multisession, workers = workers)
status <- future.apply::future_lapply(job_files, run_decontx_sample,
                                      future.seed = TRUE, future.scheduling = 1)
future::plan(future::sequential)
status <- do.call(rbind, status)
write.csv(status, file.path(out_dir, "decontX_sample_summary.csv"), row.names = FALSE)

sample_results <- lapply(sample_names, function(s) readRDS(file.path(stage_dir, paste0(s, "_decontX.rds"))))
corrected_counts <- do.call(cbind, lapply(sample_results, `[[`, "counts"))
strict_meta <- readRDS(strict_path)@meta.data
strict_order <- rownames(strict_meta)
if (!setequal(colnames(corrected_counts), strict_order)) stop("Corrected cell set differs from strict-QC cells")
corrected_counts <- corrected_counts[, strict_order, drop = FALSE]

contamination <- unlist(lapply(sample_results, `[[`, "contamination"))
strict_meta <- strict_meta[strict_order, , drop = FALSE]
strict_meta$decontX_contamination <- contamination[strict_order]
zero_count_cells <- colnames(corrected_counts)[Matrix::colSums(corrected_counts) == 0]
if (length(zero_count_cells)) {
  write.csv(data.frame(cell = zero_count_cells, reason = "all counts rounded to zero after DecontX"),
            file.path(out_dir, "decontX_removed_zero_count_cells.csv"), row.names = FALSE)
  corrected_counts <- corrected_counts[, setdiff(colnames(corrected_counts), zero_count_cells), drop = FALSE]
  strict_meta <- strict_meta[colnames(corrected_counts), , drop = FALSE]
  message("Removed zero-count cells after correction: ", length(zero_count_cells))
}
strict_meta$nCount_RNA_pre_decontX <- strict_meta$nCount_RNA
strict_meta$nFeature_RNA_pre_decontX <- strict_meta$nFeature_RNA
strict_meta$seurat_clusters_pre_decontX <- as.character(strict_meta$seurat_clusters)
strict_meta$nCount_RNA <- NULL
strict_meta$nFeature_RNA <- NULL
strict_meta$seurat_clusters <- NULL

obj <- CreateSeuratObject(counts = corrected_counts, meta.data = strict_meta,
                          project = "GSE255834", min.cells = 0, min.features = 0)
obj$percent.mt_decontX <- PercentageFeatureSet(obj, pattern = "^mt-")
rm(corrected_counts, sample_results, contamination, strict_meta)
gc(verbose = FALSE)

# Sample-level parallelism is safe here; the original object is ~0.4 GB on disk,
# while only these eight independent workers are exposed to the count matrix.
future::plan(future::multisession, workers = workers)
obj <- NormalizeData(obj, normalization.method = "LogNormalize", scale.factor = 10000, verbose = FALSE)
obj <- FindVariableFeatures(obj, selection.method = "vst", nfeatures = 3000, verbose = FALSE)
obj <- ScaleData(obj, features = VariableFeatures(obj), verbose = FALSE)
obj <- RunPCA(obj, features = VariableFeatures(obj), npcs = 50, verbose = FALSE)
obj <- FindNeighbors(obj, dims = 1:30, verbose = FALSE)
obj <- FindClusters(obj, resolution = 0.5, verbose = FALSE)
future::plan(future::sequential)

# Let uwot use all available logical CPUs without nested future workers.
umap_threads <- min(70L, parallel::detectCores(logical = TRUE))
pca <- Embeddings(obj, reduction = "pca")[, 1:30, drop = FALSE]
um <- uwot::umap(X = pca, n_neighbors = 30, n_components = 2, metric = "cosine",
                 min_dist = 0.3, n_threads = umap_threads, init = "spectral",
                 n_epochs = NULL, ret_model = FALSE, verbose = FALSE, seed = 42)
colnames(um) <- c("UMAP_1", "UMAP_2")
rownames(um) <- rownames(pca)
obj[["umap"]] <- CreateDimReducObject(embeddings = um, key = "UMAP_", assay = "RNA", global = TRUE)

out_rds <- file.path(out_dir, "GSE255834_seurat_strict_qc_decontX.rds")
saveRDS(obj, out_rds, compress = "gzip")

p_cluster <- DimPlot(obj, reduction = "umap", group.by = "seurat_clusters", label = TRUE,
                     repel = TRUE, raster = TRUE, pt.size = 0.12, shuffle = TRUE) +
  ggtitle("Strict-QC singlets after ambient RNA correction")
p_cell <- FeaturePlot(obj, features = "decontX_contamination", reduction = "umap", raster = TRUE) +
  ggtitle("Estimated ambient RNA contamination")
ggsave(file.path(out_dir, "GSE255834_strict_QC_decontX_UMAP.png"), p_cluster | p_cell,
       width = 14, height = 7, dpi = 300, bg = "white")
ggsave(file.path(out_dir, "GSE255834_strict_QC_decontX_UMAP.pdf"), p_cluster | p_cell,
       width = 14, height = 7, bg = "white")
writeLines(capture.output(sessionInfo()), file.path(out_dir, "sessionInfo_decontX.txt"))
writeLines(c(paste0("sample_workers=", workers), paste0("umap_threads=", umap_threads),
             paste0("cells=", ncol(obj)), paste0("clusters=", length(unique(as.character(Idents(obj))))),
             "DecontX used up to 20,000 sub-knee low-UMI droplets (20 to min(1000, knee-1) UMIs) per sample as ambient background.",
             "Strict-QC uncorrected object is preserved as the comparator."),
           file.path(out_dir, "decontX_notes.txt"))
message("DONE cells=", ncol(obj), " clusters=", length(unique(as.character(Idents(obj)))),
        " workers=", workers, " UMAP threads=", umap_threads)
