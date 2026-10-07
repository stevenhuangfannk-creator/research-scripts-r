"""Diagnostic QC for one independent spatial mapping; no biological testing."""
from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

import anndata as ad
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from scipy.stats import spearmanr

from importlib.util import module_from_spec, spec_from_file_location

ROOT = Path(__file__).resolve().parents[1]
spec = spec_from_file_location("reference_qc", ROOT / "scripts/17_qc_cell2location_reference.py")
module = module_from_spec(spec)
spec.loader.exec_module(module)
MARKERS = module.MARKERS.copy()
MARKERS["Macrophages"] = ["C1QA", "C1QB", "C1QC", "LST1", "TYROBP", "FCER1G", "CTSS", "CD68", "MS4A7"]
MARKERS["Monocytes"] = ["FCN1", "S100A8", "S100A9", "LST1", "CTSS", "CTSD"]
MARKERS["Plasma cells"] = ["MZB1", "JCHAIN", "SDC1", "XBP1", "PRDM1", "DERL3"]
mpl.rcParams.update({"font.family": "sans-serif", "font.size": 7, "pdf.fonttype": 42,
                     "svg.fonttype": "none", "axes.spines.top": False, "axes.spines.right": False})


def rho(x: np.ndarray, y: np.ndarray) -> float:
    if np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(spearmanr(x, y).statistic)


