# Plan: Final Audit, Gap Fixes and Submission

> Status: **active** · Last revised: 2026-10-12 · Replaces the 2026-10-11 plan
> (notebook-only pipeline), which is finished. The old plan is kept in git history
> at commit `02cc61a`.
>
> **Code fixes done and run on 2026-10-12** (see the Status in §3). The Test lock still verifies.

This plan has five parts: (1) what the old plan delivered, (2) how the project scores
against the marking rubric today, (3) the gaps found in this audit, (4) a fair split of
the remaining work across the four members, and (5) the order to do it in.

---

## 1. Old plan: closed

| Old plan item | Result |
|---|---|
| Notebook-only pipeline `01` to `14` | Done. All 14 notebooks run with every cell executed and no errors. |
| Issues I-01 to I-19 | Resolved in notebooks 01 to 14 and docs 01 to 08. |
| New decisions #21 to #28 | Logged, plus #29 and #30. |
| Doc updates (old §9) | Done. No stale `src/`, 80/20 or 62.96% baseline references left, except where they describe history. |
| Roadmap F-01 to F-11 | Not started. F-03, F-07, F-10 and F-11 move into this plan. The rest stay as future work (§7). |

Headline results: `xgboost__day_zero` selected, Test PR-AUC 0.774 [0.760, 0.787],
recall 0.778 and precision 0.653 at threshold 0.35, temporal check PR-AUC 0.650.

---

## 2. Rubric check (honest)

Verdict key: **Strong** = high-mark evidence exists · **Partial** = evidence exists but
has a gap a marker will notice · **Weak** = likely to lose marks.

