suppressPackageStartupMessages({
  library(Seurat)
  library(SingleCellExperiment)
  library(scDblFinder)
  library(BiocParallel)
  library(future)
  library(future.apply)
})

input <- "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat/GSE255834_seurat_object_joined.rds"
output <- "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat/GSE255834_seurat_object_doublet.rds"
workers <- 8L

seed_obj <- readRDS(input)
sample_names <- unique(as.character(seed_obj@meta.data[["sample"]]))
rm(seed_obj)
gc()

# One worker per biological capture/sample. Each worker reads only its sample
# slice and uses SerialParam internally, avoiding nested process explosions.
future::plan(multisession, workers = workers)
results <- future_lapply(sample_names, function(s) {
  suppressPackageStartupMessages({
    library(Seurat)
    library(SingleCellExperiment)
    library(scDblFinder)
    library(BiocParallel)
  })
  o <- readRDS(input)
  meta <- o@meta.data
  idx <- which(as.character(meta[["sample"]]) == s)
  cnt <- GetAssayData(o, assay = "RNA", layer = "counts")[, idx, drop = FALSE]
  sce <- SingleCellExperiment(list(counts = cnt))
  sce <- scDblFinder(
    sce,
    samples = rep(s, length(idx)),
    dbr.per1k = 0.008,
    BPPARAM = SerialParam(progressbar = FALSE),
    verbose = FALSE
  )
  data.frame(
    sample = s,
    cell = colnames(o)[idx],
    scDblFinder.score = as.numeric(colData(sce)$scDblFinder.score),
    scDblFinder.class = as.character(colData(sce)$scDblFinder.class),
    stringsAsFactors = FALSE
  )
}, future.seed = TRUE)
future::plan(sequential)

o <- readRDS(input)
meta <- o@meta.data
all_cells <- rownames(meta)
res <- do.call(rbind, results)
map <- match(all_cells, res$cell)
meta$scDblFinder.score <- res$scDblFinder.score[map]
meta$scDblFinder.class <- factor(res$scDblFinder.class[map], levels = c("singlet", "doublet"))
meta$doublet_pass <- meta$scDblFinder.class == "singlet"
o@meta.data <- meta

saveRDS(o, output, compress = "gzip")
write.csv(as.data.frame(table(sample = res$sample,
                              scDblFinder.class = res$scDblFinder.class)),
          "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat/scDblFinder_summary.csv",
          row.names = FALSE)
writeLines(capture.output(sessionInfo()),
           "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat/sessionInfo_scDblFinder.txt")
writeLines(paste0("scDblFinder workers: ", workers),
           "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat/scDblFinder_workers.txt")
message("DONE")
