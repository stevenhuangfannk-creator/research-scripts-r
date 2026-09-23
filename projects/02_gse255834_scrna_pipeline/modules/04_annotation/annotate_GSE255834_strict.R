suppressPackageStartupMessages({
  library(Seurat)
  library(Matrix)
  library(ggplot2)
  library(patchwork)
})
options(future.globals.maxSize = 20 * 1024^3)

default_out_dir <- "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat"
input <- Sys.getenv("GSE255834_ANNOTATION_INPUT",
                    "C:/Users/zhaozize/Desktop/APAP/results/GSE255834_seurat/GSE255834_seurat_strict_qc_70w.rds")
out_dir <- Sys.getenv("GSE255834_ANNOTATION_OUTDIR", default_out_dir)
annotation_label <- Sys.getenv("GSE255834_ANNOTATION_LABEL", "strict-QC")
annotation_rds_name <- Sys.getenv("GSE255834_ANNOTATION_RDS_NAME",
                                  "GSE255834_seurat_strict_qc_annotated.rds")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
obj <- readRDS(input)
DefaultAssay(obj) <- "RNA"

# Marker panels follow the local annotation documents:
# results/annotion/mouse_liver_level1_annotation.html
# results/annotion/mouse_liver_level2_immune_annotation.html
l1_markers <- list(
  Hepatocyte      = c("Alb", "Ttr", "Apoa1", "Cyp2e1", "G6pc"),
  Cholangiocyte   = c("Epcam", "Krt19", "Krt7", "Sox9"),
  Endothelial     = c("Pecam1", "Cdh5", "Kdr", "Clec4g", "Stab2"),
  HSC_Mesenchymal = c("Dcn", "Col1a1", "Lrat", "Reln", "Pdgfrb"),
  Myeloid         = c("Cd68", "Adgre1", "C1qa", "Ly6c2", "S100a8", "Siglech", "Flt3"),
  Lymphoid        = c("Cd3d", "Nkg7", "Ncr1", "Cd79a", "Ms4a1", "Jchain")
)

fine_markers <- list(
  Hepatocyte      = c("Alb","Apoa1","Apoa2","Ttr","Cyp2e1","Cyp2f2","G6pc","Asgr1","Fabp1","Hamp","Pck1","Oat"),
  Cholangiocyte   = c("Epcam","Krt19","Krt7","Sox9","Cftr","Hnf1b","Cldn4","Agr2","Muc1","Sctr"),
  Endothelial     = c("Pecam1","Cdh5","Kdr","Emcn","Clec4g","Stab2","Stab1","Vwf","Plvap","Egfl7","Aqp1","Flt4","Lyve1"),
  HSC_Mesenchymal = c("Dcn","Col1a1","Col3a1","Lrat","Reln","Pdgfrb","Des","Ngfr","Rgs5","Colec10","Col15a1","Vim"),
  Kupffer         = c("Adgre1","Cd68","C1qa","C1qb","C1qc","Timd4","Vsig4","Clec4f","Cd5l","Marco"),
  Monocyte        = c("Ly6c2","Ccr2","Plac8","Fcnb","Ms4a6c","Cx3cr1","Sell","Cd14","Ifitm3"),
  MoMac           = c("Adgre1","Cd68","C1qa","Ly6c2","Ccr2","Spp1","Arg1","Mrc1","Chil3","Fn1"),
  cDC             = c("Flt3","Itgax","H2-Aa","H2-Ab1","H2-Eb1","Clec9a","Xcr1","Cd209a","Cd24a","Ccr7"),
  pDC             = c("Siglech","Bst2","Irf7","Tcf4","Ccr9","Ly6d"),
  Neutrophil      = c("S100a8","S100a9","Retnlg","Ly6g","Cxcr2","Csf3r","Mmp8","S100a6"),
  T_NK            = c("Cd3d","Cd3e","Cd3g","Trbc1","Nkg7","Ncr1","Klrb1c","Gzma","Klrd1","Xcl1","Il7r","Trdc","Tcrg-C1","Tcrg-C2"),
  B               = c("Cd79a","Cd79b","Ms4a1","Cd19","Pax5","Ighm","Ighd"),
  Plasma          = c("Sdc1","Jchain","Derl3","Mzb1","Xbp1","Ighg1"),
  Mast_Baso       = c("Fcer1a","Ms4a2","Kit","Cpa3","Mcpt8","Prss34","Gata2"),
  Mesothelial     = c("Msln","Wt1","Upk3b","Calb2","Lrrn4","Cldn15","Muc16"),
  Erythroid       = c("Hba-a1","Hba-a2","Hbb-bt","Hbb-bs","Alas2","Gypa","Snca"),
  Cycling         = c("Mki67","Top2a","Birc5","Ube2c","Pcna","Ccna2","Ccnb2")
)

