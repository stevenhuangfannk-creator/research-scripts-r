# Validation Record

## 2026-09-28 environment preflight

Command:

```powershell
& 'C:\Program Files\R\R-4.3.1\bin\Rscript.exe' scripts\00_environment_check.R
```

Result: exit code `2`, meaning at least one core package could not be loaded.

| Check | Observed result | Status |
|---|---|---|
| R executable | R 4.3.1 (ucrt), Windows 11 x64 | reproduced |
| Core namespaces | 5 of 7 loaded | not reproduced |
| Seurat 5.2.1 | Failed: `Matrix` 1.5-4.1 is loaded but >= 1.6.4 is required | not reproduced |
| reshape2 1.4.4 | Failed: dependency `plyr` is absent | not reproduced |
| Upstream source snapshot | SHA-256 matched the values in `source/SOURCE.md` | reproduced |
| GSE164241 data | Not downloaded | not tested |
| Figure S1A-C QC family | No scientific output generated | not tested |

The full package matrix is in `environment/package_status.tsv`; the runtime record is in `environment/sessionInfo.txt`.

During R startup, locale-setting warnings were emitted for `C.UTF-8`. They did not prevent the preflight from writing its reports, but they should be checked when the isolated environment is created.

No package was installed or updated. No data, figure or result was fabricated to bypass the failure.

## 2026-09-28 Phase 3 shared-workflow rerun

The promoted namespace preflight was run with this reproduction's `environment/packages.tsv`. It checked 33 declared packages and returned exit code `2`; 5 of 7 required packages loaded. The same shared script was then run in the GSE255834 project with a different manifest.

This confirms that the checker transfers across package sets. It does not change the reproduction status: GSE164241 remains unavailable locally and Figure S1A-C remains not tested.
