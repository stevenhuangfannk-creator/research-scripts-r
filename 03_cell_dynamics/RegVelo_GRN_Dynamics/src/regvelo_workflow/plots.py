"""Scientific gallery from saved numerical results; missing results remain NOT_RUN."""
import json
import sys
import traceback
from pathlib import Path


CATALOG = [
    ("A01", "Cell Type UMAP", "细胞类型UMAP", "Which annotated cell classes are present?", "Observed", "Annotations and embedding do not validate fine-state identity."),
    ("A02", "Development Stage UMAP", "发育阶段UMAP", "Where are sampled stages represented?", "Observed", "Somite stage is ordinal; it is not elapsed hours."),
    ("A03", "Spliced Unspliced QC", "剪接计数质量检查", "Is splice signal detected across cells?", "Observed", "Counts and detection do not establish a valid velocity direction."),
    ("A04", "GRN Coverage", "GRN覆盖率", "Which features and prior regulators survived preprocessing?", "Observed / Prior", "Static prior coverage is not evidence of active direct regulation."),
    ("B01", "Velocity Stream", "RNA速度流场", "What direction does RegVelo predict on the embedding?", "Model-predicted", "UMAP streamlines project high-dimensional predictions; direction needs biological QC."),
    ("B02", "Velocity Arrows", "RNA速度箭头", "How heterogeneous are projected cell velocities?", "Model-predicted", "Arrows are projected model velocities, not observed cell motion."),
    ("B03", "Latent Time", "潜在时间", "How does mean inferred time vary across cells?", "Model-predicted", "Mean fit_t is min-max scaled, not calibrated elapsed time."),
    ("B04", "Velocity Phase Portrait", "速度相图", "How do selected genes relate to RNA moments and velocity?", "Observed / Model-predicted", "Moment relationships do not independently validate kinetic assumptions."),
    ("B05", "Training Curve", "模型训练曲线", "How did the recorded objective evolve?", "Model-predicted", "Finite or decreasing loss alone does not prove convergence or biological validity."),
    ("B06", "Velocity Uncertainty", "速度不确定性", "Where is saved posterior velocity uncertainty high?", "Model-predicted", "Requires saved posterior uncertainty; mean velocity cannot recover it."),
    ("B07", "RegVelo vs scVelo", "RegVelo与scVelo对照", "Do the two saved velocity fields agree?", "Model-predicted", "Agreement does not identify a ground-truth direction."),
    ("C01", "Macrostates", "宏观状态", "Which macrostates were inferred?", "Model-predicted", "Macrostates depend on the transition kernel and state-number choice."),
    ("C02", "Terminal States", "终末状态", "Which cells define the terminal sets?", "Model-predicted", "Terminal definitions must be supported by developmental biology."),
    ("C03", "Fate Probabilities", "命运概率", "How is absorption probability distributed?", "Model-predicted", "Probabilities are conditional on the model and frozen terminal definitions."),
    ("C04", "Commitment Score", "命运承诺评分", "Where is predicted terminal fate concentration strongest?", "Model-predicted", "One minus normalized Shannon entropy is not irreversible experimental commitment."),
    ("C05", "Fate Probability Heatmap", "命运概率热图", "How do annotated classes differ in mean predicted fate?", "Model-predicted", "Group means hide within-class variation and are not independent biological replicates."),
    ("D01", "TF Target Network", "TF靶基因网络", "What are the strongest saved effective connections?", "Prior / Model-predicted", "Model weight arrows denote API orientation, not proven causal binding."),
    ("D02", "GRN Adjacency Heatmap", "GRN邻接热图", "What signed weights connect selected regulators and targets?", "Model-predicted", "Display selection is based on absolute weights; full edges remain in the source table."),
    ("D03", "Regulon Ranking", "Regulon排序", "Which regulators have the largest summed absolute effective weights?", "Model-predicted", "Large summed weight is not validated TF importance or clinical effect."),
    ("D04", "Regulatory Weight Distribution", "调控权重分布", "How are signed trained weights distributed?", "Model-predicted", "fc1 weights differ from normalized-expression Jacobians."),
    ("D05", "Prior vs Inferred GRN", "先验与推断GRN比较", "How many effective learned edges overlap the prior?", "Prior / Model-predicted", "New model edges lack experimental support; threshold affects counts."),
    ("E01", "Baseline vs KO Velocity", "基线与KO速度比较", "How does a paired regulon block change projected velocity?", "Model-predicted", "Paired posterior draws and separate KO embeddings are required; this is not CRISPR."),
    ("E02", "Cell-wise Perturbation Effect", "逐细胞扰动效应", "Which cells change most in velocity magnitude or direction?", "Model-predicted", "L2 velocity difference and 1-cosine are model scores, not expression log2FC."),
    ("E03", "Fate Probability Difference", "命运概率差", "How do frozen-terminal fate probabilities change?", "Model-predicted", "KO minus paired baseline is conditional on the same terminal cell sets."),
    ("E04", "Depletion Enrichment", "命运消耗富集", "What does the official depletion statistic report?", "Model-predicted", "ROC AUC has a 0.5 neutral reference; pooled-cell ranksums/BH values do not provide biological-replicate evidence."),
    ("E05", "TF Perturbation Ranking", "TF扰动排序", "How do tested TFs rank by mean velocity change?", "Model-predicted", "Ranks compare only tested targets and cannot establish disease drivers."),
    ("E06", "GRN Before After KO", "KO前后GRN", "Were the selected TF downstream weights blocked?", "Model-predicted", "Removing model weights simulates regulon blockade, not biological gene deletion."),
]