| Criterion | Marks | Evidence in the repo | Verdict | Gap (see §3) |
|---|---|---|---|---|
| Business problem framing | 5 | `docs/01`: stakeholder, decision need, primary and secondary lens, unit of analysis, exact output, rationale, success criteria | Strong | No one-page **problem framing canvas** (listed as core evidence). A-13 |
| Workflow diagram and decision log | 10 | Mermaid diagrams in `docs/02` and README, 30 decisions with options, reasons and evidence | Strong | None |
| Data understanding, EDA, data quality | 10 | `docs/03` data dictionary, notebook 01 quality audit, notebook 03 (19 figures, Wilson CIs, MI, Cramér's V, Spearman), EDA insight log | Strong | Minor figure fixes. A-07 |
| Preprocessing and feature engineering | 15 | Notebook 04, feature spec, feature log, leakage variants, imbalance, ADR cap, unseen-category test | Partial | No explicit **feature selection** step and perfect collinearity in the linear inputs. A-03, A-04 |
| Model strategy and comparison | 20 | Two dummies + LR, DT, RF, XGBoost, SVM, both variants, written selection rule | Strong | SVM compared on a 12,000-row CV subsample; must be stated next to the chart. A-07 |
| Evaluation, validation, critical judgement | 20 | Validation gate (83 checks), CV mean ± SD, bootstrap CIs, corrected t-test, calibration, cost-based threshold, error and fairness audit, test-once lock, temporal check | Strong | "Fill in after running" cells in 11 and 13 still empty. SHAP not run. Fairness flags need CIs. A-06, A-09, A-10 |
| Recommendation, limitations, stakeholder value | 10 | `docs/07` filled with real numbers | Strong | Final report not assembled. A-14 |
| Reproducibility, documentation, AI-use | 10 | SHA-256 fingerprint, dataset link, artifact hashes, seeds, run order | **Weak** | AI-use logs are empty for two members and do not record the 2026-10-11 Claude Code sessions that wrote notebooks 01 to 14. Ownership in the docs does not match git history. `requirements.txt` has a macOS-only package. A-01, A-02, A-11 |

**Bottom line:** the technical work is at a high-mark level. The two real risks are
(1) AI-use transparency, which is both a rubric criterion and an academic-integrity
issue, and (2) the missing feature-selection evidence in the 15-mark preprocessing
criterion.

---

## 3. Gaps found in this audit

Severity: **High** = costs marks or integrity · **Medium** = a marker may notice · **Low** = hygiene.

| # | Sev | Gap | Evidence | Fix and status |
|---|---|---|---|---|
| A-01 | High | **AI-use disclosure was incomplete.** Member 2 and 3 logs were empty templates, member 4's log stopped at 2026-09-12, and member 1's log described removed `src/` files. | `ai-usage-disclosure/*.md`, commit `677280f` | **Partly done.** Contribution statement and tools per member added to `ai-usage-disclosure/README.md` and `docs/08` §8.5; Hasitha's Claude Code sessions logged. **Open:** Seneja confirms her 2026-09-16 row; Jayashan adds his Codex rows. |
| A-02 | High | **Workload was unequal on paper.** Notebooks per owner: Bhanuka 3, Seneja 4, Jayashan 1, Hasitha 6. | `docs/team/roles-and-raci.md` | **Done.** Ownership set in §4.1 and in `docs/team/roles-and-raci.md`, member docs and `docs/PROGRESS.md`. |
| A-03 | High | **No explicit feature-selection step.** Notebook 03 ranks features (MI, Cramér's V, Spearman) but no rule turns the ranking into keep or drop. No significance tests. MI does not cover the 9 engineered features. Selection today is only by leakage and timing, which is valid but not shown as a method. | Notebook 03 §12, notebook 04 §4.1 | **Done.** Notebook 04 §4.4: Mann-Whitney U / chi-square, BH correction, effect sizes, mutual information on raw and engineered inputs, VIF, decision table and chart. `docs/04` §4.13, decision #31. |
| A-04 | High | **Perfect collinearity in the linear inputs.** `total_nights = weekend + week nights`, `total_guests = adults + children + babies`, `total_previous_bookings = previous_cancellations + previous_bookings_not_canceled`. All six raw parts and three totals go into Logistic Regression and SVM. L2 keeps the fit stable, but the **odds ratios of these features cannot be read one by one** (for example `previous_cancellations` shows OR 0.96, which looks protective). | `reports/tables/05_logreg_day_zero_odds_ratios.csv` | **Done.** Caveat in notebook 05 §5; reduced input set and L1 penalty in 05 §6 with readable odds ratios. |
| A-05 | Medium | Notebook 10 has no chart (every other notebook has at least one). | Notebook outline | **Done.** Check-matrix heatmap in notebook 10 §5.2. |
| A-06 | Medium | Notebook 11 §11 and notebook 13 §7 still say "fill in after running". | Notebooks 11, 13 | **Done.** Notebook 11 §11 and 13 §7 filled with the recorded numbers. |
| A-07 | Medium | Figure fixes. `11_cv_pr_auc_comparison`: rows not sorted by score (SVM 0.677 drawn below LR 0.651) and SVM subsample not marked. `12_threshold_analysis`: legend sits on the "No model" line and the `t = 0.35` label touches the axis. `13_fairness_country`: "flag" labels overlap the overall line, and "Honouring guests" is unclear (use "Guests who stayed"). `03_mutual_information`: does not mark which features were later excluded. | `reports/figures/` | **Done.** 03 MI bars coloured by later role; 11 sorted by day-zero score with hollow SVM marker; 12 legend moved and label lifted; 13 labels per panel, away from the overall line, robust vs point flags, "Guests who stayed". |
| A-09 | Medium | SHAP was skipped because `shap` is not installed in the team kernel. | `docs/DECISIONS.md` #30 | **Done.** `shap` 0.51.0 installed, notebook 13 re-run, decision #33. |
| A-10 | Medium | Fairness audit flags 8 of 11 country groups. With small groups, many gaps may be noise. | `reports/tables/13_fairness_audit.csv` | **Done.** Notebook 13 §6.2b: bootstrap intervals per group, `13_fairness_audit_ci.csv`, decision #32. |
| A-11 | Low | `requirements.txt` has `appnope` (macOS only) and an unpinned `shap`. | `requirements.txt` | **Done.** `appnope` removed; `shap==0.51.0` and its new dependencies pinned. |
| A-12 | Low | Stale text: "proposed decision #23" in the feature spec and feature log, `src/features/` in member 2's AI log, unchecked DoD boxes in `docs/team/*.md` for finished work. | grep | **Done.** Notebook 04 source wording fixed (the saved `feature_spec.json` keeps the old wording until §6 of notebook 04 is re-run, which is not advised); member 2 AI log fixed; DoD boxes ticked for finished work. |
| A-13 | Low | No one-page problem framing canvas. | Core evidence list | **Done.** Canvas table at the top of `docs/01`. |
| A-14 | Medium | Final report not assembled. | `docs/PROGRESS.md` | **Open.** Assemble from docs 01 to 08; every number must trace to `reports/tables/`. |

---

## 4. Ownership and remaining work

### 4.1 Notebook ownership

| Member | Notebooks owned | Report sections owned |
|---|---|---|
| Bhanuka Samarasinghe | 01 Data quality, 03 EDA, 05 Baselines + LR | Data understanding (docs/03) |
| Seneja Ramanayake | 02 Split, 04 Features + preprocessing + screening, 06 Decision Tree, 07 Random Forest | Preprocessing and features (docs/04) |
| Jayashan Guruge | 08 XGBoost, 11 Evaluation + selection | Model strategy and comparison (docs/05, docs/06 §6.4) |
| Hasitha Erandika | 09 SVM, 10 Validation gate, 12 Calibration + threshold, 13 Explainability + fairness, 14 Final test | Framing, workflow, evaluation, recommendation, reproducibility (docs/01, 02, 06, 07, 08), report assembly |

### 4.2 Remaining work by member

| Member | Tasks |
|---|---|
| Bhanuka | Run notebook 03 and 05 §6 (rules in §6); review the reduced-set odds ratios and add them to docs/03 or docs/05 |
| Seneja | Run notebook 04 §4.4; review the screening table and any "candidate to drop" rows; confirm the AI-log row |
| Jayashan | Refresh the notebook 11 chart (rules in §6); add own Codex rows to the AI log; review docs/05 and docs/06 §6.4 |
| Hasitha | Install `shap` and run notebook 13; refresh the charts in 10 and 12; pin `shap`; assemble the report |
| Everyone | Review and explain own notebooks; peer-review one other member's notebook; sign off the final report |

---

## 5. Feature selection: method

Goal: show a clear, repeatable method for which inputs are kept, **without changing the
modelling spec** unless the evidence says so. The spec is already justified by leakage and
timing, and changing it would force a re-run of notebooks 05 to 14, which the test-once
lock forbids for notebook 14.

**Notebook 04, new §4.4 "Statistical feature screening (Train only)"**

1. **Relevance tests** on every candidate input, including engineered ones:
   - Numeric: Mann-Whitney U test (no normality assumption) with rank-biserial effect size.
   - Categorical: chi-square test with bias-corrected Cramér's V.
   - Benjamini-Hochberg correction across all tests.
   - With about 61,000 rows almost everything is significant, so the decision uses
     **effect size**, not the p-value. Weak = |rank-biserial| < 0.05 and V < 0.05.
2. **Mutual information** on the full candidate list (raw and engineered).
3. **Redundancy:** VIF on the linear numeric block and an exact-identity check
   (the three sums in A-04). Flag VIF > 10.
4. **Decision table** (`reports/tables/04_feature_screening.csv`): feature, test, p (adjusted),
   effect size, MI, VIF, decision (keep / keep for trees only / exclude), reason.
5. **Charts:** effect size vs MI scatter coloured by decision, and a VIF bar chart.

**Notebook 05, new §6 "Sensitivity checks"**

- Reduced linear set (drop the raw parts of the three sums): CV PR-AUC compared with
  the full set. If within 1 SD, the odds ratios from the reduced model are the ones to
  quote. Logged as decision #31.
- L1-penalised LR (`saga`) to show which inputs shrink to zero (embedded selection).

Tree models keep the full set: redundant inputs do not hurt their accuracy, and
permutation importance (07, 13) already shows which inputs they rely on.

---

## 6. How to run the new cells (and keep the Test lock valid)

Notebook 14 checks that the policy, the final model and the gate report are exactly what
it locked. Some cells rewrite those files. `models/*.joblib` is git-ignored, so a
rewritten model **cannot be restored from git**. Run only what this table says.

| Notebook | Run | Do not run | Why |
|---|---|---|---|
| 03 | Everything | | Writes report figures and tables only |
| 04 | Sections 1 to 4 (includes the new §4.4) | Section 6 | §6 rewrites the feature files, templates and feature spec |
| 05 | Sections 1 and 2, then the new §6 | Sections 3, 4 and 5 | §3 and §4 rewrite the saved models and model cards; §5 needs §4 |
| 10 | Sections 1 to 5 (includes the new chart) | Section 6 | §6 rewrites the gate report |
| 11 | Sections 1 to 9 | Section 10 | §10 rewrites `model_selection.json` |
| 12 | Sections 1 to 5 | Section 6 | §6 rewrites the policy and `final_model_calibrated.joblib` |
| 13 | Everything (after `pip install shap`) | | Writes report figures and tables only |
| 14 | Nothing | Everything | Test is scored once; the lock is already written |

After running, `git status artifacts/` should show no changes. If it does, restore them
with `git checkout -- artifacts/` before committing.

**Phases**

| Phase | Work | Status |
|---|---|---|
| 1. Integrity | A-01, A-02, A-12 | Done, except the members' own AI-log rows |
| 2. Evidence | A-03, A-04, A-09, A-10 | Done |
| 3. Polish | A-05, A-06, A-07, A-11, A-13 | Done |
| 4. Report | A-14 | Open |

---

## 7. Future work (not for this submission)

Carried from the old roadmap: shared tested package (F-01), MLflow tracking (F-02),
`country` ablation (F-03, partly covered by A-10), time-aware CV (F-04), per-hotel
thresholds (F-05), target encoding in CV (F-06), `papermill` + CI run (F-07),
`pre-commit` with `nbstripout` (F-08), drift monitoring design (F-09), Markdown model
card (F-10).
