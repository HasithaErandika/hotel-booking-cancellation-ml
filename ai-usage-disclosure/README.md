# AI-Use Disclosure

*Rubric alignment: Reproducibility, documentation, and AI-use transparency (10 marks)*

This folder is the project's honest record of **where, why, and how** generative
AI tools (e.g. ChatGPT, Claude/Claude Code, GitHub Copilot) were used, by whom,
and what was independently verified before being trusted. It exists so the
marker doesn't have to guess how much of the work is AI-assisted — we say it
directly, per person, with dates.

## Why we're disclosing this way (not just one blanket statement)

A single "we used AI" sentence at the end of a report can't show *what* was
actually delegated to a model versus done and checked by a human. Four people
used AI differently and for different parts of the pipeline, so each member
keeps their own log:

- [`member-1-bhanuka-samarasinghe.md`](member-1-bhanuka-samarasinghe.md)
- [`member-2-seneja-ramanayake.md`](member-2-seneja-ramanayake.md)
- [`member-3-jayashan-guruge.md`](member-3-jayashan-guruge.md)
- [`member-4-hasitha-erandika.md`](member-4-hasitha-erandika.md)

Each log follows [`ai-usage-log-template.md`](ai-usage-log-template.md).

## Team policy on AI use

1. **AI is a drafting/explaining tool, not a source of evidence.** No AI-generated
   claim about the data, a metric, or a model's behaviour is included in the
   report unless it was independently checked against actual code output on the
   real dataset.
2. **No AI-generated numbers go into the report unverified.** If AI is asked to
   estimate what a metric might look like, that estimate is never pasted into
   `docs/06-evaluation-plan.md` or the final report — only numbers produced by
   actually running the code are.
3. **Every use is logged at the time it happens**, not reconstructed from memory
   at submission time. If you used AI and forgot to log it, add the entry as soon
   as you remember and note that it was logged retroactively.
4. **Log the honest purpose.** "Used AI to write my entire section" and "used AI
   to explain what PR-AUC means before I computed it myself" are both fine to
   disclose — the point is accuracy, not minimising AI use for appearances.
5. **Code and prose suggested by AI are reviewed by the responsible member**
   before being committed — the member whose section it is remains accountable
   for correctness, not the AI tool.

## What "verification performed" means in the log

For each logged use, state concretely what was checked, e.g.:
- "Ran the suggested pandas code on the actual CSV and confirmed the printed
  counts matched what's in `docs/03-data-understanding.md`."
- "Cross-checked the explanation of PR-AUC against the scikit-learn
  documentation before using it in the report."
- "Reviewed the generated function line-by-line, tested it on a small sample of
  rows, and adjusted the missing-value logic to match our actual decision in
  `DECISIONS.md`."

A log entry with no verification statement is treated as incomplete — add one
before submission.
