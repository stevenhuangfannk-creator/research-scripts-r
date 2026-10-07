# How to add a method

Paper/Idea → 95_inbox → Candidate → Reproduce → Validate → Compare → Extract portable workflow
→ Generate outputs → Inspect gallery → Write method card → Promote.

1. State the research question, expected biological unit, input type/scale and decision boundary.
2. Audit official docs, tutorial/vignette, author repository and original paper. Record URL,
   commit/tag, license, adaptations and unresolved differences. Community code needs a clear license.
3. Preserve source projects. Extract only reusable logic; parameterize paths, species and decisions.
4. Use the [method card template](templates/METHOD_CARD.md). Describe core/optional/advanced/comparison,
   visual/table/object outputs with scientific meaning, parameters, code and proposed figure role.
5. Use an existing user dataset first, recoverable project data second, official demo third,
   small public data fourth. Do not download large new studies for smoke tests.
6. Run namespaces, input alignment, workflow, table/object and PNG/vector checks. Save commands,
   logs, versions, input provenance, exclusions and failure details. Add a meaningful regression
   test when repairing or refactoring behavior, including the reproduced failure.
7. Compare against the current method using the same data and biological criteria. Runtime,
   mixing, lineage preservation, inference calibration and interpretability matter differently.
8. Add a source-linked plot registry entry only after generating and inspecting it. Keep missing
   outputs planned with null paths/dates. Add palettes and stable cell colors separately.
9. Promote CANDIDATE → VALIDATED only on real execution evidence with explicit scope;
   RECOMMENDED needs comparison; DEFAULT needs a documented question-specific preference.
   Demote obsolete assets to DEPRECATED and point to the replacement; keep history.

A method contribution includes Method + Output + Visualization + Gallery + Comparison + Registry.
Candidate-only placeholders explicitly state the absent parts. Run `Rscript scripts/validate_library.R`
before committing. No raw data or local dependency libraries are committed.
