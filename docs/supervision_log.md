\# Supervision Log

\## Week 0 - w/c 21 Sept 2026

Done: Project Initiation Form submitted. Repo, Python environment and folder structure set up.
Issues resolved: Git not installed; Python Store alias blocking venv; PowerShell execution policy.
Next: Source VOA/ONS rental data.
Questions for supervisor:

1. Is Low Risk Secondary Data the correct ethics category given evaluation uses synthetic personas?
2. Any preferred dataset for the rent prediction model?

\## Week 1 - w/c 8 Oct 2026

First supervision session, 8 October. Group format, largely administrative.

Covered: 11-week schedule to 19 December, weekly supervisory meeting forms

required with e-signature, Project Approval Form due Week 6 (6 November).



Tasks set: identify one base paper and two reference papers, all practical

or empirical studies rather than surveys. Begin drafting the introduction.



Done: data inventory notebook completed across four datasets. Four questions

prepared for supervision but not answered, as the session was administrative.



\## Week 2 - w/c 15 Oct 2026

Group session not attended. Supervisory contact by email.



Detailed written feedback received 20 October on the revised proposal and

introduction chapter.



Principal issue: architectural contradiction. The original design withheld

household composition entirely from the Affordability and Alternatives agents,

which would prevent those agents from assessing statutory space requirements,

HMO licensing and minimum bedroom counts.



Resolution adopted: attribute sanitisation layer. The Profile agent applies

the statutory bedroom standard used for Local Housing Allowance assessment

and derives a numerical constraint object (occupants, min\_bedrooms,

preferred\_bedrooms, budget\_max, area, property\_type). Only this object crosses

to downstream agents. Translation implemented deterministically so it can be

audited.



Other revisions: counterfactual fairness (Kusner et al., 2017) adopted for RQ3;

manual scoring replaced with schema-validated structured outputs and RAGAS;

Wilcoxon signed-rank testing added; baseline standardised using ReAct;

React dashboard replaced with Streamlit; matched pairs increased from 4 to 12.



Reference verification: Raju et al. withdrawn after finding SSRN is a preprint

repository rather than a peer-reviewed journal. Replaced with Zhang et al. (2026),

Springer. ReAct found to have been published at ICLR 2023 rather than the 2022

preprint originally cited.



\## Week 3 - w/c 22 Oct 2026

Session 22 October on the content and structure of the introduction and

literature review.



Guidance: the introduction must incorporate base and reference papers, state

key deliverables, motivation and contribution. The literature review must cover

all material affecting the project and identify research gaps explicitly.

Sources informing practical approach should be published from 2020 onwards,

though foundational theory may be older.



Supervisor confirmed the revised architecture resolves the contradiction and

instructed to proceed with Chapters 2 and 3. Recommended moving technical

specifications from Part A of the proposal into the methodology chapter.



Base paper confirmed: Cemri et al. (2025), NeurIPS 2025.

Reference papers: Kusner et al. (2017); Zhang et al. (2026).



\## Week 4 - w/c 29 Oct 2026

Project Approval Form completed, e-signed and submitted for countersignature.

Ethics category: low-risk secondary data science project.



Literature review drafted across four themes: rent prediction and

transferability; multi-agent decomposition; retrieval grounding in legal

domains; algorithmic fairness.



\## Methodological note - proxy pathways (5 Nov 2026)

Identified while writing section 2.2.4. Peng, Chakraborty and Menzies (2023)

use residential zip codes as proxies for race in lending as their worked

example of proxy discrimination.



This applies directly to RentAgent. The sanitisation layer withholds household

composition but passes postcode district, which may carry demographic signal.



Consequence: the fairness evaluation must test two pathways, not one.

&#x20; 1. Constraint leakage - does the tuple (occupants, min\_bedrooms,

&#x20;    preferred\_bedrooms, budget\_max) imply household composition?

&#x20; 2. Location leakage - does postcode district carry demographic signal

&#x20;    correlated with protected characteristics?



The original design assumed only (1). Dutta et al. (2021) on feature exemptions

provides the formal treatment for both.



\## Week 5 - w/c 5 Nov 2026

One-to-one session. Platform and tooling confirmed: Colab and Jupyter for

development, GitHub for version control, Python as implementation language.



Dataset coverage discussed. Supervisor suggested extending the comparison to a

United States city. Noted in response that US evidence is already addressed in

the literature review, and that the primary variables are architecture and

fairness rather than geography. London-only scope retained.



Interim report timing agreed: methodology complete by Tuesday 11 November,