l2_markers <- list(
  KC          = c("Adgre1","C1qa","C1qb","C1qc","Timd4","Vsig4","Clec4f","Cd5l","Marco"),
  Macrophages = c("Adgre1","Cd68","C1qa","Ly6c2","Ccr2","Spp1","Arg1","Fn1","Chil3","Mrc1","Trem2"),
  Monocyte    = c("Ly6c2","Ccr2","Plac8","Ms4a6c","Fcnb","Sell","Cd14","Ifitm3","Cx3cr1","Nr4a1"),
  Neutrophil  = c("S100a8","S100a9","Retnlg","Ly6g","Cxcr2","Csf3r","Mmp8","S100a6","Cxcl2","Il1b"),
  cDC         = c("Flt3","Itgax","H2-Aa","H2-Ab1","H2-Eb1","Clec9a","Xcr1","Cd209a","Cd24a","Ccr7","Batf3"),
  pDC         = c("Siglech","Bst2","Tcf4","Ccr9","Ly6d","Irf7"),
  T           = c("Cd3d","Cd3e","Cd3g","Trbc1","Lat","Il7r","Cd4","Cd8a","Cd8b1","Tcrg-C1","Tcrg-C2","Trdc","Zbtb16","Foxp3","Sell","Ccr7","Tcf7","Pdcd1","Tox","Havcr2","Lag3","Gzmb","Ifng"),
  NK          = c("Ncr1","Nkg7","Klrd1","Klrb1c","Klrk1","Gzma","Prf1","Xcl1","Eomes","S1pr5","Fcer1g","Tyrobp","Klra4","Cd160"),
  B           = c("Cd79a","Cd79b","Ms4a1","Cd19","Pax5","Ighm","Ighd","Cd22","Fcmr","Sdc1","Jchain","Mzb1","Derl3","Xbp1","Igkc"),
  Cycling     = c("Mki67","Top2a","Birc5","Ube2c","Pcna","Ccna2","Ccnb2")
)

expr <- GetAssayData(obj, assay = "RNA", layer = "data")
module_pool <- rownames(expr)[Matrix::rowSums(expr > 0) > 0]
keep_genes <- function(x) lapply(x, function(g) intersect(g, rownames(expr)))
l1_markers <- keep_genes(l1_markers)
fine_markers <- keep_genes(fine_markers)
l2_markers <- keep_genes(l2_markers)

# The level-1 method in the local annotation report uses AddModuleScore at cell level,
# then averages scores by cluster. Cycling is retained as a state, not a lineage.
l1_score_sets <- list(
  Hepatocyte = fine_markers$Hepatocyte,
  Cholangiocyte = fine_markers$Cholangiocyte,
  Endothelial = fine_markers$Endothelial,
  HSC_Mesenchymal = fine_markers$HSC_Mesenchymal,
  Myeloid = unique(c(fine_markers$Kupffer, fine_markers$Monocyte, fine_markers$MoMac,
                     fine_markers$cDC, fine_markers$pDC, fine_markers$Neutrophil,
                     fine_markers$Mast_Baso)),
  Lymphoid = unique(c(fine_markers$T_NK, fine_markers$B, fine_markers$Plasma)),
  Mesothelial = fine_markers$Mesothelial,
  Erythroid = fine_markers$Erythroid
)
l1_score_sets <- lapply(l1_score_sets, unique)

