"""Official RegVelo stages; AnnData inputs are read into independent copies."""

import json
import logging
from pathlib import Path


def _directories(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "tables").mkdir(exist_ok=True)
    return output


def _json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _seed(config):
    import random
    import numpy as np
    import torch
    import scvi

    seed = int(config.get("seed", 0))
    random.seed(seed)
    np.random.seed(seed)
    scvi.settings.seed = seed
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def _posterior(config):
    options = config.get("posterior", {})
    return {"n_samples": int(options.get("n_samples", config.get("n_samples", 30))),
            "batch_size": options.get("batch_size", 128)}


def run_prepare(config: dict, output: Path):
    import anndata as ad
    import numpy as np
    import pandas as pd
    import regvelo as rgv
    import scanpy as sc
    import scvelo as scv
    from scipy import sparse

    output = _directories(output)
    _seed(config)
    data = ad.read_h5ad(config["input"])
    if not data.var_names.is_unique or not data.obs_names.is_unique:
        raise ValueError("AnnData requires unique gene and cell names.")
    for layer in ("spliced", "unspliced"):
        if layer not in data.layers:
            raise ValueError(f"Missing RNA velocity input layer: {layer}")
    options = config.get("prepare", {})
    original_shape = list(data.shape)
    maximum = options.get("max_cells")
    if maximum is not None and int(maximum) < data.n_obs:
        indices = np.sort(np.random.default_rng(config.get("seed", 0)).choice(
            data.n_obs, int(maximum), replace=False))
        data = data[indices].copy()
    n_pcs = int(options.get("n_pcs", 30))
    if "X_pca" not in data.obsm:
        sc.tl.pca(data, n_comps=min(n_pcs, data.n_obs - 1, data.n_vars - 1))
    sc.pp.neighbors(data, n_neighbors=int(options.get("n_neighbors", 30)),
                    n_pcs=min(n_pcs, data.obsm["X_pca"].shape[1]))
    moments_kept = all(layer in data.layers for layer in ("Ms", "Mu"))
    if not moments_kept or options.get("recompute_moments", False):
        scv.pp.moments(data, n_pcs=None, n_neighbors=None)
    if "X_umap" not in data.obsm:
        sc.tl.umap(data)
    for layer in ("Ms", "Mu"):
        if sparse.issparse(data.layers[layer]):
            data.layers[layer] = data.layers[layer].toarray()
        if not np.isfinite(data.layers[layer]).all():
            raise ValueError(f"Non-finite values in layer {layer}.")
    # Keep unscaled RNA moments for the scVelo baseline; no normalization is repeated.
    data.write_h5ad(output / "baseline_input.h5ad", compression="gzip")
    before_genes = data.var_names.copy()
    from .core import read_prior
    prior = read_prior(config, data.var_names)
    if not prior.index.is_unique or not prior.columns.is_unique:
        raise ValueError("Prior GRN requires unique regulator and target names.")
    orientation = config.get("grn_orientation")
    if orientation == "regulator_by_target":
        targets_by_regulators = prior.T
    elif orientation == "target_by_regulator":
        targets_by_regulators = prior
    else:
        raise ValueError("Specify grn_orientation as regulator_by_target or target_by_regulator.")
    data = rgv.pp.preprocess_data(data)
    velocity_genes = data.var_names.copy()
    data = rgv.pp.set_prior_grn(data, targets_by_regulators,
                              cor_filter=bool(options.get("cor_filter", True)))
    skeleton = data.uns["skeleton"]
    if not (skeleton.index.equals(data.var_names) and skeleton.columns.equals(data.var_names)):
        raise ValueError("Aligned GRN names/order disagree with AnnData genes.")
    # Official set_prior_grn output has regulator rows and target columns.
    active_regulators = skeleton.sum(axis=1).to_numpy() > 0
    data.var["TF"] = data.var["is_tf"].astype(bool) if "is_tf" in data.var else active_regulators
    if not active_regulators.any() or data.n_vars == 0:
        raise ValueError("No active prior GRN regulators survived preprocessing.")
    data.uns["regvelo_workflow"] = {"grn_orientation": "regulator_by_target",
                                   "input_was_preprocessed": True,
                                   "smoke_test": maximum is not None}
    data.write_h5ad(output / "prepared.h5ad", compression="gzip")
    pd.DataFrame({"gene": before_genes,
                  "velocity_retained": before_genes.isin(velocity_genes),
                  "grn_retained": before_genes.isin(data.var_names)}).to_csv(
        output / "tables" / "feature_retention.csv", index=False)
    rr, tt = np.where(skeleton.to_numpy() != 0)
    pd.DataFrame({"regulator": data.var_names[rr], "target": data.var_names[tt]}).to_csv(
        output / "tables" / "prior_edges.csv", index=False)
    # Verify labelled source edges through both transposes, including actual direction.
    W = skeleton.to_numpy().T
    examples = []
    preferred = config.get("perturb", {}).get("tfs", [])
    if isinstance(preferred, str):
        preferred = [preferred]
    regulator_indices = [data.var_names.get_loc(tf) for tf in preferred if tf in data.var_names]
    regulator_indices += [i for i in np.where(active_regulators)[0] if i not in regulator_indices]
    checked_edges = [(i, j) for i in regulator_indices[:8]
                     for j in np.where(skeleton.to_numpy()[i] != 0)[0][:3]]
    for regulator_index, target_index in checked_edges:
        regulator, target = str(data.var_names[regulator_index]), str(data.var_names[target_index])
        source_weight = float(targets_by_regulators.loc[target, regulator])
        stored = int(skeleton.loc[regulator, target])
        model_weight = int(W[target_index, regulator_index])
        if source_weight == 0 or stored != model_weight:
            raise ValueError(f"GRN direction assertion failed for {regulator} -> {target}.")
        examples.append({"regulator": regulator, "target": target,
                         "source_weight": source_weight, "skeleton_regulator_target": stored,
                         "W_target_regulator": model_weight})
    pd.DataFrame(examples).to_csv(output / "tables" / "grn_orientation_assertions.csv", index=False)
    pd.DataFrame({"feature_index": np.arange(data.n_vars), "gene": data.var_names}).to_csv(
        output / "tables" / "aligned_gene_order.csv", index=False)
    result = {"status": "PASS", "input_shape": original_shape,
              "processed_shape": list(data.shape), "velocity_genes": len(velocity_genes),
              "n_regulators": int(data.var["TF"].sum()),
              "n_active_prior_regulators": int(active_regulators.sum()), "n_prior_edges": len(rr),
              "moments_preserved": moments_kept and not options.get("recompute_moments", False),
              "normalization_repeated": False, "smoke_test": maximum is not None,
              "grn_input_orientation": orientation,
              "grn_stored_orientation": "regulator_by_target",
              "model_W_orientation": "target_by_regulator",
              "labelled_edge_orientation_assertions": len(examples),
              "artifacts": [str(output / "prepared.h5ad"), str(output / "baseline_input.h5ad"),
                            str(output / "tables" / "aligned_gene_order.csv"),
                            str(output / "tables" / "grn_orientation_assertions.csv")],
              "scientific_qc": "Requires velocity direction and biological checks."}
    _json(output / "prepare_qc.json", result)
    return result