draft interim report comprising Chapters 1 to 3 shared by Wednesday 12 November.



\### Dataset decisions (supervisor email, 9 Nov 2026)

1\. ONS postcode district suppression (47%, concentrated in rooms 76% and

&#x20;  studios 66%): fall back to borough-level figures for those categories.

&#x20;  Document in preprocessing. List spatial smoothing as a formal limitation.

2\. Cross-area comparison: substitute Local Housing Allowance BRMA rates as the

&#x20;  primary benchmark for the Alternatives agent. Retain ONS/VOA for

&#x20;  within-area context only, documenting the non-comparability warning.

3\. Structure: fold dataset specifications into Data Collection and

&#x20;  Preprocessing subsections rather than a standalone section.

4\. Versioning: fix the PIPR release of 16 September 2026 as the version of

&#x20;  record. Later revisions frozen out to prevent drift during validation.



\### LHA data finding (9 Nov 2026)

DWP LHA tables for 2026-27 show Table 1 (April 2024 rates) and Table 4

(April 2026 rates) are identical. Rates have been frozen since 2024.



Table 2 gives the 30th percentile of market rents, which LHA is nominally set

against. The gap is substantial: Central London 2-bed LHA is GBP 412.86 weekly

against a 30th percentile of GBP 690.41, a shortfall of GBP 277.55 per week.



Implication: LHA remains valid for cross-area comparison, since the freeze

applies uniformly. For affordability assessment it would understate real cost.

Proposed approach is to use Table 2 as the affordability benchmark and Table 4

for cross-area ranking, documenting the reason.



Status: to be raised with supervisor before Wednesday.



\## Next steps

\- Chapter 3 methodology, due Tuesday 11 November

\- Draft interim report (Chapters 1-3), due Wednesday 12 November

\- Chase countersignature on Project Approval Form



## Week 6 - w/c 12 Nov 2026

Interim report submitted 13 November comprising Chapters 1 to 3, with Appendix A
(signed Project Approval Form) and Appendix B (data catalogue). Revised and
resubmitted 13 November following supervisory feedback.

### Supervisor feedback on the interim report
Rated as making substantial progress. Required changes: state the exact model
and embedding model in Section 3.5; add tables for feature engineering, persona
stratification and tool parity; correct in-text citations and add formal
citations for XGBoost, the Data Protection Act 2018, UBDC and ONSPD; insert a
List of Figures and List of Tables; standardise to British English.

All actioned before resubmission, except the persona stratification table, which
was replaced by a statement that the distribution would be specified during
construction.

### Dataset question and supervisory decision (19 Nov)
Raised the sparsity and concentration findings: 123 of 224 districts held fewer
than five listings, and 36 per cent of listings fell within five districts
(E14, W8, SW5, SW7, W14), reflecting what was advertised at the time of
collection rather than the composition of the London rental stock.

Supervisor directed: proceed with the cleaned dataset; no larger open-licensed
property-level London rental dataset exists and scraping is not advisable;
replace categorical district labels with continuous ONSPD spatial features;
document the concentration explicitly; integrate MHCLG council tax rather than
narrowing the methodology.

Three technical checks were specified and all three were actioned.

**Deposit.** The supervisor stated the correlation with rent was 0.98. Measured
across the cleaned dataset it is 0.598, because 838 of 2,400 listings record a
deposit of zero as a placeholder. Among the 1,654 recording a non-zero deposit
it is 0.98 as he indicated, and the median is exactly 5.00 weeks of rent,
reflecting the cap under the Tenant Fees Act 2019. Both figures are correct for
different subsets. Deposit dropped as a predictor.

**Outer London districts.** The supervisor estimated 33 listings outside Greater
London. Thirty-nine were found, identified through the BRMA mapping rather than
by postcode prefix, since HA, UB and TW span the boundary. Districts affected
were in Slough, Watford, St Albans, Walton, Dartford and the Chilterns. Removed
so that the model and the Affordability agent share identical geographic scope.

**Spatial leakage.** No neighbourhood rent features computed; spatial variables
are static coordinates derived independently of rent.

Final cleaned dataset: 2,400 listings across 205 districts. Chapter 3 states
2,167 and 227 and requires updating.

---

## Week 7 - w/c 19 Nov 2026

One-to-one session. Platform and tooling confirmed. The supervisor asked whether
a hosted API service was in use; confirmed that inference runs locally through
Ollama and the Rights agent draws only on retrieved chunks from the Act. Advised
to secure work at each milestone, which is already the practice. Latency raised;
advised patience.

Four questions submitted by email afterwards on the RAGAS test set size and
construction, whether the Rights agent should decline on uncommenced provisions,
persona stratification, and the evaluation budget.

### RQ1 complete

| Model | R² | MAE | RMSE | MAPE |
|---|---|---|---|---|
| Linear regression | 0.7921 | £560 | £1,284 | 19.9% |
| XGBoost | 0.8225 | £538 | £1,164 | 18.3% |

Four ablation studies run as the supervisor specified.

**Spatial representation.** The decisive result. Under standard splitting the
continuous and categorical representations were nearly identical (0.8225 against
0.8172). Under leave-district-out validation the gap widened to 0.7769 against
0.7042 — fifteen times larger. A one-hot column for an unseen district carries
no information; coordinates permit interpolation from proximate areas. Continuous
used 32 features against 233.

**Curation.** Masking whole-property bathroom counts on shared lettings improved
R² by 0.008. The is_shared indicator produced no measurable benefit and MAE was
marginally better without it, the information already being captured by property
type. Retained because the Affordability agent requires a single flag. Reported
as a negative result.

**Leakage diagnostic.** Retaining deposit raised R² to 0.9266 and reduced MAE to
£305, approaching the figures reported by Tapia et al. and An et al. The model
learns to invert the statutory deposit formula rather than to price property.

**Error by household size.** MAPE is 14.6% at two bedrooms (700 training
examples) and 51.2% at four (49 examples). Bedroom entitlement derives from
household composition, so prediction quality varies systematically with a
characteristic the fairness audit examines. A fairness audit testing only
whether recommendations differ would not detect this.

### Agents implemented

Profile (bedroom standard and sanitisation), Affordability (LHA, 30th percentile
market rents, MHCLG council tax), Alternatives (nearby cheaper districts,
bedroom options, budget gap), Rights (RAG over the Act), Price Prediction
(XGBoost), and an Orchestrator with conditional routing.

### Legal corpus

149 sections extracted from the Act. Section-level chunking required three
filters: page furniture, inserted-text subsections carrying their own numbering,
and an ordering constraint rejecting any section number lower than one already
seen. Two filter errors were caught by checking the sequence for gaps: excluding
headings beginning "No " dropped section 41, "No prohibition on taking income
into account", which is the provision the RQ3 framing depends on.

As at 19 November 2026, 98 sections are in force and 51 are enacted but not yet
commenced with no appointed date, largely the database provisions in sections 64
to 96. An initial parse flagged all 149 as in force because "in force at" is a
substring of "not in force at Royal Assent"; corrected to require a date.

### Two defects found by testing

**Bedroom standard.** A person aged 16 or over passed in the children list fell
through both age filters and received no bedroom allocation, under-allocating by
one. A household entitled to four bedrooms returned three — the overcrowding the
design exists to prevent. Corrected to reclassify as an adult with a notice to
the user.

**Sanitisation boundary.** A test checking the constraint object for forbidden
keys passed while household composition leaked through the plain-language notice
explaining the reclassification. Testing the values as well as the keys exposed
four leaking terms. The notice was rerouted around the boundary, since it is
addressed to the user rather than required by any downstream agent.

### Single-agent baseline

Implemented with ReAct prompting and constrained JSON output, which eliminated
malformed tool calls. The agent failed to terminate across repeated attempts:
given six iterations for a task requiring three tool calls, a list of unused
tools, an instruction not to repeat, and an explicit command to finish on the
final step, it called a data-gathering tool instead. Reasoning across consecutive
steps was near-identical — "now that I have the benchmarks, I need to compare" —
followed by another retrieval rather than a comparison.

This corresponds to the verification failures in Cemri et al. (2025). It is not
yet a comparative result: the multi-agent system has not been run at scale, and
it completes by construction rather than by judgement, so completion rate is not
a fair comparison. The substantive comparison will be on constraint satisfaction,
factual accuracy and cost.

### Personas

Twelve of forty constructed: six matched-entitlement pairs where both personas
have identical min_bedrooms, so any divergence has no suitability justification.
Restricted to districts with BRMA modal share of 0.80 or above and with listings
present, so the mapping does not confound the comparison.

---

## Next steps
- Six differing-entitlement persona pairs and sixteen unpaired personas
- Evaluation harness running both architectures over all forty
- RAGAS test set and abstention threshold calibration
- Streamlit interface
- Chapter 3 updates: 2,400 listings, 205 districts, spatial features, council tax