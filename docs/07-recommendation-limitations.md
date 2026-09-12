# 7. Recommendation, Limitations, and Stakeholder Value

*Rubric: 10 marks — Integration; Human Dimension; Caring | Communication; human-centred AI*

This file is finalised **last**, after `06-evaluation-plan.md` has real numbers.
The structure below is fixed now so the team writes toward it; do not fabricate
conclusions before the models are actually trained and evaluated.

## 7.1 Recommendation template

> The analysis shows that cancellation risk can be estimated using information
> available at [booking time / re-score time — state which variant won, see
> `05-modeling-strategy.md` §5.3], with [final model] providing the best balance of
> [PR-AUC / recall at the chosen threshold] and interpretability among the models
> compared (`06-evaluation-plan.md` §6.4). We recommend the reservations team use
> the model's output as a **3-tier risk score (Low / Medium / High)** — not a hard
> accept/reject decision — to prioritise limited staff time on monitoring and
> follow-up for the highest-risk bookings, particularly around [state the
> segment(s) found most informative, e.g. Non Refund deposits, high lead time,
> repeat-cancellation guests — from `03-data-understanding.md` §3.5].

## 7.2 Stakeholder value

- **Reservations manager:** a ranked worklist instead of treating all bookings
  equally, focusing follow-up effort on the ~30-40% of bookings that carry most of
  the cancellation risk.
- **Revenue management:** a defensible, evidence-based input (not guesswork) for
  overbooking-allowance and deposit-policy decisions.
- **Front office / operations:** earlier visibility into likely no-shows/cancellations
  supports staffing and room-allocation planning.

## 7.3 Limitations

- **Historical, not current data.** Bookings span 2015-2017 for two specific
  hotels; guest behaviour, distribution channels, and pricing have likely shifted
  since. The model should be re-validated on recent data before real deployment,
  not assumed to generalise indefinitely.
- **Two hotels only.** One City Hotel, one Resort Hotel — findings may not
  transfer to hotels of a different size, market, or region.
- **No causal claims.** Associations found (e.g. `deposit_type`, prior
  cancellations) are *correlational*. In particular, the `Non Refund` →
  99.36%-cancellation relationship (§3.5) is almost certainly confounded by
  booking channel/process, not a simple causal effect of the deposit policy
  itself — this must not be reported as "changing deposit policy will change
  cancellation rates" without further evidence.
- **Missing real-world variables.** No data on price competitiveness, weather,
  local events, guest income, or actual reason for cancellation — the model can
  only use what's in this table.
- **Errors are inevitable.** False positives and false negatives will occur at
  whatever operating threshold is chosen (§6.5); the report states the measured
  rates at the recommended threshold rather than implying the model is exact.
- **Threshold is a business judgement, not a statistical fact.** The
  precision/recall trade-off point recommended in `06-evaluation-plan.md` §6.5
  rests on an illustrative cost assumption the project states explicitly — the
  hotel should confirm or adjust it against real operational costs.

## 7.4 Risks and responsible-use guardrails

- **Fairness:** `country` and `agent`/`company` correlate with guest nationality
  and booking channel; a risk score should never be used to justify differential
  treatment of guests by nationality. Error rates should be checked across
  `country` and `market_segment` groups before deployment (extend §6.6's error
  analysis), and any large disparity reported as a limitation, not hidden.
- **Transparency:** front-office staff should be able to see the top factors
  behind a given booking's score (via the explainability work in
  `06-evaluation-plan.md`), not just a bare number.
- **Human oversight:** the score supports a human decision (follow-up call,
  monitoring) — it must not automatically cancel, upcharge, or deny a booking.
- **Privacy:** the public dataset already has guest-identifying information
  removed; a real deployment on live guest data would need its own data-governance
  and consent review, which is out of scope for this academic project but is
  flagged here so it isn't silently assumed away.
