"""Executed posterior-seed, cutoff and target-set sensitivity on one frozen model."""
import argparse
import gc
import hashlib
import json
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path = [p for p in sys.path if Path(p or ".").resolve() != SCRIPT_DIR]
sys.path.insert(0, str(SCRIPT_DIR.parent / "src"))

import anndata as ad
import cellrank as cr
import h5py
import numpy as np
import pandas as pd
import regvelo as rgv
from scipy.stats import spearmanr

from regvelo_workflow.cli import load_config, write_json
from regvelo_workflow.dynamics import _kernel, _posterior, _seed, _save_fate


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1048576), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--resume", action="store_true", help="Reuse checksummed completed simulations with the same config and model")
    args = parser.parse_args()
    config = load_config(args.config)
    source = Path(config["output"])
    output = source / "stability"
    output.mkdir(exist_ok=True)
    protected = [source / "fate.h5ad", source / "model/model.pt", source / "terminal_cell_sets.json"]
    hashes = {str(path): file_hash(path) for path in protected}
    fingerprint = hashlib.sha256(json.dumps({"config":config,"source_hashes":hashes}, sort_keys=True).encode()).hexdigest()
    checkpoint_path = output / "SENSITIVITY_STATE.json"
    checkpoint = json.loads(checkpoint_path.read_text()) if args.resume and checkpoint_path.exists() else {
        "fingerprint":fingerprint, "completed":{}}
    if checkpoint["fingerprint"] != fingerprint:
        raise ValueError("Sensitivity cache config or protected model/input hashes changed.")
    registry_qc = []

    def release_model(model):
        # scvi 1.2.0's class registry holds AnnData strongly even after deleting a model.
        model_id = model.id
        model.deregister_manager(model.adata)
        type(model)._per_instance_manager_store.pop(model_id, None)
        del model
        gc.collect()
    data = ad.read_h5ad(source / "fate.h5ad")
    sets = json.loads((source / "terminal_cell_sets.json").read_text(encoding="utf-8"))
    names = list(sets)
    labels = pd.Series(pd.Categorical([None] * data.n_obs, categories=names), index=data.obs_names)
    for name, cells in sets.items():
        labels.loc[cells] = name
    model = rgv.REGVELOVI.load(str(source / "model"), data)
    weights = model.module.v_encoder.fc1.weight.detach().clone()
    release_model(model)
    del model
    tfs = config["perturb"]["tfs"]
    cutoff0 = float(config["perturb"]["cutoff"])
    samples = []
    comparisons = []
    reference = {}
    identical = {}

    def cached(tag, n_targets):
        record = checkpoint["completed"][tag]
        for filename, expected in record["file_hashes"].items():
            if file_hash(output / filename) != expected:
                raise ValueError(f"Sensitivity cache artifact changed: {filename}")
        probabilities = pd.read_csv(output / f"{tag}_fate_probabilities.csv", index_col=0)
        # Read only cached numerical fields; whole AnnData copies also load unused GRN/graph metadata.
        with h5py.File(output / f"{tag}.h5ad", "r") as saved:
            cells = saved["obs"][saved["obs"].attrs["_index"]].asstr()[:].tolist()
            genes = saved["var"][saved["var"].attrs["_index"]].asstr()[:].tolist()
            velocity = saved["layers/velocity"][:]
            saved_fate = saved["obsm/lineages_fwd"][:]
        if (cells != data.obs_names.tolist() or genes != data.var_names.tolist()
                or probabilities.columns.tolist() != names or probabilities.index.tolist() != cells):
            raise ValueError("Cached cell/gene/lineage order changed.")
        fate = probabilities.to_numpy()
        if (not np.isfinite(velocity).all() or not np.isfinite(fate).all()
                or fate.min() < -1e-10 or fate.max() > 1+1e-10):
            raise ValueError("Non-finite cached results.")
        np.testing.assert_allclose(fate.sum(axis=1), 1, atol=1e-10, rtol=0)
        np.testing.assert_allclose(fate, saved_fate, atol=1e-14, rtol=0)
        return velocity, fate, n_targets

    def simulate(seed, tag, tf=None, cutoff=cutoff0, fraction=1.0):
        settings = dict(config, seed=seed)
        _seed(settings)
        custom = weights.clone()
        targets = []
        if tf is not None:
            column = data.var_names.get_loc(tf)
            strength = weights[:, column].abs().cpu().numpy()
            indices = np.flatnonzero(strength > cutoff)
            indices = indices[np.argsort(-strength[indices], kind="stable")]
            selected = indices[:max(1, int(np.ceil(len(indices) * fraction)))]
            custom[selected, column] = float(config["perturb"].get("effects", 0))
            targets = data.var_names[selected].tolist()
        signature = (seed, hashlib.sha256(custom.cpu().numpy().tobytes()).hexdigest())
        target_record = {"TF":tf,"seed":seed,"cutoff":cutoff,"fraction":fraction,
                         "selection":"strongest absolute fc1 weights, stable order","blocked_targets":targets}
        if args.resume and tag in checkpoint["completed"]:
            cached_targets = json.loads((output / f"{tag}_targets.json").read_text())
            for key in ("TF","seed","cutoff","fraction","blocked_targets"):
                if cached_targets[key] != target_record[key]:
                    raise ValueError(f"Cached target selection differs in {key}.")
            actual = cached(tag, len(targets))
            identical[signature] = tag
            print(f"Resumed checksummed {tag}", flush=True)
            return actual
        reused_tag = identical.get(signature)
        if reused_tag is not None:
            for suffix in (".h5ad", "_fate_probabilities.csv", "_transition_matrix.npz", "_probability_validation.json"):
                shutil.copy2(output / f"{reused_tag}{suffix}", output / f"{tag}{suffix}")
            target_record["reused_identical_weight_matrix_and_seed"] = reused_tag
        else:
            return compute(seed, tag, custom, targets, target_record, signature)
        finish(tag, target_record, signature)
        return cached(tag, len(targets))

    def finish(tag, target_record, signature):
        write_json(output / f"{tag}_targets.json", target_record)
        files = [f"{tag}{suffix}" for suffix in (".h5ad","_fate_probabilities.csv","_transition_matrix.npz","_targets.json")]
        checkpoint["completed"][tag] = {"file_hashes":{filename:file_hash(output / filename) for filename in files}}
        write_json(checkpoint_path, checkpoint)
        identical[signature] = tag

    def compute(seed, tag, custom, targets, target_record, signature):
        _seed(dict(config, seed=seed))
        result, sampled_model = rgv.tl.in_silico_block_simulation(
            model=str(source / "model"), adata=data.copy(), TF=[], customized_GRN=custom,
            **_posterior(config))
        if not np.isfinite(result.layers["velocity"]).all():
            raise ValueError("Non-finite posterior velocity in sensitivity run.")
        # These source-derived fields were not recomputed for this posterior draw.
        result.layers.pop("velocity_std", None)
        result.obsm.pop("velocity_umap", None)
        for key in ("velocity_graph", "velocity_graph_neg", "velocity_uncertainty"):
            result.uns.pop(key, None)
        for key in ("velocity_self_transition", "latent_time_posterior_mean"):
            if key in result.obs:
                del result.obs[key]
        times = np.asarray(result.layers["fit_t"]).mean(axis=1)
        span = np.ptp(times)
        result.obs["latent_time"] = (times - times.min()) / span if span else 0
        if not result.obs_names.equals(data.obs_names) or not result.var_names.equals(data.var_names):
            raise ValueError("Cell/gene order changed in sensitivity run.")
        _, kernel = _kernel(result, config)
        estimator = cr.estimators.GPCCA(kernel).set_terminal_states(labels)
        estimator.compute_fate_probabilities(solver="direct", use_petsc=False)
        if estimator.fate_probabilities.names.tolist() != names:
            raise ValueError("Lineage order changed in sensitivity run.")
        _save_fate(result, estimator, kernel, output / f"{tag}.h5ad", output / tag)
        values = (np.asarray(result.layers["velocity"]).copy(), np.asarray(estimator.fate_probabilities).copy(), len(targets))
        release_model(sampled_model)
        del sampled_model, result, estimator, kernel
        gc.collect()
        registry_qc.append({"tag":tag, "model_instance_buckets":len(rgv.REGVELOVI._per_instance_manager_store),
                            "setup_manager_buckets":len(rgv.REGVELOVI._setup_adata_manager_store)})
        write_json(output / "MANAGER_RELEASE_QC.json", registry_qc)
        finish(tag, target_record, signature)
        return values

    baselines = {}
    # Prespecified grid: posterior seeds 0,1,2; cutoffs 0,.001,.01; strongest 50% targets.
    grid = [(seed, cutoff0, 1.0, "posterior_seed") for seed in (0, 1, 2)]
    grid += [(0, cutoff, 1.0, "cutoff") for cutoff in (0.0, 0.01) if cutoff != cutoff0]
    grid += [(0, cutoff0, 0.5, "target_subset")]
    for seed in (0, 1, 2):
        baselines[seed] = simulate(seed, f"baseline_seed{seed}")
    for seed, cutoff, fraction, axis in grid:
        for tf in tfs:
            tag = f"{tf}_seed{seed}_cutoff{cutoff:g}_fraction{fraction:g}"
            velocity, fate, n_targets = simulate(seed, tag, tf, cutoff, fraction)
            base_v, base_p, _ = baselines[seed]
            delta = fate - base_p
            effect = np.linalg.norm(velocity - base_v, axis=1)
            pd.DataFrame(delta, index=data.obs_names, columns=names).to_csv(output / f"{tag}_fate_delta.csv")
            pd.DataFrame({"velocity_l2": effect}, index=data.obs_names).to_csv(output / f"{tag}_effect.csv")
            for index, lineage in enumerate(names):
                samples.append({"TF": tf, "seed": seed, "cutoff": cutoff, "target_fraction": fraction,
                                "axis": axis, "lineage": lineage, "blocked_edges": n_targets,
                                "mean_fate_delta": float(delta[:, index].mean()),
                                "mean_velocity_l2": float(effect.mean())})
            if seed == 0 and cutoff == cutoff0 and fraction == 1:
                reference[tf] = (delta, effect)
            else:
                ref_delta, ref_effect = reference[tf]
                effect_rho = float(spearmanr(effect, ref_effect).statistic)
                for index, lineage in enumerate(names):
                    mean, ref_mean = delta[:, index].mean(), ref_delta[:, index].mean()
                    comparisons.append({"TF": tf, "seed": seed, "cutoff": cutoff,
                                        "target_fraction": fraction, "axis": axis, "lineage": lineage,
                                        "cell_fate_delta_spearman": float(spearmanr(delta[:, index], ref_delta[:, index]).statistic),
                                        "cell_effect_spearman": effect_rho,
                                        "mean_fate_delta": float(mean), "reference_mean_fate_delta": float(ref_mean),
                                        "direction_agrees": bool(np.sign(mean) == np.sign(ref_mean)),
                                        "both_mean_effects_above_1e4": bool(abs(mean) > 1e-4 and abs(ref_mean) > 1e-4)})
            print(f"Completed {tag}: {n_targets} blocked edges", flush=True)
    pd.DataFrame(samples).to_csv(output / "sensitivity_summary.csv", index=False)
    compared = pd.DataFrame(comparisons)
    compared.to_csv(output / "sensitivity_comparisons.csv", index=False)
    seed_rows = compared[compared.axis == "posterior_seed"]
    relevant = seed_rows[seed_rows.both_mean_effects_above_1e4]
    unchanged = all(file_hash(path) == hashes[str(path)] for path in protected)
    stable = bool((seed_rows.cell_effect_spearman >= .8).all() and relevant.direction_agrees.all())
    result = {"status": "PASS" if unchanged and stable else "PARTIAL", "execution_status": "PASS",
              "scope": "Posterior-sampling stability of ONE trained seed0 model; NOT training-seed stability",
              "grid": {"seeds": [0, 1, 2], "cutoffs": [0, cutoff0, .01], "target_fractions": [1, .5]},
              "n_posterior_samples": _posterior(config)["n_samples"], "source_hashes": hashes,
              "source_files_unchanged": unchanged,
              "posterior_effect_rank_min_spearman": float(seed_rows.cell_effect_spearman.min()),
              "posterior_fate_delta_min_spearman": float(seed_rows.cell_fate_delta_spearman.min()),
              "nontrivial_mean_direction_agreement": float(relevant.direction_agrees.mean()) if len(relevant) else None,
              "posterior_stability_pass": stable,
              "criterion": "cell-effect Spearman >=0.8, same mean-fate sign when both magnitudes >1e-4",
              "training_seed_stability": "NOT_RUN", "biological_validation": "NOT_RUN",
              "resume_fingerprint":fingerprint, "completed_conditions":len(checkpoint["completed"]),
              "identical_matrix_reuse": "Matching posterior seed and exact modified weight bytes reuse actual saved simulation; recorded per condition",
              "scvi_manager_release_qc":registry_qc,
              "interpretation": "Cutoff and strongest-half sensitivity describe model dependence, not experimental robustness."}
    write_json(output / "STABILITY_QC.json", result)
    if not unchanged:
        raise ValueError("Protected formal files changed.")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
