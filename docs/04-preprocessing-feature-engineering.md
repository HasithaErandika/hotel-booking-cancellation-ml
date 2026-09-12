# 4. Preprocessing and Feature-Engineering Decisions

*Rubric: 15 marks — Application | ML implementation; data reasoning*

Owner: Seneja Ramanayake (Member 2), consuming the cleaned dataset from Bhanuka
Samarasinghe (Member 1). Every decision below must also have a row in
[`../DECISIONS.md`](../DECISIONS.md).

## 4.1 Non-tabular features

This dataset is **fully tabular** — there is no free text, image, or time-series
sensor data. The only quasi-non-tabular fields are the date parts
(`arrival_date_year/month/week_number/day_of_month`), handled as engineered
calendar features in §4.5. No NLP/vision preprocessing is applicable here, and we
say so explicitly rather than silently skipping the rubric bullet.

## 4.2 Duplicates

- **Finding:** 31,994 of 119,390 rows (26.8%) are exact duplicates across all 32
  columns (see `03-data-understanding.md` §3.4).
- **Decision:** Drop exact duplicate rows, keeping the first occurrence, **before**
  the train/test split.
- **Why before the split:** if duplicates are removed after splitting, a duplicate
  pair can land one copy in train and one in test, letting the model "memorise" a
  test row it already saw in training — this would silently inflate every reported
  metric.

## 4.3 Missing values

| Column | Missing | Treatment | Reason |
|---|---:|---|---|
| `children` | 4 (0.00%) | Impute with 0 | Overwhelming majority of bookings have 0 children (110,796 of 119,390); a handful of missing values are almost certainly unrecorded-but-absent, not unknown. |
| `country` | 488 (0.41%) | Impute with an explicit `"Unknown"` category | Too small to drop meaningfully, but the true country is genuinely unknown — coding it as its own category is more honest than imputing a mode that would misrepresent 488 guests' origin. |
| `agent` | 16,340 (13.69%) | Impute with an explicit `"0"` / `"No Agent"` category, treat as categorical ID | Missing plausibly means "booking was not made through a travel agent," which is itself informative, not a random gap. |
| `company` | 112,593 (94.31%) | Impute with an explicit `"0"` / `"No Company"` category, treat as categorical ID | Same reasoning as `agent`; dropping the column or the rows would destroy 94% of the data and remove a real, if sparse, signal (company-billed bookings behave differently). |

We explicitly **reject** "drop all rows with any missing value," which would
discard effectively the whole dataset via `company` alone, and reject mean/mode
imputation for `agent`/`company`, since these are identifier-like categoricals
where a mean/mode has no meaningful interpretation.

## 4.4 Invalid / implausible values

| Issue | Decision | Reason |
|---|---|---|
| `children = 10` (1 row, with `adults = 2`) | Cap at a plausible maximum (e.g. treat as missing → impute 0, or cap at 3, the 99th-percentile-region value) rather than delete the row | A single implausible value shouldn't cost us a whole row of otherwise-valid information; capping bounds its influence on scaling without deleting data. |
| `adults = 0`, `children = 0`, `babies = 0` simultaneously (~180 rows) | Flag with a boolean `is_invalid_guest_count`, do not delete outright; investigate whether these correlate with a specific `market_segment`/`customer_type` before deciding to exclude from training | These may be corporate/placeholder bookings (e.g. `customer_type = Group`) rather than pure errors — decide from evidence, not assumption, and log the finding in `DECISIONS.md`. |
| `adr = -6.38` (1 row) | Correct to 0 or drop the single row | A negative price cannot be real; a single row has negligible impact on the training set either way. |
| `adr = 5,400` (1 row, City Hotel, cancelled) | Winsorize/cap at a high percentile (e.g. 99.5th) rather than delete, and note it explicitly in the EDA writeup | Retaining but capping preserves the "this was a high-value booking" signal without letting one point dominate scaling/coefficients; deleting would silently hide a legitimate (if rare) booking type. |
| `adr = 0` (1,959 rows) | Retain as-is; consider an `is_free_stay` flag if a later check shows it correlates with `market_segment = Complementary` | Likely legitimate complementary/comped stays, not necessarily errors. |
| `Undefined` in `meal`, `market_segment`, `distribution_channel` | Keep as its own explicit category (do not merge into mode) | `Undefined` may itself be predictive (e.g. bookings with genuinely unclear channel may behave differently) and merging would erase that signal. |

