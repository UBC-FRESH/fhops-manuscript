# SoftwareX R2 comment register (SOFTX-D-26-00697R1 → R2)

- Decision letter: `decision-letter.txt` (minor revision; resubmit by 2026-11-04).
- Parent issue: UBC-FRESH/fhops-manuscript#20; branch `revision/softx-r2`.
- Reviewer #2 comments were extracted from PDF annotations (PyMuPDF `page.annots()`) in
  `SOFTX-D-26-00697_reviewer2.pdf`. **The reviewer annotated the original submission PDF
  (SOFTX-D-26-00697, 26 pp.), not R1**; page numbers below refer to that PDF.
- FHOPS capability claims were first verified against the `v1.0.0` tag. Since the decision to
  fix and disclose (2026-10-06) the manuscript pins **FHOPS 1.0.1** (frozen release commit
  `a0b2799`; tag `v1.0.1`), and claims are re-verified against that commit.

| ID | Source / location | Comment (verbatim) | Action | Manuscript change | Status |
|----|----|----|----|----|----|
| E.1 | Editor, decision letter | "You might consider putting some of the equations in an appendix." | Move full formulation + mapping table to Appendix A; keep prose summary + objective note in §2.3. FHOPS 1.0.1: appendix is the labelled 1.0.1 formulation (OBJ/OBJ2, E1–E13 with E8a–c, INIT, D1; E1–E11 kept for persisting blocks, old E9 batching → loader threshold). Pyomo names verified in fhops a0b2799 `model/milp/{operational,data,driver}.py`. | `fhops-softx.tex` `\appendix` + `sections/includes/fhops_operational_formulation.tex` (rendered from `revisions/softx-r2/fhops_operational_formulation_labelled.md` by `render_formulation.py`); `software_description.tex` §2.3 summary; response letter E.1 | done |
| R1.1 | Reviewer #1, decision letter | "All of my comments on the original version of the article have been reviewed and corrected. Therefore, I recommend the publication of this paper." | Thank reviewer | none | done |
| R2.0 | Reviewer #2, decision letter | "The authors have done an excellent job. The application of software and process is well written and explained. I would suggest adding market price of products based on inventory which can give better insights on economic feasibility of the harvesting operations." | Thank; market-price suggestion answered under R2.9 | see R2.9 | done |
| R2.1 | p1, title "FHOPS:" | "The authors have done a good job explaining FHOPS through the manuscript" | Thank | none | done |
| R2.2 | p4, keyword "forest operations," | "Forest harvest operations and optimisation already exist in the manuscript title consider another wording." | Replace title-duplicating keywords | `fhops-softx.tex` keywords: *forest operations*, *optimisation*, *heuristics* → *machine scheduling*, *mixed-integer programming*, *metaheuristics*. **Also update EM keyword field at upload.** | done |
| R2.3 | p4, abstract "FHOPS" | "Please expand" | Expand acronym at first use in abstract | `abstract.tex`: "The Forest Harvesting Operations Planning System (FHOPS) addresses…". **Also update EM abstract field at upload.** | done |
| R2.4 | p6, contribution 1 | "Good attempt" | Thank | none | done |
| R2.5 | p7, §2 intro ("given a set of blocks … mobilization constraints, what assignments … sequence, and with") | "Does this include trucking" | Clarify scope: model ends at loading at the landing; loader output counted in truckload batches (E9); haul transport out of scope. Verified v1.0.0: no truck/haul/mill fields in `Scenario`; loader batching `DEFAULT_TRUCKLOAD_M3=30` (`model/milp/data.py`). | `software_description.tex` §2 opening paragraph (FHOPS 1.0.1: loader truckload threshold E9; batching variables removed in 1.0.1) | done |
| R2.6 | p7, "should be made, in which sequence" | "Helps in decision making to have a coupled or decoupled harvesting system" | Explain head-start buffer (E8) supports comparing coupled vs decoupled systems. Verified v1.0.0 `operational.py`: `B = buffer_shifts × upstream capacity`; loader buffer ≥ truckload batch; reference ladder head-start 0.0 for processor/loader (`scripts/rebuild_reference_datasets.py`). | `software_description.tex` §2.1, new paragraph after entity list (FHOPS 1.0.1 labels: buffer E8b, waiver E8c, loader threshold E9) | done |
| R2.7 | p8, "-specific production rates," | "I believe utilization is considered here, because delays (operational/mechanical/ personal) has a major influence on the final cost of harvesting operations" | Explain: ladder rates come from published productivity models incl. their delay/utilisation allowances (ADV6N7 skidder utilisation 0.85; Berry 2019 processor delay multiplier 0.91; TN-261 loader 0.9); availability flags remove planned downtime; stochastic delays assessed in playback (downtime / weather / landing shocks). Acknowledge delays are not yet priced in schedule cost outputs (KPIs: mobilisation cost only in v1.0.0). | `software_description.tex` §2.1 bullets; `illustrative_example.tex` §3.2 disturbance description + manuscript sampling settings; `impact.tex` §4.4 new limitation | done |
| R2.8 | p8, "re-solving" | "plays a key role during weather uncertainities and delays" | Agree; describe rolling-horizon driver (`fhops plan rolling`, SA/MILP, lock days; in v1.0.0) and companion rolling-horizon study. Do **not** claim realised-disruption feedback (not implemented). | `software_description.tex` §2.2 (FHOPS 1.0.1: replayed state carried between windows, earliness tie-break OBJ2). Response letter: [THESIS PENDING] companion-study re-run | done (thesis outcome pending) |
| R2.9 | p10, parameter δ "cost" | "If market values of various products can be added it helps to estimate the revenue generated. This helps to get a better economic perspective of the harvesting operation." | Polite decline, no code change: revenue is fixed upstream by tactical-operational decisions (blocks, systems, prescriptions → assortment volumes); the operational model optimises execution of that fixed workload, so price does not change the optimal schedule. Note: FHOPS tactical-operational layer is **not** in v1.0.0, so it is not cited. | One clarifying sentence in `software_description.tex` §2 opening paragraph (planning hierarchy) | done |
| R2.10 | p20, Figure caption "Deterministic vs. stochastic utilization" | "Please make the legends readable" | R1 already removed the overlapping suptitle/legend clipping. Remaining issue: ~10 pt fonts on a 12 in figure (≈5 pt at column width), lowercase `sa`/`ils` tick labels. Fix requires a change to `docs/softwarex/manuscript/scripts/plot_playback_variability.py` in `fhops` (separate fhops issue/PR), then `make assets`. | Figure regenerated by FHOPS PR #105 (fhops#95): 5.35 × 2.4 in at text width (9 pt at print size), legend row inside canvas, no suptitle, SA/ILS labels, y label "Mean day-level utilisation"; caption corrected (bars, not points). Stochastic values changed because of the playback event fixes (fhops#93); §3.2 numbers and event descriptions updated. | done (§3.2 values to be re-synced with final 1.0.1 assets: [NUMBERS PENDING]) |

