suppressPackageStartupMessages(library(DropletUtils))
dir <- 'C:/Users/zhaozize/Desktop/APAP/raw_data/scRNA/GSE255834_RAW'
fs <- list.files(dir, pattern='\\.h5$', full.names=TRUE)
for (f in fs) {
  cat('READ',basename(f),'\n'); x <- read10xCounts(f); m <- counts(x); br <- barcodeRanks(m); md <- metadata(br); cat('DIM',nrow(m),ncol(m),'KNEE',md$knee,'INFLECTION',md$inflection,'\n'); rm(x,m,br); gc()
}
