"""Download public source archives with streaming checksum verification."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASETS = {
    "pi-scrna": {
        "record": "19697597",
        "filename": "filtered h5 files for peri-implantitis scRNA-seq.zip",
        "md5": "cadde1d9e1d185e5ec5aa52d034959f5",
        "extract_dir": PROJECT_ROOT / "data" / "raw" / "pi_scrna",
    },
}


def digest(path: Path, algorithm: str = "md5") -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def download(url: str, destination: Path) -> None:
    partial = destination.with_suffix(destination.suffix + ".part")
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "research-os-reproduction/1.0"})
    with urllib.request.urlopen(request) as response, partial.open("wb") as target:
        shutil.copyfileobj(response, target, length=1024 * 1024)
    partial.replace(destination)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=sorted(DATASETS), required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    item = DATASETS[args.dataset]
    archive_dir = PROJECT_ROOT / "data" / "downloads"
    archive = archive_dir / item["filename"]
    encoded_name = urllib.parse.quote(item["filename"], safe="")
    url = f"https://zenodo.org/api/records/{item['record']}/files/{encoded_name}/content"

    if archive.exists() and digest(archive) == item["md5"] and not args.force:
        print(f"verified existing archive: {archive}")
    else:
        if archive.exists() and not args.force:
            print("existing archive checksum mismatch; use --force to replace it", file=sys.stderr)
            return 2
        print(f"downloading {url}")
        download(url, archive)
        observed = digest(archive)
        if observed != item["md5"]:
            print(f"MD5 mismatch: expected {item['md5']}, observed {observed}", file=sys.stderr)
            return 3
        print(f"verified MD5: {observed}")

    destination = item["extract_dir"]
    if destination.exists() and any(destination.iterdir()) and not args.force:
        print(f"extraction directory already populated: {destination}")
        return 0
    if args.force and destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(destination)
    print(f"extracted to: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

