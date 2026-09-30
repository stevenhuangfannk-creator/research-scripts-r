"""Make a documented Phase 4B reference-label correction without changing 4A/4B-2 inputs."""
from __future__ import annotations

import json
from pathlib import Path

import anndata as ad
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results/phase4b/cell2location_input/scrna_reference_counts.h5ad"
TARGET = ROOT / "results/phase4b/cell2location_input/scrna_reference_counts_curated_v1.h5ad"
AUDIT = ROOT / "results/phase4b/cell2location_input/curated_v1_annotation_audit.json"


def main() -> None:
    if TARGET.exists():
        raise FileExistsError(f"Curated reference already exists: {TARGET}")
    adata = ad.read_h5ad(SOURCE)
    cluster = adata.obs["leiden_scvi"].astype(str).eq("47")
    assert int(cluster.sum()) == 702
    assert adata.obs.loc[cluster, "major_cell_type"].astype(str).eq("Neutrophils").all()
    before = adata.obs["major_cell_type"].astype(str).value_counts().to_dict()
    labels = adata.obs["major_cell_type"].astype(str)
    labels.loc[cluster] = "Epithelial cells"
    adata.obs["major_cell_type"] = pd.Categorical(labels)
    confidence = adata.obs["annotation_confidence"].astype(str)
    confidence.loc[cluster] = "curated_marker_review"
    adata.obs["annotation_confidence"] = pd.Categorical(confidence)
    adata.obs["reference_annotation_source"] = pd.Categorical(
        ["cluster_47_marker_review" if value else "phase4a_preliminary" for value in cluster]
    )
    after = adata.obs["major_cell_type"].astype(str).value_counts().to_dict()
    assert after["Neutrophils"] == 270
    assert after["Epithelial cells"] == before["Epithelial cells"] + 702
    assert adata.obs["annotation_confidence"].astype(str).eq("low").sum() == 2080
    adata.write_h5ad(TARGET, compression="gzip")
    audit = {
        "source": str(SOURCE.relative_to(ROOT)),
        "target": str(TARGET.relative_to(ROOT)),
        "rule": "Leiden 47: Neutrophils -> Epithelial cells",
        "classification": "USER/CODEX ANALYTICAL CHOICE based on marker review",
        "changed_cells": 702,
        "unchanged_cells": int(adata.n_obs - 702),
        "unchanged_low_confidence_cells": 2080,
        "evidence": {
            "positive": ["FDCSP", "KRT13", "SPRR2A", "SPRR3", "TACSTD2", "RHCG", "ODAM"],
            "negative": ["PTPRC", "FCGR3B", "CSF3R"],
            "note": "S100A8/S100A9 drove the preliminary neutrophil marker score but are not specific here.",
        },
        "before_counts": before,
        "after_counts": after,
    }
    AUDIT.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
