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
   suggested (E.1).

Reviewer #2's annotations were made on the PDF of the original submission. Below we refer to
sections of the revised manuscript.

---

## Editor

### E.1 "You might consider putting some of the equations in an appendix."

**Response:** Done. The complete canonical formulation now appears in Appendix A: sets,
parameters, variables, the objective, constraint blocks E1–E11, domain declarations, and the
equation-to-code mapping table. Section 2.3 keeps a short prose summary of the objective and of
each constraint family, together with the traceability argument. This shortens the main text
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
loading at the landing. Loader output is counted in truckload-sized batches (constraint block
E9), but haul transport (truck fleets, dispatching, and delivery to mills) is outside the model.
We now state this boundary explicitly in the opening paragraph of Section 2.

### R2.6 (Section 2) "Helps in decision making to have a coupled or decoupled harvesting system"

**Response:** We agree, and we now make this capability explicit in Section 2.1. Each role can be
given a head-start (in shifts of upstream output), which sets the staged buffer B_{r,b} in
constraint block E8:

- A positive head-start represents a decoupled system, e.g. a roadside processor that starts
  only once a deck has accumulated.
- A zero head-start approximates a coupled (hot) system, limited only by the one-shift staging
  lag of E7.

Users can therefore compare both configurations on the same scenario and data contract. The
reference ladder uses zero head-start for processing and loading, apart from the loader's
truckload batch.

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
disruptions. The design of such rolling-horizon re-optimisation (planning-horizon length and
re-optimisation frequency) is evaluated in the companion study cited in the manuscript, across
three BC operating contexts and three problem sizes.

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

**Response:** [Pending.] The overlapping title and clipped legend in the original submission were
already corrected in the first revision. In this revision we regenerated the figure with larger
fonts, a clearly separated legend, and upper-case solver labels (SA, ILS).
