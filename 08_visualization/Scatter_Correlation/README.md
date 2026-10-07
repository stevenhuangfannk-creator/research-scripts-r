# Correlation visualization

Pearson: linear association between quantitative measurements; inspect outliers and confounding.
Spearman: monotonic rank association, useful with ordinal/skewed measurements; ties affect inference.
Neither estimates causation. Use biological samples as independent units; repeated observations need
an appropriate model. Explicit missingness policy, complete-pair n and BH-adjusted test family are
recorded by [correlation workflow](../../07_bulk_clinical_ml/correlation/METHOD_CARD.md).

[scatter + fit / CI](scatter_fit_v1.R), density-binned scatter, two-pair panel and BH-aware correlation
heatmap are rendered in the [Gallery](../../GALLERY.md). The iris pooled-species example is explicitly
confounded. A linear-model CI is not a confidence interval for Spearman rho. No Spearman CI is
claimed by the baseline cor.test implementation.