def run_fit(config: dict, output: Path):
    import anndata as ad
    import numpy as np
    import pandas as pd
    import torch
    from regvelo import REGVELOVI
    from lightning.pytorch.callbacks import ModelCheckpoint
    from scvi.train import SaveCheckpoint

    output = _directories(output)
    _seed(config)
    data = ad.read_h5ad(output / "prepared.h5ad")
    mode = config.get("mode", "hard")
    if mode not in ("hard", "soft", "soft_regularized"):
        raise ValueError(f"Unknown RegVelo mode: {mode}")
    lam2 = float(config.get("lam2", config.get("l1", 0.1))) if mode == "soft_regularized" else 0.0
    if mode == "soft_regularized" and not 0 < lam2 <= 1:
        raise ValueError("soft_regularized requires 0 < lam2 <= 1.")
    regulators = data.var_names[data.var["TF"].astype(bool)].tolist()
    W = torch.tensor(np.asarray(data.uns["skeleton"]), dtype=torch.float32).T
    REGVELOVI.setup_anndata(data, spliced_layer="Ms", unspliced_layer="Mu")
    model = REGVELOVI(data, W=W, regulators=regulators, soft_constraint=mode != "hard",
                     lam=float(config.get("lam", 1)), lam2=lam2,
                     **config.get("model_kwargs", {}))
    options = dict(config.get("train", {}))
    options.setdefault("max_epochs", 1500)
    checkpoint = ModelCheckpoint(dirpath=str(output / "checkpoints"), save_top_k=0,
                                 save_last=True, every_n_epochs=int(config.get("checkpoint_every", 50)))
    official_checkpoint = SaveCheckpoint(dirpath=str(output / "checkpoints" / "official"),
                                        monitor="elbo_validation", save_top_k=1,
                                        every_n_epochs=int(config.get("checkpoint_every", 50)))
    options["enable_checkpointing"] = True
    options["callbacks"] = [checkpoint, official_checkpoint]
    try:
        model.train(**options)
    except (Exception, KeyboardInterrupt) as error:
        # Preserve partial official weights; automatic optimizer continuation is not implemented.
        model.save(str(output / "model_partial"), overwrite=True)
        for metric, frame in (model.history or {}).items():
            frame.to_csv(output / "tables" / f"partial_training_{metric}.csv", index_label="epoch")
        _json(output / "fit_interrupted.json", {"status": "PARTIAL", "error": str(error),
               "partial_model": str(output / "model_partial"), "checkpoint": checkpoint.last_model_path,
               "optimizer_resume": "NOT_IMPLEMENTED"})
        raise
    model.save(str(output / "model"), overwrite=True)
    # Save the registered data to support an exact save/load validation.
    data.write_h5ad(output / "prepared.h5ad", compression="gzip")
    histories = []
    history_finite = True
    for metric, frame in model.history.items():
        history_finite = history_finite and bool(np.isfinite(frame.to_numpy(dtype=float)).all())
        frame.to_csv(output / "tables" / f"training_{metric}.csv", index_label="epoch")
        histories.append(frame.rename(columns={frame.columns[0]: metric}))
    history = pd.concat(histories, axis=1) if histories else pd.DataFrame()
    history.to_csv(output / "tables" / "training_history.csv", index_label="epoch")
    loaded = REGVELOVI.load(str(output / "model"), data)
    save_load_equal = all(torch.equal(value.detach().cpu(), loaded.module.state_dict()[key].detach().cpu())
                          for key, value in model.module.state_dict().items())
    weights = model.module.v_encoder.fc1.weight.detach().cpu().numpy()
    result = {"status": "PASS", "mode": mode, "lam": float(config.get("lam", 1)),
              "lam2": lam2, "training_options": {key: value for key, value in options.items() if key != "callbacks"},
              "periodic_checkpoint": checkpoint.last_model_path,
              "official_periodic_checkpoint": official_checkpoint.best_model_path,
              "optimizer_resume": "NOT_IMPLEMENTED",
              "epochs_recorded": len(history), "history_finite": history_finite,
              "weights_finite": bool(np.isfinite(weights).all()),
              "save_load_equal": save_load_equal,
              "artifacts": [str(output / "model" / "model.pt"),
                            str(output / "tables" / "training_history.csv"), str(output / "fit_qc.json")],
              "batch_size_deviation_from_official_fullbatch": options.get("batch_size") is not None,
              "scientific_qc": {"convergence": "REVIEW_REQUIRED",
                                "seed_stability": "NOT_RUN"}}
    if not (result["history_finite"] and result["weights_finite"] and save_load_equal):
        result["status"] = "FAIL"
    _json(output / "fit_qc.json", result)
    logging.info("Training completed: %s", result)
    return result


