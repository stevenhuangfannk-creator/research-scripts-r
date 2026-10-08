"""Export existing AnnData UMAP only. No expression changes, clustering or plotting."""
import argparse
import hashlib
import json
from pathlib import Path
import anndata as ad
import numpy as np

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--input", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
if args.output.exists():
    raise FileExistsError("Use a fresh output path; existing data are never overwritten")
a = ad.read_h5ad(args.input, backed="r")
xy = np.asarray(a.obsm["X_umap"])
assert xy.shape == (a.n_obs, 2) and np.isfinite(xy).all()
assert a.obs_names.is_unique
frame = a.obs[["sample_id", "condition", "celltype_broad"]].copy()
assert frame.notna().all().all()
frame.index.name = "cell_id"
frame = frame.rename(columns={"celltype_broad": "group"})
frame["x"], frame["y"] = xy[:, 0], xy[:, 1]
args.output.parent.mkdir(parents=True, exist_ok=True)
frame.to_csv(args.output)
receipt = {"source_file": args.input.name, "source_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
           "cells": a.n_obs, "genes_in_source": a.n_vars, "exported_expression": False,
           "excluded_cells": 0, "embedding_key": "X_umap", "group_key": "celltype_broad",
           "sample_counts": frame.sample_id.value_counts().to_dict(),
           "condition_counts": frame.condition.value_counts().to_dict(),
           "label_counts": frame.group.value_counts().to_dict(),
           "umap_parameters": {k: v.item() if hasattr(v, "item") else v for k, v in a.uns["umap"]["params"].items()},
           "output_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
           "limitations": "Provisional labels; one public library per condition; no independent disease effect test"}
args.output.with_suffix(".source.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
a.file.close()
print(json.dumps(receipt, indent=2))
