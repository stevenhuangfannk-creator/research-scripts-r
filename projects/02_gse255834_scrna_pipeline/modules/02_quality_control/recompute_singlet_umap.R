suppressPackageStartupMessages({
  library(Seurat)
  library(future)
  library(patchwork)
  library(ggplot2)
})

input <- "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat/GSE255834_seurat_singlet.rds"
out_dir <- "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat"
out_rds <- file.path(out_dir, "GSE255834_seurat_singlet_umap.rds")
o <- readRDS(input)
options(future.globals.maxSize = 100 * 1024^3)
workers <- 32L
future::plan(multisession, workers = workers)

features <- VariableFeatures(o)
o <- ScaleData(o, features = features, verbose = FALSE)
o <- RunPCA(o, features = features, npcs = 50, verbose = FALSE)
o <- FindNeighbors(o, dims = 1:30, verbose = FALSE)
o <- FindClusters(o, resolution = 0.5, verbose = FALSE)
o <- RunUMAP(o, dims = 1:30, n.neighbors = 30, min.dist = 0.3,
             n_threads = workers, verbose = FALSE)
future::plan(sequential)
saveRDS(o, out_rds, compress = "gzip")

p_sample <- DimPlot(o, reduction = "umap", group.by = "sample", raster = TRUE,
                    pt.size = 0.12, shuffle = TRUE) + ggtitle("Singlet UMAP by sample")
p_condition <- DimPlot(o, reduction = "umap", group.by = "condition", raster = TRUE,
                       pt.size = 0.12, shuffle = TRUE) + ggtitle("Singlet UMAP by condition")
p_tissue <- DimPlot(o, reduction = "umap", group.by = "tissue", raster = TRUE,
                    pt.size = 0.12, shuffle = TRUE) + ggtitle("Singlet UMAP by tissue")
p_cluster <- DimPlot(o, reduction = "umap", group.by = "seurat_clusters",
                     label = TRUE, repel = TRUE, raster = TRUE, pt.size = 0.12,
                     shuffle = TRUE) + ggtitle("Singlet UMAP by cluster")
panel <- (p_sample | p_condition) / (p_tissue | p_cluster)
ggsave(file.path(out_dir, "GSE255834_singlet_UMAP_overview.png"), panel,
       width = 16, height = 12, dpi = 300, bg = "white")
ggsave(file.path(out_dir, "GSE255834_singlet_UMAP_overview.pdf"), panel,
       width = 16, height = 12, bg = "white")
writeLines(capture.output(sessionInfo()), file.path(out_dir, "sessionInfo_singlet_umap.txt"))
message("DONE cells=", ncol(o), " clusters=", length(unique(as.character(Idents(o)))))
