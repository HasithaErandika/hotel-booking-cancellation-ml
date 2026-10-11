# 3. Data Understanding, EDA, and Data Quality Reasoning

*Rubric: 10 marks. Foundational Knowledge; Application | Data literacy; statistical reasoning*

All numbers on this page were computed directly from `data/hotel_bookings.csv`
(119,390 rows × 32 columns, SHA-256 `7c2ae42a...`, see
[`08-reproducibility.md`](08-reproducibility.md)), not copied from an external
description of the dataset. They are reproduced by notebooks 01 and 03 (§3.6); re-run
those notebooks if the data file changes.

## 3.1 What one row means

One row = one hotel booking record, for either the **Resort Hotel** or the
**City Hotel**, as it stood at the end of its lifecycle (`reservation_status`).
It is not one guest (a guest can book multiple times) and not one room-night.

## 3.2 Data dictionary

| Column | Type | Description | Notes |
|---|---|---|---|
| `hotel` | categorical | `Resort Hotel` / `City Hotel` | 2 categories, no missing |
| `is_canceled` | binary target | 1 = cancelled or no-show, 0 = completed | **target** |
| `lead_time` | numeric (int) | Days between booking date and arrival date | range 0–737 |
| `arrival_date_year` | numeric/categorical | 2015, 2016, 2017 | cancellation rate drifts upward by year (§3.5); excluded from features |
| `arrival_date_month` | categorical | January–December | |
| `arrival_date_week_number` | numeric | ISO week number of arrival | 1–53 |
| `arrival_date_day_of_month` | numeric | Day of month of arrival | 1–31 |
| `stays_in_weekend_nights` | numeric | # Saturday/Sunday nights booked | |
| `stays_in_week_nights` | numeric | # weekday nights booked | |
| `adults` | numeric | # adults on the booking | min 0, max 55 (see §3.4) |
| `children` | numeric | # children on the booking | 4 missing, invalid values present (see §3.4) |
| `babies` | numeric | # babies on the booking | max 10 (see §3.4) |
| `meal` | categorical | Meal plan (BB, HB, FB, SC, Undefined) | `Undefined` = unknown, treat as its own category |
| `country` | categorical | Guest country of origin, ISO 3166 code | 488 missing (0.41%), 178 distinct values, top = PRT (48,590) |
| `market_segment` | categorical | e.g. Online TA, Offline TA/TO, Groups, Direct, Corporate | 2 rows `Undefined` |
| `distribution_channel` | categorical | e.g. TA/TO, Direct, Corporate, GDS | 5 rows `Undefined` |
| `is_repeated_guest` | binary | 1 if guest booked before | see §3.5 for its relation to cancellation |
| `previous_cancellations` | numeric | # prior bookings by this guest that were cancelled | strong predictor, see §3.5 |
| `previous_bookings_not_canceled` | numeric | # prior bookings by this guest that were honoured | |
| `reserved_room_type` | categorical | Room type at booking time | anonymised codes (A, B, C, …) |
| `assigned_room_type` | categorical | Room type actually assigned | differs from reserved in 14,917 rows (12.49%) |
| `booking_changes` | numeric | # amendments made to the booking | max 21; accumulates after booking → full-lifecycle only |
| `deposit_type` | categorical | No Deposit / Non Refund / Refundable | see §3.5, strongest single association with cancellation |
| `agent` | categorical (ID) | Travel agent ID that made the booking | 16,340 missing (13.69%) |
| `company` | categorical (ID) | Company ID that made the booking | 112,593 missing (94.31%) |
| `days_in_waiting_list` | numeric | Days booking stayed on a waiting list before confirmation | max 391, non-zero in 3,698 rows; full-lifecycle only |
| `customer_type` | categorical | Transient, Transient-Party, Contract, Group | |
| `adr` | numeric | Average Daily Rate (revenue proxy) | contains 1 negative value and 1 extreme outlier, see §3.4 |
| `required_car_parking_spaces` | numeric | # parking spaces requested | **probably recorded at arrival**: 0 % cancellation when > 0 (§3.5); full-lifecycle variant only |
| `total_of_special_requests` | numeric | # special requests made | |
| `reservation_status` | categorical | Check-Out / Canceled / No-Show | **leakage, excluded from modeling, see §3.5** |
| `reservation_status_date` | date | Date the final status was set | **leakage, excluded from modeling, see §3.5** |

## 3.3 Target distribution and baseline

| `is_canceled` | Count | % |
|---|---:|---:|
| 0 (not cancelled) | 75,166 | 62.96% |
| 1 (cancelled/no-show) | 44,224 | 37.04% |

