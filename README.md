# RentAgent

Evaluating Multi-Agent Decomposition and Algorithmic Fairness in AI-Assisted
Rental Decision Support for the UK Private Rented Sector

MSc Artificial Intelligence Technology — Northumbria University
Module LD7236 | Student ID 25063317

## Overview

A rental decision-support system built in two configurations — a six-agent
orchestrated architecture and a matched single-agent baseline — to test whether
task decomposition improves constraint satisfaction and factual accuracy, and
whether recommendations remain equitable across household types.

**RQ1** How accurately can rent be predicted from listing-level UK data?
**RQ2** Does multi-agent decomposition outperform a matched single agent, and at
what computational cost?
**RQ3** Do recommendations change when only household composition varies, after
controlling for legitimate suitability requirements?

## Status

Week 7. Chapters 1 to 3 submitted. Implementation in progress.

| Component | State |
|---|---|
| Data cleaning pipeline | Complete — 3,478 raw to 2,400 Greater London listings |
| District to BRMA mapping | Complete — modal assignment with confidence score |
| District spatial features | Complete — centroids and distance from Charing Cross |
| Council tax by borough | Complete — MHCLG Band D, 33 London boroughs |
| Legal corpus | Complete — 149 sections with commencement status |
| Price Prediction agent (RQ1) | Complete — XGBoost with four ablation studies |
| Profile agent | Complete — bedroom standard and sanitisation boundary |
| Affordability agent | Complete — LHA, market rate and council tax |
| Alternatives agent | Complete — nearby areas, bedroom options, budget gap |
| Rights agent | Complete — RAG with abstention and commencement status |
| Orchestrator | Complete — conditional routing across five agents |
| Single-agent baseline | Complete — ReAct with constrained tool calling |
| Synthetic personas | 12 of 40 — six matched-entitlement pairs |
| Evaluation harness | Not started |
| Streamlit interface | Not started |

## RQ1: rent prediction

Trained on 2,400 Greater London listings with continuous spatial features
rather than categorical district labels.

| Model | R² | MAE | RMSE | MAPE |
|---|---|---|---|---|
| Linear regression | 0.7921 | £560 | £1,284 | 19.9% |
| XGBoost | **0.8225** | **£538** | **£1,164** | **18.3%** |

Comparable to Zhang et al. (2026), who report R² 0.79 on the Dublin rental market using approximately 5,000 observations.

### Ablation studies

**Spatial representation.** Continuous coordinates outperformed 205 categorical
district labels using 32 features rather than 233. Under standard
cross-validation the gap was marginal (R² 0.8225 against 0.8172). Under
leave-district-out validation, where entire districts are held out, it widened
to 0.7769 against 0.7042: a one-hot column for an unseen district carries no
information, whereas coordinates permit interpolation.

**Data curation.** Masking whole-property bathroom counts on shared lettings
improved R² by 0.008. The binary shared-letting indicator produced no
measurable benefit, the information already being captured by property type.

**Leakage diagnostic.** Retaining deposit raised R² to 0.9266 and halved MAE.
The improvement is artificial: UK deposits are capped at five weeks' rent and
the median in this dataset is exactly 5.00 weeks, making the field a
deterministic transformation of the target.

### Prediction error by household size

| Bedrooms | Training examples | MAPE |
|---|---|---|
| 1 | 795 | 16.6% |
| 2 | 700 | 14.6% |
| 4 | 49 | 51.2% |

Bedroom entitlement derives from household composition, so prediction quality
varies systematically with a characteristic the fairness audit examines.

## The legal corpus

149 sections extracted from the Renters' Rights Act 2025, each carrying its
commencement status. As at 19 November 2026, 98 sections are in force and 51
are enacted but not yet commenced with no appointed date, largely the private
rented sector database provisions in sections 64 to 96. The Rights agent
reports this status rather than presenting uncommenced provisions as current law.

## The sanitisation boundary

Household composition is received only by the Profile agent, which applies the
Local Housing Allowance size criteria and derives a numerical constraint object:
occupants, minimum and preferred bedrooms, budget ceiling, area and property
type. No demographic attribute crosses to downstream agents, so they cannot
condition recommendations on protected characteristics under Chapter 3 of Part 1
of the Renters' Rights Act 2025.

Compliance is tested rather than assumed. RQ3 evaluates whether outcomes diverge
across matched personas despite the boundary.

## Structure

```
data/raw/          source datasets (gitignored; see data/raw/README.md)
data/processed/    derived lookups and cleaned listings
notebooks/
  01_data_inventory      profiling of all source datasets
  02_data_cleaning       raw listings to 2,400 usable records
  03_brma_lookup         postcode district to Broad Rental Market Area
  04_spatial_features    district centroids and distance to centre
  05_rent_model          RQ1 prediction model and ablation studies
  06_council_tax         MHCLG Band D rates by London borough
  07_legal_corpus        Act chunking, commencement status, vector index
  08_personas            synthetic personas for RQ2 and RQ3
src/agents/        agent implementations
results/           evaluation outputs
docs/              supervision log and viva preparation notes
```

## Environment

Python 3.12. Install dependencies with:

```
pip install -r requirements.txt
```

Data sources, licences and access dates are documented in `data/raw/README.md`.
Raw data is not committed.