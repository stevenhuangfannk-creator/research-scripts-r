#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(data.table)
  library(Matrix)
  library(SeuratObject)
})

threads <- 72L
data.table::setDTthreads(threads)
options(stringsAsFactors = FALSE)

count_file <- file.path("raw_data", "scRNA", "Single_cell_UMI_COUNT.txt")
meta_file <- file.path("raw_data", "scRNA", "Single_cell_Meta_data.txt")
out_dir <- "results"
out_file <- file.path(out_dir, "APAP_merged_seurat.rds")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

message("Reading metadata with ", threads, " threads ...")
meta <- fread(meta_file, nThread = threads, showProgress = TRUE)
stopifnot("Cell_barcode" %in% names(meta))
if (anyDuplicated(meta$Cell_barcode)) {
  stop("Duplicate Cell_barcode values found in metadata")
}
meta_cells <- meta$Cell_barcode

message("Reading count matrix with ", threads, " threads ...")
counts_dt <- fread(count_file, nThread = threads, showProgress = TRUE)
if (!identical(names(counts_dt)[1L], "Gene_Name")) {
  stop("The first count-matrix column must be Gene_Name")
}
gene_names <- counts_dt[[1L]]
cell_names <- names(counts_dt)[-1L]
if (anyDuplicated(gene_names)) {
  stop("Duplicate gene names found in count matrix")
}
if (anyDuplicated(cell_names)) {
  stop("Duplicate cell barcodes found in count matrix")
}
if (!setequal(cell_names, meta_cells)) {
  missing_meta <- setdiff(cell_names, meta_cells)
  missing_counts <- setdiff(meta_cells, cell_names)
  stop(
    "Cell barcodes do not match. Missing from metadata: ", length(missing_meta),
    "; missing from count matrix: ", length(missing_counts)
  )
}

message("Converting ", nrow(counts_dt), " x ", length(cell_names), " matrix to sparse format ...")
counts_dt[[1L]] <- NULL
counts_dense <- as.matrix(counts_dt)
storage.mode(counts_dense) <- "double"
counts <- Matrix(counts_dense, sparse = TRUE)
rm(counts_dt, counts_dense)
gc(verbose = FALSE)
rownames(counts) <- gene_names
colnames(counts) <- cell_names

meta_df <- as.data.frame(meta)
rownames(meta_df) <- meta_df$Cell_barcode
meta_df <- meta_df[cell_names, , drop = FALSE]
if (!identical(rownames(meta_df), colnames(counts))) {
  stop("Metadata and count matrix could not be aligned")
}

message("Creating Seurat object ...")
obj <- CreateSeuratObject(
  counts = counts,
  meta.data = meta_df,
  project = "APAP",
  min.cells = 0,
  min.features = 0
)

if (all(c("UMAP_X", "UMAP_Y") %in% names(meta_df))) {
  umap_embeddings <- as.matrix(meta_df[, c("UMAP_X", "UMAP_Y"), drop = FALSE])
  colnames(umap_embeddings) <- c("UMAP_1", "UMAP_2")
  umap <- CreateDimReducObject(
    embeddings = umap_embeddings,
    key = "UMAP_",
    assay = DefaultAssay(obj)
  )
  rownames(umap@cell.embeddings) <- colnames(obj)
  obj[["umap"]] <- umap
}

obj@misc$input_files <- normalizePath(c(count_file, meta_file), winslash = "/", mustWork = TRUE)
obj@misc$construction <- list(
  method = "Single matrix + aligned metadata; sparse conversion",
  data.table_threads = threads,
  created = format(Sys.time(), tz = "Asia/Shanghai")
)

message("Writing ", out_file, " ...")
saveRDS(obj, out_file, compress = "gzip")

message("Verifying saved object ...")
check <- readRDS(out_file)
stopifnot(
  nrow(check) == nrow(counts),
  ncol(check) == ncol(counts),
  identical(colnames(check), cell_names),
  identical(rownames(check[[]]), cell_names)
)
message(
  "Done: ", nrow(check), " genes x ", ncol(check), " cells; ",
  "non-zero entries = ", nnzero(GetAssayData(check, layer = "counts")),
  "; file size = ", format(file.info(out_file)$size / 1024^3, digits = 3), " GiB"
)

getwd()
scRNA<-readRDS("./results/APAP_merged_seurat.rds")
table(scRNA$time_point,scRNA$cell_type)
