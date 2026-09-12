# Member 2 — Seneja Ramanayake: Feature Engineering + Preprocessing

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

1. `src/features/engineering.py` — implements every engineered feature listed in
   [`../04-preprocessing-feature-engineering.md`](../04-preprocessing-feature-engineering.md)
   §4.5 (`total_nights`, `weekend_night_ratio`, `total_guests`,
   `prior_cancellation_rate`, `room_type_changed`, `arrival_season`, `is_family`),
   each as a small, named, testable function — not a single giant script.
2. `src/features/preprocessing.py` — the shared `ColumnTransformer` +
   `Pipeline`: one-hot for low-cardinality categoricals, frequency/top-N bucketing
   for `country`/`agent`/`company`, `StandardScaler` branch for linear models,
   pass-through branch for tree models (§4.7–§4.8).
3. **Feature Log** (table: feature name, original/engineered, type, treatment,
   reason) — append to `04-preprocessing-feature-engineering.md` or a dedicated
   section once the final feature set is locked; must match what's actually in
   the pipeline code, not an aspirational list.
4. Implement the **two leakage-timing variants** (day-zero vs. full-lifecycle,
   `../05-modeling-strategy.md` §5.3) as two `ColumnTransformer` configs sharing
   the same base logic.
5. `notebooks/02_feature_engineering.ipynb` — demonstrates the pipeline end to
   end, shows before/after feature distributions.
6. Decision Tree model (`src/models/decision_tree.py`) and Random Forest model
   (`src/models/random_forest.py`), both `class_weight="balanced"`, both trained
   through the shared pipeline — never a private copy of it.
7. Feature importance / permutation importance output from Random Forest, handed
   to Hasitha for the explainability section.

## Interfaces

- **From Bhanuka:** clean dataset + list of applied cleaning transformations.
- **To Jayashan and everyone else:** the fitted `ColumnTransformer` interface
  (`fit_transform` on train, `transform` on test only) — this is the single
  contract every model must go through. No one re-implements their own encoding.
- **To Hasitha:** Random Forest feature importances for the explainability
  section, plus confirmation that class-imbalance handling
  (`class_weight="balanced"`) was applied at training time, not via row
  duplication before the split (which would leak).

## Definition of Done

- [ ] `fit()` is called on the training split only, verified explicitly (not just
      assumed) — this is the single most-checked item at Hasitha's validation
      gate.
- [ ] Feature Log matches the actual pipeline code exactly.
- [ ] Both leakage-timing variants (day-zero / full-lifecycle) produce separate,
      clearly labelled outputs.
- [ ] Decision Tree and Random Forest logged into the shared evaluation table.
- [ ] AI tool usage logged in
      `../../ai-usage-disclosure/member-2-seneja-ramanayake.md`.
