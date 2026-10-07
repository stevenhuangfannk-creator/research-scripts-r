"""Diagnose the PI depth stop gate without refitting or changing its threshold."""
from pathlib import Path
import json

import anndata as ad
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/phase4b/cell2location_mapping/pi"
FIG = ROOT / "figures/phase4b/cell2location/pi"
mpl.rcParams.update({"font.family":"sans-serif", "font.size":7, "pdf.fonttype":42, "svg.fonttype":"none"})


def rho(x, y):
    return float(spearmanr(x, y).statistic)


def main():
    a = ad.read_h5ad(OUT / "posterior.h5ad")
    means = pd.read_csv(OUT / "abundance_means.tsv.gz", sep="\t", index_col=0)
    fractions = pd.read_csv(OUT / "abundance_fractions.tsv.gz", sep="\t", index_col=0)
    modules = pd.read_csv(OUT / "normalized_marker_module_scores.tsv.gz", sep="\t", index_col=0)
    assert means.index.equals(a.obs_names) and fractions.index.equals(means.index) and modules.index.equals(means.index)
    depth = a.obs.original_total_counts.to_numpy(float)
    genes = a.obs.original_detected_genes.to_numpy(float)
    detection = np.asarray(a.uns["mod"]["post_sample_means"]["detection_y_s"]).ravel()
    assert detection.shape == depth.shape
    # Rank residual correlation is a descriptive sensitivity check, not a causal adjustment.
    design = np.column_stack([np.ones(len(depth)), rankdata(depth), rankdata(genes)])
    def residual(x):
        ranks = rankdata(x)
        return ranks - design @ np.linalg.lstsq(design, ranks, rcond=None)[0]
    rows = []
    for ct in means:
        score = modules[ct].to_numpy()
        rows.append({"cell_type":ct, "abundance_depth_adjusted_marker_rho":float(np.corrcoef(residual(means[ct]),residual(score))[0,1]),
                     "fraction_depth_adjusted_marker_rho":float(np.corrcoef(residual(fractions[ct]),residual(score))[0,1])})
    pd.DataFrame(rows).to_csv(OUT / "depth_adjusted_marker_diagnostic.tsv", sep="\t", index=False)
    spot = pd.DataFrame({"original_counts":depth, "detected_genes":genes,
                         "total_abundance":means.sum(axis=1), "posterior_mean_detection_y_s":detection}, index=a.obs_names)
    spot.to_csv(OUT / "depth_detection_diagnostic.tsv.gz", sep="\t", compression="gzip")
    summary = {"total_abundance_counts_rho":rho(spot.total_abundance,depth),
               "total_abundance_genes_rho":rho(spot.total_abundance,genes),
               "detection_counts_rho":rho(detection,depth), "detection_abundance_rho":rho(detection,spot.total_abundance),
               "detection_mean":float(detection.mean()), "detection_cv":float(detection.std()/detection.mean()),
               "detection_p05_p95":np.quantile(detection,[.05,.95]).tolist(),
               "decision":"PI QC remains blocked; Healthy not run. No threshold relaxation or reference relabeling.",
               "interpretation":"High depth association does not prove a technical artifact: true density/RNA content and detection are confounded without independent nuclei counts or parameter sensitivity. Rank residuals are descriptive, not independent validation."}
    (OUT / "depth_diagnostic_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    fig,axes=plt.subplots(1,3,figsize=(10,3),layout="constrained")
    for ax,y,label in zip(axes,[spot.total_abundance,detection,genes],["Total inferred abundance","Posterior detection sensitivity","Detected genes"]):
        ax.scatter(depth,y,s=5,alpha=.6)
        ax.set(xlabel="Original counts",ylabel=label,title=f"Spearman rho={rho(depth,y):.3f}")
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.ticklabel_format(axis="x",style="sci",scilimits=(0,0))
    for ext in ["png","pdf","svg"]:
        fig.savefig(FIG / f"depth_detection_diagnostic.{ext}",dpi=300,bbox_inches="tight")
    plt.close(fig)
    print(json.dumps(summary,indent=2))


if __name__ == "__main__":
    main()
