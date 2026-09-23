suppressPackageStartupMessages(library(Seurat))
dir <- 'C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat'
fs <- sort(list.files(dir, pattern='_raw_seurat\\.rds$', full.names=TRUE))
out <- list()
for (f in fs) {
  o <- readRDS(f); m <- o@meta.data
  samp <- unique(as.character(m[['sample']]))
  q <- function(x) as.numeric(quantile(x, c(.01,.05,.25,.5,.75,.9,.95,.99), na.rm=TRUE))
  out[[samp]] <- data.frame(sample=samp, n=nrow(m), qc_pass=sum(m[['qc_pass']]),
    nf_q01=q(m$nFeature_RNA)[1], nf_q05=q(m$nFeature_RNA)[2], nf_q50=q(m$nFeature_RNA)[4], nf_q95=q(m$nFeature_RNA)[7], nf_q99=q(m$nFeature_RNA)[8],
    nc_q01=q(m$nCount_RNA)[1], nc_q05=q(m$nCount_RNA)[2], nc_q50=q(m$nCount_RNA)[4], nc_q95=q(m$nCount_RNA)[7], nc_q99=q(m$nCount_RNA)[8],
    mt_q50=q(m$percent.mt)[4], mt_q90=q(m$percent.mt)[6], mt_q95=q(m$percent.mt)[7], mt_q99=q(m$percent.mt)[8],
    mt_gt10=sum(m$percent.mt>10), mt_gt20=sum(m$percent.mt>20), mt_gt30=sum(m$percent.mt>30), mt_gt50=sum(m$percent.mt>50),
    pass_mt20=sum(m[['qc_pass']] & m$percent.mt<=20), pass_mt30=sum(m[['qc_pass']] & m$percent.mt<=30))
  rm(o); gc()
}
df <- do.call(rbind,out); write.csv(df,file.path(dir,'qc_distribution_diagnostic.csv'),row.names=FALSE); print(df)
