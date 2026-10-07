# Registry contract

All registries are UTF-8 YAML 1.2 (JSON syntax is also used). IDs are stable and unique.
`status` is method/asset maturity: CANDIDATE, VALIDATED, RECOMMENDED, DEFAULT,
EXPERIMENTAL, DEPRECATED. `validation.status` is independent execution evidence:
PASS, UNVALIDATED, BLOCKED or FAIL. Only a real successful run can set `validated: true`.

A smoke PASS on a built-in dataset is scoped to that dataset/branch of execution; it does not
establish real-atlas validity or universal method superiority. V1 has no automatic DEFAULT
analysis method. `default_for` stays empty until comparison and biological fit are documented.
Plot `selection` is CURRENT_DEFAULT, RECOMMENDED_ALT, ARCHIVED or null; it chooses a
visual template within its declared input/demo scope and does not promote its analysis method.

Generated plots require `script`, `dataset`, `input_object`, `major_parameters`, `palette`,
`theme`, `output_file`, `vector_file`, `last_generated`, and validation evidence. Planned
plots have null output paths/date and cannot be CURRENT_DEFAULT. Retain old stable IDs
when deprecating an asset and specify `replaced_by` instead of deleting provenance.

Use `Rscript scripts/resolve_asset.R method|plot|palette ID` to resolve an ID,
`Rscript scripts/validate_library.R` for structure and promotion checks.
