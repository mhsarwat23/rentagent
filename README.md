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
| Price Prediction model (RQ1) | Baseline complete; ablation studies in progress |
| Profile agent | Complete — bedroom standard and sanitisation boundary |
| Affordability agent | Complete — LHA and market rate benchmarking |
| Council tax integration | Not started |
| Alternatives agent | Not started |
| Rights agent (RAG) | Not started |
| Orchestrator | Not started |
| Single-agent baseline | Not started |
| Streamlit interface | Not started |
| Synthetic personas | Not started |

## RQ1: rent prediction

Trained on 2,400 Greater London listings with continuous spatial features
rather than categorical district labels, enabling generalisation across
districts with few observations.

| Model | R² | MAE | RMSE | MAPE |
|---|---|---|---|---|
| Linear regression | 0.7921 | £560 | £1,284 | 19.9% |
| XGBoost | **0.8225** | **£538** | **£1,164** | **18.3%** |

Comparable to Zhang et al. (2026), who report R² 0.79 on the Dublin rental
market using approximately 5,000 observations.

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
  05_rent_model          RQ1 prediction model and baseline
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