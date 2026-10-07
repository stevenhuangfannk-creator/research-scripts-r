run_workflow <- function(input, config) {
  stopifnot(inherits(input, "Seurat"))
  set.seed(config$seed)
  obj <- Seurat::FindVariableFeatures(input, nfeatures = config$nfeatures, verbose = FALSE)
  obj <- Seurat::ScaleData(obj, features = Seurat::VariableFeatures(obj), verbose = FALSE)
  k <- min(config$npcs, length(Seurat::VariableFeatures(obj)) - 1L, ncol(obj) - 1L)
  if (k < 2L) stop("Too few cells / variable genes for PCA")
  obj <- Seurat::RunPCA(obj, npcs = k, seed.use = config$seed, verbose = FALSE)
  obj <- Seurat::FindNeighbors(obj, reduction = "pca", dims = seq_len(k), verbose = FALSE)
  obj <- Seurat::FindClusters(obj, resolution = config$resolution, random.seed = config$seed, verbose = FALSE)
  obj <- Seurat::RunUMAP(obj, reduction = "pca", dims = seq_len(k),
                        n.neighbors = min(config$n_neighbors, ncol(obj) - 1L),
                        seed.use = config$seed, verbose = FALSE)
  list(object = obj, tables = list(clusters = data.frame(cell = colnames(obj), cluster = as.character(Seurat::Idents(obj)))))
}
