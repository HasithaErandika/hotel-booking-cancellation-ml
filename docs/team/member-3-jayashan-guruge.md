# Member 3 (Jayashan Guruge): Advanced Modeling (XGBoost)

Role: **ML Engineer, advanced modeling**. Owns the project's highest-performance
model and its tuning process, built strictly on top of Seneja's shared
preprocessing pipeline; never a private feature set.

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

1. `notebooks/08_xgboost_tuning.ipynb`: XGBoost trained through the shared tree
   preprocessing template, with `scale_pos_weight` (about 2.67, from the 27% / 73%
   class balance, `../04-preprocessing-feature-engineering.md` §4.9).
2. Randomised search (50 candidates) over `learning_rate`, `max_depth`,
   `n_estimators`, `subsample`, `colsample_bytree`, `min_child_weight` and
   regularisation, inside `StratifiedKFold(5, random_state=42)` on Train only,
   scored on PR-AUC (not accuracy, see `../06-evaluation-plan.md` §6.1).
3. The distribution of CV scores across all candidates, not just the best one.
4. Final refit with early stopping on Dev, for both feature sets (day-zero and
   full-lifecycle).
5. Gain-based feature importance and false positive / false negative examples,
   used in notebook 13.
6. `notebooks/11_model_evaluation_comparison.ipynb`: one metric function for every
   eligible model, CV mean ± SD table, Dev bootstrap confidence intervals, corrected
   t-test, day-zero vs full-lifecycle comparison and the written selection rule
   (`artifacts/model_selection.json`).

## Interfaces

- **From Seneja:** the fitted preprocessing pipeline; fit **only** on training
  data; never re-fit it yourself even if it seems convenient for a particular
  experiment.
- **To Hasitha:** the model card in `artifacts/model_outputs/xgboost__*/`
  (fitted pipeline in `models/`, CV fold scores and Dev predictions), the hyperparameter search results, and
  confirmation of which random seed was used throughout.

## Definition of Done

- [x] Hyperparameter search is provably CV-only (test set never scored during
      search; verify by checking the search object was never given test data).
- [x] Both leakage-timing variants trained and reported separately.
- [x] Final model + probabilities handed to Hasitha in the exact interface the
      evaluation framework expects (see `../06-evaluation-plan.md`).
- [x] Logged into the shared evaluation comparison table.
- [ ] AI tool usage logged in `../../ai-usage-disclosure/member-3-jayashan-guruge.md`.
