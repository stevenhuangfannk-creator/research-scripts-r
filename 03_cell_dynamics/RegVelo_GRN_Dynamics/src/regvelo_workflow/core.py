"""Input invariants, named GRN validation, network extraction and reporting."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse

from .cli import write_json


def read_prior(config, genes):
    """Load a named matrix or explicit TF Atlas source/target edge schema."""
    if config.get("grn_format", "matrix") == "matrix":
        return pd.read_csv(config["grn"], index_col=0)
    if config.get("grn_format") != "edge_list":
        raise ValueError("grn_format must be matrix or edge_list.")
    columns = config.get("grn_columns", {"regulator": "source", "target": "target", "weight": "weight"})
    edges = pd.read_csv(config["grn"])
    required = [columns[key] for key in ("regulator", "target", "weight")]
    if not set(required).issubset(edges.columns):
        raise ValueError(f"Edge list is missing columns: {required}")
    edges = edges[required].rename(columns={columns[key]: key for key in columns})
    edges = edges[edges.regulator.isin(genes) & edges.target.isin(genes)]
    if edges.empty:
        raise ValueError("No species/identifier-matched TF-target edges remain.")
    if edges.duplicated(["regulator", "target"]).any():
        raise ValueError("Duplicate TF-target pairs: resolve conflicting prior evidence before modeling.")
    matrix = edges.pivot(index="target", columns="regulator", values="weight").fillna(0)
    orientation = config.get("grn_orientation")
    if orientation == "target_by_regulator":
        return matrix
    if orientation == "regulator_by_target":
        return matrix.T
    raise ValueError("Edge-list input requires an explicit grn_orientation.")


def validate_grn(frame, genes, orientation, regulators=None):
    """Return named target x regulator GRN; square matrices never imply direction."""
    if not frame.index.is_unique or not frame.columns.is_unique:
        raise ValueError("GRN has duplicate gene labels; resolve gene IDs before alignment.")
    if not pd.Index(genes).is_unique:
        raise ValueError("AnnData gene names are not unique.")
    if orientation == "auto":
        if not regulators:
            raise ValueError("GRN orientation is ambiguous: supply named regulators or an explicit orientation.")
        row_tfs = len(set(regulators) & set(frame.index))
        column_tfs = len(set(regulators) & set(frame.columns))
        if row_tfs == column_tfs:
            raise ValueError("GRN orientation is ambiguous: TF label overlap does not distinguish the axes.")
        orientation = "regulator_by_target" if row_tfs > column_tfs else "target_by_regulator"
    if orientation not in ("regulator_by_target", "target_by_regulator"):
        raise ValueError(f"Unsupported GRN orientation: {orientation}")
    result = frame.T if orientation == "regulator_by_target" else frame.copy()
    if not set(genes).intersection(result.index) or not set(genes).intersection(result.columns):
        raise ValueError("No regulator/target overlap with input gene identifiers.")
    values = result.to_numpy(dtype=np.float32)
    if not np.isfinite(values).all():
        raise ValueError("GRN contains non-finite values.")
    if not np.any(values != 0):
        raise ValueError("GRN contains no effective edges.")
    return result


def layer_summary(matrix):
    values = matrix.data if sparse.issparse(matrix) else np.asarray(matrix).ravel()
    sampled = np.asarray(values[:100000])
    return {"shape": list(matrix.shape), "nnz": int(matrix.count_nonzero() if sparse.issparse(matrix) else np.count_nonzero(matrix)),
            "sparsity": float(1 - (matrix.count_nonzero() if sparse.issparse(matrix) else np.count_nonzero(matrix)) / np.prod(matrix.shape)),
            "finite": bool(np.isfinite(values).all()), "nonnegative": bool((values >= 0).all()),
            "integer_first_100000_values": bool(np.allclose(sampled, np.rint(sampled))),
            "count_scale": "NOT_CONFIRMED: integer sample alone cannot establish raw-count provenance"}


def audit_adata(adata, group_key=None, time_key=None):
    missing = [key for key in ("spliced", "unspliced") if key not in adata.layers]
    if missing:
        raise ValueError(f"Missing required RNA layers: {', '.join(missing)}. Expression cannot reconstruct splicing counts.")
    if not adata.var_names.is_unique or not adata.obs_names.is_unique:
        raise ValueError("Cell and gene identifiers must be unique; no automatic renaming is performed.")
    layers = {key: layer_summary(value) for key, value in adata.layers.items()}
    for key in ("spliced", "unspliced"):
        if not layers[key]["finite"] or not layers[key]["nonnegative"] or layers[key]["nnz"] == 0:
            raise ValueError(f"Invalid {key} layer: {layers[key]}")
    return {"n_cells": adata.n_obs, "n_genes": adata.n_vars, "layers": layers,
            "obs_columns": list(adata.obs.columns), "embeddings": list(adata.obsm),
            "group_counts": adata.obs[group_key].value_counts().to_dict() if group_key in adata.obs else {},
            "time_counts": adata.obs[time_key].value_counts().to_dict() if time_key in adata.obs else {},
            "raw_counts_provenance": "UNKNOWN unless source metadata establishes counts",
            "readiness": "CONDITIONAL: splicing layers present; directional and biological QC still required"}


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run_audit(config, output):
    import anndata as ad
    adata = ad.read_h5ad(config["input"])
    issues = []
    try:
        result = audit_adata(adata, config.get("group_key"), config.get("time_key"))
    except ValueError as error:
        issues.append(str(error))
        result = {"n_cells": adata.n_obs, "n_genes": adata.n_vars, "layers_present": list(adata.layers),
                  "required_layers_missing": [key for key in ("spliced", "unspliced") if key not in adata.layers],
                  "obs_columns": list(adata.obs), "readiness": "NOT_READY"}
    try:
        frame = read_prior(config, adata.var_names)
        target_grn = validate_grn(frame, adata.var_names, config.get("grn_orientation", "auto"), config.get("regulators"))
        values = target_grn.to_numpy()
        result["grn"] = {"input_orientation": config["grn_orientation"], "aligned_orientation": "target_by_regulator",
                     "regulator_axis_length": target_grn.shape[1], "target_axis_length": target_grn.shape[0],
                     "active_regulators": int(np.any(values != 0, axis=0).sum()),
                     "active_targets": int(np.any(values != 0, axis=1).sum()),
                     "edges": int(np.count_nonzero(values)), "density": float(np.count_nonzero(values) / values.size),
                     "regulators_in_data": len(set(target_grn.columns) & set(adata.var_names)),
                     "targets_in_data": len(set(target_grn.index) & set(adata.var_names))}
    except (OSError, ValueError, KeyError) as error:
        issues.append(f"GRN: {error}")
        result["grn"] = {"status": "FAIL", "error": str(error)}
    result["sources"] = [{"path": config[key], "size_bytes": Path(config[key]).stat().st_size,
                          "sha256": sha256(config[key])} for key in ("input", "grn") if Path(config[key]).is_file()]
    tables = output / "tables"
    tables.mkdir(exist_ok=True)
    per_cell = adata.obs.copy()
    for layer in ("spliced", "unspliced"):
        if layer not in adata.layers:
            continue
        matrix = adata.layers[layer]
        per_cell[f"{layer}_total"] = np.asarray(matrix.sum(axis=1)).ravel()
        per_cell[f"{layer}_detected_genes"] = np.asarray((matrix > 0).sum(axis=1)).ravel()
    per_cell.to_csv(tables / "input_cell_qc.csv")
    result.update(status="FAIL" if issues else "PASS", issues=issues)
    write_json(output / "INPUT_AUDIT.json", result)
    if issues:
        raise ValueError("; ".join(issues) + f". Evidence: {output / 'INPUT_AUDIT.json'}")
    return {"artifacts": [str(output / "INPUT_AUDIT.json"), str(tables / "input_cell_qc.csv")], "n_cells": adata.n_obs, "n_genes": adata.n_vars}


def run_grn(config, output):
    import anndata as ad
    import regvelo as rgv
    adata = ad.read_h5ad(output / "velocity.h5ad")
    model = rgv.REGVELOVI.load(str(output / "model"), adata, accelerator=config.get("train", {}).get("accelerator", "cpu"))
    prior = np.asarray(adata.uns["skeleton"]).T.astype(bool)
    weights = model.module.v_encoder.fc1.weight.detach().cpu().numpy()
    jacobian = rgv.tl.inferred_grn(model, adata, label=config["group_key"], group="all", data_frame=True,
                                 device=str(model.module.device))
    if not np.isfinite(jacobian.to_numpy()).all():
        raise ValueError("Non-finite global inferred GRN Jacobian.")
    assert weights.shape == prior.shape == (adata.n_vars, adata.n_vars)
    tables = output / "tables"
    tables.mkdir(exist_ok=True)
    jacobian.to_csv(tables / "inferred_grn_jacobian.csv")
    pd.DataFrame(weights, index=adata.var_names, columns=adata.var_names).to_csv(tables / "regulatory_weights.csv")
    cutoff = config.get("grn_cutoff", 1e-3)
    rows, columns = np.where(np.abs(weights) > cutoff)
    edges = pd.DataFrame({"target": adata.var_names[rows], "regulator": adata.var_names[columns],
                          "weight": weights[rows, columns], "jacobian": jacobian.values[rows, columns],
                          "prior_supported": prior[rows, columns], "experimental_support": "NOT_CHECKED"})
    edges["abs_weight"] = edges.weight.abs()
    edges.sort_values("abs_weight", ascending=False).to_csv(tables / "tf_target_edges.csv", index=False)
    ranking = edges.groupby("regulator").agg(n_targets=("target", "size"), sum_abs_weight=("abs_weight", "sum"))
    ranking.sort_values("sum_abs_weight", ascending=False).to_csv(tables / "regulon_ranking.csv")
    comparison = {"cutoff": cutoff, "prior_edges": int(prior.sum()), "retained_prior_edges": int(prior[rows, columns].sum()),
                  "new_model_edges": int((~prior[rows, columns]).sum()), "inferred_edges": len(edges),
                  "weight_definition": "fc1 target-by-regulator weights; distinct from normalized expression Jacobian",
                  "group_jacobian_normalization": "Official API independently divides each group by its mean absolute nonzero Jacobian. Values describe within-group relative weights; cross-group absolute strength is not comparable.",
                  "interpretation": "Computational associations; prior support does not establish direct regulation"}
    write_json(output / "GRN_QC.json", comparison)
    groups = {}
    for group in adata.obs[config["group_key"]].value_counts().index[:8]:
        matrix = rgv.tl.inferred_grn(model, adata, label=config["group_key"], group=[group], data_frame=True,
                                   device=str(model.module.device))
        if not np.isfinite(matrix.to_numpy()).all():
            raise ValueError(f"Non-finite inferred Jacobian in group {group}.")
        for tf in config.get("perturb", {}).get("tfs", []):
            if tf in matrix.columns:
                groups[f"{group}|{tf}"] = matrix[tf]
    if groups:
        pd.DataFrame(groups).to_csv(tables / "state_tf_jacobians.csv")
    return {"artifacts": [str(output / "GRN_QC.json"), str(tables / "tf_target_edges.csv"), str(tables / "inferred_grn_jacobian.csv")], **comparison}


def run_report(config, output):
    state_path = output / "run_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"stages": {}}
    lines = ["# RegVelo 真实运行报告 / Executed analysis", "", "执行成功仅证明对应计算完成；科学可靠性需结合模型 QC、方向性、基线与对照。", "",
             "| 阶段 | 状态 | 秒 | 证据或错误 |", "|---|---|---:|---|"]
    from .cli import STAGES
    for stage in STAGES:
        record = state["stages"].get(stage, {"status": "NOT_RUN"})
        lines.append(f"| {stage} | {record['status']} | {record.get('elapsed_seconds', '')} | {record.get('error', ', '.join(record.get('artifacts', [])))} |")
    lines += ["", "## 参数 / Parameters", "", "```json", json.dumps(config, ensure_ascii=False, indent=2), "```", "",
              "## 解释边界 / Interpretation", "", "这是 regulon-level in silico knockout；不是 CRISPR 实验。横断面疾病组不等价于真实时间。所有缺失图件均为 NOT_RUN 或 NOT_APPLICABLE，不能以教程图替代。"]
    path = output / "ANALYSIS_REPORT.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return {"artifacts": [str(path)]}
