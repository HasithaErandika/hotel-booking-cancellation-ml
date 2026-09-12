# Member 1 — Bhanuka Samarasinghe: Data Engineering + EDA

Role: **Data Engineer / EDA Lead**. Owns the data foundation everyone else builds
on. Also owns Model 1 (Logistic Regression) as the project's interpretable
statistical baseline.

## Pipeline owned

```text
Raw CSV (data/hotel_bookings.csv)
   → Schema validation
   → Data-quality profiling (missingness, duplicates, invalid values)
   → Cleaning decisions (documented, not silently applied)
   → Leakage audit (reservation_status vs is_canceled)
   → Clean dataset + Data Dictionary + EDA Insight Log
```

## Deliverables

1. `src/data/ingestion.py` — load raw CSV, enforce dtypes per the data dictionary
   in [`../03-data-understanding.md`](../03-data-understanding.md).
2. `src/data/validation.py` — schema checks (expected columns, expected category
   values, dtype assertions); re-verify every number quoted in
   `03-data-understanding.md` (row/column counts, missingness %, duplicate count,
   target distribution) and flag any mismatch.
3. `src/data/cleaning.py` — implement the documented decisions from
   [`../04-preprocessing-feature-engineering.md`](../04-preprocessing-feature-engineering.md)
   §4.2–§4.4 (duplicates, missing values, invalid values). Cleaning logic lives
   here, not duplicated in notebooks.
4. `notebooks/01_data_quality_eda.ipynb` — reproduces every table in
   `03-data-understanding.md`, plus the full EDA visual set (cancellation by
   hotel, lead time, deposit type, market segment, previous-cancellation history,
   special requests).
5. **Leakage audit** — programmatically confirm `reservation_status` /
   `is_canceled` correspondence (already found: 100% match on hand-computed
   check) and hand this finding to the whole team before anyone starts modeling.
6. Logistic Regression baseline model (`src/models/logistic.py`), trained on
   Seneja's shared preprocessing output, using `class_weight="balanced"`.
7. Contribute EDA Insight Log rows and Data-quality rows to `../../DECISIONS.md`.

## Interfaces (what you hand off)

- **To Seneja (Member 2):** the cleaned dataset (post-dedup, post-leakage-drop,
  post-invalid-value handling) as a single `.parquet`/`.csv` output plus a written
  note of every transformation applied, so Feature Engineering starts from a known
  state, not raw data.
- **To Hasitha (Member 4):** the EDA Insight Log and data-quality report, since the
  validation gate re-checks that leakage columns are actually excluded downstream.

## Definition of Done

- [ ] Every statistic in `03-data-understanding.md` is reproduced by
      `notebooks/01_data_quality_eda.ipynb` and matches exactly (or the doc is
      corrected with a `DECISIONS.md` entry explaining the discrepancy).
- [ ] Cleaning decisions are implemented as functions in `src/data/cleaning.py`,
      not ad-hoc notebook cells.
- [ ] Logistic Regression model trained and logged into the shared evaluation
      table (`../06-evaluation-plan.md` §6.4).
- [ ] AI tool usage for this workstream logged in
      `../../ai-usage-disclosure/member-1-bhanuka-samarasinghe.md`.
