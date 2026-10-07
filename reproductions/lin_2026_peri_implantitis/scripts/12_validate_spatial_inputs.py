"""Validate extracted GSE206621 Visium assets without running biological analysis."""
from __future__ import annotations
import argparse, gzip, json
from pathlib import Path

REQUIRED=("barcodes.tsv.gz","features.tsv.gz","matrix.mtx.gz","tissue_positions_list.csv.gz","scalefactors_json.json.gz","tissue_hires_image.png.gz","tissue_lowres_image.png.gz","aligned_fiducials.jpg.gz","detected_tissue_image.jpg.gz")

def count_gzip_lines(path: Path) -> int:
    with gzip.open(path,"rt",encoding="utf-8") as f: return sum(1 for _ in f)

def matrix_shape(path: Path) -> tuple[int,int,int]:
    with gzip.open(path,"rt",encoding="utf-8") as f:
        for line in f:
            if line.startswith("%"): continue
            a=line.split(); return int(a[0]),int(a[1]),int(a[2])
    raise ValueError(f"no MatrixMarket header: {path}")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("root",type=Path); ap.add_argument("--output",type=Path,default=Path("results/phase4b/spatial_validation.json")); args=ap.parse_args()
    root=args.root; samples={}
    for barcode in sorted(root.rglob("*_barcodes.tsv.gz")):
        stem=barcode.name[:-len("_barcodes.tsv.gz")]; files={suffix: root.rglob(f"{stem}_{suffix}") for suffix in REQUIRED}; files={k:next(iter(v),None) for k,v in files.items()}
        missing=[k for k,v in files.items() if v is None]
        row={"missing":missing,"files":{k:(str(v) if v else None) for k,v in files.items()}}
        if not missing:
            genes=count_gzip_lines(files["features.tsv.gz"]); barcodes=count_gzip_lines(files["barcodes.tsv.gz"]); position_lines=list(gzip.open(files["tissue_positions_list.csv.gz"],"rt",encoding="utf-8")); rows=len(position_lines) - (1 if position_lines and position_lines[0].lower().startswith("barcode") else 0); mrows,mcols,nnz=matrix_shape(files["matrix.mtx.gz"])
            row.update({"features":genes,"barcodes":barcodes,"tissue_positions_rows":rows,"matrix_rows":mrows,"matrix_cols":mcols,"matrix_nnz":nnz,"dimensions_match":genes==mrows and barcodes==mcols,"positions_match_barcodes":rows==barcodes})
        samples[stem]=row
    out={"sample_count":len(samples),"samples":samples}; args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(out,indent=2),encoding="utf-8"); print(json.dumps({"sample_count":len(samples),"output":str(args.output),"all_complete":all(not x["missing"] for x in samples.values())},indent=2))

if __name__=="__main__": main()