CHINESE_NOTES = {
    "A01":"展示已有细胞类型标签在UMAP上的位置；聚集位置不证明精细亚群身份或动力学方向。",
    "A02":"按明确的体节阶段顺序显示取样信息；阶段序号不等于真实经过的小时数。",
    "A03":"检查保存的剪接层总量及每细胞检出基因数；已处理层单位不假设为原始UMI，检出不等于速度信号可靠。",
    "A04":"展示特征过滤及实际对齐先验的regulator、target和边覆盖；有边不等于调控在该细胞中活跃。",
    "B01":"将RegVelo预测速度投影为UMAP流线，用于审查方向；投影不是实际细胞运动，仍需发育证据。",
    "B02":"显示各细胞的预测速度箭头和局部差异；箭头的嵌入长度不是实验迁移速度。",
    "B03":"显示各细胞mean fit_t经min-max归一化后的相对顺序；不把它解释为真实时钟。",
    "B04":"查看选定基因Ms/Mu关系与预测速度；本图不宣称拟合相线或独立验证动力学假设。",
    "B05":"展示实际记录的训练目标变化；有限或下降的loss不能单独证明收敛、稳健或生物学正确。",
    "B06":"展示已保存的后验速度不确定性；没有保存抽样离散度时保持NOT_RUN，不能由平均速度反推。",
    "B07":"在同细胞与基因下比较RegVelo和scVelo stochastic投影；一致性不等于识别了真实方向。",
    "C01":"展示GPCCA推断的宏观状态；状态边界依赖转移核和状态数，不能自动当作真实亚型。",
    "C02":"标示冻结的终末细胞集合，并保留未分配细胞；终末定义仍需细胞身份和发育过程支持。",
    "C03":"展示模型转移链对各终末集合的吸收概率；这是给定核与终末定义的条件预测。",
    "C04":"用1减去归一化Shannon熵表示命运概率集中程度；不等于真实不可逆命运承诺。",
    "C05":"比较已有细胞标签内的平均命运概率；均值会隐藏群内差异，细胞不能当独立生物学重复。",
    "D01":"显示绝对有效fc1权重最强的40条边；箭头服从模型API方向，不表示已证实直接结合或因果。",
    "D02":"以target为行、regulator为列展示选定有符号权重；按绝对权重选图，完整边表保留供审查。",
    "D03":"按有效边绝对权重之和排列regulator；排序不是已验证TF功能重要性或治疗效应。",
    "D04":"查看阈值以上的有符号训练权重分布；fc1参数与归一化表达Jacobian不同，均不等于实验结合。",
    "D05":"比较有效模型边与先验的重合、丢失和新增；新增连接尚无实验支持，数量依赖cutoff。",
    "E01":"比较配对后验基线与单独重算的regulon阻断速度投影；这是模型内虚拟KO，不是CRISPR实验。",
    "E02":"显示逐细胞高维速度L2差及1-cosine方向差；这些是模型分数，不是表达log2FC或实验效应量。",
    "E03":"展示KO减配对基线的命运概率差；原始与扰动使用同一细胞、特征和冻结终末细胞集合。",
    "E04":"展示官方ROC AUC depletion likelihood及NULL对照，以0.5为无变化参照；大于0.5指向模型内消耗、小于0.5指向富集。p/FDR来自pooled-cell单侧ranksums/BH，不能当作独立生物学重复或真实实验效应。",
    "E05":"按平均逐细胞速度L2变化比较实际测试的TF；只覆盖本次目标，不能据此宣布疾病驱动因子。",
    "E06":"检查所选TF下游模型权重阻断前后的数值；删除模型连接不等于生物学删除基因。",
}


