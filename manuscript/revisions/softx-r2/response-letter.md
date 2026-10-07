# Response to Reviewer Comments — FHOPS (SOFTX-D-26-00697R2)

**Manuscript:** FHOPS: a reproducible optimisation and benchmarking stack for forest harvest operations
**Decision:** Minor revision
**Editor:** Randall Sobie (Editor-in-Chief, SoftwareX)

---

## Summary of changes

We thank the editor and both reviewers for their careful reading and positive assessment. In
this revision we have:

1. Clarified the planning scope of the operational model in Section 2: where it sits in the
   planning hierarchy, and that haul transport is outside its boundary (R2.5, R2.9).
2. Explained how production rates, availability, and stochastic playback represent
   utilisation and operational, mechanical, and weather delays, and added an explicit
   limitation on delay costing (R2.7).
3. Described how head-start buffers support comparing coupled and decoupled harvesting
   systems (R2.6), and how the rolling-horizon driver supports re-solving after disruptions
   (R2.8).
4. Revised the keywords (R2.2), spelled out FHOPS in the abstract (R2.3), and improved the
   legibility of the playback figure (R2.10).
5. Moved the full operational MILP formulation to an appendix, as the editor
   suggested (E.1), with labelled constraint blocks and an equation-to-code table.
6. Corrected defects in FHOPS that the review led us to find, released FHOPS 1.0.1, and
   regenerated every benchmark, tuning, playback, and scaling result on that release (see the
   note on FHOPS 1.0.1 at the end of this letter).

Reviewer #2's annotations were made on the PDF of the original submission. Below we refer to
sections of the revised manuscript.

---

## Editor

### E.1 "You might consider putting some of the equations in an appendix."

**Response:** Done. Appendix A now gives the complete formulation of the operational MILP as
implemented in FHOPS 1.0.1: sets, parameters, decision variables, the objective (OBJ), the
constraint blocks (E1–E13), the optional initial state (INIT) and earliness tie-break (OBJ2),
the domain declarations (D1), and a table that maps each labelled block to the Pyomo objects that
implement it. Blocks that persist from FHOPS 1.0.0 keep their labels (E1–E11). E6 (machine
moves), E7 (staged inventory), E8 (activation and head start, now E8a–E8c), E9 (loader truckload
threshold) and E11 (landing capacity per shift) were reformulated in 1.0.1, and E12 (remaining
output) and E13 (locked assignments) are new. A short paragraph at the end of the appendix
summarises what changed from FHOPS 1.0.0. Section 2.3 keeps a prose summary of the objective
and of each constraint family, with the traceability argument. This shortens the main text
without losing the auditable link between the equations and the implementation.

---

## Reviewer #1

### R1.1 "All of my comments on the original version of the article have been reviewed and corrected. Therefore, I recommend the publication of this paper."

**Response:** We thank Reviewer #1 for the constructive first-round comments and for
recommending publication.

---

## Reviewer #2

### R2.0 General comment: "The authors have done an excellent job. The application of software and process is well written and explained. I would suggest adding market price of products based on inventory which can give better insights on economic feasibility of the harvesting operations."

**Response:** We thank the reviewer for this positive assessment. We address the market-price
suggestion in detail under R2.9 below.

### R2.1 (title) "The authors have done a good job explaining FHOPS through the manuscript" — and R2.4 (contribution 1) "Good attempt"

**Response:** Thank you.

### R2.2 (keywords) "Forest harvest operations and optimisation already exist in the manuscript title consider another wording."

**Response:** Agreed. We replaced the keywords that repeat the title ("forest operations",
"optimisation") and replaced "heuristics" with more specific terms. The keywords are now:
*machine scheduling; mixed-integer programming; metaheuristics; reproducibility; forest
management planning; sustainability*.

### R2.3 (abstract) "Please expand" [FHOPS]

**Response:** Done. The abstract now spells out the name at first use: "The Forest Harvesting
Operations Planning System (FHOPS) addresses that requirement…".

### R2.5 (Section 2) "Does this include trucking"

**Response:** No. The operational model schedules the in-block machine roles up to and including
loading at the landing. A loader works only once a truckload (or the block's remaining volume,
if smaller) is staged at the landing (constraint block E9), but haul transport (truck fleets,
dispatching, and delivery to mills) is outside the model.
We now state this boundary explicitly in the opening paragraph of Section 2.

### R2.6 (Section 2) "Helps in decision making to have a coupled or decoupled harvesting system"

**Response:** We agree, and we now make this capability explicit in Section 2.1. Each role can be
given a head-start (in shifts of upstream output), which sets the staged buffer B_{r,b} in
constraint block E8b (the buffer is waived once the upstream roles have finished the block,
E8c):

