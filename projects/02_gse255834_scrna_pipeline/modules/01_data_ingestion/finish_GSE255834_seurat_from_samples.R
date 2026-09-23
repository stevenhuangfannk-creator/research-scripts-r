suppressPackageStartupMessages({
  library(Seurat)
  library(Matrix)
  library(data.table)
  library(ggplot2)
})

output_dir <- "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat"
files <- sort(list.files(output_dir, pattern = "_raw_seurat\\.rds$", full.names = TRUE))
stopifnot(length(files) == 8L)

filtered <- vector("list", length(files))
names(filtered) <- sub("_raw_seurat\\.rds$", "", basename(files))

for (i in seq_along(files)) {
  message(sprintf("[%d/%d] loading and materializing %s", i, length(files), basename(files[[i]])))
  obj <- readRDS(files[[i]])
  keep <- which(as.logical(obj$qc_pass))
  counts_delayed <- GetAssayData(obj, assay = "RNA", layer = "counts")[, keep, drop = FALSE]
  counts_sparse <- as(counts_delayed, "dgCMatrix")
  meta <- obj@meta.data[keep, , drop = FALSE]
  filtered[[i]] <- CreateSeuratObject(
    counts = counts_sparse,
    meta.data = meta,
    project = "GSE255834",
    min.cells = 0,
    min.features = 0
  )
  rm(obj, counts_delayed, counts_sparse, meta)
  gc()
}

message("merging filtered sample objects")
combined <- filtered[[1L]]
for (i in 2:length(filtered)) {
  combined <- merge(combined, filtered[[i]], merge.data = FALSE)
  gc()
}
rm(filtered)
gc()

saveRDS(combined, file.path(output_dir, "GSE255834_seurat_qc.rds"), compress = "gzip")

message(sprintf("QC object: %d genes x %d cells", nrow(combined), ncol(combined)))
combined <- NormalizeData(combined, normalization.method = "LogNormalize", scale.factor = 10000, verbose = FALSE)
combined <- FindVariableFeatures(combined, selection.method = "vst", nfeatures = 3000, verbose = FALSE)
combined <- ScaleData(combined, features = VariableFeatures(combined), verbose = FALSE)
combined <- RunPCA(combined, features = VariableFeatures(combined), npcs = 50, verbose = FALSE)
combined <- FindNeighbors(combined, dims = 1:30, verbose = FALSE)
combined <- FindClusters(combined, resolution = 0.5, verbose = FALSE)
combined <- RunUMAP(combined, dims = 1:30, n.neighbors = 30, min.dist = 0.3, verbose = FALSE)

saveRDS(combined, file.path(output_dir, "GSE255834_seurat_processed.rds"), compress = "gzip")
saveRDS(combined, file.path(output_dir, "GSE255834_seurat_object.rds"), compress = "gzip")

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
  "Requested threads: 70; execution backend: sequential (Windows-safe for sparse H5 matrices)"
), file.path(output_dir, "processing_notes.txt"))

message("DONE")
