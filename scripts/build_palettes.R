palettes <- list()
add <- function(id, type, colors, best_for, avoid_when, safe, source, recommended_n = NULL) {
  palettes[[length(palettes) + 1L]] <<- list(id = id, type = type, recommended_n = recommended_n,
      hex_colors = unname(colors), best_for = best_for, avoid_when = avoid_when,
      colorblind_safe = safe, source = source)
}
ggsci_source <- "https://nanx.me/ggsci/ (journal-inspired package palettes, not official journal prescriptions)"
add("npg_ggsci", "categorical", ggsci::pal_npg("nrc")(10), "Small separated categories", "Many touching categories or continuous values", "not_certified", ggsci_source, 6)
add("aaas_ggsci", "categorical", ggsci::pal_aaas("default")(10), "Categorical overview", "Accessibility-critical distinctions without redundant labels", "not_certified", ggsci_source, 6)
add("nejm_ggsci", "categorical", ggsci::pal_nejm("default")(8), "Small clinical groups", "More than 8 categories", "not_certified", ggsci_source, 5)
add("lancet_ggsci", "categorical", ggsci::pal_lancet("lanonc")(9), "Categorical groups", "Quantitative continuous magnitude", "not_certified", ggsci_source, 5)
add("jama_ggsci", "categorical", ggsci::pal_jama("default")(7), "Small muted categories", "More than 7 categories", "not_certified", ggsci_source, 5)
okabe <- c("#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000")
add("okabe_ito", "categorical", okabe, "Up to 8 discrete groups, with labels/shapes", "Yellow thin lines on white; excess categories", "designed_for_common_CVD; verify task contrast", "https://jfly.uni-koeln.de/color/", 8)
add("viridis", "continuous", viridisLite::viridis(6), "Nonnegative expression/activity", "Signed contrasts around zero", "designed_for_common_CVD", "https://cran.r-project.org/package=viridisLite")
add("cividis", "continuous", viridisLite::cividis(6), "Accessible ordered magnitude", "Unrelated categories", "designed_for_common_CVD", "https://cran.r-project.org/package=viridisLite")
add("blue_white_red", "diverging", c("#2166AC", "#F7F7F7", "#B2182B"), "Signed differences with meaningful zero", "Unsigned expression levels", "not_certified; add signed labels", "https://colorbrewer2.org/")
jsonlite::write_json(list(schema_version = 1, palettes = palettes), "registry/palettes.yml", pretty = TRUE, auto_unbox = TRUE, null = "null")
colors <- list(Macrophage = "#D55E00", Monocyte = "#E69F00", Neutrophil = "#CC79A7", "T cell" = "#0072B2",
               "B cell" = "#56B4E9", NK = "#009E73", Fibroblast = "#8C6BB1", Endothelial = "#4D4D4D",
               Epithelial = "#66A61E", "Plasma cell" = "#A6761D")
jsonlite::write_json(list(schema_version = 1, colors = colors,
   caveat = "Stable identity mapping; >8 colors are not certified CVD-safe. Use labels/facets as well.",
   condition_colors = list(Control = "#0072B2", Treatment = "#D55E00")),
   "registry/celltype_colors.yml", pretty = TRUE, auto_unbox = TRUE)
cat(length(palettes), "palettes registered from installed APIs\n")
