# Phase 4 Environment

## Phase 4A

- Runtime: project-local Python 3.12 virtual environment at `.venv/`.
- The environment is created from the bundled Python runtime to avoid the global R incompatibility found in Phase 2/3.
- Install the direct requirements in `requirements.in` and record the resolved environment with `python -m pip freeze > environment/requirements-lock.txt`.
- Package import checks and hardware capability are recorded after installation.

The virtual environment itself and package caches are excluded from Git. Later R-based modules will use a separate isolated environment; they will not reuse the known-broken global R package library.

`CROSS-OS VALIDATION NOT PERFORMED`

