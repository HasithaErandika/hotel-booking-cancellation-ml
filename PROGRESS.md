# Progress Tracker

Live status of every workstream. Update this whenever a status changes — don't
let it go stale. Owners match [`docs/team/roles-and-raci.md`](docs/team/roles-and-raci.md).

Status legend: `Not started` · `In progress` · `Blocked` · `Done`

## Overall project status: **In progress** (documentation & planning phase complete)

| Date | Update |
|---|---|
| 2026-09-12 | Project scaffolded: dataset confirmed in `data/hotel_bookings.csv` (119,390 rows, 32 cols, SHA-256 `7c2ae42a...`). Full `docs/` structure, team roles/RACI, `ai-usage-disclosure/`, `DECISIONS.md`, and this file created. No modeling code written yet. |
| 2026-09-12 | Locked leakage-safe Train/Dev/Test methodology (70/15/15, `docs/04-preprocessing-feature-engineering.md` §4.10) and fixed threshold selection to use Dev, not Test (`docs/06-evaluation-plan.md` §6.5). Added SVM as a 6th model so every member individually owns at least one trained model (`docs/05-modeling-strategy.md` §5.0-5.1); updated RACI and Hasitha's plan accordingly. |

## Workstream status

| Workstream | Owner | Status | Notes |
|---|---|---|---|
| Business problem framing | All / Hasitha (final review) | Done (draft) | `docs/01-business-problem-framing.md` — review as a team before treating as final. |
| Workflow & architecture diagrams | Hasitha | Done (draft) | `docs/02-workflow-and-architecture.md` — Mermaid diagrams; keep in sync with actual repo structure as it's built. |
| Data ingestion + schema validation | Bhanuka | Not started | `src/data/ingestion.py`, `src/data/validation.py` |
| Data-quality profiling & EDA | Bhanuka | Not started (documentation pre-drafted from a manual profiling pass) | `docs/03-data-understanding.md` has real numbers already computed; needs to be reproduced in `notebooks/01_data_quality_eda.ipynb` as the source of truth going forward |
| Leakage audit (`reservation_status`) | Bhanuka, confirmed by Hasitha | Done (finding), Not started (code assertion) | Finding confirmed: 100% match between `reservation_status` and `is_canceled` — see `docs/03-data-understanding.md` §3.5 |
| Feature engineering | Seneja | Not started | `src/features/engineering.py`; feature list drafted in `docs/04-preprocessing-feature-engineering.md` §4.5 |
| Preprocessing pipeline (shared) | Seneja | Not started | `src/features/preprocessing.py` |
| Decision Tree model | Seneja | Not started | |
| Random Forest model | Seneja | Not started | |
| Logistic Regression model | Bhanuka | Not started | |
| XGBoost model + tuning | Jayashan | Not started | |
| SVM model + tuning | Hasitha | Not started | Satisfies Hasitha's own "must train ≥1 model" requirement, see `docs/05-modeling-strategy.md` §5.0 |
| Dummy baseline | Bhanuka | Not started | Trivial but must be logged first as the comparison floor (62.96% accuracy) |
| Validation gate (leakage/split checks) | Hasitha | Not started | `src/evaluation/validation.py` |
| Unified evaluation framework | Hasitha | Not started | `src/evaluation/metrics.py` |
| Calibration + threshold analysis | Hasitha | Not started | |
| Explainability (SHAP, importances) | Hasitha | Not started | |
| Final recommendation & limitations | Hasitha (drafted with team input) | Not started (template ready) | `docs/07-recommendation-limitations.md` |
| Reproducibility writeup | Hasitha | Done (draft) | `docs/08-reproducibility.md` |
| AI-use disclosure logs | Each member, own file | Not started (templates ready) | `ai-usage-disclosure/member-*.md` |
| Final report assembly | Hasitha + all | Not started | |

## Immediate next steps

1. All 4 members review `docs/` and `DECISIONS.md`, correct anything that
   doesn't match how the team actually wants to work.
2. Bhanuka: stand up `notebooks/01_data_quality_eda.ipynb`, reproduce every
   number in `docs/03-data-understanding.md`.
3. Seneja: start `src/features/` once Bhanuka's cleaned dataset output exists.
4. Jayashan: wait on Seneja's shared pipeline before starting tuning.
5. Everyone: log AI usage in your own file under `ai-usage-disclosure/` as you go,
   not retroactively.