- A positive head-start represents a decoupled system, e.g. a roadside processor that starts
  only once a deck has accumulated.
- A zero head-start approximates a coupled (hot) system, limited only by the one-shift staging
  lag of E7.

Users can therefore compare both configurations on the same scenario and data contract. The
reference ladder uses zero head-start for processing and loading, apart from the loader's
truckload threshold (E9).

### R2.7 (Section 2.1, production rates) "I believe utilization is considered here, because delays (operational/mechanical/ personal) has a major influence on the final cost of harvesting operations"

**Response:** We agree that delays strongly affect production and cost. FHOPS represents them at
three levels, which we now describe in the manuscript:

1. **Production rates.** For the reference ladder, rates are derived from published productivity
   models and include each source model's delay or utilisation allowance (Section 2.1).
2. **Availability.** Machine availability flags in the shift calendar remove planned downtime,
   such as maintenance or crew days off, from the schedule (Section 2.1).
3. **Stochastic playback.** The solved schedule is replayed under sampled disruptions: machine
   downtime, weather, and landing shocks. The new text in Section 3.2 names these disturbance
   types and the sampling settings used for the reported results. Their effect on utilisation is
   shown in the playback figure.

We also added a limitation to Section 4.4. Delay effects are currently reported as utilisation
and production losses. The schedule-level cost outputs cover mobilisation only and do not yet
convert delays into standby or delay costs.

### R2.8 (Section 2.2) "[re-solving] plays a key role during weather uncertainities and delays"

**Response:** We agree. Section 2.2 now notes that FHOPS ships a rolling-horizon driver
(`fhops plan rolling`). It re-solves successive planning windows with the SA or MILP solver
while locking near-term decisions, which supports periodic re-planning after weather or delay
disruptions. Before each window, the locked plan is replayed and its state (remaining block
volume, staged inventories, machine positions, and locks) is carried into the next window; MILP
windows add an earliness tie-break so that they do not defer work beyond the locked days. While
preparing this answer we found that FHOPS 1.0.0 did not carry this state between windows; the
correction is part of FHOPS 1.0.1 (see the note at the end of this letter). The design of
rolling-horizon re-optimisation (planning-horizon length and re-optimisation frequency) is
evaluated in the companion study cited in the manuscript, across three BC operating contexts and
three problem sizes. [THESIS PENDING: outcome of the re-run of the companion study's experiment
grid on FHOPS 1.0.1.]

### R2.9 (Section 2.3, mobilisation cost parameter) "If market values of various products can be added it helps to estimate the revenue generated. This helps to get a better economic perspective of the harvesting operation."

**Response:** We thank the reviewer for this suggestion and agree that net revenue matters for
the economic feasibility of harvesting operations. However, it falls outside the decision scope
of the model presented here.

FHOPS addresses short-term (e.g. multi-week), detailed operational machine scheduling. At this
level, the decisions that determine gross revenue have already been made upstream, in
tactical-operational planning:

- which blocks are harvested;
- with which harvest system and prescription;
- and hence which assortments and volumes are produced.

The operational model takes these decisions as fixed inputs. It optimises how the resulting
workload is executed: machine–block assignments, sequencing, timing, delivered production,
mobilisation, and landing use.

Because the assortment volumes are fixed upstream, product prices are not needed to formulate
or solve this scheduling problem. The objective instead rewards delivering the planned volume
and penalises volume left unharvested. Economic feasibility in the revenue-and-margin sense is
evaluated at the tactical-operational level, where the revenue-determining decisions are
actually made.

We note that, since this manuscript was first submitted, FHOPS has gained a very early-alpha
tactical-operational planning layer, published as pre-release FHOPS 1.1.0a1. It includes
product values at mills and terminals and profit or net-present-value objectives, which is the
planning level where the reviewer's suggestion applies. That layer is provisional and outside
the scope of this paper; Section 4.3 now mentions it briefly.

To make this explicit to readers, we added a sentence to the opening paragraph of Section 2. It
positions the operational model below tactical-operational planning and explains why the
objective concerns schedule execution rather than profit.

### R2.10 (Figure: deterministic vs. stochastic utilisation) "Please make the legends readable"

**Response:** Done. The overlapping title and clipped legend in the original submission were
already corrected in the first revision. In this revision the figure is redrawn at the
manuscript text width, so all text, including the legend, prints at 9 pt or larger. The legend
now sits in a single row above the panels, the solver labels are in upper case (SA, ILS), and
the caption has been corrected. While regenerating this figure we found and fixed defects in
FHOPS's stochastic playback events. The figure and the utilisation values in Section 3.2 were
regenerated on FHOPS 1.0.1 and have changed; see the note on FHOPS 1.0.1 at the end of this
letter. [NUMBERS PENDING: size of the change in the Section 3.2 utilisation values.]

