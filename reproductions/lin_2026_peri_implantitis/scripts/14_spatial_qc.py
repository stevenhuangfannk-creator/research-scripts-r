"""Run non-destructive spatial QC for PI and healthy Visium inputs."""
from __future__ import annotations

import gzip
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
from PIL import Image
from scipy.io import mmread


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "phase4b" / "qc"
FIG = ROOT / "figures" / "phase4b" / "qc"

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 8,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "legend.frameon": False,
    }
)


def positions(path: Path, compressed: bool = False) -> pd.DataFrame:
    opener = gzip.open if compressed else open
    with opener(path, "rt", encoding="utf-8") as handle:
        first = handle.readline().strip().split(",")
    header = 0 if first[0].lower() == "barcode" else None
    frame = pd.read_csv(path, header=header, compression="gzip" if compressed else None)
    if header is None:
        frame.columns = ["barcode", "in_tissue", "array_row", "array_col", "pxl_row", "pxl_col"]
    frame["barcode"] = frame["barcode"].astype(str)
    return frame.set_index("barcode")


def load_image(path: Path, compressed: bool = False) -> np.ndarray:
    if compressed:
        with gzip.open(path, "rb") as handle:
            return np.asarray(Image.open(handle).convert("RGB"))
    return np.asarray(Image.open(path).convert("RGB"))


def qc_vectors(matrix) -> tuple[np.ndarray, np.ndarray]:
    counts = np.asarray(matrix.sum(axis=1)).ravel()
    genes = np.asarray((matrix > 0).sum(axis=1)).ravel()
    return counts, genes


