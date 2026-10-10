"""Recheck a saved model and individually logged metrics without retraining or hiding logging gaps."""
import argparse
import json
import sys
from pathlib import Path

sys.path = [entry for entry in sys.path if Path(entry).resolve() != Path(__file__).resolve().parent]
import anndata as ad
import numpy as np
import pandas as pd
import torch
from regvelo import REGVELOVI


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    qc = json.loads((output / "fit_qc.json").read_text(encoding="utf-8"))
    data = ad.read_h5ad(output / "prepared.h5ad")
    model = REGVELOVI.load(str(output / "model"), data, accelerator="cpu")
    state = torch.load(output / "model" / "model.pt", map_location="cpu", weights_only=False)["model_state_dict"]
    reload_equal = all(torch.equal(value.cpu(), state[key].cpu()) for key, value in model.module.state_dict().items())
    finite_parameters = all(torch.isfinite(value).all().item() for value in model.module.parameters())
    records = {}
    for path in sorted((output / "tables").glob("training_*.csv")):
        if path.name == "training_history.csv":
            continue
        frame = pd.read_csv(path, index_col=0)
        records[path.stem] = {"n_records": len(frame), "nonfinite": int((~np.isfinite(frame.to_numpy(dtype=float))).sum())}
    if not records:
        raise ValueError("No individual training metric records available.")
    joined = pd.read_csv(output / "tables" / "training_history.csv", index_col=0)
    evidence = {"individual_metrics": records, "joined_missing_log_entries": joined.isna().sum().to_dict(),
                "individual_metrics_finite": all(item["nonfinite"] == 0 for item in records.values()),
                "all_parameters_finite": finite_parameters, "saved_weights_reload_equal": reload_equal,
                "explanation": "Sparse step logging has fewer records than epoch logging. Outer-joined missing entries are not numeric NaNs observed during training. Original per-metric CSVs and joined gaps are preserved."}
    (output / "fit_revalidation.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    passed = evidence["individual_metrics_finite"] and finite_parameters and reload_equal
    original = output / "fit_qc_initial.json"
    if not original.exists():
        original.write_text(json.dumps(qc, indent=2), encoding="utf-8")
    qc.update(status="PASS" if passed else "FAIL", history_finite=evidence["individual_metrics_finite"],
              history_joined_missing_entries=evidence["joined_missing_log_entries"], revalidation=str(output / "fit_revalidation.json"))
    (output / "fit_qc.json").write_text(json.dumps(qc, indent=2), encoding="utf-8")
    run_state = json.loads((output / "run_state.json").read_text(encoding="utf-8"))
    run_state["stages"]["fit"].update(qc)
    (output / "run_state.json").write_text(json.dumps(run_state, indent=2), encoding="utf-8")
    print(json.dumps(evidence, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
