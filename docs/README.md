# Documentation Index — Hotel Booking Cancellation Prediction

This `docs/` folder contains the full documentation for the project, structured to
directly match the marking rubric. Each numbered file maps to one or more rubric
criteria.

| # | File | Rubric criterion covered | Marks |
|---|------|---------------------------|------:|
| 1 | [01-business-problem-framing.md](01-business-problem-framing.md) | Business problem framing and lens/task formulation | 5 |
| 2 | [02-workflow-and-architecture.md](02-workflow-and-architecture.md) | Workflow diagram and decision log | 10 |
| 3 | [03-data-understanding.md](03-data-understanding.md) | Data understanding, EDA, and data quality reasoning | 10 |
| 4 | [04-preprocessing-feature-engineering.md](04-preprocessing-feature-engineering.md) | Preprocessing and feature-engineering decisions | 15 |
| 5 | [05-modeling-strategy.md](05-modeling-strategy.md) | Model/data-mining strategy and comparison | 20 |
| 6 | [06-evaluation-plan.md](06-evaluation-plan.md) | Evaluation, validation, and critical judgement | 20 |
| 7 | [07-recommendation-limitations.md](07-recommendation-limitations.md) | Recommendation, limitations, and stakeholder value | 10 |
| 8 | [08-reproducibility.md](08-reproducibility.md) | Reproducibility, documentation, and AI-use transparency | 10 |

Total: 100 marks.

## Supporting documentation

- [`team/roles-and-raci.md`](team/roles-and-raci.md) — who owns what, and the RACI matrix for the 4-person team.
- [`team/member-1-bhanuka-samarasinghe.md`](team/member-1-bhanuka-samarasinghe.md) — Data Engineering + EDA + Logistic Regression.
- [`team/member-2-seneja-ramanayake.md`](team/member-2-seneja-ramanayake.md) — Feature Engineering + Preprocessing + Random Forest.
- [`team/member-3-jayashan-guruge.md`](team/member-3-jayashan-guruge.md) — Advanced Modeling (XGBoost) + Tuning.
- [`team/member-4-hasitha-erandika.md`](team/member-4-hasitha-erandika.md) — Validation, Evaluation, Explainability, Recommendation.
- [`../PROGRESS.md`](../PROGRESS.md) — live status tracker for every workstream.
- [`../DECISIONS.md`](../DECISIONS.md) — decision log: what we decided and why, with evidence.
- [`../ai-usage-disclosure/`](../ai-usage-disclosure/) — per-member log of how/why AI tools were used, per rubric's AI-use transparency requirement.

## How to read this documentation

Read in numeric order the first time — each file assumes the previous one's decisions.
After the project has code, the notebooks in `notebooks/` and modules in `src/` should
match what is described here; if they don't, **update this documentation**, don't let
it drift. `DECISIONS.md` and `PROGRESS.md` are living documents — update them as the
project moves, not only at the end.

## Dataset

- Source: [Kaggle — Hotel Booking Demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) (jessemostipak)
- Original paper: Antonio, de Almeida & Nunes (2019), "Hotel booking demand datasets", *Data in Brief*, 22, 41-49.
- Local file: `data/hotel_bookings.csv`
- Rows: 119,390 · Columns: 32
- SHA-256 fingerprint: `7c2ae42a7353905ea136e5c2287f17c92c5435826598bfbb8491c6f0c7b1fc06`
  (see [`08-reproducibility.md`](08-reproducibility.md) for how to verify this)
