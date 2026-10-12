# Progress Tracker

Live status of every workstream. Update it whenever a status changes. Owners match
[`team/roles-and-raci.md`](team/roles-and-raci.md).

Status legend: `Not started` · `Ready to run` · `In progress` · `Blocked` · `Done`

## Overall project status: **Pipeline complete** (notebooks 01 to 14 run; final report next)

| Date | Update |
|---|---|
| 2026-09-12 | Project scaffolded: dataset confirmed in `data/hotel_bookings.csv` (119,390 rows, 32 columns, SHA-256 `7c2ae42a...`). `docs/`, team roles/RACI, `ai-usage-disclosure/`, `DECISIONS.md` and this file created. |
| 2026-09-12 | Locked the Train/Dev/Test method (70/15/15, `docs/04` §4.10) and threshold selection on Dev, not Test (`docs/06` §6.5). Added SVM as a 6th model so every member owns at least one trained model. |
| 2026-09-15 | First data pipeline written as a `src/data/` package with `notebooks/01_data_quality_eda.ipynb`. Leakage in `reservation_status` confirmed. |
| 2026-10-11 | Moved to a notebook-only pipeline, `01` to `14` (decision #24). `src/` and the old draft notebooks retired (still in git history). `DECISIONS.md` and `PROGRESS.md` moved into `docs/`. Decisions #21 to #26 added. |
| 2026-10-11 | Notebooks 01 to 04 run end to end with no errors. Results: 87,138 clean rows, 27.28% cancelled; split 60,996 / 13,071 / 13,071; ADR cap 283.68; 94 model inputs (day-zero) and 109 (full-lifecycle). All 20 documented statistics matched the data. |
| 2026-10-11 | Fixed the project-root lookup in notebooks 05 to 14 (it still looked for `DECISIONS.md` at the repo root). |
| 2026-10-11 | Notebooks 05 and 06 run end to end. CV PR-AUC (day-zero / full-lifecycle): Logistic Regression 0.651 / 0.701, Decision Tree 0.700 / 0.745. Dummy baselines sit at 0.273 (the cancel rate). |
| 2026-10-11 | Notebook 07 search finished and both models were saved. CV PR-AUC: Random Forest 0.759 / 0.793 (Dev 0.763 / 0.801), best so far. The permutation importance cell ran out of RAM and closed VS Code: with `n_jobs=-1` every worker copied the ~200 MB forest. Fixed by running it in one process (`PERMUTATION_JOBS = 1`); the same fix was applied to notebook 13. |
| 2026-10-11 | Notebooks 07 to 09 finished. CV PR-AUC: Random Forest 0.759 / 0.793, XGBoost 0.765 / 0.805, SVM 0.677 (day-zero only, 12,000-row CV subsample). |
| 2026-10-11 | Notebook 10: 83 checks, no FAIL, 1 WARN (SVM subsample). All 11 models eligible. |
| 2026-10-11 | Notebooks 11 and 12: `xgboost__day_zero` selected (decision #27). Sigmoid calibration, threshold 0.35, tiers 0.18 / 0.35, policy locked (decision #28). |
| 2026-10-11 | Notebook 13: top drivers country, lead time, agent, special requests, market segment. Weak recall on Direct (0.32) and Corporate (0.43). Fairness audit flags 8 of 11 country groups. SHAP skipped (`shap` not installed, decision #30). |
| 2026-10-11 | Notebook 14: Test read once. PR-AUC 0.774 [0.760, 0.787], recall 0.778, precision 0.653 at 0.35. High tier = 32.5% of bookings, 77.8% of cancellations. Temporal check (2017): PR-AUC 0.650. Docs 04 to 08 and the decision log updated with the results. |
| 2026-10-12 | Rubric audit and new `plan.md`. Added: feature screening (notebook 04 §4.4), LR sensitivity checks (05 §6), gate chart (10), fairness bootstrap intervals (13 §6.2b), chart fixes (03, 11, 12, 13), framing canvas (docs/01), decisions #31 and #32. Notebook 11 ownership moved to Jayashan. `shap` 0.51.0 installed. |
| 2026-10-12 | New cells run. Notebooks 04, 05, 10, 11 and 12 were run in full: scores, predictions, parameters, the policy and the final model are identical (only timestamps changed), and the Test lock still verifies. Results: reduced-input LR 0.6506 vs 0.6507; all fairness flags confirmed by bootstrap intervals; SHAP drivers match permutation importance (decision #33). |

## Workstream status

| Workstream | Notebook | Owner | Status | Notes |
|---|---|---|---|---|
| Business problem framing | - | All / Hasitha (final review) | Done (draft) | `docs/01-business-problem-framing.md` |
| Workflow & architecture diagrams | - | Hasitha | Done (draft) | `docs/02-workflow-and-architecture.md` |
| Ingestion, data quality, leakage audit, cleaning | 01 | Bhanuka | Done | Clean file + `artifacts/data_contract.json` |
| Train / Dev / Test split | 02 | Seneja | Done | `artifacts/split_manifest.json` |
| EDA (Train only) + insight log | 03 | Bhanuka | Done | 19 figures, `reports/tables/eda_insight_log.csv` |
| Feature engineering + shared preprocessing | 04 | Seneja | Done | `artifacts/feature_spec.json`, 4 preprocessing templates, feature log |
| Dummy baselines + Logistic Regression | 05 | Bhanuka | Done | CV PR-AUC 0.651 (day-zero), 0.701 (full-lifecycle) |
| Decision Tree | 06 | Seneja | Done | CV PR-AUC 0.700 (day-zero), 0.745 (full-lifecycle) |
| Random Forest | 07 | Seneja | Done | CV PR-AUC 0.759 (day-zero), 0.793 (full-lifecycle) |
| XGBoost + tuning | 08 | Jayashan | Done | CV PR-AUC 0.765 (day-zero), 0.805 (full-lifecycle); early stop at round 610 |
| SVM (RBF) | 09 | Hasitha | Done | CV PR-AUC 0.677 (12,000-row subsample) |
| Validation gate | 10 | Hasitha | Done | 83 checks, 0 FAIL, 1 WARN; 11 of 11 models eligible |
| Evaluation, comparison, selection | 11 | Jayashan | Done | Selected `xgboost__day_zero` |
| Calibration, threshold, decision policy | 12 | Hasitha | Done | Sigmoid, threshold 0.35, policy locked |
| Explainability, errors, fairness | 13 | Hasitha | Done | Permutation importance, error profile, fairness audit; SHAP skipped |
| Final Test evaluation (once) | 14 | Hasitha | Done | Test PR-AUC 0.774; lock file written |
| Recommendation & limitations | - | Hasitha (with team input) | Done (draft) | `docs/07-recommendation-limitations.md` |
| Reproducibility write-up | - | Hasitha | Done (draft) | `docs/08-reproducibility.md` |
| AI-use disclosure logs | - | Each member, own file | In progress | `ai-usage-disclosure/` |
| Final report assembly | - | Hasitha + all | Not started | |

## Immediate next steps

1. Assemble the final report from `docs/05` to `docs/07` and the figures in
   `reports/figures/`. Every number must match a file in `reports/tables/`.
2. Optional: `pip install shap` and re-run notebook 13 for per-booking explanations
   (Test stays locked; notebook 13 only uses Dev).
3. Each member reviews the results for their own model and the recommendation.
4. Everyone: finish your AI usage log under `ai-usage-disclosure/`.
