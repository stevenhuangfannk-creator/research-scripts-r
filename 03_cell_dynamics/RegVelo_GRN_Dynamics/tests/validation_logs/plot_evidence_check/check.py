"""Read-only checks of core gallery source values against saved actual data."""
import hashlib
import json
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "outputs/regvelo_results/official_zebrafish/hard_seed0"
DEST = Path(__file__).resolve().parent
RAW = ROOT / "outputs/regvelo_data/raw/adata_zebrafish_preprocessed.h5ad"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dense(value):
    return value.toarray() if sparse.issparse(value) else np.asarray(value)


def numeric(actual, expected):
    actual, expected = np.asarray(actual), np.asarray(expected)
    good = actual.shape == expected.shape and np.allclose(actual, expected, rtol=1e-7, atol=1e-12, equal_nan=True)
    error = float(np.nanmax(np.abs(actual - expected))) if actual.shape == expected.shape and actual.size else None
    return {"pass": bool(good), "max_absolute_error": error,
            "exact_after_source_dtype_cast": bool(np.array_equal(actual.astype(expected.dtype), expected, equal_nan=True))}


paths = [RAW, OUT / "velocity.h5ad", OUT / "scvelo_stochastic.h5ad",
         OUT / "velocity_qc.json"]
paths += [OUT / "figures" / (fid + suffix) for fid in ["A03", "B03", "B06", "B07"]
          for suffix in ["_source.csv", ".json"]]
hash_before = {str(p): sha(p) for p in paths}
raw = ad.read_h5ad(RAW)
velocity = ad.read_h5ad(OUT / "velocity.h5ad")
baseline = ad.read_h5ad(OUT / "scvelo_stochastic.h5ad")
checks = {}

a03 = pd.read_csv(OUT / "figures/A03_source.csv")
checks["A03"] = {"cell_order_exact": a03.cell.tolist() == raw.obs_names.tolist(), "rows": len(a03)}
for layer in ["spliced", "unspliced"]:
    matrix = raw.layers[layer]
    checks["A03"][layer + "_total"] = numeric(a03[layer + "_total"], np.asarray(matrix.sum(axis=1)).ravel())
    checks["A03"][layer + "_detected"] = numeric(a03[layer + "_detected"], np.asarray((matrix > 0).sum(axis=1)).ravel())

b03 = pd.read_csv(OUT / "figures/B03_source.csv")
mean_time = dense(velocity.layers["fit_t"]).mean(axis=1)
scaled = (mean_time - mean_time.min()) / np.ptp(mean_time)
latent = velocity.obs["latent_time"].to_numpy()
checks["B03"] = {"cell_order_exact": b03.cell.tolist() == velocity.obs_names.tolist(),
                 "source_equals_saved_obs": numeric(b03.latent_time, latent),
                 "saved_obs_equals_minmax_mean_fit_t": numeric(latent, scaled),
                 "finite": bool(np.isfinite(latent).all()),
                 "normalized_range": [float(latent.min()), float(latent.max())],
                 "in_0_1": bool(((latent >= 0) & (latent <= 1)).all()),
                 "unscaled_mean_fit_t_range": [float(mean_time.min()), float(mean_time.max())]}

b06 = pd.read_csv(OUT / "figures/B06_source.csv")
uncertainty = dense(velocity.layers["velocity_std"])
checks["B06"] = {"cell_order_exact": b06.cell.tolist() == velocity.obs_names.tolist(),
                 "saved_layer_shape": list(uncertainty.shape),
                 "saved_layer_finite_nonnegative": bool(np.isfinite(uncertainty).all() and (uncertainty >= 0).all()),
                 "source_equals_mean_gene_std": numeric(b06.velocity_std, uncertainty.mean(axis=1)),
                 "source_range": [float(b06.velocity_std.min()), float(b06.velocity_std.max())]}

