# Member 2 (Seneja Ramanayake): Feature Engineering + Preprocessing

Role: **Feature / ML Engineer**. Owns the shared feature and preprocessing layer
every model trains on. Also owns Model 2 (Random Forest) and the supporting
Decision Tree.

## Pipeline owned

```text
Clean dataset (from Bhanuka)
   → Feature engineering (total_nights, total_guests, prior_cancellation_rate, ...)
   → Categorical encoding (one-hot / frequency, per column cardinality)
   → Numerical scaling (for linear models only)
   → Train/test split (stratified, random_state=42)
   → Shared sklearn Pipeline + ColumnTransformer
   → Model-ready train/test matrices
```

## Deliverables

1. `notebooks/02_train_dev_test_split.ipynb`: the 70 / 15 / 15 stratified split
   (60,996 / 13,071 / 13,071 rows) with overlap checks and
   `artifacts/split_manifest.json`. **Done.**
2. `notebooks/04_feature_engineering_preprocessing.ipynb`: every engineered feature
   in [`../04-preprocessing-feature-engineering.md`](../04-preprocessing-feature-engineering.md)
   §4.5 as a small named function with unit tests; the two feature sets
   (`day_zero`, `full_lifecycle`); four unfitted preprocessing templates
   (`linear`/`tree` x 2 feature sets) built from sklearn parts only; the feature
   spec and the feature log. **Done.**
3. **Feature log** (`reports/tables/feature_log.csv`): generated from the feature
   spec, so it always matches the code. **Done.**
4. `notebooks/06_decision_tree.ipynb`: tuned Decision Tree plus a shallow 3-level
   tree with readable rules.
5. `notebooks/07_random_forest.ipynb`: tuned Random Forest plus impurity and
   permutation importance, used in notebook 13.

## Interfaces

- **From Bhanuka:** clean dataset + list of applied cleaning transformations.
- **To Jayashan and everyone else:** the fitted `ColumnTransformer` interface
  (`fit_transform` on train, `transform` on test only); this is the single
  contract every model must go through. No one re-implements their own encoding.
- **To Hasitha:** Random Forest feature importances for the explainability
  section, plus confirmation that class-imbalance handling
  (`class_weight="balanced"`) was applied at training time, not via row
  duplication before the split (which would leak).

## Definition of Done

- [ ] `fit()` is called on the Train split only. Notebook 04 §5.3 checks it, and the
      validation gate (notebook 10, check M3) checks it again.
- [ ] Feature Log matches the actual pipeline code exactly.
- [ ] Both leakage-timing variants (day-zero / full-lifecycle) produce separate,
      clearly labelled outputs.
- [ ] Decision Tree and Random Forest logged into the shared evaluation table.
- [ ] AI tool usage logged in
      `../../ai-usage-disclosure/member-2-seneja-ramanayake.md`.
