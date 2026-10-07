# PI Spatial Zenodo Access Diagnostic

Date: 2026-09-28

## Identifiers

- Concept DOI: `10.5281/zenodo.19697596`
- Resolved record ID: `19697597`
- Record page: `https://zenodo.org/records/19697597`
- API record: `https://zenodo.org/api/records/19697597`
- File name: `space ranger output.zip`
- API file endpoint: `https://zenodo.org/api/records/19697597/files/space%20ranger%20output.zip/content`
- Record file URL: `https://zenodo.org/records/19697597/files/space%20ranger%20output.zip?download=1`
- Expected size: `169698220` bytes
- Expected MD5: `503e0e75aeff315b3f1a14f3cd8d3243`

## Endpoint results in the current diagnostic

The diagnostic used `HEAD` and `GET`, a normal browser-like User-Agent, and a no-redirect opener. All four endpoints returned HTTP `200` in this run:

| Endpoint | HEAD | GET | Result |
|---|---:|---:|---|
| Record page | 200 | 200 | accessible |
| API record | 200 | 200 | accessible; current file metadata readable |
| API file endpoint | 200 | 200 | binary response; `Content-Length: 169698220` |
| Record file URL | 200 | 200 | binary response; `Content-Length: 169698220` |

No redirect was observed in this diagnostic. The API response supplies the current file URL; it was not guessed or replaced with a mirror.

## Earlier 403 interpretation

A previous attempt from the same Windows environment returned HTTP 403 for the binary download endpoint. The current repeat test does not reproduce that 403. This indicates an intermittent access or edge/network condition rather than a consistently expired link. No evidence currently points to required authentication, a private record, or an access-control bypass.

The download completed through resumable official Range requests. The merged archive matched the published byte count and MD5, then was extracted and inventoried.

## Methods attempted

1. Official record page and API record retrieval.
2. Official API file endpoint.
3. Official record file URL with `?download=1`.
4. `HEAD` and `GET` requests with `User-Agent: research-os-reproduction/1.0`.
5. Existing script `scripts/00_download_public_data.py`, which validates size and MD5 before extraction.

No mirror, bypass, token, credential or unofficial source was used.

## Alternative sources if access fails again

- The same official Zenodo record's file endpoint should remain the first retry path.
- Paper supplementary information contains methods but not a replacement spatial archive.
- GEO/SRA may contain related or raw data, but no equivalent PI spatial archive has been confirmed in this project.
- No author code repository or alternate author-hosted spatial archive has been identified.

The PI spatial archive is now available locally and has passed checksum and Space Ranger inventory validation.