These are **raw** figures. More than a quarter of the raw rows are exact duplicates
(§3.4), and duplicates are disproportionately cancelled bookings. **After dropping the
leakage columns and de-duplicating** (notebook 01), the modelling dataset is:

| `is_canceled` (de-duplicated) | Count | % |
|---|---:|---:|
| 0 (not cancelled) | 63,371 | 72.72% |
| 1 (cancelled/no-show) | 23,767 | **27.28%** |
| Total | 87,138 | 100% |

This is a **moderate** imbalance (about 2.67 : 1), not severe. A model that always
predicts "not cancelled" reaches **72.72 % accuracy** on the modelling data while being
operationally useless. This is the naive baseline every real model must clearly beat
on precision/recall/PR-AUC for the cancelled class, not just accuracy (see
`06-evaluation-plan.md`). The PR-AUC of a no-skill model equals the prevalence, 0.273.
The 62.96 % figure that appeared in earlier drafts is the raw, pre-dedup baseline
(decision #25).

Cancellation rate by hotel (an early, important split):

| Hotel | Raw bookings | Raw rate | De-duplicated bookings | De-duplicated rate |
|---|---:|---:|---:|---:|
| City Hotel | 79,330 | 41.73% | 53,253 | 29.81% |
| Resort Hotel | 40,060 | 27.76% | 33,885 | 23.29% |

City Hotel bookings cancel at a materially higher rate in both views, so `hotel` is
retained as a feature. Notebook 03 shows the lead-time effect differs by hotel, which
favours interaction-capable models.

## 3.4 Data quality issues found, and how each affects the task

| Issue | Evidence | Effect on the task if ignored |
|---|---|---|
| **Exact duplicate rows** | 31,994 of 119,390 rows (26.8%) are byte-for-byte duplicates across all 32 columns. On the 30 *modelling* columns (leakage columns removed) the count is **32,252**, because some rows differ only in `reservation_status_date`. The pipeline de-duplicates on modelling columns (decision #21), leaving 87,138 rows. | If left in and split randomly into train/test, the *same* booking record can appear in both splits, inflating test performance and giving a false sense of generalisation. Must be deduplicated **before** the train/test split. |
| **Conflicting labels** | After de-duplication, **265** groups of rows have identical features but different `is_canceled` values. | Irreducible noise: no model can predict all of them correctly. They are kept and reported as a ceiling on achievable performance (decision #26), not deleted. |
| **Invalid `children` values** | 4 rows have `NaN`; 1 row has `children = 10` alongside `adults = 2, babies = 0` (a 12-person "booking" that is very likely a data-entry error). | Left uncorrected, a spurious extreme value can distort scaling and split points in tree models and skew engineered features like `total_guests`. |
| **Zero-guest bookings** | ~180 rows have `adults = 0`, `children = 0`, `babies = 0` simultaneously, a booking with nobody on it. | Not a plausible real booking; needs an explicit decision (flag, or treat as a data artefact) rather than silent inclusion, since it can't represent a real stay. |
| **Extreme `adults`** | `adults` ranges 0–55; 55 adults on one booking is implausible for the room types in this data. | Same risk as above, a small number of implausible extreme values can dominate the range used for scaling. |
| **Negative `adr`** | 1 row has `adr = -6.38`. | A negative daily rate is not a valid price; if untreated it corrupts any revenue-based feature or filter built on `adr`. |
| **Extreme `adr` outlier** | 1 row has `adr = 5,400` (City Hotel, 2 adults, 0 children, and this exact booking **was** cancelled). | A single point 27x the next-highest plausible values can dominate a linear model's coefficient for `adr` and distort scaling; must be investigated (error vs. genuine luxury booking) rather than blindly dropped, since it may carry real signal. |
| **Zero `adr`** | 1,959 rows have `adr = 0` (free stays, complementary bookings, or possible data issues). | Needs a decision: legitimate (e.g. `market_segment = Complementary`) vs. an error, affects whether `adr` is treated as fully continuous or needs a "free stay" flag. |
| **`Undefined` categories** | `meal` (1,169 rows), `market_segment` (2 rows), `distribution_channel` (5 rows) contain a literal `Undefined` category. | If silently merged into the mode or dropped, information about genuinely-unknown-channel bookings is lost; kept as its own category instead. |
| **High missingness in `agent` / `company`** | `agent` missing 13.69%; `company` missing 94.31%; 9,760 rows are missing **both**. | Missingness here plausibly means "no agent/company involved" (i.e. it is informative), not a random data-entry gap, deleting these rows would remove 94% of the dataset and destroy the ability to model direct/non-agency bookings at all. |
| **`reserved_room_type` ≠ `assigned_room_type`** | Differs in 14,917 rows (12.49%). | Room reassignment usually happens operationally close to arrival, so using `assigned_room_type` as a *predictive* (early) feature risks leaking near-outcome information; see leakage discussion below. |
| **Target leakage via `reservation_status`** | `reservation_status ∈ {Canceled, No-Show}` matches `is_canceled = 1` in **100%** of rows (0 mismatches, verified directly), and `reservation_status_date` is the date that status was recorded. | These two columns effectively **encode the label itself** (and its timing). Any model given these columns will trivially reach ~100% accuracy while learning nothing usable at the actual decision point (booking time). **Both columns are dropped before modeling**; this is the single most important data-quality finding in the project. |

## 3.5 Key EDA findings (business-relevant, verified against the data)

"Raw" = all 119,390 rows. "De-dup" = the 87,138-row modelling dataset. The
de-duplicated figures are the ones that describe what the models learn from. The
notebook-03 versions (Train split only, with 95 % Wilson intervals) are in
`reports/tables/eda_insight_log.csv` and `reports/tables/03_rate_by_*.csv`.

| Finding | Evidence (raw → de-dup) | Business meaning | Modeling implication |
|---|---|---|---|
| `deposit_type = Non Refund` bookings cancel almost always. | Raw: 14,494 of 14,587 (**99.36%**) vs 28.38% No Deposit. De-dup: only **1,017** Non-Refund rows remain, **94.59%** cancelled vs 26.48% No Deposit, i.e. ~93% of raw Non-Refund rows were duplicates. | A near-deterministic, heavily duplicated pattern points to a booking-channel/process artefact (e.g. bulk/agency bookings recorded as cancelled by convention), not a purely causal deposit effect. | Include `deposit_type`, but report this as a probable confound (decision #11), never as "non-refundable deposits cause cancellations". |
| Guests with `previous_cancellations > 0` cancel again far more often. | Raw: **91.64%** vs 33.91%. De-dup: **67.43%** (n = 1,661) vs 26.49%. | Past cancellation behaviour is highly predictive of future behaviour. | Include `previous_cancellations`; engineered `prior_cancellation_rate` (notebook 04). |
| Repeat guests cancel less. | Raw: **14.49%** vs 37.79%. De-dup: **7.62%** (n = 3,414) vs 28.08%. | Loyal/returning guests are lower risk. | Include `is_repeated_guest`. |
| City Hotel cancels more than Resort Hotel. | Raw 41.73% vs 27.76%; de-dup 29.81% vs 23.29% (§3.3). | Hotel-type-specific risk baseline. | Include `hotel`; consider hotel-specific thresholds (plan F-05). |
| Bookings with a parking request **never** cancel. | De-dup: `required_car_parking_spaces > 0` → **0 of 7,313** cancelled (0.00%) vs 29.77% otherwise. | Not a plausible behavioural effect. The field is very likely recorded at arrival (only guests who show up get a space). | **Leakage-timing suspect:** excluded from the *day-zero* variant, kept in full-lifecycle only (decision #22). |
| Portuguese (PRT) bookings cancel more often than all other countries. | De-dup: **35.29%** (n = 27,292) vs 23.62%. | Hypothesis: nationality may only be confirmed at check-in, so cancelled bookings keep a default home-country value. | Kept as a feature for now. Flagged for a with/without-`country` ablation (plan F-03) and checked in the fairness audit (notebook 13). |
| The cancellation rate drifts upward over time. | De-dup: 2015 **20.00%** → 2016 **26.23%** → 2017 **31.73%**. | Behaviour is non-stationary; a random split is optimistic for predicting the future. | `arrival_date_year` excluded from features (decision #23); temporal robustness check in notebook 14. |
| `agent`/`company` missingness is structural, not random (94.31% of `company` missing overall). | §3.4. | Most bookings are not company-billed. | Missing agent/company become explicit "No Agent"/"No Company" categories (decision #5). |

## 3.6 Reproducing this analysis

The raw-file statistics in §3.2–§3.4 were first produced with a plain Python
(`csv` + `collections`) profiling pass. They are now reproduced in pandas by
**`notebooks/01_data_ingestion_quality_cleaning.ipynb`**, whose reconciliation table
(`reports/tables/01_doc_reconciliation.csv`) compares every documented number with the
data. All 20 reconciled statistics matched on 2026-10-11. Target-relationship EDA is
in **`notebooks/03_exploratory_data_analysis.ipynb`** and runs on the **Train split
only**, to avoid tuning feature ideas to rows later used for evaluation. If a number
here ever disagrees with a notebook, trust the notebook, correct this file, and add a
[`DECISIONS.md`](DECISIONS.md) row explaining what changed and why.
