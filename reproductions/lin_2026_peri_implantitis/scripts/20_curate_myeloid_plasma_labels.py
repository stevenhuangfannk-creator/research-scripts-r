"""Versioned, evidence-limited labels for a new cell2location reference."""
from __future__ import annotations

import json
from pathlib import Path

import anndata as ad
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results/phase4b/cell2location_input/scrna_reference_counts_curated_v1.h5ad"
LOCAL = ROOT / "results/phase4a/myeloid_plasma_audit/local_embedding.tsv.gz"
OUT = ROOT / "results/phase4a/myeloid_plasma_audit"


def main() -> None:
    obs = ad.read_h5ad(SOURCE, backed="r").obs.copy()
    local = pd.read_csv(LOCAL, sep="\t", index_col=0)
    assert obs.index.is_unique and local.index.is_unique
    assert local.index.difference(obs.index).empty
    original = obs["major_cell_type"].astype(str)
    cluster = obs["leiden_scvi"].astype(str)
    assert original.loc[cluster.eq("47")].eq("Epithelial cells").all()
    assert int(cluster.eq("47").sum()) == 702

    old_macrophage = original.eq("Macrophages")
    osteoclast_like = original.eq("Monocytes") & cluster.eq("27")
    reviewed_macrophage = pd.Series(False, index=obs.index)
    eligible = local.index[local["audit_leiden"].astype(str).eq("5")]
    reviewed_macrophage.loc[eligible] = True
    reviewed_macrophage &= original.eq("Monocytes") & cluster.eq("25")
    assert (int(old_macrophage.sum()), int(osteoclast_like.sum()), int(reviewed_macrophage.sum())) == (1885, 253, 1417)

    new = original.copy()
    new.loc[old_macrophage | osteoclast_like] = "Unresolved"
    new.loc[reviewed_macrophage] = "Macrophages"
    confidence = obs["annotation_confidence"].astype(str).copy()
    confidence.loc[old_macrophage | osteoclast_like] = "low"
    confidence.loc[reviewed_macrophage] = "curated_marker_review"
    provenance = obs["reference_annotation_source"].astype(str).copy()
    provenance.loc[old_macrophage] = "phase4a_myeloid_plasma_audit_v2_mixed_old_macrophage"
    provenance.loc[osteoclast_like] = "phase4a_myeloid_plasma_audit_v2_osteoclast_like"
    provenance.loc[reviewed_macrophage] = "phase4a_myeloid_plasma_audit_v2_core_macrophage"
    assert new.loc[cluster.eq("47")].eq("Epithelial cells").all()
    assert int(new.eq("Macrophages").sum()) == 1417
    assert int(new.eq("Unresolved").sum()) == 2138
    assert new.loc[~(old_macrophage | osteoclast_like | reviewed_macrophage)].eq(
        original.loc[~(old_macrophage | osteoclast_like | reviewed_macrophage)]
    ).all()

    labels = pd.DataFrame({"major_cell_type": new, "annotation_confidence": confidence,
                           "reference_annotation_source": provenance}, index=obs.index)
    labels.index.name = "cell_id"
    labels.to_csv(OUT / "curated_v2_annotations.tsv.gz", sep="\t", compression="gzip")
    changed = obs.loc[old_macrophage | osteoclast_like | reviewed_macrophage,
                      ["sample_id", "donor_id", "condition", "leiden_scvi"]].copy()
    changed["old_label"] = original.loc[changed.index]
    changed["new_label"] = new.loc[changed.index]
    changed["old_confidence"] = obs.loc[changed.index, "annotation_confidence"].astype(str)
    changed["new_confidence"] = confidence.loc[changed.index]
    changed["decision"] = provenance.loc[changed.index]
    changed.index.name = "cell_id"
    changed.to_csv(OUT / "curated_v2_cell_changes.tsv.gz", sep="\t", compression="gzip")
    changed.groupby(["decision", "old_label", "new_label", "leiden_scvi", "sample_id"],
                    observed=True).size().rename("cells").reset_index().to_csv(
        OUT / "curated_v2_change_by_cluster_sample.tsv", sep="\t", index=False)
    summary = {
        "classification": "USER/CODEX ANALYTICAL CHOICE; not author annotation",
        "source": str(SOURCE.relative_to(ROOT)),
        "prior_macrophage_to_unresolved": int(old_macrophage.sum()),
        "osteoclast_like_monocytes_to_unresolved": int(osteoclast_like.sum()),
        "cluster25_local5_monocytes_to_macrophage": int(reviewed_macrophage.sum()),
        "total_unresolved_excluded_from_fit": int(new.eq("Unresolved").sum()),
        "cells_retained_for_fit": int(new.ne("Unresolved").sum()),
        "reference_cell_types_after_exclusion": int(new.loc[new.ne("Unresolved")].nunique()),
        "leiden47_epithelial_correction_preserved": True,
        "original_data_modified": False,
        "rationale": {
            "old_macrophage": "Multiple inconsistent fibroblast/plasma/melanocyte/epithelial/osteoclast-like signatures; no defensible single label",
            "cluster27": "CTSK/ACP5/MMP9 osteoclast-like; preliminary low-confidence monocyte label",
            "cluster25_local5": "C1QA/B/C, CD68, LST1, TYROBP, FCER1G, CTSS, MS4A7, CCL18; low Ig and SOLO scores; multiple PI samples",
        },
    }
    (OUT / "curated_v2_annotation_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
