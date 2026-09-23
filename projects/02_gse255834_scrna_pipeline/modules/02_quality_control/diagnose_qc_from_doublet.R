suppressPackageStartupMessages(library(Seurat))
f <- "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat/GSE255834_seurat_object_doublet.rds"
o <- readRDS(f)
m <- o@meta.data
q <- function(x) as.numeric(quantile(x, c(.01,.05,.25,.5,.75,.9,.95,.99), na.rm=TRUE))
samples <- unique(as.character(m[["sample"]]))
out <- lapply(samples, function(s) {
  z <- m[m[["sample"]] == s, , drop=FALSE]
  data.frame(
    sample=s, n=nrow(z),
    mt_q50=q(z[["percent.mt"]])[4], mt_q90=q(z[["percent.mt"]])[6],
    mt_q95=q(z[["percent.mt"]])[7], mt_q99=q(z[["percent.mt"]])[8],
    nf_q01=q(z[["nFeature_RNA"]])[1], nf_q50=q(z[["nFeature_RNA"]])[4], nf_q99=q(z[["nFeature_RNA"]])[8],
    nc_q01=q(z[["nCount_RNA"]])[1], nc_q50=q(z[["nCount_RNA"]])[4], nc_q99=q(z[["nCount_RNA"]])[8],
    mt_gt20=sum(z[["percent.mt"]] > 20), mt_gt30=sum(z[["percent.mt"]] > 30),
    mt_gt50=sum(z[["percent.mt"]] > 50),
    doublets=sum(z[["scDblFinder.class"]] == "doublet")
  )
})
df <- do.call(rbind, out)
write.csv(df, "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat/qc_distribution_diagnostic.csv", row.names=FALSE)
print(df)
