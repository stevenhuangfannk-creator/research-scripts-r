"""Independently map one spatial sample with the audited curated-v2 reference."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import platform
import time
from importlib.metadata import version
from pathlib import Path

import anndata as ad
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scvi
import torch
from cell2location.models import Cell2location

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results/phase4b/cell2location_input/curated_v2"
REF = ROOT / "results/phase4b/cell2location_reference/curated_v2"
REFERENCE_COMMIT = "8496f3a4ea4c75eb35b269995e9e3a6e91f12925"
REFERENCE_SHA256 = "9b244c33c045f47f2b9f5d63dee4a982eedcd6d150655b3684cfad23b39cb148"
HEALTHY = ["GSM6258251_A1", "GSM6258252_B1", "GSM6258253_C1", "GSM6258254_D1",
           "GSM6258255_A2", "GSM6258256_B2", "GSM6258257_C2", "GSM6258258_D2"]
SAMPLES = ["PI_spatial", *HEALTHY]
SEED = 20260928
mpl.rcParams.update({"font.family": "sans-serif", "font.size": 7,
                     "pdf.fonttype": 42, "svg.fonttype": "none"})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_sample(sample: str) -> ad.AnnData:
    a = ad.read_h5ad(INPUT / f"{sample}.h5ad")
    qc = pd.read_csv(ROOT / "results/phase4b/qc/spatial_spot_qc.tsv.gz", sep="\t")
    pos = qc.loc[qc["sample"].eq(sample)].set_index("barcode")
    assert a.obs_names.is_unique and pos.index.is_unique
    assert a.obs_names.isin(pos.index).all()
    pos = pos.loc[a.obs_names]
    for col in ["in_tissue", "array_row", "array_col", "pxl_row", "pxl_col"]:
        if col in a.obs:
            assert np.array_equal(a.obs[col].to_numpy(), pos[col].to_numpy())
        a.obs[col] = pos[col].to_numpy()
    a.obs["original_total_counts"] = pos["total_counts"].to_numpy()
    a.obs["original_detected_genes"] = pos["n_genes"].to_numpy()
    a.obs["shared_gene_counts"] = np.asarray(a.X.sum(axis=1)).ravel()
    a.obs["shared_detected_genes"] = np.asarray((a.X > 0).sum(axis=1)).ravel()
    a.obs["batch"] = sample
    a.obs["depth_group"] = "PI" if sample == "PI_spatial" else ("healthy_1" if sample.endswith("1") else "healthy_2")
    a.obs["data_source"] = "Zenodo PI Space Ranger" if sample == "PI_spatial" else "GSE206621 healthy gingiva"
    a.obsm["spatial"] = a.obs[["pxl_col", "pxl_row"]].to_numpy()
    if sample == "PI_spatial":
        spatial = ROOT / "data/raw/pi_spatial/space ranger output/spatial"
        scale = json.loads((spatial / "scalefactors_json.json").read_text())
        image_path = spatial / "tissue_hires_image.png"
    else:
        spatial = ROOT / "data/raw/gse206621_healthy_spatial"
        with gzip.open(spatial / f"{sample}_scalefactors_json.json.gz", "rt") as stream:
            scale = json.load(stream)
        image_path = spatial / f"{sample}_tissue_hires_image.png.gz"
    a.uns["spatial_provenance"] = {"scalefactors": scale, "image_path": str(image_path.relative_to(ROOT))}
    assert a.obs["in_tissue"].eq(1).all()
    assert a.obs["sample_id"].astype(str).eq(sample).all()
    assert a.obs["original_total_counts"].gt(0).all()
    return a


def preflight(signatures: pd.DataFrame) -> dict:
    ref = ad.read_h5ad(INPUT / "scrna_reference_counts.h5ad", backed="r")
    qc = json.loads((REF / "reference_qc_summary.json").read_text())
    trained = json.loads((REF / "reference_model_summary.json").read_text())
    assert trained["cells"] == 89974 and trained["cell_types"] == 14
    assert sha256(REF / "reference_signatures.tsv.gz") == REFERENCE_SHA256
    assert qc["automatic_gate_pass"] and ref.shape == (89974, 17211)
    assert signatures.index.equals(ref.var_names) and signatures.shape == (17211, 14)
    assert signatures.index.is_unique and signatures.columns.is_unique
    assert "Unresolved" not in signatures.columns
    assert np.isfinite(signatures.to_numpy()).all() and (signatures.to_numpy() >= 0).all()
    rows = []
    for sample in SAMPLES:
        a = load_sample(sample)
        assert a.var_names.equals(signatures.index) and a.var_names.is_unique
        assert a.layers["counts"].shape == a.shape
        assert (a.X != a.layers["counts"]).nnz == 0
        assert np.isfinite(a.X.data).all() and (a.X.data >= 0).all()
        assert np.allclose(a.X.data, np.round(a.X.data))
        rows.append({"sample_id": sample, "condition": str(a.obs["condition"].iloc[0]),
                     "depth_group": str(a.obs["depth_group"].iloc[0]), "spots": a.n_obs,
                     "genes": a.n_vars, "median_original_counts": float(a.obs["original_total_counts"].median()),
                     "gene_order_verified": True, "coordinates_verified": True,
                     "input_sha256": sha256(INPUT / f"{sample}.h5ad")})
    ref.file.close()
    return {"reference_commit": REFERENCE_COMMIT, "reference_signature_sha256": sha256(REF / "reference_signatures.tsv.gz"),
            "reference_cells": 89974, "reference_types": 14, "unresolved_is_mapping_type": False,
            "reference_qc_pass": True,
            "upstream_duplicate_symbol_exclusions": json.loads((INPUT / "duplicate_gene_summary.json").read_text()),
            "samples": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", choices=SAMPLES, default="PI_spatial")
    parser.add_argument("--epochs", type=int, default=30000)
    parser.add_argument("--posterior-samples", type=int, default=1000)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--posterior-only", action="store_true")
    args = parser.parse_args()
    key = "pi" if args.sample == "PI_spatial" else args.sample
    if args.smoke:
        key = f"smoke/{key}"
    out = ROOT / "results/phase4b/cell2location_mapping" / key
    model_path = ROOT / "models/phase4b/cell2location_mapping" / key
    fig = ROOT / "figures/phase4b/cell2location" / key
    for path in [out, model_path.parent, fig]:
        path.mkdir(parents=True, exist_ok=True)
    signatures = pd.read_csv(REF / "reference_signatures.tsv.gz", sep="\t", index_col=0)
    audit = preflight(signatures)
    (out / "input_preflight.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    if args.preflight_only:
        print(json.dumps(audit, indent=2)); return
    if args.sample != "PI_spatial":
        pi_qc = json.loads((ROOT / "results/phase4b/cell2location_mapping/pi/mapping_qc_summary.json").read_text())
        if not pi_qc["automatic_gate_pass"]:
            raise RuntimeError("PI mapping QC failed; Healthy mapping is blocked")
    if not torch.cuda.is_available():
        raise RuntimeError("Previously validated GPU is unavailable; stop for diagnosis")
    scvi.settings.seed = SEED
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)
    torch.set_num_threads(8)
    a = load_sample(args.sample)
    Cell2location.setup_anndata(a, layer="counts", batch_key="sample_id")
    if args.posterior_only:
        model = Cell2location.load(model_path, adata=a, accelerator="gpu")
        elapsed = None
        history = pd.read_csv(out / "training_history.tsv", sep="\t", index_col=0)
    else:
        model = Cell2location(a, cell_state_df=signatures, N_cells_per_location=30, detection_alpha=20)
        started = time.time()
        model.train(max_epochs=args.epochs, batch_size=None, train_size=1, lr=0.002,
                    accelerator="gpu", device="auto", enable_checkpointing=False)
        elapsed = time.time() - started
        model.save(model_path, overwrite=True)
        history = pd.DataFrame({key: np.asarray(value).ravel() for key, value in model.history.items()})
        history.to_csv(out / "training_history.tsv", sep="\t")
    a = model.export_posterior(a, sample_kwargs={"num_samples": args.posterior_samples,
                              "batch_size": 128, "accelerator": "gpu", "device": "auto"})
    assert np.array_equal(a.uns["mod"]["factor_names"], signatures.columns.to_numpy())
    for stat in ["means", "stds", "q05", "q95"]:
        matrix = a.obsm[f"{stat}_cell_abundance_w_sf"]
        frame = pd.DataFrame(np.asarray(matrix), index=a.obs_names, columns=signatures.columns)
        frame.to_csv(out / f"abundance_{stat}.tsv.gz", sep="\t", compression="gzip")
        a.obsm[f"{stat}_cell_abundance_w_sf"] = frame.to_numpy()
    a.uns["mapping_reference"] = {"commit": REFERENCE_COMMIT, "signature_sha256": audit["reference_signature_sha256"],
                                 "factor_names": signatures.columns.to_numpy()}
    a.write_h5ad(out / "posterior.h5ad", compression="gzip")
    a.obs.to_csv(out / "spot_metadata.tsv.gz", sep="\t", compression="gzip")
    loss_key = next(c for c in history if "elbo" in c.lower())
    loss = history[loss_key].to_numpy(float)
    figure, ax = plt.subplots(figsize=(4.5, 3))
    ax.plot(np.arange(1, len(loss)+1), loss, linewidth=1)
    ax.set(xlabel="Epoch", ylabel="ELBO loss", title=f"Mapping convergence: {args.sample}")
    figure.tight_layout()
    figure.savefig(fig / "training_loss.png", dpi=300)
    figure.savefig(fig / "training_loss.pdf")
    figure.savefig(fig / "training_loss.svg")
    plt.close(figure)
    summary = {"sample_id": args.sample, "reference_commit": REFERENCE_COMMIT,
               "reference_signature_sha256": audit["reference_signature_sha256"], "seed": SEED,
               "epochs": len(loss), "smoke": args.smoke, "N_cells_per_location": 30, "detection_alpha": 20,
               "prior_provenance": "USER/CODEX analytical choice; 30 cells/spot prior unverified by nuclei counts; tutorial detection_alpha=20",
               "batch_size": "full sample", "posterior_samples": args.posterior_samples,
               "elapsed_seconds": elapsed, "python": platform.python_version(), "torch": torch.__version__,
               "scvi_tools": version("scvi-tools"), "cell2location": version("cell2location"),
               "gpu": torch.cuda.get_device_name(0), "initial_loss": float(loss[0]), "final_loss": float(loss[-1]),
               "tail_relative_slope": float(np.polyfit(np.arange(min(1000,len(loss))),loss[-1000:],1)[0]/np.median(loss[-1000:])) if len(loss)>1 else None,
               "spots": a.n_obs, "genes": a.n_vars, "cell_types": len(signatures.columns)}
    (out / "mapping_model_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
