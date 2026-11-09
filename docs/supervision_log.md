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

