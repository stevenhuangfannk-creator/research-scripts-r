# Phase 4B Input Audit

Date: 2026-09-28

## Public record

The Zenodo record API for `10.5281/zenodo.19697596` resolves the spatial archive as:

- file: `space ranger output.zip`
- expected size: 169,698,220 bytes
- published MD5: `503e0e75aeff315b3f1a14f3cd8d3243`
- record: `https://zenodo.org/records/19697597`

## Access state

**NOT INSPECTED / ACCESS NOT AVAILABLE** for the archive contents in this run. The API metadata was readable, but the binary download endpoint returned HTTP 403 from the current Windows environment. No partial archive was retained and no spatial object was generated.

This is an access limitation, not evidence that the paper's spatial data are absent. The next attempt should use a browser-authenticated or alternate official download route, then verify the expected byte count and MD5 before extraction.

## Downstream gate

Phase 4B remains blocked until the archive is downloaded and its Space Ranger directory structure is inventoried. Do not run cell2location, NMF or spatial figure reconstruction on guessed or incomplete inputs.