def plot_spatial(sample: str, image: np.ndarray, pos: pd.DataFrame, scale: float, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    ax.imshow(image)
    tissue = pos["in_tissue"].astype(int).eq(1)
    ax.scatter(pos.loc[~tissue, "pxl_col"] * scale, pos.loc[~tissue, "pxl_row"] * scale,
               s=2, c="#8f99a6", alpha=0.25, linewidths=0, label="Non-tissue")
    ax.scatter(pos.loc[tissue, "pxl_col"] * scale, pos.loc[tissue, "pxl_row"] * scale,
               s=4, c="#c4473d", alpha=0.75, linewidths=0, label="Tissue")
    ax.set_title(sample)
    ax.set_axis_off()
    ax.legend(loc="upper right", markerscale=2.5)
    fig.savefig(path.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def summarize(sample: str, condition: str, matrix, barcodes: list[str], pos: pd.DataFrame,
              image: np.ndarray, scale: float) -> tuple[dict, pd.DataFrame]:
    counts, genes = qc_vectors(matrix)
    qc = pd.DataFrame({"barcode": barcodes, "total_counts": counts, "n_genes": genes}).set_index("barcode")
    joined = pos.join(qc, how="left")
    tissue = joined["in_tissue"].astype(int).eq(1)
    scaled_x = joined["pxl_col"] * scale
    scaled_y = joined["pxl_row"] * scale
    image_match = bool(scaled_x.between(0, image.shape[1]).all() and scaled_y.between(0, image.shape[0]).all())
    barcode_match = int(joined["total_counts"].notna().sum())
    tissue_qc = joined.loc[tissue & joined["total_counts"].notna()]
    row = {
        "sample": sample,
        "condition": condition,
        "matrix_spots": len(barcodes),
        "position_spots": len(pos),
        "tissue_spots": int(tissue.sum()),
        "matrix_position_overlap": barcode_match,
        "median_umi_tissue": float(tissue_qc["total_counts"].median()),
        "median_genes_tissue": float(tissue_qc["n_genes"].median()),
        "zero_count_spots": int((qc["total_counts"] == 0).sum()),
        "image_height": int(image.shape[0]),
        "image_width": int(image.shape[1]),
        "scale_factor": float(scale),
        "coordinates_within_image": image_match,
        "complete_barcode_mapping": barcode_match == len(pos),
    }
    joined["sample"] = sample
    joined["condition"] = condition
    joined["is_tissue"] = tissue
    return row, joined.reset_index()


def load_pi() -> tuple[dict, pd.DataFrame, np.ndarray, pd.DataFrame, float]:
    base = ROOT / "data" / "raw" / "pi_spatial" / "space ranger output"
    raw = sc.read_10x_h5(base / "raw_feature_bc_matrix.h5")
    pos = positions(base / "spatial" / "tissue_positions_list.csv")
    scale_data = json.loads((base / "spatial" / "scalefactors_json.json").read_text(encoding="utf-8"))
    image = load_image(base / "spatial" / "tissue_hires_image.png")
    row, spots = summarize("PI_spatial", "PI", raw.X, raw.obs_names.astype(str).tolist(), pos, image,
                           scale_data["tissue_hires_scalef"])
    filtered = sc.read_10x_h5(base / "filtered_feature_bc_matrix.h5")
    row["filtered_spots"] = int(filtered.n_obs)
    row["filtered_position_overlap"] = int(filtered.obs_names.isin(pos.index).sum())
    return row, spots, image, pos, scale_data["tissue_hires_scalef"]


def load_healthy(prefix: str) -> tuple[dict, pd.DataFrame, np.ndarray, pd.DataFrame, float]:
    base = ROOT / "data" / "raw" / "gse206621_healthy_spatial"
    matrix = mmread(base / f"{prefix}_matrix.mtx.gz").tocsr().T
    with gzip.open(base / f"{prefix}_barcodes.tsv.gz", "rt", encoding="utf-8") as handle:
        barcodes = [line.strip() for line in handle if line.strip()]
    pos = positions(base / f"{prefix}_tissue_positions_list.csv.gz", compressed=True)
    scale_data = json.loads(gzip.open(base / f"{prefix}_scalefactors_json.json.gz", "rt", encoding="utf-8").read())
    image = load_image(base / f"{prefix}_tissue_hires_image.png.gz", compressed=True)
    row, spots = summarize(prefix, "HG", matrix, barcodes, pos, image, scale_data["tissue_hires_scalef"])
    return row, spots, image, pos, scale_data["tissue_hires_scalef"]


def summary_figure(spots: pd.DataFrame, summary: pd.DataFrame) -> None:
    tissue = spots.loc[spots["is_tissue"] & spots["total_counts"].notna()].copy()
    order = summary["sample"].tolist()
    fig, axes = plt.subplots(2, 1, figsize=(8.0, 5.8), sharex=True)
    for ax, column, label in zip(axes, ["total_counts", "n_genes"], ["Total counts / UMI", "Detected genes"]):
        values = [tissue.loc[(tissue["sample"] == sample) & (tissue[column] > 0), column].to_numpy()
                  for sample in order]
        parts = ax.violinplot(values, showmedians=True, showextrema=False)
        for body in parts["bodies"]:
            body.set_facecolor("#6b88a7"); body.set_alpha(0.7); body.set_edgecolor("none")
        parts["cmedians"].set_color("#9f2f2f")
        ax.set_ylabel(label)
        ax.set_yscale("log")
        ax.grid(axis="y", alpha=0.18)
    axes[-1].set_xticks(range(1, len(order) + 1), order, rotation=45, ha="right",
                       rotation_mode="anchor")
    fig.suptitle("Spatial QC distributions (tissue spots; no filtering applied)")
    fig.tight_layout()
    path = FIG / "spatial_qc_distributions"
    fig.savefig(path.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    rows, spot_frames = [], []
    row, spots, image, pos, scale = load_pi()
    rows.append(row); spot_frames.append(spots)
    plot_spatial("PI_spatial", image, pos, scale, FIG / "PI_spatial_tissue_coverage")
    healthy = ["GSM6258251_A1", "GSM6258252_B1", "GSM6258253_C1", "GSM6258254_D1",
               "GSM6258255_A2", "GSM6258256_B2", "GSM6258257_C2", "GSM6258258_D2"]
    for sample in healthy:
        row, spots, image, pos, scale = load_healthy(sample)
        rows.append(row); spot_frames.append(spots)
        plot_spatial(sample, image, pos, scale, FIG / f"{sample}_tissue_coverage")
    summary = pd.DataFrame(rows)
    all_spots = pd.concat(spot_frames, ignore_index=True)
    summary.to_csv(OUT / "spatial_qc_summary.tsv", sep="\t", index=False)
    all_spots.to_csv(OUT / "spatial_spot_qc.tsv.gz", sep="\t", index=False, compression="gzip")
    summary_figure(all_spots, summary)
    audit = {
        "classification": "EXACTLY REPRODUCED STEP for released inputs; USER/CODEX analytical QC summary",
        "filtering_applied": False,
        "samples": len(summary),
        "all_coordinate_maps_valid": bool(summary["coordinates_within_image"].all()),
        "all_barcode_maps_complete": bool(summary["complete_barcode_mapping"].all()),
    }
    (OUT / "spatial_qc_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(summary.to_string(index=False))
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