---

## Note on FHOPS 1.0.1 (software correction)

The reviewers' questions on delays, re-solving, and figure legibility (R2.7, R2.8, R2.10) led us
to re-examine the corresponding FHOPS code paths, and from there to audit FHOPS 1.0.0 more
broadly: the MILP formulation against the heuristics and playback, the heuristic objective, and
input validation. The audit found defects. We chose to fix them and say so openly, rather than
defer, work around, or silently omit them. All fixes come with regression tests and are released
as **FHOPS 1.0.1** (https://github.com/UBC-FRESH/fhops/releases/tag/v1.0.1;
`pip install fhops==1.0.1`), which the code metadata tables now cite. The release notes list
every change.

What was corrected:

1. **Rolling-horizon driver.** State was not carried from one planning window to the next. Each
   window re-planned every block's full volume, including volume already delivered in earlier
   locked days; staged inventory between roles restarted at zero; and machine positions,
   user-specified locks, and blackout calendars were not carried across window boundaries.
   FHOPS 1.0.1 replays the locked plan before each window and carries its state forward. MILP
   windows also use an earliness tie-break, so they no longer defer work beyond the locked days.
2. **Stochastic playback.** Landing shocks were applied per assignment row rather than per
   calendar day, machine downtime always removed a whole shift instead of the configured
   duration, and weather and landing effects overwrote downtime instead of combining with it.
3. **MILP warm start.** Warm-starting the operational MILP failed with the default open-source
   solver (HiGHS). It now works, and FHOPS reports whether HiGHS accepted the start.
4. **Operational MILP formulation (Appendix A).** Several constraint blocks did not match the
   rules applied by the heuristics and by playback, so some MILP plans could not be replayed
   without sequencing violations or were charged differently:
   - staged inventories are now kept per upstream role (E7), so a role with several upstream
     roles processes only wood that each of them has staged;
   - each role's output is capped at the volume the block still holds (E12), the head-start
     buffer is waived once the upstream roles have finished the block (E8c), and the loader
     threshold is the smaller of one truckload and the remaining volume (E9);
   - landing capacity is enforced per shift and is hard at the default weight (E11); in 1.0.0 it
     was counted per day with a slack that cost nothing at the default weight, so it did not bind;
   - machine moves are charged also when a machine idles between two blocks, and staying on a
     block is no longer charged (E6);
   - the loader batching variables of 1.0.0, which imposed no restriction, were removed;
   - timeline blackouts are enforced in the MILP (E1), and blocks without a harvest system carry
     no role obligations (E2).
5. **Heuristic objective.** SA, ILS, and Tabu searched and reported a score that could be higher
   than the score of the schedule they returned, because the moves of machines not touched by
   the last repair were not charged. The reported objective is now a fresh evaluation of the
   returned schedule. The heuristics' repair step also respects landing capacity on every day,
   no longer starves downstream roles on capacity-limited landings, and penalises hard
   violations so that a schedule cannot gain from keeping an infeasible assignment.
6. **Validation and legacy code.** Scenario validation is stricter (e.g. inconsistent locks,
   invalid initial states, and unknown harvest-system identifiers are rejected when a scenario
   is loaded). The legacy day-level MIP, which was infeasible for every scenario with a loader
   role, has been retired; `fhops solve-mip` now solves the operational MILP described in the
   paper.

Effect on the manuscript:

- **All results were regenerated.** Every SoftwareX asset (benchmark, tuning, playback, costing,
  and scaling) was regenerated on FHOPS 1.0.1 in one pipeline run. Tables 4 and 5, the values
  quoted in Section 3, and the playback and scaling figures therefore changed.
  [NUMBERS PENDING: main changes, e.g. med42 objectives, the tuning Δ values, and the
  synthetic-small row.] [NUMBERS PENDING: whether the interpretation in Section 3 is unchanged.]
- **Formulation.** Appendix A states the FHOPS 1.0.1 model with labelled blocks and a short
  summary of the changes from 1.0.0 (see E.1). Section 2 describes the corrected behaviour
  (landing capacity per shift, rolling-horizon state, warm starts with HiGHS, exact heuristic
  objectives).
- **Reproducibility.** Seeded heuristic results are bit-reproducible on a fixed platform, but
  last-bit floating-point differences between NumPy or Python builds can change an SA
  trajectory. Section 4.4 now says so, and the published assets record the platform used.
- **Companion rolling-horizon study.** [THESIS PENDING: outcome of the re-run of the companion
  study's experiment grid on FHOPS 1.0.1 and any resulting wording changes in Sections 1, 2.2,
  4.2, and 5.]
