"""Optional non-visual PDF text-size audit; requires PyMuPDF. Run from repo root."""
from pathlib import Path
import json
import pymupdf

root = Path(__file__).resolve().parents[1]
plots = json.loads((root / "registry/plots.yml").read_text(encoding="utf-8"))["plots"]
rows = []
for plot in plots:
    if plot["vector_file"] is None:
        continue
    with pymupdf.open(root / plot["vector_file"]) as doc:
        spans = [span for page in doc for block in page.get_text("dict")["blocks"]
                 if "lines" in block for line in block["lines"] for span in line["spans"]]
    small = [dict(text=span["text"], size=span["size"]) for span in spans if span["size"] < 4.99]
    rows.append(dict(id=plot["id"], min_effective_pt=round(min(s["size"] for s in spans), 2) if spans else None,
                     selectable_text_spans=len(spans), below_minimum=small,
                     status="FAIL" if small or not spans else "PASS"))
(root / "docs/validation/pdf_effective_text.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
print("Checked", len(rows), "PDFs; failures:", sum(row["status"] == "FAIL" for row in rows))
if any(row["status"] == "FAIL" for row in rows):
    raise SystemExit(1)
