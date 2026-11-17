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
| Data cleaning pipeline | Complete — 3,478 raw to 2,439 usable listings |
| Profile agent | Complete — bedroom standard and sanitisation boundary |
| Affordability agent | Complete — LHA and market rate benchmarking |
| Price Prediction agent | Pending dataset confirmation |
| Alternatives agent | Not started |
| Rights agent (RAG) | Not started |
| Orchestrator | Not started |
| Single-agent baseline | Not started |
| Streamlit interface | Not started |

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
data/processed/    cleaned outputs (gitignored)
notebooks/         exploratory analysis and cleaning pipeline
src/agents/        agent implementations
src/models/        prediction model
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