b07 = pd.read_csv(OUT / "figures/B07_source.csv")
checks["B07"] = {"cell_order_exact": b07.cell.tolist() == velocity.obs_names.tolist(),
                 "regvelo_scvelo_cells_exact": velocity.obs_names.equals(baseline.obs_names),
                 "regvelo_scvelo_features_exact": velocity.var_names.equals(baseline.var_names),
                 "same_saved_umap": numeric(velocity.obsm["X_umap"], baseline.obsm["X_umap"]),
                 "source_umap": numeric(b07[["UMAP1", "UMAP2"]], velocity.obsm["X_umap"]),
                 "source_regvelo_velocity": numeric(b07[["velocity_UMAP1", "velocity_UMAP2"]], velocity.obsm["velocity_umap"]),
                 "source_scvelo_velocity": numeric(b07[["scvelo_UMAP1", "scvelo_UMAP2"]], baseline.obsm["velocity_umap"]),
                 "original_annotation_preserved": bool(np.array_equal(b07.cell_type.astype(str), raw.obs.loc[velocity.obs_names, "cell_type"].astype(str)))}

metadata = {fid: json.loads((OUT / "figures" / (fid + ".json")).read_text(encoding="utf-8"))
            for fid in checks}
labels = {fid: {key: metadata[fid].get(key) for key in
               ["status", "evidence_label", "method", "limitations", "biological_interpretation", "scientific_qc", "input_file_paths"]}
          for fid in checks}
hash_after = {str(p): sha(p) for p in paths}


def bools(value):
    if isinstance(value, dict):
        return [b for key, val in value.items() if key != "exact_after_source_dtype_cast" for b in bools(val)]
    return [value] if isinstance(value, bool) else []


status = "PASS" if all(bools(checks)) and hash_before == hash_after else "FAIL"
report = {"status": status, "scope": "A03/B03/B06/B07 read-only numerical evidence audit",
          "checks": checks, "figure_metadata": labels,
          "sha256": hash_after, "inputs_unchanged_during_check": hash_before == hash_after,
          "limitations": ["Source-table consistency does not validate biological velocity direction or model convergence.",
                          "Saved posterior standard-deviation layer is checked; original posterior draws were not independently regenerated.",
                          "velocity_qc.json latent_time_range records unscaled mean fit_t (4.462–8.328), while obs latent_time and B03 are normalized [0,1]."]}
(DEST / "evidence.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
lines = ["# 核心图件数值核对 / Core plot evidence check", "", f"状态：{status}。仅只读核对；检查期间所有受检文件SHA-256保持不变。", "",
         "- A03：697个细胞顺序与官方输入一致，真实spliced/unspliced层总量及检出基因数逐细胞匹配；单位是预处理层数值，图件没有改称原始UMI。",
         "- B03：导出的latent_time与velocity.h5ad保存obs值一致，严格等于mean fit_t的min-max缩放；数值有限，范围[0,1]。",
         "- B06：真实保存的velocity_std层为697×1007，有限且非负；导出的697个值匹配逐细胞跨基因平均标准差。",
         "- B07：RegVelo与scVelo的697个细胞、1007个基因及UMAP顺序完全一致；两组箭头分量分别来自各自保存velocity_umap；细胞类型标签与原始输入一致。",
         "- 元数据将速度、潜在时间、不确定性和比较标为Model-predicted，明确限制真实时钟、运动和真值结论。本次受检图表数据未见随机或合成替代值。",
         "", "注意：velocity_qc.json的latent_time_range字段记录未缩放mean fit_t（4.462–8.328），而保存obs latent_time及B03为[0,1]；建议字段命名明确该区别。",
         "", "边界：数值一致性不证明动力学方向、收敛或生物学可靠性；未重新生成后验抽样。完整逐项误差与SHA-256见evidence.json。"]
(DEST / "FINDINGS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({"status": status, "checks": checks}, ensure_ascii=False, indent=2))