add_module_score_matrix <- function(object, sets, prefix) {
  score_cols <- character(length(sets))
  names(score_cols) <- names(sets)
  for (nm in names(sets)) {
    genes <- unique(intersect(sets[[nm]], module_pool))
    score_col <- paste0(prefix, nm, "1")
    if (length(genes) < 2) {
      object[[score_col]] <- rep(0, ncol(object))
      score_cols[[nm]] <- score_col
      message("Skipping module score for ", nm, ": fewer than 2 detected panel genes")
      next
    }
    message("Scoring module ", nm, " (", length(genes), " detected markers)")
    object <- AddModuleScore(object, features = list(genes), pool = module_pool, assay = "RNA",
                             name = paste0(prefix, nm), seed = 42, search = FALSE)
    score_cols[[nm]] <- score_col
  }
  scores <- t(as.matrix(object@meta.data[, score_cols, drop = FALSE]))
  rownames(scores) <- names(sets)
  colnames(scores) <- rownames(object@meta.data)
  list(object = object, scores = scores)
}

m <- obj@meta.data
clusters <- as.character(sort(as.integer(unique(as.character(m$seurat_clusters)))))
cluster_id <- as.character(m$seurat_clusters)
cluster_means <- function(scores) {
  z <- t(sapply(clusters, function(cl) {
    cells <- which(cluster_id == cl)
    colMeans(t(scores[, cells, drop = FALSE]), na.rm = TRUE)
  }))
  colnames(z) <- rownames(scores)
  rownames(z) <- clusters
  z
}
z_by_row <- function(x) {
  z <- t(scale(t(x)))
  z[is.na(z)] <- 0
  z
}

sc_l1 <- add_module_score_matrix(obj, l1_score_sets, "L1score_")
obj <- sc_l1$object
scores_l1 <- sc_l1$scores
sc_fine <- add_module_score_matrix(obj, fine_markers, "FineScore_")
obj <- sc_fine$object
scores_fine <- sc_fine$scores
sc_l2 <- add_module_score_matrix(obj, l2_markers, "L2score_")
obj <- sc_l2$object
scores_l2 <- sc_l2$scores
refine_markers <- list(
  HSC = c("Lrat", "Reln", "Des", "Ngfr", "Colec10"),
  Pericyte = c("Rgs5", "Pdgfrb", "Cspg4", "Acta2", "Tagln"),
  Fibroblast = c("Col1a1", "Col3a1", "Dcn", "Col15a1", "Lum"),
  LSEC = c("Clec4g", "Stab2", "Stab1", "Lyve1"),
  Vascular_endothelial = c("Vwf", "Emcn", "Kdr", "Pecam1")
)
refine_markers <- keep_genes(refine_markers)
sc_refine <- add_module_score_matrix(obj, refine_markers, "RefineScore_")
obj <- sc_refine$object
scores_refine <- sc_refine$scores
m <- obj@meta.data
cluster_id <- as.character(m$seurat_clusters)
cl_l1 <- cluster_means(scores_l1)
cl_fine <- cluster_means(scores_fine)
cl_l2 <- cluster_means(scores_l2)
cl_l1_z <- z_by_row(cl_l1)
cl_fine_z <- z_by_row(cl_fine)
cl_l2_z <- z_by_row(cl_l2)
cl_refine <- cluster_means(scores_refine)
cl_refine_z <- z_by_row(cl_refine)

