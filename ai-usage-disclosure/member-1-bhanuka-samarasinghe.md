# AI Usage Log — Bhanuka Samarasinghe (Member 1)

Role: Data Engineering + EDA Lead, Logistic Regression. See
[`../docs/team/member-1-bhanuka-samarasinghe.md`](../docs/team/member-1-bhanuka-samarasinghe.md).

> This file is a personal, per-session log. Add a row every time you use an AI
> tool for this project's work — see [`README.md`](README.md) for the policy and
> [`ai-usage-log-template.md`](ai-usage-log-template.md) for the field guide.
> Do not leave this file as just the template — an empty log at submission time
> reads as either "no AI was used" (state that explicitly if true) or
> "undisclosed use" (which the rubric penalises); make it accurate one way or
> the other.

| Date | Tool / Model | Purpose | Prompt (summary) | Output used? | Verification performed | Notes |
|---|---|---|---|---|---|---|
| 2026-09-15 | Antigravity AI Agent | Data engineering boilerplate & EDA notebook setup | Generate modular data ingestion, cleaning, schema validation scripts, and initial EDA notebook cells | Yes | Tested via Python execution (`src.data` test suite and schema assertions) | Generated `src/data/ingestion.py`, `src/data/cleaning.py`, `src/data/validation.py`, and `notebooks/01_data_quality_eda.ipynb` |

## Note on the initial docs scaffold

The starting structure of `docs/03-data-understanding.md` and
`docs/team/member-1-bhanuka-samarasinghe.md` was drafted by Claude Code on
2026-09-12 as part of whole-project scaffolding (logged in
[`member-4-hasitha-erandika.md`](member-4-hasitha-erandika.md)). When you
(Bhanuka) start the actual EDA/data-quality notebook, re-verify every statistic
in `03-data-understanding.md` yourself against the real data rather than
trusting the draft — record that verification as your own log entry above, and
correct the doc plus add a `DECISIONS.md` entry if anything doesn't match.
