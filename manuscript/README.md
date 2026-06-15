# FHOPS SoftwareX Manuscript Workspace

This directory houses the working sources for the SoftwareX submission. It is intentionally separate from `reference/` (snapshots) and `assets/` (shared figures/data) so we can script builds without touching upstream artifacts.

```
manuscript/
├── outline.md               # Living section-by-section plan (mirrors SoftwareX template)
├── sections/                # Individual content files (LaTeX include snippets)
├── elsarticle/              # Stock CTAN elsarticle class + sample manuscript (unzipped 2025-11-23)
├── fhops-softx.tex          # Wrapper that stitches sections/includes together
├── references.bib           # Manuscript BibTeX database (exemplar + forestry cites + FHOPS refs)
├── scripts/                 # Asset-generation hooks (call FHOPS benchmarks etc.)
├── Makefile                 # `make all` orchestrates assets + PDF build
├── README.md                # (this file) build + workflow notes
└── build/ (generated)       # latexmk output directory (ignored)
```

## Template snapshot
- Source: https://mirrors.ctan.org/macros/latex/contrib/elsarticle.zip (mirrors the official Elsevier `elsarticle` bundle).
- Retrieved: 2025-11-23 via `curl -L -o docs/softwarex/reference/templates/elsarticle-template.zip …`.
- Contents live under `elsarticle/`. Keep upstream files pristine; place FHOPS-specific adjustments (title page, macros, includes) in `sections/` or sibling files so we can diff against the CTAN baseline.

## SoftwareX template compliance audit

Issue #5 rechecked the manuscript wrapper after the FHOPS v1.0.0 publication so the
submission source does not drift from Elsevier/SoftwareX expectations.

- The working source uses the official Elsevier `elsarticle` bundle snapshot stored at
  `extras/reference/templates/elsarticle-template.zip` and keeps the upstream class,
  installer, and numbered BibTeX styles under `manuscript/elsarticle/`.
- `fhops-softx.tex` intentionally mirrors `elsarticle-template-num.tex`: it uses
  `\documentclass[preprint,review,12pt]{elsarticle}`, `\journal{SoftwareX}`, a standard
  `frontmatter` block, `abstract`, `keyword`, numbered sections, `elsarticle-num`, and
  `references.bib`.
- The SoftwareX-specific requirements that are not present in the generic `elsarticle`
  shell are supplied as frontmatter inputs: `sections/highlights.tex`,
  `metadata/code_metadata.tex`, and `metadata/current_code_version.tex`.
- The Elsevier `Updated_software-update-template.tex` available online is explicitly for
  updates to an existing SoftwareX article, not for an Original Software Publication, so
  FHOPS should not be migrated into that update template.
- For submission packaging, compile the checked-in source with `make pdf`. The broader
  `make all` target refreshes local manuscript assets first and is useful for authors, but
  the source package itself should include the already-generated `sections/includes/*`
  tables and figures needed by `fhops-softx.tex`.

Audit status: `make all` passes after the v1.0.0 metadata update. Remaining overfull/float
layout warnings are tracked separately in issue #9.

## Corresponding author contact details

The manuscript source records the public corresponding-author contact details required for
submission: email via `\ead{}`, work phone in `\cortext{}`, and full UBC postal address
in `\address{}`. Editorial Manager can duplicate these details during submission, but the
LaTeX source should remain self-contained for the source package.

## Build workflow (`latexmk` + TeX Live)
We use the standard TeX Live toolchain (preferred by SoftwareX) orchestrated through `latexmk`. The Makefile also provides an `all` target so we can regenerate FHOPS assets + PDF in a single command.

```
# Rebuild everything (clean → assets → PDF)
make all

# Just build the PDF
make pdf    # or simply `make`

# Clean auxiliary files + build directory
make clean
```

`scripts/generate_assets.sh` is the one-stop entry point for reproducible artifacts. It now:

- Runs the shared Markdown/CSV exporter (`export_docs_assets.py`).
- Invokes `render_prisma_diagram.py`, which compiles the TikZ workflow figure via `latexmk` and drops PDF/PNG assets into `docs/softwarex/assets/figures/`.
- Executes dataset inspection, benchmark suites (SA/ILS/Tabu), tuning harness, playback robustness, costing demo, and scaling sweeps so every referenced CSV/JSON/PNG is fresh.

