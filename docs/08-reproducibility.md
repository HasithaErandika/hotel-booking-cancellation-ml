# 8. Reproducibility, Documentation, and AI-Use Transparency

*Rubric: 10 marks — Learning How to Learn | Professional practice; responsible AI*

## 8.1 Dataset provenance and fingerprint

- **Source:** [Kaggle — Hotel Booking Demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand)
  by Jesse Mostipak, redistributing data originally published in:
  Antonio, N., de Almeida, A., & Nunes, L. (2019). "Hotel booking demand
  datasets." *Data in Brief*, 22, 41–49.
- **Local path:** `data/hotel_bookings.csv` (not committed if the repo has a size
  limit — see `.gitignore` note in §8.4; otherwise tracked as-is since it is the
  canonical input every result depends on).
- **Row/column count:** 119,390 rows × 32 columns.
- **SHA-256 fingerprint:**
  ```
  7c2ae42a7353905ea136e5c2287f17c92c5435826598bfbb8491c6f0c7b1fc06
  ```
  Verify with:
  ```bash
  sha256sum data/hotel_bookings.csv
  ```
  If this hash doesn't match, you have a different version of the file than the
  one all numbers in `docs/` were computed against — re-run the profiling steps in
  `03-data-understanding.md` §3.6 before trusting any figure in this documentation.

## 8.2 Environment and seeds

- Fix `RANDOM_STATE = 42` everywhere: train/test split, cross-validation folds,
  every model's internal random seed, and any resampling (SMOTE, etc.).
- Record exact library versions in `requirements.txt` (created once code starts)
  — at minimum `python`, `pandas`, `numpy`, `scikit-learn`, `xgboost`,
  `matplotlib`/`seaborn`, `shap`.
- Every notebook starts with:
  ```python
  import numpy as np
  RANDOM_STATE = 42
  np.random.seed(RANDOM_STATE)
  ```

## 8.3 Reproducing the whole pipeline

1. `data/hotel_bookings.csv` present and hash-verified (§8.1).
2. Run notebooks in numeric order (`notebooks/01_...` → `notebooks/07_...`) —
   each one imports shared logic from `src/`, it does not redefine its own
   cleaning/feature logic (see `02-workflow-and-architecture.md` §2.4).
3. Outputs (figures, tables, model comparison numbers) written to
   `reports/figures/` and `reports/tables/` must match what's pasted into the
   final report 1:1 — if a notebook is re-run and a number changes, the report
   must be updated, not the other way around.
4. The notebook must run top-to-bottom without manual intervention
   ("Restart Kernel and Run All") before being considered final — this is the
   literal rubric requirement ("notebook runs clearly, outputs match the report").

## 8.4 What is and isn't version-controlled

- `data/hotel_bookings.csv` — tracked (or, if the course/repo has a file-size
  policy against it, documented here as excluded and re-downloadable from the
  Kaggle link above with the fingerprint to verify the exact version used).
- `models/*.pkl` — trained model artifacts, tracked only if small; otherwise
  regenerable from the notebooks and excluded via `.gitignore`.
- `docs/`, `ai-usage-disclosure/`, `PROGRESS.md`, `DECISIONS.md` — always tracked;
  these are graded documentation, not build artifacts.

## 8.5 AI-use transparency

Full, per-member logs of how and why generative AI tools were used are kept in
[`../ai-usage-disclosure/`](../ai-usage-disclosure/), not summarised away here.
Policy summary:

> Generative AI tools were used as a supporting tool for tasks such as
> brainstorming the business-problem framing, explaining statistical/ML concepts,
> scaffolding documentation structure, drafting boilerplate code, and assisting
> with debugging. All dataset analysis, actual model training, interpretation of
> results, and final conclusions were reviewed and validated by the team member
> responsible for that section before being included in the project. AI-generated
> suggestions were treated as a draft or a second opinion, never as evidence or a
> finding in their own right without independent verification against the actual
> data or code output.

Each member's individual log (what tool, what for, what was verified) is required
under [`../ai-usage-disclosure/ai-usage-log-template.md`](../ai-usage-disclosure/ai-usage-log-template.md)
and must be kept current throughout the project, not written retroactively at
submission time.
