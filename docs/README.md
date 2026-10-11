# Documentation Index: Hotel Booking Cancellation Prediction

This `docs/` folder contains the full project documentation, structured to match the
marking rubric. Each numbered file maps to one or more rubric criteria. The
implementation plan and issue audit live in [`../plan.md`](../plan.md). The executable
pipeline lives in [`../notebooks/`](../notebooks/) (notebooks `01` → `14`).

| # | File | Rubric criterion covered | Marks | Evidence produced by |
|---|------|---------------------------|------:|---|
| 1 | [01-business-problem-framing.md](01-business-problem-framing.md) | Business problem framing and lens/task formulation | 5 | - |
| 2 | [02-workflow-and-architecture.md](02-workflow-and-architecture.md) | Workflow diagram and decision log | 10 | [DECISIONS.md](DECISIONS.md) |
| 3 | [03-data-understanding.md](03-data-understanding.md) | Data understanding, EDA, and data quality reasoning | 10 | notebooks 01, 03 |
| 4 | [04-preprocessing-feature-engineering.md](04-preprocessing-feature-engineering.md) | Preprocessing and feature-engineering decisions | 15 | notebooks 01, 02, 04 |
| 5 | [05-modeling-strategy.md](05-modeling-strategy.md) | Model/data-mining strategy and comparison | 20 | notebooks 05–09, 11 |
| 6 | [06-evaluation-plan.md](06-evaluation-plan.md) | Evaluation, validation, and critical judgement | 20 | notebooks 10–14 |
| 7 | [07-recommendation-limitations.md](07-recommendation-limitations.md) | Recommendation, limitations, and stakeholder value | 10 | notebooks 12–14 |
| 8 | [08-reproducibility.md](08-reproducibility.md) | Reproducibility, documentation, and AI-use transparency | 10 | all notebooks |

Total: 100 marks.

## Living project records

- [`DECISIONS.md`](DECISIONS.md): decision log: what we decided and why, with evidence.
- [`PROGRESS.md`](PROGRESS.md): live status tracker for every workstream.

## Supporting documentation

- [`team/roles-and-raci.md`](team/roles-and-raci.md): who owns what, and the RACI matrix for the 4-person team.
- [`team/member-1-bhanuka-samarasinghe.md`](team/member-1-bhanuka-samarasinghe.md): Data engineering + EDA + Dummy/Logistic Regression (notebooks 01, 03, 05).
- [`team/member-2-seneja-ramanayake.md`](team/member-2-seneja-ramanayake.md): Split + features + preprocessing + Decision Tree/Random Forest (notebooks 02, 04, 06, 07).
- [`team/member-3-jayashan-guruge.md`](team/member-3-jayashan-guruge.md): Advanced modelling: XGBoost + tuning (notebook 08).
- [`team/member-4-hasitha-erandika.md`](team/member-4-hasitha-erandika.md): SVM, validation, evaluation, explainability, recommendation (notebooks 09–14).
- [`../ai-usage-disclosure/`](../ai-usage-disclosure/): per-member log of how and why AI tools were used (rubric AI-use transparency requirement).

## How to read this documentation

Read the numbered files in order the first time; each one assumes the previous one's
decisions. The notebooks are the **source of truth for numbers**. Every figure quoted
here must match a table in `reports/tables/` produced by a notebook. If a notebook and
a document disagree, correct the document and add a `DECISIONS.md` row explaining what
changed. `DECISIONS.md` and `PROGRESS.md` are living documents: update them as the
project moves, not only at the end.

## Dataset

- Source: [Kaggle: Hotel Booking Demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) (jessemostipak)
- Original paper: Antonio, de Almeida & Nunes (2019), "Hotel booking demand datasets", *Data in Brief*, 22, 41–49.
- Local file: `data/hotel_bookings.csv`
- Rows: 119,390 · Columns: 32 · After leakage-column drop + de-duplication: **87,138 rows**, 27.28 % cancelled
- SHA-256 fingerprint: `7c2ae42a7353905ea136e5c2287f17c92c5435826598bfbb8491c6f0c7b1fc06`
  (see [`08-reproducibility.md`](08-reproducibility.md) for how to verify this)
