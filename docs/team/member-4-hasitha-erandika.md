# Member 4 — Hasitha Erandika: Validation, Evaluation & Decision Science Lead

Role: **not** "the person who evaluates models at the end." This role validates
whether the *entire experimental setup* is trustworthy before any result is
accepted, then owns unified evaluation, calibration, explainability, and the
final business recommendation. See
[`../02-workflow-and-architecture.md`](../02-workflow-and-architecture.md) §2.3
for how this fits the overall architecture.

## What this role does and does not own

**Does not** repeatedly re-clean the dataset or re-engineer features — that's
Bhanuka's and Seneja's job. Instead, this role **audits** their work:

> "Was the missing-value treatment and leakage exclusion performed correctly, and
> could it have biased evaluation?" — not "let me clean it myself."

## Pipeline owned

```text
All 6 trained models (Dummy, Logistic Regression, Decision Tree,
Random Forest, XGBoost, SVM) + their probability outputs
   → Validation gate (leakage, split integrity, imbalance handling — checklist)
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
   and tune an **SVM (RBF kernel, `class_weight="balanced"`)** through the exact
   same shared preprocessing pipeline as every other model, and log it into the
   shared evaluation table. This gives an evaluation lead who is also personally
   accountable for one model, and a genuinely independent check on the
   evaluation framework (built by someone who didn't build the model it's
   scoring in every other case).
1. **Validation gate** (`src/evaluation/validation.py`) implementing the
   checklist in [`../06-evaluation-plan.md`](../06-evaluation-plan.md) §6.3 as
   executable assertions, not just a manual read-through: no leakage columns in
   the feature matrix, dedup happened pre-split, preprocessing fit on train only,
   stratified CV, hyperparameter search never touched test data.
2. **Unified evaluation framework** (`src/evaluation/metrics.py`) — one function
   every model's predictions pass through, producing accuracy, precision, recall,
   F1, ROC-AUC, PR-AUC, and confusion matrix in one consistent format, so numbers
   are comparable across Bhanuka/Seneja/Jayashan's models without re-implementing
   metric code four different ways.
3. **Calibration analysis** (`src/evaluation/calibration.py`) — reliability
   diagram + Brier score for the selected model(s); report whether "0.8
   probability" actually means ~80% observed cancellation rate.
4. **Threshold / cost analysis** — sweep decision thresholds, apply the
   illustrative cost framing from `../06-evaluation-plan.md` §6.5, produce the
   Low/Medium/High risk-tier banding used in the final recommendation.
5. **Error analysis** (`src/evaluation/error_analysis.py`) — false
   positive/negative profiling by `hotel`, `market_segment`, `deposit_type`
   (§6.6), including a fairness check across `country`/`market_segment` groups
   (`../07-recommendation-limitations.md` §7.4).
6. **Explainability** — SHAP values for the tree-based models, coefficients/odds
   ratios for Logistic Regression, computed centrally so every model is explained
   with the same rigor rather than whichever member remembered to do it.
7. `notebooks/07_final_evaluation.ipynb` — assembles the full model comparison
   table, calibration plots, threshold analysis, and explainability plots that
   feed directly into the final report.
8. Final sections: `../07-recommendation-limitations.md` filled in with real
   numbers, plus ongoing ownership of `../../DECISIONS.md` and
   `../../PROGRESS.md` staying accurate and current.

## Interfaces (what you require from others, and check independently)

- **From Bhanuka:** cleaned dataset + data-quality/EDA findings — spot-check a
  sample of the claimed statistics independently rather than trusting them
  blindly.
- **From Seneja:** the fitted preprocessing pipeline — verify with your own code
  that `fit()` was never called on test data (don't just take their word for it).
- **From Jayashan:** trained XGBoost model + search results — verify the search
  object's CV splits never included test rows.

## Definition of Done

- [ ] SVM trained end-to-end and logged into the shared evaluation table (§5.0
      non-negotiable rule — satisfies your own "at least one model" requirement).
- [ ] Validation gate checklist passes for every model before it's allowed into
      the final comparison table.
- [ ] Every model scored through the exact same evaluation code path.
- [ ] Calibration and threshold analysis completed for at least the final chosen
      model.
- [ ] Fairness/error-profile check completed across at least `market_segment`
      and `country` groupings.
- [ ] Final recommendation in `../07-recommendation-limitations.md` is backed by
      actual numbers in `../06-evaluation-plan.md`, not aspirational language.
- [ ] AI tool usage logged in `../../ai-usage-disclosure/member-4-hasitha-erandika.md`.