def run_visualize(config, output):
    import anndata as ad
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy import sparse

    output = Path(output)
    figures = output / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"], "font.size": 8, "axes.titlesize": 10,
                         "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7,
                         "legend.fontsize": 7, "figure.dpi": 110, "savefig.dpi": 300,
                         "pdf.fonttype": 42, "svg.fonttype": "none", "axes.spines.top": False,
                         "axes.spines.right": False, "figure.facecolor": "white"})
    cache = {}

    def read(name):
        path = Path(config["input"]) if name == "input" else output / f"{name}.h5ad"
        if path.is_file() and name not in cache:
            cache[name] = ad.read_h5ad(path)
        return cache.get(name)

    def table(name, index=None):
        path = output / "tables" / f"{name}.csv"
        return pd.read_csv(path, index_col=index, keep_default_na=name!="perturbation_depletion") if path.is_file() else None

    raw = read("input")
    prepared = read("prepared")
    velocity = read("velocity")
    fate = read("fate")
    data = prepared if prepared is not None else raw
    embedding_source = output / "prepared.h5ad" if prepared is not None else Path(config["input"])
    group = config.get("group_key", "cell_type")
    time = config.get("time_key", "stage")
    categories = list(raw.obs[group].cat.categories if isinstance(raw.obs[group].dtype, pd.CategoricalDtype)
                      else pd.unique(raw.obs[group])) if raw is not None and group in raw.obs else []
    palette = {str(c):matplotlib.colors.to_hex(plt.get_cmap("tab20")(i % 20)) for i,c in enumerate(categories)}
    (figures / "cell_type_colors.json").write_text(json.dumps(palette, indent=2), encoding="utf-8")
    entries = {item[0]:dict(zip(["id", "english_name", "chinese_name", "scientific_question", "evidence_label", "limitations"], item))
               for item in CATALOG}
    for entry in entries.values():
        entry.update(status="NOT_RUN", reason="Required saved numerical results are unavailable.",
                     output_file="", source_csv="", metadata_file="", code_entry="regvelo_workflow.plots.run_visualize",
                     method="", input="", biological_interpretation=CHINESE_NOTES[entry["id"]])
    wrapper = Path(__file__).resolve().parents[2] / "scripts" / "regvelo.py"
    command = f'{"& " if sys.platform == "win32" else ""}"{sys.executable}" "{wrapper}" visualize --config "{output / "resolved_config.json"}"'
    artifacts = [str(figures / "cell_type_colors.json")]
    smoke = bool(config.get("prepare", {}).get("max_cells"))

    def base_frame(adata):
        xy = np.asarray(adata.obsm["X_umap"])
        frame = pd.DataFrame({"cell":adata.obs_names, "UMAP1":xy[:,0], "UMAP2":xy[:,1]})
        if group in adata.obs:
            frame[group] = adata.obs[group].astype(str).to_numpy()
        return frame

    def scatter(ax, frame, key, title, categorical=False, vmin=None, vmax=None, cmap="viridis"):
        if categorical:
            values = frame[key].fillna("Unassigned").astype(str)
            labels = list(pd.unique(values))
            colors = {v:palette.get(v,"#bdbdbd" if v=="Unassigned" else matplotlib.colors.to_hex(plt.get_cmap("tab20")(i % 20))) for i,v in enumerate(sorted(labels))}
            for label in labels:
                mask = values == label
                ax.scatter(frame.loc[mask,"UMAP1"], frame.loc[mask,"UMAP2"], s=9, c=colors.get(label,"#bdbdbd"), label=label, linewidths=0, rasterized=False)
            ax.legend(loc="upper left", bbox_to_anchor=(1.01,1), frameon=False, markerscale=1.3)
        else:
            im=ax.scatter(frame.UMAP1, frame.UMAP2, c=frame[key], s=10, cmap=cmap, vmin=vmin, vmax=vmax, linewidths=0)
            plt.colorbar(im, ax=ax, fraction=0.04, pad=0.03, label=key)
        ax.set(title=title, xlabel="UMAP 1", ylabel="UMAP 2")
        ax.set_aspect("equal", adjustable="datalim")

    def draw(identifier, source, method, inputs, builder):
        entry=entries[identifier]
        stem=figures / identifier
        entry.update(method=method, input="; ".join(str(p) for p in inputs))
        try:
            fig=builder()
            fig.text(0.01,0.005,entry["evidence_label"]+" | "+("SMOKE TEST" if smoke else "Executed data")+" | Scientific QC requires review",fontsize=7,color="#555555")
            fig.tight_layout(rect=(0,0.035,1,1))
            fig.savefig(str(stem)+".png",dpi=300,bbox_inches="tight",facecolor="white")
            fig.savefig(str(stem)+".svg",dpi=300,bbox_inches="tight",facecolor="white")
            fig.savefig(str(stem)+".pdf",dpi=300,bbox_inches="tight",facecolor="white")
            files=[str(stem)+"."+suffix for suffix in ["png","svg","pdf"]]
            plt.close(fig)
            source.to_csv(stem.with_name(identifier+"_source.csv"),index=False)
            entry.update(status="PASS",reason="Figure rendered from saved actual numerical results; scientific validity not asserted.",
                         output_file=files[0],output_files=files,source_csv=str(stem.with_name(identifier+"_source.csv")),
                         metadata_file=str(stem.with_suffix(".json")),script=str(Path(__file__).resolve()),command=command,
                         input_file_paths=[str(p) for p in inputs],render_dpi=300,minimum_font_pt=7,
                         scientific_qc="REVIEW_REQUIRED",seed=config.get("seed"),smoke_test=smoke)
            if identifier in ["B01","B07","E01"]:
                entry["streamline_parameters"]={"grid_density":1,"plot_density":2,"line_width_pt":0.7,
                                                "mask":"Standard scVelo support/velocity grid mask; no cells removed"}
            if identifier == "E04":
                entry["statistical_definition"]={"metric":"ROC AUC", "range":[0,1], "neutral":0.5,
                                                 "labels":"Baseline=1, perturbation=0", "p_test":"Pooled-cell ranksums, alternative=less",
                                                 "multiplicity":"Benjamini-Hochberg", "independent_biological_replicates":False}
            artifacts.extend(files+[entry["source_csv"],entry["metadata_file"]])
        except Exception as error:
            plt.close("all")
            log=stem.with_name(identifier+"_error.log")
            log.write_text(traceback.format_exc(),encoding="utf-8")
            entry.update(status="FAIL",reason=f"{type(error).__name__}: {error}",error_log=str(log))
            artifacts.append(str(log))
        stem.with_suffix(".json").write_text(json.dumps(entry,ensure_ascii=False,indent=2),encoding="utf-8")

    def panel_scatter(frame, keys, titles, categorical=False, **kwargs):
        if len(keys) in [3,4]:
            fig,axes=plt.subplots(2,2,figsize=(7.2,6.4),squeeze=False)
        else:
            fig,axes=plt.subplots(1,len(keys),figsize=(5*len(keys),4),squeeze=False)
        for ax,key,title in zip(axes.ravel(),keys,titles):
            if len(keys) in [3,4] and len(title)>24:
                title=title.replace(": ",":\n",1) if ": " in title else title.replace("_head_","_head\n",1)
            scatter(ax,frame,key,title,categorical,**kwargs)
        for ax in axes.ravel()[len(keys):]:ax.set_visible(False)
        return fig

    if data is not None and "X_umap" in data.obsm:
        frame=base_frame(data)
        if group in data.obs:
            draw("A01",frame,"Saved UMAP with original cell-type annotation",[embedding_source,config["input"]],
                 lambda:panel_scatter(frame,[group],["Cell types"],True))
        if time in data.obs:
            stage_frame=frame.copy();stage_frame[time]=data.obs[time].astype(str).to_numpy()
            order=config.get("time_order",list(pd.unique(stage_frame[time])))
            stage_frame["stage_ordinal"]=stage_frame[time].map({s:i for i,s in enumerate(order)})
            def stage_plot():
                fig,ax=plt.subplots(figsize=(5.5,4))
                im=ax.scatter(stage_frame.UMAP1,stage_frame.UMAP2,c=stage_frame.stage_ordinal,s=10,cmap="viridis",vmin=0,vmax=max(len(order)-1,1))
                bar=fig.colorbar(im,ax=ax,fraction=.04,pad=.03,ticks=range(len(order)))
                bar.ax.set_yticklabels(order);bar.set_label("Sampled stage (ordinal)")
                ax.set(title="Development stage",xlabel="UMAP 1",ylabel="UMAP 2",aspect="equal")
                return fig
            draw("A02",stage_frame,"Ordinal stage mapping from explicit time_order",[embedding_source,config["input"]],stage_plot)
    if raw is not None and all(k in raw.layers for k in ["spliced","unspliced"]):
        qc=pd.DataFrame({"cell":raw.obs_names})
        for k in ["spliced","unspliced"]:
            x=raw.layers[k];qc[k+"_total"]=np.asarray(x.sum(axis=1)).ravel()
            qc[k+"_detected"]=np.asarray((x>0).sum(axis=1)).ravel()
        def splice_qc():
            fig,axes=plt.subplots(1,2,figsize=(8,3.5))
            axes[0].scatter(qc.spliced_total/1000,qc.unspliced_total/1000,s=7,color="#4c78a8",alpha=.6)
            axes[0].set(xlabel="Spliced layer sum (×10³ units)",ylabel="Unspliced layer sum (×10³ units)",title="Saved RNA layer totals")
            axes[1].hist([qc.spliced_detected,qc.unspliced_detected],bins=30,label=["Spliced","Unspliced"],color=["#4c78a8","#e69954"])
            axes[1].set(xlabel="Detected genes / cell",ylabel="Cells",title="Splice detection");axes[1].legend(frameon=False)
            return fig
        draw("A03",qc,"Saved splice-layer sums and detected-gene counts; preprocessed layer values are not assumed raw UMIs",[config["input"]],splice_qc)
    retention=table("feature_retention")
    if retention is not None:
        coverage=pd.DataFrame({"step":["Input","Velocity retained","GRN retained"],"genes":[len(retention),int(retention.velocity_retained.sum()),int(retention.grn_retained.sum())]})
        prior_edges=table("prior_edges")
        network_coverage=(pd.DataFrame({"step":["Regulators","Targets","Prior edges"],
                          "count":[prior_edges.regulator.nunique(),prior_edges.target.nunique(),len(prior_edges)]})
                          if prior_edges is not None else None)
        def coverage_plot():
            fig,axes=plt.subplots(1,2 if network_coverage is not None else 1,figsize=(9 if network_coverage is not None else 5,3.3),squeeze=False)
            ax=axes[0,0];ax.bar(coverage.step,coverage.genes,color=["#bbbbbb","#4c78a8","#668c72"])
            for i,n in enumerate(coverage.genes):ax.text(i,n,str(n),ha="center",va="bottom",fontsize=8)
            ax.set(ylabel="Genes",title="Feature retention")
            if network_coverage is not None:
                ax=axes[0,1];ax.bar(network_coverage.step,network_coverage["count"],color=["#819cbd","#aaaaaa","#668c72"])
                ax.set(ylabel="Count (log scale)",yscale="log",title="Aligned prior coverage")
                ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
                for i,n in enumerate(network_coverage["count"]):ax.text(i,n,str(n),ha="center",va="bottom",fontsize=8)
            return fig
        source=coverage.rename(columns={"genes":"count"}).assign(type="feature_retention")
        if network_coverage is not None:source=pd.concat([source,network_coverage.assign(type="aligned_prior")],ignore_index=True)
        coverage_inputs=[output/"tables/feature_retention.csv"]
        if network_coverage is not None:coverage_inputs.append(output/"tables/prior_edges.csv")
        draw("A04",source,"Recorded feature-retention and unique regulator/target/effective prior-edge counts",coverage_inputs,coverage_plot)

    def velocity_panels(adatas,titles,stream=True):
        import scvelo as scv
        from scvelo.plotting.velocity_embedding_grid import compute_velocity_on_grid
        fig,axes=plt.subplots(1,len(adatas),figsize=(5.3*len(adatas),4),squeeze=False)
        for ax,a,title in zip(axes.ravel(),adatas,titles):
            if "velocity_umap" not in a.obsm:
                raise ValueError("Saved velocity_umap is required; inherited or missing embeddings must be recomputed in the numerical stage.")
            if group in a.obs:
                a.obs[group]=a.obs[group].astype("category")
                a.uns[group+"_colors"]=[palette.get(str(c),"#bdbdbd") for c in a.obs[group].cat.categories]
            plot=scv.pl.velocity_embedding_stream if stream else scv.pl.velocity_embedding
            kwargs={}
            if stream:
                grid_x,grid_v=compute_velocity_on_grid(X_emb=np.asarray(a.obsm["X_umap"]),
                                                     V_emb=np.asarray(a.obsm["velocity_umap"]),
                                                     density=1,autoscale=False,adjust_for_stream=True)
                # Constant width preserves the default grid mask without NaN linewidths in PDF.
                kwargs={"X_grid":grid_x,"V_grid":grid_v,"linewidth":0.7}
            plot(a,basis="umap",color=group,ax=ax,show=False,title=title,legend_loc="none",size=15,**kwargs)
            ax.set(xlabel="UMAP 1",ylabel="UMAP 2")
        return fig

    if velocity is not None and "velocity_umap" in velocity.obsm:
        vf=base_frame(velocity);vf[["velocity_UMAP1","velocity_UMAP2"]]=np.asarray(velocity.obsm["velocity_umap"])
        draw("B01",vf,"scVelo stream interpolation of RegVelo velocity projection",[output/"velocity.h5ad"],lambda:velocity_panels([velocity],["RegVelo velocity"],True))
        draw("B02",vf,"scVelo arrows from RegVelo saved velocity_umap",[output/"velocity.h5ad"],lambda:velocity_panels([velocity],["RegVelo velocity arrows"],False))
        if "latent_time" in velocity.obs:
            lf=base_frame(velocity);lf["latent_time"]=velocity.obs.latent_time.to_numpy()
            draw("B03",lf,"Min-max normalized per-cell mean inferred fit_t",[output/"velocity.h5ad"],lambda:panel_scatter(lf,["latent_time"],["Mean inferred latent time"],vmin=0,vmax=1))
        if all(k in velocity.layers for k in ["Ms","Mu","velocity"]):
            preferred=list(config.get("phase_genes",config.get("perturb",{}).get("tfs",[])))
            genes=[g for g in preferred if g in velocity.var_names]
            genes += [g for g in velocity.var_names if g not in genes][:max(0,3-len(genes))]
            genes=genes[:3]; blocks=[]
            for gene in genes:
                i=velocity.var_names.get_loc(gene)
                def values(k):
                    col=velocity.layers[k][:,i];return np.asarray(col.toarray() if sparse.issparse(col) else col).ravel()
                blocks.append(pd.DataFrame({"cell":velocity.obs_names,"gene":gene,"Ms":values("Ms"),"Mu":values("Mu"),"velocity":values("velocity")}))
            pf=pd.concat(blocks,ignore_index=True)
            def phase_plot():
                fig,axes=plt.subplots(1,len(genes),figsize=(4*len(genes),3.6),squeeze=False)
                for ax,gene in zip(axes.ravel(),genes):
                    b=pf[pf.gene==gene];bound=max(float(b.velocity.abs().max()),1e-12)
                    im=ax.scatter(b.Ms,b.Mu,c=b.velocity,cmap="RdBu_r",vmin=-bound,vmax=bound,s=10)
                    fig.colorbar(im,ax=ax,fraction=.04,pad=.03,label="Velocity")
                    ax.set(xlabel="Spliced moment (Ms)",ylabel="Unspliced moment (Mu)",title=gene)
                return fig
            draw("B04",pf,"Ms/Mu relationship colored by saved predicted velocity; no fitted phase line asserted",[output/"velocity.h5ad"],phase_plot)
        uncertainty=next((k for k in ["velocity_std","velocity_uncertainty","velocity_variance"] if k in velocity.layers),None)
        if uncertainty:
            uf=base_frame(velocity);uf[uncertainty]=np.asarray(velocity.layers[uncertainty].mean(axis=1)).ravel()
            draw("B06",uf,"Mean saved posterior uncertainty across genes",[output/"velocity.h5ad"],lambda:panel_scatter(uf,[uncertainty],["Saved velocity uncertainty"]))
        else: entries["B06"]["reason"]="Posterior mean velocity exists, but posterior uncertainty was not saved; no uncertainty estimate is invented."
        baseline=read("scvelo_stochastic")
        if baseline is not None and baseline.obs_names.equals(velocity.obs_names) and "velocity_umap" in baseline.obsm:
            bf=vf.copy();bf[["scvelo_UMAP1","scvelo_UMAP2"]]=np.asarray(baseline.obsm["velocity_umap"])
            draw("B07",bf,"Same-cell RegVelo and stochastic scVelo stream projections",[output/"velocity.h5ad",output/"scvelo_stochastic.h5ad"],lambda:velocity_panels([velocity,baseline],["RegVelo","scVelo stochastic"]))
    history=table("training_history")
    if history is not None and len(history):
        def loss_plot():
            metrics=[c for c in history if c!="epoch" and pd.api.types.is_numeric_dtype(history[c])]
            fig,axes=plt.subplots(1,min(3,len(metrics)),figsize=(4*min(3,len(metrics)),3.5),squeeze=False)
            for ax,metric in zip(axes.ravel(),metrics[:3]):
                ax.plot(history.epoch,history[metric],color="#4c78a8",lw=1.2);ax.set(xlabel="Epoch",ylabel=metric,title=metric)
            return fig
        draw("B05",history,"Actual saved training metrics; no convergence threshold inferred",[output/"tables/training_history.csv"],loss_plot)

    states=table("cellrank_states",index=0)
    if fate is not None and "X_umap" in fate.obsm:
        ff=base_frame(fate)
        if states is not None:
            for identifier,column,title in [("C01","macrostate","GPCCA macrostates"),("C02","terminal_state","Frozen terminal cells")]:
                sf=ff.copy();sf[column]=states.reindex(fate.obs_names)[column].fillna("Unassigned").to_numpy()
                draw(identifier,sf,"Saved GPCCA state assignment; unassigned cells retained",[output/"fate.h5ad",output/"tables/cellrank_states.csv"],lambda sf=sf,column=column,title=title:panel_scatter(sf,[column],[title],True))
        probs=table("baseline_fate_probabilities",index=0)
        if probs is not None:
            probs=probs.reindex(fate.obs_names); ff=pd.concat([ff.reset_index(drop=True),probs.reset_index(drop=True)],axis=1)
            lineages=list(probs.columns)
            draw("C03",ff,"CellRank absorption probabilities for saved terminal sets",[output/"tables/baseline_fate_probabilities.csv",output/"fate.h5ad"],lambda:panel_scatter(ff,lineages,lineages,vmin=0,vmax=1))
            if group in ff:
                mean=ff.groupby(group,observed=True)[lineages].mean()
                def fate_heatmap():
                    fig,ax=plt.subplots(figsize=(max(5,.8*len(lineages)),max(3,.3*len(mean))))
                    im=ax.imshow(mean,aspect="auto",vmin=0,vmax=1,cmap="viridis")
                    ax.set_xticks(range(len(lineages)),lineages,rotation=40,ha="right",rotation_mode="anchor");ax.set_yticks(range(len(mean)),mean.index)
                    fig.colorbar(im,ax=ax,label="Mean fate probability");ax.set_title("Fate by annotated cell class");return fig
                draw("C05",mean.reset_index().melt(id_vars=group,var_name="lineage",value_name="mean_fate_probability"),"Mean saved fate probabilities within annotations",[output/"tables/baseline_fate_probabilities.csv",output/"fate.h5ad"],fate_heatmap)
        if "commitment_score" in fate.obs:
            cf=base_frame(fate);cf["commitment_score"]=fate.obs.commitment_score.to_numpy()
            draw("C04",cf,"Saved 1 minus base-2 Shannon entropy normalized by the base-2 logarithm of the terminal count",[output/"fate.h5ad"],lambda:panel_scatter(cf,["commitment_score"],["Predicted commitment"],vmin=0,vmax=1))

    edges=table("tf_target_edges")
    if edges is not None and len(edges):
        selected=edges.sort_values("abs_weight",ascending=False).head(40).copy()
        def network_plot():
            import networkx as nx
            from matplotlib.lines import Line2D
            graph=nx.DiGraph()
            for edge in selected.itertuples():graph.add_edge(("Regulator",edge.regulator),("Target",edge.target),weight=edge.weight)
            regulators=sorted(selected.regulator.unique());targets=sorted(selected.target.unique())
            positions={(role,gene):(x,1-i/max(len(names)-1,1)) for role,x,names in [("Regulator",0,regulators),("Target",1,targets)] for i,gene in enumerate(names)}
            fig,ax=plt.subplots(figsize=(7.2,max(6,.18*max(len(regulators),len(targets)))))
            nx.draw_networkx_nodes(graph,positions,ax=ax,node_size=60,node_color=["#819cbd" if n[0]=="Regulator" else "#d5d5d5" for n in graph])
            nx.draw_networkx_edges(graph,positions,ax=ax,arrows=True,arrowsize=8,width=.7,alpha=.65,edge_color=["#4c78a8" if d["weight"]>=0 else "#b66b60" for _,_,d in graph.edges(data=True)])
            for node,(x,y) in positions.items():ax.text(x+(-.03 if x==0 else .03),y,node[1],ha="right" if x==0 else "left",va="center",fontsize=7)
            for x,label in [(0,"Regulator"),(1,"Target")]:ax.text(x,1.04,label,ha="center",fontsize=8)
            ax.legend(handles=[Line2D([0],[0],color="#4c78a8",label="Nonnegative weight"),Line2D([0],[0],color="#b66b60",label="Negative weight")],loc="lower center",bbox_to_anchor=(.5,-.02),ncol=2,frameon=False)
            ax.set_xlim(-.35,1.5);ax.set_ylim(-.05,1.1)
            ax.set_title("Strongest 40 effective TF–target connections",pad=12);ax.axis("off");return fig
        draw("D01",selected,"Directed two-column layout of top40 absolute fc1 weights; separate regulator/target roles, signed edge colors",[output/"tables/tf_target_edges.csv"],network_plot)
        top_tfs=edges.groupby("regulator").abs_weight.sum().nlargest(12).index
        top_targets=edges[edges.regulator.isin(top_tfs)].groupby("target").abs_weight.sum().nlargest(25).index
        heat=edges[edges.regulator.isin(top_tfs)&edges.target.isin(top_targets)].pivot_table(index="target",columns="regulator",values="weight",aggfunc="first",fill_value=0).reindex(index=top_targets,columns=top_tfs,fill_value=0)
        def grn_heatmap():
            fig,ax=plt.subplots(figsize=(6.5,6));bound=max(float(np.abs(heat.to_numpy()).max()),1e-12)
            im=ax.imshow(heat,aspect="auto",cmap="RdBu_r",vmin=-bound,vmax=bound)
            ax.set_xticks(range(len(heat.columns)),heat.columns,rotation=60,ha="right",rotation_mode="anchor");ax.set_yticks(range(len(heat)),heat.index)
            ax.set(xlabel="Regulator",ylabel="Target",title="Selected effective regulatory weights")
            fig.colorbar(im,ax=ax,label="fc1 weight");return fig
        draw("D02",heat.rename_axis("target").reset_index().melt(id_vars="target",var_name="regulator",value_name="weight"),"Signed target-by-regulator weight heatmap; top12 regulators/top25 targets by sum absolute weights",[output/"tables/tf_target_edges.csv"],grn_heatmap)
        def weight_hist():
            fig,ax=plt.subplots(figsize=(5,3.5));ax.hist(edges.weight,bins=60,color="#7d8fa6")
            ax.set(xlabel="Effective signed fc1 weight",ylabel="Edges",title="Regulatory weight distribution");return fig
        draw("D04",edges,"Histogram of saved edges above configured grn_cutoff",[output/"tables/tf_target_edges.csv"],weight_hist)
    ranking=table("regulon_ranking",index=0)
    if ranking is not None and len(ranking):
        ranks=ranking.sort_values("sum_abs_weight",ascending=False).head(20).rename_axis("regulator").reset_index()
        def ranking_plot():
            fig,ax=plt.subplots(figsize=(5,max(3,len(ranks)*.24)));ax.barh(ranks.regulator,ranks.sum_abs_weight,color="#819cbd");ax.invert_yaxis()
            ax.set(xlabel="Sum absolute effective fc1 weights",title="Regulon weight ranking");return fig
        draw("D03",ranks,"Sum absolute learned effective weights per regulator; top20 display",[output/"tables/regulon_ranking.csv"],ranking_plot)
    grn_qc=output/"GRN_QC.json"
    if grn_qc.is_file():
        q=json.loads(grn_qc.read_text(encoding="utf-8"));compare=pd.DataFrame({"category":["Prior retained","Prior absent","New model edges"],"edges":[q["retained_prior_edges"],q["prior_edges"]-q["retained_prior_edges"],q["new_model_edges"]]})
        def overlap_plot():
            fig,ax=plt.subplots(figsize=(5,3.5));ax.bar(compare.category,compare.edges,color=["#688c74","#bdbdbd","#bd8764"])
            for i,n in enumerate(compare.edges):ax.text(i,n,str(n),ha="center",va="bottom",fontsize=8)
            ax.set(ylabel="Connections",title=f'Prior vs effective model edges (cutoff {q["cutoff"]:g})');return fig
        draw("D05",compare,"Thresholded effective fc1 edges intersected with aligned prior",[grn_qc],overlap_plot)

    paired=read("baseline_posterior")
    tested=config.get("perturb",{}).get("tfs",config.get("tfs",[]))
    tested=[tested] if isinstance(tested,str) else tested
    available=[tf for tf in tested if (output/f"perturb_{tf}.h5ad").is_file()]
    if available and paired is not None:
        tf=available[0];ko=read("perturb_"+tf)
        if not paired.obs_names.equals(ko.obs_names) or not paired.var_names.equals(ko.var_names):
            raise ValueError("Perturbation plots require exact paired cell/feature order.")
        if "velocity_umap" in paired.obsm and "velocity_umap" in ko.obsm:
            ef=base_frame(paired);ef[["baseline_v1","baseline_v2"]]=paired.obsm["velocity_umap"];ef[["KO_v1","KO_v2"]]=ko.obsm["velocity_umap"]
            draw("E01",ef,"Paired posterior baseline and independently recomputed KO velocity embedding",[output/"baseline_posterior.h5ad",output/f"perturb_{tf}.h5ad"],lambda:velocity_panels([paired,ko],["Paired baseline",tf+" regulon block"]))
        effect=table(tf+"_cell_effect",index=0)
        if effect is not None:
            ef=pd.concat([base_frame(ko),effect.reindex(ko.obs_names).reset_index(drop=True)],axis=1)
            keys=[k for k in ["perturbation_velocity_l2","perturbation_effect_cosine"] if k in ef]
            draw("E02",ef,"Cell-wise high-dimensional velocity L2 change and 1-cosine; saved paired predictions",[output/"tables"/(tf+"_cell_effect.csv"),output/f"perturb_{tf}.h5ad"],lambda:panel_scatter(ef,keys,[tf+": "+k for k in keys]))
        difference=table(tf+"_fate_difference",index=0)
        if difference is not None:
            df=pd.concat([base_frame(ko),difference.reindex(ko.obs_names).reset_index(drop=True)],axis=1);keys=list(difference.columns)
            bound=max(float(np.abs(difference.to_numpy()).max()),1e-12)
            draw("E03",df,"KO minus paired baseline fate probabilities; terminal cells frozen",[output/"tables"/(tf+"_fate_difference.csv"),output/f"perturb_{tf}.h5ad"],lambda:panel_scatter(df,keys,[tf+": "+k for k in keys],vmin=-bound,vmax=bound,cmap="RdBu_r"))
        blocked=table(tf+"_blocked_edges")
        if blocked is not None and len(blocked):
            b=blocked.assign(abs_weight=lambda d:d.weight_before.abs()).sort_values("abs_weight",ascending=False).head(20)
            def block_plot():
                fig,ax=plt.subplots(figsize=(7,3.8));x=np.arange(len(b));ax.bar(x-.2,b.weight_before,width=.4,label="Before",color="#819cbd");ax.bar(x+.2,b.weight_after,width=.4,label="After",color="#bd8764")
                ax.scatter(x+.2,b.weight_after,s=10,color="#bd8764",zorder=3)
                ax.set_xticks(x,b.target,rotation=70,ha="right",rotation_mode="anchor");ax.set(ylabel="fc1 downstream weight",title=tf+" regulon blockade");ax.legend(frameon=False);return fig
            draw("E06",b,"Paired model weight before/after selected TF downstream block; top20 absolute baseline targets",[output/"tables"/(tf+"_blocked_edges.csv")],block_plot)
    depletion=table("perturbation_depletion")
    if depletion is not None and len(depletion):
        def depletion_plot():
            metric="Depletion likelihood";heat=depletion.pivot(index="TF",columns="Terminal state",values=metric)
            fig,ax=plt.subplots(figsize=(max(5,len(heat.columns)*1.1),max(3,len(heat)*.5)))
            im=ax.imshow(heat,aspect="auto",cmap="RdBu_r",vmin=0,vmax=1)
            for (row,col),value in np.ndenumerate(heat.to_numpy()):
                if np.isfinite(value):
                    ax.text(col,row,f"{value:.3f}",ha="center",va="center",fontsize=7,
                            color="white" if value<0.2 or value>0.8 else "#333333")
            ax.set_xticks(range(len(heat.columns)),heat.columns,rotation=45,ha="right",rotation_mode="anchor");ax.set_yticks(range(len(heat)),heat.index)
            fig.colorbar(im,ax=ax,label=metric+" (0.5: no shift)");ax.set_title("Official cell-fate perturbation statistic");return fig
        draw("E04",depletion,"Official regvelo.mt.cellfate_perturbation(method=likelihood) ROC AUC on [0,1], neutral 0.5; NULL included as control",[output/"tables/perturbation_depletion.csv"],depletion_plot)
    summary=table("perturbation_summary")
    if summary is not None and len(summary):
        summary=summary.sort_values("mean_velocity_l2",ascending=True)
        def perturb_rank():
            fig,ax=plt.subplots(figsize=(5,max(3,len(summary)*.4)));ax.barh(summary.TF,summary.mean_velocity_l2,color="#819cbd");ax.set(xlabel="Mean paired velocity L2 difference",title="Tested TF perturbation ranking");return fig
        draw("E05",summary,"Mean saved cell-wise high-dimensional velocity change; tested targets only",[output/"tables/perturbation_summary.csv"],perturb_rank)

    for entry in entries.values():
        if entry["status"]=="NOT_RUN":
            entry.update(script=str(Path(__file__).resolve()),command=command,metadata_file=str(figures/(entry["id"]+".json")),scientific_qc="NOT_EVALUATED")
            Path(entry["metadata_file"]).write_text(json.dumps(entry,ensure_ascii=False,indent=2),encoding="utf-8")
            artifacts.append(entry["metadata_file"])
    catalog=output/"FIGURE_CATALOG.csv"
    pd.DataFrame(entries.values()).to_csv(catalog,index=False)
    lines=["# RegVelo 科学图件 / Scientific gallery","","图件来自本目录真实计算文件。PASS仅表示成功渲染；方向、终末状态与扰动科学结论仍需QC。缺失结果登记NOT_RUN，未生成占位图。","",
           "| ID | 图件 / Figure | 状态 | 解释与限制 |","|---|---|---|---|"]
    for entry in entries.values():
        lines.append(f'| {entry["id"]} | {entry["chinese_name"]} / {entry["english_name"]} | {entry["status"]} | {entry["biological_interpretation"]} |')
        if entry["status"]=="PASS":
            lines.extend(["",f'![{entry["english_name"]}](figures/{entry["id"]}.png)',"",
                          f'来源：{entry["input"]}；计算：{entry["method"]}；[绘图数据](figures/{entry["id"]}_source.csv)；[参数与限制](figures/{entry["id"]}.json)。',""])
    lines.extend(["","复现 / Reproduce:","```powershell",command,"```"])
    gallery=output/"FIGURE_GALLERY.md";gallery.write_text("\n".join(lines),encoding="utf-8")
    figures_readme=figures/"README.md"
    figures_readme.write_text("\n".join(lines).replace("(figures/","("),encoding="utf-8")
    artifacts.extend([str(catalog),str(gallery),str(figures_readme)])
    return {"status":"FAIL" if any(e["status"]=="FAIL" for e in entries.values()) else "PASS",
            "artifacts":artifacts,"figures_rendered":sum(e["status"]=="PASS" for e in entries.values()),
            "catalog_entries":len(entries),"not_run":{k:v["reason"] for k,v in entries.items() if v["status"]=="NOT_RUN"},
            "scientific_qc":"REVIEW_REQUIRED; render PASS does not assert scientific reliability."}