## 4.5 Feature engineering

| Feature | Formula | Rationale |
|---|---|---|
| `total_nights` | `stays_in_weekend_nights + stays_in_week_nights` | Total stay length is a more direct business quantity than the two separate counts, and reduces two correlated columns to one plus a ratio (see below). |
| `weekend_night_ratio` | `stays_in_weekend_nights / total_nights` (0 when `total_nights = 0`) | Captures leisure- vs. business-shaped stays without discarding the original weekend/week split entirely. |
| `total_guests` | `adults + children (imputed) + babies` | Single measure of party size; simplifies three sparsely-varying columns. |
| `total_previous_bookings` | `previous_cancellations + previous_bookings_not_canceled` | Denominator for a guest history rate feature. |
| `prior_cancellation_rate` | `previous_cancellations / total_previous_bookings`, defined as `0` when the denominator is `0` (no booking history) | Turns the two raw history counts into a single rate; §3.5 shows this history is one of the strongest signals in the data (91.64% vs 33.91% cancellation rate). |
| `room_type_changed` | `1` if `reserved_room_type != assigned_room_type` else `0` | Captures the 12.49% mismatch rate found in EDA as a single boolean rather than a 10+ level categorical interaction — **caveat:** see leakage note below. |
| `arrival_season` | Map `arrival_date_month` → {Winter, Spring, Summer, Autumn} | Reduces 12-level categorical to 4 levels while retaining seasonal signal; easier for tree splits and for a business audience to reason about. |
| `is_family` | `1` if `children > 0` or `babies > 0` | Simple, interpretable segment flag requested by revenue-management framing. |

## 4.6 Leakage prevention (the most important decision in this section)

**Dropped entirely, before any modeling:**
- `reservation_status` — encodes the final outcome (Check-Out / Canceled / No-Show),
  which matches `is_canceled` in 100% of rows. Including it would let a model reach
  near-perfect accuracy by reading the label back off a renamed copy of itself.
- `reservation_status_date` — the date the final status was recorded; only knowable
  at or after the outcome, never at booking time.

**Used with caution, documented, not dropped:**
- `assigned_room_type` — assignment can happen close to arrival (often at
  check-in), so using it to predict cancellation risk **at booking time** is
  optimistic. Decision: keep `reserved_room_type` (known at booking) as the primary
  room feature; keep the engineered `room_type_changed` boolean but treat it as an
  exploratory/explanatory feature rather than part of the "early-warning" model
  variant, and note this explicitly in the report rather than silently including it.
- `booking_changes`, `days_in_waiting_list` — both accumulate *after* the initial
  booking and could partially reflect information from later in the booking's life.
  Decision: retain them but flag in `DECISIONS.md` that a stricter "day-zero-only"
  model variant should exclude them, and compare the two variants' evaluation
  metrics side by side (see `06-evaluation-plan.md`) rather than assuming either
  choice is obviously correct.

## 4.7 Categorical encoding

- **Low-cardinality nominal** (`hotel`, `meal`, `market_segment`,
  `distribution_channel`, `deposit_type`, `customer_type`, `arrival_season`,
  `reserved_room_type`): **one-hot encoding**. Reason: no natural order exists, and
  one-hot avoids imposing a false ordinal relationship that label/ordinal encoding
  would create for linear models.
- **High-cardinality** (`country` — 178 levels, `agent`, `company` — many sparse
  IDs): frequency encoding or target-safe grouping (e.g. keep top-N countries by
  volume, bucket the rest as `"Other"`) rather than one-hot, to avoid an
  unmanageable number of sparse columns and to avoid target leakage from any
  target-mean encoding computed on the full dataset (if target encoding is used at
  all, it must be fit inside cross-validation folds only).

## 4.8 Scaling

- **Logistic Regression / SVM (distance- and gradient-based):** `StandardScaler`
  on numeric features, fit on the training split only.
