# Team Roles and RACI Matrix

Team: 4 members. Architecture is "shared data contract, shared preprocessing
pipeline, independent model per member" — see
[`../02-workflow-and-architecture.md`](../02-workflow-and-architecture.md) §2.3
for the ownership diagram. No one works from a private copy of the data or a
private preprocessing step; everyone consumes the same pipeline outputs.

> **Non-negotiable rule:** every member must personally train, tune, and log at
> least one model end-to-end into the shared evaluation table — contributing only
> to shared pipeline code (data cleaning, feature engineering) is not sufficient
> on its own. See `../05-modeling-strategy.md` §5.0.

## Ownership table, models grouped by task category

| Member | Role title | Pipeline stage owned | Model owned | Task category | Doc |
|---|---|---|---|---|---|
| **Bhanuka Samarasinghe** | Data Engineer / EDA lead | Ingestion, schema validation, data-quality audit, EDA | Logistic Regression | Linear / interpretable | [member-1-bhanuka-samarasinghe.md](member-1-bhanuka-samarasinghe.md) |
| **Seneja Ramanayake** | Feature / ML Engineer | Feature engineering, preprocessing pipeline | Random Forest (+ Decision Tree) | Ensemble (bagging) / rule-based | [member-2-seneja-ramanayake.md](member-2-seneja-ramanayake.md) |
| **Jayashan Guruge** | ML Engineer | Advanced modeling, hyperparameter tuning, cross-validation | XGBoost / Gradient Boosting | Ensemble (boosting) | [member-3-jayashan-guruge.md](member-3-jayashan-guruge.md) |
| **Hasitha Erandika** | Validation, Evaluation & Decision Science Lead | Validation gate, unified evaluation, calibration, explainability, final recommendation | SVM (RBF kernel) + calibration/threshold ownership of the final selected model | Kernel method / validation & decision layer | [member-4-hasitha-erandika.md](member-4-hasitha-erandika.md) |

Dummy Classifier (naive baseline, category 1) is trained by Bhanuka alongside
Logistic Regression, since both are needed early to establish the comparison
floor — see `../05-modeling-strategy.md` §5.1 for the full category breakdown
(6 models across 5 categories + baseline).

## RACI matrix

R = Responsible, A = Accountable, C = Consulted, I = Informed

| Deliverable | Bhanuka | Seneja | Jayashan | Hasitha |
|---|---|---|---|---|
| Data ingestion & schema validation | **R/A** | I | I | C |
| Data-quality report & leakage discovery | **R/A** | C | I | C |
| EDA + EDA Insight Log | **R/A** | C | I | C |
| Feature engineering | C | **R/A** | I | C |
| Preprocessing pipeline (shared) | I | **R/A** | C | **A** (validation) |
| Feature Log | I | **R/A** | I | I |
| Logistic Regression model | **R/A** | I | I | C |
| Decision Tree model | C | **R/A** | I | C |
| Random Forest model | I | **R/A** | I | C |
| XGBoost model + tuning | I | C | **R/A** | C |
| SVM model + tuning | I | I | I | **R/A** |
| Leakage / validation gate | C | C | C | **R/A** |
| Unified evaluation framework | I | I | I | **R/A** |
| Calibration & threshold analysis | I | I | I | **R/A** |
| Explainability (SHAP / importances) | C | C | C | **R/A** |
| Final recommendation & limitations | C | C | C | **R/A** |
| `DECISIONS.md` (all entries) | R | R | R | **A** (maintains log integrity) |
| `PROGRESS.md` | R | R | R | **A** (keeps it current) |
| AI-use disclosure (own entries) | R | R | R | R |
| Final report assembly | C | C | C | **R/A** |

## Definition of Done — applies to every member

A workstream is not "done" until:
- [ ] The member has personally trained, tuned, and logged **at least one model**
      end-to-end into the shared evaluation table (§5.0 non-negotiable rule) —
      shared pipeline contributions alone do not satisfy this.
- [ ] It consumes the **shared** cleaned dataset / preprocessing pipeline, not a
      private copy.
- [ ] Reproducible: runs top-to-bottom with `RANDOM_STATE = 42` fixed.
- [ ] Test set was touched at most once, at the very end.
- [ ] Every non-trivial choice has a row in `../../DECISIONS.md`.
- [ ] Progress is reflected in `../../PROGRESS.md`.
- [ ] Any AI-tool usage for that workstream is logged in
      `../../ai-usage-disclosure/`.
- [ ] Peer-reviewed by at least one other member before being merged into the
      final report.
