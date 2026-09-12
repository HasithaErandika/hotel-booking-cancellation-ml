# 2. Workflow Diagram and Architecture

*Rubric: 10 marks — Integration; Learning How to Learn | Reasoning; communication*

This file is the single source of truth for how the project is structured end to
end. The **decision log with options/reasons/evidence lives in
[`../DECISIONS.md`](../DECISIONS.md)** — this file shows the *shape* of the
workflow; `DECISIONS.md` shows *why* each stage was built the way it was.

## 2.1 End-to-end workflow: business problem → recommendation

```mermaid
flowchart TD
    A[Business problem:\ncan we flag high-risk\nbookings at booking time?] --> B[Data understanding\n+ data quality audit]
    B --> C[Exploratory data analysis\nEDA Insight Log]
    C --> D[Leakage audit\nreservation_status excluded]
    D --> E[Preprocessing\nmissing values, duplicates,\noutliers, encoding]
    E --> F[Feature engineering\ntotal_nights, total_guests,\nprior-cancellation rate]
    F --> G[Train / test split\nstratified on is_canceled]
    G --> H[Baseline: Dummy Classifier]
    G --> I[Model 1: Logistic Regression]
    G --> J[Model 2: Decision Tree]
    G --> K[Model 3: Random Forest]
    G --> L[Model 4: XGBoost / Gradient Boosting]
    H --> M[Evaluation framework\nCV, precision/recall, F1,\nROC-AUC, PR-AUC]
    I --> M
    J --> M
    K --> M
    L --> M
    M --> N[Calibration + threshold\nanalysis / cost trade-off]
    N --> O[Explainability\ncoefficients, feature importance, SHAP]
    O --> P[Business recommendation\n+ limitations + responsible AI]
```

## 2.2 Data pipeline architecture (leakage-safe)

```mermaid
flowchart TD
    RAW[Raw CSV\n119,390 rows x 32 cols] --> SCHEMA[Schema validation\ndtypes, expected categories]
    SCHEMA --> QUALITY[Data quality checks\nmissing values, duplicates,\nimpossible values]
    QUALITY --> CLEAN[Cleaning\ndrop exact duplicates,\nfix invalid category values]
    CLEAN --> LEAK[Leakage audit\ndrop reservation_status,\nreservation_status_date]
    LEAK --> SPLIT{Train / test split\nstratified, random_state=42}
    SPLIT -->|80%| TRAIN[Training set]
    SPLIT -->|20%| TEST[Held-out test set]
    TRAIN --> FIT[Fit feature engineering\n+ preprocessing pipeline\nON TRAIN ONLY]
    FIT --> TRANSFORMED_TRAIN[Transformed train features]
    FIT -.apply learned params\nno refit.-> TRANSFORMED_TEST[Transformed test features]
    TEST --> TRANSFORMED_TEST
    TRANSFORMED_TRAIN --> MODELS[Model training\n+ cross-validation]
    MODELS --> EVAL[Final evaluation\non untouched test set]
    TRANSFORMED_TEST --> EVAL
```

The critical rule enforced by this diagram: **the preprocessing pipeline (imputers,
encoders, scalers) is fit on the training split only**, then applied unchanged to
the test split. This is implemented as a single `sklearn.pipeline.Pipeline` +
`ColumnTransformer` object shared by every model, so no team member can
accidentally fit their own preprocessing on the full dataset.

## 2.3 Team / module ownership architecture

```mermaid
flowchart TD
    subgraph M1["Bhanuka Samarasinghe — Data & EDA"]
        M1A[Ingestion + validation]
        M1B[Data quality report]
        M1C[EDA + EDA Insight Log]
        M1D["Model: Logistic Regression"]
    end
    subgraph M2["Seneja Ramanayake — Features"]
        M2A[Feature engineering]
        M2B[Preprocessing pipeline]
        M2C[Feature Log]
        M2D["Model: Random Forest"]
    end
    subgraph M3["Jayashan Guruge — Advanced modeling"]
        M3A[Hyperparameter search]
        M3B[Cross-validation]
        M3C["Model: XGBoost / Gradient Boosting"]
    end
    subgraph M4["Hasitha Erandika — Validation & Decision Science"]
        M4A[Validation gate: leakage,\nsplit integrity, imbalance]
        M4B[Unified evaluation framework]
        M4C[Calibration + threshold + cost]
        M4D[Explainability]
        M4E[Final recommendation]
    end

    M1D --> M4B
    M2D --> M4B
    M3C --> M4B
    M1C --> M2A
    M2B --> M1D
    M2B --> M2D
    M2B --> M3C
```

Everyone consumes the **same** cleaned dataset (from M1) and the **same**
feature/preprocessing pipeline (from M2) — this prevents the classic group-project
failure mode where each member trains on a slightly different version of the data
and results become incomparable. See
[`team/roles-and-raci.md`](team/roles-and-raci.md) for the full RACI matrix and
per-member deliverables/definition-of-done.

## 2.4 Repository structure

```text
hotel-booking-cancellation-ml/
├── data/
│   └── hotel_bookings.csv                  # raw, untouched — never edited in place
├── docs/                                   # this documentation
│   └── team/
├── ai-usage-disclosure/                    # per-member AI-use logs
├── notebooks/                              # one notebook per pipeline stage/model
├── src/                                    # reusable pipeline code imported by notebooks
├── reports/
│   └── figures/                            # exported charts used in the final report
├── PROGRESS.md                             # live status tracker
└── DECISIONS.md                            # decision log: options, choice, reason, evidence
```

## 2.5 How to use the decision log

Every non-trivial choice referenced in this workflow (how missing values are
treated, which variables are dropped for leakage, which models are compared, which
metric decides the "winner") must have a row in `../DECISIONS.md` with: the
alternatives considered, the choice made, the reason, and the evidence that
supports it. This file is graded directly against rubric criterion 2, so it is not
optional bookkeeping — it is the primary evidence of reasoning.
