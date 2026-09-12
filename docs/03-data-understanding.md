# 3. Data Understanding, EDA, and Data Quality Reasoning

*Rubric: 10 marks — Foundational Knowledge; Application | Data literacy; statistical reasoning*

All numbers on this page were computed directly from `data/hotel_bookings.csv`
(119,390 rows × 32 columns, SHA-256 `7c2ae42a...`, see
[`08-reproducibility.md`](08-reproducibility.md)) — not copied from an external
description of the dataset. Regenerate them with the profiling script referenced in
§3.6 if the data file changes.

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
| `arrival_date_year` | numeric/categorical | 2015, 2016, 2017 | |
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
| `booking_changes` | numeric | # amendments made to the booking | max 21 |
| `deposit_type` | categorical | No Deposit / Non Refund / Refundable | see §3.5 — strongest single association with cancellation |
| `agent` | categorical (ID) | Travel agent ID that made the booking | 16,340 missing (13.69%) |
| `company` | categorical (ID) | Company ID that made the booking | 112,593 missing (94.31%) |
| `days_in_waiting_list` | numeric | Days booking stayed on a waiting list before confirmation | max 391, non-zero in 3,698 rows |
| `customer_type` | categorical | Transient, Transient-Party, Contract, Group | |
| `adr` | numeric | Average Daily Rate (revenue proxy) | contains 1 negative value and 1 extreme outlier, see §3.4 |
| `required_car_parking_spaces` | numeric | # parking spaces requested | |
| `total_of_special_requests` | numeric | # special requests made | |
| `reservation_status` | categorical | Check-Out / Canceled / No-Show | **leakage — excluded from modeling, see §3.5** |
| `reservation_status_date` | date | Date the final status was set | **leakage — excluded from modeling, see §3.5** |

## 3.3 Target distribution and baseline

| `is_canceled` | Count | % |
|---|---:|---:|
| 0 (not cancelled) | 75,166 | 62.96% |
| 1 (cancelled/no-show) | 44,224 | 37.04% |

This is a **moderate** imbalance (roughly 1.7 : 1), not severe. A model that always
predicts "not cancelled" reaches 62.96% accuracy while being operationally useless
— this is the naive baseline that every real model must clearly beat on
precision/recall for the cancelled class, not just accuracy (see
`06-evaluation-plan.md`).

Cancellation rate by hotel (an early, important split):

| Hotel | Bookings | Cancellation rate |
|---|---:|---:|
| City Hotel | 79,330 | 41.73% |
| Resort Hotel | 40,060 | 27.76% |

City Hotel bookings cancel at a materially higher rate — `hotel` is retained as a
feature and interactions with hotel type are worth checking during modeling.

## 3.4 Data quality issues found, and how each affects the task

