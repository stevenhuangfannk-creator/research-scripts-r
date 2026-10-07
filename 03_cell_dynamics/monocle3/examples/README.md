# Minimal validation contract

Input `list(counts, cell_metadata, gene_metadata)` with exact barcode/gene alignment and
`gene_short_name` metadata. Select a biologically connected lineage. Supply justified
root barcodes in `config/default.yml`; no interactive or arbitrary default root is chosen.

```sh
Rscript scripts/run_method.R monocle3 03_cell_dynamics/monocle3/config/default.yml --allow-unvalidated
Rscript scripts/run_method.R monocle3_dynamics 03_cell_dynamics/monocle3/config/dynamics.yml --allow-unvalidated
```

Smoke gate: namespace load, CDS counts/metadata alignment, preprocessing through ordering,
nonempty principal graph, reachable-cell report, actual PNG/PDF outputs. Re-run with alternate
biologically plausible roots and graph settings before interpreting ordering. Infinite
pseudotime is reported, never replaced by zero. 3D is optional and should use a separately
recomputed 3-component UMAP/graph and `plot_cells_3d`; no 3D result is supplied in V1.
