# Member 3 — Jayashan Guruge: Advanced Modeling (XGBoost)

Role: **ML Engineer, advanced modeling**. Owns the project's highest-performance
model and its tuning process, built strictly on top of Seneja's shared
preprocessing pipeline — never a private feature set.

## Pipeline owned

```text
Shared preprocessed train/test matrices (from Seneja)
   → Baseline XGBoost fit
   → RandomizedSearchCV / GridSearchCV (inside stratified 5-fold CV, train split only)
   → Best hyperparameters
   → Final fit on full training split
   → Predictions + probabilities handed to Hasitha's evaluation framework
```

## Deliverables

1. `src/models/xgboost_model.py` — training function that accepts the shared
   pipeline's output, uses `scale_pos_weight` for the 63/37 imbalance
   (`../04-preprocessing-feature-engineering.md` §4.9), and exposes a consistent
   `predict_proba`-based interface matching every other model in `src/models/`.
2. Hyperparameter search over at least: `learning_rate`, `max_depth`,
   `n_estimators`, `subsample`, `colsample_bytree`, `min_child_weight` —
   `RandomizedSearchCV` with `cv=StratifiedKFold(5, random_state=42)`, scored on
   PR-AUC or F1 (not accuracy — see `../06-evaluation-plan.md` §6.1), **never**
   touching the held-out test set.
3. `notebooks/03_xgboost_tuning.ipynb` — shows the search space, best parameters
   found, and CV score distribution (not just the single best point estimate).
4. Both leakage-timing variants (day-zero / full-lifecycle) trained and compared
   — a core input to the §5.3 decision about which variant the team recommends.
5. XGBoost feature importance (gain-based) as one input to Hasitha's
   explainability section (alongside SHAP, which Hasitha computes centrally so
   all models are explained the same way).
6. Error analysis input: false positive / false negative examples from XGBoost
   specifically, to compare against Random Forest's error profile.

## Interfaces

- **From Seneja:** the fitted preprocessing pipeline — fit **only** on training
  data — never re-fit it yourself even if it seems convenient for a particular
  experiment.
- **To Hasitha:** trained model object (or serialized `.pkl`), predicted
  probabilities on train/CV/test, the hyperparameter search results, and
  confirmation of which random seed was used throughout.

## Definition of Done

- [ ] Hyperparameter search is provably CV-only (test set never scored during
      search — verify by checking the search object was never given test data).
- [ ] Both leakage-timing variants trained and reported separately.
- [ ] Final model + probabilities handed to Hasitha in the exact interface the
      evaluation framework expects (see `../06-evaluation-plan.md`).
- [ ] Logged into the shared evaluation comparison table.
- [ ] AI tool usage logged in `../../ai-usage-disclosure/member-3-jayashan-guruge.md`.
