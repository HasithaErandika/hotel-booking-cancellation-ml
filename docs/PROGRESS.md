# Progress Tracker

Live status of every workstream. Update it whenever a status changes. Owners match
[`team/roles-and-raci.md`](team/roles-and-raci.md).

Status legend: `Not started` · `Ready to run` · `In progress` · `Blocked` · `Done`

## Overall project status: **In progress** (data, split, EDA and features done; modelling next)

| Date | Update |
|---|---|
| 2026-09-12 | Project scaffolded: dataset confirmed in `data/hotel_bookings.csv` (119,390 rows, 32 columns, SHA-256 `7c2ae42a...`). `docs/`, team roles/RACI, `ai-usage-disclosure/`, `DECISIONS.md` and this file created. |
| 2026-09-12 | Locked the Train/Dev/Test method (70/15/15, `docs/04` §4.10) and threshold selection on Dev, not Test (`docs/06` §6.5). Added SVM as a 6th model so every member owns at least one trained model. |
| 2026-09-15 | First data pipeline written as a `src/data/` package with `notebooks/01_data_quality_eda.ipynb`. Leakage in `reservation_status` confirmed. |
| 2026-10-11 | Moved to a notebook-only pipeline, `01` to `14` (decision #24). `src/` and the old draft notebooks retired (still in git history). `DECISIONS.md` and `PROGRESS.md` moved into `docs/`. Decisions #21 to #26 added. |
| 2026-10-11 | Notebooks 01 to 04 run end to end with no errors. Results: 87,138 clean rows, 27.28% cancelled; split 60,996 / 13,071 / 13,071; ADR cap 283.68; 94 model inputs (day-zero) and 109 (full-lifecycle). All 20 documented statistics matched the data. |
| 2026-10-11 | Fixed the project-root lookup in notebooks 05 to 14 (it still looked for `DECISIONS.md` at the repo root). |

## Workstream status

| Workstream | Notebook | Owner | Status | Notes |
|---|---|---|---|---|
| Business problem framing | - | All / Hasitha (final review) | Done (draft) | `docs/01-business-problem-framing.md` |
| Workflow & architecture diagrams | - | Hasitha | Done (draft) | `docs/02-workflow-and-architecture.md` |
| Ingestion, data quality, leakage audit, cleaning | 01 | Bhanuka | Done | Clean file + `artifacts/data_contract.json` |
| Train / Dev / Test split | 02 | Seneja | Done | `artifacts/split_manifest.json` |
| EDA (Train only) + insight log | 03 | Bhanuka | Done | 19 figures, `reports/tables/eda_insight_log.csv` |
| Feature engineering + shared preprocessing | 04 | Seneja | Done | `artifacts/feature_spec.json`, 4 preprocessing templates, feature log |
| Dummy baselines + Logistic Regression | 05 | Bhanuka | Ready to run | |
| Decision Tree | 06 | Seneja | Ready to run | |
| Random Forest | 07 | Seneja | Ready to run | |
| XGBoost + tuning | 08 | Jayashan | Blocked | `xgboost` is not installed on the team kernel yet (`pip install -r requirements.txt`) |
| SVM (RBF) | 09 | Hasitha | Ready to run | Slowest notebook (about 20 to 40 minutes) |
| Validation gate | 10 | Hasitha | Not started | Needs model cards from 05 to 09 |
| Evaluation, comparison, selection | 11 | Hasitha | Not started | Needs 10 |
| Calibration, threshold, decision policy | 12 | Hasitha | Not started | Needs 11 |
| Explainability, errors, fairness | 13 | Hasitha | Not started | Needs 12; `shap` not installed yet |
| Final Test evaluation (once) | 14 | Hasitha | Not started | Needs 12 |
| Recommendation & limitations | - | Hasitha (with team input) | Not started (template ready) | `docs/07-recommendation-limitations.md` |
| Reproducibility write-up | - | Hasitha | Done (draft) | `docs/08-reproducibility.md` |
| AI-use disclosure logs | - | Each member, own file | In progress | `ai-usage-disclosure/` |
| Final report assembly | - | Hasitha + all | Not started | |

## Immediate next steps

1. Install the missing packages on the team kernel: `pip install -r requirements.txt`
   (`xgboost` and `shap` are missing).
2. Run notebooks 05 to 09 (any order). Each one only reads Train and Dev.
3. Run notebook 10. Fix any `FAIL` in the model's own notebook, then re-run 10.
4. Run notebooks 11, 12, 13 and 14 in that order.
5. Everyone: log AI usage in your own file under `ai-usage-disclosure/` as you go.
