# 4. Preprocessing and Feature-Engineering Decisions

*Rubric: 15 marks. Application | ML implementation; data reasoning*

Owner: Seneja Ramanayake (Member 2), consuming the cleaned dataset from Bhanuka
Samarasinghe (Member 1). Every decision below must also have a row in
[`DECISIONS.md`](DECISIONS.md).

| Where it is implemented | What |
|---|---|
| `notebooks/01_data_ingestion_quality_cleaning.ipynb` | Fixed-rule cleaning (§4.2–§4.4), safe before the split |
| `notebooks/02_train_dev_test_split.ipynb` | 70 / 15 / 15 stratified split (§4.10) |
| `notebooks/04_feature_engineering_preprocessing.ipynb` | Stateless feature engineering (§4.5), feature spec and variants (§4.6), learned preprocessing templates (§4.7–§4.8), Feature Log (§4.12), statistical feature screening (§4.13) |

## 4.1 Non-tabular features

This dataset is **fully tabular**. There is no free text, image, or time-series
sensor data. The only quasi-non-tabular fields are the date parts
(`arrival_date_year/month/week_number/day_of_month`), handled as calendar features in
§4.5–§4.6. No NLP/vision preprocessing applies here, and we say so explicitly rather
than silently skipping the rubric bullet.

## 4.2 Duplicates

- **Finding:** 31,994 of 119,390 rows (26.8%) are exact duplicates across all 32
  columns. On the 30 modelling columns (after dropping the two leakage columns) the
  count is **32,252**, because some rows differ only in `reservation_status_date`
  (see `03-data-understanding.md` §3.4).
