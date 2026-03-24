# FHOPS SoftwareX Manuscript Workspace

This repository is intentionally split for Overleaf-friendly import and editing.

| Path | Purpose |
|------|---------|
| `manuscript/` | Core LaTeX source (main file, sections, metadata, bibliography, class/template files) used for paper writing and compile. |
| `assets/` | Minimal compile-time assets referenced directly by manuscript text (`tables/*.tex`, key PNG figures). |
| `extras/` | Git submodule pointing to `fhops-manuscript-extras` for non-essential artifacts (reference vault, benchmark/tuning/playback/scaling raw outputs, generation scripts, scratch files). |

## Overleaf Compile Notes

The manuscript is expected to compile from:

- `manuscript/fhops-softx.tex`
- `manuscript/references.bib`
- `manuscript/sections/**`
- `manuscript/metadata/**`
- `manuscript/elsarticle/**`
- minimal files under `assets/` used by section includes

The `extras/` submodule is not required for day-to-day Overleaf writing/compile.