def run_velocity(config: dict, output: Path):
    import anndata as ad
    import numpy as np
    import pandas as pd
    import scvelo as scv
    from regvelo import REGVELOVI
    from scipy.stats import spearmanr

    output = _directories(output)
    data = ad.read_h5ad(output / "prepared.h5ad")
    model = REGVELOVI.load(str(output / "model"), data)
    _seed(config)
    data = model.add_regvelo_outputs_to_adata(adata=data, **_posterior(config))
    for layer in ("velocity", "fit_t", "latent_time_regvelo"):
        values = np.asarray(data.layers[layer])
        if values.shape != data.shape or not np.isfinite(values).all():
            raise ValueError(f"Invalid RegVelo output {layer}: {values.shape}")
    mean_time = np.asarray(data.layers["fit_t"]).mean(axis=1)
    span = np.ptp(mean_time)
    data.obs["latent_time"] = (mean_time - mean_time.min()) / span if span > 0 else 0
    data.obs["latent_time_posterior_mean"] = np.asarray(data.layers["latent_time_regvelo"]).mean(axis=1)
    uncertainty_samples = int(config.get("posterior", {}).get("uncertainty_samples", 10))
    if uncertainty_samples >= 2:
        draws = model.get_velocity(n_samples=uncertainty_samples, return_mean=False,
                                   return_numpy=True, batch_size=_posterior(config)["batch_size"])
        if draws.shape != (uncertainty_samples, data.n_obs, data.n_vars) or not np.isfinite(draws).all():
            raise ValueError("Invalid posterior velocity samples for uncertainty estimation.")
        scaling = 20 / np.asarray(data.layers["latent_time_regvelo"]).max(axis=0)
        data.layers["velocity_std"] = draws.std(axis=0, ddof=1) / scaling
        data.uns["velocity_uncertainty"] = {"n_samples": uncertainty_samples, "definition": "Posterior sample SD, ddof=1; same gene-wise time scaling as saved velocity; not between-seed stability"}
    scv.tl.velocity_graph(data, n_jobs=int(config.get("n_jobs", 1)))
    scv.tl.velocity_embedding(data, basis="umap")
    data.write_h5ad(output / "velocity.h5ad", compression="gzip")
    data.obs.to_csv(output / "tables" / "cell_dynamics.csv", index_label="cell")
    pd.DataFrame(model.get_rates(), index=data.var_names).to_csv(
        output / "tables" / "kinetic_rates.csv", index_label="gene")
    baseline = ad.read_h5ad(output / "baseline_input.h5ad")[:, data.var_names].copy()
    scv.tl.velocity(baseline, mode="stochastic")
    scv.tl.velocity_graph(baseline, n_jobs=int(config.get("n_jobs", 1)))
    scv.tl.velocity_embedding(baseline, basis="umap")
    baseline.write_h5ad(output / "scvelo_stochastic.h5ad", compression="gzip")
    result = {"status": "PASS", "shape": list(data.shape),
              "artifacts": [str(output / "velocity.h5ad"), str(output / "scvelo_stochastic.h5ad"),
                            str(output / "tables" / "cell_dynamics.csv"), str(output / "velocity_qc.json")],
              "velocity_finite": True, "mean_fit_t_range": [float(mean_time.min()), float(mean_time.max())],
              "normalized_latent_time_range": [float(data.obs["latent_time"].min()), float(data.obs["latent_time"].max())],
              "scvelo_baseline": "stochastic", "scientific_qc": {"direction": "REVIEW_REQUIRED"}}
    time_key = config.get("time_key")
    if time_key in data.obs:
        times = pd.to_numeric(data.obs[time_key], errors="coerce")
        time_scale = "numeric_annotation"
        if config.get("time_order"):
            order = config["time_order"]
            if not set(data.obs[time_key].unique()).issubset(order):
                raise ValueError("time_order must include every observed time annotation.")
            times = data.obs[time_key].astype(str).map({label: index for index, label in enumerate(order)})
            time_scale = "explicit_stage_ordinal_not_elapsed_time"
        valid = times.notna()
        if valid.sum() > 2 and times[valid].nunique() > 1:
            corr = spearmanr(times[valid], data.obs.loc[valid, "latent_time"])
            result["time_correlation"] = {"key": time_key, "n_cells": int(valid.sum()),
                                          "scale": time_scale,
                                          "spearman_rho": float(corr.statistic), "pvalue": float(corr.pvalue)}
    _json(output / "velocity_qc.json", result)
    return result