# Marker positive fraction and mean log-normalized expression are retained as
# direct expression evidence, as in the level-2 annotation report.
marker_panel <- unique(c(unlist(l1_score_sets), unlist(fine_markers), unlist(l2_markers)))
marker_workers <- min(8L, length(clusters))
future::plan(future::multisession, workers = marker_workers)
marker_stats_by_cluster <- future.apply::future_lapply(clusters, function(cl) {
  cells <- which(cluster_id == cl)
  stats <- vector("list", length(marker_panel))
  for (gene in marker_panel) {
    x <- expr[gene, cells, drop = FALSE]
    stats[[match(gene, marker_panel)]] <- data.frame(
      cluster = cl, gene = gene,
      pct_positive = 100 * as.numeric(Matrix::rowMeans(x > 0)),
      avg_log_normalized = as.numeric(Matrix::rowMeans(x)),
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, stats)
}, future.seed = TRUE, future.packages = "Matrix")
future::plan(future::sequential)
marker_stats <- do.call(rbind, marker_stats_by_cluster)
rm(marker_stats_by_cluster)

# The first pass is deliberately cluster-level: labels are not assigned from one noisy cell.
best_label <- function(x, min_z = -Inf) {
  o <- order(x, decreasing = TRUE)
  best <- names(x)[o[1]]
  second <- names(x)[o[2]]
  gap <- unname(x[o[1]] - x[o[2]])
  if (unname(x[o[1]]) < min_z) best <- "Unresolved"
  c(label = best, second = second, best_score = unname(x[o[1]]), gap = gap)
}

l1_dec <- t(apply(cl_l1_z, 1, best_label, min_z = 0.25))
l1_dec <- as.data.frame(l1_dec, stringsAsFactors = FALSE)
l1_dec$cluster <- rownames(l1_dec)
l1_dec$n_cells <- as.integer(table(factor(cluster_id, levels = clusters)))
l1_dec$best_score <- as.numeric(l1_dec$best_score)
l1_dec$gap <- as.numeric(l1_dec$gap)

# Reconcile score-margin confidence with key-marker detection. Conflicting strong
# lineage signatures remain low confidence; several concordant markers can rescue
# an otherwise small score gap (e.g., Spp1/Trem2 macrophages or Alb/Ttr hepatocytes).
l1_key_markers <- list(
  Hepatocyte = c("Alb", "Ttr", "Apoa1", "Cyp2e1", "G6pc"),
  Cholangiocyte = c("Epcam", "Krt19", "Krt7", "Sox9"),
  Endothelial = c("Pecam1", "Cdh5", "Kdr", "Clec4g", "Stab2"),
  HSC_Mesenchymal = c("Dcn", "Col1a1", "Lrat", "Reln", "Pdgfrb"),
  Myeloid = c("Adgre1", "Cd68", "C1qa", "Ly6c2", "S100a8", "S100a9", "Flt3", "Siglech"),
  Lymphoid = c("Cd3d", "Nkg7", "Ncr1", "Cd79a", "Ms4a1", "Jchain"),
  Mast_Baso = c("Fcer1a", "Ms4a2", "Cpa3", "Mcpt8", "Gata2"),
  Erythroid = c("Hba-a1", "Hba-a2", "Hbb-bt", "Hbb-bs", "Alas2", "Gypa"),
  Mesothelial = c("Msln", "Wt1", "Upk3b", "Calb2", "Cldn15")
)
# Add rare but biologically meaningful lineages detected by the fine panel.
for (cl in clusters) {
  if (cl_fine_z[cl, "Erythroid"] >= 1.2 && cl_fine_z[cl, "Erythroid"] > cl_l1_z[cl, "Myeloid"] + 0.3) l1_dec[cl, "label"] <- "Erythroid"
  if (cl_fine_z[cl, "Mast_Baso"] >= 1.2 && cl_fine_z[cl, "Mast_Baso"] > cl_l1_z[cl, "Myeloid"] + 0.3) l1_dec[cl, "label"] <- "Mast_Baso"
  if (cl_fine_z[cl, "Mesothelial"] >= 1.2 && cl_fine_z[cl, "Mesothelial"] > cl_l1_z[cl, "HSC_Mesenchymal"] + 0.3) l1_dec[cl, "label"] <- "Mesothelial"
}

# Secondary labels follow the immune document's KC/Macrophage/Monocyte/cDC/pDC/T/NK/B scheme.
l2_dec <- data.frame(cluster = clusters, l1 = l1_dec[clusters, "label"],
                     label = "Unresolved", second = NA_character_,
                     best_score = NA_real_, gap = NA_real_, stringsAsFactors = FALSE)
l2_dec$n_cells <- l1_dec$n_cells[match(l2_dec$cluster, l1_dec$cluster)]
for (i in seq_along(clusters)) {
  cl <- clusters[i]
  l1 <- l2_dec$l1[i]
  cand <- switch(l1,
    Myeloid = c("KC", "Macrophages", "Monocyte", "Neutrophil", "cDC", "pDC"),
    Lymphoid = c("T", "NK", "B"),
    Hepatocyte = character(), Cholangiocyte = character(), Endothelial = character(),
    HSC_Mesenchymal = character(), Erythroid = character(), Mast_Baso = character(),
    Mesothelial = character(), character())
  if (length(cand) > 0) {
    dec <- best_label(cl_l2_z[cl, cand], min_z = -0.25)
    l2_dec[i, c("label", "second", "best_score", "gap")] <- c(dec["label"], dec["second"], as.numeric(dec["best_score"]), as.numeric(dec["gap"]))
  } else {
    l2_dec$label[i] <- switch(l1,
      Hepatocyte = "Hepatocyte", Cholangiocyte = "Cholangiocyte", Endothelial = "Endothelial",
      HSC_Mesenchymal = "HSC_Mesenchymal", Erythroid = "Erythroid", Mast_Baso = "Mast_Baso",
      Mesothelial = "Mesothelial", "Unresolved")
  }
}

# Refine common liver compartments with the fine marker evidence.
for (i in seq_along(clusters)) {
  cl <- clusters[i]
  cells <- which(cluster_id == cl)
  if (l2_dec$l1[i] == "HSC_Mesenchymal") {
    vals <- cl_refine_z[cl, c("HSC", "Pericyte", "Fibroblast")]
    l2_dec$label[i] <- names(which.max(vals))
    l2_dec$second[i] <- names(sort(vals, decreasing = TRUE))[2]
    l2_dec$best_score[i] <- max(vals)
    l2_dec$gap[i] <- sort(vals, decreasing = TRUE)[1] - sort(vals, decreasing = TRUE)[2]
  }
  if (l2_dec$l1[i] == "Endothelial") {
    lsec <- cl_refine_z[cl, "LSEC"]
    vascular <- cl_refine_z[cl, "Vascular_endothelial"]
    l2_dec$label[i] <- ifelse(lsec >= vascular, "LSEC", "Vascular_endothelial")
    l2_dec$second[i] <- ifelse(lsec >= vascular, "Vascular_endothelial", "LSEC")
    l2_dec$best_score[i] <- max(lsec, vascular)
    l2_dec$gap[i] <- abs(lsec - vascular)
  }
  # Plasma cells are a B-lineage state distinguished by the fine plasma panel.
  if (l2_dec$label[i] == "B" && cl_fine_z[cl, "Plasma"] > cl_fine_z[cl, "B"] + 0.25) l2_dec$label[i] <- "Plasma"
}

l1_dec$confidence <- ifelse(l1_dec$label == "Unresolved", "low",
                            ifelse(l1_dec$gap >= 0.75, "high", ifelse(l1_dec$gap >= 0.35, "medium", "low")))
for (i in seq_len(nrow(l1_dec))) {
  cl <- l1_dec$cluster[i]
  per_type <- lapply(l1_key_markers, function(genes) {
    marker_stats$pct_positive[marker_stats$cluster == cl & marker_stats$gene %in% genes]
  })
  n_strong <- vapply(per_type, function(p) sum(p >= 25, na.rm = TRUE), integer(1))
  selected <- l1_dec$label[i]
  selected_genes <- per_type[[selected]]
  selected_strong <- sum(selected_genes >= 25, na.rm = TRUE)
  selected_moderate <- sum(selected_genes >= 10, na.rm = TRUE)
  n_strong_types <- sum(n_strong >= 2)
  if (n_strong_types >= 2) {
    l1_dec$confidence[i] <- "low"
  } else if (selected_strong >= 2) {
    l1_dec$confidence[i] <- if (l1_dec$n_cells[i] < 100) "medium" else "high"
  } else if (selected_moderate >= 2 && l1_dec$confidence[i] == "low") {
    l1_dec$confidence[i] <- "medium"
  }
}
l2_dec$confidence <- ifelse(l2_dec$label == "Unresolved", "low",
                            ifelse(is.na(l2_dec$gap),
                                   unname(setNames(l1_dec$confidence, l1_dec$cluster)[l2_dec$cluster]),
                                   ifelse(l2_dec$gap >= 0.75, "high", ifelse(l2_dec$gap >= 0.35, "medium", "low"))))
l2_dec$confidence[l2_dec$n_cells < 100 & l2_dec$confidence == "high"] <- "medium"
evidence_markers <- c(l1_key_markers, list(
  KC = c("Clec4f", "Cd5l", "Timd4", "Vsig4", "Marco"),
  Macrophages = c("Adgre1", "Cd68", "C1qa", "Ccr2", "Ly6c2", "Spp1", "Trem2", "Arg1", "Mrc1"),
  Monocyte = c("Ccr2", "Ly6c2", "Plac8", "Ms4a6c", "Sell", "Cx3cr1"),
  Neutrophil = c("S100a8", "S100a9", "Retnlg", "Ly6g", "Cxcr2", "Csf3r"),
  cDC = c("Flt3", "Itgax", "Clec9a", "Xcr1", "Cd209a"),
  pDC = c("Siglech", "Ccr9", "Ly6d", "Tcf4", "Bst2"),
  T = c("Cd3d", "Cd3e", "Cd3g", "Trbc1", "Trdc", "Il7r"),
  NK = c("Ncr1", "Nkg7", "Klrd1", "Gzma", "Prf1", "Xcl1"),
  B = c("Cd79a", "Ms4a1", "Cd19", "Pax5", "Ighm", "Ighd"),
  Plasma = c("Sdc1", "Jchain", "Mzb1", "Derl3", "Xbp1"),
  HSC = c("Lrat", "Reln", "Des", "Ngfr", "Colec10"),
  Fibroblast = c("Col1a1", "Col3a1", "Dcn", "Col15a1", "Lum"),
  Pericyte = c("Rgs5", "Pdgfrb", "Cspg4", "Acta2", "Tagln"),
  LSEC = c("Clec4g", "Stab2", "Stab1", "Lyve1"),
  Vascular_endothelial = c("Vwf", "Emcn", "Kdr", "Pecam1"),
  Cycling = c("Mki67", "Top2a", "Birc5", "Ube2c", "Pcna"),
  Mast_Baso = c("Fcer1a", "Ms4a2", "Cpa3", "Mcpt8", "Gata2")
))
marker_pct <- function(cl, genes) {
  d <- marker_stats[marker_stats$cluster == cl & marker_stats$gene %in% genes, , drop = FALSE]
  setNames(d$pct_positive, d$gene)
}
count_strong_markers <- function(cl, genes, cutoff = 25) {
  p <- marker_pct(cl, genes)
  sum(p >= cutoff, na.rm = TRUE)
}
summarize_cluster_markers <- function(cl, label) {
  genes <- evidence_markers[[label]]
  if (is.null(genes)) return("")
  d <- marker_stats[marker_stats$cluster == cl & marker_stats$gene %in% genes, , drop = FALSE]
  d <- d[order(d$pct_positive, decreasing = TRUE), , drop = FALSE]
  d <- d[d$pct_positive >= 10, , drop = FALSE]
  if (nrow(d) == 0) return("<10% positive for panel markers")
  paste(sprintf("%s %.0f%%", head(d$gene, 6), head(d$pct_positive, 6)), collapse = "; ")
}
l1_dec$key_marker_evidence <- mapply(summarize_cluster_markers, l1_dec$cluster, l1_dec$label)
l2_dec$key_marker_evidence <- mapply(summarize_cluster_markers, l2_dec$cluster, l2_dec$label)
for (i in seq_len(nrow(l2_dec))) {
  cl <- l2_dec$cluster[i]
  notes_i <- character()
  pdc_hits <- count_strong_markers(cl, c("Siglech", "Bst2", "Tcf4", "Ccr9", "Ly6d"))
  mono_hits <- count_strong_markers(cl, c("Ccr2", "Ly6c2", "Plac8", "Ms4a6c"))
  b_hits <- count_strong_markers(cl, c("Cd79a", "Ms4a1", "Ighm", "Pax5"))
  hsc_hits <- count_strong_markers(cl, l1_key_markers$HSC_Mesenchymal)
  endo_hits <- count_strong_markers(cl, l1_key_markers$Endothelial)

  if (l2_dec$label[i] == "pDC" && pdc_hits >= 3 && (mono_hits >= 2 || b_hits >= 2)) {
    l2_dec$confidence[i] <- "low"
    notes_i <- c(notes_i, "pDC markers co-occur with monocyte/B-lineage markers; review for a mixed state or residual doublet")
  }
  if (hsc_hits >= 2 && endo_hits >= 2) {
    l2_dec$confidence[i] <- "low"
    notes_i <- c(notes_i, "HSC/mesenchymal and endothelial programs both detected; review the lineage boundary")
  }
  if (l2_dec$label[i] == "Macrophages" &&
      count_strong_markers(cl, c("Spp1", "Trem2", "Arg1", "Mrc1", "Chil3")) >= 2 &&
      count_strong_markers(cl, c("Clec4f", "Cd5l", "Timd4", "Vsig4", "Marco")) < 2) {
    if (l2_dec$confidence[i] == "low") l2_dec$confidence[i] <- "medium"
    notes_i <- c(notes_i, "Spp1/Trem2-associated macrophage program; canonical KC markers are limited")
  }
  if (l2_dec$label[i] == "Cholangiocyte" &&
      count_strong_markers(cl, c("Epcam", "Krt19", "Krt7", "Sox9")) >= 2 &&
      l2_dec$confidence[i] == "low") {
    l2_dec$confidence[i] <- "medium"
  }
  if (l2_dec$n_cells[i] < 50) {
    notes_i <- c(notes_i, paste0("rare cluster (n=", l2_dec$n_cells[i], "); treat identity as provisional"))
  }
  if (l1_dec$confidence[match(cl, l1_dec$cluster)] == "low" || l2_dec$confidence[i] == "low") {
    notes_i <- c(notes_i, "low-confidence label; inspect marker dot plot/feature plots before biological interpretation")
  }
  l2_dec$review_note[i] <- paste(unique(notes_i), collapse = "; ")
}

cluster_summary <- merge(
  l1_dec[, c("cluster", "label", "n_cells", "confidence", "key_marker_evidence")],
  l2_dec[, c("cluster", "label", "confidence", "key_marker_evidence", "review_note")],
  by = "cluster", suffixes = c("_l1", "_l2"), sort = FALSE
)

# Write evidence tables before adding labels to the object.
write.csv(cl_l1, file.path(out_dir, "annotation_cluster_l1_scores.csv"))
write.csv(cl_l1_z, file.path(out_dir, "annotation_cluster_l1_zscores.csv"))
write.csv(cl_fine, file.path(out_dir, "annotation_cluster_fine_scores.csv"))
write.csv(cl_l2, file.path(out_dir, "annotation_cluster_l2_scores.csv"))
write.csv(cl_l2_z, file.path(out_dir, "annotation_cluster_l2_zscores.csv"))
write.csv(cl_refine, file.path(out_dir, "annotation_cluster_refinement_scores.csv"))
write.csv(cl_refine_z, file.path(out_dir, "annotation_cluster_refinement_zscores.csv"))
write.csv(marker_stats, file.path(out_dir, "annotation_marker_expression_by_cluster.csv"), row.names = FALSE)
write.csv(l1_dec, file.path(out_dir, "annotation_cluster_l1_decision.csv"), row.names = FALSE)
write.csv(l2_dec, file.path(out_dir, "annotation_cluster_l2_decision.csv"), row.names = FALSE)
write.csv(cluster_summary, file.path(out_dir, "annotation_cluster_summary.csv"), row.names = FALSE)

# Cell-level labels inherit the cluster decision; module scores are retained for auditing.
cl_l1_map <- setNames(l1_dec$label, l1_dec$cluster)
cl_l2_map <- setNames(l2_dec$label, l2_dec$cluster)
m$celltype_l1 <- unname(cl_l1_map[cluster_id])
m$celltype_l2 <- unname(cl_l2_map[cluster_id])
m$annotation_l1_confidence <- unname(setNames(l1_dec$confidence, l1_dec$cluster)[cluster_id])
m$annotation_l2_confidence <- unname(setNames(l2_dec$confidence, l2_dec$cluster)[cluster_id])
m$celltype_l1_confidence <- m$annotation_l1_confidence
m$celltype_l2_confidence <- m$annotation_l2_confidence
m$cell_state <- ifelse(cluster_id %in% rownames(cl_fine_z)[cl_fine_z[, "Cycling"] >= 1.2], "Cycling", "Non-cycling")
for (nm in rownames(scores_l1)) m[[paste0("score_l1_", nm)]] <- as.numeric(scores_l1[nm, ])
for (nm in rownames(scores_fine)) m[[paste0("score_fine_", nm)]] <- as.numeric(scores_fine[nm, ])
for (nm in rownames(scores_l2)) m[[paste0("score_l2_", nm)]] <- as.numeric(scores_l2[nm, ])
obj@meta.data <- m
Idents(obj) <- "celltype_l2"

saveRDS(obj, file.path(out_dir, annotation_rds_name), compress = "gzip")
write.csv(as.data.frame(table(m$celltype_l1)), file.path(out_dir, "annotation_celltype_l1_counts.csv"), row.names = FALSE)
write.csv(as.data.frame(table(m$celltype_l2)), file.path(out_dir, "annotation_celltype_l2_counts.csv"), row.names = FALSE)
write.csv(as.data.frame(table(m$celltype_l1, m$celltype_l2)), file.path(out_dir, "annotation_l1_l2_crosstab.csv"))

p1 <- DimPlot(obj, reduction = "umap", group.by = "celltype_l1", label = TRUE, repel = TRUE,
              raster = TRUE, pt.size = 0.28, shuffle = TRUE) + ggtitle(paste("GSE255834", annotation_label, "level 1 annotation"))
p2 <- DimPlot(obj, reduction = "umap", group.by = "celltype_l2", label = TRUE, repel = TRUE,
              raster = TRUE, pt.size = 0.28, shuffle = TRUE) + ggtitle(paste("GSE255834", annotation_label, "level 2 annotation"))
p3 <- DimPlot(obj, reduction = "umap", group.by = "cell_state", raster = TRUE,
              pt.size = 0.28, shuffle = TRUE) + ggtitle("Cell state flag")
p <- p1 | p2
ggsave(file.path(out_dir, "GSE255834_annotation_UMAP.png"), p, width = 16, height = 8, dpi = 300, bg = "white")
ggsave(file.path(out_dir, "GSE255834_annotation_UMAP.pdf"), p, width = 16, height = 8, bg = "white")
ggsave(file.path(out_dir, "GSE255834_cell_state_UMAP.png"), p3, width = 8, height = 6, dpi = 300, bg = "white")

p_l1 <- DotPlot(obj, features = unique(unlist(l1_score_sets)), group.by = "seurat_clusters", assay = "RNA") +
  RotatedAxis() + ggtitle("Level-1 lineage marker evidence by cluster")
p_l2 <- DotPlot(obj, features = unique(unlist(l2_markers)), group.by = "seurat_clusters", assay = "RNA") +
  RotatedAxis() + ggtitle("Immune level-2 marker evidence by cluster")
ggsave(file.path(out_dir, "GSE255834_level1_marker_DotPlot.png"), p_l1, width = 20, height = 9, dpi = 300, bg = "white")
ggsave(file.path(out_dir, "GSE255834_level1_marker_DotPlot.pdf"), p_l1, width = 20, height = 9, bg = "white")
ggsave(file.path(out_dir, "GSE255834_level2_marker_DotPlot.png"), p_l2, width = 22, height = 10, dpi = 300, bg = "white")
ggsave(file.path(out_dir, "GSE255834_level2_marker_DotPlot.pdf"), p_l2, width = 22, height = 10, bg = "white")

notes <- c(
  "Annotation uses cluster-level module scores plus the marker panels in results/annotion/mouse_liver_level1_annotation.html and mouse_liver_level2_immune_annotation.html.",
  "Module scores use Seurat AddModuleScore and are summarized by the current global clusters; the local BenMoshe reference object is not present in this GSE255834 input, so reference-majority voting is unavailable here.",
  "Level 1: Hepatocyte, Cholangiocyte, Endothelial, HSC/Mesenchymal, Myeloid, Lymphoid, with rare Erythroid/Mast_Baso/Mesothelial overrides.",
  "Level 2 immune: KC, Macrophages, Monocyte, Neutrophil, cDC, pDC, T, NK, B/Plasma; non-immune compartments are refined when marker evidence supports it.",
  "Level 2 non-immune: Hepatocyte, Cholangiocyte, LSEC/Vascular_endothelial, and HSC/Fibroblast/Pericyte; rare Mast_Baso remains a provisional label.",
  "Level-1 lineage confidence and level-2 subtype confidence are stored separately; mixed marker programs and rare clusters receive explicit review notes.",
  "Labels are cluster-inherited; raw cluster IDs, module scores, z-scores, marker positive fractions, average expression, and confidence are retained in the object and CSV evidence tables.",
  paste0("This annotation run used the ", annotation_label, " expression matrix."),
  "Low-confidence or unresolved labels require manual review against DotPlot/feature plots before biological claims."
)
writeLines(notes, file.path(out_dir, "annotation_notes.txt"))
message("ANNOTATION_DONE cells=", ncol(obj), " l1_types=", length(unique(m$celltype_l1)), " l2_types=", length(unique(m$celltype_l2)))
