suppressPackageStartupMessages({
  library(Seurat)
  library(future)
  library(patchwork)
library(ggplot2)
})

# Avoid nested BLAS/OpenMP oversubscription while Seurat's future workers run.
# The final uwot call below explicitly uses 70 native threads.
Sys.setenv(OMP_NUM_THREADS = "1", OPENBLAS_NUM_THREADS = "1",
           MKL_NUM_THREADS = "1", BLAS_NUM_THREADS = "1")

input <- "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat/GSE255834_seurat_object_doublet.rds"
out_dir <- "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat"
workers <- 1L
umap_threads <- 70L

o <- readRDS(input)
m <- o@meta.data
samples <- unique(as.character(m[["sample"]]))
keep <- rep(FALSE, nrow(m))
qc_rows <- list()

for (s in samples) {
  idx <- which(as.character(m[["sample"]]) == s)
  z <- m[idx, , drop = FALSE]
  min_features <- max(300, as.numeric(quantile(z[["nFeature_RNA"]], 0.01, na.rm = TRUE)))
  min_counts <- max(500, as.numeric(quantile(z[["nCount_RNA"]], 0.01, na.rm = TRUE)))
  max_percent_mt <- min(20, as.numeric(quantile(z[["percent.mt"]], 0.99, na.rm = TRUE)))
  pass <- z[["nFeature_RNA"]] >= min_features &
    z[["nCount_RNA"]] >= min_counts &
    z[["percent.mt"]] <= max_percent_mt &
    z[["scDblFinder.class"]] == "singlet"
  keep[idx] <- pass
  qc_rows[[s]] <- data.frame(
    sample = s, input_cells = nrow(z), strict_qc_cells = sum(pass),
    min_features = min_features, min_counts = min_counts,
    max_percent_mt = max_percent_mt,
    removed_high_mt = sum(z[["percent.mt"]] > max_percent_mt),
    removed_doublet = sum(z[["scDblFinder.class"]] == "doublet")
  )
}

m$strict_qc_pass <- keep
o@meta.data <- m
s <- subset(o, cells = rownames(m)[keep])
write.csv(do.call(rbind, qc_rows), file.path(out_dir, "strict_qc_summary.csv"), row.names = FALSE)

options(future.globals.maxSize = 100 * 1024^3)
future::plan(sequential)
s <- NormalizeData(s, normalization.method = "LogNormalize", scale.factor = 10000, verbose = FALSE)
s <- FindVariableFeatures(s, selection.method = "vst", nfeatures = 3000, verbose = FALSE)
s <- ScaleData(s, features = VariableFeatures(s), verbose = FALSE)
s <- RunPCA(s, features = VariableFeatures(s), npcs = 50, verbose = FALSE)
s <- FindNeighbors(s, dims = 1:30, verbose = FALSE)
s <- FindClusters(s, resolution = 0.5, verbose = FALSE)
future::plan(sequential)
s_pca <- Embeddings(s, reduction = "pca")[, 1:30, drop = FALSE]
um <- uwot::umap(
  X = s_pca, n_neighbors = 30, n_components = 2, metric = "cosine",
  min_dist = 0.3, n_threads = umap_threads, init = "spectral",
  n_epochs = NULL, ret_model = FALSE, verbose = FALSE, seed = 42
)
colnames(um) <- c("UMAP_1", "UMAP_2")
rownames(um) <- rownames(s_pca)
s[["umap"]] <- CreateDimReducObject(embeddings = um, key = "UMAP_", assay = DefaultAssay(s), global = TRUE)

out_rds <- file.path(out_dir, "GSE255834_seurat_strict_qc_70w.rds")
saveRDS(s, out_rds, compress = "gzip")

p_sample <- DimPlot(s, reduction = "umap", group.by = "sample", raster = TRUE,
                    pt.size = 0.12, shuffle = TRUE) + ggtitle("Strict-QC UMAP by sample")
p_condition <- DimPlot(s, reduction = "umap", group.by = "condition", raster = TRUE,
                       pt.size = 0.12, shuffle = TRUE) + ggtitle("Strict-QC UMAP by condition")
p_tissue <- DimPlot(s, reduction = "umap", group.by = "tissue", raster = TRUE,
                    pt.size = 0.12, shuffle = TRUE) + ggtitle("Strict-QC UMAP by tissue")
p_cluster <- DimPlot(s, reduction = "umap", group.by = "seurat_clusters",
                     label = TRUE, repel = TRUE, raster = TRUE, pt.size = 0.12,
                     shuffle = TRUE) + ggtitle("Strict-QC UMAP by cluster")
panel <- (p_sample | p_condition) / (p_tissue | p_cluster)
ggsave(file.path(out_dir, "GSE255834_strict_QC_UMAP_70w.png"), panel,
       width = 16, height = 12, dpi = 300, bg = "white")
ggsave(file.path(out_dir, "GSE255834_strict_QC_UMAP_70w.pdf"), panel,
       width = 16, height = 12, bg = "white")
writeLines(capture.output(sessionInfo()), file.path(out_dir, "sessionInfo_strict_qc_70w.txt"))
writeLines(c(paste0("matrix_workers=", workers), paste0("umap_threads=", umap_threads), paste0("cells=", ncol(s)),
             "QC: sample-specific 1% lower quantiles for genes/UMIs, mt <= min(20%, sample 99th percentile), singlets only"),
           file.path(out_dir, "strict_qc_notes.txt"))
message("DONE cells=", ncol(s), " clusters=", length(unique(as.character(Idents(s)))))