def save(fig: plt.Figure, folder: Path, name: str) -> None:
    fig.savefig(folder / f"{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(folder / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(folder / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", required=True)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    key = "pi" if args.sample == "PI_spatial" else args.sample
    if args.smoke:
        key = f"smoke/{key}"
    out = ROOT / "results/phase4b/cell2location_mapping" / key
    figpath = ROOT / "figures/phase4b/cell2location" / key
    a = ad.read_h5ad(out / "posterior.h5ad")
    model = json.loads((out / "mapping_model_summary.json").read_text())
    assert model["smoke"] == args.smoke and model["reference_commit"].startswith("8496f3a")
    means = pd.read_csv(out / "abundance_means.tsv.gz", sep="\t", index_col=0)
    q05 = pd.read_csv(out / "abundance_q05.tsv.gz", sep="\t", index_col=0)
    q95 = pd.read_csv(out / "abundance_q95.tsv.gz", sep="\t", index_col=0)
    stds = pd.read_csv(out / "abundance_stds.tsv.gz", sep="\t", index_col=0)
    assert means.index.equals(a.obs_names) and means.shape == (a.n_obs, 14)
    for frame in [q05, q95, stds]:
        assert frame.index.equals(means.index) and frame.columns.equals(means.columns)
    counts = a.layers["counts"]
    depth = a.obs["original_total_counts"].to_numpy(float)
    genes_detected = a.obs["original_detected_genes"].to_numpy(float)
    lib = np.asarray(counts.sum(axis=1)).ravel()
    total = means.sum(axis=1).to_numpy()
    fractions = means.div(np.maximum(total, 1e-8), axis=0)
    normalized = counts.multiply((1e4 / np.maximum(lib, 1))[:, None]).tocsr()
    rows, gene_rows, modules = [], [], {}
    for ct in means.columns:
        available = [g for g in MARKERS[ct] if g in a.var_names]
        idx = a.var_names.get_indexer(available)
        raw = counts[:, idx].toarray()
        norm = np.log1p(normalized[:, idx].toarray())
        score = norm.mean(axis=1)
        modules[ct] = score
        values = means[ct].to_numpy()
        lower, upper = q05[ct].to_numpy(), q95[ct].to_numpy()
        width = (upper - lower) / np.maximum(values, 1e-8)
        k = max(1, int(np.ceil(a.n_obs * .01)))
        marker_rho = rho(values, score)
        fraction_rho = rho(fractions[ct].to_numpy(), score)
        width_med = float(np.median(width))
        detected = float(np.mean(raw.sum(axis=1) > 0))
        # Heuristic diagnostic categories, not calibrated posterior accuracy.
        if marker_rho >= .30 and fraction_rho >= .20 and width_med < 2 and detected >= .10:
            reliability = "reliable"
        elif marker_rho >= .10 and fraction_rho >= -.10 and detected >= .05:
            reliability = "partially reliable"
        else:
            reliability = "questionable"
        rows.append({"sample_id": args.sample, "cell_type": ct, "mean": values.mean(),
                     "median": np.median(values), "p95": np.quantile(values,.95), "max": values.max(),
                     "median_q05": np.median(lower), "fraction_mean_lt_0_1": np.mean(values < .1),
                     "fraction_q05_gt_1": np.mean(lower > 1), "top_1pct_abundance_share": np.sort(values)[-k:].sum()/values.sum(),
                     "median_relative_90pct_credible_width": width_med,
                     "normalized_marker_rho": marker_rho, "fraction_marker_rho": fraction_rho,
                     "raw_marker_rho": rho(values,raw.sum(axis=1)), "counts_rho": rho(values,depth),
                     "detected_genes_rho": rho(values,genes_detected), "fraction_counts_rho": rho(fractions[ct].to_numpy(),depth),
                     "marker_detected_spot_fraction": detected, "available_markers": ";".join(available),
                     "reliability": reliability})
        for j,gene in enumerate(available):
            gene_rows.append({"cell_type":ct,"gene":gene,"detected_spot_fraction":np.mean(raw[:,j]>0),
                              "abundance_normalized_expression_rho":rho(values,norm[:,j]),
                              "fraction_normalized_expression_rho":rho(fractions[ct].to_numpy(),norm[:,j])})
    qc = pd.DataFrame(rows)
    qc.to_csv(out / "cell_type_mapping_qc.tsv",sep="\t",index=False)
    pd.DataFrame(gene_rows).to_csv(out / "marker_concordance.tsv",sep="\t",index=False)
    module_scores = pd.DataFrame(modules,index=a.obs_names)
    module_scores.to_csv(out / "normalized_marker_module_scores.tsv.gz",sep="\t",compression="gzip")
    fractions.to_csv(out / "abundance_fractions.tsv.gz",sep="\t",compression="gzip")
    means.corr(method="spearman").to_csv(out / "abundance_correlations.tsv",sep="\t")
    fractions.corr(method="spearman").to_csv(out / "composition_correlations.tsv",sep="\t")
    top = pd.DataFrame({"top_cell_type":means.idxmax(axis=1),"top_abundance_fraction":fractions.max(axis=1),
                        "total_abundance":total,"original_counts":depth,"original_detected_genes":genes_detected},index=a.obs_names)
    top.to_csv(out / "spot_composition.tsv.gz",sep="\t",compression="gzip")
    history = pd.read_csv(out / "training_history.tsv",sep="\t",index_col=0)
    loss = history[next(c for c in history if "elbo" in c.lower())].to_numpy(float)
    severe_mismatch = qc.loc[(qc.normalized_marker_rho < -.25) & (qc.fraction_marker_rho < -.25) &
                             (qc.marker_detected_spot_fraction >= .2),"cell_type"].tolist()
    depth_rho, gene_rho = rho(total,depth),rho(total,genes_detected)
    depth_dominance = abs(depth_rho) > .85 and abs(gene_rho) > .85
    joint_myeloid = means["Macrophages"].to_numpy() + means["Monocytes"].to_numpy()
    myeloid_diagnostic = {
        "joint_abundance_macrophage_marker_rho": rho(joint_myeloid, modules["Macrophages"]),
        "joint_fraction_macrophage_marker_rho": rho(joint_myeloid/np.maximum(total,1e-8),modules["Macrophages"]),
        "macrophage_monocyte_abundance_rho": rho(means["Macrophages"].to_numpy(),means["Monocytes"].to_numpy()),
        "interpretation_limit": "Shared myeloid markers cannot uniquely validate macrophage versus monocyte attribution",
    }
    gates = {"formal_fit":not args.smoke,
             "loss_finite_and_decreased":bool(np.isfinite(loss).all() and loss[-1]<loss[0]),
             "loss_tail_relative_slope_lt_2e_5":bool(abs(model["tail_relative_slope"])<2e-5),
             "posterior_finite_nonnegative":all(bool(np.isfinite(frame.to_numpy()).all() and (frame.to_numpy()>=0).all()) for frame in [means,q05,q95,stds]),
             "quantiles_ordered":bool((q95.to_numpy()>=q05.to_numpy()).all()),
             "median_total_lt_500_max_lt_1000":bool(np.median(total)<500 and total.max()<1000),
             "no_severe_marker_mismatch":len(severe_mismatch)==0,
             "depth_does_not_clearly_dominate_total":not depth_dominance}
    summary = {"sample_id":args.sample,"reference_commit":model["reference_commit"],
               "median_total_abundance":float(np.median(total)),"maximum_total_abundance":float(total.max()),
               "total_abundance_counts_spearman":depth_rho,"total_abundance_genes_spearman":gene_rho,
               "severe_marker_mismatch":severe_mismatch,"macrophage_reliability":qc.loc[qc.cell_type.eq("Macrophages"),"reliability"].iloc[0],
               "myeloid_separability_diagnostic":myeloid_diagnostic,
               "reliability_by_type":qc.set_index("cell_type").reliability.to_dict(),
               "gates":gates,"automatic_gate_pass":all(gates.values()),
               "limitations":"Marker concordance is an internal diagnostic using the fitted expression data, not independent validation. Broad myeloid states overlap; prior cells/spot uncalibrated. No disease-effect inference.",
               "threshold_provenance":"USER/CODEX predeclared diagnostic heuristics; inspection of tissue maps remains required"}
    (out / "mapping_qc_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")

    provenance=a.uns["spatial_provenance"]
    imagepath=ROOT/provenance["image_path"]
    if imagepath.suffix==".gz":
        with gzip.open(imagepath,"rb") as stream: image=np.asarray(Image.open(stream).convert("RGB"))
    else: image=np.asarray(Image.open(imagepath).convert("RGB"))
    scale=provenance["scalefactors"]["tissue_hires_scalef"]
    x,y=a.obs.pxl_col.to_numpy()*scale,a.obs.pxl_row.to_numpy()*scale
    def spatial(ax,values,label,vmax=None):
        ax.imshow(image,alpha=.35)
        artist=ax.scatter(x,y,c=values,cmap="magma",s=8,vmin=0,vmax=vmax,linewidths=0,rasterized=True)
        margin=.05*max(np.ptp(x),np.ptp(y))
        ax.set_xlim(x.min()-margin,x.max()+margin)
        ax.set_ylim(y.max()+margin,y.min()-margin)
        ax.set(title=label);ax.set_axis_off()
        return artist
    figure,axes=plt.subplots(3,5,figsize=(14,8),layout="constrained")
    for ax,ct in zip(axes.flat,means.columns):
        artist=spatial(ax,q05[ct],ct)
        figure.colorbar(artist,ax=ax,fraction=.04,pad=.01)
    axes.flat[-1].axis("off")
    figure.suptitle(f"{args.sample}: lower 5% posterior abundance (individual scales)")
    save(figure,figpath,"all_cell_types_q05_maps")
    for ct in means.columns:
        figure,axes=plt.subplots(1,4,figsize=(12,3),layout="constrained")
        vmax=float(means[ct].max())
        data=[q05[ct],means[ct],module_scores[ct],(q95[ct]-q05[ct])/np.maximum(means[ct],1e-8)]
        titles=["5% quantile","Posterior mean","Normalized marker module","Relative 90% credible width"]
        for i,(ax,vals,title) in enumerate(zip(axes,data,titles)):
            artist=spatial(ax,vals,title,vmax=vmax if i<2 else None)
            figure.colorbar(artist,ax=ax,fraction=.04,pad=.01)
        figure.suptitle(f"{args.sample}: {ct}")
        save(figure,figpath,"type_"+ct.lower().replace(" ","_").replace("/","_"))
    figure,axes=plt.subplots(1,3,figsize=(11,3.4),layout="constrained")
    axes[0].boxplot([means[c] for c in means],orientation="horizontal",tick_labels=list(means),showfliers=False)
    axes[0].tick_params(axis="y",labelsize=6);axes[0].set(xlabel="Posterior mean abundance")
    axes[1].scatter(depth,total,s=5);axes[1].set(xlabel="Original counts",ylabel="Total abundance",title=f"Depth rho={depth_rho:.2f}")
    axes[2].scatter(module_scores.Macrophages,means.Macrophages,s=5)
    axes[2].set(xlabel="Normalized macrophage marker module",ylabel="Macrophage abundance")
    save(figure,figpath,"mapping_qc_overview")
    figure,ax=plt.subplots(figsize=(6,5),layout="constrained")
    corr=fractions.corr(method="spearman")
    artist=ax.imshow(corr,vmin=-1,vmax=1,cmap="RdBu_r")
    ax.set_xticks(range(14),means.columns,rotation=65,rotation_mode="anchor",ha="right",fontsize=5)
    ax.set_yticks(range(14),means.columns,fontsize=5)
    ax.set_title("Exploratory co-localization: abundance fractions")
    figure.colorbar(artist,ax=ax,label="Spearman rho")
    save(figure,figpath,"composition_correlations")
    print(json.dumps(summary,indent=2))


if __name__=="__main__": main()
