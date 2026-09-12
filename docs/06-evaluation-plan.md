# 6. Evaluation, Validation, and Critical Judgement

*Rubric: 20 marks — Application; Integration | Statistical reasoning; responsible AI*

Owner: Hasitha Erandika (Member 4) — Validation, Evaluation & Decision Science Lead.
This file defines the framework; actual numbers are filled in once models are
trained (do not pre-fill numbers here — an empty table with a defined method is
worth more than fabricated results).

## 6.1 Why accuracy alone is rejected as the primary metric

The naive baseline (§5.1, "always predict not-cancelled") already reaches **62.96%
accuracy** while identifying zero cancellations. Any model report that leads with
accuracy alone cannot be trusted to demonstrate real skill — it must be compared
against this baseline and paired with recall/precision for the cancelled class.

## 6.2 Metrics reported for every model

| Metric | What it answers | Why it's here |
|---|---|---|
| Accuracy | Overall proportion correct | Reported only as context next to the baseline, never alone |
| Precision (class = cancelled) | Of bookings flagged high-risk, how many actually cancel? | Controls the cost of unnecessary manager attention / customer friction |
| Recall (class = cancelled) | Of bookings that actually cancel, how many did we catch? | Controls the cost of missed cancellations (unmanaged revenue risk) |
| F1 (class = cancelled) | Harmonic balance of precision/recall | Single-number comparison when neither error type is declared more costly |
| ROC-AUC | Ranking quality across all thresholds | Threshold-independent comparison between models |
| PR-AUC (Average Precision) | Ranking quality, weighted for the positive class | More informative than ROC-AUC under class imbalance; primary ranking metric here |
| Confusion matrix | Raw TP/FP/FN/TN counts | Grounds every rate metric in actual counts a manager can sanity-check |
| Brier score / calibration curve | Do predicted probabilities match observed frequencies? | A 0.8 "risk score" should mean ~80% of similar bookings actually cancel — needed before probabilities are shown to staff as trustworthy numbers |

## 6.3 Validation / leakage-prevention checklist (the "validation gate")

Before any model result is accepted into the final report, Member 4 verifies:

- [ ] `reservation_status` and `reservation_status_date` are absent from the
      feature matrix (assert this programmatically, not just by eye).
- [ ] Exact duplicate rows were removed **before** the train/dev/test split, not
      after (`04-preprocessing-feature-engineering.md` §4.2, §4.10) — verified by
      checking no identical row (by hash of all columns) appears in more than one
      split.
- [ ] All imputers/encoders/scalers were `.fit()` only on the **training** split;
      `.transform()` only applied to Dev and Test (verified by inspecting the
      fitted `ColumnTransformer`, not just trusting the code comment).
- [ ] Cross-validation is stratified on `is_canceled`, run **inside the training
      split only** (§5.5).
- [ ] Hyperparameter search and early stopping used Train/Dev only — never
      touched the Test set.
- [ ] **Threshold selection (§6.5) was performed on the Dev set, not the Test
      set** — the Test set is scored exactly once, with the threshold already
      locked in, or the reported test metrics are optimistically biased.
- [ ] Class-imbalance handling (`class_weight`, `scale_pos_weight`, or SMOTE) is
      applied only within the training data / training folds.
- [ ] The two leakage-timing variants (§5.3, day-zero vs. full-lifecycle) are
      clearly labelled and never mixed together in one comparison row.

A model that fails any checklist item is **not eligible** to be recommended,
regardless of its reported score.

## 6.4 Model comparison table (template — fill in after training)

| Model | Variant | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC | CV std (F1) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Dummy (majority class) | — | 0.6296 | — | 0.000 | — | 0.500 | — | — |
| Logistic Regression | day-zero | | | | | | | |
| Decision Tree | day-zero | | | | | | | |
| Random Forest | day-zero | | | | | | | |
| XGBoost | day-zero | | | | | | | |
| SVM (RBF) | day-zero | | | | | | | |
| Random Forest | full-lifecycle | | | | | | | |
| XGBoost | full-lifecycle | | | | | | | |

All rows above are **CV means computed on the Train split** (plus a final,
single-touch confirmation on Test for the winning model only — see §6.5). Do not
populate this table using repeated Test-set evaluations of multiple models; that
would itself be a form of test-set leakage (the "many comparisons" problem).

## 6.5 Threshold analysis and business cost framing

Default `P > 0.5` is not assumed to be the operational threshold. Threshold
selection happens **entirely on the Dev split** (`04-preprocessing-feature-engineering.md`
§4.10), never on Test — Test is reserved for a single, final, already-decided
evaluation. Concretely:

1. On Dev, sweep thresholds (e.g. 0.3, 0.4, 0.5, 0.6, 0.7) and report
   precision/recall/F1 at each for the chosen final model.
2. Define an explicit (illustrative, stated-as-assumption) cost matrix, e.g.:
   - **False Negative** (missed cancellation): the hotel is caught off guard —
     assumed higher operational cost.
   - **False Positive** (flagged booking that would have honoured): a small cost —
     unnecessary manager attention or a follow-up contact to the guest.
3. Recommend a threshold (or a 3-tier Low/Medium/High banding) that reflects this
   asymmetry, and state explicitly that the *actual* costs are hotel-specific
   assumptions, not measured figures — this is a judgement call the business
   stakeholder should ultimately confirm, not one this project can decide for them.
4. **Lock the threshold**, then run the Test split exactly once through the
   winning model at that fixed threshold to produce the final reported numbers
   in §6.4. If the threshold is changed after seeing the Test result, the Test
   set has effectively become a second Dev set and the reported numbers are no
   longer an honest estimate of generalisation.

## 6.6 Error analysis

For the selected final model:
- Profile false negatives (missed cancellations) — do they cluster by
  `market_segment`, `hotel`, or lead time? This tells the business *where* the
  model is currently blind.
- Profile false positives — do they cluster around the `deposit_type = Non Refund`
  anomaly (§3.5)? If so, call this out explicitly rather than presenting the
  overall metric as uniformly reliable across segments.

## 6.7 Honest interpretation — what "good" performance does and doesn't mean

- A high ROC-AUC/PR-AUC shows the model **ranks** bookings by risk better than
  chance; it does not show the model has found a *causal* driver of cancellation
  (see limitations in `07-recommendation-limitations.md`).
- Cross-validation stability (§6.4 "CV std" column) is reported alongside the mean
  score specifically so a lucky single split isn't mistaken for genuine skill.
- If the "full-lifecycle" variant meaningfully outperforms "day-zero," that
  difference is reported as evidence of *how much* signal comes from
  post-booking events (like `booking_changes`) — not hidden by only reporting the
  better-looking number.
