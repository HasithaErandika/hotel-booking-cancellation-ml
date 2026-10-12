# Plan: Final Audit, Gap Fixes and Submission

> Status: **active** · Last revised: 2026-10-12 · Replaces the 2026-10-11 plan
> (notebook-only pipeline), which is finished. The old plan is kept in git history
> at commit `02cc61a`.

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
| Preprocessing and feature engineering | 15 | Notebook 04, feature spec, feature log, leakage variants, imbalance, ADR cap, unseen-category test | Partial | No explicit **feature selection** step and perfect collinearity in the linear inputs. SMOTE promised but not run. A-03, A-04, A-08 |
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

| # | Sev | Gap | Evidence | Fix |
|---|---|---|---|---|
| A-01 | High | **AI-use disclosure was incomplete.** Member 2 and 3 logs were empty templates, member 4's log stopped at 2026-09-12, and member 1's log described removed `src/` files. | `ai-usage-disclosure/*.md`, commit `677280f` | **Partly done 2026-10-12:** equal-contribution statement and tools (Bhanuka and Seneja: Antigravity, Jayashan: Codex, Hasitha: Claude Code) added to the disclosure README and `docs/08` section 8.5; Hasitha's Claude Code sessions logged. **Still open:** Seneja confirms the prompt for her 2026-09-16 row; Jayashan adds his Codex session rows. |
| A-02 | High | **Workload was unequal on paper.** Notebooks per owner: Bhanuka 3, Seneja 4, Jayashan 1, Hasitha 6. | `docs/team/roles-and-raci.md` | Team states equal contribution (disclosure README). Rebalance ownership (section 4) and update the RACI and team docs to match. |
| A-03 | High | **No explicit feature-selection step.** Notebook 03 ranks features (MI, Cramér's V, Spearman) but no rule turns the ranking into keep or drop. No significance tests. MI does not cover the 9 engineered features. Selection today is only by leakage and timing, which is valid but not shown as a method. | Notebook 03 §12, notebook 04 §4.1 | Add a statistical screening section to notebook 04 (§5 below). |
| A-04 | High | **Perfect collinearity in the linear inputs.** `total_nights = weekend + week nights`, `total_guests = adults + children + babies`, `total_previous_bookings = previous_cancellations + previous_bookings_not_canceled`. All six raw parts and three totals go into Logistic Regression and SVM. L2 keeps the fit stable, but the **odds ratios of these features cannot be read one by one** (for example `previous_cancellations` shows OR 0.96, which looks protective). | `reports/tables/05_logreg_day_zero_odds_ratios.csv` | VIF check in 04. Caveat in notebook 05 §5. Reduced-set LR as a sensitivity check (§5). |
| A-05 | Medium | Notebook 10 has no chart (every other notebook has at least one). | Notebook outline | Add a heatmap of the per-model check matrix (PASS / WARN / FAIL). |
| A-06 | Medium | Notebook 11 §11 and notebook 13 §7 still say "fill in after running". | Notebooks 11, 13 | Fill with the real numbers (already in `docs/06` and `docs/07`). |
| A-07 | Medium | Figure fixes. `11_cv_pr_auc_comparison`: rows not sorted by score (SVM 0.677 drawn below LR 0.651) and SVM subsample not marked. `12_threshold_analysis`: legend sits on the "No model" line and the `t = 0.35` label touches the axis. `13_fairness_country`: "flag" labels overlap the overall line, and "Honouring guests" is unclear (use "Guests who stayed"). `03_mutual_information`: does not mark which features were later excluded. | `reports/figures/` | Fix in the notebooks and re-save. See §6 for which notebooks are safe to re-run. |
| A-08 | Medium | Decision #7 says SMOTE is "kept as a documented comparison", but SMOTE was never run. | `docs/DECISIONS.md` #7, grep of notebooks | Either run SMOTE inside CV in notebook 05 (`imblearn` Pipeline, LR day-zero only) or add decision #31 that amends #7. Running it is better evidence. |
| A-09 | Medium | SHAP was skipped because `shap` is not installed in the team kernel. | `docs/DECISIONS.md` #30 | `pip install shap`, re-run notebook 13 (Dev only, Test stays locked). |
| A-10 | Medium | Fairness audit flags 8 of 11 country groups. With small groups, many gaps may be noise. | `reports/tables/13_fairness_audit.csv` | Add bootstrap CIs on group TPR and FPR. Flag only when the CI excludes the overall rate. Keep the original table for transparency. |
| A-11 | Low | `requirements.txt` has `appnope` (macOS only) and an unpinned `shap`. | `requirements.txt` | Pin from the Python 3.11 team kernel (`pip freeze`), drop `appnope`. Old F-11. |
| A-12 | Low | Stale text: "proposed decision #23" in the feature spec and feature log, `src/features/` in member 2's AI log, unchecked DoD boxes in `docs/team/*.md` for finished work. | grep | Small text fixes. |
| A-13 | Low | No one-page problem framing canvas. | Core evidence list | Add a canvas table at the top of `docs/01`. |
| A-14 | Medium | Final report not assembled. | `docs/PROGRESS.md` | Assemble from docs 01 to 08; every number must trace to `reports/tables/`. |

---

## 4. Fair split of ownership and remaining work

### 4.1 Notebook ownership (rebalanced)

| Member | Notebooks owned | Report sections owned | Count |
|---|---|---|---|
| Bhanuka Samarasinghe | 01 Data quality, 03 EDA, 05 Baselines + LR, 13 Explainability + fairness | Data understanding (docs/03) | 4 |
| Seneja Ramanayake | 02 Split, 04 Features + preprocessing, 06 Decision Tree, 07 Random Forest | Preprocessing and features (docs/04) | 4 |
| Jayashan Guruge | 08 XGBoost, 11 Evaluation + selection, 12 Calibration + threshold | Model strategy and evaluation (docs/05, docs/06) | 3 + 2 docs |
| Hasitha Erandika | 09 SVM, 10 Validation gate, 14 Final test | Framing, workflow, recommendation, reproducibility (docs/01, 02, 07, 08), report assembly | 3 + 4 docs |

Why this split: notebook 13 depends on Bhanuka's country and LR work, notebooks 11 and
12 build on Jayashan's CV and tuning work, and the validation gate and final test stay
with the validation lead. Each member now owns one model and at least one shared stage.

### 4.2 Remaining work by member

| Member | Tasks |
|---|---|
| Bhanuka | A-04 caveat + reduced-set LR in 05 · A-08 SMOTE check in 05 · A-09 SHAP in 13 · A-10 fairness CIs in 13 · A-06 fill 13 §7 · A-07 MI chart and fairness chart fixes |
| Seneja | A-03 statistical feature screening in 04 (§5) · VIF check · update docs/04 §4.5 and feature log · A-12 feature-spec wording |
| Jayashan | A-06 fill 11 §11 · A-07 sort and mark the CV chart (11), fix threshold chart (12) · review docs/05 and docs/06 against the tables |
| Hasitha | A-05 chart in 10 · A-13 framing canvas · A-11 requirements · A-12 team DoD boxes · A-01 own AI log + docs/08 §8.5 · A-14 report assembly · update RACI, team docs and PROGRESS for §4.1 |
| Everyone | Review and explain own notebooks · fill own AI-use log honestly (A-01) · peer-review one other member's notebook · sign off the final report |

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

**Notebook 05, new §5.3 "Sensitivity checks"**

- Reduced linear set (drop the raw parts of the three sums): CV PR-AUC compared with
  the full set. If within 1 SD, the odds ratios from the reduced model are the ones to
  quote. Logged as decision #31.
- L1-penalised LR (`saga`) to show which inputs shrink to zero (embedded selection).
- SMOTE inside CV, for decision #7.

Tree models keep the full set: redundant inputs do not hurt their accuracy, and
permutation importance (07, 13) already shows which inputs they rely on.

---

## 6. Order of work and re-run rules

**Re-run rule.** Notebook 14 checks that the policy, the final model and the gate report
match what it locked. Re-running 10, 11 or 12 rewrites those files (new timestamps, new
hashes), so 14 would refuse to run. That is by design. Therefore:

- Safe to re-run: 01 to 09 only if their outputs do not change the feature files or
  model files used downstream. 03, 04 (new sections only), 05 (new sections), 13 are safe.
- For 10, 11, 12: edit only the chart and text cells, and re-run them on a scratch branch
  to save the figures. Then restore `artifacts/` with `git checkout -- artifacts/` before
  committing, so the locked hashes stay valid. Notebook 10 may need the same treatment.
- Never re-run 14 against Test. If a change truly needs a new Test score, record it as a
  new decision and say so in the report.

**Phases**

| Phase | Work | Done when |
|---|---|---|
| 1. Integrity | A-01, A-02, A-12: AI logs, ownership docs, stale text | Every member log has real rows or an explicit "no AI used" line |
| 2. Evidence | A-03, A-04, A-08, A-09, A-10 | New tables and figures saved; decisions #31 and up logged |
| 3. Polish | A-05, A-06, A-07, A-11, A-13 | Every notebook has a chart, no "fill in" cells, figures re-saved |
| 4. Report | A-14 | Report numbers match `reports/tables/`; peer review signed |

---

## 7. Future work (not for this submission)

Carried from the old roadmap: shared tested package (F-01), MLflow tracking (F-02),
`country` ablation (F-03, partly covered by A-10), time-aware CV (F-04), per-hotel
thresholds (F-05), target encoding in CV (F-06), `papermill` + CI run (F-07),
`pre-commit` with `nbstripout` (F-08), drift monitoring design (F-09), Markdown model
card (F-10).
