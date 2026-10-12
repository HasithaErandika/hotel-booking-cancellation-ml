# Member 4 (Hasitha Erandika): Validation, Evaluation & Decision Science Lead

Role: **not** "the person who evaluates models at the end." This role validates
whether the *entire experimental setup* is trustworthy before any result is
accepted, then owns calibration, explainability, fairness, the final Test run and the
final business recommendation. See
[`../02-workflow-and-architecture.md`](../02-workflow-and-architecture.md) §2.3
for how this fits the overall architecture.

## What this role does and does not own

**Does not** repeatedly re-clean the dataset or re-engineer features; that's
Bhanuka's and Seneja's job. Instead, this role **audits** their work:

> "Was the missing-value treatment and leakage exclusion performed correctly, and
> could it have biased evaluation?"; not "let me clean it myself."

## Pipeline owned

```text
All 6 trained models (Dummy, Logistic Regression, Decision Tree,
Random Forest, XGBoost, SVM) + their probability outputs
   → Validation gate (leakage, split integrity, imbalance handling, checklist)
   → Unified evaluation framework (same metrics, same code path, every model)
   → Cross-model comparison table
   → Calibration analysis
   → Threshold / business-cost analysis
   → Error analysis
   → Explainability (SHAP, coefficients, permutation importance)
   → Final model selection
   → Business recommendation + limitations + responsible-AI writeup
```

## Deliverables

0. **Own model (non-negotiable, see `../05-modeling-strategy.md` §5.0):** train
   and tune an **SVM (RBF kernel, `class_weight="balanced"`)** in
   `notebooks/09_svm_rbf.ipynb` through the exact
   same shared preprocessing pipeline as every other model, and log it into the
   shared evaluation table. This gives an evaluation lead who is also personally
   accountable for one model, and a genuinely independent check on the
   evaluation framework (built by someone who didn't build the model it's
   scoring in every other case).
1. **Validation gate** (`notebooks/10_validation_gate.ipynb`): the checklist in
   [`../06-evaluation-plan.md`](../06-evaluation-plan.md) §6.3 as executable checks
   (G1 to G5 global, M1 to M7 per model). Writes the list of eligible models.
2. **Model comparison and selection** (notebook 11) is owned by Jayashan. This role
   checks that every model passed the gate before it enters that comparison.
3. **Calibration, threshold and risk tiers**
   (`notebooks/12_calibration_threshold_policy.ipynb`): reliability diagram, Brier
   score, cost-based threshold, Low/Medium/High tiers, and a locked decision policy.
4. **Explainability, error analysis and fairness**
   (`notebooks/13_explainability_error_fairness.ipynb`): permutation importance,
   SHAP, odds-ratio comparison, error profile by segment, and fairness checks by
   `country` and `market_segment` (`../07-recommendation-limitations.md` §7.4).
5. **Final Test evaluation** (`notebooks/14_final_test_evaluation.ipynb`): Test is
   scored once with the locked policy, plus a temporal robustness check.
6. Final sections: `../07-recommendation-limitations.md` filled in with real
   numbers, and keeping [`../DECISIONS.md`](../DECISIONS.md) and
   [`../PROGRESS.md`](../PROGRESS.md) accurate.

## Interfaces (what you require from others, and check independently)

- **From Bhanuka:** cleaned dataset + data-quality/EDA findings, spot-check a
  sample of the claimed statistics independently rather than trusting them
  blindly.
- **From Seneja:** the fitted preprocessing pipeline; verify with your own code
  that `fit()` was never called on test data (don't just take their word for it).
- **From Jayashan:** trained XGBoost model + search results; verify the search
  object's CV splits never included test rows.

## Definition of Done

- [x] SVM trained end-to-end and logged into the shared evaluation table (§5.0
      non-negotiable rule, satisfies your own "at least one model" requirement).
- [x] Validation gate checklist passes for every model before it's allowed into
      the final comparison table.
- [x] Every model scored through the exact same evaluation code path.
- [x] Calibration and threshold analysis completed for at least the final chosen
      model.
- [x] Fairness/error-profile check completed across at least `market_segment`
      and `country` groupings.
- [x] Final recommendation in `../07-recommendation-limitations.md` is backed by
      actual numbers in `../06-evaluation-plan.md`, not aspirational language.
- [x] AI tool usage logged in `../../ai-usage-disclosure/member-4-hasitha-erandika.md`.
