# 5. Model / Data-Mining Strategy and Comparison

*Rubric: 20 marks — Application; Integration | ML implementation; problem solving*

## 5.0 Non-negotiable team rule

> **Every team member must personally train, tune, and own at least one model
> end-to-end** (data-in → fitted model → logged into the shared evaluation table
> in `06-evaluation-plan.md`) — not just contribute to shared pipeline code. This
> is enforced in the Definition of Done for each member
> (`docs/team/roles-and-raci.md`) and is what makes the "Model/data-mining
> strategy and comparison" mark (20 pts) attributable to each individual, not
> just to the team as a whole.

## 5.1 Model portfolio, grouped by task category

Models are organised into **task categories** so the comparison in
`06-evaluation-plan.md` reads as a deliberate progression (naive → interpretable →
nonlinear → ensemble → boosting), not an arbitrary list:

| Category | Model | Owner | Why this category is included |
|---|---|---|---|
| **1. Naive baseline** | Dummy Classifier (`strategy="stratified"` and `"most_frequent"`) | Bhanuka Samarasinghe | Establishes the floor: 62.96% accuracy from always predicting "not cancelled." Every other model must beat this on precision/recall/PR-AUC for the cancelled class, not just accuracy. |
| **2. Linear / interpretable** | Logistic Regression (`class_weight="balanced"`) | Bhanuka Samarasinghe | Coefficients map directly to odds ratios a revenue manager can read (e.g. "Non Refund deposit multiplies cancellation odds by X"); fast, well-understood, a defensible minimum viable model. |
| **3. Rule-based / single tree** | Decision Tree (`class_weight="balanced"`, depth-limited) | Seneja Ramanayake | Human-readable if-then rules; useful as an explanatory artifact for non-technical stakeholders even if it's not the final deployed model. |
| **4. Ensemble (bagging)** | Random Forest (`class_weight="balanced"`) | Seneja Ramanayake | Captures nonlinear interactions (e.g. deposit type × market segment) and gives feature importance without heavy tuning; a strong, low-effort improvement over a single tree. |
| **5. Ensemble (boosting)** | XGBoost / Gradient Boosting (`scale_pos_weight` tuned) | Jayashan Guruge | Typically the strongest tabular-data performer; justifies the extra tuning effort if it beats Random Forest by a meaningful margin — if it doesn't, the simpler Random Forest is preferred (see §5.4). |
| **6. Validation & decision layer** *(not a 6th competing model — see note)* | Calibration / threshold-tuned final model | Hasitha Erandika | Owns the layer that turns whichever model wins §5.4 into a usable, calibrated, threshold-tuned decision tool — see `06-evaluation-plan.md`. |

