# AI Usage Log: Bhanuka Samarasinghe (Member 1)

Role: Data Engineering + EDA Lead. Owns notebooks 01, 03, 05 and 13. See
[`../docs/team/member-1-bhanuka-samarasinghe.md`](../docs/team/member-1-bhanuka-samarasinghe.md).

## Tool used

**Antigravity** (AI coding agent). Used for code drafting, debugging and explanations in
this member's areas. Policy: [`README.md`](README.md).

## Session log

| Date | Tool / Model | Purpose | Prompt (summary) | Output used? | Verification performed | Notes |
|---|---|---|---|---|---|---|
| 2026-09-15 | Antigravity | Code drafting: data ingestion, cleaning, schema checks and first EDA notebook | Generate data ingestion, cleaning and schema validation code, and initial EDA notebook cells | Yes: `src/data/*.py` and `notebooks/01_data_quality_eda.ipynb` (commit `1eba6c0`) | Ran the code on the real CSV; schema assertions passed; leakage crosstab showed 0 mismatches between `reservation_status` and `is_canceled` | This first version was replaced on 2026-10-11 by the notebook-only pipeline (decision #24). Its cleaning rules and leakage proof carried over into notebook 01. |

## Note on the initial docs scaffold

The starting structure of `docs/03-data-understanding.md` and
`docs/team/member-1-bhanuka-samarasinghe.md` was drafted with Claude Code on 2026-09-12
(logged in [`member-4-hasitha-erandika.md`](member-4-hasitha-erandika.md)). Every
statistic in `docs/03` was later checked against the data by notebook 01 (20 of 20
matched on 2026-10-11).
