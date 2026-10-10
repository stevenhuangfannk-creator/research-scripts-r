"""Read-only numerical evidence check of completed fate, GRN and KO plots."""
import json
from pathlib import Path
import anndata as ad
import numpy as np
import pandas as pd

workspace = Path(__file__).resolve().parents[2]
output = workspace / "outputs/regvelo_results/official_zebrafish/hard_seed0"
logs = workspace / "outputs/research-scripts-r/03_cell_dynamics/RegVelo_GRN_Dynamics/tests/validation_logs/plot_evidence_check"
checks = {}

def csv(name, index=None, figure=False):
    return pd.read_csv(output / ("figures" if figure else "tables") / (name + ".csv"), index_col=index, keep_default_na=name!="E04_source" and name!="perturbation_depletion")

def close(label, actual, expected, atol=1e-9):
    np.testing.assert_allclose(np.asarray(actual), np.asarray(expected), rtol=1e-7, atol=atol)
    checks[label] = {"status":"PASS", "elements":int(np.asarray(actual).size),
                     "maximum_absolute_error":float(np.abs(np.asarray(actual)-np.asarray(expected)).max(initial=0))}

fate = ad.read_h5ad(output / "fate.h5ad")
probs = csv("baseline_fate_probabilities", 0).reindex(fate.obs_names)
source = csv("C03_source", figure=True)
assert source.cell.tolist() == fate.obs_names.tolist()
close("C03 saved fate probabilities", source[probs.columns], probs)
values = probs.to_numpy()
terms = np.zeros_like(values)
positive = values > 0
terms[positive] = values[positive] * np.log(values[positive])
expected = 1 + terms.sum(axis=1) / np.log(values.shape[1])
close("C04 normalized entropy definition", csv("C04_source", figure=True).commitment_score, expected)
assert np.max(np.abs(values.sum(axis=1)-1)) < 1e-10
checks["C03 probability simplex"] = {"status":"PASS", "maximum_row_sum_error":float(np.max(np.abs(values.sum(axis=1)-1)))}

edges = csv("tf_target_edges").set_index(["regulator","target"])
for identifier in ["D01","D04"]:
    selected = csv(identifier+"_source", figure=True).set_index(["regulator","target"])
    close(identifier+" saved effective weights", selected.weight, edges.reindex(selected.index).weight)
heat = csv("D02_source", figure=True).set_index(["regulator","target"])
close("D02 weight matrix including absent-edge zeros", heat.weight, edges.weight.reindex(heat.index, fill_value=0))

paired = ad.read_h5ad(output / "baseline_posterior.h5ad")
ko = ad.read_h5ad(output / "perturb_elf1.h5ad")
assert paired.obs_names.equals(ko.obs_names) and paired.var_names.equals(ko.var_names)
velocity_source = csv("E01_source", figure=True)
assert velocity_source.cell.tolist() == paired.obs_names.tolist()
close("E01 paired baseline projected velocity", velocity_source[["baseline_v1","baseline_v2"]], paired.obsm["velocity_umap"])
close("E01 independently projected KO velocity", velocity_source[["KO_v1","KO_v2"]], ko.obsm["velocity_umap"])
effects = csv("elf1_cell_effect", 0).reindex(ko.obs_names)
effect_source = csv("E02_source", figure=True)
for key in ["perturbation_velocity_l2","perturbation_effect_cosine"]:
    close("E02 "+key, effect_source[key], effects[key])
difference = csv("elf1_fate_difference", 0).reindex(ko.obs_names)
fate_source = csv("E03_source", figure=True)
close("E03 saved paired fate difference", fate_source[difference.columns], difference)
close("E03 equals KO minus paired baseline", difference, np.asarray(ko.obsm["lineages_fwd"])-np.asarray(paired.obsm["lineages_fwd"]))
depletion = csv("perturbation_depletion")
depletion_source = csv("E04_source", figure=True)
pd.testing.assert_frame_equal(depletion_source, depletion)
null = depletion_source[depletion_source.TF == "NULL"]
assert len(null) == 4 and (null["Depletion likelihood"] == .5).all()
checks["E04 official statistics and literal NULL"] = {"status":"PASS", "rows":len(depletion), "NULL_rows":len(null), "neutral_AUC":.5}
blocked = csv("elf1_blocked_edges").set_index(["regulator","target"])
blocked_source = csv("E06_source", figure=True).set_index(["regulator","target"])
close("E06 weights before block", blocked_source.weight_before, blocked.reindex(blocked_source.index).weight_before)
assert (blocked_source.weight_after == 0).all()
checks["E06 weights after block"] = {"status":"PASS", "plotted_edges":len(blocked_source), "after_maximum_absolute_weight":0}

result = {"status":"PASS", "scope":"Saved C/D/E figure values, cell pairing, entropy definition and NULL labels; no model retraining or biological validation.", "checks":checks}
(logs / "cd_e_evidence.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"status":"PASS", "checks":len(checks)}, ensure_ascii=False))
