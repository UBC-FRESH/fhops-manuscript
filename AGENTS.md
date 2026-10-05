# Coding Agent Operating Notes (FHOPS SoftwareX manuscript)

These notes govern day-to-day execution for coding agents (and collaborators) working in the
`fhops-manuscript` repository, which holds the LaTeX sources, compile-time assets, and submission
tooling for the FHOPS SoftwareX paper (Editorial Manager ID `SOFTX-D-26-00697`). Treat this file
as the root `AGENTS.md`: it applies to all subdirectories unless a more specific `AGENTS.md`
overrides or extends it. It is adapted from the FHOPS package contract
(`UBC-FRESH/fhops/AGENTS.md`); where the two disagree on manuscript matters, this file wins.

## Non-negotiables
- **Never edit on `main`, and never leave work uncommitted.** `main` is the authoritative record of
  the last version uploaded to the journal. All edits happen on a branch, are committed in small
  steps, pushed, and merged back through a pull request.
- **One review round, one branch.** Do not start a new revision round until the previous round's
  branch has been committed, pushed, PR'd, and merged to `main` (see "Branch and issue workflow").
- **Read before acting:** re-read this file, the latest `CHANGE_LOG.md` entries, the current
  decision letter, and the reviewer-comment register for the active round before proposing work.
- **No silent changes:** every change set is recorded in `CHANGE_LOG.md` immediately after
  implementation (see "Planning hygiene").
- **Generated assets are never hand-edited.** Tables and figures under `assets/` and
  `manuscript/sections/includes/` are produced by the FHOPS asset pipeline; fix the generator or
  its inputs and regenerate instead.
- **Author list is frozen** once a manuscript is under review. Changing authors requires an
  editor-approved authorship-change form; never alter `\author`/`\address` blocks without explicit
  instruction from the corresponding author.

## Repository layout
| Path | Purpose |
|------|---------|
| `manuscript/` | Core LaTeX source: `fhops-softx.tex` wrapper, `sections/`, `metadata/`, `references.bib`, `elsarticle/`, `Makefile`. |
| `manuscript/sections/includes/` | Compile-time copies of generated tables/figures plus shared TeX includes (formulation, workflow figure). |
| `assets/` | Minimal compile-time assets copied from the FHOPS asset pipeline (`make assets` source). |
| `extras/` | Git submodule (`fhops-manuscript-extras`) for raw benchmark outputs, reference vault, scratch files. Not needed to compile. |
| `manuscript/revisions/softx-r<N>/` | Per-round revision material: decision letter, reviewer-comment register, response letter source (create on first use). |
| `CHANGE_LOG.md` | Dated, newest-first log of every change set. |

The manuscript is also edited through Overleaf (commits titled "Updates from Overleaf" land on
`main`). Pull/fetch before branching, and avoid concurrent Overleaf edits while a revision branch
is open; if they happen, merge `main` into the active branch before continuing.

## Branch and issue workflow
- **Revision rounds:** each journal decision opens one long-lived branch
  `revision/softx-r<N>` created from an up-to-date `main` (R1 → `revision/softx-r1`, etc.) and one
  parent GitHub issue that states the decision, due date, branch, scope, the comment register
  location, acceptance criteria, verification commands, and closeout requirements.
- **Child work:** decompose a round into child issues (one per reviewer comment or tightly related
  cluster). Child branches are `issue-<number>-<short-slug>`, branched from the revision branch and
  merged back into it by PR (`Part of #<parent>`). Small rounds may commit directly on the revision
  branch, but still in small, comment-scoped commits whose messages cite the comment IDs.
- **Unrelated work** (tooling, README, this contract, template fixes) gets its own issue and an
  `issue-<number>-<short-slug>` branch off `main`; do not mix it into a revision branch. After it
  merges, bring the open revision branch up to date with `main`.
- **Closing a round:** once the revised package has been uploaded to Editorial Manager, commit the
  exact submitted state, push, open a PR from `revision/softx-r<N>` to `main`, and merge it
  (squash merge, subject ending in `(#<PR>)`, matching repository history). Only then create the
  next round's branch.
- If GitHub CLI/auth is unavailable, record the intended issue/PR titles, bodies, and exact `gh`
  commands in the changelog entry before editing, and sync real numbers back once created.

## Reviewer comments and responses
- Extract every comment verbatim, including comments embedded as PDF annotations (e.g. with
  PyMuPDF: iterate `page.annots()` and record `info["content"]` plus the highlighted text). Note
  which manuscript version the reviewer annotated; it may not be the latest submission.