| Issue | Evidence | Effect on the task if ignored |
|---|---|---|
| **Exact duplicate rows** | 31,994 of 119,390 rows (26.8%) are byte-for-byte duplicates across all 32 columns. | If left in and split randomly into train/test, the *same* booking record can appear in both splits, inflating test performance and giving a false sense of generalisation. Must be deduplicated **before** the train/test split. |
| **Invalid `children` values** | 4 rows have `NaN`; 1 row has `children = 10` alongside `adults = 2, babies = 0` (a 12-person "booking" that is very likely a data-entry error). | Left uncorrected, a spurious extreme value can distort scaling and split points in tree models and skew engineered features like `total_guests`. |
| **Zero-guest bookings** | ~180 rows have `adults = 0`, `children = 0`, `babies = 0` simultaneously — a booking with nobody on it. | Not a plausible real booking; needs an explicit decision (flag, or treat as a data artefact) rather than silent inclusion, since it can't represent a real stay. |
| **Extreme `adults`** | `adults` ranges 0–55; 55 adults on one booking is implausible for the room types in this data. | Same risk as above — a small number of implausible extreme values can dominate the range used for scaling. |
| **Negative `adr`** | 1 row has `adr = -6.38`. | A negative daily rate is not a valid price; if untreated it corrupts any revenue-based feature or filter built on `adr`. |
| **Extreme `adr` outlier** | 1 row has `adr = 5,400` (City Hotel, 2 adults, 0 children — and this exact booking **was** cancelled). | A single point 27x the next-highest plausible values can dominate a linear model's coefficient for `adr` and distort scaling; must be investigated (error vs. genuine luxury booking) rather than blindly dropped, since it may carry real signal. |
| **Zero `adr`** | 1,959 rows have `adr = 0` (free stays, complementary bookings, or possible data issues). | Needs a decision: legitimate (e.g. `market_segment = Complementary`) vs. an error — affects whether `adr` is treated as fully continuous or needs a "free stay" flag. |
| **`Undefined` categories** | `meal` (1,169 rows), `market_segment` (2 rows), `distribution_channel` (5 rows) contain a literal `Undefined` category. | If silently merged into the mode or dropped, information about genuinely-unknown-channel bookings is lost; kept as its own category instead. |
| **High missingness in `agent` / `company`** | `agent` missing 13.69%; `company` missing 94.31%; 9,760 rows are missing **both**. | Missingness here plausibly means "no agent/company involved" (i.e. it is informative), not a random data-entry gap — deleting these rows would remove 94% of the dataset and destroy the ability to model direct/non-agency bookings at all. |
| **`reserved_room_type` ≠ `assigned_room_type`** | Differs in 14,917 rows (12.49%). | Room reassignment usually happens operationally close to arrival — using `assigned_room_type` as a *predictive* (early) feature risks leaking near-outcome information; see leakage discussion below. |
| **Target leakage via `reservation_status`** | `reservation_status ∈ {Canceled, No-Show}` matches `is_canceled = 1` in **100%** of rows (0 mismatches, verified directly), and `reservation_status_date` is the date that status was recorded. | These two columns effectively **encode the label itself** (and its timing). Any model given these columns will trivially reach ~100% accuracy while learning nothing usable at the actual decision point (booking time). **Both columns are dropped before modeling** — this is the single most important data-quality finding in the project. |

## 3.5 Key EDA findings (business-relevant, verified against the data)

| Finding | Evidence | Business meaning | Modeling implication |
|---|---|---|---|
| `deposit_type = Non Refund` bookings cancel at **99.36%** vs. 28.38% for `No Deposit` and 22.22% for `Refundable`. | Direct group-by on 14,587 Non-Refund bookings. | This is a very strong, almost deterministic association — worth flagging as a possible data/process artefact (e.g. these may be bulk/agency bookings recorded as cancelled by convention) rather than a purely causal deposit effect. | Include `deposit_type`, but call out this anomaly explicitly in the report rather than presenting it as a simple "non-refundable deposits cause cancellations" story — the direction is almost certainly reversed or confounded operationally. |
| Guests with `previous_cancellations > 0` cancel again at **91.64%** vs. 33.91% for guests with none. | Group-by on 6,484 vs. 112,906 rows. | Past cancellation behaviour is highly predictive of future behaviour. | Include `previous_cancellations`; consider an engineered prior-cancellation-rate feature. |
| Repeat guests (`is_repeated_guest = 1`) cancel less: **14.49%** vs. 37.79% for new guests. | Group-by on 3,810 vs. 115,580 rows. | Loyal/returning guests are lower risk. | Include `is_repeated_guest`. |
| City Hotel cancels more than Resort Hotel (41.73% vs. 27.76%). | §3.3. | Hotel-type-specific risk baseline. | Include `hotel`; consider hotel-specific threshold if deployed separately per property. |
| `agent`/`company` missingness is structural, not random (94.31% of `company` missing overall). | §3.4. | Most bookings are not company-billed. | Treat missing agent/company as an explicit "no agent"/"no company" category rather than imputing an ID. |

## 3.6 Reproducing this analysis

These statistics were produced with a plain Python (`csv` + `collections`) profiling
pass over the raw file (no `pandas`/`numpy` dependency assumed at documentation
time). Member 1 (Bhanuka Samarasinghe) should re-implement this as a proper
`src/data/validation.py` + `notebooks/01_data_quality_eda.ipynb` using `pandas`, and
confirm every number in this file matches — if a number here doesn't match the
notebook, the notebook is the one to trust and this file must be corrected (open a
`DECISIONS.md` entry noting what changed and why).
