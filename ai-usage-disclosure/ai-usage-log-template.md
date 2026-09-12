# AI Usage Log — Template

Copy this table format into your personal log file. Add one row **per session or
per distinct use**, not one row per project. Keep it current — log as you go.

| Date | Tool / Model | Purpose | Prompt (summary, not full transcript) | Output used? | Verification performed | Notes |
|---|---|---|---|---|---|---|
| YYYY-MM-DD | e.g. Claude Code (Sonnet 5) | e.g. Explain difference between ROC-AUC and PR-AUC | "Asked for a plain-language explanation of PR-AUC vs ROC-AUC under class imbalance" | Explanation used in docs/06-evaluation-plan.md §6.2 | Cross-checked definition against scikit-learn docs before writing it into the report | — |

## Field guide

- **Tool / Model** — name the actual product and, if known, the model (e.g.
  "ChatGPT (GPT-4o)", "Claude Code (Sonnet 5)", "GitHub Copilot"). Don't write
  just "AI."
- **Purpose** — one of: brainstorming/framing, concept explanation, code
  drafting, debugging help, documentation scaffolding, writing/editing prose,
  reviewing own work. Be specific, not "general help."
- **Prompt (summary)** — a short paraphrase of what was asked, enough for a
  reader to understand the scope of the request. Do not paste sensitive data or
  full raw output.
- **Output used?** — where exactly it landed: a file + section, or "not used, we
  discarded the suggestion." "Not used" is a legitimate, useful log entry too.
- **Verification performed** — required for anything used in the report/code.
  See `README.md` "What 'verification performed' means."
- **Notes** — anything unusual: e.g. "AI's first suggestion was wrong (it assumed
  no leakage columns), corrected manually."

## What must be logged

- Any AI help drafting or debugging code that ends up in `src/` or `notebooks/`.
- Any AI help drafting documentation text (including if a whole doc's structure
  was AI-scaffolded, like the initial `docs/` skeleton for this project).
- Any AI explanation of a statistical/ML concept that informed a decision in
  `DECISIONS.md`.
- Any AI-assisted debugging of an error or unexpected result.

## What does not need a row

- Autocomplete-level suggestions inside an IDE that a human immediately reviews
  and are equivalent to standard tooling (e.g. simple syntax completion) — use
  judgement, but when in doubt, log it.
