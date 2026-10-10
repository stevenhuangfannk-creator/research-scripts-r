"""Download only the two verified zebrafish tutorial inputs, checking frozen SHA256."""
import argparse
import hashlib
import json
import urllib.request
from pathlib import Path

FILES = [
    ("adata_zebrafish_preprocessed.h5ad", "https://drive.google.com/uc?id=1Nzq1F6dGw-nR9lhRLfZdHOG7dcYq7P0i&export=download", 42148628,
     "eccab081c44cfe335b726aec8172bbcda072241b4f006f6420bb5d46d39611cb"),
    ("prior_GRN.csv", "https://drive.google.com/uc?id=1ci_gCwdgGlZ0xSn6gSa_-LlIl9-aDa1c&export=download/", 81355039,
     "356bfde785af53e36f9334c4f5032c06f111d67d30b881b41e24a8ebde7a536a")
]


def digest(path):
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    args.directory.mkdir(parents=True, exist_ok=True)
    for name, url, size, expected in FILES:
        path = args.directory / name
        if path.exists():
            if path.stat().st_size != size or digest(path) != expected:
                raise ValueError(f"Existing file has a different version/checksum: {path}; preserved without overwriting.")
            print(f"Verified cached input: {path}")
            continue
        temporary = path.with_suffix(path.suffix + ".part")
        with urllib.request.urlopen(url, timeout=60) as response, temporary.open("wb") as stream:
            for block in iter(lambda: response.read(1024 * 1024), b""):
                stream.write(block)
        checksum = digest(temporary)
        if temporary.stat().st_size != size or checksum != expected:
            raise ValueError(f"Downloaded input differs from frozen source: {name}; inspect {temporary}.")
        temporary.replace(path)
        path.with_suffix(path.suffix + ".manifest.json").write_text(json.dumps(
            {"source_url": url, "size_bytes": size, "sha256": checksum, "status": "PASS"}, indent=2), encoding="utf-8")
        print(f"Downloaded and verified: {path}")


if __name__ == "__main__":
    main()
