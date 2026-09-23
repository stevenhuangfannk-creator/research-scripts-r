suppressPackageStartupMessages({
  library(Seurat)
  library(DropletUtils)
  library(Matrix)
  library(future)
  library(data.table)
  library(ggplot2)
})

options(stringsAsFactors = FALSE)
options(future.globals.maxSize = 100 * 1024^3)
# The requested 70-thread setting is recorded for provenance. The H5 reader and
# Seurat operations used here do not expose a safe 70-worker backend on Windows;
# keeping the controller sequential avoids duplicating multi-gigabyte sparse
# matrices across 70 R processes.
configured_threads <- 70L
future::plan(sequential)

input_dir <- "C:/Users/zhaozize/Desktop/APAP/raw_data/scRNA/GSE255834_RAW"
output_dir <- "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat"
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

files <- sort(list.files(input_dir, pattern = "\\.h5$", full.names = TRUE))
stopifnot(length(files) == 8L)

parse_sample <- function(x) {
  z <- sub("_raw_feature_bc_matrix\\.h5$", "", basename(x))
  z <- sub("^GSM[0-9]+_", "", z)
  parts <- strsplit(z, "_", fixed = TRUE)[[1]]
  data.frame(
    sample = z,
    condition = ifelse(grepl("^Ctl", z), "Ctl", "APAP"),
    time_h = as.integer(sub(".*?(48|72).*", "\\1", z)),
    tissue = ifelse(grepl("_hep", z), "hep", "npc"),
    stringsAsFactors = FALSE
  )
}

sample_info <- rbindlist(lapply(files, parse_sample), fill = TRUE)
write.csv(sample_info, file.path(output_dir, "sample_metadata.csv"), row.names = FALSE)

safe_quantile <- function(x, p, fallback) {
  q <- as.numeric(quantile(x, p = p, na.rm = TRUE, names = FALSE, type = 8))
  if (!is.finite(q)) fallback else q
}

objects <- list()
qc_rows <- list()

for (i in seq_along(files)) {
  f <- files[[i]]
  meta <- sample_info[i, ]
  message(sprintf("[%d/%d] reading %s", i, length(files), basename(f)))
  sce <- read10xCounts(f, col.names = TRUE)
  mat <- counts(sce)
  br <- barcodeRanks(mat)
  br_meta <- metadata(br)
  knee_rank <- as.numeric(br_meta$knee)
  inflection_rank <- as.numeric(br_meta$inflection)
  br_df <- as.data.frame(br)
  knee_total <- br_df$total[which.min(abs(br_df$rank - knee_rank))]
  inflection_total <- br_df$total[which.min(abs(br_df$rank - inflection_rank))]
  if (!is.finite(knee_total) || knee_total <= 0) knee_total <- max(100, inflection_total)
  totals <- Matrix::colSums(mat)
  keep_barcode <- which(totals >= knee_total)
  if (length(keep_barcode) < 100) {
    keep_barcode <- which(totals >= max(100, inflection_total))
  }
  mat <- mat[, keep_barcode, drop = FALSE]
  symbols <- as.character(rowData(sce)$Symbol)
  symbols[is.na(symbols) | symbols == ""] <- rownames(mat)[is.na(symbols) | symbols == ""]
  rownames(mat) <- make.unique(symbols)
  barcodes <- as.character(colData(sce)$Barcode)[keep_barcode]
  colnames(mat) <- paste(meta$sample, barcodes, sep = "_")
  message(sprintf("  knee rank=%g; knee total=%.1f; retained %d barcodes", knee_rank, knee_total, ncol(mat)))

  obj <- CreateSeuratObject(
    counts = mat,
    project = "GSE255834",
    min.cells = 0,
    min.features = 0
  )
  obj$sample <- meta$sample
  obj$condition <- meta$condition
  obj$time_h <- meta$time_h
  obj$tissue <- meta$tissue
  obj$barcode_knee <- knee_total
  obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern = "^mt-")

  nf <- obj$nFeature_RNA
  nc <- obj$nCount_RNA
  pm <- obj$percent.mt
  thresholds <- c(
    min_features = max(200, floor(safe_quantile(nf, 0.01, 200))),
    max_features = ceiling(safe_quantile(nf, 0.999, max(nf))),
    min_counts = max(500, floor(safe_quantile(nc, 0.01, 500))),
    max_counts = ceiling(safe_quantile(nc, 0.999, max(nc))),
    max_percent_mt = safe_quantile(pm, 0.99, max(pm))
  )
  qc_pass <- nf >= thresholds[["min_features"]] & nf <= thresholds[["max_features"]] &
    nc >= thresholds[["min_counts"]] & nc <= thresholds[["max_counts"]] &
    pm <= thresholds[["max_percent_mt"]]
  obj$qc_pass <- qc_pass
  obj$qc_fail_reason <- ifelse(qc_pass, "pass", paste(
    ifelse(nf < thresholds[["min_features"]], "low_features", ""),
    ifelse(nf > thresholds[["max_features"]], "high_features", ""),
    ifelse(nc < thresholds[["min_counts"]], "low_counts", ""),
    ifelse(nc > thresholds[["max_counts"]], "high_counts", ""),
    ifelse(pm > thresholds[["max_percent_mt"]], "high_mt", ""),
    sep = ";"
  ))
  qc_rows[[i]] <- data.frame(
    sample = meta$sample, condition = meta$condition, time_h = meta$time_h,
    tissue = meta$tissue, input_barcodes = ncol(sce), knee_rank = knee_rank,
    knee_total = knee_total, inflection_rank = inflection_rank,
    inflection_total = inflection_total, knee_barcodes = ncol(obj),
    min_features = thresholds[["min_features"]], max_features = thresholds[["max_features"]],
    min_counts = thresholds[["min_counts"]], max_counts = thresholds[["max_counts"]],
    max_percent_mt = thresholds[["max_percent_mt"]],
    qc_pass = sum(qc_pass), qc_fail = sum(!qc_pass)
  )
  write.csv(qc_rows[[i]], file.path(output_dir, paste0(meta$sample, "_qc_summary.csv")), row.names = FALSE)
  saveRDS(obj, file.path(output_dir, paste0(meta$sample, "_raw_seurat.rds")))
  objects[[meta$sample]] <- subset(obj, subset = qc_pass)
  rm(sce, mat, br, obj)
  gc()
}