- Keep a comment register for the round (`manuscript/revisions/softx-r<N>/comments.md`) with
  stable IDs (`E.1` editor, `R1.3`, `R2.7`, ...), verbatim text, location, planned action,
  manuscript change location, and status.
- **Verify before claiming.** Every capability statement in the manuscript or response letter about
  FHOPS behaviour must be checked against the code in the `fhops` repository (cite file/function in
  the register). Do not claim features that are planned, partial, or only exist in a different
  planning layer without saying so.
- Response letters answer each comment by ID, quote the change made (with section/line), and are
  courteous and concise. Where a request is out of scope, explain why and what was done instead.

## Cross-repo boundaries
- The asset pipeline (benchmarks, tuning, playback, scaling, figure scripts) lives in
  `UBC-FRESH/fhops` under `docs/softwarex/`. Regenerate there, then copy with `make assets`
  (or `make manuscript-benchmarks`) here. Record the FHOPS commit hash used.
- Do not modify the `fhops` repository as a side effect of manuscript work. If a revision needs a
  code or generator change, propose it first, then follow the FHOPS `AGENTS.md` workflow (issue,
  branch, PR, tests) in that repository.
- The code-metadata tables (`manuscript/metadata/*.tex`) are pinned to a released FHOPS tag. Any
  manuscript claim that depends on new FHOPS code requires a new release and synchronized updates to
  both tables, the installation instructions, and the reproducibility log reference.

## Build and verification cadence (run before handing work back)
1. `make -C manuscript pdf` (latexmk + TeX Live). If no system TeX is available, build with
   Tectonic from `manuscript/` (e.g. `tectonic -p -c minimal -o build fhops-softx.tex`) and say so.
2. Confirm zero unresolved references/citations (no `??` or `[?]` in the PDF text) and that every
   figure and table renders.
3. Audit layout: no text spans past the right margin and no new overfull boxes beyond those
   documented in the changelog.
4. When generated assets change: regenerate from the FHOPS pipeline and check that every number
   quoted in prose matches the regenerated tables.
5. Before an upload: `make -C manuscript submission-package`, then extract the flat zip into a
   clean temporary directory and compile it standalone to prove it builds.

Record the exact commands executed, and key outcomes (page count, reference count, warnings), in
the current `CHANGE_LOG.md` entry. Address warnings instead of suppressing them.

## Revision deliverables (per round)
- Clean manuscript PDF (`manuscript/build/fhops-softx.pdf`).
- Flat Editorial Manager source zip (`manuscript/build/fhops-softx-em-flat.zip`; EM rejects
  subfolders).
- Marked-up PDF against the previously submitted version, generated with
  `latexdiff --type=CFONT --no-del --disable-citation-markup --math-markup=off` (avoids broken
  citation markers and interleaved deleted text).
- Response-to-reviewers PDF and cover letter, built from sources under
  `manuscript/revisions/softx-r<N>/`.
- Record SHA-256 hashes of every uploaded file in the changelog.

## Planning hygiene
- `CHANGE_LOG.md` entries are dated, newest first, and headed by the round or issue they belong to
  (cite issue/PR numbers once known). Summaries should mirror the status shared with maintainers.
- Keep the comment register and the parent issue checklist in sync whenever work starts, pauses,
  or completes. Never let TODOs live only in chat history.
- Flag blockers or scope questions (e.g. a reviewer request that would need new FHOPS features) in
  the register and the parent issue, and get a decision from the corresponding author before
  implementing.

## Writing conventions
- Follow the SoftwareX Original Software Publication structure already in `fhops-softx.tex`
  (highlights, code metadata tables, motivation, software description, illustrative example,
  impact, conclusions). Keep the stock `elsarticle` files pristine; customise in `sections/` or
  the wrapper.
- Match the surrounding spelling and terminology; do not introduce new acronyms without expanding
  them at first use (abstract and body separately).
- Keep claims bounded to demonstrated evidence; limitations stay explicit.

## Credentials and secrets
- Never print, copy, or commit credential files or tokens (e.g. PyPI tokens, GitHub tokens). When
  you need to know what a credentials file contains, list key names only.
- Use the existing git credential helper for pushes; if `gh` is not logged in, pass a token through
  the environment for that command only and never echo it.

## Starting a new agent chat
- Open this repository as the workspace. Tell the agent: "We are working on the FHOPS SoftwareX
  manuscript in this workspace. Before making changes, read `AGENTS.md`, the latest
  `CHANGE_LOG.md` entries, and the active round's `manuscript/revisions/softx-r<N>/` files."
- Confirm the current branch and that the working tree is clean before editing.