- **Decision Tree / Random Forest / Gradient Boosting:** no scaling — tree splits
  are invariant to monotonic transformations of a single feature, so scaling adds
  complexity with no benefit.

## 4.9 Class imbalance (37.04% positive class)

- **Decision:** Do **not** apply aggressive resampling (e.g. full SMOTE
  oversampling to 50/50) as the default approach, because 37% is a moderate, not
  severe, imbalance.
- Instead: use **`class_weight="balanced"`** for Logistic Regression / Random
  Forest / Decision Tree, and **`scale_pos_weight`** for XGBoost, plus
  threshold tuning at evaluation time (`06-evaluation-plan.md`) as the primary
  levers.
- SMOTE is kept as a **documented alternative to compare against**, not the
  default, and if used must be applied only inside the training folds (never on
  the test set, and never before the split) to avoid synthetic leakage.

## 4.10 Train / Dev / Test split and leakage-safe order of operations

**Split ratio: 70% Train / 15% Dev / 15% Test**, stratified on `is_canceled`,
`random_state=42`. On the deduplicated dataset (~87,396 rows, after removing the
31,994 exact duplicates found in §4.2), this gives roughly:

| Split | Rows (≈) | Positives (≈37%) | Role |
|---|---:|---:|---|
| Train | 61,177 | 22,600 | Fit preprocessing; k-fold CV for model selection and hyperparameter search |
| Dev | 13,109 | 4,850 | Early stopping (XGBoost), threshold/calibration selection — touched repeatedly during development |
| Test | 13,110 | 4,850 | Final reported numbers only — touched exactly once, at the end |

15/15 (rather than 10/10) is chosen because 6 models are being compared and the
Dev set will be inspected repeatedly during tuning; the larger Dev slice reduces
the risk of quietly overfitting to it through repeated comparisons, at an
acceptable cost in training-set size given ~87K rows is not a data-constrained
regime.

**Order of operations (why it matters, not just what):**

```text
1. Load raw CSV
2. Drop reservation_status, reservation_status_date   (fixed rule — safe pre-split)
3. Drop exact duplicate rows                          (fixed rule — MUST be pre-split,
                                                        otherwise a duplicate pair can
                                                        land one copy in train, one in test)
4. Fix hard-coded invalid values (e.g. negative adr)  (fixed domain rule — safe pre-split)
5. SPLIT → Test (held out) + Train + Dev
6. Fit every statistics-dependent step on TRAIN ONLY:
      imputers, percentile-based outlier caps (winsorization thresholds),
      one-hot / frequency encoders, scalers, any target/mean encoding
7. .transform() (never .fit()) the same fitted pipeline onto Dev and Test
8. k-fold CV / hyperparameter search happens INSIDE Train only (§5.5)
9. Dev is used for early stopping, threshold selection, calibration checks
10. Test is scored exactly once, at the very end
```

The rule of thumb: if a preprocessing step needs to "look at" more than one row to
decide what to do (a mean, a percentile, a set of categories, a learned scale),
it must be fit after the split, on Train only. If it's a fixed rule that doesn't
depend on the data's distribution (drop a column, clip a value below 0), it's
safe before the split.

**Known residual leakage risk:** the dataset has no guest identifier, so a
returning guest's multiple bookings cannot be grouped into the same split. This
is recorded as a limitation (`07-recommendation-limitations.md`) rather than
silently ignored. A secondary, optional robustness check is a **time-based split**
(train on `arrival_date_year` 2015-2016, test on 2017) to simulate real
deployment (predicting the future from the past) instead of a random split —
worth running once as a sanity check on the final model, even though the primary
reported split is the random stratified 70/15/15 above.

## 4.11 Definition of done for this pipeline

- [ ] Runs as a single `sklearn.Pipeline` + `ColumnTransformer`, importable from
      `src/features/preprocessing.py`.
- [ ] Fit only ever called on the training split.
- [ ] Every decision in this file has a matching row in `DECISIONS.md`.
- [ ] Feature list and treatment logged in a Feature Log table (append to this file
      or `DECISIONS.md` once final feature set is locked).
- [ ] No leakage columns (`reservation_status`, `reservation_status_date`) reach
      the model — enforced by an explicit assertion/test in code, not just this doc.
