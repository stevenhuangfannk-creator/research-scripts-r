# --- Code Block 1 ---
cc <- readRDS("ccc_outputs/cellchat_APAP24h.rds")
levels(cc@idents)

# --- Code Block 2 ---
w <- sort(cc@net$weight[, "SPP1+ Mac"], decreasing = TRUE)
c <- sort(cc@net$count[, "SPP1+ Mac"], decreasing = TRUE)
df <- data.frame(
  上游来源 = names(w),
  信号强度 = round(as.numeric(w), 4),
  互作条数 = as.numeric(c[names(w)]),
  stringsAsFactors = FALSE
)

knitr::kable(df, caption = "上游来源 → SPP1+ 巨噬细胞的信号强度与互作条数（按信号强度降序）")

# --- Code Block 3 ---
df_lr <- read.csv("ccc_outputs/cellchat_to_SPP1Mac_LR.csv", stringsAsFactors = FALSE)

by_path <- df_lr %>%
  group_by(pathway_name) %>%
  summarise(互作条数 = n(), 信号强度 = round(sum(prob), 4)) %>%
  arrange(desc(信号强度))

knitr::kable(by_path, caption = "上游 → SPP1+ 巨噬细胞的信号通路（按信号强度降序）")

# --- Code Block 4 ---
top_lr <- df_lr %>%
  group_by(source) %>%
  arrange(desc(prob)) %>%
  slice_head(n = 1) %>%
  select(source, ligand, receptor, pathway_name, prob) %>%
  arrange(desc(prob))

knitr::kable(
  data.frame(上游来源 = top_lr$source, 配体 = top_lr$ligand,
             受体 = top_lr$receptor, 通路 = top_lr$pathway_name,
             通信概率 = round(top_lr$prob, 4)),
  caption = "每个上游来源贡献最强的配-受体对"
)