def _kernel(data, config):
    import cellrank as cr

    velocity = cr.kernels.VelocityKernel(data).compute_transition_matrix(n_jobs=int(config.get("n_jobs", 1)))
    mix = float(config.get("fate", {}).get("kernel_mix", 0.8))
    if not 0 <= mix <= 1:
        raise ValueError("fate.kernel_mix must be in [0,1].")
    if mix == 1:
        return velocity, velocity
    connectivity = cr.kernels.ConnectivityKernel(data).compute_transition_matrix()
    return velocity, mix * velocity + (1 - mix) * connectivity


def _save_fate(data, estimator, kernel, path, tables_prefix):
    import numpy as np
    import pandas as pd
    from scipy import sparse

    probabilities = np.asarray(estimator.fate_probabilities)
    names = estimator.fate_probabilities.names.tolist()
    diagnostics = {"finite": bool(np.isfinite(probabilities).all()),
                   "minimum": float(np.nanmin(probabilities)), "maximum": float(np.nanmax(probabilities)),
                   "max_row_sum_error": float(np.max(np.abs(probabilities.sum(axis=1) - 1))),
                   "row_sum_range": [float(probabilities.sum(axis=1).min()), float(probabilities.sum(axis=1).max())]}
    _json(tables_prefix.with_name(tables_prefix.name + "_probability_validation.json"), diagnostics)
    if (not np.isfinite(probabilities).all() or probabilities.min() < -1e-10
            or probabilities.max() > 1 + 1e-10
            or not np.allclose(probabilities.sum(axis=1), 1, atol=1e-5, rtol=0)):
        pd.DataFrame(probabilities, index=data.obs_names, columns=names).to_csv(
            tables_prefix.with_name(tables_prefix.name + "_FAILED_raw_fate_probabilities.csv"))
        raise ValueError(f"Invalid CellRank fate probabilities or row sums: {diagnostics}")
    data.obsm["lineages_fwd"] = estimator.fate_probabilities
    logp = np.zeros_like(probabilities)
    np.log2(probabilities, where=probabilities > 0, out=logp)
    data.obs["commitment_score"] = 1 + (probabilities * logp).sum(axis=1) / np.log2(len(names))
    data.write_h5ad(path, compression="gzip")
    pd.DataFrame(probabilities, index=data.obs_names, columns=names).to_csv(
        tables_prefix.with_name(tables_prefix.name + "_fate_probabilities.csv"), index_label="cell")
    sparse.save_npz(tables_prefix.with_name(tables_prefix.name + "_transition_matrix.npz"),
                    sparse.csr_matrix(kernel.transition_matrix))
    return names


