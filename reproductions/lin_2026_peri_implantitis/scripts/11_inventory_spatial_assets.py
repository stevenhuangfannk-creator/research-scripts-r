"""Inventory expected Visium assets from an extracted directory or GEO filelist."""
from __future__ import annotations
import argparse, json, urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GEO_FILELIST = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE206nnn/GSE206621/suppl/filelist.txt"
REQUIRED_SUFFIXES = (
    "_barcodes.tsv.gz", "_features.tsv.gz", "_matrix.mtx.gz",
    "_tissue_positions_list.csv.gz", "_scalefactors_json.json.gz",
    "_tissue_hires_image.png.gz", "_tissue_lowres_image.png.gz",
    "_aligned_fiducials.jpg.gz", "_detected_tissue_image.jpg.gz",
)

def parse_filelist(text: str) -> dict[str, dict[str, dict[str, int | str]]]:
    assets: dict[str, dict[str, dict[str, int | str]]] = {}
    for line in text.splitlines():
        fields = line.split("\t")
        if len(fields) != 5 or fields[0] != "File":
            continue
        name, size, kind = fields[1], int(fields[3]), fields[4]
        sample = name.split("_", 1)[0] + "_" + name.split("_", 2)[1]
        assets.setdefault(sample, {})[name] = {
            "name": name, "size": size, "kind": kind
        }
    return assets

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--filelist", type=Path)
    parser.add_argument("--extracted-root", type=Path)
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "results" / "phase4b" / "spatial_asset_manifest.json")
    args = parser.parse_args()
    if args.filelist:
        text = args.filelist.read_text(encoding="utf-8")
    else:
        request = urllib.request.Request(GEO_FILELIST, headers={"User-Agent": "research-os-reproduction/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            text = response.read().decode("utf-8")
    records = parse_filelist(text)
    output = {"source": "GSE206621 filelist", "samples": {}, "required_assets": list(REQUIRED_SUFFIXES)}
    for sample, files in sorted(records.items()):
        names = {str(v["name"]) for v in files.values()}
        missing = [suffix for suffix in REQUIRED_SUFFIXES if not any(name.endswith(suffix) for name in names)]
        present = []
        if args.extracted_root:
            for path in args.extracted_root.rglob("*"):
                if path.is_file() and sample in path.name:
                    present.append({"path": str(path), "bytes": path.stat().st_size})
            missing_local = [suffix for suffix in REQUIRED_SUFFIXES if not any(str(x["path"]).endswith(suffix[:-3]) or str(x["path"]).endswith(suffix) for x in present)]
        else:
            missing_local = []
        output["samples"][sample] = {"expected_files": sorted(names), "missing_expected_assets": missing, "local_files": present, "missing_local_assets": missing_local}
    output["sample_count"] = len(records)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps({"sample_count": len(records), "output": str(args.output), "samples": sorted(records)}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