- **Decision:** Drop the leakage columns first, then drop exact duplicates on the
  modelling columns, keeping the first occurrence, **before** the split (decisions #4,
  #21). Result: **87,138 rows**, of which 27.28% are cancelled.
- **Why before the split:** if duplicates are removed after splitting, a duplicate
  pair can land one copy in Train and one in Test, letting the model "memorise" a
  test row it already saw in training. This would silently inflate every reported
  metric. Notebooks 02 and 10 verify that no identical row content appears in two splits.

## 4.3 Missing values

All four treatments are **fixed rules** (constants, not statistics), so they are
applied in notebook 01 before the split.

| Column | Missing | Treatment | Reason |
|---|---:|---|---|
| `children` | 4 (0.00%) | Impute with 0 | The overwhelming majority of bookings have 0 children (110,796 of 119,390); a handful of missing values are almost certainly unrecorded-but-absent, not unknown. |
| `country` | 488 (0.41%) | Explicit `"Unknown"` category | Too few to matter for dropping, but the true country is genuinely unknown. Coding it as its own category is more honest than imputing a mode that would misrepresent 488 guests' origin. |
| `agent` | 16,340 (13.69%) | Explicit `"No Agent"` category; IDs stored as strings (`"9"`, not `9.0`) | Missing plausibly means "booking was not made through a travel agent", which is itself informative, not a random gap. |
| `company` | 112,593 (94.31%) | Explicit `"No Company"` category; IDs stored as strings | Same reasoning as `agent`. Dropping the column or the rows would destroy 94% of the data and remove a real, if sparse, signal. |

Placeholder labels deliberately avoid strings pandas reads as missing by default
(`"None"`, `"NA"`, `"NULL"`), so the categories survive a CSV round-trip. Every
notebook also reads CSVs with an explicit dtype map.

We explicitly **reject** "drop all rows with any missing value", which would
discard effectively the whole dataset via `company` alone. We also reject mean/mode
imputation for `agent`/`company`, since these are identifier-like categoricals where
a mean or mode has no meaningful interpretation. The preprocessing templates still
contain `SimpleImputer` steps as a safety net for unseen data.

## 4.4 Invalid / implausible values

| Issue | Decision (implemented) | Reason |
|---|---|---|
| `children = 10` (1 row, with `adults = 2`) | Cap `children` at **3** (fixed domain constant, notebook 01) | A single implausible value shouldn't cost a whole row of otherwise-valid information; capping bounds its influence without deleting data. |
| `adults = 0`, `children = 0`, `babies = 0` (166 rows after dedup) | Keep; flag with engineered `is_invalid_guest_count` (notebook 04). Notebook 01 profiles which segments they come from. | These may be corporate/placeholder bookings rather than pure errors. Flagging lets the model use (or ignore) the pattern instead of hiding it. |
| `adr = -6.38` (1 row) | Set to **0** (fixed rule, notebook 01) | A negative price cannot be real; a single row has negligible impact. |
| `adr = 5,400` (1 row, City Hotel, cancelled) | Winsorise at the **99.5th percentile learned on Train** (= 283.68), inside the preprocessing pipeline | Keeps the "high-value booking" signal without letting one point dominate scaling or coefficients. The cap is learned after the split, so it cannot leak Dev/Test information. |
| `adr = 0` (1,959 raw / 1,779 de-dup rows) | Retain as-is | Likely legitimate complementary or comped stays, not errors. |
| `Undefined` in `meal`, `market_segment`, `distribution_channel` | Keep as its own explicit category (do not merge into the mode) | `Undefined` may itself be predictive, and merging would erase that signal. |
| 265 feature-identical groups with conflicting labels | Keep (decision #26) | Genuine ambiguity; removing it would overstate achievable accuracy. |

## 4.5 Feature engineering

All engineered features are **stateless, row-wise formulas**: no statistic from other
rows is used, so they cannot leak information between splits. Each is a small named
function in notebook 04, covered by unit checks on hand-built edge cases (zero-night
stays, no history, zero guests, room changes).

| Feature | Formula | Rationale |
|---|---|---|
| `total_nights` | `stays_in_weekend_nights + stays_in_week_nights` | Total stay length as one business quantity. |
| `weekend_night_ratio` | `stays_in_weekend_nights / total_nights` (0 when `total_nights = 0`) | Captures leisure- vs business-shaped stays. |
| `total_guests` | `adults + children + babies` | Single measure of party size. |
| `is_family` | `1` if `children > 0` or `babies > 0` | Interpretable segment flag requested by the revenue-management framing. |
| `is_invalid_guest_count` | `1` if `total_guests == 0` | Flags zero-guest bookings instead of deleting them (§4.4). |
| `total_previous_bookings` | `previous_cancellations + previous_bookings_not_canceled` | Denominator for the guest-history rate. |
| `prior_cancellation_rate` | `previous_cancellations / total_previous_bookings`, `0` when there is no history | One of the strongest signals in the data (§3.5 of doc 03). |
| `arrival_season` | `arrival_date_month` → {Winter, Spring, Summer, Autumn} | Reduces 12 levels to 4 while keeping seasonal signal. |
| `room_type_changed` | `1` if `reserved_room_type != assigned_room_type` | Captures the 12.49% re-assignment rate as one boolean. **Full-lifecycle only** (§4.6). |

## 4.6 Leakage prevention and the two model variants (the most important decision in this section)

**Dropped entirely, before any modeling (notebook 01):**
- `reservation_status` encodes the final outcome (Check-Out / Canceled / No-Show) and
  matches `is_canceled` in 100% of rows.
- `reservation_status_date` is the date the final status was recorded; it is only
  knowable at or after the outcome.

**Excluded from features (notebook 04):**
- `arrival_date_year`. The cancellation rate drifts from 20.0% (2015) to 31.7% (2017),
  and a model cannot extrapolate a year it has never seen (decision #23). The temporal
  effect is tested in notebook 14 instead.
- `arrival_date_month`, replaced by `arrival_season` + `arrival_date_week_number`.

**Post-booking fields: full-lifecycle variant only (decisions #6, #12, #22):**

| Field | Why it is not known at booking time |
|---|---|
| `booking_changes` | Accumulates over the booking's life |
| `days_in_waiting_list` | Accumulates before confirmation |
| `required_car_parking_spaces` | 0 of 7,313 bookings with a request cancelled, which suggests it is recorded at arrival |
| `assigned_room_type`, `room_type_changed` | Room assignment usually happens close to, or at, check-in |

| Variant | Contents | Use |
|---|---|---|
| **`day_zero`** | Everything known when the booking is created | The deployable early-warning model, preferred for the recommendation |
| **`full_lifecycle`** | `day_zero` + the post-booking fields above | A "re-score later in the booking's life" model; quantifies how much signal comes from post-booking events |

Both variants are defined **once** in `artifacts/feature_spec.json`, and assertions
in notebook 04 check that every column has exactly one role. This is how the legacy
bug where `room_type_changed` was silently dropped was found and fixed (plan I-04).
The validation gate (notebook 10) checks that each fitted model consumes exactly the
columns of its declared variant.

## 4.7 Categorical encoding

- **Low-cardinality nominal** (`hotel`, `meal`, `market_segment`,
  `distribution_channel`, `deposit_type`, `customer_type`, `arrival_season`,
  `reserved_room_type`, plus `assigned_room_type` in full-lifecycle): **one-hot
  encoding** with `handle_unknown="ignore"`. No natural order exists, and one-hot
  avoids imposing a false ordinal relationship on linear models.
- **High-cardinality** (`country`, `agent`, `company`): **top-10 one-hot** with
  `OneHotEncoder(max_categories=11, handle_unknown="infrequent_if_exist")`. The 10 most
  frequent Train levels get their own column; rare and unseen levels share one
  "infrequent" column. This avoids hundreds of sparse columns and any target leakage
  from mean encoding. Target encoding remains a possible future alternative, and would
  have to be fitted inside CV folds (plan F-06).

## 4.8 Scaling

Two preprocessing **families**, built from sklearn-native components only so they
pickle and load in any notebook:

| Family | Models | Numeric treatment |
|---|---|---|
| `linear` | Dummy, Logistic Regression, SVM | median impute → `StandardScaler` (fitted on Train only) |
| `tree` | Decision Tree, Random Forest, XGBoost | median impute only; tree splits are invariant to monotonic scaling |

`adr` gets its own branch in both families: median impute → winsorise at the
Train-fitted cap → (scale, linear family only).

After preprocessing, each model gets **94 input columns** (day-zero) or **109**
(full-lifecycle), the same for both families (notebook 04 §5.2). Dev has category
levels Train never saw (rare countries, agents and companies). They go into the
"infrequent" column without errors (notebook 04 §5.4).

## 4.9 Class imbalance (27.28% positive class after de-duplication)

- **Decision:** No aggressive resampling (e.g. SMOTE to 50/50) by default. 27% is a
  moderate imbalance (≈ 2.67 : 1), and weighting is leakage-safe by construction.
- Instead: **`class_weight="balanced"`** for Logistic Regression, Decision Tree,
  Random Forest and SVM, and **`scale_pos_weight`** for XGBoost. The Train neg/pos
  ratio is 2.666; it is searched against 1.0 rather than fixed. Threshold tuning at
  evaluation time (`06-evaluation-plan.md` §6.5) is the other main lever.
- Evidence rather than assumption: the Logistic Regression grid in notebook 05
  compares `class_weight="balanced"` against `None`.
- **Result:** when given the choice, the searches did not pick weighting. Logistic
  Regression chose `class_weight=None` and XGBoost chose `scale_pos_weight=1`. Decision
  Tree, Random Forest (`balanced_subsample`) and SVM kept weighting. The imbalance is
  then handled by the calibrated 0.35 threshold in notebook 12, not by 0.5 on
  re-weighted scores.
- SMOTE remains a **documented alternative**. If ever used, it must be applied only
  inside training folds (via an `imblearn` pipeline), never before the split. The
  validation gate checks that each model was fitted on exactly the Train row count,
  which would expose resampling done outside the pipeline.

## 4.10 Train / Dev / Test split and leakage-safe order of operations

**Split ratio: 70% Train / 15% Dev / 15% Test**, stratified on `is_canceled`,
`random_state=42` (notebook 02). On the 87,138-row de-duplicated dataset:

| Split | Rows | Cancelled | Role |
|---|---:|---:|---|
| Train | 60,996 | 16,637 (27.28%) | Fit preprocessing; 5-fold CV for model selection and hyperparameter search |
| Dev | 13,071 | 3,565 (27.27%) | Early stopping (XGBoost), calibration, threshold selection, error and fairness analysis; touched repeatedly during development |
| Test | 13,071 | 3,565 (27.27%) | Final reported numbers only; read exactly once, by notebook 14 |

15/15 (rather than 10/10) is chosen because 6 models are compared and Dev is
inspected repeatedly; the larger Dev slice reduces the risk of quietly overfitting
to it, at an acceptable cost in training-set size.

**Order of operations (why it matters, not just what):**

```text
1. Load raw CSV, verify SHA-256                              (notebook 01)
2. Drop reservation_status, reservation_status_date           (fixed rule, safe pre-split)
3. Drop exact duplicate rows                                  (fixed rule, MUST be pre-split)
4. Fix hard-coded invalid values (negative adr, children)     (fixed domain rules)
5. Encode structural missingness (No Agent / No Company / Unknown)
6. SPLIT → Train + Dev + Test                                 (notebook 02)
7. Stateless feature engineering, identical per split         (notebook 04)
8. Fit every statistics-dependent step on TRAIN ONLY, inside a Pipeline:
      imputers, ADR winsorisation cap, one-hot / top-N encoders, scalers
9. .transform() (never .fit()) the fitted pipeline onto Dev and Test
10. k-fold CV / hyperparameter search happens INSIDE Train only  (notebooks 05-09)
11. Dev: early stopping, calibration, threshold selection      (notebooks 08, 12)
12. Test is scored exactly once, at the very end              (notebook 14)
```

The rule of thumb: if a preprocessing step needs to "look at" more than one row to
decide what to do (a mean, a percentile, a set of categories, a learned scale), it
must be fitted after the split, on Train only. If it is a fixed rule that doesn't
depend on the data's distribution (drop a column, clip a value below 0), it is safe
before the split.

**Known residual leakage risks (documented, not ignored):**
- The dataset has no guest identifier, so a returning guest's bookings cannot be kept
  in the same split. This is recorded as a limitation in `07-recommendation-limitations.md`.
- The ADR cap is learned once on all of Train, so the CV folds inside Train share it.
  One quantile over ~61K rows has a negligible effect (plan I-19).
- `country` may be partly recorded at check-in (doc 03 §3.5). It is kept for now, with
  an ablation planned (plan F-03).
- A **time-based check** (train on 2015–2016 arrivals, test on 2017) runs in notebook 14
  as a robustness signal alongside the primary random split.

## 4.11 Definition of done for this pipeline

- [x] Implemented as sklearn `Pipeline` + `ColumnTransformer` templates saved by
      notebook 04 (`artifacts/preprocessors/preprocessor__{linear,tree}__{day_zero,full_lifecycle}.joblib`),
      verified by a joblib round-trip test.
- [x] Fit only ever called on the Train split, checked in notebook 04
      (`n_samples_seen_`) and independently in the validation gate (notebook 10).
- [x] No leakage columns (`reservation_status`, `reservation_status_date`) reach the
      model, enforced by assertions in notebooks 01, 02, 04 and 10.
- [x] Both variants defined in `artifacts/feature_spec.json` and produce separate, labelled models.
- [ ] Every decision in this file has a matching row in `DECISIONS.md` (#21–#23 added 2026-10-11; review as a team).
- [ ] Feature Log (§4.12) reviewed against the generated `reports/tables/feature_log.csv` after the first full run.

## 4.12 Feature Log

The authoritative Feature Log is **generated from the code** by notebook 04
(`reports/tables/feature_log.csv`), so it cannot drift from the pipeline. Summary:

| Feature group | Columns | Linear treatment | Tree treatment | Day-zero | Full-lifecycle |
|---|---|---|---|:-:|:-:|
| Numeric core | lead_time, arrival_date_week_number, arrival_date_day_of_month, stays_in_weekend_nights, stays_in_week_nights, adults, children, babies, is_repeated_guest, previous_cancellations, previous_bookings_not_canceled, total_of_special_requests | median impute + standardise | median impute | ✓ | ✓ |
| Engineered | total_nights, weekend_night_ratio, total_guests, is_family, is_invalid_guest_count, total_previous_bookings, prior_cancellation_rate | median impute + standardise | median impute | ✓ | ✓ |
| Price | adr | impute + Train-fitted 99.5% cap + standardise | impute + cap | ✓ | ✓ |
| Low-cardinality categorical | hotel, meal, market_segment, distribution_channel, deposit_type, customer_type, arrival_season, reserved_room_type | one-hot | one-hot | ✓ | ✓ |
| High-cardinality categorical | country, agent, company | top-10 one-hot + infrequent | top-10 one-hot + infrequent | ✓ | ✓ |
| Post-booking numeric | booking_changes, days_in_waiting_list, required_car_parking_spaces, room_type_changed | median impute + standardise | median impute | ✗ | ✓ |
| Post-booking categorical | assigned_room_type | one-hot | one-hot | ✗ | ✓ |
| Excluded | booking_id, is_canceled, arrival_date_year, arrival_date_month, reservation_status, reservation_status_date | - | - | ✗ | ✗ |

## 4.13 Feature selection: statistical screening

Features were selected in two steps.

1. **Timing and leakage rules (decide the spec).** Leakage columns are removed
   (decisions #3, #20), post-booking fields go to the full-lifecycle variant only
   (#6, #12, #22), and `arrival_date_year` is excluded because of drift (#23).
2. **Statistical screening (evidence for the spec).** Notebook 04 §4.4 tests every
   candidate input on Train only:
   - numeric inputs: Mann-Whitney U test with rank-biserial effect size;
   - categorical inputs: chi-square test with bias-corrected Cramér's V;
   - Benjamini-Hochberg correction across all tests;
   - mutual information on raw and engineered inputs;
   - variance inflation factor (VIF) and exact-sum checks on the linear inputs.

   With about 61,000 rows nearly every test is significant, so decisions use the
   effect size (weak = below 0.05). Results: `reports/tables/04_feature_screening.csv`
   and `reports/figures/04_feature_screening.png`.

**Redundancy found.** `total_nights`, `total_guests` and `total_previous_bookings` are
exact sums of other inputs (infinite VIF). Tree models are not affected. For Logistic
Regression the odds ratios of these columns cannot be read one by one, so notebook 05
§6 refits it without the raw parts and with an L1 penalty
(`reports/tables/05_sensitivity_checks.csv`). The spec itself is unchanged: changing it
would change the feature files behind the locked Test result (decision #31).

**Results.** 36 of 38 candidates are significant after correction. The two that are
not, `arrival_date_week_number` and `arrival_date_day_of_month`, are calendar fields
with a seasonal pattern that a shift test cannot see; XGBoost uses both (permutation
importance ranks 10 and 11), so they are kept. Logistic Regression without the raw
parts of the sums scores the same CV PR-AUC (0.6506 vs 0.6507), and with an L1 penalty
0.6501 (33 encoded inputs set to zero), so the reduced model's odds ratios
(`reports/tables/05_logreg_reduced_odds_ratios.csv`) are the ones to quote: for example
`prior_cancellation_rate` OR 1.76 per SD and `total_of_special_requests` OR 0.54 per SD.

