# AI-Use Disclosure

*Rubric alignment: Reproducibility, documentation, and AI-use transparency (10 marks)*

This folder is the project's honest record of **where, why, and how** generative AI
tools were used, by whom, and what was checked before it was trusted.

## Contribution statement

All four members contributed equally to this project. Each member owns one model, at
least one shared pipeline stage and one part of the report (see
[`../docs/team/roles-and-raci.md`](../docs/team/roles-and-raci.md)).

## AI tools used, by member

| Member | Tool | Main use | Log |
|---|---|---|---|
| Bhanuka Samarasinghe | Antigravity | Data ingestion, quality audit and EDA code; logistic regression | [member-1-bhanuka-samarasinghe.md](member-1-bhanuka-samarasinghe.md) |
| Seneja Ramanayake | Antigravity | Train/Dev/Test split and preprocessing pipeline code; tree models | [member-2-seneja-ramanayake.md](member-2-seneja-ramanayake.md) |
| Jayashan Guruge | Codex | XGBoost tuning; model evaluation and threshold work | [member-3-jayashan-guruge.md](member-3-jayashan-guruge.md) |
| Hasitha Erandika | Claude Code | Documentation scaffold, the notebook-only rebuild (notebooks 01 to 14), validation, final audit | [member-4-hasitha-erandika.md](member-4-hasitha-erandika.md) |

The current notebooks 01 to 14 were rebuilt with Claude Code on 2026-10-11, starting
from the members' earlier notebooks (data quality and EDA by Bhanuka, split and
preprocessing by Seneja). Each owner then reviewed their notebooks against the outputs.
The details are in each member's log.

Each log follows [`ai-usage-log-template.md`](ai-usage-log-template.md).

## Team policy on AI use

1. **AI is a drafting and explaining tool, not a source of evidence.** No AI claim about
   the data, a metric or a model goes into the report unless it was checked against real
   code output on the real dataset.
2. **No AI-generated numbers go into the report unchecked.** Only numbers produced by
   running the notebooks are reported, and each one traces to a file in
   `reports/tables/`.
3. **Every use is logged.** If an entry is added late, the log says so.
4. **Log the honest purpose.** "AI wrote the first version of this notebook" and "AI
   explained PR-AUC" are both fine to disclose. The point is accuracy.
5. **The responsible member reviews AI code and text** before it is committed, and stays
   accountable for its correctness.

## What "verification performed" means in the log

For each logged use, state concretely what was checked, for example:
- "Ran the notebook on the team kernel and confirmed the printed counts match
  `docs/03-data-understanding.md`."
- "Checked the explanation of PR-AUC against the scikit-learn documentation."
- "Read the generated function line by line, tested it on a few rows, and changed the
  missing-value logic to match `DECISIONS.md`."

A log entry with no verification statement is incomplete.
