# V1 pre-refactor audit

Base: `2f12bd7850407fdae44497a116fab8368613526b`. Original branch: `phase4-flagship-reconstruction`.
The original checkout had four untracked sensitivity notes/scripts in an active reproduction.
They remain in the original checkout; a separate Git worktree protects them from this refactor.
No reset, forced overwrite, stash, project move or deletion was used.

Complete committed tree: [pre-refactor tree](validation/pre_refactor_tree.txt).
Every preserved project/reproduction/library/original doc has a SHA-256 record in
[preservation.json](validation/preservation.json). Existing README/docs and all 28 original
R/Quarto source files were reviewed through the script catalog and source patterns.

Known pre-existing problems: legacy absolute paths, absent RDS/raw inputs, gaps in object
production, APAP final-object merge marked non-executing, and old CellChat igraph namespace
patches. They stay documented in the original project audits. New code does not inherit these
patches, hardcoded worker counts or tissue-specific auto-labels. No large data was added.