Environment knobs:

- `FHOPS_ASSETS_FAST=1 make assets` trims benchmark budgets (shorter time limits/iterations and `run_tuner.py --tier micro`) so you can sanity-check the pipeline without waiting for the full runs. Use the default (`0`) for submission-quality artifacts.
- All scripts respect the current Python interpreter (`python`); set `PYTHONPATH`/virtualenv as usual. `render_prisma_diagram.py` requires `latexmk`, `lualatex`, and either ImageMagick (`magick`) or `pdftoppm` for PNG export (optional `pdf2svg` for SVG).

Manual verification checklist (run after `make assets`):

1. **Datasets:** `docs/softwarex/assets/data/datasets/` contains `index.json` plus per-scenario summaries (`*_summary.json`).
2. **Benchmarks:** Each scenario folder under `docs/softwarex/assets/data/benchmarks/` has `summary.(csv|json)` + `telemetry.jsonl`; `index.json` lists all runs.
3. **Tuning:** `docs/softwarex/assets/data/tuning/` includes `softwarex_summary.*` plus tuner-specific reports; `telemetry/steps/*.jsonl` remains git-ignored by design.
4. **Playback:** `docs/softwarex/assets/data/playback/<scenario>/` holds `day.csv`, `shift.csv`, `metrics.json`, and rendered Markdown summaries.
5. **Costing:** `docs/softwarex/assets/data/costing/cost_summary.(csv|json)` present with matching telemetry logs.
6. **Scaling:** `docs/softwarex/assets/data/scaling/` contains `scaling_summary.(csv|json)` and `runtime_vs_blocks.png`.
7. **Figures/snippets:** `docs/softwarex/assets/figures/prisma_overview.(pdf|png)` regenerates, and `docs/includes/softwarex/*.rst` mirror the Markdown snippets.

If any directory is missing or stale, re-run `FHOPS_ASSETS_FAST=0 make assets` to produce the canonical versions, then `make pdf` to rebuild the manuscript. `latexmk` will automatically run when the manuscript PDF is built. You’ll need a TeX Live installation that includes common packages (`latexmk`, `tikz`, `hyperref`, `lineno`, etc.). On Debian/Ubuntu, `sudo apt-get install texlive-full latexmk` is still the quickest path; we can revisit a lighter scheme/tectonic later if build times become an issue.

### Benchmark-only runs & logging

- `make manuscript-benchmarks` runs `scripts/run_manuscript_benchmarks.sh`, which in turn executes the full asset pipeline and appends a log entry (UTC start time, commit hash, runtime seconds, combined SHA-256 hash of `docs/softwarex/assets/**`) to `docs/softwarex/assets/benchmark_runs.log`.
- `make manuscript-benchmarks-fast` does the same but sets `FHOPS_ASSETS_FAST=1` for quick sanity checks.
- Use these targets before major milestones or submissions so we have a reproducibility audit trail without forcing a full PDF build each time.

## Metadata tables & reproducibility log
- `metadata/code_metadata.tex` and `metadata/current_code_version.tex` store the journal-required tables (version, licence, supported platforms, installation method, benchmark log path). Update them whenever release naming, contact info, or reproducibility evidence changes.
- The introduction references Tables~\ref{tab:code-metadata}–\ref{tab:current-code-version}, so keep those entries aligned with the text and the actual reproducibility log at `docs/softwarex/assets/benchmark_runs.log`.

## Planned workflow
1. **Template adaptation:** `fhops-softx.tex` pulls the elsarticle class and `\input`s the files under `sections/`, with citations managed via `references.bib`. Section files are intended to be reusable (shared with Sphinx via includes later).
2. **Single-source content:** Draft prose in `sections/*.tex`. When content stabilises, we can symlink or otherwise share snippets with the Sphinx docs.
3. **Automation hooks:** Once figure/table scripts exist, wire them into the Makefile (e.g., `make assets`) so `make` regenerates everything end-to-end before `latexmk` runs.

## Immediate todos
- [x] Unpack the `elsarticle` template locally, commit only the files we customise.
- [x] Decide on the LaTeX toolchain (latexmk + TeX Live) and document it here.
- [ ] Flesh out each section file with real FHOPS content and tie in shared snippets/figures.
