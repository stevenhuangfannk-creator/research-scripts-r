# Codex rules

1. Read METHOD_INDEX and registry/methods.yml before searching for packages.
2. Check DEFAULT eligibility, validation scope and input species/scale/sample design.
3. Check namespace loading and actual package versions; never silently install on source().
4. Prefer validated reusable code when it fits the scientific question. No V1 method is a universal DEFAULT.
5. Preserve project-specific assumptions and provenance; do not copy an entire legacy script as a method.
6. Put new ideas in 95_inbox. Reproduce, validate and compare before promotion.
7. Every method needs input/parameter contracts, METHOD_CARD, OUTPUT_CATALOG, examples, references and gallery status.
8. Before plotting, read GALLERY and registry/plots.yml; use the matching CURRENT_DEFAULT template.
9. A template preference does not certify the upstream analysis. Never use synthetic figures as study evidence.
10. Retain older stable versions; deprecate with a reason and replacement ID.
11. No raw matrices, RDS/H5/FASTQ, compressed datasets, credentials or local library binaries in Git.
12. Use relative paths, configuration or environment variables; never import legacy absolute paths into new workflows.
13. Require biological roots, sample units, species, annotation and contrasts; do not invent them.
14. Record missing outputs as BLOCKED/UNVALIDATED. Never assert a completed analysis from static parsing.
15. Preserve cell/condition colors. Original diagrams must have editable source and explicit provenance/license.