qc_summary <- rbindlist(qc_rows, fill = TRUE)
write.csv(qc_summary, file.path(output_dir, "qc_summary.csv"), row.names = FALSE)

combined <- Reduce(function(x, y) merge(x, y), objects)
combined <- NormalizeData(combined, normalization.method = "LogNormalize", scale.factor = 10000, verbose = FALSE)
combined <- FindVariableFeatures(combined, selection.method = "vst", nfeatures = 3000, verbose = FALSE)
combined <- ScaleData(combined, features = VariableFeatures(combined), verbose = FALSE)
combined <- RunPCA(combined, features = VariableFeatures(combined), npcs = 50, verbose = FALSE)
combined <- FindNeighbors(combined, dims = 1:30, verbose = FALSE)
combined <- FindClusters(combined, resolution = 0.5, verbose = FALSE)
combined <- RunUMAP(combined, dims = 1:30, n.neighbors = 30, min.dist = 0.3, verbose = FALSE)

saveRDS(combined, file.path(output_dir, "GSE255834_seurat_processed.rds"), compress = "xz")
saveRDS(combined, file.path(output_dir, "GSE255834_seurat_object.rds"), compress = "xz")

pdf(file.path(output_dir, "QC_plots.pdf"), width = 12, height = 8)
print(VlnPlot(combined, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), group.by = "sample", pt.size = 0, ncol = 3))
print(FeatureScatter(combined, feature1 = "nCount_RNA", feature2 = "nFeature_RNA", group.by = "sample"))
print(DimPlot(combined, reduction = "umap", group.by = "sample", raster = TRUE))
print(DimPlot(combined, reduction = "umap", group.by = "seurat_clusters", label = TRUE, raster = TRUE))
dev.off()

writeLines(capture.output(sessionInfo()), file.path(output_dir, "sessionInfo.txt"))
writeLines(c(
  "GSE255834 post-count scRNA-seq processing",
  "Input: 8 10x Genomics raw_feature_bc_matrix.h5 files",
  "Cell calling: per-sample barcodeRanks knee threshold",
  "QC: per-sample data-driven detected genes, total counts, and percent.mt thresholds",
  "Normalization: LogNormalize; HVG: vst (3000); PCA: 50 PCs; neighbors/clustering: PCs 1:30; UMAP: PCs 1:30",
  "Doublet calling: not performed (scDblFinder unavailable in the current R environment)",
  "Ambient RNA correction: not performed",
  paste0("Requested threads: ", configured_threads, "; execution backend: sequential (Windows-safe for sparse H5 matrices)")
), file.path(output_dir, "processing_notes.txt"))

message("DONE")