**Note on category 6:** Hasitha Erandika's "model ownership" requirement (§5.0) is
satisfied by taking calibration/threshold ownership of the final selected model
plus building and training the **fifth comparison point** used as the evaluation
framework's own sanity-check model — a **Support Vector Machine (SVM, RBF
kernel, `class_weight="balanced"`)** trained through the exact same shared
pipeline as everyone else's models. This gives Hasitha a genuinely independent
model (not a rerun of someone else's) to validate the evaluation framework
against, while keeping the primary 5-category comparison above intact.

This gives **6 models total** — 1 baseline + 5 alternatives across 5 distinct
task categories — exceeding the rubric's "baseline + at least three alternatives"
requirement, with **every one of the 4 team members individually training and
owning at least one model end-to-end** (§5.0).

## 5.2 Why not other models (including neural networks)

This section documents models the team considered and rejected, and why — this
is itself evidence of critical judgement, not a gap in the comparison.

- **Deep Neural Network — rejected.** Training data is ~61,177 rows (Train
  split, §4.10) of mixed categorical/continuous tabular features. This is not
  "too little data to train one" — a deep net will fit without erroring — it is
  too little data for a deep architecture's added capacity to pay off. Published
  benchmarks on tabular data of comparable scale consistently find gradient-
  boosted trees match or beat deep nets (Shwartz-Ziv & Armon, 2021, "Tabular
  Data: Deep Learning is Not All You Need"; Grinsztajn et al., 2022, "Why do
  tree-based models still outperform deep learning on tabular data?"). A deep
  net here mainly buys: much higher overfitting risk at this row count, a much
  larger tuning surface (depth, width, dropout, learning-rate schedule, batch
  size, epochs + early stopping), materially harder explainability (DeepSHAP is
  slower and less intuitive to a business stakeholder than tree feature
  importance or logistic coefficients), and no credible expected accuracy gain
  over the already-planned XGBoost. Given the rubric's weight on
  interpretability and responsible AI, this trade is not worth making.
- **Simple / shallow NN (1-2 hidden layers) — considered, not built.**
  Technically the most defensible NN variant for this dataset size, but to be
  competitive it needs entity embeddings for the high-cardinality categoricals
  (`country`: 178 levels, `agent`) rather than one-hot vectors, plus its own
  Dev-set-based early-stopping loop (§4.10) — real added engineering effort for
  a model expected to land close to, not above, Random Forest/XGBoost on this
  data. Documented here as a legitimate alternative that was weighed and
  declined, not overlooked.
- **SNN (self-normalizing network — SELU activation + alpha-dropout,
  Klambauer et al., 2017) — rejected.** SNN's actual benefit is enabling
  *deep* (roughly 8+ layer) feedforward networks on purely continuous,
  normalized inputs to train stably without batch normalization. This dataset
  is a moderate-size mix of categorical and continuous features and doesn't
  need that specific depth — so the exact problem SNN solves doesn't apply
  here, meaning it doesn't even clear the (already weak) case for the plain
  shallow NN above.
- **k-NN** — not chosen as a primary model: high-cardinality categorical features
  (`country`, `agent`) after encoding produce a very high-dimensional sparse space
  where distance metrics degrade; mentioned here for completeness, not built.
- **Naive Bayes** — the independence assumption is clearly violated (e.g.
  `deposit_type` and `market_segment` are correlated), so it is not used as more
  than a footnote comparison if time allows.

## 5.3 Two model variants, to make the leakage-timing decision explicit

Per §4.6 of `04-preprocessing-feature-engineering.md`, we deliberately train and
report **two variants** of every model (at minimum for the final chosen model):

1. **"Day-zero" variant** — excludes `booking_changes`, `days_in_waiting_list`,
   and any room-reassignment feature; uses only information realistically known the
   moment the booking is created.
2. **"Full-lifecycle" variant** — includes those fields, representing what could be
   predicted if the hotel re-scores a booking partway through its life (e.g. a
   week before arrival).

Comparing these two head-to-head is itself a modeling-strategy decision, and
directly demonstrates leakage-aware reasoning rather than blindly using every
available column.

## 5.4 Model selection criterion

The "best" model is **not** simply the one with the highest accuracy or ROC-AUC.
Selection is based on, in order:
1. No leakage (day-zero variant preferred for the deployed recommendation, unless
   the business explicitly wants a later-stage re-score model).
2. PR-AUC and recall at an operationally chosen threshold (see
   `06-evaluation-plan.md`) — because missed cancellations (false negatives) and
   false alarms (false positives) have different, asymmetric business costs.
3. Stability across cross-validation folds (low variance in CV scores) over a
   single high point estimate.
4. Interpretability, as a tiebreaker: if Random Forest and XGBoost perform within
   noise of each other, the simpler, more explainable model is preferred — matching
   the project's emphasis on decision support over pure benchmark-chasing.

## 5.5 Cross-validation strategy

Split roles are defined in `04-preprocessing-feature-engineering.md` §4.10
(Train 70% / Dev 15% / Test 15%); this section defines what happens *inside*
Train and Dev.

- **Stratified K-Fold (k=5)** on the **Train** split only, stratified on
  `is_canceled`, `random_state=42`, so each fold preserves the ~63/37 class
  balance. k=5 is chosen over k=10 because Train already has ~61K rows — each
  fold (~12K rows, ~4,500 positives) is large enough for a stable estimate, so
  k=10 would roughly double compute for negligible variance reduction.
- Hyperparameter search (`RandomizedSearchCV`, `n_iter≈40-60` for XGBoost's
  6-parameter space; `GridSearchCV` acceptable for Decision Tree/Random Forest's
  smaller grids) runs **inside** this Train-only CV loop.
- **Dev** is used for XGBoost early-stopping rounds and for threshold/calibration
  selection (`06-evaluation-plan.md` §6.5) — it can be inspected repeatedly
  during development, unlike Test.
- **Test** is used exactly once per project (not once per model) — after the
  winning model and its threshold are locked in using Train+Dev, Test produces
  the final numbers reported in `06-evaluation-plan.md` §6.4. Evaluating every
  candidate model on Test would itself leak information through repeated
  comparisons, even without ever calling `.fit()` on it.
- Once a final model is chosen, a **RepeatedStratifiedKFold (5 folds × 3
  repeats)** on that single model only is used to report a mean ± std robustness
  check — not run across the full hyperparameter search grid, which would be
  wasteful.
