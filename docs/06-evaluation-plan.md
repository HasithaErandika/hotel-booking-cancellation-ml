# 6. Evaluation, Validation, and Critical Judgement

*Rubric: 20 marks. Application; Integration | Statistical reasoning; responsible AI*

Owner: Hasitha Erandika (Member 4), Validation, Evaluation & Decision Science Lead.
This file defines the framework and records the results from notebooks 10 to 14.
Every number below comes from a file in `reports/tables/` or `artifacts/`.

## 6.1 Why accuracy alone is rejected as the primary metric

The naive baseline (§5.1, "always predict not-cancelled") already reaches **72.72%
accuracy** on the de-duplicated data while catching zero cancellations (decision
#25). A no-skill model also gets a PR-AUC equal to the cancellation rate, **0.273**.
So a report that leads with accuracy alone shows nothing. Every model must be
compared against this baseline and paired with recall/precision for the cancelled
class.

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
| Brier score / calibration curve | Do predicted probabilities match observed frequencies? | A 0.8 "risk score" should mean ~80% of similar bookings actually cancel, needed before probabilities are shown to staff as trustworthy numbers |

## 6.3 Validation / leakage-prevention checklist (the "validation gate")

Before any model result is accepted into the final report, Member 4 verifies:

- [x] `reservation_status` and `reservation_status_date` are absent from the
      feature matrix (assert this programmatically, not just by eye).
- [x] Exact duplicate rows were removed **before** the train/dev/test split, not
      after (`04-preprocessing-feature-engineering.md` §4.2, §4.10), verified by
      checking no identical row (by hash of all columns) appears in more than one
      split.
- [x] All imputers/encoders/scalers were `.fit()` only on the **training** split;
      `.transform()` only applied to Dev and Test (verified by inspecting the
      fitted `ColumnTransformer`, not just trusting the code comment).
- [x] Cross-validation is stratified on `is_canceled`, run **inside the training
      split only** (§5.5).
- [x] Hyperparameter search and early stopping used Train/Dev only; never
      touched the Test set.
- [x] **Threshold selection (§6.5) was performed on the Dev set, not the Test
      set**; the Test set is scored exactly once, with the threshold already
      locked in, or the reported test metrics are optimistically biased.
- [x] Class-imbalance handling (`class_weight`, `scale_pos_weight`, or SMOTE) is
      applied only within the training data / training folds.
- [x] The two leakage-timing variants (§5.3, day-zero vs. full-lifecycle) are
      clearly labelled and never mixed together in one comparison row.

A model that fails any checklist item is **not eligible** to be recommended,
regardless of its reported score. Notebook 10 (validation gate) runs every item above
as code: global checks G1 to G5 and per-model checks M1 to M7. Its report,
`artifacts/validation_gate_report.json`, lists the eligible models for notebooks 11
to 14.

**Result:** 83 checks ran. All global checks passed and there were no `FAIL`s, so all
11 models are eligible. One `WARN`: the SVM's CV used a 12,000-row Train subsample
(documented in its model card). Every box above is ticked because the gate checked
it in code (`reports/tables/10_validation_gate_checks.csv`).

## 6.4 Model comparison table (notebook 11)

CV columns are the mean ± SD over 5 Train folds. Dev columns use a 0.5 threshold, with
a 1,000-sample bootstrap 95% CI for PR-AUC. Sources: `reports/tables/model_comparison_cv.csv`
and `reports/tables/model_comparison_dev.csv`.

| Model | Variant | CV PR-AUC | CV ROC-AUC | CV F1 | Dev PR-AUC [95% CI] | Dev precision | Dev recall | Dev accuracy |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Dummy (majority class) | baseline | 0.273 ± 0.000 | 0.500 | 0.000 | 0.273 [0.265, 0.280] | 0.000 | 0.000 | 0.727 |
| Dummy (stratified) | baseline | 0.273 ± 0.001 | 0.502 | 0.272 | 0.270 [0.262, 0.279] | 0.264 | 0.258 | 0.601 |
| Logistic Regression | day-zero | 0.651 ± 0.006 | 0.827 | 0.532 | 0.651 [0.636, 0.666] | 0.656 | 0.458 | 0.787 |
| Decision Tree | day-zero | 0.700 ± 0.003 | 0.863 | 0.653 | 0.709 [0.694, 0.724] | 0.547 | 0.815 | 0.766 |
| Random Forest | day-zero | 0.759 ± 0.005 | 0.891 | 0.687 | 0.763 [0.750, 0.777] | 0.684 | 0.703 | 0.831 |
| **XGBoost** | **day-zero** | **0.765 ± 0.002** | **0.893** | **0.672** | **0.771 [0.758, 0.784]** | **0.722** | **0.638** | **0.834** |
| SVM (RBF) | day-zero | 0.677 ± 0.014 * | 0.850 | 0.641 | 0.689 [0.673, 0.704] | 0.668 | 0.585 | 0.808 |
| Logistic Regression | full-lifecycle | 0.701 ± 0.006 | 0.864 | 0.601 | 0.703 [0.689, 0.718] | 0.687 | 0.546 | 0.808 |
| Decision Tree | full-lifecycle | 0.745 ± 0.005 | 0.889 | 0.689 | 0.753 [0.740, 0.767] | 0.578 | 0.842 | 0.789 |
| Random Forest | full-lifecycle | 0.793 ± 0.004 | 0.912 | 0.723 | 0.801 [0.788, 0.814] | 0.711 | 0.749 | 0.848 |
| XGBoost | full-lifecycle | 0.805 ± 0.003 | 0.916 | 0.713 | 0.812 [0.801, 0.824] | 0.748 | 0.691 | 0.852 |

\* SVM CV on a 12,000-row subsample. XGBoost used Dev for early stopping, so its Dev
score is slightly optimistic; its Test score (§6.5) confirms it was not by much.

Only the selected model (`xgboost__day_zero`) was scored on Test. The other rows were
never compared on Test.

**Statistical comparison** (Nadeau and Bengio corrected t-test on the 5 CV folds,
`reports/tables/11_corrected_ttests.csv`): every pair of day-zero models differs at
p < 0.001, except XGBoost vs Random Forest (difference 0.0065, p = 0.054). Those two
are close to a tie; the selection rule in `05-modeling-strategy.md` §5.4 and §5.6 picks
XGBoost because the gap is above the 0.005 tolerance.

## 6.5 Threshold analysis and business cost framing

Default `P > 0.5` is not assumed to be the operational threshold. Threshold
selection happens **entirely on the Dev split** (`04-preprocessing-feature-engineering.md`
§4.10), never on Test; Test is reserved for a single, final, already-decided
evaluation. Concretely:

1. On Dev, sweep thresholds (e.g. 0.3, 0.4, 0.5, 0.6, 0.7) and report
   precision/recall/F1 at each for the chosen final model.
2. Define an explicit (illustrative, stated-as-assumption) cost matrix, e.g.:
   - **False Negative** (missed cancellation): the hotel is caught off guard, 
     assumed higher operational cost.
   - **False Positive** (flagged booking that would have honoured): a small cost, 
     unnecessary manager attention or a follow-up contact to the guest.
3. Recommend a threshold (or a 3-tier Low/Medium/High banding) that reflects this
   asymmetry, and state explicitly that the *actual* costs are hotel-specific
   assumptions, not measured figures; this is a judgement call the business
   stakeholder should ultimately confirm, not one this project can decide for them.
4. **Lock the threshold**, then run the Test split exactly once through the
   winning model at that fixed threshold to produce the final reported numbers
   in §6.4. If the threshold is changed after seeing the Test result, the Test
   set has effectively become a second Dev set and the reported numbers are no
   longer an honest estimate of generalisation.

### Results (notebooks 12 and 14)

**Calibration (Dev, cross-fitted).** Sigmoid (Platt) scaling was chosen because it
had the lowest Brier score. It changes the ranking very little and makes the
probabilities more honest: expected calibration error falls from 0.0118 to 0.0070.

| Method | Brier | Log loss | ECE | PR-AUC |
|---|---:|---:|---:|---:|
| None | 0.1143 | 0.3541 | 0.0118 | 0.7707 |
| **Sigmoid** | **0.1142** | **0.3539** | **0.0070** | **0.7705** |
| Isotonic | 0.1147 | 0.3569 | 0.0054 | 0.7635 |

**Cost assumptions** (illustrative, `artifacts/decision_policy.json`): median booking
value 303 (Train); a missed cancellation loses 30% of it (90.9); a caught one still
loses 10% plus a 15 follow-up cost (45.3); a false alarm costs 25 (follow-up plus guest
friction). So a missed cancellation costs about 1.8 times a false alarm, net.

**Threshold.** The cost-optimal threshold on Dev is **0.35**, which is also the
F1-optimal threshold (F1 0.703). The theory value for these costs is 0.354, so the
sweep agrees with it. The threshold stays at 0.35 for any cost ratio between 1.5 and
2.0; at 1.0 it rises to 0.52, and at 3.0 it falls to 0.25
(`reports/tables/12_threshold_sensitivity.csv`).

**Risk tiers.** Low < 0.18 ≤ Medium < 0.35 ≤ High. The policy was hashed and locked
before Test was read.

**Final Test result (read once, notebook 14, threshold 0.35):**

| Metric | Test estimate | 95% bootstrap CI | Dev |
|---|---:|---:|---:|
| PR-AUC | 0.774 | 0.760 to 0.787 | 0.771 |
| ROC-AUC | 0.895 | 0.889 to 0.901 | 0.894 |
| Precision | 0.653 | 0.639 to 0.667 | 0.647 |
| Recall | 0.778 | 0.764 to 0.792 | 0.770 |
| F1 | 0.710 | 0.699 to 0.722 | 0.703 |
| Brier | 0.113 | 0.110 to 0.117 | 0.114 |
| Accuracy | 0.827 | | |
| Flag rate | 32.5% | | 32.4% |

Confusion matrix on 13,071 Test bookings: TP 2,774, FP 1,474, FN 791, TN 8,032.
Test and Dev agree within 0.01 on every metric, so the threshold choice did not
overfit Dev.

| Tier (Test) | Bookings | Share of bookings | Cancellation rate | Share of all cancellations |
|---|---:|---:|---:|---:|
| Low | 6,829 | 52.2% | 4.8% | 9.2% |
| Medium | 1,994 | 15.3% | 23.2% | 13.0% |
| High | 4,248 | 32.5% | 65.3% | 77.8% |

Expected cost per 1,000 bookings (under the stated assumptions): **17,934 with the
model vs 24,792 with no model, 27.7% lower**.

**Temporal robustness** (train 2015 to 2016, 55,531 rows; test 2017, 31,607 rows). The
random split hides drift. On the later year PR-AUC drops from 0.774 to 0.650, ROC-AUC
from 0.895 to 0.809 and recall from 0.778 to 0.519, while precision holds (0.657). The
2017 cancel rate (31.7%) is higher than the training years (24.7%), so at a fixed
threshold the model under-flags. See `07-recommendation-limitations.md` §7.3.

## 6.6 Error analysis (notebook 13, Dev, threshold 0.35)

The questions we planned to ask, and what the data answered:

- **Where are missed cancellations?** By market segment
  (`reports/tables/13_error_profile_by_segment.csv`):

  | Segment | Bookings | Cancel rate | Recall | False negative rate | False positive rate |
  |---|---:|---:|---:|---:|---:|
  | Online TA | 7,769 | 35.2% | 0.811 | 0.189 | 0.239 |
  | Offline TA/TO | 2,039 | 13.9% | 0.810 | 0.190 | 0.085 |
  | Direct | 1,749 | 14.5% | **0.316** | **0.684** | 0.055 |
  | Groups | 745 | 27.1% | 0.896 | 0.104 | 0.079 |
  | Corporate | 647 | 11.9% | **0.429** | **0.571** | 0.032 |

  The model is weakest on **Direct and Corporate** bookings: it misses most of their
  cancellations. Their cancel rates are low, so their scores rarely reach 0.35. By
  hotel, recall is almost the same (City 0.772, Resort 0.765), but City Hotel has more
  false alarms (FPR 0.178 vs 0.128).
- **Do false positives cluster on `Non Refund` deposits?** No. 99.9% of false positives
  are `No Deposit` bookings, which are 98.5% of all bookings. The Non Refund anomaly
  (§3.5) does not drive the false alarms. The most confident false alarms are mostly
  Resort Hotel, Online TA, long lead time bookings that did not cancel
  (`reports/tables/13_confident_errors.csv`).
- **What drives the score?** Permutation importance on Dev (drop in PR-AUC):
  `country` 0.168, `lead_time` 0.141, `agent` 0.122, `total_of_special_requests`
  0.115, `market_segment` 0.069. `deposit_type` is only 9th (0.028), even though it
  tops XGBoost's built-in gain ranking; gain over-rates a feature that splits a small,
  very pure group. Rank agreement with Logistic Regression is 0.62 (Spearman), so the
  two model families mostly agree on what matters.
- **SHAP** was not run because `shap` was not installed on the team kernel; the
  notebook skips that section cleanly. Permutation importance covers the global view.

### Fairness audit (Dev, threshold 0.35)

Overall: recall 0.770, false positive rate 0.158, selection rate 32.5%. A group is
flagged when its recall differs from the overall by more than 0.10 or its FPR ratio falls outside 0.8
to 1.25 (`reports/tables/13_fairness_audit.csv`).

- **Country** (10 largest countries plus "Other"): 8 flagged. Recall ranges from 0.571 (NLD) to
  0.876 (BRA). Portuguese bookings get more false alarms (FPR 0.214, 1.36 times the
  overall rate); Dutch, Belgian, French and German bookings get fewer false alarms
  but more missed cancellations.
- **Market segment:** every segment with enough data is flagged, mainly the low
  recall for Direct and Corporate and the high FPR for Online TA (1.51 times).

These gaps mostly follow differences in base rates between groups (PRT 34% cancel vs
NLD 15%), but the effect on guests is the same. `country` is the most important
feature, so the score must not be used to treat guests differently by nationality
(`07-recommendation-limitations.md` §7.4).

## 6.7 Honest interpretation: what "good" performance does and doesn't mean

- A high ROC-AUC/PR-AUC shows the model **ranks** bookings by risk better than
  chance; it does not show the model has found a *causal* driver of cancellation
  (see limitations in `07-recommendation-limitations.md`).
- Cross-validation stability (§6.4 "CV std" column) is reported alongside the mean
  score specifically so a lucky single split isn't mistaken for genuine skill.
- If the "full-lifecycle" variant meaningfully outperforms "day-zero," that
  difference is reported as evidence of *how much* signal comes from
  post-booking events (like `booking_changes`); not hidden by only reporting the
  better-looking number. **Result:** full-lifecycle XGBoost reaches 0.805 CV PR-AUC
  vs 0.765 for day-zero (+0.039, 5.1% relative). This gain is real but modest, and the
  full-lifecycle model cannot be used at booking time.
- The random-split Test score (0.774 PR-AUC) is an honest estimate for bookings from
  the same period. The temporal check (0.650 on 2017) is the better guide for future
  bookings.