## Side findings (for `fhops` follow-up; decision 2026-10-06: fix all, re-check thesis, disclose)
- `planning/rolling.py` (identical in v1.0.0 and `main`) carries **no state** between windows, contrary to `notes/rolling_horizon_plan.md` (which marks demand/inventory carry-forward as done):
  - `_filter_and_rebase_blocks` keeps full `work_required` for every block (finished blocks re-planned).
  - Staged role inventories restart at zero each window (MILP `inventory_start == 0` at first slot; tracker `role_inventory` starts empty); upstream role progress (`role_remaining`) is not carried.
  - No initial machine position: first-shift moves in a window are free in the solve but charged in stitched playback.
  - User `Scenario.locked_assignments` are lost: hooks overwrite with `[]` in iteration 0, and slices ignore them from iteration 1. Locks from earlier windows are never active inside a window (by construction), and the operational MILP builder ignores locks entirely.
  - `ScheduleLock` has no `shift_id`; hooks drop `shift_id`/`production`, creating duplicate (machine, day) locks in multi-shift scenarios.
  - `copy.timeline` (blackouts) not rebased into window coordinates.
  - SA hook `runtime_s` always `None`; MILP hook default `solver="auto"` passed to `SolverFactory` unchanged.
  - No test asserts carry-forward behaviour; `docs/howto/rolling_horizon.rst` overstates lock handling.
- Thesis impact: Jaffray MASc Ch. 4 ran `fhops plan rolling` (editable fhops `1.0.0a2`) over 3 contexts × 3 sizes × θ∈{2,4,8,16} wk × lock∈{1,7,14} d × {SA, MIP/HiGHS 1800 s} = 216 runs; metric = last-iteration window objective (`json_processing_to_summary.py`), not stitched-plan KPIs. Findings cited in manuscript §1, §2.2, §4.2, §5 must be re-checked on fixed code using stitched-plan evaluation (`compute_rolling_kpis`).
- `LandingShockEvent.apply` decrements `remaining` per assignment row rather than per day; `DowntimeEvent` ignores `mean_duration_hours`/`std_duration_hours` (whole shift lost); `WeatherEvent` ignores `correlated_days`.
- `Block.work_required` is documented as generic work units (e.g. machine-hours) but loader batching treats it as m³.

## FHOPS 1.0.1 disclosure and regeneration (status 2026-10-07)
- Defects in `comments.md` side findings and the later audits (MILP formulation vs heuristics/playback, heuristic
  objective overstatement, landing guard/starvation, validation, legacy MIP) are fixed in FHOPS 1.0.1
  (`docs/releases/v1.0.1.md`). Response letter "Note on FHOPS 1.0.1" and cover letter rewritten to the
  final facts; the earlier claim that deterministic results were unchanged is withdrawn.
- All SoftwareX benchmark/tuning/playback/costing/scaling assets are regenerated on 1.0.1 (separate task).
  Open: sync Tables 4–5, §3 prose values, figures, and fill `[NUMBERS PENDING]` in both letters.
- Open: companion-study re-run on 1.0.1 (`[THESIS PENDING]` in both letters; manuscript claims in §1, §2.2,
  §4.2, §5 to be re-checked).
