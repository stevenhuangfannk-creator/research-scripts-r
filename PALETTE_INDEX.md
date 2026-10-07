# Palette Index

Journal-inspired palettes are ggsci assets, not official journal rules. CVD accessibility must be checked for the actual task, labels and contrast.

![Palette swatches](08_visualization/palettes/gallery/palette_swatches_v1.png)

| Palette ID | Type | Recommended n | Hex colors | Best for | Avoid when | CVD status | Source |
|---|---|---|---|---|---|---|---|
| npg_ggsci | categorical | 6 | #E64B35FF, #4DBBD5FF, #00A087FF, #3C5488FF, #F39B7FFF, #8491B4FF, #91D1C2FF, #DC0000FF, #7E6148FF, #B09C85FF | Small separated categories | Many touching categories or continuous values | not_certified | https://nanx.me/ggsci/ (journal-inspired package palettes, not official journal prescriptions) |
| aaas_ggsci | categorical | 6 | #3B4992FF, #EE0000FF, #008B45FF, #631879FF, #008280FF, #BB0021FF, #5F559BFF, #A20056FF, #808180FF, #1B1919FF | Categorical overview | Accessibility-critical distinctions without redundant labels | not_certified | https://nanx.me/ggsci/ (journal-inspired package palettes, not official journal prescriptions) |
| nejm_ggsci | categorical | 5 | #BC3C29FF, #0072B5FF, #E18727FF, #20854EFF, #7876B1FF, #6F99ADFF, #FFDC91FF, #EE4C97FF | Small clinical groups | More than 8 categories | not_certified | https://nanx.me/ggsci/ (journal-inspired package palettes, not official journal prescriptions) |
| lancet_ggsci | categorical | 5 | #00468BFF, #ED0000FF, #42B540FF, #0099B4FF, #925E9FFF, #FDAF91FF, #AD002AFF, #ADB6B6FF, #1B1919FF | Categorical groups | Quantitative continuous magnitude | not_certified | https://nanx.me/ggsci/ (journal-inspired package palettes, not official journal prescriptions) |
| jama_ggsci | categorical | 5 | #374E55FF, #DF8F44FF, #00A1D5FF, #B24745FF, #79AF97FF, #6A6599FF, #80796BFF | Small muted categories | More than 7 categories | not_certified | https://nanx.me/ggsci/ (journal-inspired package palettes, not official journal prescriptions) |
| okabe_ito | categorical | 8 | #E69F00, #56B4E9, #009E73, #F0E442, #0072B2, #D55E00, #CC79A7, #000000 | Up to 8 discrete groups, with labels/shapes | Yellow thin lines on white; excess categories | designed_for_common_CVD; verify task contrast | https://jfly.uni-koeln.de/color/ |
| viridis | continuous | continuous | #440154FF, #414487FF, #2A788EFF, #22A884FF, #7AD151FF, #FDE725FF | Nonnegative expression/activity | Signed contrasts around zero | designed_for_common_CVD | https://cran.r-project.org/package=viridisLite |
| cividis | continuous | continuous | #00204DFF, #31446BFF, #666970FF, #958F78FF, #CBBA69FF, #FFEA46FF | Accessible ordered magnitude | Unrelated categories | designed_for_common_CVD | https://cran.r-project.org/package=viridisLite |
| blue_white_red | diverging | continuous | #2166AC, #F7F7F7, #B2182B | Signed differences with meaningful zero | Unsigned expression levels | not_certified; add signed labels | https://colorbrewer2.org/ |

[Palette code](08_visualization/palettes/palettes.R) · [registry](registry/palettes.yml) · [fixed cell and condition colors](registry/celltype_colors.yml). Capacity checks reject excessive categorical colors; do not interpolate arbitrary cell identities.
