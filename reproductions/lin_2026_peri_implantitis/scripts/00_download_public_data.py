"""Download public source archives with streaming checksum verification."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import math
import shutil
import sys
import tarfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PI_SCRNA = {
    "record": "19697597",
    "filename": "filtered h5 files for peri-implantitis scRNA-seq.zip",
    "bytes": 175825893,
    "md5": "cadde1d9e1d185e5ec5aa52d034959f5",
    "extract_dir": PROJECT_ROOT / "data" / "raw" / "pi_scrna",
}
GEO_SUPPLEMENT_ROOT = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE164nnn/GSE164241/suppl"
GEO_SPATIAL_ROOT = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE206nnn/GSE206621/suppl"
PI_SPATIAL = {"record": "19697597", "filename": "space ranger output.zip", "bytes": 169698220, "md5": "503e0e75aeff315b3f1a14f3cd8d3243"}
HEALTHY_SPATIAL = {"filename": "GSE206621_RAW.tar", "bytes": 133652480}


def digest(path: Path, algorithm: str = "md5") -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def download(url: str, destination: Path, expected_bytes: int) -> Path:
    partial = destination.with_suffix(destination.suffix + ".part")
    destination.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, 6):
        received = partial.stat().st_size if partial.exists() else 0
        headers = {"User-Agent": "research-os-reproduction/1.0"}
        if received:
            headers["Range"] = f"bytes={received}-"
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=60) as response:
            status = getattr(response, "status", None)
            append = received > 0 and status == 206
            mode = "ab" if append else "wb"
            with partial.open(mode) as target:
                shutil.copyfileobj(response, target, length=1024 * 1024)
        received = partial.stat().st_size
        print(f"download attempt {attempt}: {received}/{expected_bytes} bytes")
        if received == expected_bytes:
            return partial
        if received > expected_bytes:
            raise RuntimeError(f"download exceeds expected size: {received} > {expected_bytes}")
    raise RuntimeError(f"incomplete download after 5 attempts: {received}/{expected_bytes} bytes")


def download_parallel_ranges(url: str, destination: Path, expected_bytes: int, workers: int = 4) -> Path:
    partial = destination.with_suffix(destination.suffix + ".part")
    destination.parent.mkdir(parents=True, exist_ok=True)
    existing = partial.stat().st_size if partial.exists() else 0
    if existing == expected_bytes:
        return partial
    if existing > expected_bytes:
        raise RuntimeError(f"partial download exceeds expected size: {existing} > {expected_bytes}")

    remaining = expected_bytes - existing
    chunk_size = math.ceil(remaining / workers)
    ranges = []
    for index in range(workers):
        start = existing + index * chunk_size
        end = min(expected_bytes - 1, start + chunk_size - 1)
        if start <= end:
            ranges.append((index, start, end, partial.with_suffix(partial.suffix + f".chunk{index}")))

    def fetch_range(item: tuple[int, int, int, Path]) -> tuple[int, Path]:
        index, start, end, chunk_path = item
        expected_chunk = end - start + 1
        for attempt in range(1, 9):
            have = chunk_path.stat().st_size if chunk_path.exists() else 0
            if have == expected_chunk:
                return index, chunk_path
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "research-os-reproduction/1.0",
                    "Range": f"bytes={start + have}-{end}",
                },
            )
            with urllib.request.urlopen(request, timeout=60) as response:
                if getattr(response, "status", None) != 206:
                    raise RuntimeError(f"server did not honor byte range {start + have}-{end}")
                with chunk_path.open("ab") as target:
                    shutil.copyfileobj(response, target, length=1024 * 1024)
            have = chunk_path.stat().st_size
            print(f"range {index} attempt {attempt}: {have}/{expected_chunk} bytes")
            if have > expected_chunk:
                raise RuntimeError(f"range {index} exceeds expected size")
        raise RuntimeError(f"range {index} incomplete after 8 attempts")

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        completed = sorted(executor.map(fetch_range, ranges))
    with partial.open("ab") as target:
        for _, chunk_path in completed:
            with chunk_path.open("rb") as source:
                shutil.copyfileobj(source, target, length=1024 * 1024)
            chunk_path.unlink()
    if partial.stat().st_size != expected_bytes:
        raise RuntimeError(f"combined download size mismatch: {partial.stat().st_size}/{expected_bytes}")
    return partial


def acquire_pi_scrna(force: bool) -> int:
    item = PI_SCRNA
    archive_dir = PROJECT_ROOT / "data" / "downloads"
    archive = archive_dir / item["filename"]
    encoded_name = urllib.parse.quote(item["filename"], safe="")
    url = f"https://zenodo.org/api/records/{item['record']}/files/{encoded_name}/content"

    if archive.exists() and digest(archive) == item["md5"] and not force:
        print(f"verified existing archive: {archive}")
    else:
        if archive.exists() and not force:
            print("existing archive checksum mismatch; use --force to replace it", file=sys.stderr)
            return 2
        partial = archive.with_suffix(archive.suffix + ".part")
        if archive.exists() and archive.stat().st_size < item["bytes"]:
            archive.replace(partial)
            print(f"resuming incomplete archive at {partial.stat().st_size} bytes")
        elif archive.exists():
            archive.unlink()
        print(f"downloading {url}")
        partial = download(url, archive, item["bytes"])
        observed = digest(partial)
        if observed != item["md5"]:
            print(f"MD5 mismatch: expected {item['md5']}, observed {observed}", file=sys.stderr)
            return 3
        partial.replace(archive)
        print(f"verified MD5: {observed}")

    destination = item["extract_dir"]
    if destination.exists() and any(destination.iterdir()) and not force:
        print(f"extraction directory already populated: {destination}")
        return 0
    if force and destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(destination)
    print(f"extracted to: {destination}")
    return 0


def acquire_healthy_scrna(force: bool) -> int:
    filelist_url = f"{GEO_SUPPLEMENT_ROOT}/filelist.txt"
    request = urllib.request.Request(filelist_url, headers={"User-Agent": "research-os-reproduction/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        filelist = response.read().decode("utf-8")
    raw_root = PROJECT_ROOT / "data" / "raw" / "gse164241_healthy_gingiva"
    raw_root.mkdir(parents=True, exist_ok=True)
    (raw_root / "filelist.txt").write_text(filelist, encoding="utf-8")

    records: list[tuple[str, int]] = []
    for line in filelist.splitlines():
        fields = line.split("\t")
        if len(fields) == 5 and fields[0] == "File" and "_GM" in fields[1]:
            records.append((fields[1], int(fields[3])))
    if len(records) != 39:
        raise RuntimeError(f"expected 39 files for 13 healthy gingiva samples, found {len(records)}")

    archive = PROJECT_ROOT / "data" / "downloads" / "GSE164241_RAW.tar"
    archive_bytes = 796436480
    if not (archive.exists() and archive.stat().st_size == archive_bytes):
        if archive.exists() and not force:
            raise RuntimeError(f"size mismatch for {archive}; use --force to replace or resume")
        partial = archive.with_suffix(archive.suffix + ".part")
        if archive.exists() and archive.stat().st_size < archive_bytes:
            archive.replace(partial)
        elif archive.exists():
            archive.unlink()
        print("downloading GSE164241_RAW.tar")
        partial = download_parallel_ranges(
            f"{GEO_SUPPLEMENT_ROOT}/GSE164241_RAW.tar", archive, archive_bytes
        )
        partial.replace(archive)
    print(f"verified archive size: {archive.stat().st_size} bytes")

    expected = dict(records)
    extracted = 0
    with tarfile.open(archive, mode="r") as bundle:
        members = {Path(member.name).name: member for member in bundle.getmembers() if member.isfile()}
        missing = sorted(set(expected) - set(members))
        if missing:
            raise RuntimeError(f"healthy gingiva files missing from archive: {missing}")
        for filename, expected_bytes in records:
            sample_id = filename.rsplit("_", 1)[0]
            destination = raw_root / sample_id / filename
            if destination.exists() and destination.stat().st_size == expected_bytes and not force:
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            stale_partial = destination.with_suffix(destination.suffix + ".part")
            if stale_partial.exists():
                stale_partial.unlink()
            source = bundle.extractfile(members[filename])
            if source is None:
                raise RuntimeError(f"cannot extract {filename}")
            with source, destination.open("wb") as target:
                shutil.copyfileobj(source, target, length=1024 * 1024)
            if destination.stat().st_size != expected_bytes:
                raise RuntimeError(f"size mismatch after extracting {filename}")
            extracted += 1
    print(f"healthy gingiva acquisition complete: {len(records)} files, {extracted} extracted")
    return 0



def acquire_pi_spatial(force: bool) -> int:
    item = PI_SPATIAL
    archive_dir = PROJECT_ROOT / "data" / "downloads"
    archive = archive_dir / item["filename"]
    encoded_name = urllib.parse.quote(item["filename"], safe="")
    url = f"https://zenodo.org/api/records/{item['record']}/files/{encoded_name}/content"
    if archive.exists() and digest(archive) == item["md5"] and not force:
        print(f"verified existing archive: {archive}")
        return 0
    if archive.exists() and not force:
        raise RuntimeError("existing PI spatial archive is incomplete or has the wrong MD5; use --force")
    partial = archive.with_suffix(archive.suffix + ".part")
    print(f"downloading {url}")
    partial = download(url, archive, item["bytes"])
    observed = digest(partial)
    if observed != item["md5"]:
        raise RuntimeError(f"MD5 mismatch: expected {item['md5']}, observed {observed}")
    partial.replace(archive)
    print(f"verified MD5: {observed}")
    destination = PROJECT_ROOT / "data" / "raw" / "pi_spatial"
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(destination)
    print(f"extracted to: {destination}")
    return 0


def acquire_healthy_spatial(force: bool) -> int:
    item = HEALTHY_SPATIAL
    archive = PROJECT_ROOT / "data" / "downloads" / item["filename"]
    filelist_url = f"{GEO_SPATIAL_ROOT}/filelist.txt"
    request = urllib.request.Request(filelist_url, headers={"User-Agent": "research-os-reproduction/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        filelist = response.read().decode("utf-8")
    raw_root = PROJECT_ROOT / "data" / "raw" / "gse206621_healthy_spatial"
    raw_root.mkdir(parents=True, exist_ok=True)
    (raw_root / "filelist.txt").write_text(filelist, encoding="utf-8")
    if archive.exists() and archive.stat().st_size == item["bytes"] and not force:
        print(f"verified archive size: {archive.stat().st_size} bytes")
    else:
        if archive.exists() and not force:
            raise RuntimeError("existing healthy spatial archive has the wrong size; use --force")
        print(f"downloading {GEO_SPATIAL_ROOT}/{item['filename']}")
        partial = download_parallel_ranges(f"{GEO_SPATIAL_ROOT}/{item['filename']}", archive, item["bytes"])
        partial.replace(archive)
    with tarfile.open(archive, mode="r") as bundle:
        bundle.extractall(raw_root)
    print(f"extracted to: {raw_root}")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=("pi-scrna", "healthy-scrna", "pi-spatial", "healthy-spatial"), required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.dataset == "pi-scrna":
        return acquire_pi_scrna(args.force)
    if args.dataset == "healthy-scrna":
        return acquire_healthy_scrna(args.force)
    if args.dataset == "pi-spatial":
        return acquire_pi_spatial(args.force)
    return acquire_healthy_spatial(args.force)


if __name__ == "__main__":
    raise SystemExit(main())