def run_fate(config: dict, output: Path):
    import anndata as ad
    import cellrank as cr
    import pandas as pd
    from scipy import sparse

    output = _directories(output)
    _seed(config)
    data = ad.read_h5ad(output / "velocity.h5ad")
    group = config.get("group_key", "cell_type")
    data.obs[group] = data.obs[group].astype("category")
    options = config.get("fate", {})
    terminal = config["terminal_states"]
    if len(terminal) < 2 or not set(terminal).issubset(data.obs[group].unique()):
        raise ValueError("At least two terminal states must be supported by cell annotations.")
    velocity, kernel = _kernel(data, config)
    estimator = cr.estimators.GPCCA(kernel)
    estimator.compute_macrostates(n_states=int(options.get("n_states", 7)),
                                 n_cells=int(options.get("n_cells", 30)), cluster_key=group)
    estimator.set_terminal_states(terminal)
    # Avoid CellRank 2.0.7's missing-PETSc fallback silently replacing direct with GMRES.
    estimator.compute_fate_probabilities(solver=options.get("solver", "direct"), use_petsc=False)
    names = _save_fate(data, estimator, kernel, output / "fate.h5ad", output / "tables" / "baseline")
    estimator.write(str(output / "cellrank_gpcca.pkl"))
    pd.DataFrame({"macrostate": estimator.macrostates, "terminal_state": estimator.terminal_states}).to_csv(
        output / "tables" / "cellrank_states.csv", index_label="cell")
    terminal_sets = {name: estimator.terminal_states.index[estimator.terminal_states == name].tolist()
                     for name in names}
    if any(not cells for cells in terminal_sets.values()):
        raise ValueError("CellRank produced an empty terminal cell set.")
    _json(output / "terminal_cell_sets.json", terminal_sets)
    sparse.save_npz(output / "tables" / "velocity_transition_matrix.npz",
                    sparse.csr_matrix(velocity.transition_matrix))
    result = {"status": "PASS", "terminal_states": names,
              "artifacts": [str(output / "fate.h5ad"), str(output / "cellrank_gpcca.pkl"),
                            str(output / "terminal_cell_sets.json"),
                            str(output / "tables" / "baseline_fate_probabilities.csv"),
                            str(output / "tables" / "baseline_transition_matrix.npz")],
              "terminal_cell_counts": {key: len(value) for key, value in terminal_sets.items()},
              "kernel_mix": options.get("kernel_mix", 0.8),
              "probability_solver": options.get("solver", "direct"), "use_petsc": False,
              "fate_probabilities_finite": True, "fate_row_sums_one": True,
              "scientific_qc": "Terminal annotations require biological interpretation."}
    _json(output / "fate_qc.json", result)
    return result


def run_perturb(config: dict, output: Path):
    import anndata as ad
    import cellrank as cr
    import numpy as np
    import pandas as pd
    import regvelo as rgv
    import scvelo as scv
    from regvelo import REGVELOVI

    output = _directories(output)
    data = ad.read_h5ad(output / "fate.h5ad")
    terminal_sets = json.loads((output / "terminal_cell_sets.json").read_text(encoding="utf-8"))
    terminal = list(terminal_sets)
    # CellRank sorts names when converting a dict; preserve the baseline column order explicitly.
    terminal_labels = pd.Series(pd.Categorical([None] * data.n_obs, categories=terminal), index=data.obs_names)
    for name, cells in terminal_sets.items():
        terminal_labels.loc[cells] = name
    options = config.get("perturb", {})
    candidates = options.get("tfs", config.get("tfs", ["elf1"]))
    if isinstance(candidates, str):
        candidates = [candidates]
    missing = set(candidates).difference(data.var_names)
    if missing:
        raise ValueError(f"Perturbation TFs absent from prepared features: {sorted(missing)}")
    model_path = str(output / "model")
    model = REGVELOVI.load(model_path, data)
    weights = model.module.v_encoder.fc1.weight.detach().clone()
    cutoff = float(options.get("cutoff", 0))
    effects = float(options.get("effects", 0))
    solver = config.get("fate", {}).get("solver", "direct")

    def simulation(tf, customized=None):
        # Seed before official load+sampling in both arms to pair posterior random draws.
        _seed(config)
        result, perturbed_model = rgv.tl.in_silico_block_simulation(
            model=model_path, adata=data.copy(), TF=tf, cutoff=cutoff, effects=effects,
            customized_GRN=customized, **_posterior(config))
        _, kernel = _kernel(result, config)
        estimator = cr.estimators.GPCCA(kernel)
        estimator.set_terminal_states(terminal_labels)
        estimator.compute_fate_probabilities(solver=solver, use_petsc=False)
        if not result.obs_names.equals(data.obs_names) or not result.var_names.equals(data.var_names):
            raise ValueError("Perturbation changed the cell or gene order.")
        if estimator.fate_probabilities.names.tolist() != terminal:
            raise ValueError("Perturbation changed the lineage column order.")
        return result, perturbed_model, estimator, kernel

    baseline, _, baseline_estimator, baseline_kernel = simulation([], weights.clone())
    scv.tl.velocity_graph(baseline, n_jobs=int(config.get("n_jobs", 1)))
    scv.tl.velocity_embedding(baseline, basis="umap")
    _save_fate(baseline, baseline_estimator, baseline_kernel, output / "baseline_posterior.h5ad",
               output / "tables" / "paired_baseline")
    null, _, null_estimator, null_kernel = simulation([], weights.clone())
    _save_fate(null, null_estimator, null_kernel, output / "perturb_null.h5ad", output / "tables" / "null")
    null_velocity_diff = float(np.max(np.abs(np.asarray(null.layers["velocity"]) - np.asarray(baseline.layers["velocity"]))))
    null_fate_diff = float(np.max(np.abs(np.asarray(null_estimator.fate_probabilities) -
                                       np.asarray(baseline_estimator.fate_probabilities))))
    perturbed = {"NULL": null}
    zero_columns = np.where((weights.detach().abs().cpu().numpy() <= cutoff).all(axis=0))[0]
    negative_qc = {"status": "NOT_APPLICABLE", "reason": "No zero-edge gene column at the chosen cutoff."}
    if len(zero_columns):
        negative_gene = str(data.var_names[zero_columns[0]])
        negative, _, negative_estimator, negative_kernel = simulation(negative_gene)
        _save_fate(negative, negative_estimator, negative_kernel, output / "perturb_no_edges.h5ad",
                   output / "tables" / "no_edges")
        negative_diff = float(np.max(np.abs(np.asarray(negative.layers["velocity"]) -
                                           np.asarray(baseline.layers["velocity"]))))
        negative_fate_diff = float(np.max(np.abs(np.asarray(negative_estimator.fate_probabilities) -
                                                np.asarray(baseline_estimator.fate_probabilities))))
        negative_qc = {"status": "PASS" if negative_diff < 1e-6 and negative_fate_diff < 1e-6 else "FAIL",
                       "gene": negative_gene, "control_definition": "Gene column with no effective downstream weights.",
                       "velocity_max_abs_difference": negative_diff, "fate_max_abs_difference": negative_fate_diff}
        perturbed["NO_EDGES_" + negative_gene] = negative
    summary = []
    for tf in candidates:
        if not str(tf).replace("_", "").replace("-", "").replace(".", "").isalnum():
            raise ValueError(f"TF name cannot be used as an output filename: {tf}")
        column = data.var_names.get_loc(tf)
        active = weights[:, column].abs().cpu().numpy() > cutoff
        if not active.any():
            raise ValueError(f"{tf} has no effective downstream edges at cutoff {cutoff}.")
        target, knockout_model, estimator, kernel = simulation(tf)
        base_v = np.asarray(baseline.layers["velocity"])
        target_v = np.asarray(target.layers["velocity"])
        delta = target_v - base_v
        denominator = np.linalg.norm(base_v, axis=1) * np.linalg.norm(target_v, axis=1)
        cosine = np.divide((base_v * target_v).sum(axis=1), denominator,
                           out=np.full(data.n_obs, np.nan), where=denominator > 0)
        target.obs["perturbation_effect_cosine"] = 1 - np.clip(cosine, -1, 1)
        target.obs["perturbation_velocity_l2"] = np.linalg.norm(delta, axis=1)
        target.obsm["fate_probability_difference"] = (np.asarray(estimator.fate_probabilities) -
                                                     np.asarray(baseline_estimator.fate_probabilities))
        scv.tl.velocity_graph(target, n_jobs=int(config.get("n_jobs", 1)))
        scv.tl.velocity_embedding(target, basis="umap")
        _save_fate(target, estimator, kernel, output / f"perturb_{tf}.h5ad", output / "tables" / tf)
        pd.DataFrame(target.obsm["fate_probability_difference"], index=data.obs_names,
                     columns=terminal).to_csv(output / "tables" / f"{tf}_fate_difference.csv", index_label="cell")
        target.obs[["perturbation_effect_cosine", "perturbation_velocity_l2"]].to_csv(
            output / "tables" / f"{tf}_cell_effect.csv", index_label="cell")
        after = knockout_model.module.v_encoder.fc1.weight.detach().cpu().numpy()
        pd.DataFrame({"regulator": tf, "target": data.var_names[active],
                      "weight_before": weights[:, column].detach().cpu().numpy()[active],
                      "weight_after": after[:, column][active]}).to_csv(
            output / "tables" / f"{tf}_blocked_edges.csv", index=False)
        perturbed[tf] = target
        summary.append({"TF": tf, "blocked_edges": int(active.sum()),
                        "mean_velocity_l2": float(np.linalg.norm(delta, axis=1).mean())})
    statistics = rgv.mt.cellfate_perturbation(perturbed=perturbed, baseline=baseline,
                                           terminal_state=terminal, method="likelihood")
    statistics.to_csv(output / "tables" / "perturbation_depletion.csv", index=False)
    pd.DataFrame(summary).to_csv(output / "tables" / "perturbation_summary.csv", index=False)
    result = {"status": "PASS" if null_velocity_diff < 1e-6 and null_fate_diff < 1e-6
              and negative_qc["status"] != "FAIL" else "FAIL",
              "targets": summary, "cutoff": cutoff, "effects": effects,
              "artifacts": [str(output / "baseline_posterior.h5ad"), str(output / "perturb_null.h5ad"),
                            str(output / "tables" / "perturbation_depletion.csv"),
                            *[str(output / f"perturb_{tf}.h5ad") for tf in candidates]],
              "no_op_velocity_max_abs_difference": null_velocity_diff,
              "no_op_fate_max_abs_difference": null_fate_diff,
              "no_effective_edges_control": negative_qc,
              "terminal_cells_frozen": True, "posterior_draws_paired_by_seed": True,
              "scientific_qc": {"interpretation": "Regulon-level in silico knockout; not experimental CRISPR.",
                                "seed_stability": "NOT_RUN", "cutoff_sensitivity": "NOT_RUN"}}
    _json(output / "perturb_qc.json", result)
    return result
